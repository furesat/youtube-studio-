import { timingSafeEqual } from "node:crypto";
import { z } from "zod";
import catalog from "../../engine/tools/opportunity_engine/config.json" with { type: "json" };

const repo = "furesat/youtube-studio-";
const workflow = "fasulye-opportunity.yml";
const apiRoot = `https://api.github.com/repos/${repo}/actions`;
const ids = z.string().regex(/^[1-9]\d{0,15}$/);

export const startSchema = z.strictObject({
  query: z.string().trim().min(1).max(160).regex(/^[^\u0000-\u001F\u007F]+$/u).optional(),
  region: z.string().regex(/^[A-Z]{2}$/).optional(),
  language: z.string().regex(/^(?:[a-z]{2}|zh-Hans|zh-Hant)$/).optional(),
  topics: z.array(z.enum(catalog.topics.map(({ id }) => id))).max(catalog.topics.length).optional(),
  markets: z.array(z.enum(catalog.markets.map(({ id }) => id))).max(catalog.markets.length).optional(),
}).refine(value => value.query ? !value.topics?.length && !value.markets?.length :
  !value.region && !value.language, "Manuel sorgu ile hazır konu/pazar seçimini ayrı kullanın.");

export const publicCatalog = {
  topics: catalog.topics.map(({ id, label }) => ({ id, label })),
  markets: catalog.markets.map(({ id, label, language, region }) => ({ id, label, language, region })),
};
export const readSchema = ids;

export class ResearchError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

export function env(name) {
  return globalThis.Netlify?.env.get(name) ?? process.env[name];
}

export function readBearer(request) {
  return request.headers.get("authorization")?.match(/^Bearer ([^\s]+)$/i)?.[1];
}

export function acceptsToken(token) {
  const expected = env("FASULYE_ACCESS_TOKEN");
  if (!expected || !token) return false;
  const a = Buffer.from(token);
  const b = Buffer.from(expected);
  return a.length === b.length && timingSafeEqual(a, b);
}

export function json(body, status = 200, headers = {}) {
  return Response.json(body, {
    status,
    headers: { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", ...headers },
  });
}

export function errorResponse(error) {
  if (error instanceof ResearchError) return json({ error: error.message }, error.status);
  return json({ error: "Araştırma servisine şu anda ulaşılamıyor." }, 502);
}

export function trustedOrigin(request) {
  const origin = request.headers.get("origin");
  return origin === null || origin === new URL(request.url).origin;
}

async function github(path, request = {}, fetcher = fetch) {
  const token = env("FASULYE_GITHUB_TOKEN");
  if (!token) throw new ResearchError(503, "GitHub bağlantısı Netlify'da yapılandırılmalı.");
  return fetcher(apiRoot + path, {
    ...request,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2026-03-10",
      ...request.headers,
    },
    redirect: "error", signal: AbortSignal.timeout(12_000),
  });
}

export async function startResearch(input, fetcher = fetch) {
  const parsed = startSchema.safeParse(input);
  if (!parsed.success) throw new ResearchError(400, "Sorgu, konu veya pazar girdisi geçersiz.");
  const { query, region, language, topics, markets } = parsed.data;
  const inputs = query ? { query, region: region ?? "TR", language: language ?? "tr" } : {
    topics: [...new Set(topics ?? [])].join(","), markets: [...new Set(markets ?? [])].join(","),
  };
  const response = await github(`/workflows/${workflow}/dispatches`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ref: "main", inputs }),
  }, fetcher);
  if (response.status === 404) {
    throw new ResearchError(503, "GitHub iş akışı main dalında bulunamadı veya erişim yetkisi eksik.");
  }
  if (!response.ok) throw new ResearchError(502, `GitHub araştırmayı başlatamadı (HTTP ${response.status}).`);
  const body = response.status === 200 ? await response.json() : {};
  const id = String(body.workflow_run_id ?? "");
  if (!ids.safeParse(id).success) {
    throw new ResearchError(502, "GitHub çalıştırma kimliğini döndürmedi. Yeniden göndermeden önce Actions sayfasını kontrol edin.");
  }
  return { id, status: "queued", url: `https://github.com/${repo}/actions/runs/${id}` };
}

export async function getRun(id, fetcher = fetch) {
  if (!ids.safeParse(id).success) throw new ResearchError(400, "Çalıştırma numarası geçersiz.");
  if (/^9\d{15}$/.test(id)) {
    const rows = await supabase("fasulye_runs", {select:"run_id,collected_at",run_id:"eq."+id,limit:"1"}, fetcher);
    if (!rows.length) throw new ResearchError(404,"Yerel araştırma bulunamadı.");
    return {id,status:"completed",conclusion:null,started_at:rows[0].collected_at,url:null,source:"standalone"};
  }
  const response = await github(`/runs/${id}`, {}, fetcher);
  if (response.status === 404) throw new ResearchError(404, "Araştırma bulunamadı.");
  if (!response.ok) throw new ResearchError(502, "GitHub çalıştırma durumu okunamadı.");
  const run = await response.json();
  if (run.path?.split("@")[0] !== ".github/workflows/" + workflow) {
    throw new ResearchError(404, "Fasulye araştırması bulunamadı.");
  }
  return {
    id, status: run.status, conclusion: run.conclusion, started_at: run.created_at,
    url: `https://github.com/${repo}/actions/runs/${id}`,
  };
}

const projectUrl = "https://niihqywncuwxfxipkgte.supabase.co";
async function supabase(table, params, fetcher = fetch) {
  const url = (env("SUPABASE_URL") ?? projectUrl).replace(/\/$/, "");
  const key = env("SUPABASE_SECRET_KEY") ?? "";
  if (url !== projectUrl || !key.startsWith("sb_secret_")) {
    throw new ResearchError(503, "Supabase sunucu bağlantısı yapılandırılmalı.");
  }
  const response = await fetcher(url + "/rest/v1/" + table + "?" + new URLSearchParams(params), {
    headers: { apikey: key, Accept: "application/json" },
    redirect: "error", signal: AbortSignal.timeout(12_000),
  });
  if (!response.ok) throw new ResearchError(502, "Supabase raporu okunamadı.");
  return response.json();
}
export async function getReport(id, fetcher = fetch) {
  const run = await getRun(id, fetcher);
  if (run.status !== "completed") throw new ResearchError(409, "Araştırma devam ediyor.");
  const rows = await supabase("fasulye_reports", {
    select: "report,expires_at", run_id: "eq." + id, expires_at: "gt." + new Date().toISOString(), limit: "1",
  }, fetcher);
  if (!rows.length) throw new ResearchError(404, "Rapor kaydedilmemiş veya 30 günlük süresi dolmuş.");
  const report = rows[0].report;
  if (report?.schema_version !== 1 || !Array.isArray(report.opportunities)) throw new ResearchError(502, "Rapor biçimi geçersiz.");
  for(const row of report.opportunities)row.sample_total_known_views=null;
  if(rows[0].expires_at)report.expires_at=rows[0].expires_at;
  return report;
}
export async function getHistory(fetcher = fetch) {
  return supabase("fasulye_runs", {select:"run_id,attempt,collected_at,context",order:"collected_at.desc",limit:"50"},fetcher);
}

export async function startQueueWorker(fetcher=fetch) {
  const response=await github(`/workflows/${workflow}/dispatches`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({ref:"main",inputs:{queue:"true"}})},fetcher);
  if(!response.ok)throw new ResearchError(502,"Kuyruk worker başlatılamadı; zamanlanmış işlem çalışacak.");
  const result=response.status===200?await response.json():{};
  const id=String(result.workflow_run_id??"");
  return {state:"dispatched",run_id:ids.safeParse(id).success?id:null};
}
export async function listReportVideos(id,{offset=0,limit=50,region,language,sort="views",max_subscribers}={},fetcher=fetch) {
  if(!Number.isInteger(offset)||offset<0||!Number.isInteger(limit)||limit<1||limit>100)throw new ResearchError(400,"Geçersiz sayfalama.");
  const report=await getReport(id,fetcher);
  const rows=report.opportunities.filter(r=>(!region||r.region===region)&&(!language||r.language===language));
  const keys=[...new Set(rows.flatMap(r=>r.video_ids))];
  const videos=keys.map(k=>report.videos[k]).filter(v=>v&&(max_subscribers==null||v.subscribers!=null&&v.subscribers<=max_subscribers));
  videos.sort((a,b)=>sort==="subscribers"?(a.subscribers??Infinity)-(b.subscribers??Infinity):sort==="date"?String(b.published_at??"").localeCompare(String(a.published_at??"")):(b.views??-1)-(a.views??-1));
  return {run_id:id,collected_at:report.collected_at,total_sample:videos.length,offset,limit,videos:videos.slice(offset,offset+limit).map(v=>({...v,url:"https://www.youtube.com/watch?v="+encodeURIComponent(v.video_id)}))};
}
