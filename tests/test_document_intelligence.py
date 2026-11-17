"""
NEXUS AI ENTERPRISE — DOCUMENT INTELLIGENCE & AI HUMANIZER TEST SUITE
Tests PDF text extraction, robotic AI marker detection,
human-grade paraphrasing, and styled DOCX export.
"""

import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.document_intelligence.pdf_extractor import pdf_extractor
from services.document_intelligence.ai_humanizer import ai_humanizer

class TestDocumentIntelligence(unittest.TestCase):
    def setUp(self):
        self.sample_ai_text = (
            "Dalam era digitalisasi yang serba cepat ini, transformasi teknologi memainkan peran yang sangat penting dalam "
            "pelayanan publik. Tidak dapat dipungkiri bahwa integrasi sistem informasi merupakan hal yang sangat krusial. "
            "Penting untuk dicatat bahwa seiring dengan perkembangan zaman, instansi pemerintah harus menyelami lebih dalam "
            "penerapan arsitektur SPBE. Dengan demikian, dapat dipahami bahwa keberhasilan digitalisasi merupakan bukti nyata bahwa "
            "reformasi birokrasi telah berjalan secara holistik dan komprehensif. Dapat disimpulkan bahwa inovasi adalah kuncinya."
        )

    def test_01_detect_ai_markers(self):
        res = ai_humanizer.detect_ai_markers(self.sample_ai_text)
        self.assertIn("ai_score_percentage", res)
        self.assertGreaterEqual(res["ai_score_percentage"], 50.0)
        self.assertGreater(res["total_markers_detected"], 5)
        self.assertIn("ROBOTIK", res["classification"])

    def test_02_humanize_and_rephrase(self):
        res = ai_humanizer.humanize_and_rephrase(self.sample_ai_text)
        self.assertEqual(res["status"], "success")
        self.assertIn("humanized_text", res)
        
        # Verify cliches are eliminated
        humanized = res["humanized_text"].lower()
        self.assertNotIn("dalam era digitalisasi yang serba cepat ini", humanized)
        self.assertNotIn("tidak dapat dipungkiri bahwa", humanized)
        self.assertNotIn("secara holistik dan komprehensif", humanized)
        
        # Verify AI score significantly dropped
        before_score = res["before_metrics"]["ai_score_percentage"]
        after_score = res["after_metrics"]["ai_score_percentage"]
        self.assertLess(after_score, before_score)

    def test_03_generate_docx_export(self):
        h_res = ai_humanizer.humanize_and_rephrase(self.sample_ai_text)
        filename = ai_humanizer.generate_humanized_docx(
            original_text=self.sample_ai_text,
            humanized_text=h_res["humanized_text"],
            doc_title="TEST_HUMANIZED_DOC",
            markers_info=h_res
        )
        self.assertTrue(filename.endswith(".docx"))
        full_path = os.path.join(BASE_DIR, "public", "downloads", filename)
        self.assertTrue(os.path.exists(full_path))
        self.assertGreater(os.path.getsize(full_path), 5000)

    def test_04_pdf_extractor_graceful_missing(self):
        res = pdf_extractor.extract_from_path("non_existent_file.pdf")
        self.assertEqual(res["status"], "error")
        self.assertIn("tidak ditemukan", res["message"])

if __name__ == "__main__":
    unittest.main()
