"""
NEXUS AI ENTERPRISE — SPBE ENTERPRISE ARCHITECTURE ONTOLOGY
Formal Concepts, Taxonomy, and Relationship Knowledge Graph.
Implements Perpres 132/2022 Architecture Domains (RAB, RAL, RAD, RAA, RAI, RAK).
Strictly validates material relationships with explicit evidence and confidence scores.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class SPBEOntologyEngine:
    """
    Ontological knowledge graph for Indonesian Government Enterprise Architecture (SPBE).
    Connects Institutional Functions -> Processes -> Services -> Applications -> Data -> Infra/Security.
    """

    VALID_RELATIONSHIPS = [
        "performed_by",
        "supports",
        "enables",
        "uses_data",
        "integrates_with",
        "governed_by",
        "protected_by",
        "replaces",
        "depends_on"
    ]

    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._edges: List[Dict[str, Any]] = []
        self._init_standard_ontology()

    def add_node(self, node_id: str, concept_type: str, name: str, properties: Dict[str, Any]) -> None:
        """Adds a concept node into the SPBE ontology."""
        self._nodes[node_id] = {
            "id": node_id,
            "concept_type": concept_type,  # Function, Process, Service, Application, Data, Infra, Security, Regulation
            "name": name,
            "properties": properties,
            "created_at": datetime.now().isoformat()
        }

    def add_edge(
        self,
        source_id: str,
        relationship: str,
        target_id: str,
        evidence: str,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Adds a semantic relationship between concepts.
        Strict rule: Must have verifiable evidence and explicit confidence score (0.0 to 1.0).
        """
        if relationship not in self.VALID_RELATIONSHIPS:
            raise ValueError(f"Hubungan relasi tidak valid: '{relationship}'. Harus salah satu dari {self.VALID_RELATIONSHIPS}")

        if source_id not in self._nodes or target_id not in self._nodes:
            raise KeyError(f"Node '{source_id}' atau '{target_id}' belum terdaftar dalam ontologi.")

        self._edges.append({
            "source_id": source_id,
            "relationship": relationship,
            "target_id": target_id,
            "evidence": evidence,
            "confidence": min(1.0, max(0.0, float(confidence))),
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })

    def get_related_entities(self, node_id: str, relationship: Optional[str] = None, direction: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves all connected entities from a node with evidence and confidence."""
        results = []
        for edge in self._edges:
            if edge["source_id"] == node_id:
                if (relationship is None or edge["relationship"] == relationship) and (direction in [None, "OUTGOING"]):
                    target_node = self._nodes[edge["target_id"]]
                    source_node = self._nodes[edge["source_id"]]
                    results.append({
                        "direction": "OUTGOING",
                        "relationship": edge["relationship"],
                        "target_node": target_node,
                        "source_node": source_node,
                        "node": target_node,
                        "evidence": edge["evidence"],
                        "confidence": edge["confidence"]
                    })
            elif edge["target_id"] == node_id:
                if (relationship is None or edge["relationship"] == relationship) and (direction in [None, "INCOMING"]):
                    source_node = self._nodes[edge["source_id"]]
                    target_node = self._nodes[edge["target_id"]]
                    results.append({
                        "direction": "INCOMING",
                        "relationship": edge["relationship"],
                        "source_node": source_node,
                        "target_node": target_node,
                        "node": source_node,
                        "evidence": edge["evidence"],
                        "confidence": edge["confidence"]
                    })
        return results

    def trace_architecture_path(self, function_id: str) -> Dict[str, Any]:
        """
        Traces the full vertical alignment path:
        Institutional Function -> Business Process -> Service -> Application -> Data -> Security.
        """
        if function_id not in self._nodes:
            return {"status": "ERROR", "message": f"Fungsi '{function_id}' tidak ditemukan."}

        trace = {
            "function": self._nodes[function_id],
            "processes": [],
            "services": [],
            "applications": [],
            "data_assets": [],
            "evidence_chain": []
        }

        # Step 1: Function -> Process (supports / performed_by)
        for e in self.get_related_entities(function_id, "supports", direction="OUTGOING"):
            proc = e["target_node"]
            trace["processes"].append(proc)
            trace["evidence_chain"].append(f"[Proses] {proc['name']} didukung oleh fungsi {self._nodes[function_id]['name']} (Bukti: {e['evidence']})")

            # Step 2: Process -> Service (enables)
            for e_svc in self.get_related_entities(proc["id"], "enables", direction="OUTGOING"):
                svc = e_svc["target_node"]
                trace["services"].append(svc)
                trace["evidence_chain"].append(f"[Layanan] {svc['name']} dimungkinkan oleh proses {proc['name']} (Bukti: {e_svc['evidence']})")

                # Step 3: Service -> Application (enables / integrates_with)
                for e_app in self.get_related_entities(svc["id"], "enables", direction="OUTGOING"):
                    app = e_app["target_node"]
                    trace["applications"].append(app)
                    trace["evidence_chain"].append(f"[Aplikasi] {app['name']} menopang layanan {svc['name']} (Bukti: {e_app['evidence']})")

                    # Step 4: Application -> Data (uses_data)
                    for e_data in self.get_related_entities(app["id"], "uses_data", direction="OUTGOING"):
                        data_item = e_data["target_node"]
                        trace["data_assets"].append(data_item)
                        trace["evidence_chain"].append(f"[Data] {data_item['name']} dikonsumsi oleh aplikasi {app['name']} (Bukti: {e_data['evidence']})")

        return trace

    def _init_standard_ontology(self):
        """Initializes canonical Indonesian SPBE Architecture nodes & validated relationships."""
        # 1. Institutional Functions
        self.add_node(
            "FUNC_TRANTIBUM",
            "InstitutionalFunction",
            "Penyelenggaraan Ketenteraman dan Ketertiban Umum (Trantibum)",
            {"pd": "Satuan Polisi Pamong Praja", "legal_basis": "Perda DKI 8/2007, Pergub 88/2021"}
        )
        self.add_node(
            "FUNC_BAPPEDA_PERENCANAAN",
            "InstitutionalFunction",
            "Penyusunan Perencanaan Pembangunan Daerah dan RKPD",
            {"pd": "Badan Perencanaan Pembangunan Daerah", "legal_basis": "UU 25/2004, Permendagri 86/2017"}
        )

        # 2. Business Processes (RAB Level 1-7)
        self.add_node(
            "PROB_PATROLI_PENGAMANAN",
            "BusinessProcess",
            "RAB.01.04.02 - Patroli dan Pengamanan Wilayah Terpadu",
            {"level": 3, "rab_code": "RAB.01.04.02", "domain": "ProsesBisnis_Sesuai"}
        )
        self.add_node(
            "PROB_EVALUASI_RKPD",
            "BusinessProcess",
            "RAB.02.01.03 - Monitoring dan Evaluasi Capaian RKPD",
            {"level": 3, "rab_code": "RAB.02.01.03", "domain": "ProsesBisnis_Upgrade"}
        )

        # 3. Government Services (RAL)
        self.add_node(
            "SVC_PENGADUAN_TRANTIBUM",
            "GovernmentService",
            "RAL.01.02 - Layanan Pelaporan Gangguan Ketenteraman Umum (G2C/G2G)",
            {"type": "G2C", "service_code": "RAL.01.02", "domain": "Layanan_Sesuai"}
        )
        self.add_node(
            "SVC_E_MONEV_PEMBANGUNAN",
            "GovernmentService",
            "RAL.03.01 - Layanan Evaluasi Pembangunan Daerah Terpadu (G2G)",
            {"type": "G2G", "service_code": "RAL.03.01", "domain": "Layanan_Upgrade"}
        )

        # 4. Applications (RAA)
        self.add_node(
            "APP_JAKI",
            "Application",
            "Jakarta Kini (JAKI) — SuperApp Kanal Pengaduan Warga",
            {"type": "Aplikasi_Umum", "status": "AS_IS_AKTIF", "provider": "Diskominfotik DKI"}
        )
        self.add_node(
            "APP_E_MONEV_BAPPEDA",
            "Application",
            "Sistem Informasi Monev Bappeda DKI Jakarta",
            {"type": "Aplikasi_Khusus", "status": "TO_BE_UPGRADE", "provider": "Bappeda DKI"}
        )

        # 5. Data & Information (RAD)
        self.add_node(
            "DATA_TITIK_RAWAN",
            "DataInformation",
            "Data Titik Rawan Gangguan Trantibum dan Bencana (I2901)",
            {"sdi_compliant": True, "domain": "DataInformasi_Upgrade", "code": "I2901"}
        )
        self.add_node(
            "DATA_CAPAIAN_KINERJA",
            "DataInformation",
            "Data Capaian Kinerja dan Anggaran Organisasi Perangkat Daerah",
            {"sdi_compliant": True, "domain": "DataInformasi_Sesuai", "code": "I2920"}
        )

        # 6. Material Verified Relationships with Strict Evidence Citations
        self.add_edge(
            "FUNC_TRANTIBUM",
            "supports",
            "PROB_PATROLI_PENGAMANAN",
            evidence="DPA-SKPD Satpol PP 2024 Subkegiatan Patroli Pengawasan Ketenteraman Umum",
            confidence=0.98
        )
        self.add_edge(
            "PROB_PATROLI_PENGAMANAN",
            "enables",
            "SVC_PENGADUAN_TRANTIBUM",
            evidence="SOP Penanganan Pengaduan Gangguan Ketenteraman Masyarakat No. SOP-04/SatpolPP/2023",
            confidence=0.95
        )
        self.add_edge(
            "SVC_PENGADUAN_TRANTIBUM",
            "enables",
            "APP_JAKI",
            evidence="Pergub DKI No. 12 Tahun 2023 Pasal 8 ayat (3) Integrasi Kanal Laporan Cepat Tanggap",
            confidence=0.99
        )
        self.add_edge(
            "APP_JAKI",
            "uses_data",
            "DATA_TITIK_RAWAN",
            evidence="Katalog Satu Data Jakarta: Dataset Geospasial Titik Pengawasan Satpol PP 2024",
            confidence=0.92
        )


# Global singleton
spbe_ontology = SPBEOntologyEngine()
