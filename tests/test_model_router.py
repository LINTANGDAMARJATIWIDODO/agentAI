"""
NEXUS AI ENTERPRISE — SMART MODEL ROUTER & AI PROVIDER TEST SUITE
Tests provider discovery, task classification, cost tracking, budget enforcement,
circuit breaker state management, and fallback execution.
"""

import unittest
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.ai_providers.provider_registry import ProviderRegistry
from services.ai_providers.gemini_provider import GeminiProvider
from services.ai_providers.openai_provider import OpenAIProvider
from services.ai_providers.claude_provider import ClaudeProvider
from services.ai_router.cost_tracker import CostTracker
from services.ai_router.budget_guard import BudgetGuard
from services.ai_router.model_router import SmartModelRouter

class TestSmartModelRouter(unittest.TestCase):
    def setUp(self):
        self.registry = ProviderRegistry()
        self.router = SmartModelRouter()
        self.tracker = CostTracker()
        self.guard = BudgetGuard(self.tracker)

    def test_provider_registry_loading(self):
        providers = self.registry.list_providers()
        self.assertIn("gemini", providers)
        self.assertIn("openai", providers)
        self.assertIn("anthropic", providers)
        self.assertTrue(providers["gemini"]["is_primary"])
        # Anthropic should be disabled by default
        self.assertFalse(providers["anthropic"]["is_enabled"])

    def test_task_classification(self):
        # Coding task
        code_prompt = "def calculate_hash(data: str) -> str: return hashlib.sha256(data.encode()).hexdigest()"
        self.assertEqual(self.router.classify_task(code_prompt), "CODING")

        # Document / SPBE task
        doc_prompt = "Audit pemenuhan regulasi Perpres 95/2018 untuk domain arsitektur SPBE"
        self.assertEqual(self.router.classify_task(doc_prompt), "DOCUMENT")

        # Complex reasoning
        reasoning_prompt = "Susun strategi komprehensif master blueprint dan roadmap 5 tahun C-Suite"
        self.assertEqual(self.router.classify_task(reasoning_prompt), "COMPLEX_REASONING")

        # Lightweight
        short_prompt = "Halo selamat pagi"
        self.assertEqual(self.router.classify_task(short_prompt), "LIGHTWEIGHT")

    def test_model_selection(self):
        prov, model = self.router.select_model("LIGHTWEIGHT")
        self.assertEqual(prov, "gemini")
        self.assertEqual(model, "gemini-2.0-flash-lite")

        prov, model = self.router.select_model("CODING")
        self.assertEqual(prov, "gemini")
        self.assertEqual(model, "gemini-2.0-flash")

    def test_cost_calculation(self):
        gemini = self.registry.get_provider("gemini")
        self.assertIsNotNone(gemini)
        # gemini-2.0-flash: $0.10/1M in, $0.40/1M out
        # 10,000 in tokens = $0.0010
        # 2,000 out tokens = $0.0008
        # total = $0.0018
        cost = gemini.calculate_cost("gemini-2.0-flash", 10000, 2000)
        self.assertAlmostEqual(cost, 0.0018, places=4)

    def test_circuit_breaker(self):
        gemini = self.registry.get_provider("gemini")
        gemini.record_success()
        self.assertFalse(gemini.is_circuit_tripped())

        # Simulate 3 failures
        gemini.record_failure()
        gemini.record_failure()
        gemini.record_failure()
        self.assertTrue(gemini.is_circuit_tripped())

        # Reset for subsequent tests
        gemini.record_success()
        self.assertFalse(gemini.is_circuit_tripped())

    def test_budget_guard(self):
        status = self.guard.check_budget()
        self.assertIn("can_proceed", status)
        self.assertIn("status", status)
        self.assertIn("current_spent_usd", status)
        self.assertIn("daily_limit_usd", status)

    def test_router_execution_with_cost_tracking(self):
        initial_calls = self.tracker.session_calls
        res = self.router.execute_with_fallback(
            prompt="Periksa kepatuhan arsitektur layanan SPBE",
            task_type="DOCUMENT"
        )
        self.assertIn("status", res)
        self.assertIn("provider", res)
        self.assertIn("cost_usd", res)
        self.assertGreater(self.tracker.session_calls, initial_calls)

    def test_claude_disabled_by_default(self):
        claude = self.registry.get_provider("anthropic")
        res = claude.generate(prompt="Test claude prompt")
        self.assertEqual(res["status"], "disabled")
        self.assertIn("disabled by default", res["error"])

    def test_chat_streaming(self):
        chunks = []
        for item in self.router.stream_with_fallback(prompt="Streaming test query"):
            chunks.append(item)

        self.assertGreater(len(chunks), 1)
        final_chunk = chunks[-1]
        self.assertTrue(final_chunk["done"])
        self.assertIn("cost_usd", final_chunk)
        self.assertIn("full_text", final_chunk)

if __name__ == "__main__":
    unittest.main()
