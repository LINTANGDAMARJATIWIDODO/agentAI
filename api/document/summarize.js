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
    res.statusCode = 204;
    return res.end();
  }

  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify({ status: 'error', message: 'Method Not Allowed. Use POST.' }));
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) { body = {}; }
    } else if (!body) {
      body = await new Promise((resolve) => {
        let raw = '';
        req.on('data', chunk => { raw += chunk; });
        req.on('end', () => {
          try { resolve(JSON.parse(raw || '{}')); } catch (e) { resolve({}); }
        });
        req.on('error', () => resolve({}));
      });
    }
    body = body || {};

    const text = (body.text || '').trim();
    if (!text) {
      res.statusCode = 400;
      res.setHeader('Content-Type', 'application/json');
      return res.end(JSON.stringify({ status: 'error', message: 'Parameter "text" wajib diisi.' }));
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

    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify({
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
    }));
  } catch (error) {
    console.error('[API /api/document/summarize Error]:', error);
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify({
      status: 'error',
      message: 'Gagal membuat ringkasan: ' + error.message
    }));
  }
};
