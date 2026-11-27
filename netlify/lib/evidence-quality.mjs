import { z } from "zod";
import { ResearchError } from "./research.mjs";
const note=z.string().trim().min(1).max(1600);
const url=z.url().max(1500).refine(raw=>{try{const u=new URL(raw);return u.protocol==="https:"&&!u.username&&!u.password&&!/(^|\.)(youtube\.com|youtu\.be|googlevideo\.com|youtube-nocookie\.com|ytimg\.com|googleapis\.com)$/.test(u.hostname.toLowerCase().replace(/\.$/,""));}catch{return false;}});
export const evidenceTypes=["general_interest","search_interest","youtube_demand","historical_context","market_coverage","editorial_fit"];
export const evidenceQualitySchema=z.strictObject({
 topic:note, hypothesis:note,
 sources:z.array(z.strictObject({url,publisher:note,checked_on:z.iso.date(),type:z.enum(evidenceTypes),
  credibility:z.enum(["primary","secondary","unverified"]),independence_group:note,
  direction:z.enum(["supports","contradicts","neutral","unknown"]),finding:note,methodology:note,limitations:note,
  region:z.string().regex(/^[A-Z]{2}$/).nullable(),language:z.string().regex(/^[a-z]{2}(?:-[A-Za-z]+)?$/).nullable(),license:note.nullable()
 })).max(40)
});
export function assessEvidence(input, now=new Date()){
 const parsed=evidenceQualitySchema.safeParse(input);
 if(!parsed.success)throw new ResearchError(400,"Kanıt kalite alanları geçersiz.");
 const seen=new Set(), sources=[];
 for(const raw of parsed.data.sources){
  const checked=Date.parse(raw.checked_on+"T00:00:00Z");
  if(checked>now.getTime())throw new ResearchError(400,"Kaynak kontrol tarihi gelecekte olamaz.");
  const u=new URL(raw.url);u.hash="";const normalized=u.href;
  const key=normalized+"|"+raw.type;
  if(seen.has(key))throw new ResearchError(400,"Aynı kaynak ve kanıt türü tekrarlanmış.");
  seen.add(key);
  const age=Math.floor((now.getTime()-checked)/86400000);
  sources.push({...raw,url:normalized,age_days:age,freshness:age>90?"review_due":"recently_checked"});
 }
 const types=Object.fromEntries(evidenceTypes.map(type=>{
  const items=sources.filter(s=>s.type===type);
  return [type,{coverage:items.length?"documented":"unknown",sources:items.length,
   independence_groups:new Set(items.map(s=>s.independence_group.toLowerCase())).size,
   credible_sources:items.filter(s=>s.credibility!=="unverified").length,
   stale_sources:items.filter(s=>s.freshness==="review_due").length,
   contradictions:items.filter(s=>s.direction==="contradicts").map(s=>s.url)}];
 }));
 return {topic:parsed.data.topic,hypothesis:parsed.data.hypothesis,as_of:now.toISOString(),types,sources,
  coverage:{documented:evidenceTypes.filter(t=>types[t].sources>0).length,total:evidenceTypes.length},
  statistical_confidence:null,success_probability:null,
  limitations:["Source quality and independence groups are editor declarations, not automatically verified.","Freshness is time since manual checking, not the age or validity of historical facts.","Wikipedia views and normalized Trends values cannot establish YouTube demand."]};
}
