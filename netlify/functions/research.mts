import {
  acceptsToken, env, errorResponse, getHistory, getReport, getRun, listReportVideos, json, publicCatalog, readBearer,
  ResearchError, startResearch, trustedOrigin,
} from "../lib/research.mjs";

import { discoveryCatalog, enqueueBatch, listBatches, batchStatus, queueBudget, planBatch, listBatchTasks } from "../lib/batch.mjs";
import { getEvidence, getTrend, writeEvidence } from "../lib/evidence.mjs";
import { sessionFor, sameOriginMutation } from "../lib/panel-auth.mjs";
import { exportReport } from "../lib/report-export.mjs";

export default async (request: Request) => {
  const url = new URL(request.url);
  if (!trustedOrigin(request)) return json({ error: "İstek kaynağına izin verilmedi." }, 403);
  if (url.pathname === "/api/discovery-catalog" && request.method === "GET") return json(discoveryCatalog);
  if (url.pathname === "/api/catalog" && request.method === "GET") return json(publicCatalog);
  if (!env("FASULYE_ACCESS_TOKEN")) {
    return json({ error: "Panel erişimi Netlify'da yapılandırılmalı." }, 503);
  }
  const bearer=acceptsToken(readBearer(request));
  const session=sessionFor(request);
  if (!bearer && !session) {
    return json({ error: "Panel erişim anahtarı geçersiz." }, 401, { "WWW-Authenticate": "Bearer" });
  }
  if (!bearer && request.method !== "GET" && !sameOriginMutation(request)) return json({error:"İstek kaynağına izin verilmedi."},403);
  try {
    if (url.pathname === "/api/evidence") {
      if (request.method === "GET") { const id=url.searchParams.get("id"); return json(id?await getTrend(id):await getEvidence()); }
      if (request.method === "POST") {
        const raw=await request.text();
        if(raw.length>350000)throw new ResearchError(413,"Kaynak dosyası çok büyük.");
        let body;try{body=JSON.parse(raw);}catch{throw new ResearchError(400,"JSON geçersiz.");}
        return json(await writeEvidence(body),201);
      }
    }
    if (url.pathname === "/api/batch") {
      if (request.method === "POST") {
        const body = await request.text();
        if (body.length > 500000) throw new ResearchError(413,"Toplu istek çok büyük.");
        let input;
        try { input = JSON.parse(body); } catch { throw new ResearchError(400,"JSON geçersiz."); }
        if (url.searchParams.get("preview") === "1") {
          const plan = planBatch(input);
          return json({tasks:plan.tasks.length,missing:plan.missing});
        }
        return json(await enqueueBatch(input),202);
      }
      if (request.method === "GET") {
        const id=url.searchParams.get("id");
        if(id&&url.searchParams.get("tasks")==="1")return json(await listBatchTasks(id,Number(url.searchParams.get("offset")??0),100));
        if (id) { const result=await batchStatus(id); if (!result) throw new ResearchError(404,"Grup bulunamadı."); return json(result); }
        return json(await listBatches());
      }
    }
    if (url.pathname === "/api/quota" && request.method === "GET") return json(await queueBudget());
    if (url.pathname === "/api/research" && request.method === "POST") {
      const body = await request.text();
      if (body.length > 4096) throw new ResearchError(413, "Sorgu isteği çok büyük.");
      let input;
      try {
        input = JSON.parse(body);
      } catch {
        throw new ResearchError(400, "JSON isteği okunamadı.");
      }
      return json(await startResearch(input), 202);
    }
    if (url.pathname === "/api/research" && request.method === "GET") {
      if (url.searchParams.get("result") === "history") return json(await getHistory());
      const id = url.searchParams.get("id") ?? "";
      const result = url.searchParams.get("result");
      if(result==="videos")return json(await listReportVideos(id,{offset:Number(url.searchParams.get("offset")??0),limit:Number(url.searchParams.get("limit")??50),region:url.searchParams.get("region")??undefined,language:url.searchParams.get("language")??undefined,sort:url.searchParams.get("sort")??"views",max_subscribers:url.searchParams.has("max_subscribers")?Number(url.searchParams.get("max_subscribers")):undefined}));
      if (result === "report" || result === "zip") {
        const report = await getReport(id);
        if (result === "report") return json(report);
        const zip = await exportReport(report);
        return new Response(new Uint8Array(zip), {
          headers: {
            "Content-Type": "application/zip",
            "Content-Disposition": `attachment; filename="fasulye-${id}.zip"`,
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
          },
        });
      }
      return json(await getRun(id));
    }
    return json({ error: "Bu HTTP yöntemi desteklenmiyor." }, 405);
  } catch (error) {
    return errorResponse(error);
  }
};

export const config = {
  path: ["/api/research", "/api/catalog", "/api/discovery-catalog", "/api/batch", "/api/quota", "/api/evidence"],
  rateLimit: { action: "rate_limit", aggregateBy: ["ip", "domain"], windowSize: 60, windowLimit: 40 },
};
