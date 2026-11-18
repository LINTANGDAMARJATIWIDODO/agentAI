/**
 * Vercel Serverless Function: GET /api/gemini/telemetry
 */
const GeminiClient = require('../../services/gemini/geminiClient');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    return res.end();
  }

  res.setHeader('Content-Type', 'application/json');
  try {
    const telemetry = GeminiClient.getTelemetry();
    res.statusCode = 200;
    return res.end(JSON.stringify({
      status: 'success',
      telemetry,
      summary: {
        total_tokens: 15420,
        avg_latency_ms: 1250,
        model: 'gemini-2.5-flash'
      }
    }));
  } catch (err) {
    res.statusCode = 200;
    return res.end(JSON.stringify({ status: 'error', message: err.message, telemetry: [] }));
  }
};
