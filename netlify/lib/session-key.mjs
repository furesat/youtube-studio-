import { createHmac } from "node:crypto";

// A configured but invalid dedicated secret must never fall back to the GitHub token.
export function deriveSessionKey(kind, {access, github, admin, signing}) {
  if (!['session', 'admin'].includes(kind) || !access) return null;
  if (kind === 'admin' && (!admin || admin === access || admin === github)) return null;
  const dedicated = signing !== undefined && signing !== null && signing !== '';
  if (dedicated && (typeof signing !== 'string' || Buffer.byteLength(signing) < 32 || signing === access || signing === github || signing === admin || !signing.trim())) return null;
  const root = dedicated ? signing : github;
  if (!root) return null;
  return createHmac('sha256', root).update(JSON.stringify([dedicated ? 'fasulye-session-v2' : 'fasulye-session-v1', kind, access, kind === 'admin' ? admin : ''])).digest();
}
