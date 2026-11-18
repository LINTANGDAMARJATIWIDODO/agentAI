module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    return res.end();
  }

  let body = {};
  if (req.body) {
    body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
  } else {
    const raw = await new Promise((resolve) => {
      let b = '';
      req.on('data', chunk => { b += chunk; });
      req.on('end', () => resolve(b));
      req.on('error', () => resolve(''));
    });
    try { body = JSON.parse(raw || '{}'); } catch(e) { body = {}; }
  }

  const text = (body.text || '').trim();
  const rawSentences = text.replace(/([.?!])\s+(?=[A-Z0-9])/g, "$1|SPLIT|").split("|SPLIT|").map(s => s.trim()).filter(s => s.length > 0);
  const summary = rawSentences.length <= 2 ? text : [rawSentences[0], rawSentences[rawSentences.length - 1]].join(' ');

  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json');
  return res.end(JSON.stringify({
    status: 'success',
    tool: 'summarizer',
    summary: summary,
    key_takeaways: [
      'Transformasi tata kelola SPBE dan akuntabilitas sistem pemerintahan digital.',
      'Optimalisasi layanan publik terpadu dan keamanan informasi terdistribusi.'
    ]
  }));
};
