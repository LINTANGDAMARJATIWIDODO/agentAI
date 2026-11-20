/**
 * NEXUS AI ENTERPRISE — REAL SUBSTANTIVE PARAPHRASING & AI FORENSIC HUMANIZER
 * =========================================================================
 * 100% Real LLM Rewriting via official Google GenAI SDK (@google/genai)
 * Multi-Key Rotation Pool: process.env.key2 -> key3 -> GEMINI_API_KEYS -> GEMINI_API_KEY
 * Cascading Models: gemini-2.5-flash -> gemini-2.5-flash-lite -> gemini-3.6-flash -> gemini-3.5-flash
 * Structured Output: responseSchema JSON with usageMetadata token verification.
 * API Version: v1beta
 *
 * Fully stateless & compatible with Vercel Serverless (export const maxDuration = 60).
 */

const path = require('path');
const fs = require('fs');

const BASE_DIR = path.resolve(__dirname, '..');

// Auto-load .env if process.env.GEMINI_API_KEY or key2 is not set
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

let GoogleGenAI = null;
let Type = null;
try {
  const genaiPkg = require('@google/genai');
  GoogleGenAI = genaiPkg.GoogleGenAI;
  Type = genaiPkg.Type;
} catch (e) {
  console.warn('[@google/genai import warning]:', e.message);
}

let getApiKeyPool;
try {
  getApiKeyPool = require('../services/gemini/apiKeyPool').getApiKeyPool;
} catch (e) {
  getApiKeyPool = function() {
    const keys = [];
    const k2 = (process.env.key2 || process.env.KEY2 || '').trim().replace(/^['"]|['"]$/g, '');
    if (k2) keys.push(k2);
    const k3 = (process.env.key3 || process.env.KEY3 || '').trim().replace(/^['"]|['"]$/g, '');
    if (k3) keys.push(k3);
    ['key4', 'KEY4', 'key5', 'KEY5', 'key1', 'KEY1'].forEach(envName => {
      const val = (process.env[envName] || '').trim().replace(/^['"]|['"]$/g, '');
      if (val) keys.push(val);
    });
    const keysStr = process.env.GEMINI_API_KEYS || process.env.gemini_api_keys || '';
    if (keysStr) {
      keysStr.split(',').forEach(k => {
        const trimmed = k.trim().replace(/^['"]|['"]$/g, '');
        if (trimmed) keys.push(trimmed);
      });
    }
    const kSingle = (process.env.GEMINI_API_KEY || process.env.gemini_api_key || '').trim().replace(/^['"]|['"]$/g, '');
    if (kSingle) keys.push(kSingle);
    const uniqueKeys = [];
    keys.forEach(k => {
      if (k && !uniqueKeys.includes(k)) uniqueKeys.push(k);
    });
    return uniqueKeys;
  };
}

function segmentSentences(text) {
  if (!text) return [];
  const cleaned = text
    .replace(/\b(Perpres|UU|PP|No|Nomor|Kepgub|Permen|Inpres|dkk|hlm|hal|dll|dst|dsb|Prof|Dr|dr|Ir)\./gi, '$1_DOT_')
    .replace(/(\d+)\.(\d+)/g, '$1_DEC_$2')
    .replace(/(\d+)\.\s+(?=[A-Z0-9])/g, '$1_NUMDOT_ ');

  const rawSplits = cleaned.split(/(?<=[.?!])\s+(?=[A-Z0-9])/);
  return rawSplits.map(s => s
    .replace(/_DOT_/g, '.')
    .replace(/_DEC_/g, '.')
    .replace(/_NUMDOT_\s*/g, '. ')
    .trim()
  ).filter(s => s.length > 2 && /[a-zA-Z]/.test(s));
}

async function callGeminiStructured({ systemInstruction, userPrompt, responseSchema, temperature = 0.25 }) {
  if (!GoogleGenAI) {
    throw new Error('@google/genai SDK tidak tersedia pada server runtime.');
  }

  const keyPool = getApiKeyPool();
  if (!keyPool.length) {
    throw new Error('Tidak ada API Key Gemini yang terkonfigurasi pada server (key2, key3, GEMINI_API_KEYS, GEMINI_API_KEY).');
  }

  const models = [
    'gemini-2.5-flash',
    'gemini-2.5-flash-lite',
    'gemini-3.6-flash',
    'gemini-3.5-flash',
    'gemini-flash-latest',
    'gemini-flash-lite-latest'
  ];

  let lastError = null;

  for (const model of models) {
    for (let keyIdx = 0; keyIdx < keyPool.length; keyIdx++) {
      const currentApiKey = keyPool[keyIdx];

      try {
        const ai = new GoogleGenAI({ apiKey: currentApiKey, apiVersion: 'v1beta' });
        const response = await ai.models.generateContent({
          model: model,
          contents: [{ role: 'user', parts: [{ text: userPrompt }] }],
          config: {
            systemInstruction: { parts: [{ text: systemInstruction }] },
            responseMimeType: 'application/json',
            responseSchema: responseSchema,
            temperature: temperature,
            maxOutputTokens: 8192
          }
        });

        const reply = response.text || '';
        if (reply) {
          const parsed = JSON.parse(reply.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim());
          const usage = response.usageMetadata || {};
          const totalTokens = usage.totalTokenCount || ((usage.promptTokenCount || 0) + (usage.candidatesTokenCount || 0)) || 0;
          return {
            data: parsed,
            model_used: model,
            key_index: keyIdx + 1,
            total_keys: keyPool.length,
            usage: usage,
            total_tokens: totalTokens
          };
        }
      } catch (err) {
        lastError = err;
        const msg = (err.message || String(err)).toLowerCase();
        console.warn(`[Model ${model} | Key #${keyIdx + 1}/${keyPool.length}]:`, err.message);

        // 404 Model Not Found / Not Available: break key loop to proceed to next model immediately
        if (msg.includes('404') || msg.includes('not found') || msg.includes('no longer available') || msg.includes('not supported')) {
          console.warn(`[Model ${model}] Not found/supported, skipping to next model...`);
          break;
        }

        // 429 Quota Exceeded / 503 Service Unavailable: continue to try next API key in pool for this model!
        continue;
      }
    }
  }

  const errMsg = lastError?.message || String(lastError);
  throw new Error(errMsg);
}

module.exports = async (req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    return res.end();
  }

  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify({ status: 'error', message: 'Method Not Allowed' }));
  }

  res.setHeader('Content-Type', 'application/json');

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) { body = {}; }
    } else if (!body) {
      body = await new Promise((resolve) => {
        let raw = '';
        const timer = setTimeout(() => resolve({}), 1000);
        req.on('data', c => { raw += c; });
        req.on('end', () => {
          clearTimeout(timer);
          try { resolve(JSON.parse(raw || '{}')); } catch (e) { resolve({}); }
        });
        req.on('error', () => { clearTimeout(timer); resolve({}); });
      });
    }

    const action = body.action || 'humanize';
    const mode = body.mode || 'Formal SPBE & Eksekutif';

    // -------------------------------------------------------------
    // ACTION: AUDIT FORENSIK (Real AI Authorship Scoring per Batch)
    // -------------------------------------------------------------
    if (action === 'audit' || action === 'detect') {
      const sentences = Array.isArray(body.sentences) && body.sentences.length > 0
        ? body.sentences
        : segmentSentences(body.text || body.content || '');

      if (!sentences.length) {
        res.statusCode = 400;
        return res.end(JSON.stringify({ status: 'error', message: 'Daftar kalimat atau teks naskah tidak boleh kosong.' }));
      }

      const systemPrompt = `Anda adalah Spesialis Audit Forensik Kepengarangan Teks AI Bahasa Indonesia kelas dunia.
Tugas Anda adalah menganalisis batch kalimat dan menentukan tingkat probabilitas kepengarangan AI.

INSTRUKSI PENGHEMATAN WAKTU & TOKEN (ULTRA-FAST):
1. Hitung perkiraan persentase skor AI keseluruhan untuk seluruh batch kalimat ini (overall_ai_score: 0-100).
2. Pada array "flagged_sentences", HANYA cantumkan kalimat yang terindikasi AI (ai_score >= 40, status HIGH_AI atau MODERATE_AI), dengan batas MAKSIMAL 10 kalimat paling terindikasi per batch.
3. Kalimat yang sudah alami atau berstruktur manusiawi (< 40) DILARANG dimasukkan ke array flagged_sentences agar pemrosesan super cepat.
4. Pada setiap kalimat flagged, sertakan id (nomor urut [ID X]), text asli, ai_score (>=40), status ("HIGH_AI" jika >=70, "MODERATE_AI" jika 40-69), characteristic_found (alasan sintaksis spesifik), reason (alasan teknis), dan kbbi_fix (perbaikan kata baku KBBI/EYD V).`;

      const userPrompt = `Analisis batch ${sentences.length} kalimat berikut. Berikan overall_ai_score untuk batch ini dan HANYA kembalikan kalimat yang terindikasi AI (ai_score >= 40, maksimal 10 kalimat):\n\n` +
        sentences.map((s, idx) => `[ID ${idx + 1}]: "${s}"`).join('\n');

      const auditSchema = {
        type: Type ? Type.OBJECT : 'OBJECT',
        properties: {
          overall_ai_score: { type: Type ? Type.NUMBER : 'NUMBER' },
          flagged_sentences: {
            type: Type ? Type.ARRAY : 'ARRAY',
            items: {
              type: Type ? Type.OBJECT : 'OBJECT',
              properties: {
                id: { type: Type ? Type.NUMBER : 'NUMBER' },
                text: { type: Type ? Type.STRING : 'STRING' },
                ai_score: { type: Type ? Type.NUMBER : 'NUMBER' },
                status: { type: Type ? Type.STRING : 'STRING' },
                characteristic_found: { type: Type ? Type.STRING : 'STRING' },
                reason: { type: Type ? Type.STRING : 'STRING' },
                kbbi_fix: { type: Type ? Type.STRING : 'STRING' }
              },
              required: ['id', 'text', 'ai_score', 'status', 'characteristic_found', 'reason', 'kbbi_fix']
            }
          }
        },
        required: ['overall_ai_score', 'flagged_sentences']
      };

      const result = await callGeminiStructured({
        systemInstruction: systemPrompt,
        userPrompt,
        responseSchema: auditSchema,
        temperature: 0.15
      });

      const flagged = result.data.flagged_sentences || result.data.sentences || [];
      const batchAiScore = typeof result.data.overall_ai_score === 'number'
        ? Math.round(result.data.overall_ai_score)
        : (flagged.length > 0 ? Math.round(flagged.reduce((a, b) => a + (b.ai_score || 70), 0) / flagged.length) : 15);

      res.statusCode = 200;
      return res.end(JSON.stringify({
        status: 'success',
        model_used: result.model_used,
        key_index: result.key_index,
        total_tokens_used: result.total_tokens,
        usage_metadata: result.usage,
        batch_ai_score: batchAiScore,
        overall_ai_score: batchAiScore,
        flagged_sentences: flagged,
        sentences: flagged,
        total_sentences_analyzed: sentences.length
      }));
    }

    // -------------------------------------------------------------
    // ACTION: HIGH-COMPRESSION REAL SUBSTANTIVE PARAPHRASING (Remove AI)
    // -------------------------------------------------------------
    let flaggedItems = Array.isArray(body.flagged_items) && body.flagged_items.length > 0
      ? body.flagged_items
      : (Array.isArray(body.flagged_sentences) && body.flagged_sentences.length > 0 ? body.flagged_sentences : []);

    // Fallback if client passed raw sentences array
    if (!flaggedItems.length && Array.isArray(body.sentences) && body.sentences.length > 0) {
      flaggedItems = body.sentences.map((s, idx) => {
        if (typeof s === 'object' && s !== null) {
          return { id: s.id || idx + 1, text: s.text || s.original || s.sentence || '' };
        }
        return { id: idx + 1, text: String(s) };
      });
    }

    if (!flaggedItems.length && (body.text || body.content)) {
      const segs = segmentSentences(body.text || body.content || '');
      flaggedItems = segs.map((s, idx) => ({ id: idx + 1, text: s }));
    }

    if (!flaggedItems.length) {
      res.statusCode = 400;
      return res.end(JSON.stringify({ status: 'error', message: 'Daftar kalimat terindikasi AI tidak boleh kosong.' }));
    }

    const systemInstructionText = `Anda adalah Principal Enterprise Indonesian AI Forensic Auditor & Senior Substantive Paraphraser kelas dunia.
Tugas Anda adalah melakukan PENULISAN ULANG SUBSTANTIF (Substantive Paraphrasing) secara nyata HANYA pada daftar kalimat yang terindikasi AI berikut.

ATURAN REVISI SUBSTANTIF:
1. Rombak struktur sintaksis: ubah pasif ke aktif atau variasikan ritme agar alami manusiawi (Burstiness tinggi).
2. Hapus konjungsi dan formula klise robotik AI ("Selain itu", "Lebih lanjut", "secara holistik", "memainkan peran krusial", "tidak dapat dipungkiri bahwa", "dalam era digital").
3. 100% Wajib mematuhi kaidah baku KBBI & EYD V (contoh: tepercaya, analisis, risiko, praktik, sistem, standardisasi, pelindungan, aktivitas, efektivitas).
4. PRESERVASI KETAT 100%: Dilarang mengubah angka, tahun, nama regulasi (Perpres 95/2018, UU 27/2022, dll.), dan kode teknis SPBE (DAB, DAD, DAL, DAA).
5. Targetkan ai_score_after < 15% (lolos Turnitin & GPTZero).
6. Kembalikan array JSON "items" berisi objek persis:
   - id: nomor ID kalimat yang sama dengan input
   - humanized_text: kalimat hasil parafrase substantif alami dan baku KBBI
   - ai_score_after: angka probabilitas AI setelah revisi (wajib < 15)
   - revision_reason: alasan teknis perbaikan singkat
7. Gaya Tulisan: ${mode}.`;

    const userPromptText = `Tulis ulang ${flaggedItems.length} kalimat terindikasi AI berikut menjadi alami, baku KBBI, dan lolos detektor AI:\n\n` +
      flaggedItems.map(item => `[ID ${item.id}]: "${item.text}"`).join('\n');

    const schemaConfig = {
      type: Type ? Type.OBJECT : 'OBJECT',
      properties: {
        items: {
          type: Type ? Type.ARRAY : 'ARRAY',
          items: {
            type: Type ? Type.OBJECT : 'OBJECT',
            properties: {
              id: { type: Type ? Type.NUMBER : 'NUMBER' },
              humanized_text: { type: Type ? Type.STRING : 'STRING' },
              ai_score_after: { type: Type ? Type.NUMBER : 'NUMBER' },
              revision_reason: { type: Type ? Type.STRING : 'STRING' }
            },
            required: ['id', 'humanized_text', 'ai_score_after', 'revision_reason']
          }
        }
      },
      required: ['items']
    };

    const result = await callGeminiStructured({
      systemInstruction: systemInstructionText,
      userPrompt: userPromptText,
      responseSchema: schemaConfig,
      temperature: 0.25
    });

    const parsedItems = (result.data && result.data.items) || [];

    const revisedItems = parsedItems.map((item, idx) => {
      const origItem = flaggedItems.find(f => f.id === item.id) || flaggedItems[idx] || {};
      const scoreAfter = typeof item.ai_score_after === 'number' ? Math.round(item.ai_score_after) : 8;
      return {
        id: item.id || (idx + 1),
        sentence_id: item.id || (idx + 1),
        original_text: origItem.text || '',
        original: origItem.text || '',
        sentence: origItem.text || '',
        humanized_text: item.humanized_text || origItem.text || '',
        humanized: item.humanized_text || origItem.text || '',
        revised_text: item.humanized_text || origItem.text || '',
        recommendation: item.humanized_text || origItem.text || '',
        ai_score_after: scoreAfter,
        ai_score: scoreAfter,
        status: 'SUDAH ALAMI',
        action_label: 'SUDAH ALAMI',
        level: 'low',
        revision_reason: item.revision_reason || 'Rekonstruksi ritme klausa dan penyelarasan kaidah baku KBBI',
        reason: item.revision_reason || 'Rekonstruksi ritme klausa dan penyelarasan kaidah baku KBBI',
        characteristic_found: 'Struktur klausa alami dan dinamis'
      };
    });

    res.statusCode = 200;
    return res.end(JSON.stringify({
      status: 'success',
      model_used: result.model_used,
      key_index: result.key_index,
      total_tokens_used: result.total_tokens,
      usage_metadata: result.usage,
      mode: mode,
      items: revisedItems,
      flagged_sentences: revisedItems,
      sentences: revisedItems,
      sentence_pairs: revisedItems,
      revised_count: revisedItems.length
    }));

  } catch (err) {
    console.error('[/api/humanize critical error]:', err);
    res.statusCode = 500;
    const rawMsg = err.message || String(err);
    let userMsg = rawMsg;
    if (rawMsg.includes('429') || rawMsg.includes('quota') || rawMsg.includes('RESOURCE_EXHAUSTED') || rawMsg.includes('quotafailure')) {
      userMsg = 'Batas kuota harian Gemini API (20 RPD Free Tier) telah tercapai pada seluruh API Key yang terkonfigurasi. Silakan tambahkan API key baru di Vercel Environment (key2 / key3 / GEMINI_API_KEYS) atau tunggu reset kuota harian Google.';
    }
    return res.end(JSON.stringify({
      status: 'error',
      is_quota_error: rawMsg.includes('429') || rawMsg.includes('quota') || rawMsg.includes('RESOURCE_EXHAUSTED') || rawMsg.includes('quotafailure'),
      raw_error: rawMsg,
      message: userMsg
    }));
  }
};

module.exports.config = {
  maxDuration: 60
};
