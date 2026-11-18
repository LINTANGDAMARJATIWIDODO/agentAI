/**
 * VERCEL SERVERLESS ENDPOINT — /api/spbe/*
 * SPBE Intelligence Hub Serverless Router
 */

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const action = url.pathname.split('/').pop() || 'portals';

  if (action === 'portals') {
    return res.status(200).json({
      status: 'success',
      portals: [
        { id: 'JAKEVO', name: 'Jakevo (Pelayanan Terpadu Satu Pintu)', domain: 'Layanan Publik', status: 'AKTIF' },
        { id: 'JAKARTA_SATU', name: 'Jakarta Satu (Simpul Jaringan Geospasial)', domain: 'Data & Informasi', status: 'AKTIF' },
        { id: 'JAKI', name: 'JAKI (Jakarta Kini - SuperApp Warga)', domain: 'Layanan Publik', status: 'AKTIF' },
        { id: 'SIPD', name: 'SIPD (Sistem Informasi Pemerintahan Daerah)', domain: 'Proses Bisnis', status: 'TERHUBUNG' }
      ]
    });
  }

  if (action === 'regulations') {
    return res.status(200).json({
      status: 'success',
      regulations: [
        { id: 'PERPRES_95_2018', title: 'Peraturan Presiden Nomor 95 Tahun 2018 tentang SPBE', year: 2018, scope: 'Nasional' },
        { id: 'PERPRES_39_2019', title: 'Peraturan Presiden Nomor 39 Tahun 2019 tentang Satu Data Indonesia', year: 2019, scope: 'Nasional' },
        { id: 'PERGUB_DKI_2024', title: 'Peraturan Gubernur DKI Jakarta tentang Pedoman Arsitektur SPBE 2024-2027', year: 2024, scope: 'Daerah' }
      ]
    });
  }

  // Default fallback
  res.status(200).json({
    status: 'success',
    action: action,
    message: 'Data intelijen SPBE berhasil disinkronkan.',
    domains_covered: 6,
    active_lineage: 'Perpres 95/2018 -> Pergub DKI Jakarta 2024'
  });
};
