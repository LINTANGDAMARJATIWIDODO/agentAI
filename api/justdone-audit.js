/**
 * Vercel Serverless Function: POST /api/justdone-audit
 * ==========================================================
 * Real AI Forensic Scoring & Substantive Paraphrasing Humanizer
 * Powered 100% by Google GenAI SDK (@google/genai) with v1beta & Direct REST Failover
 *
 * 100% Stateless & Vercel Serverless Ready (export const maxDuration = 60).
 */

const humanizeHandler = require('./humanize');

module.exports = async (req, res) => {
  return humanizeHandler(req, res);
};

module.exports.config = {
  maxDuration: 60
};
