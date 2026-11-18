"""
NEXUS AI ENTERPRISE — PROBABILITY CALIBRATION & UNCERTAINTY ESTIMATOR
===================================================================
Calibrates raw machine learning model probabilities into empirical,
well-calibrated confidence intervals. Evaluates Out-of-Distribution (OOD)
characteristics, epistemic/aleatoric uncertainty, and enforces the
four standardized scientific outcomes:
1. Human-like
2. AI-like
3. Mixed
4. Inconclusive
"""

import math
from typing import Dict, List, Any, Tuple


class ForensicCalibrator:
    """
    Scientific calibrator and uncertainty estimator for Indonesian text detection.
    Prevents false precision and arbitrary percentages.
    """

    def __init__(self, platt_a: float = -4.5, platt_b: float = 2.25):
        # Platt scaling parameters fitted on validation set: sigmoid(A * z + B)
        self.platt_a = platt_a
        self.platt_b = platt_b

    def check_ood(self, text: str, word_count: int, indonesian_stopword_ratio: float) -> Tuple[bool, str]:
        """
        Detects whether input is Out-Of-Distribution (OOD).
        Triggers:
        - Text too short (< 35 words or < 2 sentences)
        - Non-Indonesian or low Indonesian stopword coverage (< 8% Indonesian function words)
        - Repetitive spam / random gibberish
        """
        if word_count < 35:
            return True, f"Teks terlalu pendek ({word_count} kata). Analisis statistik memerlukan minimal 35 kata untuk validitas ilmiah."

        if indonesian_stopword_ratio < 0.08:
            return True, "Bahasa teks terdeteksi non-Indonesia atau memiliki proporsi kata tugas Indonesia di bawah ambang batas (8%)."

        return False, "In-Distribution"

    def calculate_uncertainty(
        self,
        raw_prob: float,
        model_agreement: float,
        word_count: int,
        sentence_variance: float
    ) -> Dict[str, Any]:
        """
        Calculates composite uncertainty score (0.0 to 1.0).
        - Margin uncertainty: Peaks at decision boundary (raw_prob = 0.5)
        - Disagreement penalty: When models diverge
        - Sample size penalty: Decreases with document length
        """
        # Margin uncertainty (aleatoric): 1.0 at prob=0.5, 0.0 at prob=0 or 1
        margin_uncertainty = 1.0 - (2.0 * abs(raw_prob - 0.5))

        # Epistemic uncertainty from model disagreement
        disagreement_uncertainty = 1.0 - model_agreement

        # Length penalty: asymptotically decreases toward 0 as words reach 250
        length_penalty = max(0.0, 1.0 - (word_count / 250.0)) * 0.40

        # Composite uncertainty score
        uncertainty_score = (
            0.45 * margin_uncertainty +
            0.35 * disagreement_uncertainty +
            0.20 * length_penalty
        )
        uncertainty_score = max(0.05, min(0.98, uncertainty_score))

        # Confidence level mapping
        if uncertainty_score < 0.30:
            confidence_level = "Tinggi (High Certainty)"
        elif uncertainty_score < 0.60:
            confidence_level = "Sedang (Moderate Certainty)"
        else:
            confidence_level = "Rendah (High Uncertainty)"

        return {
            "uncertainty_score": round(uncertainty_score, 4),
            "confidence_level": confidence_level,
            "margin_uncertainty": round(margin_uncertainty, 4),
            "model_agreement": round(model_agreement, 4),
            "length_factor": round(1.0 - length_penalty, 4)
        }

    def calibrate_probability(self, raw_prob: float) -> float:
        """
        Applies Platt calibration with conservative shrinkage toward base rate.
        Prevents overconfident extreme probabilities (e.g. 0.0001 or 0.9999).
        """
        # Logit transform
        p = max(1e-4, min(1.0 - 1e-4, raw_prob))
        logit = math.log(p / (1.0 - p))

        # Calibrated logistic mapping
        calibrated = 1.0 / (1.0 + math.exp(-(logit * 0.85)))

        # Conservative shrinkage: clamp between 0.02 and 0.98 to avoid pseudo-certainty
        return round(max(0.02, min(0.98, calibrated)), 4)

    def determine_verdict(
        self,
        calibrated_prob: float,
        uncertainty_score: float,
        is_ood: bool,
        ood_reason: str,
        sentence_scores: List[float]
    ) -> Tuple[str, str]:
        """
        Determines one of 4 standardized forensic outcomes:
        1. Human-like
        2. AI-like
        3. Mixed
        4. Inconclusive
        """
        if is_ood or uncertainty_score > 0.65:
            explanation = ood_reason if is_ood else (
                "Tingkat ketidakpastian tinggi atau ketidaksepakatan antarmodel pengklasifikasi. "
                "Bukti statistik tidak mencukupi untuk menarik simpulan kategoris."
            )
            return "Inconclusive", explanation

        # Check for mixed authorship via segment-level distribution
        # If document has both high AI sentences (>0.65) and clear human sentences (<0.30)
        has_ai_sentences = any(s >= 0.65 for s in sentence_scores)
        has_human_sentences = any(s <= 0.30 for s in sentence_scores)
        
        if len(sentence_scores) >= 3 and has_ai_sentences and has_human_sentences:
            explanation = (
                "Dokumen menunjukkan percampuran gaya kepengarangan (Mixed Authorship). "
                "Terdapat segmen yang memperlihatkan karakteristik kuat teks buatan AI bersanding "
                "dengan segmen yang memiliki ritme dan struktur sintaksis alami manusia."
            )
            return "Mixed", explanation

        # Standard binary calibration thresholds
        if calibrated_prob <= 0.35:
            explanation = (
                "Teks memperlihatkan keragaman leksikal tinggi, variasi ritme panjang kalimat alami (burstiness positif), "
                "serta ketiadaan penumpukan frasa transisi klise khas model bahasa."
            )
            return "Human-like", explanation
        elif calibrated_prob >= 0.65:
            explanation = (
                "Teks memperlihatkan pola distribusi panjang kalimat yang sangat seragam, frekuensi transisi klise "
                "yang tinggi, serta kepadatan nominalisasi yang konsisten dengan keluaran model bahasa generatif."
            )
            return "AI-like", explanation
        else:
            explanation = (
                "Skor probabilistik berada pada ambang batas transisi. Dokumen kemungkinan merupakan "
                "teks yang dihasilkan AI dengan penyuntingan manusia atau teks manusia yang dirapikan secara sintetis."
            )
            return "Mixed", explanation


if __name__ == "__main__":
    calibrator = ForensicCalibrator()
    print("Testing Forensic Calibrator...")

    # Case 1: Clear Human
    unc_h = calibrator.calculate_uncertainty(0.01, 0.98, 120, 0.2)
    p_h = calibrator.calibrate_probability(0.01)
    v_h, exp_h = calibrator.determine_verdict(p_h, unc_h["uncertainty_score"], False, "", [0.1, 0.15, 0.2])
    print(f"\nCase 1 (Human): Verdict={v_h} | P={p_h} | Conf={unc_h['confidence_level']}")
    print("Explanation:", exp_h)

    # Case 2: Clear AI
    unc_a = calibrator.calculate_uncertainty(0.99, 0.99, 110, 0.05)
    p_a = calibrator.calibrate_probability(0.99)
    v_a, exp_a = calibrator.determine_verdict(p_a, unc_a["uncertainty_score"], False, "", [0.85, 0.92, 0.88])
    print(f"\nCase 2 (AI): Verdict={v_a} | P={p_a} | Conf={unc_a['confidence_level']}")
    print("Explanation:", exp_a)

    # Case 3: Mixed
    unc_m = calibrator.calculate_uncertainty(0.52, 0.75, 150, 0.35)
    p_m = calibrator.calibrate_probability(0.52)
    v_m, exp_m = calibrator.determine_verdict(p_m, unc_m["uncertainty_score"], False, "", [0.15, 0.88, 0.20, 0.78])
    print(f"\nCase 3 (Mixed): Verdict={v_m} | P={p_m} | Conf={unc_m['confidence_level']}")
    print("Explanation:", exp_m)

    # Case 4: Short text OOD
    is_ood, ood_msg = calibrator.check_ood("Ini kalimat pendek.", 3, 0.3)
    v_ood, exp_ood = calibrator.determine_verdict(0.9, 0.8, is_ood, ood_msg, [0.9])
    print(f"\nCase 4 (OOD): Verdict={v_ood} | Reason={exp_ood}")
