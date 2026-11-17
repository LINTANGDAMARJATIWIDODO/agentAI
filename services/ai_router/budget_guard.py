"""
NEXUS AI ENTERPRISE — BUDGET GUARD & HARD STOP ENFORCER
Protects enterprise infrastructure from cost overruns and uncontrolled token consumption.
"""

import os
import json
from typing import Dict, Any, Tuple
from services.ai_router.cost_tracker import CostTracker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRICING_FILE = os.path.join(BASE_DIR, "config", "model_pricing.json")

class BudgetGuard:
    def __init__(self, cost_tracker: CostTracker):
        self.tracker = cost_tracker
        self.config = self._load_budget_config()
        self.daily_limit = self.config.get("daily_limit_usd", 5.0)
        self.warning_threshold = self.config.get("warning_threshold_usd", 3.5)
        self.hard_stop_enabled = self.config.get("hard_stop_enabled", True)

    def _load_budget_config(self) -> Dict[str, Any]:
        if os.path.exists(PRICING_FILE):
            try:
                with open(PRICING_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("budget", {})
            except Exception:
                pass
        return {}

    def check_budget(self) -> Dict[str, Any]:
        today_usage = self.tracker.get_today_usage()
        current_spent = today_usage["cost_usd"]
        remaining = max(0.0, self.daily_limit - current_spent)

        if current_spent >= self.daily_limit:
            if self.hard_stop_enabled:
                return {
                    "can_proceed": False,
                    "status": "HARD_STOP",
                    "current_spent_usd": current_spent,
                    "daily_limit_usd": self.daily_limit,
                    "remaining_usd": 0.0,
                    "message": f"Daily AI budget limit (${self.daily_limit:.2f}) reached! Hard stop active."
                }
            else:
                return {
                    "can_proceed": True,
                    "status": "OVER_BUDGET_SOFT",
                    "current_spent_usd": current_spent,
                    "daily_limit_usd": self.daily_limit,
                    "remaining_usd": 0.0,
                    "message": "Daily budget exceeded, running under soft allowance."
                }
        elif current_spent >= self.warning_threshold:
            return {
                "can_proceed": True,
                "status": "WARNING",
                "current_spent_usd": current_spent,
                "daily_limit_usd": self.daily_limit,
                "remaining_usd": round(remaining, 4),
                "message": f"Approaching daily budget limit (${current_spent:.2f} of ${self.daily_limit:.2f})."
            }
        else:
            return {
                "can_proceed": True,
                "status": "OK",
                "current_spent_usd": current_spent,
                "daily_limit_usd": self.daily_limit,
                "remaining_usd": round(remaining, 4),
                "message": "Budget healthy."
            }
