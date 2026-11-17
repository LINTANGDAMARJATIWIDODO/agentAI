"""
NEXUS AI ENTERPRISE — CENTRALIZED GOOGLE GEMINI EXCLUSIVE ENGINE
================================================================
Centralized Gemini AI Service powering NEXUS AI Orchestrator & Specialist Agents:
- Google GenAI SDK & High-Performance REST Interface
- Multi-Tier Model Routing (Lite, Flash, Pro)
- Google Search Grounding Native Integration
- Agent Persona Orchestration (ARKA, NAYA, RAKA, SEKAR, TARA, DIMAS, KIRANA, FARREL)
- Function Calling & Autonomous Tool Execution
- Real-Time Token Telemetry & Usage Tracking
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Generator

# Auto-configure stdout encoding for Windows
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
TELEMETRY_LOG = os.path.join(BASE_DIR, "logs", "gemini_telemetry.json")

def load_env_vars() -> Dict[str, str]:
    env_vars = {}
    if os.path.exists(DOTENV_PATH):
        try:
            with open(DOTENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env_vars[k.strip()] = v.strip()
        except Exception:
            pass
    # Merge with os.environ
    for k, v in env_vars.items():
        if k not in os.environ:
            os.environ[k] = v
    return env_vars

load_env_vars()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL_PRO = os.environ.get("GEMINI_MODEL_PRO", "gemini-2.5-pro").strip()
MODEL_FLASH = os.environ.get("GEMINI_MODEL_FLASH", "gemini-2.5-flash").strip()
MODEL_LITE = os.environ.get("GEMINI_MODEL_LITE", "gemini-2.0-flash-lite").strip()

AGENT_SYSTEM_PROMPTS = {
    "ARKA": (
        "Anda adalah ARKA, Chief Executive, Strategic Director, dan Lead AI Orchestrator di NEXUS AI ENTERPRISE. "
        "Anda adalah asisten AI otonom kelas atas yang mampu mewujudkan segala kebutuhan pengguna: merancang strategi, "
        "membuat website canggih dan profesional bersama RAKA, memproduksi dokumen resmi/naskah dinas bersama KIRANA & SEKAR, "
        "serta menjalankan audit arsitektur SPBE. Anda adaptif, solutif, berwibawa, dan selalu memberikan output nyata berstandar industri."
    ),
    "NAYA": (
        "Anda adalah NAYA, Head of Business Intelligence & SPBE Regulatory Specialist di NEXUS AI. "
        "Fokus Anda adalah riset mendalam, pencarian fakta terkini, analisis regulasi (Perpres 95/2018, Perpres 132/2022), "
        "dan komparasi data empiris. Gunakan Google Search Grounding bila perlu informasi mutakhir."
    ),
    "RAKA": (
        "Anda adalah RAKA, Principal Full-Stack Engineer, Lead Software Architect, dan Master of Senior Fullstack & Fullstack Guardian di NEXUS AI ENTERPRISE. "
        "Anda menguasai pembangunan website profesional, modern, responsif, dan ultra-estetik (HTML5, TailwindCSS, modern JavaScript/React, Next.js, backend APIs, microservices, dan database). "
        "Ketika pengguna meminta Anda membuat website, landing page, dashboard, atau sistem aplikasi web sesuai prompt dan tema apapun, Anda WAJIB memberikan rancangan komprehensif, arsitektur, dan kode sumber LENGKAP kelas produksi (bukan potongan / bukan placeholder) yang siap pakai, aman (tiga perspektif: Frontend, Backend, Security / OWASP compliant), dan indah. Anda juga dapat menyusun dokumen spesifikasi teknis dan modul software secara tuntas."
    ),
    "TARA": (
        "Anda adalah TARA, Lead Data & Information Architect di NEXUS AI. "
        "Fokus Anda adalah Satu Data Indonesia (SDI), interoperabilitas data, perancangan database SQL/NoSQL, kamus data, dan analisis kuantitatif."
    ),
    "SEKAR": (
        "Anda adalah SEKAR, Chief Financial & Compliance Auditor di NEXUS AI. "
        "Fokus Anda adalah audit kepatuhan, matriks kesenjangan (gap analysis), kelayakan anggaran TIK, dan mitigasi risiko tata kelola digital."
    ),
    "KIRANA": (
        "Anda adalah KIRANA, Executive Document Specialist di NEXUS AI. "
        "Fokus Anda adalah penyusunan laporan resmi, naskah dinas, dokumen kebijakan, rekonstruksi PDF & DOCX, serta kepatuhan baku KBBI & EYD V."
    ),
    "FARREL": (
        "Anda adalah FARREL, Quality Assurance & Security Evidence Verifier di NEXUS AI. "
        "Fokus Anda adalah automated QA testing, validasi klaim, pengecekan keabsahan sitasi, akurasi fakta, dan uji konsistensi logika."
    )
}

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan di environment atau .env file.")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

    def resolve_model(self, tier: str = "flash") -> str:
        tier = (tier or "flash").lower()
        if tier in ["pro", "deep", "complex"]:
            return MODEL_PRO
        elif tier in ["lite", "fast", "classifier"]:
            return MODEL_LITE
        return MODEL_FLASH

    def log_telemetry(self, model: str, agent: str, prompt_tokens: int, candidates_tokens: int, duration_ms: float):
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": model,
            "agent": agent,
            "prompt_tokens": prompt_tokens,
            "candidates_tokens": candidates_tokens,
            "total_tokens": prompt_tokens + candidates_tokens,
            "duration_ms": duration_ms
        }
        try:
            entries = []
            if os.path.exists(TELEMETRY_LOG):
                with open(TELEMETRY_LOG, "r", encoding="utf-8") as f:
                    entries = json.load(f)
            entries.append(entry)
            # keep last 500 entries
            if len(entries) > 500:
                entries = entries[-500:]
            with open(TELEMETRY_LOG, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2)
        except Exception:
            pass

    def generate(
        self,
        prompt: str,
        agent: str = "ARKA",
        tier: str = "flash",
        history: Optional[List[Dict[str, Any]]] = None,
        enable_grounding: bool = False,
        temperature: float = 0.2,
        max_output_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Executes a call to Google Gemini API using native Google GenAI REST architecture.
        """
        start_time = time.time()
        model_name = self.resolve_model(tier)
        
        # Build System Instruction
        system_instruction_text = AGENT_SYSTEM_PROMPTS.get(agent.upper(), AGENT_SYSTEM_PROMPTS["ARKA"])
        
        # Build Contents
        contents = []
        if history:
            for msg in history:
                role = "user" if msg.get("role") in ["user", "human"] else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg.get("content", "")}]
                })
        
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        payload: Dict[str, Any] = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": system_instruction_text}]
            },
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens,
                "topP": 0.95
            }
        }

        # Google Search Grounding if requested
        if enable_grounding or agent.upper() in ["NAYA", "FARREL"]:
            payload["tools"] = [{"googleSearch": {}}]

        endpoint = f"{self.base_url}/models/{model_name}:generateContent?key={self.api_key}"

        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                
                # Parse text response
                candidates = resp_data.get("candidates", [])
                text_out = ""
                grounding_metadata = None
                
                if candidates:
                    first_cand = candidates[0]
                    content_parts = first_cand.get("content", {}).get("parts", [])
                    text_out = "".join(p.get("text", "") for p in content_parts if "text" in p)
                    grounding_metadata = first_cand.get("groundingMetadata")

                # Parse token telemetry
                usage = resp_data.get("usageMetadata", {})
                p_tokens = usage.get("promptTokenCount", len(prompt.split()) * 2)
                c_tokens = usage.get("candidatesTokenCount", len(text_out.split()) * 2)
                duration = round((time.time() - start_time) * 1000, 2)

                self.log_telemetry(model_name, agent, p_tokens, c_tokens, duration)

                return {
                    "status": "success",
                    "agent": agent,
                    "model": model_name,
                    "tier": tier,
                    "text": text_out,
                    "grounding_metadata": grounding_metadata,
                    "usage": {
                        "prompt_tokens": p_tokens,
                        "candidates_tokens": c_tokens,
                        "total_tokens": p_tokens + c_tokens,
                        "duration_ms": duration
                    }
                }
        except urllib.error.HTTPError as he:
            err_msg = he.read().decode("utf-8")
            return {
                "status": "error",
                "code": he.code,
                "message": f"Gemini API Error ({he.code}): {err_msg}"
            }
        except Exception as ex:
            return {
                "status": "error",
                "message": f"Gemini Service Exception: {str(ex)}"
            }

    def stream_generate(
        self,
        prompt: str,
        agent: str = "ARKA",
        tier: str = "flash",
        history: Optional[List[Dict[str, Any]]] = None,
        enable_grounding: bool = False
    ) -> Generator[str, None, None]:
        """
        Streams chunks using server-sent chunks from Google Gemini.
        """
        model_name = self.resolve_model(tier)
        system_instruction_text = AGENT_SYSTEM_PROMPTS.get(agent.upper(), AGENT_SYSTEM_PROMPTS["ARKA"])
        
        contents = []
        if history:
            for msg in history:
                role = "user" if msg.get("role") in ["user", "human"] else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg.get("content", "")}]
                })
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "systemInstruction": {"parts": [{"text": system_instruction_text}]},
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 4096}
        }
        if enable_grounding or agent.upper() in ["NAYA", "FARREL"]:
            payload["tools"] = [{"googleSearch": {}}]

        endpoint = f"{self.base_url}/models/{model_name}:streamGenerateContent?alt=sse&key={self.api_key}"
        
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=90) as resp:
            for line in resp:
                line_str = line.decode("utf-8").strip()
                if line_str.startswith("data: "):
                    data_json = line_str[6:].strip()
                    if data_json:
                        try:
                            parsed = json.loads(data_json)
                            cands = parsed.get("candidates", [])
                            if cands:
                                parts = cands[0].get("content", {}).get("parts", [])
                                for p in parts:
                                    if "text" in p:
                                        yield p["text"]
                        except Exception:
                            pass


# CLI Dispatcher for Node.js backend integration
if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        gemini = GeminiService()
        
        if action == "test":
            res = gemini.generate("Halo, verifikasi sistem NEXUS AI aktif.", agent="ARKA", tier="lite")
            print(json.dumps(res, ensure_ascii=False, indent=2))
            
        elif action == "chat":
            input_data = sys.stdin.read()
            payload = json.loads(input_data) if input_data.strip() else {}
            prompt = payload.get("prompt", "")
            agent = payload.get("agent", "ARKA")
            tier = payload.get("tier", "flash")
            history = payload.get("history", [])
            enable_grounding = payload.get("enable_grounding", False)
            
            res = gemini.generate(
                prompt=prompt,
                agent=agent,
                tier=tier,
                history=history,
                enable_grounding=enable_grounding
            )
            print(json.dumps(res, ensure_ascii=False))
            
        elif action == "telemetry":
            if os.path.exists(TELEMETRY_LOG):
                with open(TELEMETRY_LOG, "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print(json.dumps([]))
    else:
        print("GeminiService CLI ready. Actions: test, chat, telemetry")
