"""
NEXUS AI ENTERPRISE — ADVANCED LINGUISTIC & STATISTICAL FEATURE EXTRACTOR
========================================================================
Scientific feature extraction engine for Indonesian AI-generated text detection.
Extracts 28+ quantitative markers spanning:
1. Sentence length distribution & burstiness (variation in cadence)
2. Lexical diversity (TTR, Root TTR, Log TTR, Yule's K, Hapax Legomena)
3. Information-theoretic entropy & n-gram predictability proxy
4. Indonesian discourse markers & AI stylistic hallmarks
5. Morphological affix distribution (nominalization & voice)
6. Sentence-level and paragraph-level segmentation
"""

import re
import math
from collections import Counter
from typing import Dict, List, Any, Tuple


# ---------------------------------------------------------------------------
# INDONESIAN AI STYLISTIC HALLMARKS & TRANSITION PHRASES
# Statistically overrepresented in LLM Indonesian outputs
# ---------------------------------------------------------------------------
AI_CLICHE_PHRASES = [
    "dalam era digitalisasi",
    "dalam era digital",
    "yang serba cepat ini",
    "memainkan peran penting",
    "memainkan peranan krusial",
    "memegang peranan krusial",
    "tidak dapat dipungkiri",
    "tidak dapat dipungkiri bahwa",
    "langkah konkret dan strategis",
    "secara holistik dan komprehensif",
    "sebagai kesimpulan",
    "membawa angin segar",
    "senantiasa berupaya",
    "penting untuk dicatat bahwa",
    "dapat dipahami bahwa",
    "menyelami lebih dalam",
    "secara signifikan",
    "kunci utama keberlanjutan",
    "bukan lagi sekadar pilihan melainkan",
    "tata kelola yang inklusif",
    "memberikan kontribusi nyata"
]

# Legitimate academic markers (EXCLUDED from AI suspicion per ai-authorship-forensics):
# "selain itu", "dengan demikian", "oleh karena itu", "berdasarkan hasil penelitian"
LEGITIMATE_ACADEMIC_CONNECTORS = {
    "selain itu", "dengan demikian", "oleh karena itu", "berdasarkan hasil penelitian"
}

# Formulaic repetitive transition markers over-indexed in LLM outputs:
AI_TRANSITION_MARKERS = [
    "lebih lanjut",
    "di sisi lain",
    "secara keseluruhan",
    "sebagai penutup",
    "pada intinya",
    "dalam konteks ini",
    "pada akhirnya",
    "namun demikian"
]

INDONESIAN_STOPWORDS = {
    "yang", "di", "dan", "itu", "dengan", "untuk", "tidak", "ini", "dari", "dalam",
    "akan", "pada", "juga", "saya", "ke", "karena", "tersebut", "bisa", "ada", "mereka",
    "lebih", "tahun", "oleh", "saat", "sudah", "dapat", "ia", "atas", "seperti", "tapi",
    "sampai", "kembali", "bahkan", "atau", "hanya", "sangat", "secara", "sebagai", "tentang"
}


def clean_text(text: str) -> str:
    """Normalize whitespace and strip control characters."""
    return re.sub(r'\s+', ' ', text).strip()


def segment_sentences(text: str) -> List[str]:
    """
    Carefully segments Indonesian text into sentences, respecting abbreviations
    (e.g., No., Rp., dkk., dll., Prof., Dr.).
    """
    text = clean_text(text)
    if not text:
        return []
    
    # Protect common Indonesian abbreviations
    abbr_map = {
        "No.": "NO_ABBR_TOKEN",
        "no.": "no_ABBR_TOKEN",
        "Rp.": "RP_ABBR_TOKEN",
        "dkk.": "DKK_ABBR_TOKEN",
        "dll.": "DLL_ABBR_TOKEN",
        "dst.": "DST_ABBR_TOKEN",
        "Prof.": "PROF_ABBR_TOKEN",
        "Dr.": "DR_ABBR_TOKEN",
        "Ir.": "IR_ABBR_TOKEN",
        "H.": "H_ABBR_TOKEN",
        "Hj.": "HJ_ABBR_TOKEN",
        "Sp.": "SP_ABBR_TOKEN",
    }
    
    protected = text
    for abbr, token in abbr_map.items():
        protected = protected.replace(abbr, token)
        
    # Split on sentence boundaries: period, exclamation, question mark followed by space or end
    raw_sentences = re.split(r'(?<=[.!?])\s+', protected)
    
    sentences = []
    for s in raw_sentences:
        restored = s.strip()
        for abbr, token in abbr_map.items():
            restored = restored.replace(token, abbr)
        if restored:
            sentences.append(restored)
            
    return sentences if sentences else [text]


def segment_paragraphs(text: str) -> List[str]:
    """Segments text into non-empty paragraphs."""
    raw_paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    return raw_paras if raw_paras else [text.strip()]


def tokenize_words(text: str) -> List[str]:
    """Tokenize Indonesian text into lowercased alphabetic/alphanumeric tokens."""
    return re.findall(r'\b[a-zA-Z0-9_\-]+\b', text.lower())


class IndonesianFeatureExtractor:
    """
    Extracts deep linguistic, statistical, and stylistic features for Indonesian text.
    """

    FEATURE_NAMES = [
        "sentence_length_mean",
        "sentence_length_std",
        "sentence_length_cv",
        "burstiness",
        "sentence_length_min",
        "sentence_length_max",
        "ttr",
        "root_ttr",
        "log_ttr",
        "hapax_ratio",
        "dis_legomena_ratio",
        "yules_k",
        "simpson_diversity",
        "shannon_entropy",
        "char_entropy",
        "bigram_entropy",
        "ai_transition_density",
        "ai_cliche_density",
        "nominalization_density",
        "passive_voice_density",
        "conjunction_density",
        "punctuation_diversity",
        "mean_words_per_para",
        "para_length_std",
        "indonesian_stopword_ratio",
        "avg_word_length",
        "flesch_kincaid_id_proxy",
        "sentence_predictability_proxy"
    ]

    def extract_features(self, text: str) -> Dict[str, float]:
        """
        Extract complete 28-feature dictionary from input text.
        """
        sentences = segment_sentences(text)
        paragraphs = segment_paragraphs(text)
        words = tokenize_words(text)
        n_words = len(words)
        n_sentences = max(1, len(sentences))
        n_paras = max(1, len(paragraphs))

        if n_words == 0:
            return {feat: 0.0 for feat in self.FEATURE_NAMES}

        # -------------------------------------------------------------------
        # 1. SENTENCE LENGTH DISTRIBUTION & BURSTINESS
        # Human writing has high variance in sentence length (staccato + long clauses).
        # AI models generate consistently medium-length sentences (low burstiness).
        # -------------------------------------------------------------------
        sent_lengths = [len(tokenize_words(s)) for s in sentences]
        sent_lengths = [l for l in sent_lengths if l > 0] or [1]
        
        sent_mean = sum(sent_lengths) / len(sent_lengths)
        sent_var = sum((l - sent_mean) ** 2 for l in sent_lengths) / len(sent_lengths)
        sent_std = math.sqrt(sent_var)
        sent_cv = sent_std / (sent_mean + 1e-9)
        
        # Standard Burstiness metric: (std - mean) / (std + mean)
        # B in [-1, 1]. Positive B implies high burstiness (human-like).
        burstiness = (sent_std - sent_mean) / (sent_std + sent_mean + 1e-9)
        sent_min = float(min(sent_lengths))
        sent_max = float(max(sent_lengths))

        # -------------------------------------------------------------------
        # 2. LEXICAL DIVERSITY (TTR, YULE'S K, HAPAX LEGOMENA)
        # -------------------------------------------------------------------
        word_counts = Counter(words)
        v_types = len(word_counts)
        
        # Type-Token Ratio
        ttr = v_types / n_words
        root_ttr = v_types / math.sqrt(n_words)
        log_ttr = math.log(v_types + 1e-9) / math.log(n_words + 1e-9) if n_words > 1 else 1.0

        # Frequency of spectrum elements (V_i = words occurring exactly i times)
        freq_spectrum = Counter(word_counts.values())
        hapax = freq_spectrum.get(1, 0)
        dis_legomena = freq_spectrum.get(2, 0)
        hapax_ratio = hapax / n_words
        dis_legomena_ratio = dis_legomena / n_words

        # Yule's Characteristic K = 10^4 * [ (sum(i^2 * V_i) - N) / N^2 ]
        # Invariant to text length. Lower K indicates richer vocabulary.
        sum_i2_vi = sum((i ** 2) * vi for i, vi in freq_spectrum.items())
        yules_k = 10000.0 * (sum_i2_vi - n_words) / ((n_words ** 2) + 1e-9)

        # Simpson's Diversity Index: 1 - sum(n_i * (n_i - 1) / (N * (N - 1)))
        if n_words > 1:
            simpson = 1.0 - sum(c * (c - 1) for c in word_counts.values()) / (n_words * (n_words - 1))
        else:
            simpson = 1.0

        # -------------------------------------------------------------------
        # 3. ENTROPY & INFORMATION THEORY
        # Shannon entropy of words and characters
        # -------------------------------------------------------------------
        shannon_entropy = -sum((c / n_words) * math.log2(c / n_words) for c in word_counts.values())
        
        # Character entropy
        chars = [c for c in text.lower() if c.isalnum()]
        n_chars = max(1, len(chars))
        char_counts = Counter(chars)
        char_entropy = -sum((c / n_chars) * math.log2(c / n_chars) for c in char_counts.values())

        # Bigram transition entropy (predictability proxy)
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words) - 1)]
        n_bigrams = max(1, len(bigrams))
        bigram_counts = Counter(bigrams)
        bigram_entropy = -sum((c / n_bigrams) * math.log2(c / n_bigrams) for c in bigram_counts.values())

        # -------------------------------------------------------------------
        # 4. INDONESIAN DISCOURSE & STYLISTIC HALLMARKS
        # Count frequency of transition markers and AI clichés per 100 words
        # -------------------------------------------------------------------
        lower_text = text.lower()
        
        transition_matches = 0
        for marker in AI_TRANSITION_MARKERS:
            # Word boundary regex for markers
            pattern = r'\b' + re.escape(marker) + r'\b'
            transition_matches += len(re.findall(pattern, lower_text))
        ai_transition_density = (transition_matches / n_words) * 100.0

        cliche_matches = 0
        for cliche in AI_CLICHE_PHRASES:
            pattern = r'\b' + re.escape(cliche) + r'\b'
            cliche_matches += len(re.findall(pattern, lower_text))
        ai_cliche_density = (cliche_matches / n_words) * 100.0

        # -------------------------------------------------------------------
        # 5. MORPHOLOGY: NOMINALIZATION & VOICE
        # AI in Indonesian heavily overuses nominalization (pe-...-an, per-...-an, ke-...-an)
        # -------------------------------------------------------------------
        nominal_count = 0
        passive_count = 0
        for w in words:
            if (w.startswith("pe") and w.endswith("an")) or \
               (w.startswith("per") and w.endswith("an")) or \
               (w.startswith("ke") and w.endswith("an")):
                nominal_count += 1
            if w.startswith("di") or w.startswith("ter"):
                passive_count += 1
                
        nominalization_density = (nominal_count / n_words) * 100.0
        passive_voice_density = (passive_count / n_words) * 100.0

        # Conjunction density (kata hubung)
        conjunctions = {"dan", "atau", "tetapi", "namun", "karena", "sehingga", "meskipun", "walaupun", "jika", "kalau", "ketika", "saat"}
        conjunction_count = sum(1 for w in words if w in conjunctions)
        conjunction_density = (conjunction_count / n_words) * 100.0

        # Punctuation diversity
        punct_matches = re.findall(r'[,.;:!?—\-"\'\(\)\[\]]', text)
        punct_counts = Counter(punct_matches)
        punctuation_diversity = len(punct_counts) / 10.0

        # Paragraph uniformity
        para_word_counts = [len(tokenize_words(p)) for p in paragraphs]
        mean_words_per_para = sum(para_word_counts) / n_paras
        para_var = sum((c - mean_words_per_para) ** 2 for c in para_word_counts) / n_paras
        para_length_std = math.sqrt(para_var)

        # Indonesian stopword ratio (validates Indonesian language domain)
        id_stop_count = sum(1 for w in words if w in INDONESIAN_STOPWORDS)
        indonesian_stopword_ratio = id_stop_count / n_words

        # Average word length
        avg_word_length = sum(len(w) for w in words) / n_words

        # Flesch-Kincaid Indonesian proxy (Readability)
        # Based on syllable estimate (Indonesian syllables approx = vowel count)
        vowel_count = sum(len(re.findall(r'[aiueo]', w)) for w in words)
        syllables_per_word = vowel_count / n_words
        flesch_kincaid_id_proxy = 0.39 * sent_mean + 11.8 * syllables_per_word - 15.59

        # Sentence predictability proxy:
        # Measures how many sentences start with repetitive transitions
        starts_with_transition = 0
        for s in sentences:
            s_clean = s.strip().lower()
            if any(s_clean.startswith(m) for m in AI_TRANSITION_MARKERS):
                starts_with_transition += 1
        sentence_predictability_proxy = starts_with_transition / n_sentences

        return {
            "sentence_length_mean": float(sent_mean),
            "sentence_length_std": float(sent_std),
            "sentence_length_cv": float(sent_cv),
            "burstiness": float(burstiness),
            "sentence_length_min": float(sent_min),
            "sentence_length_max": float(sent_max),
            "ttr": float(ttr),
            "root_ttr": float(root_ttr),
            "log_ttr": float(log_ttr),
            "hapax_ratio": float(hapax_ratio),
            "dis_legomena_ratio": float(dis_legomena_ratio),
            "yules_k": float(yules_k),
            "simpson_diversity": float(simpson),
            "shannon_entropy": float(shannon_entropy),
            "char_entropy": float(char_entropy),
            "bigram_entropy": float(bigram_entropy),
            "ai_transition_density": float(ai_transition_density),
            "ai_cliche_density": float(ai_cliche_density),
            "nominalization_density": float(nominalization_density),
            "passive_voice_density": float(passive_voice_density),
            "conjunction_density": float(conjunction_density),
            "punctuation_diversity": float(punctuation_diversity),
            "mean_words_per_para": float(mean_words_per_para),
            "para_length_std": float(para_length_std),
            "indonesian_stopword_ratio": float(indonesian_stopword_ratio),
            "avg_word_length": float(avg_word_length),
            "flesch_kincaid_id_proxy": float(flesch_kincaid_id_proxy),
            "sentence_predictability_proxy": float(sentence_predictability_proxy)
        }

    def analyze_sentences(self, text: str) -> List[Dict[str, Any]]:
        """
        Segment-level analysis: extracts per-sentence metrics and individual risk scores
        for UI heatmap rendering and forensic explanation.
        """
        sentences = segment_sentences(text)
        results = []

        for idx, s in enumerate(sentences):
            words = tokenize_words(s)
            n_w = len(words)
            s_lower = s.lower().strip()

            if n_w == 0:
                continue

            # Identify specific cliches and transitions in this sentence
            found_cliches = [c for c in AI_CLICHE_PHRASES if c in s_lower]
            found_transitions = [m for m in AI_TRANSITION_MARKERS if s_lower.startswith(m) or f", {m}" in s_lower]
            
            # Sentence-level synthetic risk heuristic (0.0 to 1.0)
            risk_score = 0.20  # Base neutral baseline

            # Cliche penalty
            if found_cliches:
                risk_score += 0.35 * len(found_cliches)

            # Transition at beginning penalty
            if found_transitions:
                risk_score += 0.25

            # Monotonous sentence length penalty (LLM sentences tend to cluster heavily around 16-24 words)
            if 16 <= n_w <= 24:
                risk_score += 0.12
            elif n_w < 8 or n_w > 38:
                # Extreme staccato or very long run-on sentences are very common in human writing
                risk_score -= 0.15

            # Clamp between 0.05 and 0.95
            risk_score = max(0.05, min(0.95, risk_score))

            if risk_score > 0.60:
                level = "high"
                explanation = "Mengandung frasa transisi klise AI dan struktur klausa yang sangat simetris."
            elif risk_score >= 0.35:
                level = "medium"
                explanation = "Struktur kalimat formal dengan ritme moderat; perlu audit kontekstual."
            else:
                level = "low"
                explanation = "Variasi panjang dan pilihan diksi menunjukkan karakteristik tulisan manusia alami."

            results.append({
                "index": idx,
                "text": s,
                "word_count": n_w,
                "ai_score": round(risk_score, 3),
                "level": level,
                "markers_found": found_cliches + found_transitions,
                "explanation": explanation
            })

        return results


if __name__ == "__main__":
    extractor = IndonesianFeatureExtractor()
    sample_text = (
        "Dalam era digitalisasi yang serba cepat ini, penerapan teknologi informasi menjadi suatu keniscayaan yang "
        "tidak dapat dihindari bagi setiap organisasi. Selain itu, integrasi sistem kecerdasan buatan memainkan peran "
        "yang sangat penting dalam meningkatkan efisiensi operasional secara signifikan."
    )
    feats = extractor.extract_features(sample_text)
    print("Extracted Features (Total:", len(feats), "):")
    for k, v in list(feats.items())[:10]:
        print(f"  {k}: {v:.4f}")
    sents = extractor.analyze_sentences(sample_text)
    print("\nSentence Analysis:")
    for s in sents:
        print(f"  [{s['level'].upper()}] ({s['ai_score']}) {s['text'][:60]}... -> {s['explanation']}")
