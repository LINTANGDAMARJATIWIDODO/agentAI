"""
NEXUS AI ENTERPRISE — BASE AI PROVIDER ADAPTER
Abstract base class defining the unified interface for all multi-model providers
(Gemini, OpenAI, Claude, Local/Offline Mock).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time

class BaseAIProvider(ABC):
    def __init__(self, provider_id: str, config: Dict[str, Any]):
        self.provider_id = provider_id
        self.config = config
        self.is_enabled = config.get("is_enabled", True)
        self.is_primary = config.get("is_primary", False)
        self.models_config = config.get("models", {})
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.circuit_open = False

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if provider has necessary API keys and configuration."""
        pass

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        model_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def stream_generate(
        self,
        prompt: str,
        system_prompt: str = "",
        model_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        tools: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Yields streaming dictionary chunks:
        {"chunk": str, "done": False}
        and finishes with:
        {"chunk": "", "done": True, "input_tokens": int, "output_tokens": int, "cost_usd": float, "latency_ms": float}
        """
        pass

    def estimate_tokens(self, text: str) -> int:
        """Heuristic token estimator: approx 4 characters per token for English/Code, 2.5 for Indonesian."""
        if not text:
            return 0
        return max(1, int(len(text) / 3.5))

    def calculate_cost(self, model_id: str, input_tokens: int, output_tokens: int) -> float:
        """Calculates USD cost based on configured rates per 1M tokens."""
        m_cfg = self.models_config.get(model_id, {})
        in_rate = m_cfg.get("input_cost_per_1m", 0.10)
        out_rate = m_cfg.get("output_cost_per_1m", 0.40)
        cost = (input_tokens / 1_000_000.0) * in_rate + (output_tokens / 1_000_000.0) * out_rate
        return round(cost, 7)

    def record_success(self):
        self.failure_count = 0
        self.circuit_open = False

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= 3:
            self.circuit_open = True

    def is_circuit_tripped(self, cooldown_seconds: float = 60.0) -> bool:
        if not self.circuit_open:
            return False
        if time.time() - self.last_failure_time > cooldown_seconds:
            # Half-open state: allow a retry
            self.circuit_open = False
            return False
        return True

    def health_check(self) -> Dict[str, Any]:
        start = time.time()
        available = self.is_available()
        return {
            "provider": self.provider_id,
            "available": available,
            "circuit_open": self.is_circuit_tripped(),
            "failure_count": self.failure_count,
            "latency_ms": round((time.time() - start) * 1000, 2)
        }
