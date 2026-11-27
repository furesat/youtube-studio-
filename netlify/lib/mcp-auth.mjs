import { createRemoteJWKSet, jwtVerify } from "jose";
import { acceptsToken, env, json, readBearer } from "./research.mjs";

const keySets = new Map();

export function oauthConfig() {
  const issuer = env("FASULYE_OAUTH_ISSUER");
  const resource = env("FASULYE_OAUTH_RESOURCE");
  const subject = env("FASULYE_OAUTH_SUBJECT");
  if (!issuer || !resource || !subject) return null;
  try {
    const authority = new URL(issuer);
    const endpoint = new URL(resource);
    if (authority.protocol !== "https:" || endpoint.protocol !== "https:" ||
        endpoint.pathname !== "/mcp" || endpoint.href !== resource ||
        authority.href !== issuer || authority.pathname !== "/" ||
        [authority, endpoint].some(url => url.username || url.password || url.search || url.hash)) {
      return null;
    }
    return { issuer, resource, subject };
  } catch {
    return null;
  }
}

export function resourceMetadata(settings) {
  if (!settings) return json({ error: "OAuth yapılandırılmamış." }, 404);
  return json({
    resource: settings.resource,
    resource_name: "Fasulye Opportunity Engine",
    authorization_servers: [settings.issuer],
    bearer_methods_supported: ["header"],
  });
}

export function mcpUnauthorized(settings) {
  const challenge = settings
    ? `Bearer resource_metadata="${new URL("/.well-known/oauth-protected-resource/mcp", settings.resource)}"`
    : "Bearer";
  return json({ error: "Geçerli bir araştırma erişim anahtarı gerekli." }, 401, {
    "WWW-Authenticate": challenge,
  });
}

export async function verifyAccessToken(token, settings, getKey) {
  const { payload } = await jwtVerify(token, getKey, {
    issuer: settings.issuer,
    audience: settings.resource,
    algorithms: ["RS256"],
    requiredClaims: ["exp", "sub"],
  });
  return payload.sub === settings.subject;
}

export async function mcpAuthorized(request, settings) {
  const token = readBearer(request);
  if (acceptsToken(token)) return true;
  if (!token || !settings) return false;
  try {
    if (!keySets.has(settings.issuer)) {
      keySets.set(settings.issuer, createRemoteJWKSet(new URL(".well-known/jwks.json", settings.issuer)));
    }
    return await verifyAccessToken(token, settings, keySets.get(settings.issuer));
  } catch {
    return false;
  }
}
