/**
 * VERCEL SERVERLESS ENDPOINT — /api/detector/analyze
 * NEXUS AI Advanced Indonesian AI Text Detection & Forensic Analysis
 */

let detectorModule;
try {
  detectorModule = require('./detector_node');
} catch (e) {
  detectorModule = require('../../services/detection_engine/detector_node');
}
const { analyzeText } = detectorModule;

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
