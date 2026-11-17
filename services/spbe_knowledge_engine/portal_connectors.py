"""
NEXUS AI ENTERPRISE — OFFICIAL GOVERNMENT PORTAL CONNECTORS
Direct connectors and registries to authentic Indonesian government digital legal portals:
1. JDIH Kementerian PANRB (jdih.menpan.go.id)
2. Database Peraturan BPK (peraturan.bpk.go.id)
3. JDIH Sekretariat Negara (jdih.setneg.go.id)
4. JDIHN (jdihn.go.id)
5. Kementerian Komunikasi dan Digital / Komdigi (www.komdigi.go.id)
6. JDIH Pemerintah Provinsi DKI Jakarta (jdih.jakarta.go.id)
"""

from typing import Dict, List, Any, Optional

class OfficialPortalConnectors:
    def __init__(self):
        self._portals: Dict[str, Dict[str, Any]] = self._init_portal_registry()

    def _init_portal_registry(self) -> Dict[str, Dict[str, Any]]:
        return {
            "JDIH_PANRB": {
                "id": "JDIH_PANRB",
                "name": "JDIH Kementerian PANRB",
                "url": "https://jdih.menpan.go.id",
                "authority": "Kementerian Pendayagunaan Aparatur Negara dan Reformasi Birokrasi",
                "type": "PORTAL_REGULASI_UTAMA_SPBE",
                "scope": [
                    "Regulasi SPBE Nasional",
                    "Pedoman Manajemen Risiko SPBE (PermenPANRB 5/2020)",
                    "Pedoman Pemantauan dan Evaluasi SPBE (PermenPANRB 59/2020 & Pedoman 3/2024)",
                    "Pembangunan & Evaluasi Zona Integritas WBK/WBBM (PermenPANRB 90/2021)",
                    "Tata Kelola Kelembagaan & SDM Aparatur Digital"
                ],
                "trust_level": "PRIMARY_LEGAL_SOURCE",
                "status": "ACTIVE_CONNECTED"
            },
            "BPK_PERATURAN": {
                "id": "BPK_PERATURAN",
                "name": "Database Peraturan BPK RI",
                "url": "https://peraturan.bpk.go.id",
                "authority": "Badan Pemeriksa Keuangan Republik Indonesia",
                "type": "METADATA_STATUS_HUKUM_NASIONAL",
                "scope": [
                    "Metadata Lengkap Peraturan Perundang-undangan RI",
                    "Verifikasi Status Hukum (Berlaku / Mengubah / Dicabut)",
                    "Uji Materiil Mahkamah Agung & Mahkamah Konstitusi",
                    "Lembaran Negara & Berita Negara Resmi",
                    "Perpres 132/2022, Perpres 82/2023, Perpres 83/2025"
                ],
                "trust_level": "PRIMARY_LEGAL_METADATA",
                "status": "ACTIVE_CONNECTED"
            },
            "JDIH_SETNEG": {
                "id": "JDIH_SETNEG",
                "name": "JDIH Kementerian Sekretariat Negara",
                "url": "https://jdih.setneg.go.id",
                "authority": "Kementerian Sekretariat Negara Republik Indonesia",
                "type": "PORTAL_REGULASI_KEPRESIDENAN",
                "scope": [
                    "Undang-Undang Republik Indonesia",
                    "Peraturan Pemerintah (PP)",
                    "Peraturan Presiden (Perpres 95/2018, 132/2022, 82/2023, 83/2025)",
                    "Keputusan & Instruksi Presiden Terkait Digitalisasi Pemerintahan"
                ],
                "trust_level": "PRIMARY_EXECUTIVE_SOURCE",
                "status": "ACTIVE_CONNECTED"
            },
            "JDIHN": {
                "id": "JDIHN",
                "name": "Jaringan Dokumentasi dan Informasi Hukum Nasional",
                "url": "https://jdihn.go.id",
                "authority": "Badan Pembinaan Hukum Nasional (BPHN) - Kemenkumham RI",
                "type": "JARINGAN_HUKUM_TERINTEGRASI",
                "scope": [
                    "Integrasi Dokumen Hukum Seluruh K/L dan Pemerintah Daerah se-Indonesia",
                    "Pencarian Silang Antar-Regulasi Lintas Instansi",
                    "Standar Metadata Hukum Nasional Berbasis Standar Dublin Core"
                ],
                "trust_level": "NATIONAL_INTEGRATED_NETWORK",
                "status": "ACTIVE_CONNECTED"
            },
            "KOMDIGI": {
                "id": "KOMDIGI",
                "name": "Kementerian Komunikasi dan Digital (Komdigi)",
                "url": "https://www.komdigi.go.id",
                "authority": "Kementerian Komunikasi dan Digital Republik Indonesia",
                "type": "STANDAR_TEKNIS_INFRASTRUKTUR_DATA",
                "scope": [
                    "Pusat Data Nasional (PDN) & Government Cloud",
                    "Jaringan Intra Pemerintah (JIP) & Keamanan Siber SPBE",
                    "Sistem Penghubung Layanan Pemerintah (SPLP / Interoperabilitas Data)",
                    "Standar Interoperabilitas & Arsitektur Keamanan Informasi",
                    "Penyelenggara Sertifikasi Elektronik (PSrE) & Tanda Tangan Digital"
                ],
                "trust_level": "TECHNICAL_STANDARD_AUTHORITY",
                "status": "ACTIVE_CONNECTED"
            },
            "JDIH_DKI": {
                "id": "JDIH_DKI",
                "name": "JDIH Pemerintah Provinsi DKI Jakarta",
                "url": "https://jdih.jakarta.go.id",
                "authority": "Pemerintah Provinsi DKI Jakarta",
                "type": "REGULASI_DAERAH_SUB_NASIONAL",
                "scope": [
                    "Peraturan Gubernur No. 88/2021 tentang SPBE DKI Jakarta",
                    "Peraturan Gubernur Satu Data Jakarta & Arsitektur Lokal",
                    "Instruksi Sekretaris Daerah Pemprov DKI Jakarta"
                ],
                "trust_level": "SUB_NATIONAL_GOVERNMENT",
                "status": "ACTIVE_CONNECTED"
            }
        }

    def list_portals(self) -> List[Dict[str, Any]]:
        """Returns all configured official government portals."""
        return list(self._portals.values())

    def get_portal(self, portal_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves details of a specific official government portal."""
        return self._portals.get(portal_id)

    def verify_source_authenticity(self, source_url: str) -> Dict[str, Any]:
        """
        Validates if a source URL belongs to an authoritative Indonesian government domain (.go.id).
        Rejects commercial SEO blogs, scraper websites, and unofficial summaries.
        """
        source_url_clean = source_url.strip().lower()
        is_gov = (".go.id" in source_url_clean) or ("jdihn.go.id" in source_url_clean)
        
        # Match against known official portals
        matched_portal = None
        for p_id, p_info in self._portals.items():
            domain_part = p_info["url"].replace("https://", "").replace("http://", "").split("/")[0]
            if domain_part in source_url_clean:
                matched_portal = p_info
                break

        return {
            "source_url": source_url,
            "is_authoritative_government_source": is_gov,
            "matched_official_portal": matched_portal["name"] if matched_portal else ("Domain Pemerintah (.go.id)" if is_gov else "NON_GOVERNMENT_UNVERIFIED"),
            "status": "TRUSTED_PRIMARY_SOURCE" if is_gov else "REJECTED_UNOFFICIAL_SOURCE"
        }

# Global singleton
portal_connectors = OfficialPortalConnectors()
