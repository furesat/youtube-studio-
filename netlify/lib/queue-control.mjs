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
 return {queue_controls:env("FASULYE_QUEUE_CONTROLS")==="1",controlled_campaigns:env("FASULYE_CONTROLLED_CAMPAIGNS")==="1",wikimedia_evidence:env("FASULYE_WIKIMEDIA_EVIDENCE")==="1"};
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
export async function queueHealth(fetcher=fetch){
 enabled();
 const data=await db("rpc/fasulye_queue_health",{method:"POST",body:{},fetcher});
 if(!data||typeof data!=="object"||!data.counts||!Array.isArray(data.workers))throw new ResearchError(502,"Kuyruk sağlığı yanıtı geçersiz.");
 return {...data,software_version:"4.0-draft",features:featureFlags(),provider_status:{google_trends_api:"awaiting_approved_access",wikimedia:featureFlags().wikimedia_evidence?"configured_not_live_checked":"disabled"},scope:"Application reservation and worker telemetry, not upstream Google quota."};
}
