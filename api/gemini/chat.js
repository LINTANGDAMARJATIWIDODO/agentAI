/**
 * Vercel Serverless Function: POST /api/gemini/chat
 * Native Node.js Serverless Handler for Google Gemini Chat, Extended Thinking, & General-Purpose Intelligence
 */
const GeminiClient = require('../../services/gemini/geminiClient');

module.exports = async (req, res) => {
  // CORS Headers
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
      if (req.readableEnded || typeof req.on !== 'function') {
        payload = {};
      } else {
        payload = await new Promise((resolve) => {
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
    }

    const prompt = payload.prompt || '';
    const agent = payload.agent || 'ARKA';
    const tier = payload.tier || payload.cognitive_brain || 'flash';
    const cognitive_brain = payload.cognitive_brain || payload.tier || 'flash';
    const history = payload.history || [];
    const enable_grounding = payload.enable_grounding || false;

    // Dispatches to GeminiClient with general-purpose routing & optional web grounding
    const result = await GeminiClient.chat({
      prompt,
      agent,
      tier,
      cognitive_brain,
      history,
      enable_grounding
    });

    res.statusCode = 200;
    return res.end(JSON.stringify(result));
  } catch (err) {
    console.error('[API /api/gemini/chat error]:', err);
    res.statusCode = 200;
    return res.end(JSON.stringify({
      status: 'error',
      message: err.message || 'Terjadi kendala pada layanan kognitif Google Gemini.'
    }));
  }
};

module.exports.config = {
  maxDuration: 60
};
