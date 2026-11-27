import { z } from "zod";
import { ResearchError } from "./research.mjs";
const currencies=new Set(Intl.supportedValuesOf("currency"));
const currency=z.string().refine(c=>currencies.has(c),"ISO currency required");
const amount=z.number().finite().min(0).max(10000000), count=z.number().int().min(0).max(1000000000);
const band=field=>z.strictObject({low:field,base:field,high:field}).refine(x=>x.low<=x.base&&x.base<=x.high,"Low/base/high must be ordered");
const costs=z.strictObject({research_hours:band(amount),hourly_rate:band(amount),translation:band(amount),voice:band(amount),visuals:band(amount),editing:band(amount),other:band(amount)});
const line=z.strictObject({label:z.string().trim().min(1).max(160),format:z.enum(["shorts","long_form"]),videos:z.number().int().min(0).max(1000),currency,rpm:band(amount),rpm_basis:z.string().trim().min(1).max(1000),rpm_kind:z.enum(["owner_assumption","owner_actual","third_party_estimate"]),view_targets:band(count),costs,cost_basis:z.string().trim().min(1).max(1000)});
export const monthlyPlanSchema=z.strictObject({currency,monthly_budget:amount,monthly_fixed:band(amount),lines:z.array(line).min(1).max(12)});
const bands=["low","base","high"],money=n=>Math.round((n+Number.EPSILON)*100)/100;
function breakEven(cost,rpm){return cost===0?0:rpm===0?null:Math.ceil(cost*1000/rpm);}
export function monthlyEconomics(input){
 const p=monthlyPlanSchema.safeParse(input);
 if(!p.success)throw new ResearchError(400,"Bütçe, para birimi veya düşük/orta/yüksek senaryo geçersiz.");
 const x=p.data;
 if(x.lines.some(l=>l.currency!==x.currency))throw new ResearchError(400,"Para birimleri karıştırılamaz; önce kendi dönüşümünüzü belgeleyin.");
 const lines=x.lines.map(l=>{
  const cost=Object.fromEntries(bands.map(k=>[k,money(l.costs.research_hours[k]*l.costs.hourly_rate[k]+["translation","voice","visuals","editing","other"].reduce((sum,c)=>sum+l.costs[c][k],0))]));
  const revenue=Object.fromEntries(bands.map(k=>[k,money(l.rpm[k]*l.view_targets[k]/1000)]));
  return {...l,cost_per_video:cost,revenue_per_video:revenue,profit_per_video:{low:money(revenue.low-cost.high),base:money(revenue.base-cost.base),high:money(revenue.high-cost.low)},break_even_views:{low:breakEven(cost.high,l.rpm.low),base:breakEven(cost.base,l.rpm.base),high:breakEven(cost.low,l.rpm.high)}};
 });
 const totalCosts=Object.fromEntries(bands.map(k=>[k,money(x.monthly_fixed[k]+lines.reduce((s,l)=>s+l.videos*l.cost_per_video[k],0))]));
 const totalRevenue=Object.fromEntries(bands.map(k=>[k,money(lines.reduce((s,l)=>s+l.videos*l.revenue_per_video[k],0))]));
 return {currency:x.currency,monthly_budget:x.monthly_budget,monthly_fixed:x.monthly_fixed,lines,monthly_costs:totalCosts,monthly_revenue:totalRevenue,monthly_profit:{low:money(totalRevenue.low-totalCosts.high),base:money(totalRevenue.base-totalCosts.base),high:money(totalRevenue.high-totalCosts.low)},budget_remaining:{low:money(x.monthly_budget-totalCosts.high),base:money(x.monthly_budget-totalCosts.base),high:money(x.monthly_budget-totalCosts.low)},budget_exceeded_at_base:totalCosts.base>x.monthly_budget,limitations:["Hypothetical owner production and revenue scenarios only; no competitor views or estimated competitor earnings.","Shorts targets must be the applicable engaged views, long-form targets ordinary views; neither is predicted.","Not statistical confidence bounds. Pre-tax; fixed costs not included in per-video break-even."]};
}
export function rpmProvenance(row,now=new Date()){
 const warnings=[];
 if(!row.source_date)warnings.push("source_publication_date_unknown");
 if(!row.source_checked_at)warnings.push("source_review_date_unknown");
 else if(now.getTime()-Date.parse(row.source_checked_at+"T00:00:00Z")>90*86400000)warnings.push("source_review_due");
 if(row.source_date&&now.getTime()-Date.parse(row.source_date+"T00:00:00Z")>365*86400000)warnings.push("source_older_than_one_year");
 if(row.reliability==="unspecified"||!row.reliability)warnings.push("methodology_unspecified");
 if(row.reliability!=="owner_actual")warnings.push("not_verified_creator_earnings");
 if(/RevenueLab/i.test(row.source??""))warnings.push("third_party_model_currency_and_sample_need_confirmation");
 if(/AIR Media-Tech/i.test(row.source??""))warnings.push("third_party_sample_country_method_and_size_need_confirmation");
 return {status:warnings.length?"review_required":"owner_declared",warnings,verified_earnings:false};
}
