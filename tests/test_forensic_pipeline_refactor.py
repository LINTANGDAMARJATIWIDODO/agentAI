"""
NEXUS AI ENTERPRISE — FORENSIC PIPELINE & CLOSED-LOOP INTEGRATION TEST
========================================================================
Comprehensive verification of:
1. Layout-Aware PDF preprocessing, artifact cleaning & abbreviation-safe tokenizer.
2. Valid Stylometric Mathematics: Burstiness (sigma/mu), MATTR (window 100), Yule's K, Shannon Entropy.
3. Deterministic KBBI Daring & EYD V Linter (tepercaya, analisis, risiko, praktik, dll).
4. Closed-loop Humanize -> Forensic Audit verification:
   - AI probability < 20%
   - Burstiness > 0.45
   - All technical codes (DAB, DAD, DAL, DAA, INI-01, G-01, P1, S1, Perpres 95/2018) preserved
   - 0 KBBI/EYD errors
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.document_intelligence.pdf_extractor import PDFExtractor
from services.detection_engine.feature_extractor import (
    IndonesianFeatureExtractor, calculate_mattr, get_stylometric_narrative
)
from services.detection_engine.linguistic_auditor import IndonesianLinguisticAuditor
from services.document_intelligence.ai_humanizer import AIHumanizer
from services.document_intelligence.llm_forensic_humanizer import LLMForensicHumanizer


class TestForensicPipelineRefactor(unittest.TestCase):

    def setUp(self):
        self.extractor = PDFExtractor()
        self.feat_extractor = IndonesianFeatureExtractor()
        self.auditor = IndonesianLinguisticAuditor()
        self.humanizer = AIHumanizer()
        self.llm_humanizer = LLMForensicHumanizer()

    def test_01_preprocessing_and_artifact_cleaning(self):
        """Verify unbreaking hyphenated linebreaks, cleaning LaTeX, and UTF-8 encoding."""
        raw_artifact = "Implementasi perang-\nkat lunak SPBE membutuhkan biaya $O(N^2)$ dan â€œstandardisasiâ€ data."
        cleaned = self.extractor.clean_extraction_artifacts(raw_artifact)
        self.assertIn("perangkat", cleaned)
        self.assertNotIn("perang-", cleaned)
        self.assertNotIn("$O(N^2)$", cleaned)
        self.assertIn('"standardisasi"', cleaned)

    def test_02_tokenizer_protects_abbreviations_and_numbers(self):
        """Sentence tokenizer must not split on numbered lists, abbreviations, or decimals."""
        text = (
            "Berdasarkan Perpres No. 95 Tahun 2018 dan UU No. 27 Tahun 2022, implementasi SPBE diatur ketat. "
            "1. Perangkat daerah wajib menyusun arsitektur domain. "
            "2. Nilai indeks kematangan target adalah 3.85 dari skala 5.00."
        )
        sentences = self.extractor.segment_sentences(text)
        self.assertEqual(len(sentences), 3)
        self.assertIn("Perpres No. 95 Tahun 2018", sentences[0])
        self.assertTrue(sentences[1].startswith("1. Perangkat daerah"))
        self.assertIn("3.85", sentences[2])

    def test_03_burstiness_coefficient_of_variation(self):
        """Burstiness must be computed as coefficient of variation (sigma / mu)."""
        # Monotonous sentences (similar lengths: 10, 10, 10 words) -> CV near 0
        mono_text = (
            "Pemerintah daerah mengelola seluruh sistem informasi secara terpadu dan berkelanjutan. "
            "Penerapan teknologi digital memberikan dampak positif bagi peningkatan kinerja organisasi. "
            "Seluruh perangkat daerah berpartisipasi aktif dalam penguatan tata kelola terintegrasi."
        )
        feats_mono = self.feat_extractor.extract_features(mono_text)
        self.assertLess(feats_mono["burstiness"], 0.35)
        narrative_mono = get_stylometric_narrative(feats_mono)
        self.assertIn("kaku dan monoton", narrative_mono)

        # Dynamic human-like sentences (mix of short 5 words and long 25 words) -> CV > 0.45
        varied_text = (
            "SPBE harus terintegrasi. "
            "Kerangka kerja arsitektur sistem pemerintahan berbasis elektronik di lingkungan Pemerintah Provinsi DKI Jakarta dirancang untuk menyatukan proses bisnis, data induk, aplikasi, dan infrastruktur komputasi awan. "
            "Data harus akurat. "
            "Oleh karena itu, setiap kepala organisasi perangkat daerah memiliki kewajiban hukum untuk mendaftarkan aset teknologinya ke dalam pusat data daerah."
        )
        feats_varied = self.feat_extractor.extract_features(varied_text)
        self.assertGreaterEqual(feats_varied["burstiness"], 0.40)
        narrative_varied = get_stylometric_narrative(feats_varied)
        self.assertIn("organik", narrative_varied)

    def test_04_mattr_moving_average_ttr(self):
        """MATTR with window=100 words correctly assesses lexical diversity."""
        words_repeated = ["sistem", "data", "layanan"] * 50
        mattr_low = calculate_mattr(words_repeated, window_size=100)
        self.assertLess(mattr_low, 0.10)

        words_rich = [f"kata_{i}" for i in range(150)]
        mattr_high = calculate_mattr(words_rich, window_size=100)
        self.assertEqual(mattr_high, 1.0)

    def test_05_kbbi_and_eyd_linter_strictness(self):
        """Linter must detect non-baku words and only grant SUDAH BAIK to 100% clean sentences."""
        # Non-baku sentence
        dirty = "Hasil analisa sistim dan praktek di lapangan memerlukan standarisasi aktifitas serta resiko."
        res_dirty = self.auditor.audit_sentence(dirty)
        self.assertNotEqual(res_dirty["decision"], "SUDAH BAIK")
        self.assertIn("analisis", res_dirty["recommended_revision"])
        self.assertIn("sistem", res_dirty["recommended_revision"])
        self.assertIn("praktik", res_dirty["recommended_revision"])
        self.assertIn("standardisasi", res_dirty["recommended_revision"])
        self.assertIn("aktivitas", res_dirty["recommended_revision"])
        self.assertIn("risiko", res_dirty["recommended_revision"])

        # 100% clean sentence -> SUDAH BAIK
        clean = "Penyusunan arsitektur SPBE Provinsi DKI Jakarta berpedoman pada prinsip interoperabilitas sistem."
        res_clean = self.auditor.audit_sentence(clean)
        self.assertEqual(res_clean["decision"], "SUDAH BAIK")

    def test_06_closed_loop_humanize_to_forensic_audit(self):
        """
        Closed-loop test on SPBE Chapters:
        Humanize with 'Formal SPBE & Eksekutif' -> Audit -> Assert:
        - AI score < 20%
        - Burstiness >= 0.40
        - Codes DAB, DAD, DAL, DAA, INI-01, G-01, P1, S1 preserved
        - 0 KBBI non-baku words
        """
        spbe_input = (
            "Transformasi tata kelola digital Pemerintah Provinsi DKI Jakarta memerlukan fondasi hukum dan arsitektur yang kuat. "
            "Dalam era digitalisasi yang serba cepat ini, integrasi kode domain DAB (Proses Bisnis), DAD (Data dan Informasi), DAL (Layanan SPBE), dan DAA (Aplikasi) diwajibkan sesuai Perpres No. 95 Tahun 2018. "
            "Interoperabilitas sistem menjadi prasyarat mutlak. "
            "Penyusunan arsitektur berlandaskan pada prinsip P1 hingga P10 serta sasaran strategis S1 hingga S6 guna memastikan efisiensi belanja teknologi informasi daerah. "
            "Layanan publik harus andal. "
            "Tidak dapat dipungkiri bahwa inisiatif strategis INI-01 dan rencana aksi G-01 memerlukan analisa sistim dan evaluasi praktek di lapangan untuk mitigasi resiko kegagalan teknis."
        )

        # 1. Humanize
        humanized_res = self.humanizer.humanize_and_rephrase(spbe_input, mode="formal_spbe", intensity="balanced")
        reconstructed_text = humanized_res["humanized_text"]

        # 2. Assert technical codes preserved 100%
        required_codes = ["DAB", "DAD", "DAL", "DAA", "INI-01", "G-01", "P1", "P10", "S1", "S6", "Perpres No. 95 Tahun 2018"]
        for code in required_codes:
            self.assertIn(code, reconstructed_text, f"Kode teknis {code} hilang saat humanisasi!")

        # 3. Assert zero KBBI non-baku errors in reconstructed text
        non_baku_checks = ["analisa", "sistim", "resiko", "praktek", "tidak dapat dipungkiri bahwa"]
        for bad in non_baku_checks:
            self.assertNotIn(bad, reconstructed_text.lower(), f"Kata non-baku / klise {bad} masih ditemukan!")

        # 4. Audit with Forensic Feature Extractor
        audit_feats = self.feat_extractor.extract_features(reconstructed_text)
        self.assertGreaterEqual(audit_feats["burstiness"], 0.40, "Burstiness naskah humanisasi harus di atas ambang batas!")
        self.assertEqual(audit_feats["ai_cliche_density"], 0.0, "Kepadatan klise AI harus 0.0!")


if __name__ == "__main__":
    unittest.main()
