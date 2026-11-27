import { z } from "zod";
import { db, discoveryCatalog } from "./batch.mjs";
import { ResearchError } from "./research.mjs";

const text=z.string().trim().min(1).max(160);
const source=z.string().trim().min(1).max(1000);
const region=z.string().regex(/^[A-Z]{2}$/);
const language=z.enum(Object.keys(discoveryCatalog.languages));
const market=z.enum(discoveryCatalog.markets.map(m=>m.id));
const format=z.enum(["long_form","shorts"]);
const money=z.number().finite().min(0).max(10000000);
const factor=z.number().finite().min(0).max(100).nullable().optional();
export const factorWeights={demand:.2,gap:.2,competition:.15,revenue:.15,cost:.1,cultural_fit:.1,long_term:.1};
export const evidenceSchema=z.discriminatedUnion("kind",[
  z.strictObject({kind:z.literal("trend"),topic:text,region,language,source,csv:z.string().min(1).max(300000)}),
  z.strictObject({kind:z.literal("rpm"),market_id:market,format,currency:z.string().regex(/^[A-Z]{3}$/),low:z.number().finite().min(0).max(1000000),base:z.number().finite().min(0).max(1000000),high:z.number().finite().min(0).max(1000000),source,source_date:z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),reliability:z.enum(["unspecified","third_party_sample","third_party_model","owner_actual","user_assumption"]).optional()}),
  z.strictObject({kind:z.literal("cost"),market_id:market,format,currency:z.string().regex(/^[A-Z]{3}$/),voice:money,visuals:money,translation:money,editing:money,other:money,source}),
  z.strictObject({kind:z.literal("review"),topic:text,market_id:market,source,factors:z.strictObject(Object.fromEntries(Object.keys(factorWeights).map(k=>[k,factor])))}),
]);
export function scoreIndependent(factors) {
  let total=0,coverage=0;
  for(const [key,weight] of Object.entries(factorWeights)) {
    const value=factors[key];
    if(value===null||value===undefined)continue;
    if(typeof value!=="number"||!Number.isFinite(value)||value<0||value>100)throw new ResearchError(400,"Geçersiz değerlendirme.");
    coverage+=weight;total+=weight*(["competition","cost"].includes(key)?100-value:value);
  }
  return {score:coverage+1e-10>=.75?Math.round(total/coverage*100)/100:null,coverage:Math.round(coverage*100)/100,coverage_band:coverage+1e-10>=.9?"high":coverage+1e-10>=.75?"medium":"low",confidence:null,statistical_confidence:null,basis:"independent_user_inputs"};
}
export function profitScenarios(row,cost) {
  const total=cost&&cost.currency===row.currency?["voice","visuals","translation","editing","other"].reduce((sum,k)=>sum+Number(cost[k]),0):null;
  return revenueScenarios(row).map(s=>({...s,production_cost:total,break_even_views:total===null?null:Object.fromEntries(["low","base","high"].map(k=>[k,total===0?0:Number(row[k])>0?Math.ceil(total*1000/Number(row[k])):null])),profit:total===null?null:Object.fromEntries(["low","base","high"].map(k=>[k,Math.round((s[k]-total)*100)/100]))}));
}
export function revenueScenarios(row) {
  return [10000,100000,1000000,10000000].map(views=>({views,format:row.format,currency:row.currency,source:row.source,...Object.fromEntries(["low","base","high"].map(k=>[k,Math.round(Number(row[k])*views/1000*100)/100]))}));
}
function csvRows(csv) {
  const rows=[];let row=[],cell="",quoted=false;
  for(let i=0;i<csv.length;i++){
    const ch=csv[i];
    if(ch==='"'){if(quoted&&csv[i+1]==='"'){cell+='"';i++;}else quoted=!quoted;}
    else if(!quoted&&ch===","){row.push(cell.trim());cell="";}
    else if(!quoted&&(ch==="\r"||ch==="\n")){if(ch==="\r"&&csv[i+1]==="\n")i++;row.push(cell.trim());if(row.some(Boolean))rows.push(row);row=[];cell="";}
    else cell+=ch;
  }
  if(quoted)throw new ResearchError(400,"CSV tırnakları geçersiz.");
  row.push(cell.trim());if(row.some(Boolean))rows.push(row);
  return rows;
}
function dateKey(raw) {
  if(!/^\d{4}-\d{2}(-\d{2})?$/.test(raw))return null;
  const day=raw.length===7?raw+"-01":raw;
  const d=new Date(day+"T00:00:00Z");
  return Number.isNaN(d.getTime())||d.toISOString().slice(0,10)!==day?null:day;
}
export class CsvTrendProvider {
  name="google_trends_csv";
  parse(csv) {
    const rows=csvRows(csv.replace(/^\uFEFF/,""));
    const first=rows.findIndex(r=>dateKey(r[0]));
    if(first<1||rows[first-1].length!==2)throw new ResearchError(400,"Tek sorgulu Google Trends zaman serisi CSV'si gerekli.");
    const seen=new Set(),series=[];
    for(const row of rows.slice(first)){
      const date=dateKey(row[0]),raw=row[1];
      if(!date||row.length!==2||!(/^(?:[0-9]{1,2}|100|<1)$/.test(raw??""))||seen.has(date))throw new ResearchError(400,"CSV tarihleri veya 0–100 değerleri geçersiz/tekrarlı.");
      seen.add(date);series.push({date,label:row[0],value:raw==="<1"?null:Number(raw),below_one:raw==="<1"});
    }
    if(series.length>10000)throw new ResearchError(400,"En fazla 10.000 gözlem.");
    return series.sort((a,b)=>a.date.localeCompare(b.date));
  }
}
export class GoogleTrendsApiProvider {
  name="google_trends_api";
  constructor(adapter=null){this.adapter=adapter;}
  status(){return this.adapter?"configured":"awaiting_approved_api_access";}
  async fetch(input){if(!this.adapter)throw new ResearchError(503,"Google Trends Alpha erişimi henüz yapılandırılmadı.");return this.adapter(input);}
}
export async function writeEvidence(input,fetcher=fetch) {
  const parsed=evidenceSchema.safeParse(input);
  if(!parsed.success)throw new ResearchError(400,"Kaynak veya veri alanları geçersiz.");
  const {kind,...row}=parsed.data;
  if(kind==="trend"){
    const provider=new CsvTrendProvider(),series=provider.parse(row.csv);
    const {csv,...meta}=row;
    const saved=await db("fasulye_trend_series",{method:"POST",body:{...meta,provider:provider.name,period_start:series[0].date,period_end:series.at(-1).date,series},prefer:"return=representation",fetcher});
    return {kind,id:saved?.[0]?.id,points:series.length};
  }
  if(kind==="rpm"&&!(row.low<=row.base&&row.base<=row.high))throw new ResearchError(400,"RPM düşük ≤ orta ≤ yüksek olmalı.");
  if(kind==="review"&&!Object.values(row.factors).some(v=>v!=null))throw new ResearchError(400,"En az bir bağımsız değerlendirme gerekli.");
  if(kind==="rpm"&&row.source_date&&dateKey(row.source_date)!==row.source_date)throw new ResearchError(400,"Kaynak tarihi geçersiz.");
  const table=kind==="rpm"?"fasulye_rpm_assumptions":kind==="cost"?"fasulye_production_costs":"fasulye_independent_reviews";
  const conflict=kind==="review"?"topic,market_id":"market_id,format";
  if(kind==="rpm"){row.reliability=row.reliability??"user_assumption";row.source_date=row.source_date??null;row.source_checked_at=null;}
  const saved=await db(table+"?on_conflict="+conflict,{method:"POST",body:{...row,updated_at:new Date().toISOString()},prefer:"resolution=merge-duplicates,return=representation",fetcher});
  return {kind,saved:saved?.[0]??null};
}
export async function getEvidence(fetcher=fetch) {
  const [trends,rpm,reviews,costs]=await Promise.all([
    db("fasulye_trend_series?select=id,topic,region,language,provider,source,period_start,period_end&order=created_at.desc&limit=100",{fetcher}),
    db("fasulye_rpm_assumptions?select=*&order=market_id&limit=100",{fetcher}),
    db("fasulye_independent_reviews?select=*&order=updated_at.desc&limit=100",{fetcher}),
    db("fasulye_production_costs?select=*&order=market_id&limit=100",{fetcher}),
  ]);
  return {trends,costs,rpm:rpm.map(r=>({...r,scenarios:profitScenarios(r,costs.find(c=>c.market_id===r.market_id&&c.format===r.format))})),reviews:reviews.map(r=>({...r,...scoreIndependent(r.factors)})),trend_api:new GoogleTrendsApiProvider().status(),search_volume:null};
}
export async function getTrend(id,fetcher=fetch) {
  if(!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id))throw new ResearchError(400,"Geçersiz seri kimliği.");
  const rows=await db("fasulye_trend_series?select=*&id=eq."+id,{fetcher});
  if(!rows.length)throw new ResearchError(404,"Trend serisi bulunamadı.");
  return rows[0];
}
