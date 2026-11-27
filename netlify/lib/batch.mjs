import { z } from "zod";
import { buildControlled } from "./controlled-campaign.mjs";
import catalog from "../../engine/tools/opportunity_engine/catalog_v2.json" with { type: "json" };
import campaign from "../../engine/tools/opportunity_engine/catalog_v3.json" with { type: "json" };
import { env, ResearchError, startQueueWorker } from "./research.mjs";

export const discoveryCatalog = {...catalog,campaign};
const marketIds = catalog.markets.map(m => m.id);
const categoryIds = [...new Set([...catalog.categories,...campaign.categories].map(c => c.id))];
const phrase = z.string().trim().min(1).max(160).regex(/^[^\u0000-\u001f\u007f]+$/u);
export const batchSchema = z.strictObject({
  label: phrase.optional(),
  mode: z.enum(["discovery","bulk","campaign","controlled"]),
  markets: z.array(z.enum(marketIds)).max(marketIds.length).optional(),
  countries: z.array(z.string().regex(/^[A-Z]{2}$/)).max(36).optional(),
  languages: z.array(z.enum(Object.keys(catalog.languages))).max(23).optional(),
  categories: z.array(z.enum(categoryIds)).max(categoryIds.length).optional(),
  lookback_days:z.array(z.union([z.literal(7),z.literal(30),z.literal(90),z.literal(365)])).max(4).optional(),
  orders:z.array(z.enum(["relevance","date","viewCount"])).max(3).optional(),
  comparison_axis:z.enum(["window","order","variant"]).optional(),
  query_variant:z.union([z.literal(0),z.literal(1)]).optional(),
  window_anchor:z.string().datetime({precision:3}).optional(),
  topics: z.array(z.strictObject({topic:phrase,queries:z.partialRecord(z.enum(Object.keys(catalog.languages)),phrase).optional()})).max(500).optional(),
});
export function planBatch(input) {
  const parsed = batchSchema.safeParse(input);
  if (!parsed.success) throw new ResearchError(400,"Toplu araştırma girdisi geçersiz.");
  const x = parsed.data;
  const markets = catalog.markets.filter(m => (!x.markets?.length || x.markets.includes(m.id))
    && (!x.countries?.length || x.countries.includes(m.region))
    && (!x.languages?.length || x.languages.includes(m.language)));
  if (!markets.length) throw new ResearchError(400,"Eşleşen pazar bulunamadı.");
  if(x.mode==="campaign")return planCampaign(x,markets);
  if(x.mode==="controlled"){
    const selected=markets.filter(m=>Boolean(x.markets?.length||x.countries?.length||x.languages?.length)||campaign.priority_markets.includes(m.id));
    const categories=campaign.categories.filter(c=>(x.categories?.length?x.categories:campaign.priority_categories).includes(c.id));
    const anchor=x.window_anchor??new Date(Math.floor(Date.now()/86400000)*86400000).toISOString();
    if(Date.parse(anchor)>Date.now())throw new ResearchError(400,"Gelecekteki pencere tarihi geçersiz.");
    const p=buildControlled(categories,selected,{axis:x.comparison_axis,variant:x.query_variant,anchor});
    if(!p.tasks.length||p.tasks.length>10000)throw new ResearchError(400,"Kontrollü kampanya için geçerli sorgu bulunamadı.");
    return {label:x.label??"4.0 / Kontrollü araştırma",...p};
  }
  const topics = x.mode === "discovery"
    ? catalog.categories.filter(c => !x.categories?.length || x.categories.includes(c.id)).map(c => ({topic:c.label,queries:c.queries}))
    : x.topics ?? [];
  if (!topics.length) throw new ResearchError(400,"En az bir konu gerekli.");
  const normalize = value => value.normalize("NFC").trim().toLocaleLowerCase("tr");
  const tasks = [], missing = [], seen = new Set();
  for (const topic of topics) for (const m of markets) {
    const known = catalog.topics?.find(t => [t.id,t.label,...t.aliases].some(v=>normalize(v)===normalize(topic.topic)));
    const query = topic.queries?.[m.language] ?? known?.queries[m.language];
    if (!query) {missing.push({topic:topic.topic,language:m.language,market_id:m.id});continue;}
    for(const days of x.lookback_days?.length?[...new Set(x.lookback_days)]:[365])for(const order of x.orders?.length?[...new Set(x.orders)]:["relevance"]){
      const key = JSON.stringify([query.normalize("NFC").trim(),m.region,m.language,days,order]);
      if (seen.has(key)) continue;
      seen.add(key);
      tasks.push({topic:topic.topic,query:query.normalize("NFC"),region:m.region,language:m.language,market_id:m.id,lookback_days:days,search_order:order});
    }
  }
  if (!tasks.length || tasks.length > 10000) throw new ResearchError(400,"Görev sayısı 1–10.000 olmalı; eksik yerelleştirmeleri tamamlayın.");
  return {label:x.label ?? (x.mode === "discovery" ? "Pazar keşfi" : "Toplu araştırma"),tasks,missing};
}
export function planCampaign(x,markets){
  const hasSelection=Boolean(x.markets?.length||x.countries?.length||x.languages?.length);
  const selected=markets.filter(m=>hasSelection||campaign.priority_markets.includes(m.id));
  const categories=campaign.categories.filter(c=>(x.categories?.length?x.categories:campaign.priority_categories).includes(c.id));
  const tasks=[],missing=[];
  // Breadth before depth: each window spans category and market before the next window.
  for(const profile of campaign.profiles)for(const category of categories)for(const m of selected){
    const query=category.queries[m.language]?.[profile.variant];
    if(!query){missing.push({topic:category.label,language:m.language,market_id:m.id,lookback_days:profile.days});continue;}
    tasks.push({topic:category.label,query,region:m.region,language:m.language,market_id:m.id,lookback_days:profile.days,search_order:profile.order});
  }
  if(!tasks.length)throw new ResearchError(400,"Bu pazar için 3.0 sorgu profili hazır değil; standart keşfi kullan.");
  return {label:x.label??"3.0 / Dört dönemli pazar keşfi",tasks,missing};
}
export async function db(path,{method="GET",body,fetcher=fetch,prefer}={}) {
  const url = "https://niihqywncuwxfxipkgte.supabase.co";
  const key = env("SUPABASE_SECRET_KEY") ?? "";
  if ((env("SUPABASE_URL") ?? url).replace(/\/$/,"") !== url || !key.startsWith("sb_secret_"))
    throw new ResearchError(503,"Supabase sunucu bağlantısı yapılandırılmalı.");
  const response = await fetcher(url+"/rest/v1/"+path,{method,headers:{apikey:key,"Content-Type":"application/json",Accept:"application/json",...(prefer?{Prefer:prefer}:{})},body:body===undefined?undefined:JSON.stringify(body),redirect:"error",signal:AbortSignal.timeout(12000)});
  if (!response.ok) throw new ResearchError(502,"Supabase kuyruk işlemi başarısız.");
  const raw=await response.text();
  return raw ? JSON.parse(raw) : null;
}
export async function enqueueBatch(input,fetcher=fetch) {
  const plan=planBatch(input);
  if(input.mode==="controlled"&&env("FASULYE_CONTROLLED_CAMPAIGNS")!=="1")throw new ResearchError(503,"Kontrollü kampanya henüz etkin değil.");
  const id=await db(input.mode==="controlled"?"rpc/fasulye_enqueue_controlled":"rpc/fasulye_enqueue",{method:"POST",body:{p_label:plan.label,p_tasks:plan.tasks},fetcher});
  if (typeof id!=="string" || !/^[0-9a-f-]{36}$/i.test(id)) throw new ResearchError(502,"Kuyruk kimliği alınamadı.");
  let worker={state:"scheduled",run_id:null};
  try { worker=await startQueueWorker(fetcher); } catch { /* Durable queue already saved; scheduled worker is fallback. */ }
  return {id,status:"queued",tasks:plan.tasks.length,missing:plan.missing,worker};
}
export async function listBatches(fetcher=fetch) {
  const columns="id,label,created_at"+(env("FASULYE_QUEUE_CONTROLS")==="1"?",paused,priority":"");
  return db("fasulye_batches?select="+columns+"&order=created_at.desc&limit=50",{fetcher});
}
export async function batchStatus(id,fetcher=fetch) {
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) throw new ResearchError(400,"Geçersiz grup kimliği.");
  return db("rpc/fasulye_batch_status",{method:"POST",body:{p_batch_id:id},fetcher});
}
export async function queueBudget(fetcher=fetch) {
  const rows=await db("fasulye_queue_budget?select=day,reserved&order=day.desc&limit=7",{fetcher});
  return {daily_limit:30,reservations:rows,scope:"Fasulye uygulama rezervasyonları; Google Cloud proje kotası değildir."};
}

export async function listBatchTasks(id,offset=0,limit=100,fetcher=fetch) {
  if(!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)||!Number.isInteger(offset)||offset<0||!Number.isInteger(limit)||limit<1||limit>100)throw new ResearchError(400,"Grup veya sayfalama geçersiz.");
  const columns="id,topic,query,region,language,search_order,lookback_days,status,attempts,next_attempt_at,report_run_id,error_code"+(env("FASULYE_QUEUE_CONTROLS")==="1"?",priority,cancel_requested,source_task_id,reused_at,methodology_version,comparison_axis,query_variant,window_anchor":"");
  return db("fasulye_tasks?"+new URLSearchParams({select:columns,batch_id:"eq."+id,order:"id.asc",offset:String(offset),limit:String(limit)}),{fetcher});
}

export async function marketEvidence(id,{topic=null,market=null,days=null,offset=0,limit=50}={},fetcher=fetch){
  if(!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)||!Number.isInteger(offset)||offset<0||!Number.isInteger(limit)||limit<1||limit>100||days!==null&&![7,30,90,365].includes(days)||topic!==null&&(typeof topic!=="string"||topic.length>160)||market!==null&&!marketIds.includes(market))throw new ResearchError(400,"Karşılaştırma filtresi geçersiz.");
  const result=await db("rpc/fasulye_market_evidence",{method:"POST",body:{p_batch_id:id,p_topic:topic,p_market:market,p_days:days,p_offset:offset,p_limit:limit},fetcher});
  if(!result)throw new ResearchError(404,"Araştırma grubu bulunamadı.");
  return result;
}
