/**
 * NEXUS AI ENTERPRISE — GOOGLE GEMINI CLIENT (NODE.JS)
 * ====================================================
 * Interconnects Node.js backend with Centralized Gemini Python Service / Native REST
 * Features automatic failover to native Google GenAI REST API for Serverless / Vercel deployment.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const BASE_DIR = path.resolve(__dirname, '..', '..');
const SCRIPT_PATH = path.join(BASE_DIR, 'services', 'gemini', 'gemini_service.py');
const PYTHON_EXEC = process.platform === 'win32' ? 'python' : 'python3';

class GeminiClient {
  static async chat({ prompt, agent = 'ARKA', tier = 'flash', history = [], enable_grounding = false }) {
    // Attempt local python orchestrator first
    try {
      return await GeminiClient.chatViaPython({ prompt, agent, tier, history, enable_grounding });
    } catch (pyErr) {
      console.warn('[GEMINI CLIENT] Python runner unavailable or failed, switching to native Direct REST API:', pyErr.message);
      return await GeminiClient.chatDirectRest({ prompt, agent, tier, history, enable_grounding });
    }
  }

  static async chatViaPython({ prompt, agent = 'ARKA', tier = 'flash', history = [], enable_grounding = false }) {
    return new Promise((resolve, reject) => {
      const child = spawn(PYTHON_EXEC, [SCRIPT_PATH, 'chat'], {
        cwd: BASE_DIR,
        env: { ...process.env, PYTHONIOENCODING: 'utf-8', PYTHONUTF8: '1' }
      });

      let stdout = '';
      let stderr = '';

      child.stdout.on('data', chunk => { stdout += chunk; });
      child.stderr.on('data', chunk => { stderr += chunk; });

      child.on('error', err => {
        reject(err);
      });

      child.on('close', code => {
        if (code !== 0 && !stdout.trim()) {
          return reject(new Error(stderr || `Gemini Python process exited with code ${code}`));
        }
        try {
          const result = JSON.parse(stdout.trim());
          resolve(result);
        } catch (e) {
          reject(new Error(`Failed to parse Gemini output: ${stdout || stderr}`));
        }
      });

      const payload = JSON.stringify({ prompt, agent, tier, history, enable_grounding });
      child.stdin.write(payload);
      child.stdin.end();
    });
  }

  static async chatDirectRest({ prompt, agent = 'ARKA', tier = 'flash', history = [], enable_grounding = false }) {
    const apiKey = process.env.GEMINI_API_KEY || '';
    if (!apiKey) {
      return {
        status: 'error',
        message: 'GEMINI_API_KEY belum dikonfigurasi di Environment Variable server.'
      };
    }

    const modelName = (tier === 'pro') ? 'gemini-2.5-pro' : (tier === 'lite' ? 'gemini-2.5-flash-lite' : 'gemini-2.5-flash');
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;

    const systemPrompts = {
      ARKA: "Anda adalah ARKA, Chief Executive, Strategic Director, dan Lead AI Orchestrator di NEXUS AI ENTERPRISE. Anda mampu memenuhi seluruh instruksi pengguna secara nyata: merancang website canggih, menyusun dokumen resmi, melakukan analisis strategis, dan memimpin tim agen otonom.",
      NAYA: "Anda adalah NAYA, Head of Business Intelligence & Lead Analyst di NEXUS AI. Anda menguasai riset mendalam, audit domain proses bisnis, domain data & informasi, serta integrasi satu data.",
      RAKA: "Anda adalah RAKA, Principal Full-Stack Engineer, Lead Software Architect, dan Master of Senior Fullstack & Fullstack Guardian di NEXUS AI ENTERPRISE. Anda menguasai pembuatan website profesional, modern, responsif, dan ultra-estetik (HTML5, TailwindCSS, modern JavaScript/React, Next.js, backend APIs, microservices, dan database). Ketika pengguna meminta Anda membuat website atau aplikasi web, Anda WAJIB memberikan kode sumber LENGKAP kelas produksi siap pakai, aman (tiga perspektif: Frontend, Backend, Security/OWASP), dan indah.",
      SEKAR: "Anda adalah SEKAR, Chief Financial & Compliance Auditor. Anda ahli dalam kelayakan anggaran TIK, kepatuhan regulasi Perpres 95/2018, dan tata naskah dinas baku KBBI.",
      DIMAS: "Anda adalah DIMAS, Lead IT Infrastructure & Security Officer. Anda ahli dalam domain infrastruktur, cloud computing, pusat data nasional, dan keamanan informasi bersertifikasi.",
      KIRANA: "Anda adalah KIRANA, Executive Document Specialist di NEXUS AI. Fokus Anda adalah penyusunan laporan resmi, naskah dinas, dokumen kebijakan, serta rekonstruksi format dokumen profesional."
    };
    const sysPrompt = systemPrompts[agent] || systemPrompts['ARKA'];

    const contents = [];
    if (Array.isArray(history)) {
      for (const h of history) {
        if (h.role && (h.text || h.content)) {
          contents.push({
            role: h.role === 'user' ? 'user' : 'model',
            parts: [{ text: h.text || h.content }]
          });
        }
      }
    }
    contents.push({
      role: 'user',
      parts: [{ text: prompt }]
    });

    const body = {
      contents,
      systemInstruction: {
        parts: [{ text: sysPrompt }]
      }
    };

    if (enable_grounding) {
      body.tools = [{ googleSearch: {} }];
    }

    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error?.message || `Gemini REST API error: HTTP ${res.status}`);
    }

    const candidate = data.candidates?.[0];
    const text = candidate?.content?.parts?.map(p => p.text).join('') || '';
    const groundingChunks = candidate?.groundingMetadata?.groundingChunks || [];
    const searchQueries = candidate?.groundingMetadata?.webSearchQueries || [];

    return {
      status: 'success',
      agent,
      tier,
      model: modelName,
      response: text,
      grounding: {
        search_queries: searchQueries,
        sources: groundingChunks.map(g => ({ title: g.web?.title, uri: g.web?.uri }))
      },
      tokens: data.usageMetadata || { promptTokenCount: 0, candidatesTokenCount: 0, totalTokenCount: 0 }
    };
  }

  static getTelemetry() {
    const logPath = path.join(BASE_DIR, 'logs', 'gemini_telemetry.json');
    if (fs.existsSync(logPath)) {
      try {
        return JSON.parse(fs.readFileSync(logPath, 'utf-8'));
      } catch (e) {
        return [];
      }
    }
    return [];
  }
}

module.exports = GeminiClient;
