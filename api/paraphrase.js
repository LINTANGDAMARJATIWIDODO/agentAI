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
  const paraphrased = text
    .replace(/\bdalam rangka untuk\b/gi, 'guna')
    .replace(/\bmerupakan salah satu\b/gi, 'tergolong sebagai')
    .replace(/\bsangat penting sekali\b/gi, 'esensial');

  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json');
  return res.end(JSON.stringify({
    status: 'success',
    tool: 'paraphraser',
    original_text: text,
    paraphrased_text: paraphrased,
    sentences: [{ index: 1, original: text, paraphrased: paraphrased, ai_score: 0.04, level: 'low' }],
    sentence_counts: { total: 1, ai: 0, mixed: 0, human: 1 }
  }));
};
