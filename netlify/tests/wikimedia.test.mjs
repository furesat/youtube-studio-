import assert from "node:assert/strict";
import {test} from "node:test";
import {WikimediaProvider,searchWiki,normalizePageviews} from "../lib/wikimedia.mjs";
const now=()=>new Date("2026-11-27T00:00:00Z");
const input={language:"de",topic:"Fork",page_id:42,start:"2026-11-23",end:"2026-11-25"};
const meta={query:{pages:[{pageid:42,ns:0,title:"Gabel (Werkzeug)"}]}};
const item={project:"de.wikipedia",article:"Gabel_(Werkzeug)",access:"all-access",agent:"user",granularity:"daily",timestamp:"2026112300",views:0};
test("manual candidate search returns no automatic selection",async()=>{
 const p=await searchWiki({language:"de",query:"Gabel"},async(url,req)=>{
  assert.match(url,/^https:\/\/de\.wikipedia\.org\/w\/api\.php/);
  assert.match(req.headers["User-Agent"],/Fasulye/);
  return Response.json({query:{search:[{pageid:42,title:"Gabel"}]}});
 });
 assert.equal(p.results[0].page_id,42);
 await assert.rejects(()=>searchWiki({language:"../../host",query:"x"},()=>assert.fail()),{status:400});
});
test("pageview collection preserves explicit zero and missing days",async()=>{
 const p=await new WikimediaProvider(async(url)=>{
  if(url.includes("/w/api.php"))return Response.json(meta);
  assert.match(url,/^https:\/\/wikimedia\.org\/api\/rest_v1\/metrics\/pageviews\/per-article\/de\.wikipedia\/all-access\/user\//);
  return Response.json({items:[item]});
 },now).collect(input);
 assert.deepEqual(p.series.map(r=>r.views),[0,null,null]);
 assert.equal(p.region,null);assert.equal(p.license,"CC0-1.0");assert.equal(p.evidence_type,"general_public_interest");
});
test("unavailable providers, ambiguity and malformed observations never fabricate data",async()=>{
 await assert.rejects(()=>new WikimediaProvider(async()=>new Response("",{status:429}),now).collect(input),{status:429});
 await assert.rejects(()=>new WikimediaProvider(async()=>Response.json({query:{pages:[{...meta.query.pages[0],pageprops:{disambiguation:""}}]}}),now).collect(input),{status:400});
 assert.throws(()=>normalizePageviews({items:[item,item]},["2026-11-23"],"de.wikipedia",item.article),{status:502});
 await assert.rejects(()=>new WikimediaProvider(()=>assert.fail(),now).collect({...input,end:"2026-11-27"}),{status:400});
});
