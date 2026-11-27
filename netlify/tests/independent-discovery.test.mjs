import {test} from "node:test";
import assert from "node:assert/strict";
import {planIndependent,discoverIndependent,crossLanguageEvidence} from "../lib/independent-discovery.mjs";
test("localized discovery templates include forgotten professions and do not invent missing translations",()=>{
 const p=planIndependent({categories:["professions"],languages:["tr","de","ja"]});
 assert.equal(p.queries.length,2);assert.equal(p.missing[0].language,"ja");assert.equal(p.interest_verified,false);
});
test("independent discovery is capped and stops at rate limit",async()=>{
 process.env.FASULYE_WIKIMEDIA_EVIDENCE="1";
 try{
  let calls=0;
  const r=await discoverIndependent({categories:["history"],languages:["tr","de","en"]},async()=>{calls++;return new Response(null,{status:429});});
  assert.equal(calls,1);assert.equal(r.observations[0].articles,null);assert.equal(r.unattempted.length,2);
  await assert.rejects(()=>discoverIndependent({categories:["history","science"],languages:["tr","de","en","fr"]},()=>assert.fail("no request")),{status:400});
 }finally{delete process.env.FASULYE_WIKIMEDIA_EVIDENCE;}
});
test("cross-language map does not convert missing evidence into zero",async()=>{
 process.env.SUPABASE_SECRET_KEY="sb_secret_fixture";
 try{
  const result=await crossLanguageEvidence({topic:"fork",markets:["tr","de"]},async(url)=>{
    assert.equal(new URL(url).hostname,"niihqywncuwxfxipkgte.supabase.co");
    return Response.json([]);
  });
  assert.equal(result.markets.length,2);assert.ok(result.markets.every(m=>m.local_expressions.length&&m.youtube_demand===null&&m.worldwide_language_interest===null));
  assert.equal(result.providers.wikimedia.status,"disabled");
 }finally{delete process.env.SUPABASE_SECRET_KEY;}
});
