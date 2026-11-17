"""
NEXUS AI ENTERPRISE — SMART MODEL ROUTER
Directs incoming AI prompts to the optimal model based on cost, task domain,
context requirements, latency targets, and fallback circuit status.
"""

import os
import re
from typing import Dict, Any, List, Optional, Tuple
from services.ai_providers.provider_registry import ProviderRegistry
from services.ai_router.cost_tracker import CostTracker
from services.ai_router.budget_guard import BudgetGuard

class SmartModelRouter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SmartModelRouter, cls).__new__(cls)
            cls._instance._init_router()
        return cls._instance

    def _init_router(self):
        self.registry = ProviderRegistry()
        self.tracker = CostTracker()
        self.guard = BudgetGuard(self.tracker)

    def classify_task(self, prompt: str) -> str:
        """Classifies the task domain to pick the most cost-effective capable model."""
        prompt_lower = prompt.lower()
        
        # Coding keywords
        coding_kw = ["def ", "class ", "function", "javascript", "python", "html", "css", "bug", "terminal", "powershell", "regex", "api endpoint"]
        if any(kw in prompt_lower for kw in coding_kw):
            return "CODING"
            
        # Document & SPBE keywords
        doc_kw = ["spbe", "perpres", "permenpanrb", "audit", "rekap", "excel", "docx", "arsitektur", "domain", "indikator"]
        if any(kw in prompt_lower for kw in doc_kw):
            return "DOCUMENT"
            
        # Complex multi-step reasoning keywords
        complex_kw = ["strategi", "master blueprint", "roadmap", "evaluasi komprehensif", "tobe", "gap analysis", "anggaran rab", "c-suite"]
        if any(kw in prompt_lower for kw in complex_kw):
            return "COMPLEX_REASONING"
            
        # Default / Lightweight
        if len(prompt.split()) < 30:
            return "LIGHTWEIGHT"
            
        return "GENERAL"

    def select_model(self, task_type: str, requested_model: Optional[str] = None) -> Tuple[str, str]:
        """
        Returns (provider_id, model_id) optimized for cost and task capability.
        """
        if requested_model:
            provider = self.registry.get_provider_for_model(requested_model)
            if provider and not provider.is_circuit_tripped():
                return provider.provider_id, requested_model

        # Smart cost-based selection
        if task_type == "LIGHTWEIGHT":
            # Lowest cost
            return "gemini", "gemini-2.0-flash-lite"
        elif task_type == "CODING":
            return "gemini", "gemini-2.0-flash"
        elif task_type == "DOCUMENT":
            return "gemini", "gemini-2.0-flash"
        elif task_type == "COMPLEX_REASONING":
            # For complex reasoning: Gemini 1.5 Pro or Gemini 2.0 Flash
            return "gemini", "gemini-2.0-flash"
        else:
            return "gemini", "gemini-2.0-flash"

    def execute_with_fallback(
        self,
        prompt: str,
        system_prompt: str = "",
        requested_model: Optional[str] = None,
        task_type: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Executes generation with automatic classification, budget enforcement,
        cost tracking, and circuit-breaker fallback.
        """
        # 1. Budget check
        budget_status = self.guard.check_budget()
        if not budget_status["can_proceed"]:
            return {
                "provider": "system",
                "model": "budget_guard",
                "text": f"MOHON MAAF: {budget_status['message']}",
                "tool_calls": [],
                "input_tokens": 0,
                "output_tokens": 0,
                "cost_usd": 0.0,
                "latency_ms": 0.0,
                "status": "blocked_by_budget",
                "budget_info": budget_status,
                "error": "Daily budget hard stop active"
            }

        # 2. Determine task type & model
        determined_task = task_type or self.classify_task(prompt)
        provider_id, model_id = self.select_model(determined_task, requested_model)
        
        provider = self.registry.get_provider(provider_id)
        
        # 3. Attempt Primary Provider
        if provider and not provider.is_circuit_tripped():
            res = provider.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                model_id=model_id,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools
            )
            
            if res.get("status") == "success":
                self.tracker.log_call(
                    provider=provider_id,
                    model=model_id,
                    task_type=determined_task,
                    input_tokens=res.get("input_tokens", 0),
                    output_tokens=res.get("output_tokens", 0),
                    cost_usd=res.get("cost_usd", 0.0),
                    latency_ms=res.get("latency_ms", 0.0),
                    status="success"
                )
                res["task_type"] = determined_task
                res["fallback_triggered"] = False
                return res

        # 4. Fallback Triggered (OpenAI secondary)
        openai_provider = self.registry.get_provider("openai")
        if openai_provider and not openai_provider.is_circuit_tripped():
            fallback_model = "gpt-4o-mini"
            res = openai_provider.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                model_id=fallback_model,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools
            )
            self.tracker.log_call(
                provider="openai",
                model=fallback_model,
                task_type=determined_task,
                input_tokens=res.get("input_tokens", 0),
                output_tokens=res.get("output_tokens", 0),
                cost_usd=res.get("cost_usd", 0.0),
                latency_ms=res.get("latency_ms", 0.0),
                status=res.get("status", "fallback")
            )
            res["task_type"] = determined_task
            res["fallback_triggered"] = True
            res["primary_provider_failed"] = provider_id
            return res

        # 5. Safe Local Offline Fallback
        return {
            "provider": "nexus_local",
            "model": "offline_safety_fallback",
            "text": f"[NEXUS OFFLINE FALLBACK]\nInstruksi: {prompt[:120]}...\nSemua provider online tidak merespon, sistem menjaga stabilitas lokal.",
            "tool_calls": [],
            "input_tokens": 10,
            "output_tokens": 20,
            "cost_usd": 0.0,
            "latency_ms": 5.0,
            "status": "offline_fallback",
            "task_type": determined_task,
            "fallback_triggered": True,
            "error": "All external providers offline or circuit-tripped"
        }

    def stream_with_fallback(
        self,
        prompt: str,
        system_prompt: str = "",
        requested_model: Optional[str] = None,
        task_type: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        tools: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Yields real-time streaming chunks with automatic classification, budget enforcement,
        cost tracking, and circuit-breaker fallback.
        """
        budget_status = self.guard.check_budget()
        if not budget_status["can_proceed"]:
            yield {
                "chunk": f"MOHON MAAF: {budget_status['message']}",
                "done": True,
                "status": "blocked_by_budget"
            }
            return

        determined_task = task_type or self.classify_task(prompt)
        provider_id, model_id = self.select_model(determined_task, requested_model)
        provider = self.registry.get_provider(provider_id)

        if provider and not provider.is_circuit_tripped():
            for item in provider.stream_generate(
                prompt=prompt,
                system_prompt=system_prompt,
                model_id=model_id,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools
            ):
                if item.get("done"):
                    self.tracker.log_call(
                        provider=provider_id,
                        model=model_id,
                        task_type=determined_task,
                        input_tokens=item.get("input_tokens", 0),
                        output_tokens=item.get("output_tokens", 0),
                        cost_usd=item.get("cost_usd", 0.0),
                        latency_ms=item.get("latency_ms", 0.0),
                        status="success"
                    )
                yield item
            return

        # Fallback to OpenAI
        openai_provider = self.registry.get_provider("openai")
        if openai_provider and not openai_provider.is_circuit_tripped():
            fallback_model = "gpt-4o-mini"
            for item in openai_provider.stream_generate(
                prompt=prompt,
                system_prompt=system_prompt,
                model_id=fallback_model,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools
            ):
                if item.get("done"):
                    self.tracker.log_call(
                        provider="openai",
                        model=fallback_model,
                        task_type=determined_task,
                        input_tokens=item.get("input_tokens", 0),
                        output_tokens=item.get("output_tokens", 0),
                        cost_usd=item.get("cost_usd", 0.0),
                        latency_ms=item.get("latency_ms", 0.0),
                        status="fallback"
                    )
                yield item
            return

        # Local offline fallback chunk
        yield {
            "chunk": f"[OFFLINE FALLBACK] {prompt[:100]}...",
            "done": True,
            "status": "offline_fallback"
        }
