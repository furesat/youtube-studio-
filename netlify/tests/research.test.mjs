import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { generateKeyPair, SignJWT } from "jose";
import { test } from "node:test";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import research from "../functions/research.mts";
import mcp from "../functions/mcp.mts";
import { verifyAccessToken } from "../lib/mcp-auth.mjs";
import { getArtifact, getRun, reportFromZip, startResearch } from "../lib/research.mjs";

process.env.FASULYE_GITHUB_TOKEN = "test-github";
process.env.FASULYE_ACCESS_TOKEN = "test-personal-token";

const auth = { Authorization: "Bearer test-personal-token" };
const run = { path: ".github/workflows/fasulye-opportunity.yml", status: "completed", conclusion: "success" };
const report = { schema_version: 1, opportunities: [], test: "Türkçe" };
const zip = execFileSync("python3", ["-c", [
  "import io,sys,zipfile", "stream=io.BytesIO()",
  "archive=zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED)",
  `archive.writestr('report.json',${JSON.stringify(JSON.stringify(report))})`,
  "archive.close()", "sys.stdout.buffer.write(stream.getvalue())",
].join("\n")]);

test("dispatches a project run with manual query but without exposing GitHub token", async () => {
  const result = await startResearch({query: " çatalın tarihi ", region: "TR", language: "tr"}, async (url, options) => {
    assert.match(url, /fasulye-opportunity\.yml\/dispatches$/);
    assert.equal(options.headers["X-GitHub-Api-Version"], "2026-03-10");
    assert.equal(options.headers.Authorization, "Bearer test-github");
    assert.deepEqual(JSON.parse(options.body), {
      ref: "main", inputs: {query: "çatalın tarihi", region: "TR", language: "tr"},
    });
    return Response.json({workflow_run_id: 123});
  });
  assert.equal(result.id, "123");
  assert.doesNotMatch(JSON.stringify(result), /test-github/);
});

test("rejects invalid inputs before contacting GitHub", async () => {
  for (const input of [{query: "çatal", topics: ["fork"]}, {topics: ["arbitrary"]}, {query: "   "},
    {query: "a\nb"}, {language: "de"}, {region: "ZZZ"}, {ref: "untrusted-branch"}]) {
    await assert.rejects(() => startResearch(input, () => assert.fail("Unexpected request")), {status: 400});
  }
});

test("verifies run ownership before retrieving the artifact without leaking bearer to storage", async () => {
  const calls = [];
  const bytes = await getArtifact("123", async (url, request) => {
    const address = String(url);
    calls.push(address);
    if (address === "https://object.example/signed") {
      assert.equal(request.headers, undefined);
      return new Response(zip);
    }
    if (address.endsWith("/runs/123")) return Response.json(run);
    if (address.endsWith("/runs/123/artifacts")) {
      return Response.json({artifacts: [{name: "fasulye-opportunity-report", id: 987, expired: false}]});
    }
    assert.match(address, /artifacts\/987\/zip$/);
    assert.equal(request.redirect, "manual");
    return new Response(null, {status: 302, headers: {location: "https://object.example/signed"}});
  });
  assert.equal(calls.length, 4);
  assert.deepEqual(await reportFromZip(bytes), report);
  await assert.rejects(() => getRun("123", async () => Response.json({...run, path: "different.yml"})),
    {status: 404});
});

test("returns a clear error when Actions has no archive", async () => {
  await assert.rejects(getArtifact("123", async url =>
    Response.json(url.endsWith("/123") ? run : {artifacts: []})), {status: 404});
});

test("REST catalog is public while runs and cross-origin requests are protected", async () => {
  const catalog = await research(new Request("https://example.test/api/catalog"));
  assert.equal(catalog.status, 200);
  assert.equal((await catalog.json()).markets.length, 3);
  const result = await research(new Request("https://example.test/api/research?id=123"));
  assert.equal(result.status, 401);
  assert.equal(result.headers.get("cache-control"), "no-store");
  const foreign = await research(new Request("https://example.test/api/catalog", {
    headers: {Origin: "https://other.example"},
  }));
  assert.equal(foreign.status, 403);
  const invalid = await research(new Request("https://example.test/api/research", {
    method: "POST", headers: auth, body: "{not json",
  }));
  assert.equal(invalid.status, 400);
});

test("an MCP client connects, lists tools and reads the catalog using its bearer token", async () => {
  const url = new URL("https://example.test/mcp");
  const client = new Client({name: "test-client", version: "1.0"});
  const transport = new StreamableHTTPClientTransport(url, {
    requestInit: {headers: auth},
    fetch: (input, init) => mcp(new Request(input, init)),
  });
  await client.connect(transport);
  try {
    const tools = await client.listTools();
    assert.equal(tools.tools.length, 3);
    assert.equal(tools.tools.find(tool => tool.name === "start_youtube_research").annotations.readOnlyHint, false);
    const result = await client.callTool({name: "list_research_catalog"});
    assert.equal(JSON.parse(result.content[0].text).topics.length, 4);
    const anonymous = await mcp(new Request(url, {method: "POST"}));
    assert.equal(anonymous.status, 401);
  } finally {
    await client.close();
  }
});

test("optional OAuth discovery advertises the protected resource and enforces issuer, audience and user", async () => {
  const issuer = "https://issuer.example/";
  const resource = "https://example.test/mcp";
  process.env.FASULYE_OAUTH_ISSUER = issuer;
  process.env.FASULYE_OAUTH_RESOURCE = resource;
  process.env.FASULYE_OAUTH_SUBJECT = "owner";
  try {
    const anonymous = await mcp(new Request(resource, {method: "POST"}));
    assert.match(anonymous.headers.get("www-authenticate"), /oauth-protected-resource\/mcp/);
    const metadata = await mcp(new Request("https://example.test/.well-known/oauth-protected-resource/mcp"));
    assert.deepEqual((await metadata.json()).authorization_servers, [issuer]);
    const {privateKey, publicKey} = await generateKeyPair("RS256");
    const settings = {issuer, resource, subject: "owner"};
    const sign = (subject, audience) => new SignJWT({})
      .setProtectedHeader({alg: "RS256"}).setIssuer(issuer).setAudience(audience)
      .setSubject(subject).setExpirationTime("2m").sign(privateKey);
    assert.equal(await verifyAccessToken(await sign("owner", resource), settings, publicKey), true);
    assert.equal(await verifyAccessToken(await sign("other", resource), settings, publicKey), false);
    await assert.rejects(verifyAccessToken(await sign("owner", "https://other.example"), settings, publicKey));
  } finally {
    delete process.env.FASULYE_OAUTH_ISSUER;
    delete process.env.FASULYE_OAUTH_RESOURCE;
    delete process.env.FASULYE_OAUTH_SUBJECT;
  }
});
