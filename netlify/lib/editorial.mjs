import { z } from "zod";
import { db, discoveryCatalog } from "./batch.mjs";
import { ResearchError } from "./research.mjs";

const table = "fasulye_editorial_candidates";
const market = z.enum(discoveryCatalog.markets.map(({ id }) => id));
const status = z.enum(["draft", "researching", "ready", "in_production", "published", "archived"]);
const text = max => z.string().trim().min(1).max(max).regex(/^[^\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]+$/u);
const youtubeDomain = /(?:^|\.)(?:youtube(?:-nocookie|kids|education)?\.[a-z.]+|youtu\.be|ytimg\.com|googlevideo\.com|googleapis\.com)$/i;
const sourceUrl = z.string().trim().max(1500).refine(value => {
  try {
    const url = new URL(value);
    return /^https:\/\//i.test(value) && url.protocol === "https:"
      && !url.username && !url.password && !youtubeDomain.test(url.hostname.replace(/\.$/, ""));
  } catch {
    return false;
  }
}, "Bağımsız bir HTTPS kaynak adresi girin.").transform(value => new URL(value).href)
  .pipe(z.string().max(1500));

const source = z.strictObject({
  publisher: text(120),
  url: sourceUrl,
  checked_on: z.iso.date(),
  kind: z.enum(["demand", "coverage", "context"]),
  finding: text(800),
});

export const candidateSchema = z.strictObject({
  title: text(160),
  market_id: market,
  hypothesis: text(1600),
  narrative_angle: text(1600),
  format: z.enum(["shorts", "long_form", "undecided"]),
  cost: z.strictObject({
    amount: z.number().min(0).max(10000000),
    currency: z.string().regex(/^[A-Z]{3}$/),
    basis: text(400),
  }).nullable(),
  uncertainty: text(1200),
  status,
  sources: z.array(source).max(8),
  independent: z.literal(true),
}).superRefine((candidate, ctx) => {
  if (["ready", "in_production", "published"].includes(candidate.status) && !candidate.sources.length) {
    ctx.addIssue({ code: "custom", path: ["sources"], message: "Bu durum için en az bir bağımsız kaynak gerekli." });
  }
});

export const candidateListSchema = z.strictObject({
  market_id: market.optional(),
  status: status.optional(),
  offset: z.number().int().min(0).max(1000000).default(0),
  limit: z.number().int().min(1).max(20).default(10),
});
export const candidateUpdateSchema = z.strictObject({
  id: z.uuid(), revision: z.number().int().min(1).max(2_147_483_646), candidate: candidateSchema,
});

function validate(schema, input) {
  const parsed = schema.safeParse(input);
  if (parsed.success) return parsed.data;
  const issue = parsed.error.issues[0];
  throw new ResearchError(400, issue.code === "custom" ? issue.message : "Geçersiz aday alanı: " + (issue.path.join(".") || "istek"));
}

export async function listCandidates(input, fetcher = fetch) {
  const { market_id, status, offset, limit } = validate(candidateListSchema, input);
  const query = new URLSearchParams({ select: "*", order: "updated_at.desc,id.desc", offset, limit: limit + 1 });
  if (market_id) query.set("market_id", "eq." + market_id);
  if (status) query.set("status", "eq." + status);
  const rows = await db(table + "?" + query, { fetcher });
  return { candidates: rows.slice(0, limit), next_offset: rows.length > limit ? offset + limit : null };
}

export async function createCandidate(input, fetcher = fetch) {
  const candidate = validate(candidateSchema, input);
  const rows = await db(table, { method: "POST", body: candidate, prefer: "return=representation", fetcher });
  const saved = rows?.[0];
  if (!saved) throw new ResearchError(502, "Adayın kaydı doğrulanamadı.");
  return saved;
}

export async function updateCandidate(input, fetcher = fetch) {
  const { id, revision, candidate } = validate(candidateUpdateSchema, input);
  const query = new URLSearchParams({ id: "eq." + id, revision: "eq." + revision });
  const rows = await db(table + "?" + query, {
    method: "PATCH", body: { ...candidate, revision: revision + 1, updated_at: new Date().toISOString() },
    prefer: "return=representation", fetcher,
  });
  const saved = rows?.[0];
  if (!saved) throw new ResearchError(409, "Aday değişmiş veya artık erişilemiyor. Güncel kaydı açıp tekrar deneyin.");
  return saved;
}

export async function editorialRequest(request, url) {
  if (request.method === "GET") {
    if (url.searchParams.has("brief")) {
      if ([...url.searchParams.keys()].length !== 1) throw new ResearchError(400,"Brif için yalnızca aday kimliği gerekli.");
      return {body:await getProductionBrief(url.searchParams.get("brief")),status:200};
    }
    const params = Object.fromEntries(url.searchParams);
    for (const key of ["offset", "limit"]) {
      if (key in params) params[key] = /^\d+$/.test(params[key]) ? Number(params[key]) : NaN;
    }
    return { body: await listCandidates(params), status: 200 };
  }
  const raw = await request.text();
  if (Buffer.byteLength(raw, "utf8") > 80_000) throw new ResearchError(413, "Aday kaydı çok büyük.");
  let body;
  try { body = JSON.parse(raw); } catch { throw new ResearchError(400, "JSON geçersiz."); }
  return request.method === "POST"
    ? { body: await createCandidate(body), status: 201 }
    : { body: await updateCandidate(body), status: 200 };
}

export function buildProductionBrief(candidate) {
  const market=discoveryCatalog.markets.find(m=>m.id===candidate.market_id);
  const sources=candidate.sources??[];
  const presence=Object.fromEntries(["context","demand","coverage"].map(kind=>[kind,sources.some(s=>s.kind===kind)]));
  const pending=[];
  if(!presence.context)pending.push("Hikâyedeki tarihsel veya bilimsel iddiaları bağımsız kaynaklarla kontrol et.");
  if(!presence.demand)pending.push("Hedef pazarda bağımsız izleyici ilgisi verisi ara; arama hacmi bilinmiyor.");
  if(!presence.coverage)pending.push("Hedef dilde içerik kapsamını bağımsız olarak incele; içerik boşluğu doğrulanmadı.");
  if(candidate.format==="undecided")pending.push("Shorts veya uzun video formatını belirle.");
  if(candidate.cost==null)pending.push("Üretim maliyetlerini hesapla; bütçe bilinmiyor.");
  pending.push("Kaynakların doğruluğunu, görsel kullanım haklarını ve özgün anlatımı yayın öncesi kontrol et.");
  const clean=v=>String(v??"Bilinmiyor").replace(/\r?\n/g," ").replace(/[\\`*_{}\[\]<>#!|]/g,"\\$&");
  const format={shorts:"Shorts",long_form:"Uzun video",undecided:"Karar verilmedi"}[candidate.format];
  const status={draft:"Taslak",researching:"Araştırılıyor",ready:"Hazır",in_production:"Üretimde",published:"Yayınlandı",archived:"Arşivlendi"}[candidate.status];
  const cost=candidate.cost?candidate.cost.amount+" "+candidate.cost.currency+" ("+candidate.cost.basis+")":"Bilinmiyor";
  const markdown=[
    "# "+clean(candidate.title),
    "",
    "- Hedef pazar: "+clean(market?.label??candidate.market_id),
    "- Format: "+format,
    "- Durum: "+status,
    "- Kayıt revizyonu: "+candidate.revision,
    "- Tahmini üretim maliyeti: "+clean(cost),
    "",
    "## Pazar hipotezi","",clean(candidate.hypothesis),"",
    "## Özgün anlatım açısı","",clean(candidate.narrative_angle),"",
    "## Belirsizlikler","",clean(candidate.uncertainty),"",
    "## Bağımsız kaynaklar","",
    ...(sources.length?sources.flatMap(s=>["- "+clean(s.publisher)+" ("+s.checked_on+" / "+s.kind+")", "  - "+clean(s.url), "  - "+clean(s.finding)]):["Henüz kaynak eklenmedi."]),
    "","## Üretim öncesi kontrol listesi","",...pending.map(s=>"- [ ] "+s),"",
    "Not: Kaynak kaydı varlığı, kaynağın doğruluğunu veya talebi kanıtlamaz. Bu belge bir editoryal briftir, doğrulanmış senaryo veya kesin fırsat puanı değildir."
  ].join("\n")+"\n";
  return {candidate_id:candidate.id,revision:candidate.revision,source_presence:presence,pending,markdown};
}
export async function getProductionBrief(id,fetcher=fetch){
  const valid=validate(z.uuid(),id);
  const rows=await db(table+"?"+new URLSearchParams({select:"*",id:"eq."+valid,limit:"1"}),{fetcher});
  if(!rows?.length)throw new ResearchError(404,"Aday bulunamadı.");
  return buildProductionBrief(rows[0]);
}
