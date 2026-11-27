import { z } from "zod";
import { db } from "./batch.mjs";
import { ResearchError } from "./research.mjs";

const editions=["tr","de","en","nl","pl","cs","ro","sv","no","da","fi","fr","it","es","pt","ja","ko","hi","bn","id","vi","ar","hu"];
const language=z.enum(editions);
const text=z.string().trim().min(1).max(160).regex(/^[^\u0000-\u001f\u007f]+$/u);
const day=z.iso.date();
export const wikiSearchSchema=z.strictObject({language,query:text});
export const wikiCollectSchema=z.strictObject({language,topic:text,page_id:z.number().int().positive().max(2147483647),start:day,end:day});
export const wikiListSchema=z.strictObject({offset:z.number().int().min(0).max(1000000).default(0),limit:z.number().int().min(1).max(50).default(20)});
const UA="FasulyeOpportunityEngine/4.0 (https://github.com/furesat/youtube-studio-)";
const limitations="Wikipedia language edition, worldwide user pageviews; not national readership, unique people, YouTube demand or search volume. Missing days are unknown.";
function parse(schema,input){const r=schema.safeParse(input);if(!r.success)throw new ResearchError(400,"Wikimedia giriş alanları geçersiz.");return r.data;}
function wikiUrl(lang,params){return "https://"+lang+".wikipedia.org/w/api.php?"+new URLSearchParams({action:"query",format:"json",formatversion:"2",...params});}
async function wikiJson(url,fetcher){
 let res;
 try{res=await fetcher(url,{headers:{"User-Agent":UA,Accept:"application/json"},redirect:"error",signal:AbortSignal.timeout(8000)});}
 catch{throw new ResearchError(502,"Wikimedia bağlantısı kurulamadı.");}
 if(res.status===429)throw new ResearchError(429,"Wikimedia istek sınırı; daha sonra yeniden deneyin.");
 if(res.status===404)throw new ResearchError(404,"Wikimedia verisi bulunamadı; sıfır olarak kaydedilmedi.");
 if(!res.ok)throw new ResearchError(502,"Wikimedia veri isteği başarısız.");
 try{const p=await res.json();if(!p||typeof p!=="object"||p.error)throw new Error();return p;}
 catch{throw new ResearchError(502,"Wikimedia yanıtı geçersiz.");}
}
export async function searchWiki(input,fetcher=fetch){
 const x=parse(wikiSearchSchema,input);
 const p=await wikiJson(wikiUrl(x.language,{list:"search",srsearch:x.query,srnamespace:"0",srlimit:"10",srprop:"timestamp"}),fetcher);
 const rows=p.query?.search;
 if(!Array.isArray(rows)||rows.some(r=>!r||!Number.isSafeInteger(r.pageid)||r.pageid<=0||typeof r.title!=="string"))throw new ResearchError(502,"Wikimedia arama yanıtı geçersiz.");
 return {language:x.language,query:x.query,results:rows.map(r=>({page_id:r.pageid,title:r.title,last_edited_at:r.timestamp??null,url:"https://"+x.language+".wikipedia.org/?curid="+r.pageid})),has_more:!!p.continue,limitations:"Article candidates only; manually select the intended subject. Search hits are not a demand measure."};
}
function dateWindow(start,end,now){
 const a=Date.parse(start+"T00:00:00Z"),b=Date.parse(end+"T00:00:00Z");
 const lastComplete=new Date(now).toISOString().slice(0,10);
 if(!Number.isFinite(a)||!Number.isFinite(b)||new Date(a).toISOString().slice(0,10)!==start||new Date(b).toISOString().slice(0,10)!==end||start<"2015-07-01"||end>=lastComplete||b<a||b-a>=90*86400000)throw new ResearchError(400,"Geçmişte kalan en fazla 90 günlük geçerli dönem seçin.");
 return Array.from({length:(b-a)/86400000+1},(_,i)=>new Date(a+i*86400000).toISOString().slice(0,10));
}
export function normalizePageviews(payload,days,project,title){
 if(!Array.isArray(payload?.items))throw new ResearchError(502,"Sayfa görüntüleme yanıtı geçersiz.");
 const seen=new Map(),allowed=new Set(days);
 for(const r of payload.items){
  const stamp=r?.timestamp;
  if(typeof stamp!=="string"||!/^\d{10}$/.test(stamp)||!stamp.endsWith("00")||!Number.isSafeInteger(r.views)||r.views<0||r.project!==project||r.article!==title||r.access!=="all-access"||r.agent!=="user"||r.granularity!=="daily")throw new ResearchError(502,"Sayfa görüntüleme gözlemi geçersiz.");
  const date=stamp.slice(0,4)+"-"+stamp.slice(4,6)+"-"+stamp.slice(6,8);
  if(!allowed.has(date)||seen.has(date))throw new ResearchError(502,"Beklenmeyen veya tekrarlı gözlem.");
  seen.set(date,r.views);
 }
 return days.map(date=>({date,views:seen.get(date)??null}));
}
export class WikimediaProvider{
 constructor(fetcher=fetch,now=()=>new Date()){this.fetcher=fetcher;this.now=now;}
 async collect(input){
  const x=parse(wikiCollectSchema,input),now=this.now(),days=dateWindow(x.start,x.end,now);
  const meta=await wikiJson(wikiUrl(x.language,{pageids:String(x.page_id),prop:"info|pageprops",ppprop:"disambiguation",inprop:"url",redirects:"1"}),this.fetcher);
  const rows=meta.query?.pages;
  if(!Array.isArray(rows)||rows.length!==1)throw new ResearchError(502,"Wikimedia sayfa kimliği doğrulanamadı.");
  const page=rows[0];
  if(page.missing||page.ns!==0||page.pageid!==x.page_id||typeof page.title!=="string"||!page.title)throw new ResearchError(400,"Geçerli, yönlendirme olmayan bir makale seçin.");
  if(Object.hasOwn(page.pageprops??{},"disambiguation"))throw new ResearchError(400,"Anlam ayrımı sayfası; gerçek makaleyi seçin.");
  const article=page.title.replaceAll(" ","_"),project=x.language+".wikipedia";
  const url="https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+project+"/all-access/user/"+encodeURIComponent(article)+"/daily/"+x.start.replaceAll("-","")+"/"+x.end.replaceAll("-","");
  const raw=await wikiJson(url,this.fetcher);
  const series=normalizePageviews(raw,days,project,article);
  return {provider:"wikimedia_pageviews",topic:x.topic,language:x.language,region:null,project,page_id:x.page_id,article_title:page.title,article_url:"https://"+x.language+".wikipedia.org/?curid="+x.page_id,source_url:url,retrieved_at:now.toISOString(),period_start:x.start,period_end:x.end,evidence_type:"general_public_interest",methodology:"per-article daily / all-access / user / worldwide",license:"CC0-1.0",limitations,series};
 }
}
export async function collectWiki(input,fetcher=fetch,now=()=>new Date()){
 const record=await new WikimediaProvider(fetcher,now).collect(input);
 const rows=await db("fasulye_wikimedia_evidence?on_conflict=topic,project,page_id,period_start,period_end",{method:"POST",body:record,prefer:"resolution=merge-duplicates,return=representation",fetcher});
 if(!rows?.[0]?.id)throw new ResearchError(502,"Wikimedia kanıtı kaydedilemedi.");
 return rows[0];
}
export async function listWiki(input={},fetcher=fetch,now=new Date()){
 const {offset,limit}=parse(wikiListSchema,input);
 const rows=await db("fasulye_wikimedia_evidence?"+new URLSearchParams({select:"*",order:"retrieved_at.desc,id.desc",offset:String(offset),limit:String(limit+1)}),{fetcher});
 if(!Array.isArray(rows))throw new ResearchError(502,"Kanıt listesi geçersiz.");
 return {records:rows.slice(0,limit).map(r=>({...r,freshness:Date.parse(r.retrieved_at)<now.getTime()-30*86400000?"stale":"recently_retrieved"})),next_offset:rows.length>limit?offset+limit:null};
}
