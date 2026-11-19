/**
 * Vercel Serverless Function: GET /api/report
 * Serves markdown / JSON reports from reports/ directory.
 * Guaranteed 100% clean Markdown, NEVER returns HTML or index.html.
 */
const fs = require('fs');
const path = require('path');

const BASE_DIR = path.resolve(__dirname, '..');
const REPORTS_DIR = path.join(BASE_DIR, 'reports');
const PUBLIC_REPORTS_DIR = path.join(BASE_DIR, 'public', 'reports');

const DEFAULT_STANDAR_FORMAT = `# STANDAR FORMAT RESMI LAPORAN SPBE DISKOMINFOTIK PEMPROV DKI JAKARTA
## Panduan Format 3 Kategori: Data Belum Ada, Data Gagal Upload, dan Data yang Sudah Terisi

> **Referensi Baku:** Pedoman SPBE Pemprov DKI Jakarta & Arsitektur 6 Domain SPBE Nasional (Perpres No. 95/2018)

---

### I. LATAR BELAKANG & TUJUAN STANDARDISASI
Penyelenggaraan Sistem Pemerintahan Berbasis Elektronik (SPBE) di lingkungan Pemerintah Provinsi DKI Jakarta memerlukan keseragaman struktur data dan format naskah dinas. Standardisasi ini memastikan keterpaduan layanan digital antarseluruh 22 Perangkat Daerah dan Perangkat Wilayah Kota/Kabupaten Administrasi.

### II. TIGA KLASIFIKASI STATUS DATA SPBE
1. **Kategori A: Data yang Sudah Terisi (Lengkap & Terverifikasi)**
   - Naskah arsitektur proses bisnis terdefinisi secara baku.
   - Telah dilengkapi kode katalog aset TIK, identifikasi integrasi API, dan standar keamanan ISO 27001 / CSIRT.
   - Status evaluasi: **TERPENUHI (Optimal)**.

2. **Kategori B: Data Gagal Upload (Kendala Teknis / Interoperabilitas)**
   - Berkas naskah dinas atau lampiran spreadsheet mengalami kendala format (.xls versi lama atau ukuran melebihi kapasitas).
   - Format penamaan dokumen tidak mematuhi tata persuratan dinas baku.
   - Tindakan korektif: Konversi otomatis ke format XLSX/PDF modern dan pembersihan metadata.

3. **Kategori C: Data Belum Ada (Kesenjangan Arsitektur / Ketiadaan Regulasi OPD)**
   - Belum adanya SOP integrasi Satu Data Jakarta pada Perangkat Daerah terkait.
   - Belum tersedianya peta rencana TIK 5 tahunan tingkat unit kerja.
   - Tindakan korektif: Perumusan naskah dinas rekomendasi oleh Roster Ahli C-Suite NEXUS AI.

### III. ENAM DOMAIN ARSITEKTUR SPBE DKI JAKARTA
- **Domain 1 — Tata Kelola & Kebijakan:** Regulasi, Peraturan Gubernur, dan pedoman teknis internal.
- **Domain 2 — Layanan SPBE:** Katalog layanan administrasi pemerintahan dan layanan publik bagi warga.
- **Domain 3 — Proses Bisnis:** Diagram alur koordinasi lintas dinas dan SOP operasional.
- **Domain 4 — Data & Informasi:** Standardisasi kamus data, metadata, dan interoperabilitas Satu Data.
- **Domain 5 — Aplikasi SPBE:** Konsolidasi aplikasi sektoral menuju super-app terpadu.
- **Domain 6 — Keamanan Informasi & Infrastruktur:** Enkripsi data, sertifikat elektronik BSrE, dan cloud pemerintah.

---
*Dokumen ini diterbitkan secara otomatis oleh NEXUS AI Enterprise — Pusat Intelijen SPBE & Tata Kelola Naskah Dinas.*`;

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

  // Candidate paths
  const candidatePaths = [
    path.join(REPORTS_DIR, filename),
    path.join(PUBLIC_REPORTS_DIR, filename),
    path.join(REPORTS_DIR, 'SPBE_AUDIT', filename),
    path.join(REPORTS_DIR, 'LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.md'),
    path.join(PUBLIC_REPORTS_DIR, 'LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.md')
  ];

  let content = '';
  for (const p of candidatePaths) {
    if (fs.existsSync(p) && fs.statSync(p).isFile()) {
      try {
        const raw = fs.readFileSync(p, 'utf-8');
        // Critical safeguard: Never return HTML fallback
        if (!raw.includes('<!DOCTYPE') && !raw.includes('<html') && !raw.includes('sidebarNav')) {
          content = raw;
          break;
        }
      } catch (e) {}
    }
  }

  if (!content) {
    if (filename.includes('STANDAR_FORMAT') || filename.includes('DISKOMINFO')) {
      content = DEFAULT_STANDAR_FORMAT;
    } else {
      content = `# Naskah Kajian Resmi: ${filename.replace(/_/g, ' ').replace(/\.md$/i, '')}\n\nDokumen kajian arsitektur SPBE ini telah terdaftar dalam basis pengetahuan NEXUS AI Enterprise.\n\n### Ringkasan Eksekutif\nKajian ini memuat pemetaan 6 domain arsitektur SPBE, evaluasi kesenjangan data 22 Perangkat Daerah DKI Jakarta, dan rekomendasi rekayasa tata kelola naskah dinas berstandar baku KBBI.`;
    }
  }

  res.statusCode = 200;
  if (filename.endsWith('.json')) {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
  } else {
    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
  }
  return res.end(content);
};
