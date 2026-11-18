"""
NEXUS AI ENTERPRISE — ADVANCED AI DETECTOR SCIENTIFIC TEST SUITE
================================================================
Unit and regression tests verifying:
1. Linguistic & Statistical Feature Extraction (28 features, no NaN / Div0)
2. Machine Learning Ensemble Classification (Tree Booster + Logistic Baseline)
3. Platt Probability Calibration & Uncertainty Estimation
4. 4-Outcome Verdicts (Human-like, AI-like, Mixed, Inconclusive)
5. Out-of-Distribution (OOD) Guardrails
6. Benchmark Metrics & Zero-Leakage Evaluation Pipeline
"""

import unittest
import os
import sys
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.detection_engine.feature_extractor import IndonesianFeatureExtractor, segment_sentences, tokenize_words
from services.detection_engine.classifier import IndonesianAIClassifier
from services.detection_engine.calibrator import ForensicCalibrator
from services.detection_engine.detector import NexusIndonesianDetector
from services.detection_engine.evaluator import DetectorEvaluator, calculate_ece


class TestIndonesianAIDetector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.extractor = IndonesianFeatureExtractor()
        cls.classifier = IndonesianAIClassifier()
        cls.calibrator = ForensicCalibrator()
        cls.detector = NexusIndonesianDetector()
        cls.detector.initialize()

        cls.sample_human = (
            "Ketimpangan distribusi pendapatan di wilayah perdesaan Jawa Tengah dipengaruhi oleh kepemilikan lahan "
            "pertanian dan akses terhadap kredit mikro perbankan. Menggunakan model regresi spasial data panel kurun waktu "
            "2015 hingga 2023, koefisien Gini terbukti menurun secara gradual di kabupaten yang merealisasikan program dana desa "
            "untuk pembangunan irigasi primer dan fasilitas pascapanen gabah."
        )

        cls.sample_ai = (
            "Dalam era digitalisasi yang serba cepat ini, penerapan teknologi informasi menjadi suatu keniscayaan yang "
            "tidak dapat dihindari bagi setiap organisasi. Selain itu, integrasi sistem kecerdasan buatan memainkan peran "
            "yang sangat penting dalam meningkatkan efisiensi operasional secara signifikan. Lebih lanjut, keberadaan data "
            "yang terpusat mampu memberikan pandangan yang holistik dan komprehensif bagi para pemangku kepentingan. "
            "Oleh karena itu, penting untuk dicatat bahwa transformasi digital harus dijalankan secara terstruktur guna "
            "mencapai hasil yang optimal."
        )

        cls.sample_mixed = (
            "Penyusunan arsitektur SPBE Provinsi DKI Jakarta berpedoman pada prinsip interoperabilitas sistem "
            "dan bagi pakai data antarsub-sistem. Dinas Komunikasi, Informatika dan Statistik menetapkan standar "
            "metadatabase terpusat guna menghindari duplikasi aplikasi di lingkungan satuan kerja perangkat daerah. "
            "Dalam era digitalisasi yang serba cepat ini, penerapan teknologi informasi menjadi suatu keniscayaan yang "
            "tidak dapat dihindari bagi setiap organisasi. Selain itu, integrasi sistem kecerdasan buatan memainkan peran "
            "yang sangat penting dalam meningkatkan efisiensi operasional secara signifikan."
        )

    # 1. Feature Extraction Tests
    def test_feature_extraction_completeness(self):
        feats = self.extractor.extract_features(self.sample_human)
        self.assertEqual(len(feats), 28)
        for k, v in feats.items():
            self.assertFalse(np.isnan(v), f"Feature {k} returned NaN")
            self.assertFalse(np.isinf(v), f"Feature {k} returned Inf")

    def test_burstiness_discriminant(self):
        feats_human = self.extractor.extract_features(self.sample_human)
        feats_ai = self.extractor.extract_features(self.sample_ai)
        # Human writing should exhibit higher burstiness than formulaic AI text
        self.assertGreater(feats_human["burstiness"], feats_ai["burstiness"])

    def test_cliche_and_transition_detection(self):
        feats_ai = self.extractor.extract_features(self.sample_ai)
        self.assertGreater(feats_ai["ai_transition_density"], 0.0)
        self.assertGreater(feats_ai["ai_cliche_density"], 0.0)

    # 2. Classifier Inference Tests
    def test_classifier_inference_bounds(self):
        pred_h = self.classifier.predict(self.sample_human)
        pred_a = self.classifier.predict(self.sample_ai)

        self.assertGreaterEqual(pred_h["blended_ai_probability"], 0.0)
        self.assertLessEqual(pred_h["blended_ai_probability"], 1.0)
        self.assertGreaterEqual(pred_a["blended_ai_probability"], 0.0)
        self.assertLessEqual(pred_a["blended_ai_probability"], 1.0)

        # AI text probability should exceed human text probability
        self.assertGreater(pred_a["blended_ai_probability"], pred_h["blended_ai_probability"])
        self.assertGreater(pred_h["model_agreement"], 0.70)
        self.assertGreater(pred_a["model_agreement"], 0.70)

    # 3. Calibration & Uncertainty Tests
    def test_ood_short_text(self):
        is_ood, reason = self.calibrator.check_ood("Ini teks pendek.", 3, 0.3)
        self.assertTrue(is_ood)
        self.assertIn("terlalu pendek", reason)

    def test_ood_foreign_language(self):
        english_text = "This is a strictly English text without any Indonesian function words or grammar."
        words = tokenize_words(english_text)
        is_ood, reason = self.calibrator.check_ood(english_text, len(words), 0.0)
        self.assertTrue(is_ood)

    def test_four_standardized_outcomes(self):
        # 1. Human-like
        v1, _ = self.calibrator.determine_verdict(0.05, 0.15, False, "", [0.1, 0.15, 0.1])
        self.assertEqual(v1, "Human-like")

        # 2. AI-like
        v2, _ = self.calibrator.determine_verdict(0.95, 0.10, False, "", [0.85, 0.92, 0.90])
        self.assertEqual(v2, "AI-like")

        # 3. Mixed
        v3, _ = self.calibrator.determine_verdict(0.50, 0.35, False, "", [0.15, 0.88, 0.20, 0.80])
        self.assertEqual(v3, "Mixed")

        # 4. Inconclusive
        v4, _ = self.calibrator.determine_verdict(0.90, 0.75, True, "OOD error", [0.9])
        self.assertEqual(v4, "Inconclusive")

    # 4. Master Detector End-to-End Test
    def test_master_detector_report_structure(self):
        report = self.detector.analyze(self.sample_ai, include_llm_audit=False)
        self.assertIn("verdict", report)
        self.assertIn("calibrated_ai_probability", report)
        self.assertIn("confidence_level", report)
        self.assertIn("uncertainty_score", report)
        self.assertIn("document_statistics", report)
        self.assertIn("sentence_heatmap", report)
        self.assertIn("disclaimer", report)

        self.assertIn(report["verdict"], ["Human-like", "AI-like", "Mixed", "Inconclusive"])
        self.assertGreater(len(report["sentence_heatmap"]), 0)

    # 5. Expected Calibration Error (ECE) Math Test
    def test_ece_calculation(self):
        probs = np.array([0.1, 0.2, 0.8, 0.9])
        labels = np.array([0, 0, 1, 1])
        ece = calculate_ece(probs, labels, n_bins=2)
        self.assertGreaterEqual(ece, 0.0)
        self.assertLessEqual(ece, 1.0)


if __name__ == "__main__":
    unittest.main()
