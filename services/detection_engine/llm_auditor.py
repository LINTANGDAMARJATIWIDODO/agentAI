"""
NEXUS AI ENTERPRISE — GEMINI LLM CONTEXTUAL FORENSIC AUDITOR
============================================================
Performs qualitative, contextual linguistic forensic audit on Indonesian text.
Adheres strictly to the scientific guidelines:
- Gemini is an independent contextual analyst, NOT the source of statistical truth.
- Never invents percentages or claims absolute certainty.
- Identifies specific Indonesian stylistic patterns, institutional cadence,
  and lexical nuances in accordance with standard KBBI and EYD V.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.gemini.gemini_service import GEMINI_API_KEY, MODEL_FLASH


class GeminiForensicAuditor:
    """
    Contextual linguistic auditor using Google Gemini API.
    Provides deep qualitative forensic review of Indonesian text structure.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "").strip()
        self.model = model or MODEL_FLASH or "gemini-2.5-flash"

    def audit_text(
        self,
        text: str,
        statistical_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Conducts forensic audit using Gemini.
        Falls back to local heuristic linguistic critique if API key is absent or offline.
        """
        if not self.api_key:
            return self._fallback_audit(text, statistical_metrics, reason="GEMINI_API_KEY belum dikonfigurasi; audit berbasis analitik heuristik linguistik.")

        prompt = f"""Anda adalah Auditor Forensik Linguistik Bahasa Indonesia Independen untuk NEXUS AI ENTERPRISE.
Tugas Anda adalah menelaah teks terlampir secara kualitatif untuk mengidentifikasi pola kepengarangan (apakah mencerminkan gaya bahasa manusia otentik atau bentukan model bahasa buatan / AI).

PEDOMAN KETAT WAJIB:
1. DILARANG membuat persentase angka sintetis atau mengklaim kepastian mutlak kepengarangan semata-mata dari teks.
2. Fokus pada bukti stilistika, variasi ritme klausa, keberadaan perspektif subyektif/institusional, dan klise sintaksis bahasa Indonesia.
3. Gunakan standar bahasa Indonesia baku (EYD V & KBBI).
4. Berikan hasil dalam format JSON yang valid dengan skema berikut:
{{
  "contextual_assessment": "Deskripsi analisis menyeluruh mengenai karakter dan alur teks",
  "human_like_indicators": ["Daftar indikator gaya tulisan manusia yang ditemukan"],
  "ai_like_indicators": ["Daftar indikator gaya khas model bahasa buatan yang ditemukan"],
  "stylistic_critique": "Kritik linguistik mendalam terhadap diksi, transisi, dan kohesi paragraf",
  "recommended_investigation": "Langkah verifikasi kontekstual yang disarankan bagi pembaca/peneliti"
}}

METRIK STATISTIK OBJEKTIF SEBAGAI REFERENSI:
- Nilai Burstiness (Variasi Ritme Kalimat): {statistical_metrics.get('burstiness', 'N/A')}
- Type-Token Ratio (TTR): {statistical_metrics.get('ttr', 'N/A')}
- Karakteristik Yule's K: {statistical_metrics.get('yules_k', 'N/A')}
- Kepadatan Frasa Transisi AI: {statistical_metrics.get('ai_transition_density', 'N/A')}%
- Prediksi Model Statistik: {statistical_metrics.get('verdict', 'N/A')}

TEKS YANG DIAUDIT:
\"\"\"
{text[:2500]}
\"\"\"

Balas HANYA dengan blok JSON murni tanpa markdown atau teks tambahan.
"""

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1024,
                "responseMimeType": "application/json"
            }
        }

        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                content = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
                
                # Parse JSON output
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                
                parsed = json.loads(content.strip())
                parsed["source"] = f"Google Gemini ({self.model})"
                parsed["status"] = "success"
                return parsed

        except Exception as e:
            return self._fallback_audit(text, statistical_metrics, reason=f"Gemini API offline/unreachable: {str(e)}")

    def _fallback_audit(
        self,
        text: str,
        statistical_metrics: Dict[str, Any],
        reason: str = ""
    ) -> Dict[str, Any]:
        """
        Deterministic, robust heuristic forensic commentary when LLM is unavailable.
        """
        burstiness = statistical_metrics.get("burstiness", 0.0)
        ai_trans = statistical_metrics.get("ai_transition_density", 0.0)
        verdict = statistical_metrics.get("verdict", "Inconclusive")

        human_ind = []
        ai_ind = []

        if burstiness > -0.2:
            human_ind.append("Variasi panjang kalimat tinggi dengan fluktuasi ritme yang dinamis (burstiness alami).")
        else:
            ai_ind.append("Panjang kalimat terdistribusi sangat seragam tanpa jeda staccato khas tuturan manusia.")

        if ai_trans > 1.5:
            ai_ind.append("Kepadatan tinggi konjungsi transisi formal klise ('Selain itu', 'Lebih lanjut', 'Dengan demikian').")
        else:
            human_ind.append("Penggunaan konjungsi transisi proporsional dan tidak terjadi penumpukan mekanis di awal kalimat.")

        if "memainkan peran" in text.lower() or "dalam era" in text.lower() or "tidak dapat dipungkiri" in text.lower():
            ai_ind.append("Ditemukan kolokasi metaforis generik yang lazim dihasilkan oleh model bahasa.")

        if not human_ind:
            human_ind.append("Keteraturan tata bahasa formal sesuai kaidah baku KBBI.")
        if not ai_ind:
            ai_ind.append("Tidak ditemukan tanda-tanda repetisi frasa sintetis yang mencolok.")

        return {
            "source": "NEXUS Heuristic Forensic Rules (Offline Mode)",
            "status": "fallback",
            "reason": reason,
            "contextual_assessment": (
                f"Berdasarkan analisis struktural, dokumen diklasifikasikan sebagai '{verdict}'. "
                f"Karakteristik teks memperlihatkan skor variasi ritme {burstiness:.2f} dan kepadatan transisi {ai_trans:.2f}%."
            ),
            "human_like_indicators": human_ind,
            "ai_like_indicators": ai_ind,
            "stylistic_critique": (
                "Kohesi antarkalimat tersusun rapi. Namun, untuk menjamin integritas naskah secara komprehensif, "
                "pemeriksaan silang terhadap sumber rujukan faktual dan jejak revisi dokumen tetap dianjurkan."
            ),
            "recommended_investigation": "Lakukan wawancara kepengarangan atau periksa riwayat versi berkas (version history) untuk verifikasi empiris tambahan."
        }


if __name__ == "__main__":
    auditor = GeminiForensicAuditor()
    sample = (
        "Dalam era digitalisasi yang serba cepat ini, penerapan teknologi informasi menjadi suatu keniscayaan yang "
        "tidak dapat dihindari bagi setiap organisasi. Selain itu, integrasi sistem kecerdasan buatan memainkan peran "
        "yang sangat penting dalam meningkatkan efisiensi operasional secara signifikan."
    )
    res = auditor.audit_text(sample, {"burstiness": -0.85, "ttr": 0.91, "yules_k": 85.0, "ai_transition_density": 4.5, "verdict": "AI-like"})
    print("Auditor Result:")
    print(json.dumps(res, indent=2, ensure_ascii=False))
