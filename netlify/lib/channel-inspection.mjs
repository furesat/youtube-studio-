import { z } from "zod";
import {getReport,readSchema,ResearchError} from "./research.mjs";
const day=z.iso.date();
export const channelInspectionSchema=z.strictObject({id:readSchema,channel_id:z.string().min(1).max(128).optional(),start:day.optional(),end:day.optional(),duration:z.enum(["all","short","long","unknown"]).default("all"),language:z.string().min(1).max(32).optional(),sort:z.enum(["date","views"]).default("date"),offset:z.number().int().min(0).default(0),limit:z.number().int().min(1).max(100).default(50)});
function group(duration){
 const m=/^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/.exec(duration??"");
 return !m||!m.slice(1).some(Boolean)?"unknown":Number(m[1]??0)*3600+Number(m[2]??0)*60+Number(m[3]??0)<=180?"short":"long";
}
export function inspectSamples(report,input,now=new Date()){
 const parsed=channelInspectionSchema.safeParse(input);
 if(!parsed.success)throw new ResearchError(400,"Kanal filtresi geçersiz.");
 const x=parsed.data;
 if(x.start&&x.end&&x.start>x.end)throw new ResearchError(400,"Başlangıç bitişten sonra olamaz.");
 const collected=Date.parse(report.collected_at),expiry=report.expires_at?Date.parse(report.expires_at):collected+30*86400000;
 if(!Number.isFinite(collected)||!Number.isFinite(expiry)||expiry<=now.getTime())throw new ResearchError(404,"Raporun saklama süresi doldu veya tarih geçersiz.");
 const channels=(report.channel_samples??[]).filter(c=>!x.channel_id||c.channel_id===x.channel_id);
 const videos=channels.flatMap(c=>(c.videos??[]).filter(v=>{
   const date=v.published_at?.slice(0,10),lang=v.audio_language??v.default_language??"unknown";
   return (!x.start||date&&date>=x.start)&&(!x.end||date&&date<=x.end)&&(x.duration==="all"||group(v.duration)===x.duration)&&(!x.language||lang===x.language);
 }).map(v=>({...v,channel_id:c.channel_id,channel_title:c.channel_title,current_subscribers:c.current_subscribers,subscriber_observed_at:report.collected_at,format_classification:"unverified"})));
 videos.sort((a,b)=>x.sort==="views"?(b.views??-1)-(a.views??-1)||String(a.video_id).localeCompare(String(b.video_id)):String(b.published_at??"").localeCompare(String(a.published_at??""))||String(a.video_id).localeCompare(String(b.video_id)));
 return {collected_at:report.collected_at,expires_at:new Date(expiry).toISOString(),channels:channels.map(({videos,...meta})=>meta),videos:videos.slice(x.offset,x.offset+x.limit),total_sample:videos.length,next_offset:x.offset+x.limit<videos.length?x.offset+x.limit:null,limitations:"Stored bounded upload sample only; current subscribers at collection, not at publication. Duration is not Shorts classification. No live YouTube request or derived performance measure."};
}
export async function inspectChannels(input,fetcher=fetch){
 const p=channelInspectionSchema.safeParse(input);
 if(!p.success)throw new ResearchError(400,"Kanal filtresi geçersiz.");
 return inspectSamples(await getReport(p.data.id,fetcher),p.data);
}
