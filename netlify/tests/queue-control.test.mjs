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
   assert.match(url,/\/rpc\/fasulye_queue_health$/);
   return Response.json({counts:{queued:1},workers:[],reserved_today:5});
  });
  assert.equal(h.reserved_today,5);assert.equal(h.provider_status.google_trends_api,"awaiting_approved_access");
 }finally{delete process.env.FASULYE_QUEUE_CONTROLS;delete process.env.SUPABASE_SECRET_KEY;}
});
