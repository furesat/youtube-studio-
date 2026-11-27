import { env, json, errorResponse, ResearchError, trustedOrigin } from "../lib/research.mjs";
import { login, logoutCookies, sessionStatus, unlockAdmin, adminFor, sameOriginMutation, auditLog } from "../lib/panel-auth.mjs";

function reply(body:unknown,cookies:string[]=[],status=200){
  const response=json(body,status);
  for(const cookie of cookies)response.headers.append("Set-Cookie",cookie);
  return response;
}
async function readBody(request:Request){
  const raw=await request.text();
  if(raw.length>8192)throw new ResearchError(413,"İstek çok büyük.");
  try{const body=JSON.parse(raw);if(!body||typeof body!=="object"||Array.isArray(body))throw new Error();return body;}
  catch{throw new ResearchError(400,"Geçersiz giriş isteği.");}
}
export default async (request:Request)=>{
  if(!trustedOrigin(request))return json({error:"İstek kaynağına izin verilmedi."},403);
  const path=new URL(request.url).pathname;
  try{
    if(!env("FASULYE_ACCESS_TOKEN"))throw new ResearchError(503,"Panel parolası yapılandırılmamış.");
    if(request.method==="GET"&&path==="/api/session")return json(sessionStatus(request));
    if(request.method==="GET"&&path==="/api/admin/logins"){
      if(!adminFor(request))throw new ResearchError(403,"Yönetici oturumu gerekli.");
      return json(await auditLog());
    }
    if(request.method!=="POST")throw new ResearchError(405,"Bu yöntem desteklenmiyor.");
    if(!sameOriginMutation(request))throw new ResearchError(403,"İstek kaynağına izin verilmedi.");
    if(path==="/api/login"){
      const result=await login(request,await readBody(request));
      return reply(result.body,result.cookies);
    }
    if(path==="/api/logout")return reply({authenticated:false},logoutCookies());
    if(path==="/api/admin/unlock"){
      const {password}=await readBody(request);
      return reply({admin:true},[unlockAdmin(request,password)]);
    }
    throw new ResearchError(404,"İşlem bulunamadı.");
  }catch(error){return errorResponse(error);}
};
export const config={
  path:["/api/session","/api/login","/api/logout","/api/admin/unlock","/api/admin/logins"],
  rateLimit:{action:"rate_limit",aggregateBy:["ip","domain"],windowSize:60,windowLimit:10}
};
