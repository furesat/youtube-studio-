import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { test } from "node:test";

test("dashboard JavaScript parses and all static DOM bindings exist",()=>{
  execFileSync(process.execPath,["--check","web/app.js"]);
  const html=readFileSync("web/index.html","utf8");
  const js=readFileSync("web/app.js","utf8");
  const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(new Set(ids).size,ids.length);
  for(const [,id] of js.matchAll(/\bel\("([a-z0-9-]+)"\)/g))assert.ok(ids.includes(id),"Missing HTML element: "+id);
  for(const id of ["batch-form","batch-preview","batch-submit","batch-progress","trend-form","rpm-form","review-form","system-check","video-comparison","page-editorial","editorial-form","editorial-source-template"])assert.ok(ids.includes(id));
  assert.doesNotMatch(html+js,/sb_secret_[a-z0-9_]{12,}/i);
});
