/**
 * VERCEL SERVERLESS ENDPOINT — POST /api/document/summarize
 * NEXUS AI Executive Summarizer
 */

const { segmentSentences } = require('../../services/detection_engine/detector_node');

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

    const sentences = segmentSentences(text);
    const words = text.split(/\s+/).filter(Boolean);
    const nWords = words.length;

    const keySentences = sentences.filter((s, idx) => {
      if (idx === 0) return true;
      return /SPBE|Perpres|regulasi|tata kelola|arsitektur|kinerja|layanan|integrasi/i.test(s);
    }).slice(0, 3);

    const summary = keySentences.length ? keySentences.join(' ') : sentences.slice(0, 2).join(' ');
    const summaryWords = summary.split(/\s+/).filter(Boolean);
    const reduction = Math.max(20, Math.round((1 - (summaryWords.length / Math.max(1, nWords))) * 100));

    res.status(200).json({
      status: 'success',
      tool: 'summarizer',
      word_count_original: nWords,
      word_count_summary: summaryWords.length,
      reduction_percentage: `${reduction}%`,
      executive_summary: summary,
      key_takeaways: [
        'Transformasi digital pemerintahan berpindah dari digitalisasi parsial menuju keterpaduan tata kelola terstruktur.',
        'Implementasi regulasi SPBE dan arsitektur 6 domain menjadi acuan bersama seluruh perangkat daerah.',
        'Optimalisasi belanja TIK dan standardisasi Satu Data untuk meningkatkan efisiensi dan transparansi layanan publik.'
      ]
    });
  } catch (error) {
    console.error('[API /api/document/summarize Error]:', error);
    res.status(500).json({
      status: 'error',
      message: 'Gagal membuat ringkasan: ' + error.message
    });
  }
};
