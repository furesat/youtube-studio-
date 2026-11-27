import { timingSafeEqual } from "node:crypto";
import yauzl from "yauzl";
import { z } from "zod";
import catalog from "../../engine/tools/opportunity_engine/config.json" with { type: "json" };

const repo = "furesat/youtube-studio-";
const workflow = "fasulye-opportunity.yml";
const apiRoot = `https://api.github.com/repos/${repo}/actions`;
const artifactName = "fasulye-opportunity-report";
const maxBytes = 3_000_000;
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
    signal: AbortSignal.timeout(12_000),
  });
}

export async function startResearch(input, fetcher = fetch) {
  const parsed = startSchema.safeParse(input);
  if (!parsed.success) throw new ResearchError(400, "Sorgu, konu veya pazar girdisi geçersiz.");
  const { query, region, language, topics, markets } = parsed.data;
  const inputs = query ? { query, region: region ?? "TR", language: language ?? "tr" } : {
    topics: [...new Set(topics)].join(","), markets: [...new Set(markets)].join(","),
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

async function boundedBytes(response) {
  if (!response.body) throw new ResearchError(502, "GitHub rapor arşivi boş.");
  const reader = response.body.getReader();
  const parts = [];
  let length = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) return Buffer.concat(parts, length);
      length += value.byteLength;
      if (length > maxBytes) {
        await reader.cancel();
        throw new ResearchError(413, "Rapor büyük. Tam arşivi GitHub Actions üzerinden indirin.");
      }
      parts.push(value);
    }
  } finally {
    reader.releaseLock();
  }
}

export async function getArtifact(id, fetcher = fetch) {
  const run = await getRun(id, fetcher);
  if (run.status !== "completed") throw new ResearchError(409, "Araştırma devam ediyor.");
  const response = await github(`/runs/${id}/artifacts`, {}, fetcher);
  if (!response.ok) throw new ResearchError(502, "GitHub rapor listesi okunamadı.");
  const { artifacts } = await response.json();
  const artifact = artifacts.find(item => item.name === artifactName && !item.expired);
  if (!artifact) throw new ResearchError(404, "İndirilebilir rapor arşivi bulunamadı. Arşiv yüklenememiş veya saklama süresi dolmuş olabilir.");
  if (artifact.size_in_bytes > maxBytes) {
    throw new ResearchError(413, "Rapor büyük. Tam arşivi GitHub Actions üzerinden indirin.");
  }
  const download = await github(`/artifacts/${artifact.id}/zip`, { redirect: "manual" }, fetcher);
  if (download.status !== 302 || !download.headers.has("location")) {
    throw new ResearchError(502, "GitHub rapor indirme bağlantısını döndürmedi.");
  }
  const url = new URL(download.headers.get("location"));
  if (url.protocol !== "https:") throw new ResearchError(502, "Rapor bağlantısı geçersiz.");
  const bytes = await fetcher(url, { signal: AbortSignal.timeout(12_000), redirect: "error" });
  if (!bytes.ok) throw new ResearchError(502, "GitHub arşivi indirilemedi.");
  return boundedBytes(bytes);
}

export async function reportFromZip(zip) {
  const file = await yauzl.fromBufferPromise(zip);
  try {
    for await (const entry of file.eachEntry()) {
      if (entry.fileName !== "report.json") continue;
      if (entry.uncompressedSize > maxBytes) throw new ResearchError(413, "JSON raporu çok büyük.");
      const stream = await file.openReadStreamPromise(entry);
      const parts = [];
      for await (const piece of stream) parts.push(piece);
      const report = JSON.parse(Buffer.concat(parts).toString("utf-8"));
      if (report.schema_version !== 1 || !Array.isArray(report.opportunities)) break;
      return report;
    }
  } finally {
    file.close();
  }
  throw new ResearchError(502, "Arşivde okunabilir JSON raporu yok.");
}
