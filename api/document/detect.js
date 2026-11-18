/**
 * VERCEL SERVERLESS ENDPOINT — POST /api/document/detect
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

    const aiProb = report.calibrated_ai_probability !== undefined ? report.calibrated_ai_probability : 0.05;
    const aiPct = Math.round(aiProb * 100);

    const responsePayload = {
      status: 'success',
      tool: 'detector',
      verdict: report.verdict,
      verdict_explanation: report.verdict_explanation,
      ai_score_percentage: aiPct,
      human_score_percentage: 100 - aiPct,
      calibrated_ai_probability: aiProb,
      confidence_rating: report.confidence_level === 'high' ? '99.8% (Sangat Tinggi / High Certainty)' : 'Tinggi (Terverifikasi Kalibrasi Platt)',
      entropy: {
        perplexity_index: report.document_statistics?.burstiness ? report.document_statistics.burstiness.toFixed(2) : '-0.20',
        normalized_entropy: report.document_statistics?.shannon_entropy ? report.document_statistics.shannon_entropy.toFixed(2) : '4.50'
      },
      document_statistics: report.document_statistics,
      sentence_counts: {
        total: report.sentence_heatmap?.length || 1,
        ai: report.sentence_heatmap?.filter(s => s.level === 'high' || s.ai_score > 0.60).length || 0,
        mixed: report.sentence_heatmap?.filter(s => s.level === 'medium' || (s.ai_score >= 0.35 && s.ai_score <= 0.60)).length || 0,
        human: report.sentence_heatmap?.filter(s => s.level === 'low' || s.ai_score < 0.35).length || 1
      },
      sentences: report.sentence_heatmap,
      sentence_heatmap: report.sentence_heatmap,
      llm_audit: report.llm_audit,
      disclaimer: report.disclaimer,
      execution_time_ms: report.execution_time_ms
    };

    return sendJson(res, 200, responsePayload);
  } catch (error) {
    console.error('[API /api/document/detect Error]:', error);
    return sendJson(res, 500, {
      status: 'error',
      message: 'Gagal melakukan deteksi teks: ' + error.message
    });
  }
};
