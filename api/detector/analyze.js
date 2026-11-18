/**
 * VERCEL SERVERLESS ENDPOINT — /api/detector/analyze
 * NEXUS AI Advanced Indonesian AI Text Detection & Forensic Analysis
 */

const { analyzeText } = require('../../services/detection_engine/detector_node');
const { sendJson, handleCors, parseBody } = require('../_util');

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

    const report = await analyzeText(text, {
      geminiApiKey: process.env.GEMINI_API_KEY || ''
    });

    return sendJson(res, 200, report);
  } catch (error) {
    console.error('Detector API Error:', error);
    return sendJson(res, 500, {
      status: 'error',
      message: 'Gagal melakukan analisis deteksi teks: ' + error.message
    });
  }
};
