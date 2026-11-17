"""
NEXUS AI ENTERPRISE — COST TRACKER & USAGE ANALYTICS
Tracks token usage, computes real-time micro-costs in USD & IDR,
and persists usage logs for auditing and budget enforcement.
"""

import os
import json
import time
from typing import Dict, Any, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRICING_FILE = os.path.join(BASE_DIR, "config", "model_pricing.json")
LOG_DIR = os.path.join(BASE_DIR, "logs")
USAGE_LOG_FILE = os.path.join(LOG_DIR, "ai_usage.jsonl")

class CostTracker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CostTracker, cls).__new__(cls)
            cls._instance._init_tracker()
        return cls._instance

    def _init_tracker(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        self.pricing = self._load_pricing()
        self.exchange_rate = self.pricing.get("exchange_rate_usd_idr", 16250.0)
        self.session_calls = 0
        self.session_input_tokens = 0
        self.session_output_tokens = 0
        self.session_cost_usd = 0.0

    def _load_pricing(self) -> Dict[str, Any]:
        if os.path.exists(PRICING_FILE):
            try:
                with open(PRICING_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def log_call(
        self,
        provider: str,
        model: str,
        task_type: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        latency_ms: float,
        status: str = "success"
    ) -> Dict[str, Any]:
        cost_idr = round(cost_usd * self.exchange_rate, 2)
        
        self.session_calls += 1
        self.session_input_tokens += input_tokens
        self.session_output_tokens += output_tokens
        self.session_cost_usd += cost_usd

        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "provider": provider,
            "model": model,
            "task_type": task_type,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost_usd": cost_usd,
            "cost_idr": cost_idr,
            "latency_ms": latency_ms,
            "status": status
        }

        try:
            with open(USAGE_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[WARN] Failed to write usage log: {e}")

        return entry

    def get_session_summary(self) -> Dict[str, Any]:
        return {
            "total_calls": self.session_calls,
            "total_input_tokens": self.session_input_tokens,
            "total_output_tokens": self.session_output_tokens,
            "total_tokens": self.session_input_tokens + self.session_output_tokens,
            "total_cost_usd": round(self.session_cost_usd, 5),
            "total_cost_idr": round(self.session_cost_usd * self.exchange_rate, 2)
        }

    def get_today_usage(self) -> Dict[str, Any]:
        """Calculates today's cumulative usage from the log file."""
        today_str = time.strftime("%Y-%m-%d", time.gmtime())
        calls = 0
        in_tok = 0
        out_tok = 0
        cost_usd = 0.0

        if os.path.exists(USAGE_LOG_FILE):
            try:
                with open(USAGE_LOG_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        rec = json.loads(line)
                        if rec.get("timestamp", "").startswith(today_str):
                            calls += 1
                            in_tok += rec.get("input_tokens", 0)
                            out_tok += rec.get("output_tokens", 0)
                            cost_usd += rec.get("cost_usd", 0.0)
            except Exception:
                pass

        return {
            "date": today_str,
            "calls": calls,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "total_tokens": in_tok + out_tok,
            "cost_usd": round(cost_usd, 5),
            "cost_idr": round(cost_usd * self.exchange_rate, 2)
        }
