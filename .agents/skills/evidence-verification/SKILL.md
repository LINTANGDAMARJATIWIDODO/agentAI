---
name: evidence-verification
description: Independent verification, model evaluation, uncertainty estimation, and false-positive prevention for AI text detection.
version: 1.0
---

# EVIDENCE VERIFICATION ENGINE

## MISSION

Validate all AI detection findings before producing the final report.

## VALIDATION PROCESS

1. Verify that the input text is sufficiently long.
2. Identify the applicable document genre.
3. Evaluate the reliability of the detection model.
4. Check whether the model has been tested on Indonesian text.
5. Check whether the input resembles the model training distribution.
6. Compare independent analysis methods.
7. Identify contradictory findings.
8. Estimate uncertainty.
9. Produce the final evidence report.

## MODEL EVALUATION

Track:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- False Positive Rate.
- ROC-AUC.
- Calibration Error.

Evaluate separately across:
- Academic writing.
- Business writing.
- Informal writing.
- AI-generated writing.
- Human-edited AI writing.
- Human writing assisted by AI.

## STRICT RULE

If evidence is insufficient, return INCONCLUSIVE.

Never manufacture percentages.

Never interpret model disagreement as proof of mixed authorship.

Always disclose detection limitations.
