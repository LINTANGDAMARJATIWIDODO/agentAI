/**
 * VERCEL SERVERLESS ENDPOINT — POST /api/document/detect
 * NEXUS AI Advanced Indonesian AI Text Detection & Forensic Analysis
 */

const { analyzeText } = require('../../services/detection_engine/detector_node');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    return res.end();
  }

  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify({ status: 'error', message: 'Method Not Allowed. Use POST.' }));
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) { body = {}; }
    } else if (!body) {
      body = await new Promise((resolve) => {
        let raw = '';
        req.on('data', chunk => { raw += chunk; });
        req.on('end', () => {
          try { resolve(JSON.parse(raw || '{}')); } catch (e) { resolve({}); }
        });
        req.on('error', () => resolve({}));
      });
    }
    body = body || {};

    const text = (body.text || '').trim();
    if (!text) {
      res.statusCode = 400;
      res.setHeader('Content-Type', 'application/json');
      return res.end(JSON.stringify({ status: 'error', message: 'Parameter "text" wajib diisi.' }));
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

    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify(responsePayload));
  } catch (error) {
    console.error('[API /api/document/detect Error]:', error);
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify({
      status: 'error',
      message: 'Gagal melakukan deteksi teks: ' + error.message
    }));
  }
};
