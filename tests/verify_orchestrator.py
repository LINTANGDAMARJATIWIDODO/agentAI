import sys, os
sys.path.insert(0, r"C:\Users\LENOVO\.gemini\antigravity\scratch\NEXUS-AI-ENTERPRISE")
from orchestrator import NexusOrchestrator

orch = NexusOrchestrator()
print(f"Orchestrator loaded {len(orch.agents_config)} employees successfully:")
for a in orch.agents_config:
    print(f" - [{a['id']}] {a['name']} ({a['title']}) | Level {a['competency_tier']['level']} (Score: {a['competency_tier']['score_average']})")
