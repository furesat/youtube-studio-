import {test} from "node:test";
import assert from "node:assert/strict";
import {assessEvidence} from "../lib/evidence-quality.mjs";
const date=new Date("2026-11-27T00:00:00Z");
const base={url:"https://example.test/a",publisher:"Fixture",checked_on:"2026-01-01",type:"historical_context",credibility:"primary",independence_group:"archive",direction:"contradicts",finding:"Fixture",methodology:"Archive inspection",limitations:"Fixture only",region:null,language:"en",license:null};
test("distinguishes coverage, contradiction, stale evidence and unknown demand",()=>{
 const r=assessEvidence({topic:"Topic",hypothesis:"Hypothesis",sources:[base,{...base,url:"https://example.test/b"}]},date);
 assert.equal(r.types.historical_context.independence_groups,1);
 assert.equal(r.types.historical_context.stale_sources,2);
 assert.equal(r.types.historical_context.contradictions.length,2);
 assert.equal(r.types.youtube_demand.coverage,"unknown");
 assert.equal(r.statistical_confidence,null);
 assert.equal(r.success_probability,null);
});
test("rejects repeated, future and credential-bearing sources",()=>{
 for(const sources of [[base,base],[{...base,checked_on:"2027-01-01"}],[{...base,url:"https://user:example@example.test/a"}]])
  assert.throws(()=>assessEvidence({topic:"Topic",hypothesis:"Hypothesis",sources},date),{status:400});
});
