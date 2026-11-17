---
name: quality-assurance
description: Rigorous cross-divisional quality control, fact-checking, consistency verification, and acceptance gate enforcement. Use when evaluating agent deliverables, verifying factual claims, or approving reports.
---

# SKILL: Enterprise Quality Assurance & Acceptance Governance

## 1. Nama Skill
**Enterprise Quality Assurance & Acceptance Governance (Audit & Verification Gates)**

## 2. Deskripsi
Skill pengawasan mutu dan kontrol kualitas independen untuk memvalidasi setiap deliverable yang dihasilkan oleh AI agent, memastikan kepatuhan terhadap standar profesionalitas korporasi, memverifikasi ketiadaan halusinasi fakta/angka, dan menjalankan gerbang persetujuan (Acceptance Gates) sebelum diserahkan kepada dewan komisaris / pengguna.

## 3. Tujuan
- Mencegah masuknya data palsu, halusinasi model AI, atau klaim tidak berdasar ke dalam dokumen resmi perusahaan.
- Memastikan konsistensi silang (cross-consistency) antar data teknis, finansial, operasional, dan riset.
- Menjalankan mekanisme koreksi balik (Feedback & Revision Loop) apabila draf kerja belum memenuhi kriteria mutu.

## 4. Ruang Lingkup
- Audit integritas data (Fact-checking, verification of sources).
- Audit konsistensi matematis (verifikasi ulang perhitungan finansial, alokasi kapasitas server).
- Standar penulisan bahasa dan nada komunikasi eksekutif (Executive Tone Review).
- Gerbang Penerimaan Kualitas (Quality Gates: Gate 1 Discovery, Gate 2 Architecture & Feasibility, Gate 3 Pre-Flight Approval).
- Pengendalian status tugas (transisi `UNDER REVIEW` -> `REVISION REQUIRED` atau `COMPLETED`).

## 5. Metodologi Kerja
- **Three Lines of Defense Model:**
  - Lini 1: Self-Audit oleh masing-masing Direktur pelaksana.
  - Lini 2: Cross-Divisional Peer Review (e.g. SEKAR mereview budget RAKA).
  - Lini 3: Quality Control & Executive Sign-off independen oleh ARKA.
- **Red Team / Devil's Advocate Review:** Menguji kelemahan argumentasi bisnis secara sengaja untuk menemukan celah tersembunyi.
- **Hallucination Detection Protocol:** Mengisolasi setiap klaim numerik dan menelusuri rumus atau sumber asal datanya.

## 6. Langkah Pelaksanaan
1. **Penerimaan Deliverable Berstatus `UNDER REVIEW`:** Membuka draf deliverable dari folder `reports/` atau task registry.
2. **Eksekusi 5 Kriteria Audit Mutu:**
   - **Completeness:** Apakah semua poin mandat terpenuhi?
   - **Accuracy:** Apakah angka dan data terbukti valid tanpa halusinasi?
   - **Consistency:** Apakah angka selaras dengan divisi lain?
   - **Actionability:** Apakah rekomendasi konkret dan dapat dieksekusi?
   - **Compliance:** Apakah memenuhi batasan hukum dan keamanan?
3. **Keputusan Gerbang Mutu:**
   - Jika Lolos: Ubah status menjadi `COMPLETED` dan catat di log audit.
   - Jika Gagal: Ubah status menjadi `REVISION REQUIRED`, lampirkan catatan perbaikan spesifik, dan kembalikan ke agent terkait.
4. **Final Gate Clearance:** Memberikan stempel persetujuan eksekutif untuk kompilasi laporan akhir.

## 7. Standar Kualitas
- Setiap penolakan (Rejection) wajib disertai alasan tertulis yang spesifik dan petunjuk perbaikan yang jelas.
- Tidak ada dokumen yang dapat diserahkan ke pengguna tanpa melewati gerbang mutu ini.
- Hasil audit dicatat secara permanen di `logs/activity_log.json`.

## 8. Format Output
- **Quality Assurance Audit Checklist Table**
- **Defect & Inconsistency Log (jika ada temuan cacat)**
- **Cross-Divisional Reconciliation Verdict**
- **Quality Gate Decision: [APPROVED / REVISION REQUIRED / REJECTED]**
- **Audit Sign-off Signature Block**

## 9. Contoh Penggunaan
ARKA menggunakan skill ini ketika memeriksa draf laporan RAKA yang mengusulkan cluster Kubernetes 20 node, mencocokkannya dengan estimasi biaya di draf SEKAR untuk memastikan tidak ada selisih perhitungan biaya lisensi cloud.

## 10. Batasan dan Hal yang Tidak Boleh Dilakukan
- DILARANG meloloskan dokumen yang memiliki kontradiksi internal (misal di halaman 2 tertulis target 100 klien, di halaman 10 tertulis 500 klien).
- DILARANG menyetujui klaim pasar tanpa adanya sitasi sumber atau penjelasan metode estimasi.
- DILARANG mengabaikan feedback perbaikan dari peer reviewer.
