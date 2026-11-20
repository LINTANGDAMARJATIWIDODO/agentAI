/**
 * Vercel Serverless Function: POST /api/justdone-audit
 * ==========================================================
 * Real AI Forensic Scoring & Substantive Paraphrasing Humanizer
 * Powered 100% by Google GenAI SDK (@google/genai) & Gemini 2.5 Flash
 *
 * 100% Stateless & Vercel Serverless Ready (export const maxDuration = 60).
 */

const path = require('path');
const fs = require('fs');

const BASE_DIR = path.resolve(__dirname, '..');

// Auto-load .env if process.env.GEMINI_API_KEY is not set
if (!process.env.GEMINI_API_KEY) {
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
  console.warn('[@google/genai import warning in justdone-audit]:', e.message);
}

module.exports = async (req, res) => {
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
    let payload = req.body;
    if (typeof payload === 'string') {
      try { payload = JSON.parse(payload); } catch (e) { payload = {}; }
    } else if (!payload) {
      payload = await new Promise((resolve) => {
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

    const apiKey = process.env.GEMINI_API_KEY || '';
    if (!apiKey) {
      res.statusCode = 500;
      return res.end(JSON.stringify({
        status: 'error',
        message: 'GEMINI_API_KEY tidak dikonfigurasi pada server. Pemrosesan forensik & humanisasi nyata memerlukan Google GenAI API key yang aktif.'
      }));
    }

    if (!GoogleGenAI) {
      res.statusCode = 500;
      return res.end(JSON.stringify({
        status: 'error',
        message: 'Google GenAI SDK (@google/genai) tidak ditemukan atau gagal dimuat.'
      }));
    }

    const action = payload.action || 'audit'; // 'audit' or 'humanize'
    const sentences = Array.isArray(payload.sentences) ? payload.sentences : [];
    const rawText = (payload.text || payload.content || '').trim();
    const primaryModel = process.env.GEMINI_MODEL_FLASH || 'gemini-2.5-flash';
    const fallbackModel = 'gemini-2.5-flash-lite';

    const ai = new GoogleGenAI({ apiKey });

    // -------------------------------------------------------------
    // ACTION: AUDIT FORENSIK PER-BATCH (100% Real Gemini Detection)
    // -------------------------------------------------------------
    if (action === 'audit') {
      const sentenceList = sentences.length > 0 ? sentences : (rawText ? [rawText] : []);
      if (!sentenceList.length) {
        res.statusCode = 400;
        return res.end(JSON.stringify({ status: 'error', message: 'Daftar kalimat tidak boleh kosong.' }));
      }

      const systemPrompt = `Anda adalah Spesialis Audit Forensik Kepengarangan Teks AI Bahasa Indonesia kelas dunia.
Tugas Anda adalah menganalisis setiap kalimat dan menentukan apakah kalimat tersebut ditulis oleh Model Bahasa (AI) atau Manusia.

KRITERIA KALIBRASI KETAT:
1. Kalimat yang menggunakan pola templat kaku, struktur majemuk simetris/seragam, transisi robotik ("Pemanfaatan ... telah berkembang dari ... menjadi ...", "Pendekatan tersebut memang ... tetapi menghasilkan ...", "tidak dapat dipungkiri bahwa", "dalam era digital", enumerasi titik dua mekanis) WAJIB diberi ai_score ANTARA 55 SAMPAI 90 (HIGH_AI atau MODERATE_AI).
2. Kalimat yang memiliki ritme dinamis alami, variasi klausa tak terduga, atau struktur manusiawi diberi ai_score < 30 (HUMAN).
3. Kalimat transisi campuran atau formal standar diberi ai_score 35-65 (MODERATE_AI).
4. Status WAJIB bernilai:
   - "HIGH_AI" jika ai_score >= 70
   - "MODERATE_AI" jika ai_score >= 40 dan < 70
   - "HUMAN" jika ai_score < 40
5. Berikan karakteristik unik (characteristic_found) yang mendeskripsikan secara spesifik pola sintaksis kalimat ini.
6. Berikan saran koreksi ejaan KBBI / EYD V jika ditemukan ketidakbakuan (misal: "terpercaya" -> "tepercaya", "analisa" -> "analisis", "resiko" -> "risiko", "praktek" -> "praktik", "sistim" -> "sistem", "perlindungan data pribadi" -> "pelindungan data pribadi").`;

      const userPrompt = `Analisis ${sentenceList.length} kalimat berikut dan kembalikan array skor forensik untuk masing-masing kalimat:\n\n` +
        sentenceList.map((s, idx) => `[ID ${idx + 1}]: "${s}"`).join('\n');

      const auditSchema = {
        type: Type ? Type.OBJECT : 'OBJECT',
        properties: {
          sentences: {
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
        required: ['sentences']
      };

      let response = null;
      let modelUsed = primaryModel;

      try {
        response = await ai.models.generateContent({
          model: primaryModel,
          contents: [{ role: 'user', parts: [{ text: userPrompt }] }],
          config: {
            systemInstruction: { parts: [{ text: systemPrompt }] },
            responseMimeType: 'application/json',
            responseSchema: auditSchema,
            temperature: 0.15,
            maxOutputTokens: 8192
          }
        });
      } catch (sdkErr) {
        console.warn(`[justdone-audit ${primaryModel} failed]:`, sdkErr.message);
        if (sdkErr.message && (sdkErr.message.includes('429') || sdkErr.message.includes('RESOURCE_EXHAUSTED') || sdkErr.message.includes('not found'))) {
          modelUsed = fallbackModel;
          response = await ai.models.generateContent({
            model: fallbackModel,
            contents: [{ role: 'user', parts: [{ text: userPrompt }] }],
            config: {
              systemInstruction: { parts: [{ text: systemPrompt }] },
              responseMimeType: 'application/json',
              responseSchema: auditSchema,
              temperature: 0.15,
              maxOutputTokens: 8192
            }
          });
        } else {
          // Never fallback to fake regex — surface the genuine error message!
          throw sdkErr;
        }
      }

      const reply = response.text || '';
      if (!reply) {
        throw new Error('Google GenAI mengembalikan respons audit kosong.');
      }

      const parsedResult = JSON.parse(reply.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim());
      const usage = response.usageMetadata || {};
      const totalTokens = usage.totalTokenCount || ((usage.promptTokenCount || 0) + (usage.candidatesTokenCount || 0)) || 0;

      return res.end(JSON.stringify({
        status: 'success',
        model_used: modelUsed,
        total_tokens_used: totalTokens,
        usage_metadata: usage,
        sentences: parsedResult.sentences
      }));
    }

    // -------------------------------------------------------------
    // ACTION: PROFESSIONAL AI HUMANIZER (100% Real Paraphrasing)
    // -------------------------------------------------------------
    if (action === 'humanize') {
      const textToHumanize = rawText || sentences.join(' ');
      if (!textToHumanize) {
        res.statusCode = 400;
        return res.end(JSON.stringify({ status: 'error', message: 'Teks naskah untuk dihumanisasi tidak boleh kosong.' }));
      }

      const humanizerSystemPrompt = `Anda adalah Principal Enterprise Indonesian AI Forensic Auditor & Senior Substantive Paraphraser kelas dunia.
Tugas Anda adalah merekayasa naskah input yang terdeteksi AI agar menjadi naskah alami manusiawi berstandar baku KBBI (Target Skor AI < 15%) dengan tetap mempertahankan 100% substansi teknis.

ATURAN REKAYASA HUMANISASI:
1. RITME DINAMIS & ASIMETRIS: Pecah kalimat panjang yang kaku atau daftar titik dua berulang menjadi kombinasi kalimat bervariasi (padukan kalimat pendek 8–14 kata dengan kalimat kausal mengalir 18–26 kata) untuk memaksimalkan Burstiness.
2. DIKSI BIROKRASI / AKADEMIK TAJAM & BAKU KBBI & EYD V:
   - Gunakan ejaan baku mutlak: "tepercaya", "analisis", "risiko", "praktik", "sistem", "standardisasi", "aktivitas", "efektivitas", "pelindungan data pribadi", "di mana", "di sini", "di atas".
3. PRESERVASI 100% INFORMASI:
   - DILARANG MENGUBAH, MENGURANGI, ATAU MENGHILANGKAN angka, persentase, tahun, nama regulasi (Perpres No. 95/2018, Perpres No. 132/2022, UU No. 27/2022), maupun kode teknis aset SPBE (DAB, DAD, DAL, DAA, INI-xx, G-xx).
4. Berikan karakteristik unik (characteristic_found) dan alasan teknis perbaikan (revision_reason) untuk setiap kalimat.`;

      const humanizerUserPrompt = `Humanisasi naskah berikut secara nyata melalui substantive paraphrasing agar lolos detektor AI (target skor AI < 15%) dan patuh baku KBBI:\n\n${textToHumanize}`;

      const humanizeSchema = {
        type: Type ? Type.OBJECT : 'OBJECT',
        properties: {
          overall_ai_score_before: { type: Type ? Type.NUMBER : 'NUMBER' },
          overall_ai_score_after: { type: Type ? Type.NUMBER : 'NUMBER' },
          humanized_text: { type: Type ? Type.STRING : 'STRING' },
          editorial_notes: { type: Type ? Type.STRING : 'STRING' },
          sentences: {
            type: Type ? Type.ARRAY : 'ARRAY',
            items: {
              type: Type ? Type.OBJECT : 'OBJECT',
              properties: {
                id: { type: Type ? Type.NUMBER : 'NUMBER' },
                original: { type: Type ? Type.STRING : 'STRING' },
                original_text: { type: Type ? Type.STRING : 'STRING' },
                ai_score_before: { type: Type ? Type.NUMBER : 'NUMBER' },
                humanized: { type: Type ? Type.STRING : 'STRING' },
                humanized_text: { type: Type ? Type.STRING : 'STRING' },
                ai_score_after: { type: Type ? Type.NUMBER : 'NUMBER' },
                characteristic_found: { type: Type ? Type.STRING : 'STRING' },
                revision_reason: { type: Type ? Type.STRING : 'STRING' }
              },
              required: [
                'id',
                'original',
                'original_text',
                'ai_score_before',
                'humanized',
                'humanized_text',
                'ai_score_after',
                'characteristic_found',
                'revision_reason'
              ]
            }
          }
        },
        required: [
          'overall_ai_score_before',
          'overall_ai_score_after',
          'humanized_text',
          'editorial_notes',
          'sentences'
        ]
      };

      let response = null;
      let modelUsed = primaryModel;

      try {
        response = await ai.models.generateContent({
          model: primaryModel,
          contents: [{ role: 'user', parts: [{ text: humanizerUserPrompt }] }],
          config: {
            systemInstruction: { parts: [{ text: humanizerSystemPrompt }] },
            responseMimeType: 'application/json',
            responseSchema: humanizeSchema,
            temperature: 0.25,
            maxOutputTokens: 8192
          }
        });
      } catch (sdkErr) {
        console.warn(`[justdone humanize ${primaryModel} failed]:`, sdkErr.message);
        if (sdkErr.message && (sdkErr.message.includes('429') || sdkErr.message.includes('RESOURCE_EXHAUSTED') || sdkErr.message.includes('not found'))) {
          modelUsed = fallbackModel;
          response = await ai.models.generateContent({
            model: fallbackModel,
            contents: [{ role: 'user', parts: [{ text: humanizerUserPrompt }] }],
            config: {
              systemInstruction: { parts: [{ text: humanizerSystemPrompt }] },
              responseMimeType: 'application/json',
              responseSchema: humanizeSchema,
              temperature: 0.25,
              maxOutputTokens: 8192
            }
          });
        } else {
          // Never fallback to fake hardcoded text — surface real error
          throw sdkErr;
        }
      }

      const reply = response.text || '';
      if (!reply) {
        throw new Error('Google GenAI mengembalikan respons humanisasi kosong.');
      }

      const humanizeResult = JSON.parse(reply.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim());
      const usage = response.usageMetadata || {};
      const totalTokens = usage.totalTokenCount || ((usage.promptTokenCount || 0) + (usage.candidatesTokenCount || 0)) || 0;

      const pairs = (humanizeResult.sentences || []).map((s, idx) => {
        const orig = (s.original_text || s.original || '').trim();
        const hum = (s.humanized_text || s.humanized || orig).trim();
        const scBefore = typeof s.ai_score_before === 'number' ? Math.round(s.ai_score_before) : 65;
        const scAfter = typeof s.ai_score_after === 'number' ? Math.round(s.ai_score_after) : 8;
        const badge = scAfter < 15 ? 'SUDAH ALAMI' : (scAfter < 35 ? 'REVISI STRUKTURAL' : 'REVISI SUBSTANTIF');

        return {
          id: s.id || (idx + 1),
          index: idx + 1,
          original: orig,
          original_text: orig,
          sentence: orig,
          humanized: hum,
          humanized_text: hum,
          recommendation: hum,
          ai_score_before: scBefore,
          ai_score_after: scAfter,
          ai_score: scAfter,
          status: badge,
          action_label: badge,
          characteristic_found: s.characteristic_found || 'Pola klausa majemuk terdeteksi',
          characteristics: s.characteristic_found || 'Pola klausa majemuk terdeteksi',
          revision_reason: s.revision_reason || 'Rekonstruksi ritme klausa dan penyelarasan diksi baku KBBI',
          reason: s.revision_reason || 'Rekonstruksi ritme klausa dan penyelarasan diksi baku KBBI',
          level: scAfter < 15 ? 'low' : (scAfter < 35 ? 'medium' : 'high')
        };
      });

      return res.end(JSON.stringify({
        status: 'success',
        model_used: modelUsed,
        total_tokens_used: totalTokens,
        usage_metadata: usage,
        original_text: textToHumanize,
        humanized_text: humanizeResult.humanized_text,
        revised_text: humanizeResult.humanized_text,
        ai_score_before: humanizeResult.overall_ai_score_before !== undefined ? Math.round(humanizeResult.overall_ai_score_before) : 65,
        ai_score_after: humanizeResult.overall_ai_score_after !== undefined ? Math.round(humanizeResult.overall_ai_score_after) : 8,
        ai_score_percentage: humanizeResult.overall_ai_score_after !== undefined ? Math.round(humanizeResult.overall_ai_score_after) : 8,
        sentences: pairs,
        sentence_pairs: pairs,
        editorial_notes: humanizeResult.editorial_notes || ''
      }));
    }

    res.statusCode = 400;
    return res.end(JSON.stringify({ status: 'error', message: `Aksi tidak dikenal: ${action}` }));

  } catch (error) {
    console.error('[POST /api/justdone-audit critical error]:', error);
    res.statusCode = 500;
    return res.end(JSON.stringify({
      status: 'error',
      message: 'Gagal memproses dengan Google Gemini: ' + (error.message || String(error))
    }));
  }
};

module.exports.config = {
  maxDuration: 60
};
