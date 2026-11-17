# WORKFLOW: Quality Control & Executive Audit

> **Workflow ID:** WF-05-QUALITY-CONTROL  
> **Lead Owner:** ARKA (Chief Executive & Strategy Officer)  
> **Classification:** Executive Gatekeeping Protocol

---

## 1. TUJUAN WORKFLOW
Menjalankan audit kualitas independen tingkat C-Suite terhadap seluruh deliverable yang telah melewati peer review, memastikan integritas data, ketiadaan halusinasi AI, konsistensi lintas dokumen, dan kepatuhan terhadap standar enterprise sebelum disahkan menjadi dokumen final.

---

## 2. PEMICU (TRIGGER)
- Seluruh tugas divisional telah menyelesaikan peer review (WF-04) dan siap untuk verifikasi akhir.

---

## 3. PARTISIPAN & PERAN
- **ARKA:** Auditor eksekutif utama, penentu keputusan akhir kelulusan (Sign-off Authority).
- **Direktur Terkait (NAYA / RAKA / SEKAR / DIMAS):** Bertanggung jawab memberikan klarifikasi atau revisi cepat jika ditemukan defek.

---

## 4. 5 PILAR GERBANG AUDIT MUTU (QUALITY GATES)

```
+--------------------------------------------------------------------------+
|                     ARKA QUALITY CONTROL CHECKLIST                       |
+--------------------------------------------------------------------------+
| [ ] 1. KELENGKAPAN (Completeness)                                        |
|     - Seluruh butir mandat awal pengguna terjawab tuntas.               |
|                                                                          |
| [ ] 2. INTEGRITAS DATA & ANTI-HALUSINASI (Fact & Citation Integrity)     |
|     - Tidak ada statistik karangan; sumber atau formula tercantum.       |
|                                                                          |
| [ ] 3. KONSISTENSI SILANG (Cross-Document Consistency)                   |
|     - Angka biaya RAKA == Angka CAPEX/OPEX SEKAR == Batas Anggaran DIMAS.|
|                                                                          |
| [ ] 4. STANDAR BAHASA EKSEKUTIF (Executive Tone & Readability)           |
|     - Bahasa baku korporat, terstruktur, rapi, tanpa jargon tak perlu.   |
|                                                                          |
| [ ] 5. KEPATUHAN & MANAJEMEN RISIKO (Governance & Risk Compliance)       |
|     - Semua risiko kritis memiliki mitigasi; human approval gate aktif.  |
+--------------------------------------------------------------------------+
```

---

## 5. LANGKAH-LANGKAH PELAKSANAAN

### Langkah 1: Intake & Audit Multi-Dokumen
ARKA membuka seluruh draf laporan di `reports/` dan memeriksa kelima pilar checklist di atas.

### Langkah 2: Cross-Reconciliation Check
ARKA membandingkan secara otomatis:
- Estimasi kebutuhan server RAKA vs. Baris biaya infrastruktur di model keuangan SEKAR.
- Target pasar SOM NAYA vs. Target proyeksi penjualan DIMAS.

### Langkah 3: Pengambilan Keputusan Mutu
- **KASUS A (REVISI DIPERLUKAN):** Jika ditemukan inkonsistensi atau ketiadaan dasar perhitungan, ARKA menandai status tugas sebagai `REVISION REQUIRED`, menuliskan arahan perbaikan spesifik di log, dan menginstruksikan agent terkait untuk memperbaiki dalam 1 siklus revisi.
- **KASUS B (DISETUJUI):** Jika kelima kriteria terpenuhi dengan sempurna, ARKA mengubah status tugas menjadi `COMPLETED` dan membubuhkan persetujuan eksekutif.

### Langkah 4: Pembaruan Status Terpusat
ARKA memperbarui status di `logs/activity_log.json` dan mempersiapkan data untuk proses kompilasi laporan akhir.

---

## 6. INPUT & OUTPUT ARTIFACTS
- **Input:** Kumpulan draf laporan divisional di `reports/`.
- **Output:** Catatan hasil audit mutu, stempel persetujuan eksekutif, dan status `COMPLETED` di log sistem.

---

## 7. VALIDASI & EXIT CRITERIA
- Tidak boleh ada toleransi terhadap data yang tidak konsisten antar-laporan.
- Status `COMPLETED` hanya boleh diberikan jika checklist lolos 100%.
