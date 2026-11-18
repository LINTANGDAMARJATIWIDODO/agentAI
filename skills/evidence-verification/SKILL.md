---
name: evidence-verification
description: Independent verification, model evaluation, uncertainty estimation, and false-positive prevention for AI text detection.
version: 1.0
---

# EVIDENCE VERIFICATION ENGINE

## MISSION

Validate all AI detection findings before producing the final report.

## VALIDATION PROCESS

1. Verify that the input text is sufficiently long (minimum 35 words and 2 sentences).
2. Identify the applicable document genre (academic, government regulation, executive report, technical manual).
3. Evaluate the reliability of the detection model.
4. Check whether the model has been tested on Indonesian text corpora.
5. Check whether the input resembles the model training distribution (Out-of-Distribution / OOD monitoring).
6. Compare independent analysis methods (statistical vs. linguistic vs. stylometric).
7. Identify contradictory findings and resolve conflicts objectively.
8. Estimate epistemic and aleatoric uncertainty.
9. Produce the final evidence report with transparent disclosures.

## MODEL EVALUATION

Track:
- Accuracy.
- Precision.
- Recall.
- F1-score.
- False Positive Rate (FPR).
- ROC-AUC.
- Expected Calibration Error (ECE).

Evaluate separately across:
- Academic writing.
- Business & government writing.
- Informal writing.
- Raw AI-generated writing.
- Human-edited AI writing.
- Human writing assisted by AI.

## STRICT RULES

- If evidence is insufficient, return **INCONCLUSIVE**.
- Never manufacture percentages or arbitrary consensus numbers.
- Never interpret model disagreement as proof of mixed authorship.
- Always disclose detection limitations: statistical likelihood is not categorical proof of physical authorship.
