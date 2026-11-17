---
name: risk-management
description: Identify, quantify, and mitigate enterprise risks using 5x5 Probability-Impact matrices, failure mode analysis, and contingency planning. Use when conducting risk assessments or stress-testing corporate strategies.
---

# SKILL: Enterprise Risk Management & Stress-Testing

## 1. Nama Skill
**Enterprise Risk Management & Stress-Testing (Risk Quantification & Mitigation)**

## 2. Deskripsi
Skill manajemen risiko korporasi komprehensif untuk mengidentifikasi potensi bahaya operasional, finansial, hukum, reputasi, dan teknis, menilai tingkat keparahan melalui matriks probabilitas-dampak, serta merumuskan rencana kontingensi mitigasi proaktif.

## 3. Tujuan
- Memproteksi kelangsungan bisnis korporasi dari kegagalan operasional dan kerugian finansial mendadak.
- Menyediakan peta risiko kuantitatif yang jelas sebelum inisiatif strategis dieksekusi.
- Merumuskan rencana respon risiko: Avoid (Hindari), Mitigate (Kurangi), Transfer (Alihkan), atau Accept (Terima).

## 4. Ruang Lingkup
- Kategori risiko: Finansial, Teknologi/Siber, Regulasi/Kepatuhan, Operasional, Pasar/Kompetisi.
- Matriks Risiko 5x5 (Probability vs. Impact Scoring).
- Risk Severity Index (RSI) dan Risk Appetite korporasi.
- Disaster Recovery & Business Continuity Planning (BCP).
- Key Risk Indicators (KRI) dan sistem peringatan dini (early warning triggers).

## 5. Metodologi Kerja
- **ISO 31000 Risk Management Standard:** Risk Identification -> Risk Analysis -> Risk Evaluation -> Risk Treatment -> Monitoring & Review.
- **COSO Enterprise Risk Management Framework:** Tata kelola risiko terintegrasi dari level dewan direksi hingga operasional lini depan.
- **Failure Mode and Effects Analysis (FMEA):** Menghitung Risk Priority Number (RPN) berdasarkan Severity x Occurrence x Detection.

## 6. Langkah Pelaksanaan
1. **Brainstorming & Ekstraksi Risiko Multi-Divisi:** Mengumpulkan masukan dari NAYA (pasar), RAKA (sistem), DIMAS (operasi).
2. **Scoring Probabilitas & Dampak:** Memberikan nilai 1 (Sangat Rendah) hingga 5 (Kritis/Katastropik) untuk setiap risiko.
3. **Penyusunan Heatmap Risiko:** Memetakan posisi risiko pada matriks 5x5 kuadran (Hijau, Kuning, Merah).
4. **Formulasi Strategi Mitigasi:** Menentukan tindakan pencegahan konkret untuk semua risiko berkategori Tinggi/Ekstrem.
5. **Penetapan Risk Owner & KRI:** Menugaskan direktur penanggung jawab dan metrik pemicu eskalasi.
6. **Laporan Audit Risiko:** Menyerahkan dokumen evaluasi risiko kepada ARKA untuk tinjauan kelayakan final.

## 7. Standar Kualitas
- Setiap risiko yang masuk kategori Merah (Critical/High) wajib memiliki rencana mitigasi bertahap dan rencana darurat (fallback).
- Tidak boleh menggunakan deskripsi risiko yang ambigu (misalnya "sistem bisa error" — harus spesifik: "Potensi kegagalan API gateway pihak ketiga akibat lonjakan traffic melebihi kuota 10.000 req/min").
- Menentukan batas ambang kerugian finansial maksimum yang dapat ditoleransi perusahaan (Risk Tolerance).

## 8. Format Output
- **Enterprise Risk Register Table (ID, Kategori, Deskripsi, Prob, Dampak, Skor RSI, Owner)**
- **5x5 Risk Heatmap Visualization Table**
- **Detailed Mitigation & Contingency Protocols for High-Severity Items**
- **Early Warning Indicators (KRI Trigger Thresholds)**
- **Executive Risk Sign-off Statement**

## 9. Contoh Penggunaan
SEKAR menggunakan skill ini untuk mengevaluasi: *"Risiko ketergantungan pada vendor penyedia model LLM eksternal untuk core business SaaS dan mitigasi transisi ke open-weight self-hosted models."*

## 10. Batasan dan Hal yang Tidak Boleh Dilakukan
- DILARANG mengabaikan risiko regulasi dan privasi data konsumen.
- DILARANG menetapkan tindakan mitigasi tanpa menghitung estimasi biaya mitigasi tersebut.
- DILARANG menurunkan skor dampak risiko secara subyektif tanpa justifikasi teknis atau operasional yang sah.
