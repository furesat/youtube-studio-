import { ResearchError } from "./research.mjs";
const fail=message=>{throw new ResearchError(400,message)};
export const metricUnits={impressions:"count",ctr:"percent",audience_retention:"percent",average_view_duration:"seconds",returning_viewers:"count",traffic_sources:"count",viewer_geography:"count",watch_time:"hours",revenue:"currency",views:"count"};
const header=["metric","period_start","period_end","value","unit","dimension_type","dimension_value"];
function rows(csv){
 const output=[];let row=[],cell="",state="start";
 const push=()=>{row.push(cell);cell="";state="start";};
 const line=()=>{push();if(row.some(v=>v.trim()))output.push(row);row=[];};
 csv=csv.replace(/^\uFEFF/,"");
 for(let i=0;i<csv.length;i++){
  const c=csv[i];
  if(state==="quoted"){
   if(c==='"'&&csv[i+1]==='"'){cell+='"';i++;}
   else if(c==='"')state="closed";else cell+=c;
  }else if(c===",")push();
  else if(c==="\r"||c==="\n"){if(c==="\r"&&csv[i+1]==="\n")i++;line();}
  else if(c==='"'&&state==="start")state="quoted";
  else{if(state==="closed"||c==='"')fail("CSV quote syntax invalid.");cell+=c;state="plain";}
 }
 if(state==="quoted")fail("CSV quote not closed.");
 if(cell||row.length||state!=="start")line();
 return output;
}
function date(s){const d=new Date(s+"T00:00:00Z");return /^\d{4}-\d{2}-\d{2}$/.test(s)&&Number.isFinite(d.getTime())&&d.toISOString().slice(0,10)===s;}
export function parseOwnerCsv(csv,{publication,now=new Date()}={}){
 if(typeof csv!=="string"||Buffer.byteLength(csv)>300000)fail("CSV missing or too large.");
 const data=rows(csv);
 if(JSON.stringify(data.shift())!==JSON.stringify(header)||!data.length||data.length>5000)fail("Use the documented normalized analytics CSV header and 1-5000 rows.");
 const seen=new Set(),out=[];
 for(const raw of data){
  if(raw.length!==header.length)fail("CSV row width invalid.");
  const [metric,start,end,value,unit,dimensionType,dimensionValue]=raw.map(s=>s.trim());
  if(!Object.hasOwn(metricUnits,metric)||!date(start)||!date(end)||start>end||end>now.toISOString().slice(0,10)||publication&&start<publication.slice(0,10))fail("Metric or observation date invalid.");
  const expected=metricUnits[metric];
  if(expected==="currency"?!/^[A-Z]{3}$/.test(unit):unit!==expected)fail("Metric unit invalid.");
  if(!["none","traffic_source","country","elapsed_seconds"].includes(dimensionType)||dimensionValue.length>120||/[\u0000-\u001f]/.test(dimensionValue))fail("Dimension invalid.");
  if(dimensionType==="none"&&dimensionValue||dimensionType!=="none"&&!dimensionValue)fail("Dimension value invalid.");
  if(metric==="traffic_sources"&&dimensionType!=="traffic_source"||metric==="viewer_geography"&&(dimensionType!=="country"||! /^[A-Z]{2}$/.test(dimensionValue))||metric==="audience_retention"&&(dimensionType!=="elapsed_seconds"||!/^\d{1,6}$/.test(dimensionValue)))fail("Metric requires its documented dimension.");
  if(!["traffic_sources","viewer_geography","audience_retention"].includes(metric)&&dimensionType!=="none")fail("Unexpected metric dimension.");
  if(value!==""&&!/^-?\d+(?:\.\d+)?$/.test(value))fail("Metric value invalid.");
  const n=value===""?null:Number(value);
  if(n!==null&&(!Number.isFinite(n)||Math.abs(n)>1e12||expected!=="currency"&&n<0||expected==="count"&&!Number.isSafeInteger(n)||metric==="ctr"&&n>100))fail("Metric value outside valid range.");
  const key=JSON.stringify([metric,start,end,unit,dimensionType,dimensionValue]);
  if(seen.has(key))fail("Duplicate observation.");
  seen.add(key);out.push({metric,period_start:start,period_end:end,value:n,unit,dimension_type:dimensionType,dimension_value:dimensionValue||null});
 }
 if(!out.some(r=>r.value!==null))fail("At least one known observation is required.");
 return out;
}
