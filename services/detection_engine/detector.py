"""
NEXUS AI ENTERPRISE — MASTER AI DETECTION & AUTHORSHIP ANALYSIS ENGINE
======================================================================
Unified orchestrator for Indonesian AI-generated text detection.
Integrates:
- 28-feature linguistic & statistical extraction
- Machine learning gradient boosting + logistic ensemble
- Probability calibration & uncertainty estimation (Platt scaling)
- Segment-level heatmap sentence scoring
- Gemini LLM contextual forensic auditor
- Transparent evidence attribution & scientific limitations disclaimer
"""

import os
import sys
import json
import time
from typing import Dict, List, Any, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.detection_engine.feature_extractor import IndonesianFeatureExtractor, segment_sentences, tokenize_words
from services.detection_engine.classifier import IndonesianAIClassifier
from services.detection_engine.calibrator import ForensicCalibrator
from services.detection_engine.llm_auditor import GeminiForensicAuditor


class NexusIndonesianDetector:
    """
    Main forensic detection engine for Indonesian text authorship analysis.
    """

    def __init__(self):
        self.extractor = IndonesianFeatureExtractor()
        self.classifier = IndonesianAIClassifier()
        self.calibrator = ForensicCalibrator()
        self.auditor = GeminiForensicAuditor()
        self._initialized = False

    def initialize(self):
        """Pre-loads classifier model."""
        if not self._initialized:
            self.classifier.ensure_trained()
            self._initialized = True

    def analyze(self, text: str, include_llm_audit: bool = True) -> Dict[str, Any]:
        """
        Executes full forensic detection pipeline on Indonesian text.
        """
        start_time = time.time()
        self.initialize()

        raw_text = text.strip() if text else ""
        words = tokenize_words(raw_text)
        n_words = len(words)
        sentences = segment_sentences(raw_text)
        n_sentences = len(sentences)

        # 1. Feature Extraction
        features = self.extractor.extract_features(raw_text)

        # 2. Check Out-Of-Distribution (OOD)
        is_ood, ood_reason = self.calibrator.check_ood(
            raw_text,
            n_words,
            features.get("indonesian_stopword_ratio", 0.0)
        )

        # 3. Model Inference
        inference_res = self.classifier.predict(raw_text)
        raw_ai_prob = inference_res["blended_ai_probability"]
        model_agreement = inference_res["model_agreement"]
        top_features = inference_res["top_driving_features"]

        # 4. Sentence-Level Analysis (Heatmap)
        sentence_analysis = self.extractor.analyze_sentences(raw_text)
        sentence_scores = [s["ai_score"] for s in sentence_analysis]
        sent_variance = (
            sum((s - (sum(sentence_scores) / len(sentence_scores))) ** 2 for s in sentence_scores) / len(sentence_scores)
            if sentence_scores else 0.0
        )

        # 5. Calibration & Uncertainty
        uncertainty_info = self.calibrator.calculate_uncertainty(
            raw_ai_prob,
            model_agreement,
            n_words,
            sent_variance
        )
        uncertainty_score = uncertainty_info["uncertainty_score"]
        confidence_level = uncertainty_info["confidence_level"]
        calibrated_prob = self.calibrator.calibrate_probability(raw_ai_prob)

        # 6. Final 4-Outcome Verdict
        verdict, verdict_explanation = self.calibrator.determine_verdict(
            calibrated_prob,
            uncertainty_score,
            is_ood,
            ood_reason,
            sentence_scores
        )

        # If Inconclusive due to OOD, adjust display probability
        display_probability = round(calibrated_prob * 100.0, 1)
        if verdict == "Inconclusive":
            display_prob_text = "N/A (Tidak Konklusif)"
        else:
            display_prob_text = f"{display_probability}%"

        # 7. LLM Contextual Audit (Gemini)
        statistical_summary = {
            "burstiness": round(features.get("burstiness", 0.0), 4),
            "ttr": round(features.get("ttr", 0.0), 4),
            "yules_k": round(features.get("yules_k", 0.0), 2),
            "ai_transition_density": round(features.get("ai_transition_density", 0.0), 2),
            "verdict": verdict,
            "calibrated_probability": calibrated_prob
        }

        llm_audit = {}
        if include_llm_audit and not is_ood:
            llm_audit = self.auditor.audit_text(raw_text, statistical_summary)
        else:
            llm_audit = {
                "status": "skipped",
                "reason": ood_reason if is_ood else "LLM audit disabled by caller."
            }

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        # 8. Forensic Summary & Transparency Limitations
        return {
            "status": "success",
            "verdict": verdict,
            "verdict_explanation": verdict_explanation,
            "calibrated_ai_probability": calibrated_prob,
            "display_probability": display_prob_text,
            "confidence_level": confidence_level,
            "uncertainty_score": uncertainty_score,
            "model_agreement": model_agreement,
            "document_statistics": {
                "word_count": n_words,
                "sentence_count": n_sentences,
                "avg_sentence_length": round(features.get("sentence_length_mean", 0.0), 1),
                "sentence_length_std": round(features.get("sentence_length_std", 0.0), 2),
                "burstiness": round(features.get("burstiness", 0.0), 4),
                "ttr": round(features.get("ttr", 0.0), 4),
                "yules_k": round(features.get("yules_k", 0.0), 2),
                "shannon_entropy": round(features.get("shannon_entropy", 0.0), 2),
                "ai_transition_density": round(features.get("ai_transition_density", 0.0), 2),
                "nominalization_density": round(features.get("nominalization_density", 0.0), 2),
                "indonesian_stopword_ratio": round(features.get("indonesian_stopword_ratio", 0.0), 3)
            },
            "top_driving_features": top_features,
            "sentence_heatmap": sentence_analysis,
            "llm_audit": llm_audit,
            "disclaimer": (
                "DISCLAIMER ILMIAH: Hasil analisis deteksi teks berbasis AI ini merupakan taksiran "
                "probabilistik dari fitur linguistik dan statistik komparatif. Analisis teks tidak dapat "
                "dijadikan bukti mutlak kepengarangan tanpa didukung konfirmasi riwayat berkas, wawancara, "
                "dan bukti forensik digital lainnya. NEXUS AI secara ketat menolak klaim kepastian 100%."
            ),
            "execution_time_ms": elapsed_ms
        }


if __name__ == "__main__":
    detector = NexusIndonesianDetector()
    print("Nexus Indonesian AI Detector Initialized.")

    sample_doc = (
        "Penyusunan arsitektur SPBE Provinsi DKI Jakarta berpedoman pada prinsip interoperabilitas sistem "
        "dan bagi pakai data antarsub-sistem. Dinas Komunikasi, Informatika dan Statistik menetapkan standar "
        "metadatabase terpusat guna menghindari duplikasi aplikasi di lingkungan satuan kerja perangkat daerah. "
        "Dalam era digitalisasi yang serba cepat ini, penerapan teknologi informasi menjadi suatu keniscayaan yang "
        "tidak dapat dihindari bagi setiap organisasi. Selain itu, integrasi sistem kecerdasan buatan memainkan peran "
        "yang sangat penting dalam meningkatkan efisiensi operasional secara signifikan."
    )

    report = detector.analyze(sample_doc)
    print("\n--- FORENSIC REPORT SUMMARY ---")
    print("Verdict:", report["verdict"])
    print("Probability:", report["display_probability"])
    print("Confidence:", report["confidence_level"])
    print("Uncertainty Score:", report["uncertainty_score"])
    print("Model Agreement:", report["model_agreement"])
    print("Words:", report["document_statistics"]["word_count"])
    print("Sentences:", report["document_statistics"]["sentence_count"])
    print("Burstiness:", report["document_statistics"]["burstiness"])
    print("Sentence Heatmap items:", len(report["sentence_heatmap"]))
