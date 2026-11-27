import {test} from "node:test";
import assert from "node:assert/strict";
import {prepareStage,workflowExport} from "../lib/editorial-workflow.mjs";
import {parseOwnerCsv} from "../lib/first-party-analytics.mjs";
const id="00000000-0000-4000-8000-000000000001";
const head="metric,period_start,period_end,value,unit,dimension_type,dimension_value\n";
const csv=head+"ctr,2026-11-02,2026-11-10,0,percent,none,\nviews,2026-11-02,2026-11-10,,count,none,";
const now=new Date("2026-11-27T00:00:00Z");
test("owner CSV preserves zero and unknown, checks dates and duplicates",()=>{
 const r=parseOwnerCsv(csv,{now});
 assert.equal(r[0].value,0);assert.equal(r[1].value,null);
 assert.throws(()=>parseOwnerCsv(csv+"\n"+csv.split("\n")[1],{now}),{status:400});
 assert.throws(()=>parseOwnerCsv(csv.replace("0,percent","105,percent"),{now}),{status:400});
 assert.throws(()=>parseOwnerCsv(csv,{now,publication:"2026-11-03T00:00:00Z"}),{status:400});
});
const request=(stage,revision,data)=>({candidate_id:id,candidate_revision:1,expected_revision:revision,stage,data,confirm:true});
test("stage order, source gates and no skipped decisions",()=>{
 const start=prepareStage(request("discovered",0,{origin:"Independent idea"}),[],now);
 assert.equal(start.stage,"discovered");
 assert.throws(()=>prepareStage(request("long_form_decision",0,{decision:"go",reason:"Fixture",episode_outline:"Outline"}),[],now),{status:409});
 assert.throws(()=>prepareStage(request("sources_collected",1,{evidence:{topic:"Topic",hypothesis:"Hypothesis",sources:[]}}),[{stage:"discovered"}],now),{status:400});
 const r=workflowExport({title:"Fixture",revision:1},[]);
 assert.equal(r.next_stage,"discovered");assert.match(r.markdown,/Aday revizyonu/);
});
test("preregistered owner experiment cannot record before publication or bypass planned interval",()=>{
 const history=Array.from({length:7},(_,i)=>({revision:i+1,stage:i===6?"experiment_ready":"earlier",created_at:"2026-11-01T00:00:00Z",data:{observation_days:7}}));
 const data={published_at:"2026-11-02T00:00:00Z",video_reference:"Owner video",source:"owner_youtube_studio_csv",own_channel:true,csv,evaluation:"Inconclusive",limitations:"Small sample"};
 const p=prepareStage(request("experiment_completed",7,data),history,now);
 assert.equal(p.data.observations[0].value,0);assert.equal(p.data.ownership_verified,false);assert.equal(p.data.csv,undefined);
 assert.throws(()=>prepareStage(request("experiment_completed",7,{...data,published_at:"2026-10-30T00:00:00Z"}),history,now),{status:400});
 assert.throws(()=>prepareStage(request("experiment_completed",7,{...data,csv:csv.replaceAll("2026-11-10","2026-11-03")}),history,now),{status:400});
});
