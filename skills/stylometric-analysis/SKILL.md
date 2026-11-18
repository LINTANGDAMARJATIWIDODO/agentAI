---
name: stylometric-analysis
description: Quantitative stylometrics, syntactic complexity, lexical diversity, authorial rhythm, and writing consistency analysis for Indonesian texts.
version: 1.0
---

# STYLOMETRIC ANALYSIS ENGINE

## 1. MISSION

Analyze quantitative stylistic patterns and structural habits in Indonesian writing to support forensic authorship evaluation without confusing academic rigor with synthetic regularity.

## 2. STYLOMETRIC PARAMETERS

### A. Sentence Length Dynamics
- **Mean Sentence Length (MSL)**: Average words per sentence across the document.
- **Sentence Length Standard Deviation (SLSD)**: Spread of sentence lengths. Low variance across 10+ sentences indicates rigid pacing; natural human writing shows higher rhythmic ebb and flow.
- **Clause Embedding**: Ratio of complex sentences with subordinate clauses (anak kalimat) versus simple compound structures.

### B. Lexical Richness & Diversity
- **Type-Token Ratio (TTR)**: Ratio of unique words (types) to total words (tokens). Calculated as:
  $$TTR = \frac{V}{N}$$
- **Root-TTR & Log-TTR**: Length-invariant measures of vocabulary richness.
- **Yule's Characteristic K**: Measure of lexical repetition independent of document length:
  $$K = 10^4 \times \frac{\sum (i^2 \cdot V_i) - N}{N^2}$$
  Higher Yule's K indicates higher concentration of repeated vocabulary.

### C. Function Word & Morphological Distribution
- **Indonesian Function Words**: Density and relative frequencies of prepositions, conjunctions, and particles ("yang", "di", "dan", "ke", "dari", "pada").
- **Nominalization Density**: Distribution of affixes creating nouns from verbs/adjectives (*pe-an*, *ke-an*, *per-an*). High nominalization is normal and expected in Indonesian legal, SPBE, and academic discourse.

### D. Punctuation Fingerprint
- Comma density per 100 words.
- Semicolon and colon usage patterns.
- Parenthetical clause frequency.

## 3. LINGUISTIC PROTECTION RULES

- **Academic Conventions**: Do not penalize consistent sentence lengths in technical specifications, SPBE architecture matrices, or regulatory citations.
- **Domain Vocabulary**: A low TTR due to necessary repetitions of statutory terms ("SPBE", "perangkat daerah", "infrastruktur") is a hallmark of domain precision, not machine synthesis.
- **Never infer AI generation solely from stylometric regularity without corroborating statistical and linguistic markers.**
