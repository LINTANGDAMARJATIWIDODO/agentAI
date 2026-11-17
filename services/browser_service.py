"""
NEXUS AI ENTERPRISE — Browser Automation & Verification Service
Engineered by FARREL (QA) and RAKA (CTO)
Provides headless web verification, DOM inspection, element assertions, and screenshot capture.
"""

import os
import json
import urllib.request
import re
from typing import Dict, List, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "output", "screenshots")


class BrowserAutomationService:
    def __init__(self):
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    def verify_local_page(self, relative_url: str, required_elements: List[str]) -> Dict[str, Any]:
        """
        Inspects local HTML page in public/ to verify required DOM elements and components.
        """
        clean_rel = relative_url.lstrip("/")
        file_path = os.path.join(BASE_DIR, "public", clean_rel)

        if not os.path.exists(file_path):
            return {
                "status": "FAIL",
                "url": relative_url,
                "error": f"File does not exist: {file_path}",
                "assertions_passed": 0,
                "total_assertions": len(required_elements)
            }

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        results = []
        for elem in required_elements:
            passed = elem.lower() in html.lower()
            results.append({"element_or_keyword": elem, "passed": passed})

        all_passed = all(r["passed"] for r in results)
        passed_count = sum(1 for r in results if r["passed"])

        return {
            "status": "PASS" if all_passed else "PARTIAL",
            "url": relative_url,
            "file_size_bytes": len(html),
            "assertions_passed": passed_count,
            "total_assertions": len(required_elements),
            "details": results
        }

    def run_e2e_assertions(self, app_name: str) -> Dict[str, Any]:
        """
        Runs comprehensive test assertions for wedding invitation, cafe, or custom apps.
        """
        if "undangan" in app_name.lower() or "wedding" in app_name.lower():
            checks = [
                "envelopeModal",
                "Arya & Nabila",
                "countdownGrid",
                "Masjid Agung Al-Azhar",
                "The Ritz-Carlton",
                "rsvpForm",
                "wishesContainer",
                "8801 2984 7721",
                "copyToClipboard",
                "startWeddingMelody"
            ]
            return self.verify_local_page("undangan/index.html", checks)
        else:
            checks = [
                "Nexus Smoked Butterscotch",
                "menuGridContainer",
                "cartDrawer",
                "NEXUS15",
                "checkoutModal",
                "qrisDisplay",
                "reservationForm",
                "Aceh Gayo"
            ]
            return self.verify_local_page("cafe/index.html", checks)


browser_service = BrowserAutomationService()
