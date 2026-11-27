import {test} from "node:test";
import assert from "node:assert/strict";
import {monthlyEconomics,rpmProvenance} from "../lib/economics.mjs";
const b=(low,base,high)=>({low,base,high}),zero=b(0,0,0);
const line={label:"Owner plan",format:"shorts",videos:4,currency:"EUR",rpm:b(0,.1,.2),rpm_basis:"Owner assumption",rpm_kind:"owner_assumption",view_targets:b(10000,100000,1000000),costs:{research_hours:b(1,2,3),hourly_rate:b(5,10,15),translation:zero,voice:b(1,2,3),visuals:zero,editing:zero,other:zero},cost_basis:"Fixture"};
test("monthly downside uses high cost and low revenue; zero RPM gives unknown break-even",()=>{
 const r=monthlyEconomics({currency:"EUR",monthly_budget:100,monthly_fixed:b(0,5,10),lines:[line]});
 assert.deepEqual(r.monthly_costs,b(24,93,202));assert.deepEqual(r.monthly_revenue,b(0,40,800));
 assert.deepEqual(r.monthly_profit,b(-202,-53,776));assert.equal(r.lines[0].break_even_views.low,null);assert.equal(r.lines[0].break_even_views.base,220000);
 assert.equal(r.budget_exceeded_at_base,false);
});
test("rejects currency mix, invalid code and reversed assumptions",()=>{
 for(const bad of [{...line,currency:"USD"},{...line,currency:"ZZZ"},{...line,rpm:b(2,1,3)}])
  assert.throws(()=>monthlyEconomics({currency:"EUR",monthly_budget:100,monthly_fixed:zero,lines:[bad]}),{status:400});
});
test("external benchmark cannot become verified earnings",()=>{
 const r=rpmProvenance({source:"RevenueLab fixture",reliability:"third_party_model",source_date:null,source_checked_at:"2026-01-01"},new Date("2026-11-27"));
 assert.ok(r.warnings.includes("source_publication_date_unknown"));assert.ok(r.warnings.includes("source_review_due"));assert.equal(r.verified_earnings,false);
});
