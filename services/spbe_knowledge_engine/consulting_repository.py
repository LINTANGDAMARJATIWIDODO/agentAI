"""
NEXUS AI ENTERPRISE — SPBE CONSULTANT LEARNING REPOSITORY
Validated As-Is, To-Be, Gap Analysis (Sesuai/Upgrade/Sunset/Baru),
Hierarchical RAB Level 1-7, RACI, and Approved Terminology Glossary.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class SPBEConsultantRepository:
    """
    Curated, verified consulting intelligence repository for government digital transformation.
    Stores peer-reviewed architectural mappings, gap analyses, and authoritative terminology.
    """

    def __init__(self):
        self._cases = self._init_validated_cases()
        self._rab_hierarchy = self._init_rab_hierarchy()
        self._glossary = self._init_approved_glossary()

    def get_validated_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        return self._cases.get(case_id)

    def list_validated_cases(self) -> List[Dict[str, Any]]:
        return [{"id": k, **v} for k, v in self._cases.items()]

    def get_rab_level_hierarchy(self, level: Optional[int] = None) -> List[Dict[str, Any]]:
        if level is not None:
            return [item for item in self._rab_hierarchy if item["level"] == level]
        return self._rab_hierarchy

    def lookup_term(self, term: str) -> Optional[Dict[str, Any]]:
        t_clean = term.lower().strip()
        for k, v in self._glossary.items():
            if t_clean in k.lower() or t_clean in v["term"].lower():
                return v
        return None

    def _init_validated_cases(self) -> Dict[str, Dict[str, Any]]:
        return {
            "CASE_SATPOL_PP_DKI_3C": {
                "id": "CASE_SATPOL_PP_DKI_3C",
                "title": "Audit As-Is & To-Be Arsitektur SPBE Satuan Polisi Pamong Praja DKI Jakarta",
                "perangkat_daerah": "Satuan Polisi Pamong Praja",
                "governing_entity": "Pemerintah Provinsi DKI Jakarta",
                "year": 2024,
                "validation_status": "APPROVED_BY_EXPERT",
                "lead_consultant": "ARKA & NAYA (Nexus SPBE Advisory)",
                "as_is_baseline": {
                    "probis_count": 8,
                    "active_apps": ["JAKI (Kanal Trantibum)", "Si-Pol PP Internal (Legacy Desktop)"],
                    "data_status": "Parsial, belum terstandarisasi SDI secara menyeluruh",
                    "infra_status": "Server lokal di kantor Satpol PP + sebagian Cloud DKI"
                },
                "to_be_target": {
                    "probis_count": 12,
                    "target_apps": ["SuperApp JAKI Terpadu (Mobile Patrol)", "Dashboard Eksekutif Trantibum Real-Time"],
                    "data_status": "Interoperabilitas penuh dengan Satu Data Jakarta melalui REST API",
                    "infra_status": "100% Hosted di Pusat Data Pemprov DKI Jakarta (Government Cloud)"
                },
                "gap_analysis": [
                    {
                        "domain": "ProsesBisnis_Upgrade",
                        "code": "RAB.01.04.02",
                        "description": "Patroli dan Penanganan Pelanggaran Trantibum Terintegrasi Geospasial",
                        "status": "UPGRADE_REQUIRED",
                        "root_cause": "Proses pencatatan patroli lapangan masih manual berbasis kertas (form fisik)",
                        "recommendation": "Digitalisasi formulir Berita Acara Pemeriksaan (BAP) lapangan pada aplikasi mobile JAKI Petugas"
                    },
                    {
                        "domain": "Aplikasi_Sunset",
                        "code": "RAA.02.01",
                        "description": "Si-Pol PP Internal (Aplikasi Desktop Berbasis FoxPro/VB)",
                        "status": "SUNSET",
                        "root_cause": "Aplikasi lama tidak memiliki API, tidak aman, dan rentan kehilangan data",
                        "recommendation": "Penetapan jadwal sunset (decommissioning) akhir Q3 2025 dan migrasi seluruh basis data ke platform web"
                    },
                    {
                        "domain": "DataInformasi_Sesuai",
                        "code": "RAD.03.01",
                        "description": "Data Kunjungan Tamu dan Sarana Prasarana Satpol PP",
                        "status": "SESUAI",
                        "root_cause": "Telah tercatat rapi dan sinkron dengan Sistem Informasi Aset BPAD",
                        "recommendation": "Pertahankan pemeliharaan berkala dan lakukan audit berkala setiap triwulan"
                    }
                ],
                "raci": [
                    {"activity": "Penetapan Kebijakan Arsitektur SPBE Satpol PP", "R": "Kepala Satpol PP", "A": "Sekretaris Daerah", "C": "Diskominfotik", "I": "Seluruh Bidang"},
                    {"activity": "Integrasi Data Titik Rawan ke Satu Data Jakarta", "R": "Pranata Komputer Satpol PP", "A": "Kepala Bidang TIK Satpol PP", "C": "Walidata (Kominfotik)", "I": "Inspektorat"}
                ]
            }
        }

    def _init_rab_hierarchy(self) -> List[Dict[str, Any]]:
        """Canonical 7-level Business Architecture Reference (RAB Level 1 to Level 7)."""
        return [
            {"level": 1, "code": "RAB.01", "name": "Urusan Pemerintahan Wajib Terkait Pelayanan Dasar", "description": "Fungsi fundamental pemerintahan daerah yang menyangkut hak-hak dasar konstitusional warga negara."},
            {"level": 2, "code": "RAB.01.04", "name": "Ketenteraman, Ketertiban Umum, dan Pelindungan Masyarakat", "description": "Penyelenggaraan ketenteraman umum, penegakan peraturan daerah, dan kesiapsiagaan bencana."},
            {"level": 3, "code": "RAB.01.04.02", "name": "Penegakan Peraturan Daerah dan Peraturan Kepala Daerah", "description": "Kegiatan pengawasan, patroli, penindakan non-yustisial dan yustisial pelanggaran perda."},
            {"level": 4, "code": "RAB.01.04.02.01", "name": "Patroli Pengawasan Kepatuhan Trantibum", "description": "Pengerahan personel lapangan untuk melakukan monitoring kepatuhan ruang publik."},
            {"level": 5, "code": "RAB.01.04.02.01.01", "name": "Pencatatan Temuan Lapangan dan Verifikasi Bukti", "description": "Identifikasi subjek pelanggaran, dokumentasi foto/koordinat, dan penerbitan surat peringatan."},
            {"level": 6, "code": "RAB.01.04.02.01.01.01", "name": "Input Berita Acara Pemeriksaan Digital", "description": "Penginputan form BAP digital tersanitasi ke dalam sistem komando terpadu."},
            {"level": 7, "code": "RAB.01.04.02.01.01.01.01", "name": "Penandatanganan Digital Tersertifikasi oleh Penyidik PNS", "description": "Otentikasi hukum dokumen hasil pemeriksaan menggunakan sertifikat digital Balai Sertifikasi Elektronik (BSrE)."}
        ]

    def _init_approved_glossary(self) -> Dict[str, Dict[str, Any]]:
        """Authoritative SPBE definitions derived directly from Perpres 95/2018 & PermenPANRB."""
        return {
            "arsitektur_spbe": {
                "term": "Arsitektur SPBE",
                "definition": "Kerangka dasar yang mendeskripsikan integrasi proses bisnis, data dan informasi, infrastruktur SPBE, aplikasi SPBE, dan keamanan SPBE untuk menghasilkan layanan SPBE yang terintegrasi.",
                "legal_source": "Perpres No. 95 Tahun 2018 Pasal 1 angka 4"
            },
            "interoperabilitas_data": {
                "term": "Interoperabilitas Data",
                "definition": "Kemampuan data untuk dibagipakaikan antar sistem elektronik yang saling berinteraksi menggunakan format terbuka dan protokol standar.",
                "legal_source": "Perpres No. 39 Tahun 2019 Pasal 1 angka 11"
            },
            "aplikasi_umum": {
                "term": "Aplikasi Umum",
                "definition": "Aplikasi SPBE yang sama, standar, dan digunakan secara berbagi pakai oleh Instansi Pusat dan/atau Pemerintah Daerah untuk memberikan layanan SPBE yang serupa.",
                "legal_source": "Perpres No. 95 Tahun 2018 Pasal 1 angka 14"
            },
            "aplikasi_khusus": {
                "term": "Aplikasi Khusus",
                "definition": "Aplikasi SPBE yang dibangun, dikembangkan, dan digunakan oleh 1 (satu) Instansi Pusat atau Pemerintah Daerah tertentu untuk memenuhi kebutuhan khusus yang tidak dipenuhi oleh Aplikasi Umum.",
                "legal_source": "Perpres No. 95 Tahun 2018 Pasal 1 angka 15"
            },
            "pusat_data_nasional": {
                "term": "Pusat Data Nasional (PDN)",
                "definition": "Fasilitas infrastruktur komputasi dan penyimpanan data terpadu yang digunakan secara bersama oleh seluruh kementerian, lembaga, dan pemerintah daerah untuk mewujudkan efisiensi dan keamanan kedaulatan data.",
                "legal_source": "Perpres No. 132 Tahun 2022 Pasal 12"
            }
        }


# Global singleton
consulting_repository = SPBEConsultantRepository()
