"""
NEXUS AI ENTERPRISE — SPBE Knowledge Engine CLI Dispatcher
Handles standard input requests for SPBE regulations, ontology, 12-step reasoning, and QA audits.
"""

import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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


def main():
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input) if raw_input.strip() else {}
        action = payload.get("action", "list_regulations")

        if action == "list_portals":
            res = portal_connectors.list_portals()
            print(json.dumps(res, ensure_ascii=False))

        elif action == "verify_source":
            url = payload.get("url", "")
            res = portal_connectors.verify_source_authenticity(url)
            print(json.dumps(res, ensure_ascii=False))

        elif action == "get_lineage":
            reg_id = payload.get("regulation_id", "PERPRES_95_2018")
            res = regulatory_intelligence.get_regulatory_lineage(reg_id)
            print(json.dumps(res, ensure_ascii=False))

        elif action == "list_regulations":
            domain = payload.get("domain")
            query = payload.get("query", "")
            res = regulatory_intelligence.search_regulations(query, domain=domain, enforce_active=True)
            print(json.dumps(res, ensure_ascii=False))

        elif action == "verify_regulation":
            reg_id = payload.get("regulation_id", "PERPRES_132_2022")
            res = regulatory_intelligence.verify_legal_status(reg_id)
            print(json.dumps(res, ensure_ascii=False))

        elif action == "get_article":
            reg_id = payload.get("regulation_id", "PERPRES_132_2022")
            art_num = payload.get("article", "6")
            para_num = payload.get("paragraph")
            res = regulatory_intelligence.get_article(reg_id, art_num, para_num)
            print(json.dumps(res, ensure_ascii=False))

        elif action == "trace_ontology":
            func_id = payload.get("function_id", "FUNC_TRANTIBUM")
            res = spbe_ontology.trace_architecture_path(func_id)
            print(json.dumps(res, ensure_ascii=False))

        elif action == "lookup_glossary":
            term = payload.get("term", "")
            res = consulting_repository.lookup_term(term)
            print(json.dumps(res or {}, ensure_ascii=False))

        elif action == "execute_reasoning":
            opd = payload.get("opd_name", "Satuan Polisi Pamong Praja")
            domains = payload.get("domains", ["Proses Bisnis", "Layanan", "Aplikasi", "Data & Informasi"])
            inputs = payload.get("evidence_inputs", {"has_3c_file": True, "total_rows_audited": 12, "missing_rows_count": 5})
            res = spbe_reasoning_engine.execute_12_step_advisory(opd, domains, inputs)
            print(json.dumps(res, ensure_ascii=False))

        elif action == "qa_audit":
            report_data = payload.get("report", {})
            res = spbe_qa_agent.audit_consulting_report(report_data)
            print(json.dumps(res, ensure_ascii=False))

        elif action == "hybrid_search":
            q = payload.get("query", "")
            dom = payload.get("domain")
            res = spbe_retriever.hybrid_search(q, domain_filter=dom)
            print(json.dumps(res, ensure_ascii=False))

        else:
            print(json.dumps({"error": f"Aksi tidak dikenal: '{action}'"}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()
