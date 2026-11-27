import { z } from "zod";
import { db,discoveryCatalog } from "./batch.mjs";
import { env,ResearchError } from "./research.mjs";
import { searchWiki } from "./wikimedia.mjs";
const languages=Object.keys(discoveryCatalog.languages);
const lang=z.enum(languages), market=z.enum(discoveryCatalog.markets.map(m=>m.id));
const phrase=z.string().trim().min(1).max(160).regex(/^[^\u0000-\u001f\u007f]+$/u);
export const templates={
 everyday:["Gündelik nesneler","Tarihi ev eşyaları","Historische Alltagsgegenstände","History of household objects"],
 history:["Tuhaf tarih","Tarihteki sıra dışı olaylar","Kuriose historische Ereignisse","Unusual historical events"],
 professions:["Unutulan meslekler","Kaybolan meslekler","Historische Berufe","Obsolete occupations"],
 companies:["Şirket başarısızlıkları","Tarihi şirket iflasları","Historische Unternehmensinsolvenzen","Historical business failures"],
 inventions:["İcatlar","İcatların tarihi","Geschichte der Erfindungen","History of inventions"],
 psychology:["Psikoloji","Psikoloji deneyleri","Psychologische Experimente","Psychology experiments"],
 geography:["Coğrafya","Sınır anomalileri","Geographische Grenzanomalien","Geographical border anomalies"],
 culture:["Kültürel farklar","Geleneklerin tarihi","Geschichte der Bräuche","History of cultural customs"],
 laws:["Tuhaf yasalar","Tarihi yasaklar","Historische Verbote","Historical prohibitions"],
 science:["Bilimsel keşifler","Bilim tarihindeki keşifler","Wissenschaftsgeschichte Entdeckungen","History of scientific discoveries"],
 mystery:["Tarihsel gizemler","Çözülememiş tarihsel olaylar","Ungeklärte historische Ereignisse","Unsolved historical events"],
 archives:["Eski gazeteler","Tarihi gazete arşivleri","Historische Zeitungsarchive","Historical newspaper archives"],
 economics:["Ekonomi tarihi","Ekonomik balonların tarihi","Geschichte der Spekulationsblasen","History of economic bubbles"],
 events:["Gerçek olaylar","Tarihte belgelenmiş olaylar","Dokumentierte historische Ereignisse","Documented historical events"]
};
export const discoveryPlanSchema=z.strictObject({categories:z.array(z.enum(Object.keys(templates))).min(1).max(6),languages:z.array(lang).min(1).max(6),interest_hypothesis:z.enum(["emerging","evergreen","seasonal","uncertain"]).default("uncertain")});
export const evidenceMapSchema=z.strictObject({topic:phrase,markets:z.array(market).min(1).max(12),localized:z.partialRecord(lang,z.array(phrase).min(1).max(4)).optional()});
function validated(schema,input){const r=schema.safeParse(input);if(!r.success)throw new ResearchError(400,"Keşif / pazar alanları geçersiz.");return r.data;}
export function planIndependent(input){
 const x=validated(discoveryPlanSchema,input),queries=[],missing=[];
 for(const category of new Set(x.categories))for(const language of new Set(x.languages)){
  const [label,tr,de,en]=templates[category];
  const native={tr,de,en}[language];
  const fallback=discoveryCatalog.campaign.categories.find(c=>c.id===category)?.queries[language]?.[0]??discoveryCatalog.categories.find(c=>c.id===category)?.queries[language];
  const query=native??fallback;
  if(query)queries.push({category,label,language,query,query_basis:native?"independent_wiki_template":"existing_localized_catalog_expression"});
  else missing.push({category,language});
 }
 return {queries,missing,interest_hypothesis:x.interest_hypothesis,interest_verified:false,limits:"Templates and search expressions are hypotheses, not observed trends. No YouTube requests."};
}
export async function discoverIndependent(input,fetcher=fetch){
 if(env("FASULYE_WIKIMEDIA_EVIDENCE")!=="1")throw new ResearchError(503,"Wikimedia kanıt modülü henüz etkin değil.");
 const plan=planIndependent(input);
 if(!plan.queries.length||plan.queries.length>6)throw new ResearchError(400,"Her keşif isteğinde 1-6 yerelleştirilmiş arama seçin.");
 const observations=[];
 for(const item of plan.queries){
  try{const r=await searchWiki({language:item.language,query:item.query},fetcher);observations.push({...item,status:"observed",articles:r.results,has_more:r.has_more});}
  catch(e){observations.push({...item,status:"unavailable",articles:null,error:e instanceof ResearchError?e.message:"Provider unavailable"});if(e.status===429)break;}
 }
 return {...plan,observations,unattempted:plan.queries.slice(observations.length),limitations:"Manually verify article relevance and originality. Search hits do not establish demand, trend growth or market gaps."};
}
export async function crossLanguageEvidence(input,fetcher=fetch,now=new Date()){
 const x=validated(evidenceMapSchema,input),markets=discoveryCatalog.markets.filter(m=>x.markets.includes(m.id));
 const known=discoveryCatalog.topics.find(t=>t.id===x.topic||t.label===x.topic||t.aliases.includes(x.topic));
 const topic=known?.label??x.topic;
 const q=(fields,extra={})=>new URLSearchParams({select:fields,topic:"eq."+topic,...extra,limit:"101"});
 const requests=[
  db("fasulye_trend_series?"+q("id,topic,region,language,provider,source,created_at,period_start,period_end",{order:"created_at.desc"}),{fetcher}),
  db("fasulye_independent_reviews?"+q("topic,market_id,factors,source,updated_at",{order:"updated_at.desc"}),{fetcher}),
  env("FASULYE_WIKIMEDIA_EVIDENCE")==="1"?db("fasulye_wikimedia_evidence?"+q("id,topic,language,article_title,article_url,retrieved_at,period_start,period_end,source_url,methodology,limitations",{order:"retrieved_at.desc"}),{fetcher}):Promise.resolve(null),
  db("fasulye_editorial_candidates?"+new URLSearchParams({select:"id,title,market_id,hypothesis,narrative_angle,uncertainty,sources,updated_at",title:"eq."+topic,order:"updated_at.desc",limit:"101"}),{fetcher})
 ];
 const results=await Promise.allSettled(requests),keys=["trends","reviews","wikimedia","editorial"];
 const providers=Object.fromEntries(results.map((r,i)=>[keys[i],r.status==="rejected"?{status:"unavailable",rows:null}:r.value===null?{status:"disabled",rows:null}:{status:"available",rows:r.value.slice(0,100),truncated:r.value.length>100}]));
 const recent=(value)=>{const age=Math.floor((now.getTime()-Date.parse(value))/86400000);return Number.isFinite(age)?{age_days:age,review_due:age>90}:null;};
 return {topic,requested_topic:x.topic,markets:markets.map(m=>({...m,
  local_expressions:x.localized?.[m.language]??(known?.queries[m.language]?[known.queries[m.language]]:[]),
  trends:providers.trends.rows?.filter(r=>r.region===m.region&&r.language===m.language).map(r=>({...r,freshness:recent(r.created_at),measure:"normalized_search_interest"}))??null,
  worldwide_language_interest:providers.wikimedia.rows?.filter(r=>r.language===m.language).map(r=>({...r,freshness:recent(r.retrieved_at),region:null,measure:"worldwide_language_edition_pageviews"}))??null,
  manual_reviews:providers.reviews.rows?.filter(r=>r.market_id===m.id).map(r=>({...r,freshness:recent(r.updated_at)}))??null,
  editorial_angles:providers.editorial.rows?.filter(r=>r.market_id===m.id).map(r=>({...r,freshness:recent(r.updated_at)}))??null,
  youtube_demand:null,competition_gap:null})),
  providers:Object.fromEntries(Object.entries(providers).map(([k,{rows,...meta}])=>[k,meta])),
  limitations:["Exact topic labels only; local expressions require semantic review.","Wikipedia language readership is not country readership.","Normalized Trends series from different requests are not directly comparable in level.","Missing evidence is unknown; no cross-market score or automatic conclusion."]};
}
