"""
NEXUS AI ENTERPRISE — INDONESIAN AI TEXT CLASSIFIER (XGBOOST / GRADIENT BOOSTING)
================================================================================
Scientific supervised ensemble classifier for Indonesian AI-generated text detection.
Combines:
1. HistGradientBoostingClassifier (Tree-based ensemble for non-linear interactions)
2. Calibrated Logistic / Linear model (Auxiliary baseline for model agreement)
3. Feature standardization and importance tracking
"""

import json
import os
import sys

# Silence joblib multiprocessing warning on Windows
os.environ["LOKY_MAX_CPU_COUNT"] = "1"

import pickle
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from typing import Dict, List, Any, Tuple, Optional
from sklearn.ensemble import HistGradientBoostingClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_score

from services.detection_engine.feature_extractor import IndonesianFeatureExtractor

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(MODEL_DIR)), "data", "indonesian_detection_dataset")
MODEL_FILE_PATH = os.path.join(MODEL_DIR, "indo_detector_model.pkl")


class IndonesianAIClassifier:
    """
    Supervised classifier for detecting Indonesian AI-generated texts.
    Features model agreement, calibrated tree predictions, and top driving feature attribution.
    """

    def __init__(self):
        self.extractor = IndonesianFeatureExtractor()
        self.feature_names = self.extractor.FEATURE_NAMES
        self.scaler = StandardScaler()
        self.tree_model = HistGradientBoostingClassifier(
            max_iter=100,
            learning_rate=0.08,
            max_depth=5,
            min_samples_leaf=3,
            random_state=42
        )
        self.linear_model = LogisticRegression(
            C=1.0,
            max_iter=500,
            random_state=42
        )
        self.is_trained = False
        self.cv_accuracy_mean = 0.0
        self.cv_f1_mean = 0.0

    def load_dataset(self, split: str = "train") -> Tuple[List[Dict[str, float]], List[int], List[str]]:
        """
        Loads dataset split (train, val, or test) from JSONL files.
        """
        file_path = os.path.join(DATASET_DIR, f"{split}.jsonl")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset split not found: {file_path}")

        features_list = []
        labels = []
        texts = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                doc = json.loads(line)
                feats = self.extractor.extract_features(doc["text"])
                features_list.append(feats)
                labels.append(int(doc["ground_truth"]))
                texts.append(doc["text"])

        return features_list, labels, texts

    def _features_to_matrix(self, features_list: List[Dict[str, float]]) -> np.ndarray:
        """Converts list of feature dicts to 2D numpy array with fixed column order."""
        matrix = []
        for feats in features_list:
            row = [feats.get(name, 0.0) for name in self.feature_names]
            matrix.append(row)
        return np.array(matrix, dtype=np.float64)

    def train(self) -> Dict[str, Any]:
        """
        Trains both tree-based and linear classifiers on the train + val splits
        with 5-fold stratified cross-validation.
        """
        train_feats, train_labels, _ = self.load_dataset("train")
        val_feats, val_labels, _ = self.load_dataset("val")

        all_feats = train_feats + val_feats
        all_labels = train_labels + val_labels

        X = self._features_to_matrix(all_feats)
        y = np.array(all_labels, dtype=np.int32)

        # 5-Fold Stratified Cross Validation
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_acc = cross_val_score(self.tree_model, X, y, cv=skf, scoring='accuracy')
        cv_f1 = cross_val_score(self.tree_model, X, y, cv=skf, scoring='f1')

        self.cv_accuracy_mean = float(np.mean(cv_acc))
        self.cv_f1_mean = float(np.mean(cv_f1))

        # Fit Scaler and Models on full training set
        X_scaled = self.scaler.fit_transform(X)
        self.tree_model.fit(X_scaled, y)
        self.linear_model.fit(X_scaled, y)
        self.is_trained = True

        # Save artifacts
        self.save_model()

        return {
            "status": "success",
            "samples_trained": len(y),
            "cv_accuracy_mean": self.cv_accuracy_mean,
            "cv_f1_mean": self.cv_f1_mean,
            "features_count": len(self.feature_names)
        }

    def save_model(self, file_path: Optional[str] = None):
        """Serializes trained models and scaler."""
        path = file_path or MODEL_FILE_PATH
        state = {
            "scaler": self.scaler,
            "tree_model": self.tree_model,
            "linear_model": self.linear_model,
            "feature_names": self.feature_names,
            "cv_accuracy_mean": self.cv_accuracy_mean,
            "cv_f1_mean": self.cv_f1_mean,
            "is_trained": self.is_trained
        }
        with open(path, "wb") as f:
            pickle.dump(state, f)

    def load_model(self, file_path: Optional[str] = None) -> bool:
        """Loads serialized trained models and scaler."""
        path = file_path or MODEL_FILE_PATH
        if not os.path.exists(path):
            return False

        try:
            with open(path, "rb") as f:
                state = pickle.load(f)
            self.scaler = state["scaler"]
            self.tree_model = state["tree_model"]
            self.linear_model = state["linear_model"]
            self.feature_names = state["feature_names"]
            self.cv_accuracy_mean = state.get("cv_accuracy_mean", 0.0)
            self.cv_f1_mean = state.get("cv_f1_mean", 0.0)
            self.is_trained = state.get("is_trained", True)
            return True
        except Exception:
            return False

    def ensure_trained(self):
        """Ensures the model is loaded or trained."""
        if not self.is_trained:
            if not self.load_model():
                self.train()

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Runs model inference on input Indonesian text.
        Returns tree probability, linear probability, ensemble agreement,
        and top driving features.
        """
        self.ensure_trained()

        raw_feats = self.extractor.extract_features(text)
        X_raw = self._features_to_matrix([raw_feats])
        X_scaled = self.scaler.transform(X_raw)

        # Probabilities
        tree_prob_ai = float(self.tree_model.predict_proba(X_scaled)[0, 1])
        linear_prob_ai = float(self.linear_model.predict_proba(X_scaled)[0, 1])

        # Ensemble agreement: 1.0 = perfect agreement, 0.0 = total contradiction
        agreement = 1.0 - abs(tree_prob_ai - linear_prob_ai)

        # Blended base probability (70% tree ensemble, 30% linear baseline)
        blended_ai_prob = 0.70 * tree_prob_ai + 0.30 * linear_prob_ai

        # Top driving feature attribution using linear model coefficients * scaled values
        coefficients = self.linear_model.coef_[0]
        feature_impacts = []
        for name, coef, val, s_val in zip(self.feature_names, coefficients, X_raw[0], X_scaled[0]):
            contribution = coef * s_val
            feature_impacts.append({
                "feature": name,
                "raw_value": round(float(val), 4),
                "scaled_value": round(float(s_val), 4),
                "coefficient": round(float(coef), 4),
                "impact": round(float(contribution), 4),
                "direction": "ai" if contribution > 0 else "human"
            })

        # Sort features by absolute impact
        feature_impacts.sort(key=lambda x: abs(x["impact"]), reverse=True)

        return {
            "blended_ai_probability": round(blended_ai_prob, 4),
            "tree_ai_probability": round(tree_prob_ai, 4),
            "linear_ai_probability": round(linear_prob_ai, 4),
            "model_agreement": round(agreement, 4),
            "top_driving_features": feature_impacts[:6],
            "raw_features": raw_feats
        }


if __name__ == "__main__":
    classifier = IndonesianAIClassifier()
    print("Training Indonesian AI Classifier...")
    res = classifier.train()
    print("Training Results:", json.dumps(res, indent=2))

    test_human = (
        "Ketimpangan distribusi pendapatan di wilayah perdesaan Jawa Tengah dipengaruhi oleh kepemilikan lahan "
        "pertanian dan akses terhadap kredit mikro perbankan. Menggunakan model regresi spasial data panel kurun waktu "
        "2015 hingga 2023, koefisien Gini terbukti menurun secara gradual di kabupaten yang merealisasikan program dana desa."
    )
    test_ai = (
        "Dalam era digitalisasi yang serba cepat ini, penerapan teknologi informasi menjadi suatu keniscayaan yang "
        "tidak dapat dihindari bagi setiap organisasi. Selain itu, integrasi sistem kecerdasan buatan memainkan peran "
        "yang sangat penting dalam meningkatkan efisiensi operasional secara signifikan. Lebih lanjut, hal ini krusial."
    )

    pred_h = classifier.predict(test_human)
    pred_a = classifier.predict(test_ai)

    print("\n--- INFERENCE TEST 1 (Authentic Human) ---")
    print(f"Blended AI Prob: {pred_h['blended_ai_probability']} | Agreement: {pred_h['model_agreement']}")
    print("Top features:", [f"{f['feature']} ({f['direction']})" for f in pred_h['top_driving_features'][:3]])

    print("\n--- INFERENCE TEST 2 (Raw AI) ---")
    print(f"Blended AI Prob: {pred_a['blended_ai_probability']} | Agreement: {pred_a['model_agreement']}")
    print("Top features:", [f"{f['feature']} ({f['direction']})" for f in pred_a['top_driving_features'][:3]])
