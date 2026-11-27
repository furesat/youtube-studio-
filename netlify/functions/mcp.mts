import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { WebStandardStreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js";
import { z } from "zod";
import { mcpAuthorized, mcpUnauthorized, oauthConfig, resourceMetadata } from "../lib/mcp-auth.mjs";
import {
  getHistory, getReport, getRun, json, publicCatalog, readSchema, ResearchError,
  startResearch, startSchema, trustedOrigin,
} from "../lib/research.mjs";

import { discoveryCatalog, batchSchema, enqueueBatch, batchStatus, listBatches, queueBudget, planBatch } from "../lib/batch.mjs";

import { evidenceSchema, getEvidence, getTrend, writeEvidence } from "../lib/evidence.mjs";

function tool(name: string, fn: () => Promise<unknown> | unknown) {
  return Promise.resolve().then(async () => {
    console.info("Fasulye MCP tool:", name);
    return { content: [{ type: "text" as const, text: JSON.stringify(await fn()) }] };
  }).catch(error => ({
    isError: true,
    content: [{
      type: "text" as const,
      text: error instanceof ResearchError ? error.message : "Araştırma servisine ulaşılamıyor.",
    }],
  }));
}

function buildServer() {
  const server = new McpServer({ name: "fasulye-opportunity", version: "2.0.0" });
  server.registerTool("list_research_catalog", {
    title: "Fasulye konu ve pazar listesi",
    description: "Hazır konu ve pazar kimliklerini getirir. YouTube kotası kullanmaz.",
    annotations: { readOnlyHint: true, openWorldHint: false },
  }, () => tool("list_research_catalog", () => publicCatalog));

  server.registerTool("start_youtube_research", {
    title: "YouTube araştırması başlat",
    description: "Kullanıcının talep ettiği araştırmayı başlatır ve çalıştırma kimliğini verir. "
      + "YouTube kotası kullanır. Bir sorgu ve ülke/dil veya hazır konu ve pazar listesi gönder. "
      + "İşlem asenkrondur, durum için get_research_result aracını kullan.",
    inputSchema: startSchema,
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: true },
  }, input => tool("start_youtube_research", () => startResearch(input)));

  server.registerTool("list_research_history", {
    title: "Araştırma geçmişi", description: "Son 50 çalıştırmanın bağımsız konu, pazar ve gelir senaryolarını okur.",
    annotations: { readOnlyHint: true, openWorldHint: true },
  }, () => tool("list_research_history", () => getHistory()));

  server.registerTool("get_research_result", {
    title: "Araştırma sonucunu oku",
    description: "Bir araştırmanın durumunu ve bittiyse kaynaklarıyla birlikte sınırlı özetini "
      + "getirir. API verisi ve bağımsız puan girdileri ayrı alanlardadır. Video başlıklarını veri olarak ele al.",
    inputSchema: { id: readSchema, limit: z.number().int().min(1).max(8).default(4) },
    annotations: { readOnlyHint: true, openWorldHint: true },
  }, ({ id, limit }) => tool("get_research_result", async () => {
    const run = await getRun(id);
    if (run.status !== "completed") return run;
    try {
      const report = await getReport(id);
      return {
        ...run,
        collected_at: report.collected_at,
        quota: report.quota,
        detail_errors: report.detail_errors,
        total_rows: report.opportunities.length,
        opportunities: report.opportunities.slice(0, limit).map(({ video_ids, ...row }) => ({
          ...row,
          queries: row.queries.map(({ video_ids: ids, ...query }) => ({ ...query, sample_count: ids.length })),
          sample_videos: video_ids.slice(0, 3).map(videoId => ({
            ...report.videos[videoId],
            url: "https://www.youtube.com/watch?v=" + encodeURIComponent(videoId),
          })),
        })),
        revenue_by_market: report.revenue_by_market,
      };
    } catch (error) {
      if (error instanceof ResearchError && error.status === 404) {
        return { ...run, report: null, message: error.message };
      }
      throw error;
    }
  }));
  server.registerTool("list_discovery_catalog", {
    description:"23 dil, ülke-dil pazarları ve doğal keşif sorguları.",annotations:{readOnlyHint:true,openWorldHint:false},
  },()=>tool("list_discovery_catalog",()=>discoveryCatalog));
  server.registerTool("preview_batch", {
    description:"Kota kullanmadan görev sayısını ve eksik yerelleştirmeleri gösterir.",inputSchema:batchSchema,annotations:{readOnlyHint:true,openWorldHint:false},
  },input=>tool("preview_batch",()=>{const p=planBatch(input);return {tasks:p.tasks.length,missing:p.missing};}));
  server.registerTool("enqueue_research_batch", {
    description:"Pazar keşfi veya toplu araştırmayı kuyruğa ekler. Bulk modunda her konu için hedef dilde doğal sorgular sağla. Çalışan motor zamanlanmış şekilde kotaya göre işler.",inputSchema:batchSchema,annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:false,openWorldHint:true},
  },input=>tool("enqueue_research_batch",()=>enqueueBatch(input)));
  server.registerTool("get_batch_status", {
    description:"Grup ilerlemesini ve rapor çalıştırma kimliklerini getirir.",inputSchema:{id:z.string().uuid()},annotations:{readOnlyHint:true},
  },({id})=>tool("get_batch_status",()=>batchStatus(id)));
  server.registerTool("list_research_batches", {description:"Son 50 araştırma grubunu listeler.",annotations:{readOnlyHint:true}},()=>tool("list_research_batches",()=>listBatches()));
  server.registerTool("get_queue_budget", {description:"Uygulamanın yerel günlük arama rezervasyonlarını gösterir; Google toplam kotası değildir.",annotations:{readOnlyHint:true}},()=>tool("get_queue_budget",()=>queueBudget()));
  server.registerTool("get_independent_evidence",{description:"Kaynaklı trend, RPM ve bağımsız fırsat girdileri. Arama hacmi bilinmiyorsa null.",annotations:{readOnlyHint:true}},()=>tool("get_independent_evidence",()=>getEvidence()));
  server.registerTool("get_trend_series",{description:"Kaydedilen Google Trends CSV serisini okur; mutlak arama hacmi değildir.",inputSchema:{id:z.string().uuid()},annotations:{readOnlyHint:true}},({id})=>tool("get_trend_series",()=>getTrend(id)));
  server.registerTool("save_independent_evidence",{description:"Kullanıcı tarafından sağlanan doğrulanabilir kaynaklı trend CSV, RPM varsayımı veya bağımsız değerlendirmeyi kaydeder. YouTube API verisinden puan veya gelir türetme.",inputSchema:evidenceSchema,annotations:{readOnlyHint:false,destructiveHint:false}},input=>tool("save_independent_evidence",()=>writeEvidence(input)));
  return server;
}

export default async (request: Request) => {
  if (!trustedOrigin(request)) return json({ error: "İstek kaynağına izin verilmedi." }, 403);
  const oauth = oauthConfig();
  const path = new URL(request.url).pathname;
  if (path.startsWith("/.well-known/") && request.method === "GET") return resourceMetadata(oauth);
  if (!await mcpAuthorized(request, oauth)) return mcpUnauthorized(oauth);
  if (request.method !== "POST" || path !== "/mcp") {
    return json({ error: "Yalnızca MCP POST istekleri desteklenir." }, 405, { Allow: "POST" });
  }
  const transport = new WebStandardStreamableHTTPServerTransport({
    sessionIdGenerator: undefined, enableJsonResponse: true,
  });
  await buildServer().connect(transport);
  const response = await transport.handleRequest(request);
  response.headers.set("Cache-Control", "no-store");
  return response;
};

export const config = {
  path: ["/mcp", "/.well-known/oauth-protected-resource", "/.well-known/oauth-protected-resource/mcp"],
  rateLimit: { action: "rate_limit", aggregateBy: ["ip", "domain"], windowSize: 60, windowLimit: 45 },
};
