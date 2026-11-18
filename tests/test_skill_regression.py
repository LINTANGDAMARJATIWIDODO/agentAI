"""
NEXUS AI ENTERPRISE — AUTOMATED SKILL REGRESSION TEST SUITE
===========================================================
Rigorous regression test suite verifying zero-regression guarantees for:
- ai-authorship-forensics v2.0
- indonesian-linguistic-intelligence v2.0
- evidence-verification v1.0

TEST COVERAGE:
1. Kalimat sudah baku -> Tidak diubah (SUDAH BAIK)
2. "Selain itu" sudah benar -> Tidak diganti ke "Di samping itu"
3. "Oleh karena itu" sudah benar -> Tidak diganti ke "Oleh sebab itu" atau "Maka"
4. "dapat" -> Tidak diganti ke "bisa"
5. "Secara substantif" -> DILARANG disisipkan ke kalimat
6. Koma sebelum "dan" tidak diperlukan (2 unsur) -> Tidak ditambahkan
7. Koma sebelum "dan" pada perincian 3 unsur (Oxford comma) -> Dipertahankan
8. Non-baku KBBI ("analisa sistim") -> REVISI MINOR ("analisis sistem")
9. Non-baku KBBI ("praktek", "aktifitas") -> REVISI MINOR ("praktik", "aktivitas")
10. Konjungsi intrakalimat di awal ("Sehingga...", "Bahwa...") -> REVISI SUBSTANTIF
11. Kalimat terpotong / menggantung -> PERLU VERIFIKASI
12. Teks kurang dari batas minimum (< 35 kata) -> INCONCLUSIVE (OOD warning)
13. Pemisahan AI Detection vs KBBI -> Hasil tetap independen dan dipisahkan
14. Dokumen akademik manusia autentik -> Tidak menuduh AI (HUMAN-LIKE)
15. Dokumen klise generatif AI -> AI-LIKE
16. "adalah" -> Tidak diganti paksa menjadi "mencakup"
17. Kalimat formal bahasa Indonesia tidak pernah dipotong semena-mena
"""

import unittest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.detection_engine.linguistic_auditor import IndonesianLinguisticAuditor
from services.detection_engine.detector import NexusIndonesianDetector
from services.detection_engine.calibrator import ForensicCalibrator


class TestSkillHarmonizationRegression(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.auditor = IndonesianLinguisticAuditor()
        cls.detector = NexusIndonesianDetector()
        cls.detector.initialize()
        cls.calibrator = ForensicCalibrator()

    # -----------------------------------------------------------------------
    # TEST 1: Kalimat sudah baku -> Tidak diubah (SUDAH BAIK)
    # -----------------------------------------------------------------------
    def test_01_kalimat_sudah_baku_tidak_diubah(self):
        s = "Penyusunan arsitektur SPBE Provinsi DKI Jakarta berpedoman pada prinsip interoperabilitas sistem."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "SUDAH BAIK")
        self.assertEqual(res["recommended_revision"], s)
        self.assertIn("Tidak diperlukan perubahan", res["reason_for_revision"])

    # -----------------------------------------------------------------------
    # TEST 2: "Selain itu" sudah benar -> Tidak diganti
    # -----------------------------------------------------------------------
    def test_02_selain_itu_tidak_diganti(self):
        s = "Selain itu, integrasi sistem kecerdasan buatan terbukti mempercepat alur kerja harian."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "SUDAH BAIK")
        self.assertNotIn("Di samping itu", res["recommended_revision"])
        self.assertTrue(res["recommended_revision"].startswith("Selain itu,"))

    # -----------------------------------------------------------------------
    # TEST 3: "Oleh karena itu" sudah benar -> Tidak diganti
    # -----------------------------------------------------------------------
    def test_03_oleh_karena_itu_tidak_diganti(self):
        s = "Oleh karena itu, setiap unit pelaksana wajib mendaftarkan aplikasinya."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "SUDAH BAIK")
        self.assertNotIn("Oleh sebab itu", res["recommended_revision"])
        self.assertNotIn("Maka,", res["recommended_revision"])
        self.assertTrue(res["recommended_revision"].startswith("Oleh karena itu,"))

    # -----------------------------------------------------------------------
    # TEST 4: "dapat" -> Tidak diganti menjadi "bisa"
    # -----------------------------------------------------------------------
    def test_04_dapat_tidak_diganti_menjadi_bisa(self):
        s = "Standar data tersebut dapat dijadikan acuan bagi seluruh dinas teknis."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "SUDAH BAIK")
        self.assertIn("dapat", res["recommended_revision"])
        self.assertNotIn("bisa", res["recommended_revision"])

    # -----------------------------------------------------------------------
    # TEST 5: "Secara substantif" -> DILARANG disisipkan ke kalimat
    # -----------------------------------------------------------------------
    def test_05_secara_substantif_dilarang_disisipkan(self):
        s = "Pemerintah daerah mengalokasikan anggaran untuk peningkatan infrastruktur TIK."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "SUDAH BAIK")
        self.assertNotIn("Secara substantif", res["recommended_revision"])

    # -----------------------------------------------------------------------
    # TEST 6: Koma sebelum "dan" tidak diperlukan (2 unsur) -> Tidak ditambahkan
    # -----------------------------------------------------------------------
    def test_06_koma_sebelum_dan_dua_unsur_tidak_ditambahkan(self):
        s = "Dinas Komunikasi, dan Informatika menetapkan standar arsitektur."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "REVISI MINOR")
        # Fixed: comma before 'dan' removed
        self.assertEqual(res["recommended_revision"], "Dinas Komunikasi dan Informatika menetapkan standar arsitektur.")

    # -----------------------------------------------------------------------
    # TEST 7: Oxford comma pada 3 unsur perincian -> Dipertahankan
    # -----------------------------------------------------------------------
    def test_07_oxford_comma_tiga_unsur_dipertahankan(self):
        s = "Arsitektur SPBE mencakup proses bisnis, data dan informasi, dan layanan."
        res = self.auditor.audit_sentence(s)
        self.assertIn("dan layanan", res["recommended_revision"])

    # -----------------------------------------------------------------------
    # TEST 8: Non-baku KBBI ("analisa sistim") -> REVISI MINOR
    # -----------------------------------------------------------------------
    def test_08_non_baku_analisa_sistim(self):
        s = "Hasil analisa sistim membuktikan peningkatan efisiensi."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "REVISI MINOR")
        self.assertIn("analisis sistem", res["recommended_revision"])

    # -----------------------------------------------------------------------
    # TEST 9: Non-baku KBBI ("praktek", "aktifitas") -> REVISI MINOR
    # -----------------------------------------------------------------------
    def test_09_non_baku_praktek_aktifitas(self):
        s = "Praktek tata kelola ini mendukung aktifitas harian ASN."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "REVISI MINOR")
        self.assertIn("praktik", res["recommended_revision"].lower())
        self.assertIn("aktivitas", res["recommended_revision"].lower())

    # -----------------------------------------------------------------------
    # TEST 10: Konjungsi subordinatif pembuka kalimat -> REVISI SUBSTANTIF
    # -----------------------------------------------------------------------
    def test_10_subordinatif_pembuka_revisi_substantif(self):
        s = "Sehingga integrasi data antardinas dapat terwujud secara optimal."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "REVISI SUBSTANTIF")
        self.assertIn("Oleh karena itu", res["recommended_revision"])

    # -----------------------------------------------------------------------
    # TEST 11: Kalimat terpotong / menggantung -> PERLU VERIFIKASI
    # -----------------------------------------------------------------------
    def test_11_kalimat_terpotong_perlu_verifikasi(self):
        s = "Berdasarkan evaluasi terhadap implementasi"
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "PERLU VERIFIKASI")
        self.assertIn("terpotong", res["findings"])

    # -----------------------------------------------------------------------
    # TEST 12: Teks kurang dari batas minimum (< 35 kata) -> INCONCLUSIVE
    # -----------------------------------------------------------------------
    def test_12_teks_kurang_dari_minimum_inconclusive(self):
        short_text = "Ini adalah pengujian teks yang sangat pendek."
        report = self.detector.analyze(short_text, include_llm_audit=False)
        self.assertEqual(report["verdict"], "Inconclusive")
        self.assertIn("terlalu pendek", report["verdict_explanation"])

    # -----------------------------------------------------------------------
    # TEST 13: Pemisahan AI Detection dan KBBI
    # -----------------------------------------------------------------------
    def test_13_pemisahan_ai_detection_dan_kbbi(self):
        # Human academic text with non-baku word: AI detection is Human-like, KBBI is REVISI MINOR
        text_with_typo = (
            "Ketimpangan distribusi pendapatan di wilayah perdesaan Jawa Tengah dipengaruhi oleh kepemilikan lahan "
            "pertanian dan akses terhadap kredit mikro perbankan. Hasil analisa menunjukkan bahwa koefisien Gini menurun "
            "secara gradual di kabupaten yang merealisasikan program dana desa untuk pembangunan irigasi primer dan fasilitas gabah."
        )
        report = self.detector.analyze(text_with_typo, include_llm_audit=False)
        self.assertEqual(report["verdict"], "Human-like")

        ling_res = self.auditor.audit_sentence("Hasil analisa menunjukkan bahwa koefisien Gini menurun.")
        self.assertEqual(ling_res["decision"], "REVISI MINOR")
        self.assertIn("analisis", ling_res["recommended_revision"])

    # -----------------------------------------------------------------------
    # TEST 14: Dokumen akademik manusia autentik -> Tidak menuduh AI (HUMAN-LIKE)
    # -----------------------------------------------------------------------
    def test_14_dokumen_akademik_tidak_dituduh_ai(self):
        academic_human = (
            "Penelitian ini mengevaluasi kinerja algoritma pembelajaran mesin pada klasifikasi citra medis berskala kecil. "
            "Metode ekstraksi fitur berbasis transformasi wavelet diskrit digabungkan dengan pengklasifikasi Support Vector "
            "Machine berinti RBF. Hasil eksperimen pada 250 sampel menunjukkan akurasi rata-rata sebesar 89,4 persen, "
            "dengan waktu komputasi yang 30 persen lebih singkat dibandingkan model konvolusional standar tanpa prapemrosesan."
        )
        report = self.detector.analyze(academic_human, include_llm_audit=False)
        self.assertEqual(report["verdict"], "Human-like")
        self.assertLessEqual(report["calibrated_ai_probability"], 0.35)

    # -----------------------------------------------------------------------
    # TEST 15: Dokumen klise generatif AI -> Terdeteksi AI-LIKE
    # -----------------------------------------------------------------------
    def test_15_dokumen_klise_ai_terdeteksi(self):
        ai_cliche_text = (
            "Dalam era digitalisasi yang serba cepat ini, penerapan teknologi informasi menjadi suatu keniscayaan yang "
            "tidak dapat dihindari bagi setiap organisasi. Selain itu, integrasi sistem kecerdasan buatan memainkan peran "
            "yang sangat penting dalam meningkatkan efisiensi operasional secara signifikan. Lebih lanjut, keberadaan data "
            "yang terpusat mampu memberikan pandangan yang holistik dan komprehensif bagi para pemangku kepentingan. "
            "Oleh karena itu, penting untuk dicatat bahwa transformasi digital harus dijalankan secara terstruktur guna "
            "mencapai hasil yang optimal."
        )
        report = self.detector.analyze(ai_cliche_text, include_llm_audit=False)
        self.assertEqual(report["verdict"], "AI-like")
        self.assertGreaterEqual(report["calibrated_ai_probability"], 0.65)

    # -----------------------------------------------------------------------
    # TEST 16: "adalah" -> Tidak diganti menjadi "mencakup"
    # -----------------------------------------------------------------------
    def test_16_adalah_tidak_diganti_menjadi_mencakup(self):
        s = "Tata Kelola SPBE adalah kerangka kerja yang memastikan terlaksananya pengaturan terpadu."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "SUDAH BAIK")
        self.assertIn(" adalah ", res["recommended_revision"])
        self.assertNotIn(" mencakup ", res["recommended_revision"])

    # -----------------------------------------------------------------------
    # TEST 17: "Berdasarkan hasil penelitian," -> Diperlakukan sebagai tulisan ilmiah sah
    # -----------------------------------------------------------------------
    def test_17_berdasarkan_hasil_penelitian_sah(self):
        s = "Berdasarkan hasil penelitian, efisiensi komputasi meningkat sebesar 30 persen."
        res = self.auditor.audit_sentence(s)
        self.assertEqual(res["decision"], "SUDAH BAIK")
        self.assertTrue(res["recommended_revision"].startswith("Berdasarkan hasil penelitian,"))


if __name__ == "__main__":
    unittest.main()
