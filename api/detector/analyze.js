/**
 * VERCEL SERVERLESS ENDPOINT — /api/detector/analyze
 * NEXUS AI Advanced Indonesian AI Text Detection & Forensic Analysis
 */

const { analyzeText } = require('../../services/detection_engine/detector_node');

module.exports = async function handler(req, res) {
  // CORS Headers
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
      try {
        body = JSON.parse(body);
      } catch (e) {
        body = {};
      }
    }
    body = body || {};

    const text = (body.text || '').trim();
    if (!text) {
      res.status(400).json({ status: 'error', message: 'Parameter "text" wajib diisi.' });
      return;
    }

    const report = await analyzeText(text, {
      geminiApiKey: process.env.GEMINI_API_KEY || ''
    });

    res.status(200).json(report);
  } catch (error) {
    console.error('Detector API Error:', error);
    res.status(500).json({
      status: 'error',
      message: 'Gagal melakukan analisis deteksi teks: ' + error.message
    });
  }
};
