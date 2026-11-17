"""
NEXUS AI ENTERPRISE — SMART MODEL ROUTER CLI DISPATCHER
Reads JSON payload from sys.stdin to execute AI chat requests, model listings,
and usage summaries securely without Windows shell escaping issues.
"""

import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.ai_router.model_router import SmartModelRouter
from services.ai_providers.provider_registry import ProviderRegistry
from services.ai_router.cost_tracker import CostTracker
from services.ai_router.budget_guard import BudgetGuard

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"status": "error", "message": "Empty stdin payload"}))
            sys.exit(1)

        payload = json.loads(raw_input)
        action = payload.get("action", "chat")
        
        router = SmartModelRouter()
        registry = ProviderRegistry()
        tracker = CostTracker()
        guard = BudgetGuard(tracker)

        if action == "chat":
            prompt = payload.get("prompt", "")
            system_prompt = payload.get("system_prompt", "")
            requested_model = payload.get("model")
            task_type = payload.get("task_type")
            temperature = payload.get("temperature", 0.7)
            max_tokens = payload.get("max_tokens", 2048)

            result = router.execute_with_fallback(
                prompt=prompt,
                system_prompt=system_prompt,
                requested_model=requested_model,
                task_type=task_type,
                temperature=temperature,
                max_tokens=max_tokens
            )
            print(json.dumps(result, ensure_ascii=False))

        elif action == "stream":
            prompt = payload.get("prompt", "")
            system_prompt = payload.get("system_prompt", "")
            requested_model = payload.get("model")
            task_type = payload.get("task_type")
            temperature = payload.get("temperature", 0.7)
            max_tokens = payload.get("max_tokens", 2048)

            for chunk_data in router.stream_with_fallback(
                prompt=prompt,
                system_prompt=system_prompt,
                requested_model=requested_model,
                task_type=task_type,
                temperature=temperature,
                max_tokens=max_tokens
            ):
                print(json.dumps(chunk_data, ensure_ascii=False), flush=True)

        elif action == "models":
            providers = registry.list_providers()
            pricing = registry.pricing_config
            print(json.dumps({
                "status": "success",
                "providers": providers,
                "pricing": pricing
            }, ensure_ascii=False))

        elif action == "usage":
            session = tracker.get_session_summary()
            today = tracker.get_today_usage()
            budget = guard.check_budget()
            print(json.dumps({
                "status": "success",
                "session_summary": session,
                "today_usage": today,
                "budget_status": budget
            }, ensure_ascii=False))

        else:
            print(json.dumps({
                "status": "error",
                "message": f"Unknown action '{action}'"
            }))

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()
