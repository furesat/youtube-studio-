import assert from "node:assert/strict";
import { test } from "node:test";
import { login, sessionFor, adminFor, unlockAdmin, logoutCookies, activeSession, revokeSession, sessionStatus } from "../lib/panel-auth.mjs";
import auth from "../functions/panel-auth.mts";
import research from "../functions/research.mts";
import { planBatch } from "../lib/batch.mjs";
process.env.FASULYE_ACCESS_TOKEN="unit-test-panel";
process.env.FASULYE_GITHUB_TOKEN="unit-test-signing-secret";
process.env.FASULYE_ADMIN_TOKEN="unit-test-owner";
const host="https://example.test";
const request=(path,headers={},method="GET")=>new Request(host+path,{method,headers});
test("remembered sessions use signed HttpOnly cookies and are invalidated by token rotation",async()=>{
 const result=await login(request("/api/login"),{password:"unit-test-panel",remember:true,label:"Mac"});
 assert.equal(result.body.authenticated,true);
 assert.match(result.cookies[0],/HttpOnly; SameSite=Strict; Max-Age=7776000/);
 const cookie=result.cookies.map(c=>c.split(";")[0]).join("; ");
 assert.ok(sessionFor(request("/api/session",{cookie})));
 assert.equal(sessionFor(request("/api/session",{cookie}),Date.now()+91*86400000),null);
 assert.equal(sessionFor(request("/api/session",{cookie:cookie.replace(/\.[A-Za-z0-9_-]+;/,".invalid;")})),null);
 assert.equal(adminFor(request("/api/admin/logins",{cookie})),false);
 const unlocked=unlockAdmin(request("/api/admin/unlock",{cookie}),"unit-test-owner");
 const both=cookie.split("; ").filter(s=>!s.startsWith("__Host-fasulye_admin=")).concat(unlocked.split(";")[0]).join("; ");
 assert.equal(adminFor(request("/api/admin/logins",{cookie:both})),true);
 assert.match(logoutCookies()[0],/Max-Age=0/);
 process.env.FASULYE_ACCESS_TOKEN="rotated";
 assert.equal(sessionFor(request("/api/session",{cookie})),null);
 process.env.FASULYE_ACCESS_TOKEN="unit-test-panel";
});
test("password errors, CSRF, and anonymous admin requests are rejected",async()=>{
 await assert.rejects(()=>login(request("/api/login"),{password:"wrong"}),{status:401});
 const foreign=await auth(new Request(host+"/api/login",{method:"POST",headers:{origin:"https://other.example"},body:"{}"}));
 assert.equal(foreign.status,403);
 assert.equal((await auth(request("/api/admin/logins"))).status,403);
 const result=await login(request("/api/login"),{password:"unit-test-panel",remember:false});
 const cookie=result.cookies[0].split(";")[0];
 assert.doesNotMatch(result.cookies[0],/Max-Age=/);
 assert.equal((await research(new Request(host+"/api/research",{method:"POST",headers:{cookie,origin:host},body:"{bad"}))).status,400);
 assert.equal((await research(new Request(host+"/api/research",{method:"POST",headers:{cookie},body:"{}"}))).status,403);
});
test("3.0 campaign has all 8 markets, 10 categories and four reserved search profiles",()=>{
 const plan=planBatch({mode:"campaign"});
 assert.equal(plan.tasks.length,320);
 assert.equal(plan.missing.length,0);
 assert.equal(new Set(plan.tasks.map(t=>t.market_id)).size,8);
 assert.deepEqual([...new Set(plan.tasks.map(t=>t.lookback_days))],[365,90,30,7]);
 assert.equal(new Set(plan.tasks.map(t=>t.search_order)).size,3);
 assert.equal(planBatch({mode:"campaign",countries:["DE"],categories:["history"]}).tasks.length,4);
});

test("dedicated session signing migration rejects legacy cookies without coupling GitHub rotation",async()=>{
 const previous=process.env.FASULYE_SESSION_SECRET;
 const github=process.env.FASULYE_GITHUB_TOKEN;
 try{
  delete process.env.FASULYE_SESSION_SECRET;
  const legacy=await login(request("/api/login"),{password:"unit-test-panel"});
  const oldCookie=legacy.cookies[0].split(";")[0];
  process.env.FASULYE_SESSION_SECRET="unit-test-new-dedicated-session-secret";
  assert.equal(sessionFor(request("/api/session",{cookie:oldCookie})),null);
  const fresh=await login(request("/api/login"),{password:"unit-test-panel"});
  const cookie=fresh.cookies[0].split(";")[0];
  process.env.FASULYE_GITHUB_TOKEN="rotated-github";
  assert.ok(sessionFor(request("/api/session",{cookie})));
  process.env.FASULYE_SESSION_SECRET="too-short";
  assert.equal(sessionFor(request("/api/session",{cookie})),null);
  await assert.rejects(()=>login(request("/api/login"),{password:"unit-test-panel"}),{status:503});
 }finally{
  if(previous===undefined)delete process.env.FASULYE_SESSION_SECRET;else process.env.FASULYE_SESSION_SECRET=previous;
  process.env.FASULYE_GITHUB_TOKEN=github;
 }
});

test("registered session is rejected after server-side revocation, with fail-closed lookup",async()=>{
 const names=["FASULYE_SESSION_REVOCATION","SUPABASE_SECRET_KEY"];
 const previous=Object.fromEntries(names.map(n=>[n,process.env[n]]));
 process.env.FASULYE_SESSION_REVOCATION="1";
 process.env.SUPABASE_SECRET_KEY="sb_secret_fixture";
 const registry=new Map();
 const fake=async(url,options)=>{
   const u=new URL(url);
   if(u.pathname.endsWith("/fasulye_login_events"))return new Response(null,{status:201});
   assert.ok(u.pathname.endsWith("/fasulye_sessions"));
   if(options.method==="POST"){const row=JSON.parse(options.body);registry.set(row.sid,row);return Response.json([row]);}
   const sid=u.searchParams.get("sid").slice(3);
   const row=registry.get(sid);
   if(options.method==="PATCH"){if(row)row.revoked_at=JSON.parse(options.body).revoked_at;return new Response(null,{status:204});}
   return Response.json(row&&!row.revoked_at?[{sid}]:[]);
 };
 try{
   const logged=await login(request("/api/login"),{password:"unit-test-panel"},fake);
   const req=request("/api/session",{cookie:logged.cookies[0].split(";")[0]});
   assert.ok(await activeSession(req,fake));
   assert.equal((await sessionStatus(req,fake)).authenticated,true);
   await assert.rejects(()=>activeSession(req,async()=>new Response(null,{status:503})));
   await revokeSession(req,fake);
   await revokeSession(req,fake);
   assert.equal(await activeSession(req,fake),null);
   assert.equal((await sessionStatus(req,fake)).authenticated,false);
 }finally{for(const n of names){if(previous[n]===undefined)delete process.env[n];else process.env[n]=previous[n];}}
});
