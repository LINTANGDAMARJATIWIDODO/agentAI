/**
 * VERCEL SERVERLESS ENDPOINT — POST /api/document/grammar
 * NEXUS AI Indonesian Grammar & Spelling Checker (KBBI & EYD V)
 */

const { sendJson, handleCors, parseBody } = require('../_util');

const TYPO_RULES = [
  { wrong: /\bpraktek\b/gi, right: 'praktik', note: 'KBBI: Ragam baku adalah praktik' },
  { wrong: /\baktifitas\b/gi, right: 'aktivitas', note: 'KBBI: Ragam baku menggunakan v' },
  { wrong: /\befisiensi anggaran yang mana\b/gi, right: 'efisiensi anggaran yang', note: 'EYD V: Bentuk mubazir (yang mana)' },
  { wrong: /\bmerubah\b/gi, right: 'mengubah', note: 'KBBI: Imbuhan meng- bertemu bentuk dasar ubah' },
  { wrong: /\bkualitas daripada\b/gi, right: 'kualitas', note: 'EYD V: Kata daripada hanya untuk perbandingan' },
  { wrong: /\bdimana\b/gi, right: 'tempat', note: 'EYD V: Dimana adalah kata tanya tempat, bukan relatif' },
  { wrong: /\bhakekat\b/gi, right: 'hakikat', note: 'KBBI: Bentuk baku adalah hakikat' },
  { wrong: /\bkhromosom\b/gi, right: 'kromosom', note: 'KBBI: Bentuk serapan baku tanpa h' },
  { wrong: /\bkomplit\b/gi, right: 'lengkap', note: 'KBBI: Penggunaan ragam formal adalah lengkap' }
];

module.exports = async function handler(req, res) {
  if (handleCors(req, res)) return;

  if (req.method !== 'POST') {
    return sendJson(res, 405, { status: 'error', message: 'Method Not Allowed. Use POST.' });
  }

  try {
    const body = await parseBody(req);
    const text = (body.text || '').trim();
    if (!text) {
      return sendJson(res, 400, { status: 'error', message: 'Parameter "text" wajib diisi.' });
    }

    let correctedText = text;
    const issues = [];

    TYPO_RULES.forEach(r => {
      let m;
      const re = new RegExp(r.wrong.source, 'gi');
      while ((m = re.exec(text)) !== null) {
        issues.push({
          wrong: m[0],
          suggestion: r.right,
          rule: r.note,
          index: m.index
        });
      }
      correctedText = correctedText.replace(r.wrong, r.right);
    });

    const score = issues.length === 0 ? '100% (Sempurna Baku)' : `${Math.max(70, 100 - issues.length * 6)}%`;

    return sendJson(res, 200, {
      status: 'success',
      tool: 'grammar_checker',
      original_text: text,
      corrected_text: correctedText,
      issues_count: issues.length,
      issues: issues,
      grammar_score: score
    });
  } catch (error) {
    console.error('[API /api/document/grammar Error]:', error);
    return sendJson(res, 500, {
      status: 'error',
      message: 'Gagal melakukan audit tata bahasa: ' + error.message
    });
  }
};
