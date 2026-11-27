import {
  acceptsToken, env, errorResponse, getHistory, getReport, getRun, listReportVideos, json, publicCatalog, readBearer,
  ResearchError, startResearch, trustedOrigin,
} from "../lib/research.mjs";

import { discoveryCatalog, enqueueBatch, listBatches, batchStatus, queueBudget, planBatch, listBatchTasks, marketEvidence } from "../lib/batch.mjs";
import { getEvidence, getTrend, writeEvidence } from "../lib/evidence.mjs";
import {searchWiki,collectWiki,listWiki} from "../lib/wikimedia.mjs";
import {featureFlags,controlQueue,queueHealth} from "../lib/queue-control.mjs";
import { activeSession, sameOriginMutation } from "../lib/panel-auth.mjs";
import {planIndependent,discoverIndependent,crossLanguageEvidence} from "../lib/independent-discovery.mjs";
import { readWorkflow,advanceWorkflow } from "../lib/editorial-workflow.mjs";
import { editorialRequest } from "../lib/editorial.mjs";
import { exportReport } from "../lib/report-export.mjs";

export default async (request: Request) => {
  const url = new URL(request.url);
  if (!trustedOrigin(request)) return json({ error: "İstek kaynağına izin verilmedi." }, 403);
  if (url.pathname === "/api/discovery-catalog" && request.method === "GET") return json({...discoveryCatalog,features:featureFlags()});
  if (url.pathname === "/api/catalog" && request.method === "GET") return json(publicCatalog);
  if (!env("FASULYE_ACCESS_TOKEN")) {
    return json({ error: "Panel erişimi Netlify'da yapılandırılmalı." }, 503);
  }
  const bearer=acceptsToken(readBearer(request));
  try {
  const session=bearer?null:await activeSession(request);
  if (!bearer && !session) {
    return json({ error: "Panel erişim anahtarı geçersiz." }, 401, { "WWW-Authenticate": "Bearer" });
  }
  if (!bearer && request.method !== "GET" && !sameOriginMutation(request)) return json({error:"İstek kaynağına izin verilmedi."},403);
    if(url.pathname==="/api/discover"&&request.method==="POST"){
      const raw=await request.text();if(Buffer.byteLength(raw)>12000)throw new ResearchError(413,"İstek çok büyük.");
      let body;try{body=JSON.parse(raw);}catch{throw new ResearchError(400,"JSON geçersiz.");}
      const mode=url.searchParams.get("mode");
      if(mode==="plan")return json(planIndependent(body));
      if(mode==="map")return json(await crossLanguageEvidence(body));
      if(mode==="search")return json(await discoverIndependent(body));
      throw new ResearchError(400,"Keşif işlemi seçin.");
    }
    if(url.pathname==="/api/workflow"){
      if(request.method==="GET")return json(await readWorkflow({candidate_id:url.searchParams.get("candidate_id")}));
      if(request.method==="POST"){
        const raw=await request.text();if(Buffer.byteLength(raw)>350000)throw new ResearchError(413,"İstek çok büyük.");
        let body;try{body=JSON.parse(raw);}catch{throw new ResearchError(400,"JSON geçersiz.");}
        return json(await advanceWorkflow(body),201);
      }
    }
    if (url.pathname === "/api/editorial" && ["GET", "POST", "PUT"].includes(request.method)) {
      const result = await editorialRequest(request, url);
      return json(result.body, result.status);
    }
    if(url.pathname==="/api/queue"){
      if(request.method==="GET")return json(await queueHealth());
      if(request.method==="POST"){
        const raw=await request.text();if(raw.length>4096)throw new ResearchError(413,"İstek çok büyük.");
        let body;try{body=JSON.parse(raw);}catch{throw new ResearchError(400,"JSON geçersiz.");}
        return json(await controlQueue(body));
      }
    }
    if (url.pathname === "/api/wikimedia") {
      if(env("FASULYE_WIKIMEDIA_EVIDENCE")!=="1")throw new ResearchError(503,"Wikimedia kanıt modülü henüz etkin değil.");
      if(request.method==="GET")return json(await listWiki({offset:Number(url.searchParams.get("offset")??0)}));
      if(request.method==="POST"){
        const raw=await request.text();if(raw.length>4096)throw new ResearchError(413,"İstek çok büyük.");
        let body;try{body=JSON.parse(raw);}catch{throw new ResearchError(400,"JSON geçersiz.");}
        if(url.searchParams.get("search")==="1")return json(await searchWiki(body));
        return json(await collectWiki(body),201);
      }
    }
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
          return json({tasks:plan.tasks.length,missing:plan.missing,methodology:plan.methodology??null});
        }
        return json(await enqueueBatch(input),202);
      }
      if (request.method === "GET") {
        const id=url.searchParams.get("id");
        if(id&&url.searchParams.get("compare")==="1")return json(await marketEvidence(id,{topic:url.searchParams.get("topic")||null,market:url.searchParams.get("market")||null,days:url.searchParams.has("days")?Number(url.searchParams.get("days")):null,offset:Number(url.searchParams.get("offset")??0),limit:50}));
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
  path: ["/api/research", "/api/catalog", "/api/discovery-catalog", "/api/batch", "/api/quota", "/api/evidence", "/api/editorial", "/api/wikimedia", "/api/queue", "/api/workflow", "/api/discover"],
  rateLimit: { action: "rate_limit", aggregateBy: ["ip", "domain"], windowSize: 60, windowLimit: 40 },
};
