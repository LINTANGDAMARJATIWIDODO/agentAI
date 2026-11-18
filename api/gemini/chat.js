/**
 * Vercel Serverless Function: POST /api/gemini/chat
 * Native Node.js Serverless Handler for Google Gemini Chat & Code Generation
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
      // Buffer stream if body was not auto-parsed by Vercel
      payload = await new Promise((resolve) => {
        let raw = '';
        req.on('data', chunk => { raw += chunk; });
        req.on('end', () => {
          try { resolve(JSON.parse(raw || '{}')); } catch (e) { resolve({}); }
        });
        req.on('error', () => resolve({}));
      });
    }

    const prompt = payload.prompt || '';
    const agent = payload.agent || 'ARKA';
    const tier = payload.tier || 'flash';
    const history = payload.history || [];
    const enable_grounding = payload.enable_grounding || false;

    // Direct REST invocation to Google Gemini API
    const result = await GeminiClient.chatDirectRest({
      prompt,
      agent,
      tier,
      history,
      enable_grounding
    });

    res.statusCode = 200;
    return res.end(JSON.stringify(result));
  } catch (err) {
    console.error('[API /api/gemini/chat error]:', err);
    res.statusCode = 200; // Return 200 with error JSON so frontend handles gracefully
    return res.end(JSON.stringify({
      status: 'error',
      message: err.message || 'Terjadi kesalahan saat menghubungi Google Gemini API.'
    }));
  }
};
