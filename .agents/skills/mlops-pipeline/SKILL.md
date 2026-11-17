---
name: mlops-pipeline
description: Operationalize, deploy, monitor, and govern AI/ML models and LLM agent chains. Implement model versioning, prompt management, evaluation benchmarks, and latency/drift monitoring. Use when operationalizing AI/ML services.
---

# SKILL: Enterprise MLOps & LLM Systems Governance

> **Origin Repository:** https://github.com/j4flmao/agent-skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `agent-skills` (j4flmao) AI/ML & Agent Systems category.  
> **Target Owner:** RAKA (Director of Technology & Engineering)

---

## 1. PURPOSE & OBJECTIVE
To provide a production-grade framework for versioning, evaluating, serving, monitoring, and governing machine learning models and large language model (LLM) agent chains in corporate environments.

## 2. SCOPE
- Model artifact tracking (MLflow, Weights & Biases), prompt versioning, automated evaluation harnesses, LLM inference latency optimization (quantization, vLLM, TensorRT-LLM), and data/concept drift detection.

## 3. CORE MLOPS WORKFLOW
```
[Data Ingestion & Feature Engineering] -> [Model Training / Fine-Tuning]
                   |
                   v
[Evaluation Benchmark & Safety Red-Teaming] -> [Model Registry & Versioning]
                   |
                   v
[Canary Inference Deployment] -> [Observability & Drift Telemetry]
```

## 4. STEP-BY-STEP PROCEDURE
1. **Model & Prompt Tracking:** Version all model checkpoints, weights, and system prompts alongside commit hashes.
2. **Automated Evaluation Suite:** Run benchmark test datasets measuring accuracy, F1-score, latency, and hallucination rate prior to deployment.
3. **Inference Serving Topology:** Deploy models using high-throughput engines with continuous batching and PagedAttention.
4. **Token Cost & Latency Guardrails:** Enforce hard timeouts and maximum token limits per agent inference request.
5. **Continuous Telemetry:** Monitor token throughput, cost per query, latency percentiles, and semantic drift.

## 5. QUALITY STANDARDS & METRICS
- All production models must pass automated regression evals before serving live traffic.
- Inference server autoscaling based on queue depth and GPU memory utilization.

## 6. CONSTRAINTS & SECURITY RULES
- Never feed unredacted customer PII into external commercial LLM APIs without enterprise data isolation agreements.
- Implement guardrails preventing prompt injection and jailbreak attacks.
