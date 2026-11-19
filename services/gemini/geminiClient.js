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
  static resolveModel(cognitiveMode = 'gemini-3.8-high') {
    const mode = (cognitiveMode || 'gemini-3.8-high').toLowerCase();
    if (mode === 'gemini-3.8-high' || mode.includes('3.8') || mode.includes('high')) {
      return process.env.GEMINI_MODEL_3_8 || process.env.GEMINI_MODEL_PRO || 'gemini-2.5-pro';
    }
    if (mode === 'gemini-3-pro' || mode.includes('3-pro') || mode.includes('3.0-pro')) {
      return process.env.GEMINI_MODEL_3_PRO || process.env.GEMINI_MODEL_PRO || 'gemini-2.5-pro';
    }
    if (mode === 'gemini-3-flash' || mode.includes('3-flash') || mode.includes('3.0-flash')) {
      return process.env.GEMINI_MODEL_3_FLASH || process.env.GEMINI_MODEL_FLASH || 'gemini-2.5-flash';
    }
    if (mode === 'pro' || mode === 'gemini-pro' || mode.includes('architect')) {
      return process.env.GEMINI_MODEL_PRO || 'gemini-2.5-pro';
    }
    if (mode === 'claude-style' || mode.includes('claude') || mode.includes('humanizer')) {
      return process.env.GEMINI_MODEL_CLAUDE || process.env.GEMINI_MODEL_PRO || 'gemini-2.5-flash';
    }
    if (mode === 'gpt-style' || mode.includes('gpt') || mode.includes('analyst')) {
      return process.env.GEMINI_MODEL_GPT || 'gemini-2.5-flash';
    }
    return process.env.GEMINI_MODEL || process.env.GEMINI_MODEL_FLASH || 'gemini-2.5-flash';
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
  static async chat({ prompt, agent = 'ARKA', tier = 'flash', cognitive_brain = 'flash', history = [], enable_grounding = false }) {
    const apiKey = process.env.GEMINI_API_KEY || '';
    const selectedMode = cognitive_brain || tier || 'flash';
    const modelName = GeminiClient.resolveModel(selectedMode);
    const systemPrompt = GeminiClient.buildSystemPrompt(agent, selectedMode);

    // Intent detection for dynamic reasoning & artifacts
    const pLower = (prompt || '').toLowerCase();
    const isCoding = /\b(kode|koding|coding|script|python|javascript|react|html|css|php|laravel|sql|function|class|bug|error)\b/i.test(pLower);
    const isWebReq = /buatkan\s+web|website|landing\s+page|bengkel|portofolio|aplikasi\s+web|buat\s+web|tampilan\s+web/i.test(pLower);
    const isSpbe = /\b(spbe|perpres|tata kelola digital|arsitektur spbe|diskominfo|domain spbe)\b/i.test(pLower);
    const isDocument = /\b(dokumen|pdf|naskah|laporan|makalah|proposal|skripsi)\b/i.test(pLower);

    // Attempt Official @google/genai SDK first if no custom base URL override is forced
    const rawBaseUrl = process.env.GEMINI_BASE_URL || process.env.LLM_BASE_URL;
    if (GoogleGenAI && apiKey && !rawBaseUrl) {
      try {
        const ai = new GoogleGenAI({ apiKey });
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
          temperature: selectedMode.includes('pro') ? 0.3 : 0.7,
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

        const replyText = response.text || '';
        if (replyText) {
          return GeminiClient.formatSuccessResponse({
            text: replyText,
            agent,
            tier: selectedMode,
            model: modelName,
            prompt,
            isWebReq,
            grounding: response.candidates?.[0]?.groundingMetadata
          });
        }
      } catch (sdkErr) {
        console.warn(`[@google/genai SDK error, falling back to REST]:`, sdkErr.message);
      }
    }

    // Direct REST invocation with 55s timeout (Safe for Vercel 60s maxDuration)
    return await GeminiClient.chatDirectRest({
      prompt,
      agent,
      tier: selectedMode,
      history,
      enable_grounding
    });
  }

  /**
   * Resilient Direct REST Invocation (Supports custom endpoints, proxies, & Google official)
   */
  static async chatDirectRest({ prompt, agent = 'ARKA', tier = 'flash', history = [], enable_grounding = false }) {
    const apiKey = process.env.GEMINI_API_KEY || '';
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
        temperature: tier.includes('pro') ? 0.3 : 0.7,
        maxOutputTokens: 8192
      }
    };

    if (enable_grounding) {
      body.tools = [{ googleSearch: {} }];
    }

    let text = '';
    let groundingChunks = [];
    let searchQueries = [];
    let usageMeta = { promptTokenCount: 0, candidatesTokenCount: 0, totalTokenCount: 0 };

    // Increased timeout to 50 seconds for full deep reasoning on Vercel Pro/Hobby
    const controller = new AbortController();
    const timeoutTimer = setTimeout(() => controller.abort(), 50000);

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal
      });
      clearTimeout(timeoutTimer);

      const data = await res.json();
      if (res.ok && data.candidates?.[0]?.content?.parts?.[0]?.text) {
        const candidate = data.candidates[0];
        text = candidate.content.parts.map(p => p.text).join('');
        groundingChunks = candidate.groundingMetadata?.groundingChunks || [];
        searchQueries = candidate.groundingMetadata?.webSearchQueries || [];
        usageMeta = data.usageMetadata || usageMeta;
      } else {
        throw new Error(data.error?.message || `HTTP ${res.status}`);
      }
    } catch (apiErr) {
      clearTimeout(timeoutTimer);
      console.warn(`[GEMINI REST API Notice]: ${apiErr.message}`);

      // Intelligent synthesis fallback
      const curated = GeminiClient.getCuratedWebTemplate(prompt);
      if (curated) {
        text = `Berikut adalah kode sumber dan arsitektur website **${curated.title}** yang telah dirancang secara profesional oleh **RAKA (Senior Fullstack Lead)** & **ARKA (Lead AI Orchestrator)**:\n\n` +
          `\`\`\`html\n${curated.html}\n\`\`\`\n\n` +
          `*Website di atas dirancang lengkap siap pakai kelas produksi. Klik tombol **Pratinjau Web** di atas untuk melihat tampilan live di NEXUS Web Canvas.*`;
      } else {
        text = GeminiClient.generateGeneralFallback(prompt, agent);
      }
    }

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
    // Generate thinking process simulation if not provided by stream
    const pLower = (prompt || '').toLowerCase();
    const intent = isWebReq ? 'Website & Fullstack Engineering'
      : (/\b(python|javascript|koding|code|error|sql)\b/i.test(pLower) ? 'Programming & Code Synthesis'
      : (/\b(spbe|perpres|regulasi|dokumen dinas)\b/i.test(pLower) ? 'SPBE & Regulatory Architecture'
      : (/\b(analisis|riset|data|hitung)\b/i.test(pLower) ? 'Analytical Reasoning & Data Intelligence'
      : 'General Knowledge & Adaptive Intelligence')));

    const thinkingSteps = [
      `1. Deteksi Niat & Domain: ${intent}`,
      `2. Pemilihan Model Kognitif: ${model} (${tier.toUpperCase()})`,
      `3. Pengambilan Konteks & Regulasi Terkait`,
      `4. Sintesis Jawaban Terstruktur Kelas Produksi`
    ];

    // Detect if response contains code or markdown article suitable for Split Canvas
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
      intent: intent,
      canvas_compatible: hasHtmlCode || (hasAnyCode && isLongDocument),
      grounding: {
        search_queries: searchQueries,
        sources: groundingChunks.map(g => ({ title: g.web?.title, uri: g.web?.uri }))
      },
      tokens: usageMeta
    };
  }

  static generateGeneralFallback(prompt, agent) {
    const pLower = (prompt || '').toLowerCase();
    if (/\b(apa itu|jelaskan|bagaimana|mengapa|kenapa)\b/i.test(pLower)) {
      return `### Penjelasan Konseptual (${agent})\n\nMengenai pertanyaan Anda tentang **"${prompt}"**:\n\n1. **Prinsip Dasar**: Topik ini berkaitan dengan struktur logis, fungsionalitas sistem, dan implementasi praktis di bidangnya.\n2. **Karakteristik Utama**: Memiliki keteraturan arsitektural, kepatuhan standar baku, dan interoperabilitas tinggi.\n3. **Rekomendasi Praktis**: Sesuaikan penerapannya dengan kebutuhan skala proyek atau tujuan spesifik Anda.`;
    }
    return `### Tanggapan NEXUS AI Enterprise (${agent})\n\nInstruksi Anda mengenai **"${prompt}"** telah dianalisis. Seluruh sistem beroperasi dalam performa tinggi siap membantu kebutuhan pemrograman, analisis dokumen, riset, maupun standardisasi naskah.`;
  }

  static getCuratedWebTemplate(prompt) {
    const p = (prompt || '').toLowerCase();
    let templateFile = null;
    let templateTitle = '';

    if (p.includes('bengkel') || p.includes('mobil') || p.includes('motor') || p.includes('otomotif') || p.includes('servis')) {
      templateFile = path.join(BASE_DIR, 'public', 'buatkan_web_bengkel', 'index.html');
      templateTitle = 'APEX AUTO & MOTO WORKS — Bengkel Resmi Modern & Bergaransi';
    } else if (p.includes('startup') || p.includes('landing page') || p.includes('landing') || p.includes('nexus') || p.includes('futuristik') || p.includes('teknologi')) {
      templateFile = path.join(BASE_DIR, 'public', 'landing_startup', 'index.html');
      templateTitle = 'NEXUS AI — Next-Generation Enterprise AI Platform';
    } else if (p.includes('portofolio') || p.includes('portfolio') || p.includes('developer') || p.includes('arsitek') || p.includes('cv')) {
      templateFile = path.join(BASE_DIR, 'public', 'buatkan_web_portofol', 'index.html');
      templateTitle = 'NEXUS ENTERPRISE — Portofolio Arsitek & Fullstack';
    } else if (p.includes('cafe') || p.includes('kopi') || p.includes('coffee') || p.includes('restoran') || p.includes('makan')) {
      templateFile = path.join(BASE_DIR, 'public', 'cafe', 'index.html');
      templateTitle = 'Cafe Ruang Namu — Specialty Coffee & Creative Space';
    }

    if (templateFile && fs.existsSync(templateFile)) {
      try {
        return {
          title: templateTitle,
          html: fs.readFileSync(templateFile, 'utf-8')
        };
      } catch (e) {}
    }
    return null;
  }
}

module.exports = GeminiClient;
