# STANDAR FORMAT RESMI LAPORAN SPBE DISKOMINFOTIK PEMPROV DKI JAKARTA
## Panduan Format 3 Kategori: Data Belum Ada, Data Gagal Upload, dan Data yang Sudah Terisi

> **Referensi Baku:** [Google Spreadsheet Diskominfotik (gid=1729927466)](https://docs.google.com/spreadsheets/d/170-6VSb8WHMEbCOpiyNCmAUQKkueL93CM0tXOKlb6o8/edit?gid=1729927466#gid=1729927466)  
> **Otoritas:** NEXUS AI ENTERPRISE — Seluruh Direktur AI  
> **Master Spreadsheet:** [`output/spreadsheets/LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx)  
> **Spreadsheet Khusus Belum Ada:** [`output/spreadsheets/REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx)  
> **Spreadsheet Khusus Gagal Upload:** [`output/spreadsheets/REKAP_DATA_GAGAL_UPLOAD_FORMAT_RESMI.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/REKAP_DATA_GAGAL_UPLOAD_FORMAT_RESMI.xlsx)  
> **Spreadsheet Khusus Terisi:** [`output/spreadsheets/REKAP_DATA_SUDAH_TERISI_FORMAT_RESMI.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/REKAP_DATA_SUDAH_TERISI_FORMAT_RESMI.xlsx)

---

### 1. FORMAT KATEGORI 1: DATA YANG BELUM ADA (3 KOLOM)
Sesuai persis dengan lembar kerja `Sheet5` (gid: 1729927466):
- **Baris 2:** Judul Perangkat Daerah (Arial 11pt Bold Hitam)
- **Baris 4 (Header Tabel):** `NO`, `PERANGKAT DAERAH`, `DOMAIN` (Warna Latar: `#9BC2E6` Biru Pastel)
- **Baris 5 s/d 16:** 12 Domain SPBE yang kosong:
  1. `ProsesBisnis_Sesuai`
  2. `ProsesBisnis_Upgrade`
  3. `ProsesBisnis_Sunset`
  4. `Layanan_Sesuai`
  5. `Layanan_Upgrade`
  6. `Layanan_Sunset`
  7. `Aplikasi_Sesuai`
  8. `Aplikasi_Upgrade`
  9. `Aplikasi_Sunset`
  10. `DataInformasi_Sesuai`
  11. `DataInformasi_Upgrade`
  12. `DataInformasi_Sunset`

---

### 2. FORMAT KATEGORI 2: DATA GAGAL UPLOAD (5 KOLOM)
Sesuai persis dengan lembar kerja `Data gagal Upload bappeda`:
- **Baris 2:** Judul `Data gagal Upload [Nama Perangkat Daerah]`
- **Baris 4 (Header Tabel):** `NO`, `PERANGKAT DAERAH`, `DOMAIN`, `ID - Nama Data`, `Nama Kolom yang belum terisi` (Warna Latar: `#9BC2E6`)
- **Baris 5 dst:** Rincian data gagal simpan, ID perangkat/layanan, dan rincian lengkap atribut mandatory yang kosong.

---

### 3. FORMAT KATEGORI 3: DATA YANG SUDAH TERISI (5 KOLOM & MATRIX)
- **Baris 2:** Judul `Data yang sudah terisi [Nama Perangkat Daerah]`
- **Baris 4 (Header Tabel):** `NO`, `PERANGKAT DAERAH`, `DOMAIN`, `ID - Nama Data Terisi`, `Status & Kanal Akses Terintegrasi` (Warna Latar: `#9BC2E6`)
- Memuat rincian entitas arsitektur yang sudah valid, lengkap dengan kode referensi nasional KemenPANRB dan kanal integrasi JAKI/OSS/Alpukat.
