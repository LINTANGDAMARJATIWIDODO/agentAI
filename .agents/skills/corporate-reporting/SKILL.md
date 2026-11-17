---
name: corporate-reporting
description: Synthesize cross-divisional findings into boardroom-ready executive summaries, comprehensive feasibility studies, and final project reports. Use when producing executive-level consolidated documentation.
---

# SKILL: Executive Corporate Reporting & Boardroom Synthesis

## 1. Nama Skill
**Executive Corporate Reporting & Boardroom Synthesis (Consolidated Reporting Standard)**

## 2. Deskripsi
Skill sintesis tingkat C-Suite untuk menggabungkan laporan sektoral yang terpisah dari divisi riset (NAYA), teknologi (RAKA), keuangan/risiko (SEKAR), dan operasi/pertumbuhan (DIMAS) menjadi satu dokumen komprehensif berstandar direksi yang elegan, kohesif, dan actionable.

## 3. Tujuan
- Menyediakan pandangan holistik 360 derajat atas suatu inisiatif strategis bagi para pengambil keputusan utama (C-Suite dan Dewan Komisaris).
- Menghilangkan friksi komunikasi dan inkonsistensi data antar-divisi.
- Menyajikan ringkasan eksekutif (Executive Summary) yang dapat dipahami dalam waktu 3 menit namun didukung data lampiran yang sangat mendalam.

## 4. Ruang Lingkup
- Executive Summary & Board Briefing Papers.
- Comprehensive Feasibility Study (Studi Kelayakan Bisnis Komprehensif).
- Annual / Quarterly Strategic Review Reports.
- Investment Memorandums & Business Plans.
- Format pelaporan ganda: Laporan Naratif Markdown dan metadata terstruktur JSON (`reports/laporan.json`).

## 5. Metodologi Kerja
- **The Pyramid Principle (Barbara Minto):** Menyampaikan kesimpulan dan rekomendasi utama terlebih dahulu di bagian atas, diikuti oleh pilar-pilar argumen pendukung dan data pembuktian empiris.
- **Cross-Divisional Reconciliation:** Mencocokkan angka-angka antar laporan (misalnya anggaran infrastruktur RAKA harus 100% konsisten dengan angka di laporan keuangan SEKAR).
- **Executive Readability Standard:** Menggunakan heading hirarkis, callout box penting, tabel perbandingan ringkas, dan visualisasi diagram konseptual.

## 6. Langkah Pelaksanaan
1. **Konsolidasi Seluruh Laporan Divisi:** Mengumpulkan draf laporan yang telah berstatus `COMPLETED` dari NAYA, RAKA, SEKAR, dan DIMAS.
2. **Pemeriksaan Konsistensi Data & Fakta:** Memastikan tidak ada pertentangan angka atau premis antar-divisi.
3. **Penyusunan Executive Summary (Minto Pyramid):** Merangkum intisari proyek, rasional strategis, indikator keuangan kunci, dan rekomendasi utama dalam 1 halaman eksekutif.
4. **Strukturisasi Tubuh Laporan:** Menyusun bab-bab mendalam: Market Intelligence, Technical Blueprint, Financial Valuation, Risk Assessment, dan Operational Roadmap.
5. **Penyusunan Action Matrix & Next Steps:** Menetapkan keputusan dewan yang dibutuhkan (Board Decisions Required).
6. **Ekspor & Sinkronisasi:** Menyimpan dokumen Markdown di `reports/` dan mencatat metadata di `reports/laporan.json` serta log aktivitas.

## 7. Standar Kualitas
- Setiap laporan final wajib memiliki struktur formal: Judul, Dokumen Kontrol, Executive Summary, Metodologi, Temuan Kunci, Analisis Risiko, Rekomendasi Tindakan, dan Kesimpulan.
- Tidak boleh ada bagian yang berulang secara redundan tanpa memberikan nilai tambah informasi.
- Bahasa baku profesional tingkat tinggi (Bahasa Indonesia Korporat atau Business English).

## 8. Format Output
Dokumen Final Report mencakup:
1. **Document Control & Classification Header**
2. **Executive Summary (TL;DR for Board of Directors)**
3. **Strategic Context & Business Objectives**
4. **Market & Competitive Intelligence (NAYA)**
5. **Technical Architecture & Infrastructure Blueprint (RAKA)**
6. **Financial Projections, Valuation & Budget Feasibility (SEKAR)**
7. **Risk Assessment & Compliance Governance Matrix (SEKAR)**
8. **Operational Roadmap, Milestones & RACI (DIMAS)**
9. **Final Strategic Recommendation & Governance Approval Gate (ARKA)**

## 9. Contoh Penggunaan
ARKA menggunakan skill ini untuk menyusun: *"Laporan Studi Kelayakan Komprehensif (Comprehensive Feasibility Study) Pendirian Unit Bisnis NEXUS Cloud AI Enterprise 2026."*

## 10. Batasan dan Hal yang Tidak Boleh Dilakukan
- DILARANG mempublikasikan laporan final jika masih ada tugas divisi yang berstatus `FAILED` atau `REVISION REQUIRED` tanpa penjelasan alasan.
- DILARANG mengubah kesimpulan divisi tanpa persetujuan atau catatan sanggahan resmi.
- DILARANG menyembunyikan risiko kritis yang ditemukan oleh SEKAR dalam ringkasan eksekutif.
