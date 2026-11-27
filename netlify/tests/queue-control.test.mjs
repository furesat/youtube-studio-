import assert from "node:assert/strict";
import {test} from "node:test";
import {controlQueue,queueHealth} from "../lib/queue-control.mjs";
const id="00000000-0000-4000-8000-000000000001";
test("queue actions require feature enablement and explicit confirmation",async()=>{
 await assert.rejects(()=>controlQueue({id,action:"pause"},()=>assert.fail()),{status:503});
 process.env.FASULYE_QUEUE_CONTROLS="1";process.env.SUPABASE_SECRET_KEY="sb_secret_test";
 try{
  await assert.rejects(()=>controlQueue({id,action:"cancel"},()=>assert.fail()),{status:400});
  await assert.rejects(()=>controlQueue({id,action:"priority",priority:11},()=>assert.fail()),{status:400});
  const result=await controlQueue({id,action:"retry_failed",task_id:12,confirm:true},async(url,req)=>{
   assert.match(url,/\/rpc\/fasulye_queue_control$/);
   assert.deepEqual(JSON.parse(req.body),{p_batch_id:id,p_action:"retry_failed",p_task_id:12,p_priority:null});
   return Response.json({batch_id:id,action:"retry_failed",changed:1,quota_refunded:false});
  });
  assert.equal(result.changed,1);assert.equal(result.quota_refunded,false);
  const h=await queueHealth(async(url,req)=>{
   if(url.includes("/rpc/fasulye_queue_health"))return Response.json({counts:{queued:1},workers:[],reserved_today:5});
   assert.match(url,/\/fasulye_(reports|tasks)\?/);return Response.json([]);
  });
  assert.equal(h.reserved_today,5);assert.equal(h.provider_status.google_trends_api,"awaiting_approved_access");
 }finally{delete process.env.FASULYE_QUEUE_CONTROLS;delete process.env.SUPABASE_SECRET_KEY;}
});

test("health distinguishes unavailable, empty and observed records without quota use",async()=>{
 process.env.FASULYE_QUEUE_CONTROLS="1";process.env.FASULYE_SHARED_DETAIL_BUDGET="1";process.env.SUPABASE_SECRET_KEY="sb_secret_test";
 try{
  const h=await queueHealth(async(url,req)=>{
   if(url.includes("/rpc/fasulye_queue_health"))return Response.json({counts:{queued:1},workers:[{heartbeat_at:"2026-11-27T00:00:00Z"}],reserved_today:2});
   assert.equal(req.method,"GET");
   if(url.includes("/fasulye_reports?"))return new Response(null,{status:503});
   if(url.includes("/fasulye_tasks?"))return Response.json([]);
   assert.match(url,/fasulye_detail_budget/);assert.equal(new URL(url).searchParams.get("day"),"eq.2026-11-26");
   return Response.json([{videos:3,channels:2,playlist_items:1}]);
  },new Date("2026-11-27T00:02:00Z"));
  assert.equal(h.database,"reachable");assert.equal(h.report_freshness.status,"unavailable");
  assert.equal(h.last_completed_task.status,"no_record");assert.equal(h.detail_reservations.reserved,6);
  assert.equal(h.worker_telemetry[0].heartbeat_age_seconds,120);assert.equal(h.provider_status.youtube,"not_live_checked");
 }finally{delete process.env.FASULYE_QUEUE_CONTROLS;delete process.env.FASULYE_SHARED_DETAIL_BUDGET;delete process.env.SUPABASE_SECRET_KEY;}
});
