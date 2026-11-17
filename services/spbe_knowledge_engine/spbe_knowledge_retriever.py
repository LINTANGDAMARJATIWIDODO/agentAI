"""
NEXUS AI ENTERPRISE — SPBE KNOWLEDGE RETRIEVER & HYBRID SEARCH
Structured Metadata Filtering, Keyword Match, Semantic Similarity,
and Citation-Aware Evidence Generation.
"""

import math
from typing import Dict, List, Any, Optional
from services.spbe_knowledge_engine.regulatory_intelligence import regulatory_intelligence
from services.spbe_knowledge_engine.spbe_ontology import spbe_ontology
from services.spbe_knowledge_engine.consulting_repository import consulting_repository


class SPBEKnowledgeRetriever:
    """
    Hybrid retriever combining structured legal filters, exact legal terminology,
    and semantic context retrieval for SPBE consultants.
    """

    def __init__(self):
        self.regulatory = regulatory_intelligence
        self.ontology = spbe_ontology
        self.repo = consulting_repository

    def hybrid_search(
        self,
        query: str,
        domain_filter: Optional[str] = None,
        enforce_active_laws: bool = True,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Executes hybrid retrieval:
        1. Exact legal and regulatory matching (Active Laws Only).
        2. Architectural concept mapping from Ontology.
        3. Validated case examples from Consulting Repository.
        """
        # 1. Regulations
        reg_results = self.regulatory.search_regulations(
            query=query,
            domain=domain_filter,
            enforce_active=enforce_active_laws
        )

        # 2. Terminology Glossary
        term_result = self.repo.lookup_term(query)

        # 3. Validated Cases
        matching_cases = []
        for case in self.repo.list_validated_cases():
            c_text = (case.get("title", "") + " " + case.get("perangkat_daerah", "")).lower()
            if query.lower() in c_text or (domain_filter and domain_filter.lower() in c_text):
                matching_cases.append(case)

        # 4. Formatted Citations
        citations = []
        for r in reg_results[:top_k]:
            citations.append({
                "source_type": "PERATURAN_PERUNDANG_UNDANGAN",
                "citation": r["citation"],
                "title": r["title"],
                "legal_status": r["legal_status"],
                "relevance_score": r["score"],
                "key_articles": r["matched_articles"]
            })

        return {
            "query": query,
            "domain_filter": domain_filter,
            "enforce_active_laws": enforce_active_laws,
            "results_summary": {
                "regulations_found": len(reg_results),
                "glossary_match": term_result["term"] if term_result else None,
                "validated_cases_found": len(matching_cases)
            },
            "glossary_definition": term_result,
            "legal_citations": citations,
            "validated_cases": matching_cases
        }


# Global singleton
spbe_retriever = SPBEKnowledgeRetriever()
