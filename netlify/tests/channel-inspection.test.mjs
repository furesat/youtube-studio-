import {test} from "node:test";
import assert from "node:assert/strict";
import {inspectSamples} from "../lib/channel-inspection.mjs";
const report={collected_at:"2026-11-25T00:00:00Z",channel_samples:[{channel_id:"a",current_subscribers:20,videos:[{video_id:"x",published_at:"2026-11-01T00:00:00Z",duration:"PT30S",views:0,audio_language:"de"},{video_id:"y",published_at:"2026-11-10T00:00:00Z",duration:"PT5M",views:null},{video_id:"z",published_at:null,duration:null,views:10}]}]};
const now=new Date("2026-11-27T00:00:00Z");
test("raw channel filters preserve zero and unknown, and never classify Shorts",()=>{
 const r=inspectSamples(report,{id:"123",start:"2026-11-01",end:"2026-11-05",duration:"short",language:"de"},now);
 assert.equal(r.total_sample,1);assert.equal(r.videos[0].views,0);assert.equal(r.videos[0].format_classification,"unverified");
 assert.equal(r.videos[0].subscriber_observed_at,report.collected_at);
 assert.equal(inspectSamples(report,{id:"123",duration:"unknown"},now).videos[0].video_id,"z");
 const page=inspectSamples(report,{id:"123",sort:"views",limit:1},now);assert.equal(page.next_offset,1);assert.equal(page.videos[0].video_id,"z");
});
test("expired sample and reversed dates are rejected",()=>{
 assert.throws(()=>inspectSamples(report,{id:"123"},new Date("2026-12-26")), {status:404});
 assert.throws(()=>inspectSamples(report,{id:"123",start:"2026-11-10",end:"2026-11-01"},now),{status:400});
 assert.throws(()=>inspectSamples({...report,collected_at:"invalid"},{id:"123"},now),{status:404});
});
