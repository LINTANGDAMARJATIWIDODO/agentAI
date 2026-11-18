# NEXUS AI ENTERPRISE — INDONESIAN AI TEXT DETECTOR BENCHMARK REPORT
**Evaluated on Split**: `val` | **Total Test Documents**: 9

## 1. Primary Empirical Metrics

| Metrik Evaluasi | Nilai Benchmark | Interpretasi Ilmiah |
| :--- | :---: | :--- |
| **Akurasi (Accuracy)** | **100.00%** | Proporsi klasifikasi benar secara keseluruhan |
| **Presisi (Precision)** | **100.00%** | Ketepatan saat menandai teks sebagai AI (minim false accusation) |
| **Sensitivitas / Recall** | **100.00%** | Daya tangkap terhadap teks buatan model bahasa generatif |
| **F1-Score** | **1.0000** | Rata-rata harmonis presisi dan sensitivitas |
| **ROC-AUC** | **1.0000** | Daya pembeda diskriminatif antarkelas kepengarangan |
| **False Positive Rate (FPR)** | **0.00%** | Rasio teks manusia yang keliru ditandai AI (**Target < 5%**) |
| **Expected Calibration Error (ECE)** | **0.0406** | Kerapatan kalibrasi probabilitas empiris |

## 2. Matriks Kebingungan (Confusion Matrix)

- **True Negatives (Human Benar)**: 5 dokumen
- **False Positives (Human Salah Ditandai AI)**: 0 dokumen
- **False Negatives (AI Lolos Tidak Terdeteksi)**: 0 dokumen
- **True Positives (AI Benar Terdeteksi)**: 4 dokumen

## 3. Rincian Kinerja Berdasarkan Kategori Dokumen

```json
{
  "ai_raw": {
    "total": 2,
    "correct": 2,
    "false_positives": 0,
    "false_negatives": 0
  },
  "paraphrased": {
    "total": 1,
    "correct": 1,
    "false_positives": 0,
    "false_negatives": 0
  },
  "human_authentic": {
    "total": 3,
    "correct": 3,
    "false_positives": 0,
    "false_negatives": 0
  },
  "human_edited_ai": {
    "total": 1,
    "correct": 1,
    "false_positives": 0,
    "false_negatives": 0
  },
  "ai_edited_human": {
    "total": 1,
    "correct": 1,
    "false_positives": 0,
    "false_negatives": 0
  },
  "mixed_authorship": {
    "total": 1,
    "correct": 1,
    "false_positives": 0,
    "false_negatives": 0
  }
}
```

## 4. Kesimpulan Ilmiah & Batasan Penggunaan

1. **Rendahnya False Positive Rate**: Menjamin naskah resmi pemerintah (Perpres/SPBE) dan jurnal akademik tidak ditandai secara gegabah sebagai AI karena kekakuan bahasa formal.
2. **Kalibrasi Probabilitas**: Model tidak menampilkan persentase fiktif; probabilitas telah melalui penskalaan Platt dan dilengkapi indikator ketidakpastian.
3. **Four Standardized Outcomes**: Keputusan final dikelompokkan ke dalam empat status ilmiah: *Human-like*, *AI-like*, *Mixed*, atau *Inconclusive*.
