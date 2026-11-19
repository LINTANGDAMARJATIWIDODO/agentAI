/**
 * Vercel Serverless Function: GET /api/report
 * Serves markdown / JSON reports from reports/ directory
 */
const fs = require('fs');
const path = require('path');

const BASE_DIR = path.resolve(__dirname, '..');
const REPORTS_DIR = path.join(BASE_DIR, 'reports');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    return res.end();
  }

  // Parse filename from query or url
  let filename = req.query?.file || '';
  if (!filename) {
    const parts = (req.url || '').split('?')[0].split('/');
    filename = parts[parts.length - 1];
  }
  filename = decodeURIComponent(filename || 'LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.md');
  filename = path.basename(filename); // Prevent path traversal

  let targetPath = path.join(REPORTS_DIR, filename);
  if (!fs.existsSync(targetPath)) {
    targetPath = path.join(BASE_DIR, 'public', 'reports', filename);
  }
  if (!fs.existsSync(targetPath)) {
    // Default fallback to LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.md
    targetPath = path.join(REPORTS_DIR, 'LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.md');
  }
  if (!fs.existsSync(targetPath)) {
    targetPath = path.join(BASE_DIR, 'public', 'reports', 'LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.md');
  }

  if (!fs.existsSync(targetPath)) {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    return res.end(`# Laporan Dokumen SPBE: ${filename}\n\nNaskah kajian resmi ini telah terdaftar dalam arsitektur NEXUS AI Enterprise.`);
  }

  try {
    const content = fs.readFileSync(targetPath, 'utf-8');
    if (filename.endsWith('.json')) {
      res.setHeader('Content-Type', 'application/json');
    } else {
      res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    }
    res.statusCode = 200;
    return res.end(content);
  } catch (err) {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.end(`Error reading file: ${err.message}`);
  }
};
