import assert from "node:assert/strict";
import { test } from "node:test";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import research from "../functions/research.mts";
import mcp from "../functions/mcp.mts";
import { login } from "../lib/panel-auth.mjs";
import { candidateSchema, buildProductionBrief, getProductionBrief } from "../lib/editorial.mjs";

const host = "https://example.test";
const api = host + "/api/editorial";
const bearer = { authorization: "Bearer test-panel" };
const id = "891a048d-b1c1-4ec7-a81b-63704ae44fc6";
const source = {
  publisher: "Arşiv", url: "https://archive.example/calendar", checked_on: "2026-11-27",
  kind: "context", finding: "Tarihli kayıt, hikâyenin başlangıç noktasını belirliyor.",
};
const candidate = {
  title: "Eksik takvim yaprağı", market_id: "de",
  hypothesis: "Almanca tarih meraklıları için yerel takvim geçişinin gündelik etkisi ilgi çekebilir.",
  narrative_angle: "Bir arşiv kaydındaki tarih farkını günlük tutan birinin gözünden anlat.",
  format: "long_form", cost: null, uncertainty: "Bu pazardaki izleyici ilgisini henüz ölçmedik.",
  status: "draft", independent: true, sources: [],
};

process.env.FASULYE_ACCESS_TOKEN = "test-panel";
process.env.FASULYE_GITHUB_TOKEN = "test-signing-secret";
process.env.SUPABASE_SECRET_KEY = "sb_secret_test_only";

test("only original editorial fields and independent source records pass validation", () => {
  assert.ok(candidateSchema.safeParse(candidate).success);
  assert.ok(candidateSchema.safeParse({
    ...candidate, status: "ready", sources: [source], cost: { amount: 0, currency: "EUR", basis: "Kendi emeğim" },
  }).success);
  for (const invalid of [
    { ...candidate, independent: false },
    { ...candidate, status: "ready" },
    { ...candidate, status: "published" },
    { ...candidate, market_id: "unknown" },
    { ...candidate, video_ids: ["abc"] },
    { ...candidate, report_run_id: "1234" },
    { ...candidate, opportunity_score: 90 },
    { ...candidate, sources: [{ ...source, checked_on: "2025-02-29" }] },
    { ...candidate, sources: [{ ...source, views: 500 }] },
    ...["https://www.youtube.com./watch?v=abc", "https://youtu.be/abc", "https://www.youtube-nocookie.com/embed/abc",
      "https://www.googleapis.com/youtube/v3/videos", "https://i.ytimg.com/a.jpg", "https://youtube.com@archive.example",
      "https://archive.example@www.youtube.com", "http://archive.example", "javascript:alert(1)"]
      .map(url => ({ ...candidate, sources: [{ ...source, url }] })),
  ]) assert.equal(candidateSchema.safeParse(invalid).success, false);
});

test("REST protects reads and writes, validates JSON, filters, and reuses panel CSRF checks", async t => {
  const session = await login(new Request(host + "/api/login"), { password: "test-panel", remember: false });
  const cookie = session.cookies[0].split(";")[0];
  const get = (headers = {}, query = "") => research(new Request(api + query, { headers }));
  const write = (method, headers, body = candidate) => research(new Request(api, {
    method, headers, body: typeof body === "string" ? body : JSON.stringify(body),
  }));
  const fetcher = t.mock.method(globalThis, "fetch", async (url, init) => {
    const target = new URL(url);
    assert.equal(target.host, "niihqywncuwxfxipkgte.supabase.co");
    assert.equal(target.pathname, "/rest/v1/fasulye_editorial_candidates");
    assert.equal(init.headers.apikey, "sb_secret_test_only");
    if (init.method === "GET") {
      assert.equal(target.searchParams.get("market_id"), "eq.de");
      assert.equal(target.searchParams.get("status"), "eq.draft");
      assert.equal(target.searchParams.get("offset"), "0");
      assert.equal(target.searchParams.get("limit"), "2");
      return Response.json([{ id, ...candidate }, { id: "another" }]);
    }
    const row = JSON.parse(init.body);
    if (init.method === "POST") return Response.json([{ id, revision: 1, ...row }]);
    assert.equal(init.method, "PATCH");
    assert.equal(target.searchParams.get("id"), "eq." + id);
    assert.ok(row.updated_at);
    return Response.json(target.searchParams.get("revision") === "eq.1" ? [{ id, ...row }] : []);
  });

  assert.equal((await get()).status, 401);
  assert.equal((await write("POST", {})).status, 401);
  assert.equal((await write("POST", { cookie })).status, 403);
  assert.equal((await write("PUT", { cookie, origin: "https://other.example" })).status, 403);
  assert.equal((await write("POST", bearer, "{")).status, 400);
  assert.equal((await write("POST", bearer, "x".repeat(80_001))).status, 413);
  assert.equal((await get(bearer, "?limit=99")).status, 400);
  assert.equal((await get(bearer, "?offset=")).status, 400);
  assert.equal(fetcher.mock.callCount(), 0);
  const listed = await get({ cookie }, "?market_id=de&status=draft&limit=1");
  assert.equal(listed.headers.get("Cache-Control"), "no-store");
  assert.deepEqual(await listed.json(), { candidates: [{ id, ...candidate }], next_offset: 1 });

  const created = await write("POST", { cookie, origin: host });
  assert.equal(created.status, 201);
  assert.equal((await created.json()).revision, 1);
  const change = { id, revision: 1, candidate: { ...candidate, status: "ready", sources: [source] } };
  const updated = await write("PUT", bearer, change);
  assert.equal(updated.status, 200);
  assert.equal((await updated.json()).revision, 2);
  assert.equal((await write("PUT", bearer, { ...change, revision: 2 })).status, 409);
});

test("MCP uses the shared editorial contract on all three tools", async t => {
  const saves = [];
  t.mock.method(globalThis, "fetch", async (url, init) => {
    assert.match(url, /\/rest\/v1\/fasulye_editorial_candidates(?:\?|$)/);
    if (init.method === "GET") return Response.json(saves.slice(-1));
    const row = { id, revision: 1, ...JSON.parse(init.body) };
    saves.push(row);
    return Response.json([row]);
  });
  const client = new Client({ name: "editorial-test", version: "1.0" });
  const url = new URL(host + "/mcp");
  const transport = new StreamableHTTPClientTransport(url, {
    requestInit: { headers: bearer },
    fetch: (input, init) => mcp(new Request(input, init)),
  });
  await client.connect(transport);
  try {
    const call = (name, args) => client.callTool({ name, arguments: args });
    const invalid = await call("create_editorial_candidate", { ...candidate, status: "ready" });
    assert.equal(invalid.isError, true);
    assert.equal(saves.length, 0);
    const created = await call("create_editorial_candidate", candidate);
    assert.equal(JSON.parse(created.content[0].text).revision, 1);
    const updated = await call("update_editorial_candidate", {
      id, revision: 1, candidate: { ...candidate, status: "ready", sources: [source] },
    });
    assert.equal(JSON.parse(updated.content[0].text).revision, 2);
    const result = await call("list_editorial_candidates", { status: "ready" });
    assert.equal(JSON.parse(result.content[0].text).candidates[0].status, "ready");
  } finally {
    await client.close();
  }
});

test("production briefs preserve missing evidence and do not invent facts", async () => {
  const saved={...candidate,id,revision:1,sources:[source]};
  const brief=buildProductionBrief(saved);
  assert.deepEqual(brief.source_presence,{context:true,demand:false,coverage:false});
  assert.match(brief.markdown,/arama hacmi bilinmiyor/);
  assert.match(brief.markdown,/içerik boşluğu doğrulanmadı/);
  assert.match(brief.markdown,/bütçe bilinmiyor/);
  assert.match(brief.markdown,/https:\/\/archive\.example\/calendar/);
  assert.equal(brief.revision,1);
  assert.doesNotMatch(buildProductionBrief({...saved,title:"<script>alert(1)</script>"}).markdown,/<script>/);
  const loaded=await getProductionBrief(id,async(url,init)=>{
    assert.equal(new URL(url).searchParams.get("id"),"eq."+id);
    assert.equal(init.method,"GET");
    return Response.json([saved]);
  });
  assert.deepEqual(loaded,brief);
  await assert.rejects(()=>getProductionBrief("invalid"),{status:400});
  await assert.rejects(()=>getProductionBrief(id,async()=>Response.json([])),{status:404});
});
