import {
  acceptsToken, env, errorResponse, getArtifact, getRun, json, publicCatalog, readBearer,
  reportFromZip, ResearchError, startResearch, trustedOrigin,
} from "../lib/research.mjs";

export default async (request: Request) => {
  const url = new URL(request.url);
  if (!trustedOrigin(request)) return json({ error: "İstek kaynağına izin verilmedi." }, 403);
  if (url.pathname === "/api/catalog" && request.method === "GET") return json(publicCatalog);
  if (!env("FASULYE_ACCESS_TOKEN")) {
    return json({ error: "Panel erişimi Netlify'da yapılandırılmalı." }, 503);
  }
  if (!acceptsToken(readBearer(request))) {
    return json({ error: "Panel erişim anahtarı geçersiz." }, 401, { "WWW-Authenticate": "Bearer" });
  }
  try {
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
      const id = url.searchParams.get("id") ?? "";
      const result = url.searchParams.get("result");
      if (result === "report" || result === "zip") {
        const zip = await getArtifact(id);
        if (result === "report") return json(await reportFromZip(zip));
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
  path: ["/api/research", "/api/catalog"],
  rateLimit: { action: "rate_limit", aggregateBy: ["ip", "domain"], windowSize: 60, windowLimit: 40 },
};
