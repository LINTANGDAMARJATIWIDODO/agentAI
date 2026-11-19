/**
 * NEXUS AI ENTERPRISE — GOOGLE GEMINI CLIENT (NODE.JS)
 * ====================================================
 * Unified, enterprise-grade Gemini integration with:
 * 1. Official @google/genai SDK + Native REST Failover
 * 2. General-Purpose AI Assistant (ChatGPT/Claude/Gemini Grade across all 12 knowledge domains)
 * 3. Deep Specialized SPBE & Indonesian Regulatory Intelligence
 * 4. Multi-Cognitive Brain Routing (Gemini Pro, Gemini Flash, Claude-Style, GPT-Style)
 * 5. Real-Time Web Grounding (Google Search)
 * 6. Extended Thinking Process & Autonomous Skills Execution
 */

const path = require('path');
const fs = require('fs');

const BASE_DIR = path.resolve(__dirname, '..', '..');

// Auto-load .env
if (!process.env.GEMINI_API_KEY) {
  const envFile = path.join(BASE_DIR, '.env');
  if (fs.existsSync(envFile)) {
    try {
      const rawEnv = fs.readFileSync(envFile, 'utf-8');
      rawEnv.split(/\r?\n/).forEach(line => {
        line = line.trim();
        if (line && !line.startsWith('#') && line.includes('=')) {
          const eqIdx = line.indexOf('=');
          const k = line.slice(0, eqIdx).trim();
          const v = line.slice(eqIdx + 1).trim().replace(/^['"]|['"]$/g, '');
          if (!process.env[k]) process.env[k] = v;
        }
      });
    } catch (e) {}
  }
}

let GoogleGenAI = null;
try {
  const genaiPkg = require('@google/genai');
  GoogleGenAI = genaiPkg.GoogleGenAI;
} catch (e) {}

class GeminiClient {
  /**
   * Resolve appropriate model identifier based on cognitive mode / tier
   */
  static resolveModel(cognitiveMode = 'gemini-2.5-flash') {
    const mode = (cognitiveMode || 'gemini-2.5-flash').toLowerCase();
    if (mode === 'gemini-2.5-pro' || mode.includes('2.5-pro') || mode.includes('pro') || mode.includes('architect') || mode.includes('deep')) {
      return process.env.GEMINI_MODEL_PRO || 'gemini-2.5-pro';
    }
    if (mode === 'claude-style' || mode.includes('claude') || mode.includes('editorial') || mode.includes('humanizer')) {
      return process.env.GEMINI_MODEL_CLAUDE || process.env.GEMINI_MODEL_PRO || 'gemini-2.5-pro';
    }
    if (mode === 'gpt-style' || mode.includes('gpt') || mode.includes('analyst')) {
      return process.env.GEMINI_MODEL_GPT || process.env.GEMINI_MODEL_FLASH || 'gemini-2.5-flash';
    }
    return process.env.GEMINI_MODEL_FLASH || 'gemini-2.5-flash';
  }

  /**
   * System Prompt Generator: True General-Purpose Assistant with Specialized SPBE Intelligence
   */
  static buildSystemPrompt(agent = 'ARKA', cognitiveMode = 'flash') {
    const mode = (cognitiveMode || 'flash').toLowerCase();

    // Persona-specific flavoring
    let personaBio = "Anda adalah ARKA, Lead AI Orchestrator & Principal Enterprise Assistant di NEXUS AI ENTERPRISE.";
    if (agent === 'RAKA') {
      personaBio = "Anda adalah RAKA, Principal Full-Stack Engineer & Lead Software Architect di NEXUS AI ENTERPRISE.";
    } else if (agent === 'NAYA') {
      personaBio = "Anda adalah NAYA, Head of Business Intelligence & Lead Researcher di NEXUS AI ENTERPRISE.";
    } else if (agent === 'SEKAR') {
      personaBio = "Anda adalah SEKAR, Chief Financial, Legal & Compliance Auditor di NEXUS AI ENTERPRISE.";
    } else if (agent === 'DIMAS') {
      personaBio = "Anda adalah DIMAS, Lead IT Infrastructure, Cloud & Operations Director di NEXUS AI ENTERPRISE.";
    } else if (agent === 'KIRANA') {
      personaBio = "Anda adalah KIRANA, Lead Linguistic Specialist & Executive Editorial Director di NEXUS AI ENTERPRISE.";
    }

    // Cognitive style guidance
    let cognitiveGuidance = "";
    if (mode === 'claude-style' || mode.includes('claude')) {
      cognitiveGuidance = `
[COGNITIVE STYLE: CLAUDE-STYLE EDITORIAL & ORGANIC WRITING]
- Gunakan bahasa yang hidup, jernih, dan memiliki variasi ritme klausa tinggi (High Burstiness > 0.55).
- Hindari frasa klise robotik generik seperti "dalam era digital", "memainkan peran krusial", "secara holistik".
- Berikan wawasan mendalam dengan nuansa elegan, presisi leksikal KBBI V, dan kejernihan konseptual.`;
    } else if (mode === 'gpt-style' || mode.includes('gpt')) {
      cognitiveGuidance = `
[COGNITIVE STYLE: GPT-STYLE STRUCTURED ANALYST]
- Gunakan pendekatan penalaran bertingkat, taksonomi terstruktur, dan matriks keputusan jelas.
- Pecah masalah kompleks menjadi langkah-langkah analitis berurutan (Step-by-step breakdown).`;
    } else if (mode === 'pro' || mode.includes('pro')) {
      cognitiveGuidance = `
[COGNITIVE STYLE: DEEP REASONING & SYSTEMS ARCHITECT]
- Lakukan analisis multi-dimensi secara komprehensif, telaah akar masalah teknis, arsitektural, dan regulasi.`;
    }

    return `${personaBio}

[IDENTITAS & PERAN UTAMA: GENERAL-PURPOSE AI ASSISTANT]
NEXUS AI adalah asisten kecerdasan buatan serbaguna kelas dunia (setara ChatGPT, Claude, dan Gemini).
Anda BUKAN hanya asisten SPBE. Anda BEBAS dan MAMPU berdiskusi mengenai SEGALA TOPIK:
1. PENGETAHUAN UMUM: Sejarah, sains, geografi, filsafat, budaya, astronomi, dan fenomena dunia.
2. PENDIDIKAN & AKADEMIK: Matematika, fisika, kimia, biologi, linguistik, statistik, dan materi perkuliahan/sekolah.
3. PEMROGRAMAN & KODING: Python, JavaScript, TypeScript, React, Next.js, Node.js, PHP, Laravel, Java, C++, Go, Rust, SQL, arsitektur database, debugging, dan integrasi REST/GraphQL API.
4. SOFTWARE ENGINEERING: Desain sistem mikroservis, cloud computing (AWS, GCP, Vercel, Docker, K8s), keamanan siber (OWASP), dan UI/UX modern.
5. KECERDASAN BUATAN & DATA: Machine learning, deep learning, NLP, arsitektur LLM, prompt engineering, data engineering, dan visualisasi data.
6. BISNIS & STRATEGI: Model bisnis, kewirausahaan, pemasaran digital, keuangan, analisis pasar, pitch deck, dan manajemen produk.
7. PENULISAN & PENYUNTINGAN: Pembuatan artikel, esai, proposal, naskah dinas, dokumen teknis, email profesional, dan penulisan kreatif.
8. RISET & ANALISIS: Tinjauan literatur, sintesis informasi, perbandingan metodologi, dan perumusan kesimpulan empiris.
9. ASISTEN HARIAN & PRODUKTIVITAS: Brainstorming ide, penyusunan jadwal, pemecahan masalah praktis, dan perencanaan kegiatan.
10. TATA KELOLA PEMERINTAHAN & SPBE (LAPISAN KEKEAHLIAN SPESIALIS TERTINGGI):
    Ketika pengguna menanyakan SPBE, Anda memiliki kepakaran mendalam mengenai Perpres 95/2018, Perpres 132/2022, 6 Domain SPBE (Proses Bisnis, Data & Informasi, Layanan, Aplikasi, Infrastruktur, Keamanan), Integrasi Satu Data, Tata Naskah Dinas Baku KBBI & EYD V, dan kode teknis (DAB, DAD, DAL, DAA, INI-xx, G-xx). SPBE adalah keunggulan spesialisasi Anda, BUKAN batas pengetahuan Anda!

[PANDUAN PEMAHAMAN INTENT & RESPON]:
- Jawab secara langsung, relevan, cerdas, dan tidak kaku.
- Jawab singkat dan to-the-point jika pertanyaannya sederhana; berikan penjelasan terstruktur dan mendalam jika pertanyaannya kompleks.
- Pahami konteks percakapan multi-turn tanpa meminta pengguna mengulang informasi yang sudah ada di riwayat.
- Dukung bahasa Indonesia (formal baku maupun santai) dan bahasa Inggris.
${cognitiveGuidance}

[PROTOKOL PEMBUATAN WEBSITE & KODE WEB]:
Jika pengguna meminta pembuatan website, landing page, atau aplikasi web:
1. Hasilkan KODE LENGKAP UTUH dari <!DOCTYPE html> sampai </html> di dalam blok kode \`\`\`html.
2. Gunakan TailwindCSS CDN dan FontAwesome 6 dengan desain modern, estetik, responsif (mobile/desktop), dan interaktif.

[PROTOKOL VISUAL DIAGRAM & FLOWCHART (MERMAID.JS)]:
Jika pengguna meminta diagram, alur proses bisnis, flowchart, sequence diagram, arsitektur sistem, ERD database, mindmap, atau Gantt chart:
1. Hasilkan diagram menggunakan sintaks Mermaid.js di dalam blok kode \`\`\`mermaid ... \`\`\`.
2. Selalu gunakan tanda kutip dua untuk teks label node yang mengandung karakter khusus (misal: id["Proses Utama (Aktif)"]).
3. Jangan sertakan tag HTML di dalam label node.
4. Diagram akan otomatis di-render oleh Visual Architecture Studio di Split Canvas dengan kontrol interaktif Zoom In, Zoom Out, Reset, dan Ekspor SVG/PNG.`;
  }

  /**
   * Main Chat Dispatcher: Uses @google/genai SDK when available, with resilient REST failover
   */
    /**
   * Main Chat Dispatcher: Uses official @google/genai SDK (v1beta) with resilient Direct REST failover
   */
  static async chat({ prompt, agent = 'ARKA', tier = 'gemini-2.5-flash', cognitive_brain = 'gemini-2.5-flash', history = [], enable_grounding = false }) {
    const apiKey = process.env.GEMINI_API_KEY || '';
    if (!apiKey) {
      throw new Error('GEMINI_API_KEY tidak ditemukan di environment server. Pastikan API Key telah diatur di Vercel Environment Variables atau .env.');
    }

    const selectedMode = cognitive_brain || tier || 'gemini-2.5-flash';
    const modelName = GeminiClient.resolveModel(selectedMode);
    const systemPrompt = GeminiClient.buildSystemPrompt(agent, selectedMode);
    const isWebReq = /buatkan\s+web|website|landing\s+page|bengkel|portofolio|aplikasi\s+web|buat\s+web|tampilan\s+web/i.test(prompt);

    // 1. Official @google/genai SDK invocation (using apiVersion v1beta)
    if (GoogleGenAI && apiKey && !process.env.GEMINI_BASE_URL) {
      try {
        const ai = new GoogleGenAI({ apiKey, httpOptions: { apiVersion: 'v1beta' } });
        const contents = [];

        if (Array.isArray(history)) {
          for (const h of history) {
            const role = h.role === 'user' ? 'user' : 'model';
            const content = h.text || h.content || '';
            if (content) {
              contents.push({ role, parts: [{ text: content }] });
            }
          }
        }
        contents.push({ role: 'user', parts: [{ text: prompt }] });

        const config = {
          systemInstruction: { parts: [{ text: systemPrompt }] },
          temperature: (selectedMode.includes('pro') || selectedMode.includes('claude')) ? 0.3 : 0.7,
          maxOutputTokens: 8192
        };

        if (enable_grounding) {
          config.tools = [{ googleSearch: {} }];
        }

        const response = await ai.models.generateContent({
          model: modelName,
          contents: contents,
          config: config
        });

        const replyText = response.text || (response.candidates?.[0]?.content?.parts?.[0]?.text) || '';
        if (replyText) {
          const usage = response.usageMetadata || {};
          const totalToks = usage.totalTokenCount || 0;
          return GeminiClient.formatSuccessResponse({
            text: replyText,
            agent,
            tier: selectedMode,
            model: modelName,
            prompt,
            isWebReq,
            groundingChunks: response.candidates?.[0]?.groundingMetadata?.groundingChunks || [],
            searchQueries: response.candidates?.[0]?.groundingMetadata?.webSearchQueries || [],
            usageMeta: {
              total_tokens: totalToks,
              totalTokenCount: totalToks,
              prompt_tokens: usage.promptTokenCount || 0,
              promptTokenCount: usage.promptTokenCount || 0,
              candidates_tokens: usage.candidatesTokenCount || 0,
              candidatesTokenCount: usage.candidatesTokenCount || 0
            }
          });
        }
      } catch (sdkErr) {
        console.warn('[@google/genai SDK notice, falling back to REST]:', sdkErr.message);
        // Note: We proceed to REST failover below
      }
    }

    // 2. Direct REST invocation
    return await GeminiClient.chatDirectRest({
      prompt,
      agent,
      tier: selectedMode,
      history,
      enable_grounding
    });
  }

  /**
   * Resilient Direct REST Invocation
   */
  static async chatDirectRest({ prompt, agent = 'ARKA', tier = 'gemini-2.5-flash', history = [], enable_grounding = false }) {
    const apiKey = process.env.GEMINI_API_KEY || '';
    if (!apiKey) {
      throw new Error('GEMINI_API_KEY belum dikonfigurasikan di environment server.');
    }

    const isWebReq = /buatkan\s+web|website|landing\s+page|bengkel|portofolio|aplikasi\s+web|buat\s+web|tampilan\s+web/i.test(prompt);
    const modelName = GeminiClient.resolveModel(tier);
    const sysPrompt = GeminiClient.buildSystemPrompt(agent, tier);

    const rawBaseUrl = (process.env.GEMINI_BASE_URL || process.env.LLM_BASE_URL || 'https://generativelanguage.googleapis.com').replace(/\/+$/, '');
    const url = rawBaseUrl.includes('/models')
      ? `${rawBaseUrl}/${modelName}:generateContent?key=${apiKey}`
      : `${rawBaseUrl}/v1beta/models/${modelName}:generateContent?key=${apiKey}`;

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
      },
      generationConfig: {
        temperature: (tier.includes('pro') || tier.includes('claude')) ? 0.3 : 0.7,
        maxOutputTokens: 8192
      }
    };

    if (enable_grounding) {
      body.tools = [{ googleSearch: {} }];
    }

    const controller = new AbortController();
    const timeoutTimer = setTimeout(() => controller.abort(), 50000);

    let res;
    let data;
    try {
      res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal
      });
      clearTimeout(timeoutTimer);
      data = await res.json();
    } catch (fetchErr) {
      clearTimeout(timeoutTimer);
      throw new Error(`Koneksi ke Google Gemini API gagal: ${fetchErr.message}`);
    }

    if (!res.ok || !data.candidates?.[0]?.content?.parts?.[0]?.text) {
      const errMsg = data?.error?.message || `HTTP ${res.status}: Gagal memproses balasan dari model ${modelName}`;
      throw new Error(`Google Gemini Error (${modelName}): ${errMsg}`);
    }

    const candidate = data.candidates[0];
    const text = candidate.content.parts.map(p => p.text).join('');
    const groundingChunks = candidate.groundingMetadata?.groundingChunks || [];
    const searchQueries = candidate.groundingMetadata?.webSearchQueries || [];
    const u = data.usageMetadata || {};
    const totalToks = u.totalTokenCount || 0;

    const usageMeta = {
      total_tokens: totalToks,
      totalTokenCount: totalToks,
      prompt_tokens: u.promptTokenCount || 0,
      promptTokenCount: u.promptTokenCount || 0,
      candidates_tokens: u.candidatesTokenCount || 0,
      candidatesTokenCount: u.candidatesTokenCount || 0
    };

    return GeminiClient.formatSuccessResponse({
      text,
      agent,
      tier,
      model: modelName,
      prompt,
      isWebReq,
      groundingChunks,
      searchQueries,
      usageMeta
    });
  }

  /**
   * Universal response formatter with cognitive thinking metadata & artifact detection
   */
  static formatSuccessResponse({ text, agent, tier, model, prompt, isWebReq, groundingChunks = [], searchQueries = [], usageMeta = {} }) {
    const pLower = (prompt || '').toLowerCase();
    const intent = isWebReq ? 'Website & Fullstack Engineering'
      : (/\b(python|javascript|koding|code|error|sql)\b/i.test(pLower) ? 'Programming & Code Synthesis'
      : (/\b(spbe|perpres|regulasi|dokumen dinas)\b/i.test(pLower) ? 'SPBE & Regulatory Architecture'
      : (/\b(analisis|riset|data|hitung)\b/i.test(pLower) ? 'Analytical Reasoning & Data Intelligence'
      : 'General Knowledge & Adaptive Intelligence')));

    const totalTok = usageMeta.totalTokenCount || usageMeta.total_tokens || 0;

    const thinkingSteps = [
      `1. Deteksi Niat & Domain: ${intent}`,
      `2. Pemilihan Model Kognitif: ${model} (${tier.toUpperCase()})`,
      `3. Eksekusi Penalaran Multimodal Realtime`,
      `4. Total Token Digunakan: ${totalTok.toLocaleString()} tok`
    ];

    const hasHtmlCode = /```html\s*<!DOCTYPE html[\s\S]*?<\/html>\s*```/i.test(text);
    const hasAnyCode = /```[a-z0-9_-]+\n[\s\S]*?```/i.test(text);
    const isLongDocument = text.length > 1200;

    return {
      status: 'success',
      agent,
      tier,
      model,
      response: text,
      text: text,
      thinking: thinkingSteps.join('\n'),
      intent,
      canvas_compatible: hasHtmlCode || (hasAnyCode && isLongDocument),
      grounding: {
        search_queries: searchQueries,
        sources: groundingChunks.map(g => ({ title: g.web?.title, uri: g.web?.uri }))
      },
      grounding_sources: groundingChunks.map(g => ({ title: g.web?.title, uri: g.web?.uri })),
      tokens: usageMeta
    };
  }
}

module.exports = GeminiClient;
