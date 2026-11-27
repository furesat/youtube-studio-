import { z } from "zod";
import { db } from "./batch.mjs";
import { env, ResearchError } from "./research.mjs";
const id=z.uuid(),task_id=z.number().int().positive().max(Number.MAX_SAFE_INTEGER).optional();
export const queueControlSchema=z.discriminatedUnion("action",[
 z.strictObject({id,action:z.literal("pause")}),
 z.strictObject({id,action:z.literal("resume")}),
 z.strictObject({id,action:z.literal("cancel"),task_id,confirm:z.literal(true)}),
 z.strictObject({id,action:z.literal("retry_failed"),task_id,confirm:z.literal(true)}),
 z.strictObject({id,action:z.literal("priority"),task_id,priority:z.number().int().min(-10).max(10)})
]);
export function featureFlags(){
 return {queue_controls:env("FASULYE_QUEUE_CONTROLS")==="1",controlled_campaigns:env("FASULYE_CONTROLLED_CAMPAIGNS")==="1",wikimedia_evidence:env("FASULYE_WIKIMEDIA_EVIDENCE")==="1",editorial_workflow:env("FASULYE_EDITORIAL_WORKFLOW")==="1"};
}
function enabled(){if(!featureFlags().queue_controls)throw new ResearchError(503,"Gelişmiş kuyruk yönetimi henüz etkin değil.");}
export async function controlQueue(input,fetcher=fetch){
 enabled();
 const parsed=queueControlSchema.safeParse(input);
 if(!parsed.success)throw new ResearchError(400,"Kuyruk işlemi veya açık onay geçersiz.");
 const x=parsed.data;
 const result=await db("rpc/fasulye_queue_control",{method:"POST",body:{p_batch_id:x.id,p_action:x.action,p_task_id:x.task_id??null,p_priority:x.priority??null},fetcher});
 if(result===null)throw new ResearchError(404,"Grup veya görev bulunamadı.");
 if(!result||!Number.isInteger(result.changed)||result.changed<0||result.batch_id!==x.id)throw new ResearchError(502,"Kuyruk değişikliği doğrulanamadı.");
 return result;
}
export async function queueHealth(fetcher=fetch,now=new Date()){
 enabled();
 const data=await db("rpc/fasulye_queue_health",{method:"POST",body:{},fetcher});
 if(!data||typeof data!=="object"||!data.counts||!Array.isArray(data.workers))throw new ResearchError(502,"Kuyruk sağlığı yanıtı geçersiz.");
 const features=featureFlags();
 const detailEnabled=env("FASULYE_SHARED_DETAIL_BUDGET")==="1";
 const parts=Object.fromEntries(new Intl.DateTimeFormat("en-US",{timeZone:"America/Los_Angeles",year:"numeric",month:"2-digit",day:"2-digit"}).formatToParts(now).map(p=>[p.type,p.value]));
 const day=parts.year+"-"+parts.month+"-"+parts.day;
 const query=(table,params)=>db(table+"?"+new URLSearchParams(params),{fetcher});
 const [fresh,completed,detail]=await Promise.allSettled([
  query("fasulye_reports",{select:"collected_at,expires_at",expires_at:"gt."+now.toISOString(),order:"collected_at.desc",limit:"1"}),
  query("fasulye_tasks",{select:"updated_at",status:"eq.done",source_task_id:"is.null",updated_at:"not.is.null",order:"updated_at.desc",limit:"1"}),
  detailEnabled?query("fasulye_detail_budget",{select:"videos,channels,playlist_items",day:"eq."+day,limit:"1"}):Promise.resolve(null)
 ]);
 const rows=r=>r.status==="fulfilled"&&Array.isArray(r.value)?r.value:null;
 const last=rows(fresh),done=rows(completed),counts=rows(detail);
 const detailCounts=counts===null?null:counts[0]??{videos:0,channels:0,playlist_items:0};
 const validDetails=detailCounts&&["videos","channels","playlist_items"].every(k=>Number.isSafeInteger(detailCounts[k])&&detailCounts[k]>=0);
 const total=validDetails?detailCounts.videos+detailCounts.channels+detailCounts.playlist_items:null;
 return {...data,software_version:"4.0-draft",database:"reachable",features:{...features,shared_detail_budget:detailEnabled},
  worker_telemetry:data.workers.map(w=>({...w,heartbeat_age_seconds:Number.isFinite(Date.parse(w.heartbeat_at))?Math.max(0,Math.floor((now.getTime()-Date.parse(w.heartbeat_at))/1000)):null})),
  report_freshness:last===null?{status:"unavailable"}:last.length?{status:"available",...last[0]}:{status:"no_unexpired_report"},
  last_completed_task:done===null?{status:"unavailable"}:done.length?{status:"observed",at:done[0].updated_at}:{status:"no_record"},
  detail_reservations:{status:!detailEnabled?"disabled":total===null?"unavailable":"observed",day,limit:6000,reserved:total,by_endpoint:validDetails?detailCounts:null},
  provider_status:{google_trends_api:"awaiting_approved_access",wikimedia:features.wikimedia_evidence?"configured_not_live_checked":"disabled",youtube:"not_live_checked"},
  scope:"Application reservation and worker telemetry, not upstream Google quota. A heartbeat timestamp is not proof of an active worker."};
}
