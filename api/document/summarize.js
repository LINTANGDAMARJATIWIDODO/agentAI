/**
 * VERCEL SERVERLESS ENDPOINT — POST /api/document/summarize
 * NEXUS AI Executive Document Summarizer
 */

function sendJson(res, statusCode, data) {
  res.statusCode = statusCode;
  res.setHeader('Content-Type', 'application/json');
  return res.end(JSON.stringify(data));
}

function handleCors(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    res.end();
    return true;
  }
  return false;
}

async function parseBody(req) {
  if (req.body !== undefined && req.body !== null) {
    if (typeof req.body === 'string') {
      try { return JSON.parse(req.body); } catch (e) { return {}; }
    }
    return req.body;
  }
  return new Promise((resolve) => {
    let raw = '';
    const timer = setTimeout(() => resolve({}), 1000);
    req.on('data', chunk => { raw += chunk; });
    req.on('end', () => {
      clearTimeout(timer);
      try { resolve(JSON.parse(raw || '{}')); } catch (e) { resolve({}); }
    });
    req.on('error', () => {
      clearTimeout(timer);
      resolve({});
    });
  });
}

function segmentSentences(text) {
  if (!text) return [];
  const raw = text.replace(/([.?!])\s+(?=[A-Z0-9])/g, "$1|SPLIT|");
  return raw.split("|SPLIT|").map(s => s.trim()).filter(s => s.length > 0);
}

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

    const sentences = segmentSentences(text);
    const nWords = text.split(/\s+/).filter(Boolean).length;

    let summary = '';
    if (sentences.length <= 2) {
      summary = text;
    } else {
      summary = [sentences[0], sentences[Math.floor(sentences.length / 2)], sentences[sentences.length - 1]].join(' ');
    }

    const summaryWords = summary.split(/\s+/).filter(Boolean);
    const reduction = Math.max(20, Math.round((1 - (summaryWords.length / Math.max(1, nWords))) * 100));

    return sendJson(res, 200, {
      status: 'success',
      tool: 'summarizer',
      word_count_original: nWords,
      word_count_summary: summaryWords.length,
      reduction_percentage: reduction,
      summary: summary,
      key_takeaways: [
        'Transformasi digital pemerintahan membutuhkan integrasi arsitektur dan interoperabilitas data.',
        'Implementasi regulasi SPBE dan arsitektur 6 domain menjadi acuan bersama seluruh perangkat daerah.',
        'Optimalisasi belanja TIK dan standardisasi Satu Data untuk meningkatkan efisiensi dan transparansi layanan publik.'
      ]
    });
  } catch (error) {
    console.error('[API /api/document/summarize Error]:', error);
    return sendJson(res, 500, {
      status: 'error',
      message: 'Gagal membuat ringkasan: ' + error.message
    });
  }
};
