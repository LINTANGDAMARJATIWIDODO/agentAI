"""
NEXUS AI ENTERPRISE — SPBE CONSULTANT KNOWLEDGE ENGINE TEST SUITE
Automated unit & integration tests for Regulatory Intelligence, Ontology,
Consulting Repository, 12-Step Reasoning Workflow, QA Agent, and Hybrid Retriever.
"""

import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.spbe_knowledge_engine import (
    portal_connectors,
    regulatory_intelligence,
    spbe_ontology,
    consulting_repository,
    spbe_reasoning_engine,
    spbe_qa_agent,
    spbe_retriever
)


class TestSPBEKnowledgeEngine(unittest.TestCase):

    # ==========================================================
    # 1. REGULATORY INTELLIGENCE TESTS
    # ==========================================================
    def test_01_regulatory_active_status(self):
        res_95 = regulatory_intelligence.verify_legal_status("PERPRES_95_2018")
        self.assertEqual(res_95["status"], "FOUND")
        self.assertEqual(res_95["legal_status"], "BERLAKU")
        self.assertTrue(res_95["is_valid_baseline"])

        res_132 = regulatory_intelligence.verify_legal_status("PERPRES_132_2022")
        self.assertEqual(res_132["legal_status"], "BERLAKU")
        self.assertTrue(res_132["is_valid_baseline"])

    def test_02_regulatory_revoked_rejection(self):
        res_rev = regulatory_intelligence.verify_legal_status("PERPRES_XX_HISTORICAL_SAMPLE")
        self.assertEqual(res_rev["status"], "FOUND")
        self.assertEqual(res_rev["legal_status"], "DICABUT")
        self.assertFalse(res_rev["is_valid_baseline"])
        self.assertIsNotNone(res_rev["revocation_warning"])

    def test_03_regulatory_article_extraction(self):
        art_res = regulatory_intelligence.get_article("PERPRES_132_2022", "6", "1")
        self.assertEqual(art_res["status"], "SUCCESS")
        self.assertIn("6 (enam) domain arsitektur", art_res["text"])
        self.assertIn("Peraturan Presiden No. 132/2022 Pasal 6 ayat (1)", art_res["citation"])

    # ==========================================================
    # 2. SPBE ONTOLOGY TESTS
    # ==========================================================
    def test_04_ontology_node_and_edge(self):
        trace = spbe_ontology.trace_architecture_path("FUNC_TRANTIBUM")
        self.assertEqual(trace["function"]["name"], "Penyelenggaraan Ketenteraman dan Ketertiban Umum (Trantibum)")
        self.assertTrue(len(trace["processes"]) > 0)
        self.assertTrue(len(trace["services"]) > 0)
        self.assertTrue(len(trace["applications"]) > 0)
        self.assertTrue(len(trace["evidence_chain"]) >= 3)

    # ==========================================================
    # 3. CONSULTING REPOSITORY TESTS
    # ==========================================================
    def test_05_consulting_rab_hierarchy(self):
        rab_levels = consulting_repository.get_rab_level_hierarchy()
        self.assertEqual(len(rab_levels), 7)
        self.assertEqual(rab_levels[0]["level"], 1)
        self.assertEqual(rab_levels[6]["level"], 7)
        self.assertIn("BSrE", rab_levels[6]["description"])

    def test_06_consulting_terminology(self):
        term = consulting_repository.lookup_term("Interoperabilitas Data")
        self.assertIsNotNone(term)
        self.assertEqual(term["term"], "Interoperabilitas Data")
        self.assertIn("Perpres No. 39 Tahun 2019", term["legal_source"])

    # ==========================================================
    # 4. 12-STEP REASONING WORKFLOW TESTS
    # ==========================================================
    def test_07_reasoning_12_step_workflow(self):
        adv_res = spbe_reasoning_engine.execute_12_step_advisory(
            opd_name="Satuan Polisi Pamong Praja",
            domain_scope=["Proses Bisnis", "Layanan", "Aplikasi", "Data & Informasi"],
            evidence_inputs={
                "has_3c_file": True,
                "total_rows_audited": 12,
                "missing_rows_count": 5
            }
        )
        self.assertEqual(adv_res["findings_count"], 12)
        breakdown = adv_res["epistemic_breakdown"]
        self.assertTrue(breakdown["VERIFIED_FACT"] >= 2)
        self.assertTrue(breakdown["SOURCE_EVIDENCE"] >= 2)
        self.assertTrue(breakdown["RECOMMENDATION"] >= 2)

    # ==========================================================
    # 5. SPBE QA AGENT TESTS
    # ==========================================================
    def test_08_qa_agent_valid_report(self):
        adv_res = spbe_reasoning_engine.execute_12_step_advisory(
            opd_name="Satuan Polisi Pamong Praja",
            domain_scope=["Proses Bisnis", "Aplikasi"],
            evidence_inputs={"has_3c_file": True, "total_rows_audited": 10, "missing_rows_count": 2}
        )
        qa_result = spbe_qa_agent.audit_consulting_report(adv_res)
        self.assertEqual(qa_result["qa_status"], "PASS")
        self.assertEqual(qa_result["issues_count"], 0)
        self.assertIn("100", qa_result["evidence_sufficiency_score"])

    def test_09_qa_agent_flags_revoked_law(self):
        bad_report = {
            "findings": [
                {
                    "step": 1,
                    "category": "SOURCE_EVIDENCE",
                    "statement": "Merujuk pada Contoh Regulasi Lampau yang Telah Dicabut (PERPRES_XX).",
                    "evidence": "PERPRES_XX_HISTORICAL_SAMPLE"
                }
            ]
        }
        qa_result = spbe_qa_agent.audit_consulting_report(bad_report)
        self.assertEqual(qa_result["qa_status"], "WARNING")
        self.assertEqual(qa_result["metrics"]["revoked_regulations_detected"], 1)

    # ==========================================================
    # 6. HYBRID KNOWLEDGE RETRIEVER TESTS
    # ==========================================================
    def test_10_hybrid_retrieval(self):
        ret_res = spbe_retriever.hybrid_search("Arsitektur SPBE", domain_filter="PROSES_BISNIS")
        self.assertTrue(ret_res["results_summary"]["regulations_found"] > 0)
        self.assertIsNotNone(ret_res["glossary_definition"])

    # ==========================================================
    # 7. OFFICIAL PORTAL CONNECTORS & EXPANDED REGULATIONS TESTS
    # ==========================================================
    def test_11_portal_connectors_registry(self):
        portals = portal_connectors.list_portals()
        portal_ids = [p["id"] for p in portals]
        self.assertIn("JDIH_PANRB", portal_ids)
        self.assertIn("BPK_PERATURAN", portal_ids)
        self.assertIn("JDIH_SETNEG", portal_ids)
        self.assertIn("JDIHN", portal_ids)
        self.assertIn("KOMDIGI", portal_ids)

        # Authenticity verification
        auth_gov = portal_connectors.verify_source_authenticity("https://jdih.menpan.go.id/dokumen-hukum/971")
        self.assertTrue(auth_gov["is_authoritative_government_source"])
        self.assertEqual(auth_gov["status"], "TRUSTED_PRIMARY_SOURCE")

        auth_fake = portal_connectors.verify_source_authenticity("https://blog-spbe-seo-random.com/artikel")
        self.assertFalse(auth_fake["is_authoritative_government_source"])
        self.assertEqual(auth_fake["status"], "REJECTED_UNOFFICIAL_SOURCE")

    def test_12_new_regulations_status_and_articles(self):
        # Perpres 82/2023 (GovTech INA Digital)
        res_82 = regulatory_intelligence.verify_legal_status("PERPRES_82_2023")
        self.assertEqual(res_82["legal_status"], "BERLAKU")
        art_82 = regulatory_intelligence.get_article("PERPRES_82_2023", "3", "1")
        self.assertIn("9 (sembilan) layanan prioritas", art_82["text"])

        # Perpres 83/2025 (Komite Percepatan Transformasi Digital)
        res_83 = regulatory_intelligence.verify_legal_status("PERPRES_83_2025")
        self.assertEqual(res_83["legal_status"], "BERLAKU")

        # PermenPANRB 5/2020 (Manajemen Risiko SPBE)
        res_5 = regulatory_intelligence.verify_legal_status("PERMENPANRB_5_2020")
        self.assertEqual(res_5["legal_status"], "BERLAKU")
        art_5 = regulatory_intelligence.get_article("PERMENPANRB_5_2020", "7", "1")
        self.assertIn("Risiko Keamanan Informasi", art_5["text"])

        # PermenPANRB 90/2021 (Zona Integritas WBK/WBBM)
        res_90 = regulatory_intelligence.verify_legal_status("PERMENPANRB_90_2021")
        self.assertEqual(res_90["legal_status"], "BERLAKU")

        # Pedoman PANRB 3/2024 (Tauval SPBE Terkini)
        res_ped3 = regulatory_intelligence.verify_legal_status("PEDOMAN_PANRB_3_2024")
        self.assertEqual(res_ped3["legal_status"], "BERLAKU")

    def test_13_regulatory_lineage_no_isolated_evaluation(self):
        lineage_95 = regulatory_intelligence.get_regulatory_lineage("PERPRES_95_2018")
        self.assertEqual(lineage_95["status"], "SUCCESS")
        self.assertTrue(len(lineage_95["direct_relationships"]) >= 3)
        self.assertTrue(any("Perpres 132/2022" in n for n in lineage_95["contextual_evaluation_notes"]))
        self.assertTrue(any("Perpres 82/2023" in n for n in lineage_95["contextual_evaluation_notes"]))

        lineage_59 = regulatory_intelligence.get_regulatory_lineage("PERMENPANRB_59_2020")
        self.assertTrue(any("Pedoman Menteri PANRB No. 3 Tahun 2024" in n for n in lineage_59["contextual_evaluation_notes"]))


if __name__ == "__main__":
    unittest.main()
