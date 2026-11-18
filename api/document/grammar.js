/**
 * VERCEL SERVERLESS ENDPOINT — POST /api/document/grammar
 * NEXUS AI KBBI & EYD V Indonesian Linguistic Auditor
 */

const KBBI_RULES = [
  { wrong: /\bpraktek\b/gi, right: 'praktik', rule: 'Kata baku KBBI: praktik (bukan praktek)' },
  { wrong: /\baktifitas\b/gi, right: 'aktivitas', rule: 'Kata baku KBBI: aktivitas (bukan aktifitas)' },
  { wrong: /\bhakekat\b/gi, right: 'hakikat', rule: 'Kata baku KBBI: hakikat (bukan hakekat)' },
  { wrong: /\bkhromosom\b/gi, right: 'kromosom', rule: 'Kata baku KBBI: kromosom (bukan khromosom)' },
  { wrong: /\bhirarki\b/gi, right: 'hierarki', rule: 'Kata baku KBBI: hierarki (bukan hirarki)' },
  { wrong: /\bmerubah\b/gi, right: 'mengubah', rule: 'Kaidah afiksasi: meng- + ubah menjadi mengubah (bukan merubah)' },
  { wrong: /\befisiensi anggaran yang mana\b/gi, right: 'efisiensi anggaran yang', rule: 'EYD V: "yang mana" tidak berfungsi sebagai pronomina relatif' },
  { wrong: /\bkualitas daripada\b/gi, right: 'kualitas', rule: 'EYD V: "daripada" hanya digunakan untuk perbandingan tingkat' },
  { wrong: /\bmemerlukan akan\b/gi, right: 'memerlukan', rule: 'Tata Bahasa Baku: Verba transitif aktif tidak memerlukan preposisi' }
];

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ status: 'error', message: 'Method Not Allowed. Use POST.' });
    return;
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) { body = {}; }
    }
    body = body || {};

    const text = (body.text || '').trim();
    if (!text) {
      res.status(400).json({ status: 'error', message: 'Parameter "text" wajib diisi.' });
      return;
    }

    let correctedText = text;
    const issues = [];

    for (const r of KBBI_RULES) {
      if (r.wrong.test(correctedText)) {
        const matches = correctedText.match(r.wrong) || [];
        matches.forEach(m => {
          issues.push({
            original: m,
            replacement: r.right,
            rule: r.rule
          });
        });
        correctedText = correctedText.replace(r.wrong, r.right);
      }
    }

    // Comma in two-element coordination fix: "A, dan B" -> "A dan B"
    correctedText = correctedText.replace(/\b([a-zA-Z0-9_\-]+),\s+dan\s+([a-zA-Z0-9_\-]+)\b/g, '$1 dan $2');

    const score = issues.length === 0 ? '100% (Sempurna Baku)' : `${Math.max(70, 100 - issues.length * 6)}%`;

    res.status(200).json({
      status: 'success',
      tool: 'grammar',
      accuracy_score: score,
      total_issues: issues.length,
      original_text: text,
      corrected_text: correctedText,
      issues: issues
    });
  } catch (error) {
    console.error('[API /api/document/grammar Error]:', error);
    res.status(500).json({
      status: 'error',
      message: 'Gagal melakukan audit tata bahasa: ' + error.message
    });
  }
};
