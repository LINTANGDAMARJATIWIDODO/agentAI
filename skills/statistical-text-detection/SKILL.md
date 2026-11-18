---
name: statistical-text-detection
description: Mathematical and statistical modeling of text predictability, perplexity, burstiness, Shannon entropy, and calibrated probability estimation for Indonesian text.
version: 1.0
---

# STATISTICAL TEXT DETECTION ENGINE

## 1. MISSION

Execute rigorous statistical computations to evaluate the distributional regularity of tokens, clauses, and n-grams in Indonesian prose.

## 2. MATHEMATICAL METRICS

### A. Burstiness (B)
Measures the irregularity or "clustering" of sentence lengths and token occurrences:
$$B = \frac{\sigma - \mu}{\sigma + \mu}$$
Where $\mu$ is the mean sentence length and $\sigma$ is the standard deviation.
- Natural human writing exhibits burstiness with varying clause lengths ($B > -0.30$).
- Raw AI generation often clusters tightly around uniform sentence lengths ($B < -0.45$).
- *Note:* Do not treat low burstiness alone as proof of AI authorship.

### B. Shannon Information Entropy (H)
Measures the information density and vocabulary uncertainty:
$$H = -\sum_{i=1}^{V} p(w_i) \log_2 p(w_i)$$
Where $p(w_i)$ is the empirical probability of token $w_i$.
- Natural human academic Indonesian text typically achieves $H \in [5.5, 7.5]$ bits.

### C. N-gram Predictability & Token Likelihood
- Evaluates transition probabilities between adjacent word pairs and trigrams.
- Compares observed sequence frequencies against baseline Indonesian language corpora.

## 3. STRICT VALIDATION & CALIBRATION

1. **Strict Text Length Threshold**:
   - Minimum sample requirement: **35 words** and **2 complete sentences**.
   - If input is below threshold or consists solely of headings/titles:
     **MUST RETURN INCONCLUSIVE.**
     Display: *"Data tidak cukup untuk klasifikasi kepengarangan."*

2. **No Fabricated Scores**:
   - Never output hardcoded, arbitrary, or fabricated percentages.
   - If a metric cannot be mathematically calculated, display:
     *"Data tidak tersedia"* or *"Tidak dapat dihitung"*.

3. **Probability Calibration**:
   - Scores must be calibrated using Platt sigmoid scaling or empirical binning.
   - Raw heuristic sums must never be presented as validated posterior probabilities.
