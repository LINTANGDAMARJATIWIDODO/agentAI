"""
NEXUS AI ENTERPRISE — PROVIDER REGISTRY
Central factory and discovery service for all configured AI providers.
"""

import os
import json
from typing import Dict, Any, Optional
from services.ai_providers.base_provider import BaseAIProvider
from services.ai_providers.gemini_provider import GeminiProvider
from services.ai_providers.openai_provider import OpenAIProvider
from services.ai_providers.claude_provider import ClaudeProvider

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRICING_FILE = os.path.join(BASE_DIR, "config", "model_pricing.json")

class ProviderRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProviderRegistry, cls).__new__(cls)
            cls._instance._init_registry()
        return cls._instance

    def _init_registry(self):
        self.pricing_config = self._load_pricing()
        self.providers: Dict[str, BaseAIProvider] = {}
        
        providers_cfg = self.pricing_config.get("providers", {})
        if "gemini" in providers_cfg:
            self.providers["gemini"] = GeminiProvider(providers_cfg["gemini"])
        if "openai" in providers_cfg:
            self.providers["openai"] = OpenAIProvider(providers_cfg["openai"])
        if "anthropic" in providers_cfg:
            self.providers["anthropic"] = ClaudeProvider(providers_cfg["anthropic"])

    def _load_pricing(self) -> Dict[str, Any]:
        if os.path.exists(PRICING_FILE):
            try:
                with open(PRICING_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARN] Error loading model pricing config: {e}")
        return {}

    def get_provider(self, provider_id: str) -> Optional[BaseAIProvider]:
        return self.providers.get(provider_id)

    def get_provider_for_model(self, model_id: str) -> Optional[BaseAIProvider]:
        for p_id, provider in self.providers.items():
            if model_id in provider.models_config:
                return provider
        return None

    def list_providers(self) -> Dict[str, Any]:
        status_map = {}
        for p_id, provider in self.providers.items():
            status_map[p_id] = {
                "display_name": provider.config.get("display_name", p_id),
                "is_primary": provider.is_primary,
                "is_enabled": provider.is_enabled,
                "is_available": provider.is_available(),
                "circuit_tripped": provider.is_circuit_tripped(),
                "models": list(provider.models_config.keys())
            }
        return status_map

    def get_model_spec(self, model_id: str) -> Optional[Dict[str, Any]]:
        for provider in self.providers.values():
            if model_id in provider.models_config:
                spec = dict(provider.models_config[model_id])
                spec["provider"] = provider.provider_id
                return spec
        return None
