/**
 * NEXUS AI ENTERPRISE — DEDUPLICATED GEMINI API KEY ROTATION POOL
 * ===============================================================
 * Priority Order:
 * 1. process.env.key2 / KEY2 / key_2 / KEY_2
 * 2. process.env.key3 / KEY3 / key_3 / KEY_3
 * 3. Additional numbered keys: key4, key5, key1, etc.
 * 4. process.env.GEMINI_API_KEYS (comma-separated list)
 * 5. process.env.GEMINI_API_KEY
 * 6. Dynamic Auto-Discovery of any env var containing Gemini keys (starting with AIza or AQ.)
 *
 * Compatible with standard keys and AQ. prefixed keys using official @google/genai SDK.
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = path.resolve(__dirname, '..', '..');

// Auto-load .env if needed
if (!process.env.GEMINI_API_KEY || !process.env.key2) {
  const envFile = path.join(BASE_DIR, '.env');
  if (fs.existsSync(envFile)) {
    try {
      const rawEnv = fs.readFileSync(envFile, 'utf-8');
      rawEnv.split(/\r?\n/).forEach(line => {
        line = line.trim();
        if (line && !line.startsWith('#') && line.includes('=')) {
          const eqIdx = line.indexOf('=');
          const k = line.slice(0, eqIdx).trim();
          const v = line.slice(eqIdx + 1).trim().replace(/^['"]|['"]$/g, '');
          if (!process.env[k]) process.env[k] = v;
        }
      });
    } catch (e) {}
  }
}

function getApiKeyPool() {
  const keys = [];

  // Priority 1: process.env.key2 / KEY2 / key_2
  const k2 = (process.env.key2 || process.env.KEY2 || process.env.key_2 || process.env.KEY_2 || process.env.gemini_key_2 || process.env.GEMINI_KEY_2 || '').trim().replace(/^['"]|['"]$/g, '');
  if (k2) keys.push(k2);

  // Priority 2: process.env.key3 / KEY3 / key_3
  const k3 = (process.env.key3 || process.env.KEY3 || process.env.key_3 || process.env.KEY_3 || process.env.gemini_key_3 || process.env.GEMINI_KEY_3 || '').trim().replace(/^['"]|['"]$/g, '');
  if (k3) keys.push(k3);

  // Additional numbered keys if present
  ['key4', 'KEY4', 'key_4', 'KEY_4', 'key5', 'KEY5', 'key_5', 'KEY_5', 'key1', 'KEY1', 'key_1', 'KEY_1'].forEach(envName => {
    const val = (process.env[envName] || '').trim().replace(/^['"]|['"]$/g, '');
    if (val) keys.push(val);
  });

  // Priority 3: process.env.GEMINI_API_KEYS (split by comma and trim)
  const keysStr = process.env.GEMINI_API_KEYS || process.env.gemini_api_keys || '';
  if (keysStr) {
    keysStr.split(',').forEach(k => {
      const trimmed = k.trim().replace(/^['"]|['"]$/g, '');
      if (trimmed) keys.push(trimmed);
    });
  }

  // Priority 4: process.env.GEMINI_API_KEY
  const kSingle = (process.env.GEMINI_API_KEY || process.env.gemini_api_key || '').trim().replace(/^['"]|['"]$/g, '');
  if (kSingle) keys.push(kSingle);

  // Priority 5: Dynamic Auto-Discovery of any other env var containing valid Gemini keys
  Object.keys(process.env).forEach(envKey => {
    const val = (process.env[envKey] || '').trim().replace(/^['"]|['"]$/g, '');
    if (val && (val.startsWith('AIza') || val.startsWith('AQ.')) && val.length > 25) {
      if (!keys.includes(val)) {
        keys.push(val);
      }
    }
  });

  // Deduplicate and filter non-empty
  const uniqueKeys = [];
  keys.forEach(k => {
    if (k && !uniqueKeys.includes(k)) {
      uniqueKeys.push(k);
    }
  });

  return uniqueKeys;
}

module.exports = {
  getApiKeyPool
};
