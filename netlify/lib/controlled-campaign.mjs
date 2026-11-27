/** Pure controlled campaign planner. No external calls. */
export function controlledProfiles(axis,variant){
 if(!["window","order","variant"].includes(axis)||![0,1].includes(variant))throw new Error("invalid controlled profile");
 if(axis==="window")return [365,90,30,7].map(days=>({days,order:"relevance",variant}));
 if(axis==="order")return ["relevance","date","viewCount"].map(order=>({days:90,order,variant}));
 return [0,1].map(v=>({days:90,order:"relevance",variant:v}));
}

export function buildControlled(campaign,markets,{axis="window",variant=0,anchor}){
 const parsed=new Date(anchor);
 if(typeof anchor!=="string"||!Number.isFinite(parsed.getTime())||parsed.toISOString()!==anchor)throw new Error("invalid anchor");
 const tasks=[],missing=[],seen=new Set();
 for(const profile of controlledProfiles(axis,variant))for(const category of campaign)for(const m of markets){
   const query=category.queries[m.language]?.[profile.variant];
   if(!query){missing.push({topic:category.label,market_id:m.id,language:m.language,variant:profile.variant,lookback_days:profile.days,search_order:profile.order});continue;}
   const q=query.normalize("NFC").trim();
   const k=JSON.stringify([q,m.region,m.language,profile.days,profile.order]);
   if(seen.has(k))continue;
   seen.add(k);
   tasks.push({topic:category.label,query:q,region:m.region,language:m.language,market_id:m.id,lookback_days:profile.days,search_order:profile.order,methodology_version:"controlled-v1",comparison_axis:axis,query_variant:profile.variant,window_anchor:anchor});
 }
 return {tasks,missing,methodology:{version:"controlled-v1",axis,anchor,sample_only:true,viewer_geography:"unknown",pages_per_query:1,results_per_page:50,limitation:"Fixed publication bounds do not freeze live YouTube ranking or metadata."}};
}
