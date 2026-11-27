import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createHmac } from 'node:crypto';
import { deriveSessionKey } from '../lib/session-key.mjs';
const base = {access:'panel', github:'legacy', admin:'owner'};
const signing = 'test-dedicated-secret-32-bytes-minimum';
test('legacy configuration preserves existing cookies', () => {
  assert.deepEqual(deriveSessionKey('session', base), createHmac('sha256', 'legacy').update(JSON.stringify(['fasulye-session-v1','session','panel',''])).digest());
});
test('dedicated key invalidates legacy signatures and ignores GitHub rotation', () => {
  const config = {...base, signing};
  const key = deriveSessionKey('session', config);
  assert.ok(key);
  assert.notDeepEqual(key, deriveSessionKey('session', base));
  assert.deepEqual(key, deriveSessionKey('session', {...config, github:'rotated'}));
  assert.deepEqual(key, deriveSessionKey('session', {...config, github:undefined}));
  assert.notDeepEqual(key, deriveSessionKey('session', {...config, access:'rotated'}));
  assert.notDeepEqual(key, deriveSessionKey('session', {...config, signing:signing+'rotated'}));
});
test('invalid dedicated configuration fails closed; admin remains separate', () => {
  for (const bad of ['short', ' '.repeat(32), signing]) {
    assert.equal(deriveSessionKey('session', {...base, signing:bad, ...(bad===signing?{github:signing}:{})}), null);
  }
  assert.equal(deriveSessionKey('admin', {...base, signing, admin:'panel'}), null);
  assert.notDeepEqual(deriveSessionKey('session', {...base, signing}), deriveSessionKey('admin', {...base, signing}));
});
