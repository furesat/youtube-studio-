import assert from "node:assert/strict";
import {test} from "node:test";
import {buildControlled} from "../lib/controlled-campaign.mjs";
import {planBatch} from "../lib/batch.mjs";
const anchor="2026-11-27T00:00:00.000Z";
const cat=[{label:"History",queries:{de:["eins","zwei"]}}], markets=[{id:"de",region:"DE",language:"de"}];
test("controlled windows hold query, order and anchor constant",()=>{
 const p=buildControlled(cat,markets,{anchor});
 assert.deepEqual(p.tasks.map(t=>t.lookback_days),[365,90,30,7]);
 assert.equal(new Set(p.tasks.map(t=>t.query)).size,1);
 assert.ok(p.tasks.every(t=>t.search_order==="relevance"&&t.window_anchor===anchor));
});
test("order and variant campaigns change only their declared axis",()=>{
 const p=buildControlled(cat,markets,{anchor,axis:"order"});
 assert.equal(new Set(p.tasks.map(t=>t.search_order)).size,3);
 assert.ok(p.tasks.every(t=>t.lookback_days===90&&t.query==="eins"));
 const v=buildControlled(cat,markets,{anchor,axis:"variant"});
 assert.deepEqual(v.tasks.map(t=>t.query),["eins","zwei"]);
 assert.ok(v.tasks.every(t=>t.lookback_days===90&&t.search_order==="relevance"));
});
test("missing language is not a zero observation",()=>{
 const p=buildControlled(cat,[{id:"tr",region:"TR",language:"tr"}],{anchor});
 assert.equal(p.tasks.length,0);assert.equal(p.missing.length,4);
});
test("legacy campaign stays unchanged and controlled plan is opt-in",()=>{
 assert.equal(planBatch({mode:"campaign"}).tasks.length,320);
 const p=planBatch({mode:"controlled",countries:["DE"],categories:["history"],comparison_axis:"window",window_anchor:anchor});
 assert.equal(p.tasks.length,4);assert.equal(p.methodology.version,"controlled-v1");
});
