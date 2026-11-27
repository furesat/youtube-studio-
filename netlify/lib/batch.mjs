import { z } from "zod";
import catalog from "../../engine/tools/opportunity_engine/catalog_v2.json" with { type: "json" };
import { env, ResearchError } from "./research.mjs";

export const discoveryCatalog = catalog;
const marketIds = catalog.markets.map(m => m.id);
const categoryIds = catalog.categories.map(c => c.id);
const phrase = z.string().trim().min(1).max(160).regex(/^[^\u0000-\u001f\u007f]+$/u);
export const batchSchema = z.strictObject({
  label: phrase.optional(),
  mode: z.enum(["discovery","bulk"]),
  markets: z.array(z.enum(marketIds)).max(marketIds.length).optional(),
  countries: z.array(z.string().regex(/^[A-Z]{2}$/)).max(36).optional(),
  languages: z.array(z.enum(Object.keys(catalog.languages))).max(23).optional(),
  categories: z.array(z.enum(categoryIds)).max(categoryIds.length).optional(),
  topics: z.array(z.strictObject({topic:phrase,queries:z.record(z.enum(Object.keys(catalog.languages)),phrase)})).max(500).optional(),
});
export function planBatch(input) {
  const parsed = batchSchema.safeParse(input);
  if (!parsed.success) throw new ResearchError(400,"Toplu araştırma girdisi geçersiz.");
  const x = parsed.data;
  const markets = catalog.markets.filter(m => (!x.markets?.length || x.markets.includes(m.id))
    && (!x.countries?.length || x.countries.includes(m.region))
    && (!x.languages?.length || x.languages.includes(m.language)));
  if (!markets.length) throw new ResearchError(400,"Eşleşen pazar bulunamadı.");
  const topics = x.mode === "discovery"
    ? catalog.categories.filter(c => !x.categories?.length || x.categories.includes(c.id)).map(c => ({topic:c.label,queries:c.queries}))
    : x.topics ?? [];
  if (!topics.length) throw new ResearchError(400,"En az bir konu gerekli.");
  const tasks = [], missing = [], seen = new Set();
  for (const topic of topics) for (const m of markets) {
    const query = topic.queries[m.language];
    if (!query) {missing.push({topic:topic.topic,language:m.language,market_id:m.id});continue;}
    const key = JSON.stringify([query.normalize("NFC").trim(),m.region,m.language]);
    if (seen.has(key)) continue;
    seen.add(key);
    tasks.push({topic:topic.topic,query:query.normalize("NFC"),region:m.region,language:m.language,market_id:m.id});
  }
  if (!tasks.length || tasks.length > 10000) throw new ResearchError(400,"Görev sayısı 1–10.000 olmalı; eksik yerelleştirmeleri tamamlayın.");
  return {label:x.label ?? (x.mode === "discovery" ? "Pazar keşfi" : "Toplu araştırma"),tasks,missing};
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
  const id=await db("rpc/fasulye_enqueue",{method:"POST",body:{p_label:plan.label,p_tasks:plan.tasks},fetcher});
  if (typeof id!=="string" || !/^[0-9a-f-]{36}$/i.test(id)) throw new ResearchError(502,"Kuyruk kimliği alınamadı.");
  return {id,status:"queued",tasks:plan.tasks.length,missing:plan.missing};
}
export async function listBatches(fetcher=fetch) {
  return db("fasulye_batches?select=id,label,created_at&order=created_at.desc&limit=50",{fetcher});
}
export async function batchStatus(id,fetcher=fetch) {
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) throw new ResearchError(400,"Geçersiz grup kimliği.");
  return db("rpc/fasulye_batch_status",{method:"POST",body:{p_batch_id:id},fetcher});
}
export async function queueBudget(fetcher=fetch) {
  const rows=await db("fasulye_queue_budget?select=day,reserved&order=day.desc&limit=7",{fetcher});
  return {daily_limit:30,reservations:rows,scope:"Fasulye Actions rezervasyonları; Google Cloud proje kotası değildir."};
}
