---
name: intelligent-revision-engine
description: Multi-skill harmonization engine that synthesizes linguistic, stylometric, statistical, and forensic findings to execute precise, minimal, and justified text revisions.
version: 1.0
---

# INTELLIGENT REVISION ENGINE

## 1. MISSION

Synthesize findings from all specialized analytical modules (Forensics, Linguistic, Stylometry, Statistics, Academic Writing, and Evidence Verification) to produce actionable, evidence-based revisions while rigorously protecting authentic human writing.

## 2. MULTI-SKILL ORCHESTRATION ARCHITECTURE

```
                  ┌────────────────────────┐
                  │    Main NEXUS Agent    │
                  │   Document Intake &    │
                  │    Task Allocation     │
                  └───────────┬────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
┌────────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
│  AI Authorship  │  │   Indonesian    │  │   Stylometric   │
│    Forensics    │  │   Linguistic    │  │    Analysis     │
│   (Detection)   │  │  (KBBI & EYD V) │  │  (Rhythm/MSL)   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
┌────────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
│   Statistical   │  │Academic Writing │  │    Evidence     │
│  Text Analysis  │  │  Intelligence   │  │  Verification   │
│(Entropy/Burst.) │  │  (Transitions)  │  │ (Uncertainty)   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
               ┌──────────────▼──────────────┐
               │ Intelligent Revision Engine │
               │   Harmonize Findings &      │
               │   Apply Targeted Fixes      │
               └──────────────┬──────────────┘
                              │
               ┌──────────────▼──────────────┐
               │    Final Forensic Report    │
               │   (7-Column PDF & Audit)    │
               └─────────────────────────────┘
```

## 3. DECISION FRAMEWORK & ACTION LABELS

Every sentence must be classified into one of four mutually exclusive decisions:

1. **`SUDAH BAIK`**:
   The sentence is already correct according to KBBI, EYD V, and standard academic conventions.
   - **Recommendation**: `"SUDAH BAIK — TIDAK MEMERLUKAN REVISI."`
   - **Revision Reason**: `"Sesuai kaidah KBBI & EYD V."`
   - **Rule**: Never modify or paraphrase a sentence marked SUDAH BAIK.

2. **`REVISI MINOR`**:
   Only spelling, punctuation (EYD V), capitalization, or small grammatical corrections are required.
   - Examples: Fixing non-standard words (*"praktek"* -> *"praktik"*, *"aktifitas"* -> *"aktivitas"*), adding missing comma after sentence-initial conjunctions (*"Selain itu, ..."*).
   - **Recommendation**: Clean sentence with the minimal correction applied.
   - **Revision Reason**: Explicit citation of the specific KBBI or EYD V rule.

3. **`REVISI SUBSTANTIF`**:
   The sentence has an incomplete clause structure (e.g., subordinate conjunction opening without main clause), pleonasm, or severe machine-generated clichés (*"dalam era digitalisasi yang serba cepat ini"*).
   - **Recommendation**: Reconstructed formal sentence retaining 100% of the original factual meaning.
   - **Revision Reason**: Clear explanation of the structural defect and the de-cliché rationale.

4. **`PERLU VERIFIKASI`**:
   The sentence is truncated, missing contextual references, or structurally ambiguous.
   - **Recommendation**: Prompt the user/author to verify the complete sentence fragment.
   - **Revision Reason**: Insufficient syntactic context.

## 4. STRICT PROHIBITIONS (ZERO FALSE POSITIVE TOLERANCE)

The revision engine is strictly prohibited from:
1. Automatically replacing *"Selain itu"* with *"Di samping itu"*.
2. Automatically replacing *"Oleh karena itu"* with *"Oleh sebab itu"*.
3. Replacing *"dapat"* with *"bisa"*.
4. Inserting *"Secara substantif"* into sentences.
5. Adding commas before ordinary coordinating conjunctions (*"dan"*, *"atau"*) when joining only two coordinate elements.
6. Rewriting or paraphrasing a correct sentence merely to create stylistic variety.
7. Altering the meaning, intent, or factual assertion of the author.

## 5. AUDIT MATRIX SPECIFICATION (7 COLUMNS)

The output matrix produced for both the PDF report and dashboard must strictly follow:
1. **Nomor Kalimat (`No.`)**
2. **Naskah Asli**
3. **Karakteristik Temuan**
4. **Status Pemeriksaan** (`SUDAH BAIK`, `REVISI MINOR`, `REVISI SUBSTANTIF`, `PERLU VERIFIKASI`)
5. **Skor / Indikator Deteksi**
6. **Rekomendasi Naskah Baku KBBI**
7. **Alasan Revisi / Justifikasi EYD V**
