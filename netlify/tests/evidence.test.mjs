import assert from "node:assert/strict";
import { test } from "node:test";
import { CsvTrendProvider, GoogleTrendsApiProvider, scoreIndependent, revenueScenarios, profitScenarios, writeEvidence } from "../lib/evidence.mjs";
test("parses single-series Google Trends CSV with censored values",()=>{
  const series=new CsvTrendProvider().parse('\uFEFFCategory: All categories\r\n\r\nWeek,Query: (Germany)\r\n2026-01-04,100\r\n2026-01-11,<1\r\n2026-01-18,0');
  assert.equal(series.length,3);assert.equal(series[0].value,100);assert.equal(series[1].value,null);assert.equal(series[1].below_one,true);assert.equal(series[2].value,0);
  assert.throws(()=>new CsvTrendProvider().parse("Week,A,B\n2026-01-04,10,20"));
  assert.throws(()=>new CsvTrendProvider().parse("Week,A\n2026-02-31,10"));
  assert.throws(()=>new CsvTrendProvider().parse("Week,A\n2026-01-04,101"));
});
test("no invented scoring or API data",async()=>{
  assert.equal(scoreIndependent({}).score,null);
  assert.equal(scoreIndependent({demand:100}).confidence,"low");
  assert.equal(scoreIndependent({demand:100,gap:100,competition:0,revenue:100,cost:0,cultural_fit:100,long_term:100}).score,100);
  assert.equal(new GoogleTrendsApiProvider().status(),"awaiting_approved_api_access");
  await assert.rejects(()=>new GoogleTrendsApiProvider().fetch({}),{status:503});
});
test("independent RPM calculations use four targets",()=>{
  const r=revenueScenarios({format:"shorts",currency:"USD",source:"unit test",low:0,base:.1,high:.2});
  assert.deepEqual(r.map(x=>x.views),[10000,100000,1000000,10000000]);
  assert.equal(r[3].base,1000);
});
test("source is mandatory and invalid RPM order never reaches database",async()=>{
  await assert.rejects(()=>writeEvidence({kind:"rpm",market_id:"tr",format:"shorts",currency:"USD",low:3,base:2,high:1,source:"unit test"},()=>assert.fail("Unexpected DB call")),{status:400});
});

test("profit estimates use independent costs and do not silently convert currencies",()=>{
  const rpm={format:"shorts",currency:"USD",source:"unit test",low:0,base:.1,high:.2};
  const cost={currency:"USD",voice:5,visuals:10,translation:0,editing:5,other:0};
  assert.equal(profitScenarios(rpm,cost)[0].profit.base,-19);
  assert.equal(profitScenarios(rpm,{...cost,currency:"EUR"})[0].profit,null);
  assert.equal(profitScenarios(rpm,null)[0].profit,null);
});
