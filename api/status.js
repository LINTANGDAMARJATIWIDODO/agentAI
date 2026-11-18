/**
 * Vercel Serverless Function: GET /api/status
 */
const fs = require('fs');
const path = require('path');

const BASE_DIR = path.resolve(__dirname, '..');
const LOGS_FILE = path.join(BASE_DIR, 'logs', 'activity_log.json');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    return res.end();
  }

  res.setHeader('Content-Type', 'application/json');

  let state = {
    status: 'ONLINE',
    orchestrator: 'ARKA',
    tasks: [],
    active_app: {
      title: "APEX MOTO & AUTO WORKS — Bengkel Resmi Modern",
      button_label: "🚀 Buka Web Bengkel",
      url: "/buatkan_web_bengkel/index.html",
      status: "LIVE & DEPLOYED"
    }
  };

  try {
    if (fs.existsSync(LOGS_FILE)) {
      const parsed = JSON.parse(fs.readFileSync(LOGS_FILE, 'utf-8'));
      state = { ...state, ...parsed };
    }
  } catch (e) {}

  state.status = state.status || state.system_state || 'ONLINE';
  res.statusCode = 200;
  return res.end(JSON.stringify(state));
};
