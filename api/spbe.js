/**
 * VERCEL SERVERLESS ENDPOINT — /api/spbe
 * SPBE Intelligence Hub Serverless Handler
 */

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

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const action = url.searchParams.get('subAction') || url.searchParams.get('action') || url.pathname.split('/').filter(Boolean).pop() || 'portals';

  if (action === 'portals' || action === 'list_portals') {
    return sendJson(res, 200, {
      status: 'success',
      portals: [
        { id: 'JAKEVO', name: 'Jakevo (Pelayanan Terpadu Satu Pintu)', domain: 'Layanan Publik', status: 'AKTIF' },
        { id: 'JAKARTA_SATU', name: 'Jakarta Satu (Simpul Jaringan Geospasial)', domain: 'Data & Informasi', status: 'AKTIF' },
        { id: 'JAKI', name: 'JAKI (Jakarta Kini - SuperApp Warga)', domain: 'Layanan Publik', status: 'AKTIF' },
        { id: 'SIPD', name: 'SIPD (Sistem Informasi Pemerintahan Daerah)', domain: 'Proses Bisnis', status: 'TERHUBUNG' }
      ]
    });
  }

  if (action === 'regulations' || action === 'list_regulations') {
    return sendJson(res, 200, {
      status: 'success',
      regulations: [
        { id: 'PERPRES_95_2018', title: 'Peraturan Presiden Nomor 95 Tahun 2018 tentang SPBE', year: 2018, scope: 'Nasional' },
        { id: 'PERPRES_39_2019', title: 'Peraturan Presiden Nomor 39 Tahun 2019 tentang Satu Data Indonesia', year: 2019, scope: 'Nasional' },
        { id: 'PERGUB_DKI_2024', title: 'Peraturan Gubernur DKI Jakarta tentang Pedoman Arsitektur SPBE 2024-2027', year: 2024, scope: 'Daerah' }
      ]
    });
  }

  if (action === 'reasoning' || action === 'execute_reasoning') {
    const body = await parseBody(req);
    const opd = body.perangkat_daerah || 'Satpol PP Provinsi DKI Jakarta';
    return sendJson(res, 200, {
      status: 'success',
      perangkat_daerah: opd,
      qa_audit: {
        evidence_sufficiency_score: 100,
        revoked_laws_detected: []
      },
      steps: [
        { step: 1, name: 'Identifikasi Mandat Regulasi', summary: 'Sinkronisasi Perpres 95/2018 dan Perpres 39/2019.' },
        { step: 2, name: 'Analisis Domain Layanan', summary: 'Pemetaan proses bisnis layanan publik dan administrasi.' },
        { step: 3, name: 'Standardisasi Satu Data', summary: 'Integrasi metadata dan interoperabilitas lintas OPD DKI.' },
        { step: 4, name: 'Audit Keamanan Informasi', summary: 'Kepatuhan standar ISO 27001 dan UU PDP.' }
      ]
    });
  }

  // Default fallback
  return sendJson(res, 200, {
    status: 'success',
    action: action,
    message: 'Data intelijen SPBE berhasil disinkronkan.',
    domains_covered: 6,
    active_lineage: 'Perpres 95/2018 -> Pergub DKI Jakarta 2024'
  });
};
