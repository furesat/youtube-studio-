import assert from "node:assert/strict";
import { test } from "node:test";
import { discoveryCatalog, planBatch, enqueueBatch, batchStatus, marketEvidence } from "../lib/batch.mjs";
test("catalog covers 23 languages with natural discovery queries",()=>{
  assert.equal(Object.keys(discoveryCatalog.languages).length,23);
  assert.equal(discoveryCatalog.markets.length,36);
  assert.equal(planBatch({mode:"discovery"}).tasks.length,396);
  assert.equal(planBatch({mode:"discovery",countries:["DE","AT"],languages:["de"],categories:["history"]}).tasks.length,2);
});
test("bulk deduplicates and never fabricates translations",()=>{
  const topic={topic:"Özel örnek konu",queries:{tr:"özel örnek konu tarihi"}};
  const p=planBatch({mode:"bulk",countries:["TR","DE"],topics:[topic,topic]});
  assert.equal(p.tasks.length,1);assert.equal(p.missing.length,2);
  assert.throws(()=>planBatch({mode:"bulk",countries:["DE"],topics:[topic]}),/Görev sayısı/);
});
test("known topics automatically resolve local expressions",()=>{
  const p=planBatch({mode:"bulk",countries:["TR","DE"],topics:[{topic:"çatal"}]});
  assert.equal(p.tasks.length,2);assert.equal(p.missing.length,0);assert.ok(p.tasks.some(t=>t.query.includes("Geschichte")));
});
test("enqueue uses fixed project and only server secret",async()=>{
  process.env.SUPABASE_SECRET_KEY="sb_secret_unit_test";
  try{
    const id="00000000-0000-4000-8000-000000000001";
    const result=await enqueueBatch({mode:"discovery",countries:["TR"],categories:["history"]},async(url,request)=>{
      assert.equal(url,"https://niihqywncuwxfxipkgte.supabase.co/rest/v1/rpc/fasulye_enqueue");
      assert.equal(request.headers.apikey,"sb_secret_unit_test");
      assert.equal(JSON.parse(request.body).p_tasks.length,1);
      return Response.json(id);
    });
    assert.equal(result.id,id);
    assert.equal(result.tasks,1);
    assert.doesNotMatch(JSON.stringify(result),/sb_secret/);
    await assert.rejects(()=>batchStatus("invalid"),{status:400});
  }finally{delete process.env.SUPABASE_SECRET_KEY;}
});

test("market evidence forwards bounded filters and preserves unknown data",async()=>{
  process.env.SUPABASE_SECRET_KEY="sb_secret_unit_test";
  try{
    const id="00000000-0000-4000-8000-000000000001";
    const payload={total:1,offset:0,limit:50,topics:["History"],markets:["de"],rows:[{sample_video_count:null,report_state:"not_collected",independent_trend_available:false}]};
    const result=await marketEvidence(id,{market:"de",days:90},async(url,request)=>{
      assert.equal(url,"https://niihqywncuwxfxipkgte.supabase.co/rest/v1/rpc/fasulye_market_evidence");
      assert.deepEqual(JSON.parse(request.body),{p_batch_id:id,p_topic:null,p_market:"de",p_days:90,p_offset:0,p_limit:50});
      return Response.json(payload);
    });
    assert.deepEqual(result,payload);
    await assert.rejects(()=>marketEvidence(id,{days:12}),{status:400});
    await assert.rejects(()=>marketEvidence(id,{limit:101}),{status:400});
    await assert.rejects(()=>marketEvidence(id,{},async()=>Response.json(null)),{status:404});
  }finally{delete process.env.SUPABASE_SECRET_KEY;}
});
