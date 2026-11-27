import { z } from "zod";
import { db } from "./batch.mjs";
import { env, ResearchError } from "./research.mjs";
import { assessEvidence,evidenceQualitySchema } from "./evidence-quality.mjs";
import { parseOwnerCsv } from "./first-party-analytics.mjs";
const note=z.string().trim().min(1).max(4000);
const amount=z.number().finite().min(0).max(10000000);
export const stages=["discovered","sources_collected","demand_evaluated","coverage_reviewed","angle_validated","cost_estimated","experiment_ready","experiment_completed","long_form_decision"];
const evidence=evidenceQualitySchema;
const claim=z.strictObject({claim:note,kind:z.enum(["verified_fact","creative_storytelling","unverified"]),source_url:z.string().url().max(1500).nullable()});
const payloads={
 discovered:z.strictObject({origin:note}),
 sources_collected:z.strictObject({evidence}),
 demand_evaluated:z.strictObject({evidence,conclusion:z.enum(["supports","contradicts","inconclusive"]),reason:note}),
 coverage_reviewed:z.strictObject({manual_review:z.literal(true),method:note,findings:note,limitations:note}),
 angle_validated:z.strictObject({angle:note,claims:z.array(claim).min(1).max(30),original:z.literal(true)}),
 cost_estimated:z.strictObject({currency:z.string().regex(/^[A-Z]{3}$/),research_hours:amount,hourly_rate:amount,translation:amount,voice:amount,visuals:amount,editing:amount,other:amount,basis:note}),
 experiment_ready:z.strictObject({hypothesis:note,format:z.enum(["shorts","long_form"]),primary_metric:note,success_rule:note,observation_days:z.number().int().min(1).max(90),script_outline:note,scene_requirements:note,thumbnail_concept:note,publication_checklist:z.array(note).min(1).max(20),proposed_long_form:note.nullable()}),
 experiment_completed:z.strictObject({published_at:z.iso.datetime({offset:true}),video_reference:note,source:z.literal("owner_youtube_studio_csv"),own_channel:z.literal(true),csv:z.string().min(1).max(300000),evaluation:note,limitations:note}),
 long_form_decision:z.strictObject({decision:z.enum(["go","hold","no_go"]),reason:note,episode_outline:note.nullable()})
};
export const workflowAdvanceSchema=z.strictObject({candidate_id:z.uuid(),candidate_revision:z.number().int().positive(),expected_revision:z.number().int().min(0),stage:z.enum(stages),data:z.record(z.string(),z.unknown()),confirm:z.literal(true)});
export const workflowReadSchema=z.strictObject({candidate_id:z.uuid()});
const enabled=()=>{if(env("FASULYE_EDITORIAL_WORKFLOW")!=="1")throw new ResearchError(503,"Editoryal iş akışı henüz etkin değil.");};
function validate(schema,input){const p=schema.safeParse(input);if(!p.success)throw new ResearchError(400,"Geçersiz iş akışı alanı: "+(p.error.issues[0]?.path.join(".")||"istek"));return p.data;}
export function prepareStage(input,history,now=new Date()){
 const x=validate(workflowAdvanceSchema,input);
 if(x.expected_revision!==history.length||stages[history.length]!==x.stage)throw new ResearchError(409,"Geçersiz veya eski iş akışı aşaması.");
 let data=validate(payloads[x.stage],x.data);
 if(x.stage==="sources_collected"||x.stage==="demand_evaluated"){
  const assessment=assessEvidence(data.evidence,now);
  if(!assessment.sources.length)throw new ResearchError(400,"Bağımsız kaynak gerekli.");
  if(x.stage==="demand_evaluated"&&data.conclusion!=="inconclusive"){
   if(!assessment.sources.some(s=>["general_interest","search_interest","youtube_demand"].includes(s.type)&&s.direction===data.conclusion&&s.credibility!=="unverified"))throw new ResearchError(400,"Talep hipotezi için ilgili, incelenmiş kaynak gerekli.");
  }
  data={...data,evidence:assessment};
 }
 if(x.stage==="angle_validated"){
  const links=new Set(history.flatMap(e=>e.data?.evidence?.sources??[]).map(s=>s.url));
  for(const c of data.claims){
   if(c.kind==="verified_fact"){
    if(!c.source_url||!links.has(new URL(c.source_url).href))throw new ResearchError(400,"Doğrulanmış olgu için önceki kaynak kaydı gerekli.");
   }
  }
  if(data.claims.some(c=>c.kind==="unverified"))throw new ResearchError(400,"Doğrulanmamış iddialar hazır açı olarak işaretlenemez.");
 }
 if(x.stage==="cost_estimated")data={...data,total:data.research_hours*data.hourly_rate+data.translation+data.voice+data.visuals+data.editing+data.other};
 if(x.stage==="experiment_completed"){
  const ready=history.find(e=>e.stage==="experiment_ready");
  if(!ready||Date.parse(data.published_at)<Date.parse(ready.created_at)||Date.parse(data.published_at)>now.getTime())throw new ResearchError(400,"Yayın, kayıtlı deney planından sonra ve geçmişte olmalı.");
  const observations=parseOwnerCsv(data.csv,{publication:data.published_at,now});
  const requiredEnd=new Date(Date.parse(data.published_at)+ready.data.observation_days*86400000).toISOString().slice(0,10);
  if(!observations.some(o=>o.period_end>=requiredEnd))throw new ResearchError(400,"Önceden seçilen gözlem süresi henüz tamamlanmadı.");
  const {csv,...meta}=data;data={...meta,observations,plan_revision:ready.revision,ownership_verified:false};
 }
 if(x.stage==="long_form_decision"&&data.decision==="go"&&!data.episode_outline)throw new ResearchError(400,"Uzun video kararı için özgün bölüm taslağı gerekli.");
 return {...x,data};
}
export function workflowExport(candidate,events){
 const clean=v=>String(v??"").replace(/\r?\n/g," ").replace(/[\\`*_{}\[\]<>#!|]/g,"\\$&");
 const markdown=["# "+clean(candidate.title),"","Aday revizyonu: "+candidate.revision,"İş akışı revizyonu: "+events.length,"",...events.flatMap(e=>["## "+e.revision+". "+e.stage,"","Kayıt: "+e.created_at,"",...Object.entries(e.data).filter(([k])=>k!=="observations").map(([k,v])=>"- "+clean(k)+": "+clean(typeof v==="object"?JSON.stringify(v):v)),""]),"İlk taraf analitik verileri editör tarafından içe aktarılmıştır; otomatik sahiplik doğrulaması veya başarı tahmini değildir."].join("\n");
 return {schema_version:1,candidate,events,markdown,stage:events.at(-1)?.stage??null,next_stage:stages[events.length]??null};
}
export async function readWorkflow(input,fetcher=fetch){
 enabled();const {candidate_id}=validate(workflowReadSchema,input);
 const [c,events]=await Promise.all([db("fasulye_editorial_candidates?"+new URLSearchParams({select:"*",id:"eq."+candidate_id,limit:"1"}),{fetcher}),db("fasulye_editorial_events?"+new URLSearchParams({select:"*",candidate_id:"eq."+candidate_id,order:"revision.asc",limit:"9"}),{fetcher})]);
 if(!c?.length)throw new ResearchError(404,"Aday bulunamadı.");
 return workflowExport(c[0],events);
}
export async function advanceWorkflow(input,fetcher=fetch){
 enabled();const x=validate(workflowAdvanceSchema,input);
 const current=await readWorkflow({candidate_id:x.candidate_id},fetcher);
 if(current.candidate.revision!==x.candidate_revision)throw new ResearchError(409,"Aday revizyonu değişti.");
 const p=prepareStage(x,current.events);
 const result=await db("rpc/fasulye_advance_editorial",{method:"POST",body:{p_candidate_id:p.candidate_id,p_candidate_revision:p.candidate_revision,p_expected_revision:p.expected_revision,p_stage:p.stage,p_data:p.data},fetcher});
 if(result?.conflict)throw new ResearchError(409,"Aday veya iş akışı revizyonu değişti.");
 if(!result?.revision)throw new ResearchError(502,"İş akışı kaydı doğrulanamadı.");
 return result;
}
