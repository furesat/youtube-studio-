import { createHmac, randomUUID, timingSafeEqual } from "node:crypto";
import { env, acceptsToken, ResearchError } from "./research.mjs";
import { db } from "./batch.mjs";

const SESSION="__Host-fasulye_session", DEVICE="__Host-fasulye_device", ADMIN="__Host-fasulye_admin";
const DAY=86400;
const uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
function equal(a,b){const x=Buffer.from(a??""),y=Buffer.from(b??"");return x.length===y.length&&timingSafeEqual(x,y);}
function secret(kind){
  const access=env("FASULYE_ACCESS_TOKEN"), github=env("FASULYE_GITHUB_TOKEN");
  const admin=env("FASULYE_ADMIN_TOKEN");
  if(!access||!github||(kind==="admin"&&(!admin||admin===access||admin===github)))return null;
  return createHmac("sha256",github).update(JSON.stringify(["fasulye-session-v1",kind,access,kind==="admin"?admin:""])).digest();
}
function sign(payload,kind){
  const key=secret(kind);if(!key)throw new ResearchError(503,"Oturum yapılandırması eksik.");
  const data=Buffer.from(JSON.stringify(payload)).toString("base64url");
  return data+"."+createHmac("sha256",key).update(data).digest("base64url");
}
function readCookie(request,name){
  return (request.headers.get("cookie")??"").split(";").map(s=>s.trim()).find(s=>s.startsWith(name+"="))?.slice(name.length+1)??"";
}
function verify(token,kind,now=Date.now()){
  const key=secret(kind);
  if(!key||!token||token.length>2048)return null;
  const [data,signature,...extra]=token.split(".");
  if(!data||!signature||extra.length||!equal(signature,createHmac("sha256",key).update(data).digest("base64url")))return null;
  try{
    const p=JSON.parse(Buffer.from(data,"base64url").toString("utf8"));
    return p.kind===kind&&uuid.test(p.sid)&&uuid.test(p.device)&&Number.isSafeInteger(p.exp)&&p.exp>Math.floor(now/1000)?p:null;
  }catch{return null;}
}
function cookie(name,value,maxAge){
  return name+"="+value+"; Path=/; Secure; HttpOnly; SameSite=Strict"+(maxAge==null?"":"; Max-Age="+maxAge);
}
export function sessionFor(request,now=Date.now()){return verify(readCookie(request,SESSION),"session",now);}
export function adminFor(request,now=Date.now()){
  const session=sessionFor(request,now),admin=verify(readCookie(request,ADMIN),"admin",now);
  return Boolean(session&&admin&&admin.sid===session.sid&&admin.device===session.device);
}
export function sameOriginMutation(request){
  return request.headers.get("origin")===new URL(request.url).origin;
}
function deviceInfo(ua){
  const browser=/Edg\//.test(ua)?"Edge":/Firefox\//.test(ua)?"Firefox":/CriOS\//.test(ua)?"Chrome iOS":/Chrome\//.test(ua)?"Chrome":/Safari\//.test(ua)?"Safari":"Diğer";
  const platform=/iPhone|iPad/.test(ua)?"iOS/iPadOS":/Android/.test(ua)?"Android":/Windows/.test(ua)?"Windows":/Macintosh/.test(ua)?"macOS":/Linux/.test(ua)?"Linux":"Bilinmiyor";
  return {browser,platform};
}
export function auditConfigured(){return (env("SUPABASE_SECRET_KEY")??"").startsWith("sb_secret_");}
export function sessionStatus(request){
  return {authenticated:!!sessionFor(request),admin:adminFor(request),admin_configured:!!secret("admin"),audit_configured:auditConfigured()};
}
export async function login(request,{password,remember=true,label=""},fetcher=fetch){
  if(typeof password!=="string"||password.length>4096||!acceptsToken(password))throw new ResearchError(401,"Parola yanlış.");
  if(typeof remember!=="boolean"||typeof label!=="string"||label.length>80||/[\u0000-\u001f\u007f]/.test(label))throw new ResearchError(400,"Cihaz bilgisi geçersiz.");
  const age=remember?90*DAY:12*3600;
  let device=readCookie(request,DEVICE);
  if(!uuid.test(device))device=randomUUID();
  const sid=randomUUID(), exp=Math.floor(Date.now()/1000)+age;
  const value=sign({kind:"session",sid,device,exp},"session");
  let audit="unavailable";
  if(auditConfigured()){
    try{
      await db("fasulye_login_events",{method:"POST",body:{device_id:device,device_label:label.trim(),...deviceInfo(request.headers.get("user-agent")??""),remembered:remember},prefer:"return=minimal",fetcher});
      audit="recorded";
    }catch{audit="unavailable";}
  }
  return {body:{authenticated:true,audit,admin_configured:!!secret("admin"),audit_configured:auditConfigured()},cookies:[cookie(SESSION,value,remember?age:null),cookie(DEVICE,device,remember?365*DAY:null),cookie(ADMIN,"",0)]};
}
export function unlockAdmin(request,password){
  const session=sessionFor(request),expected=env("FASULYE_ADMIN_TOKEN");
  if(!session)throw new ResearchError(401,"Önce giriş yap.");
  if(!secret("admin"))throw new ResearchError(503,"Ayrı yönetici parolası yapılandırılmamış.");
  if(typeof password!=="string"||password.length>4096||!equal(password,expected))throw new ResearchError(401,"Yönetici parolası yanlış.");
  const age=Math.min(DAY,session.exp-Math.floor(Date.now()/1000));
  return cookie(ADMIN,sign({kind:"admin",sid:session.sid,device:session.device,exp:Math.floor(Date.now()/1000)+age},"admin"),age);
}
export function logoutCookies(){return [cookie(SESSION,"",0),cookie(ADMIN,"",0)];}
export async function auditLog(fetcher=fetch){
  const [summary,events]=await Promise.all([
    db("rpc/fasulye_login_summary",{method:"POST",body:{},fetcher}),
    db("fasulye_login_events?"+new URLSearchParams({select:"signed_in_at,device_id,device_label,browser,platform,remembered",signed_in_at:"gte."+new Date(Date.now()-90*DAY*1000).toISOString(),order:"signed_in_at.desc",limit:"100"}),{fetcher})
  ]);
  return {summary,events};
}
