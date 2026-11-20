/**
 * NEXUS AI ENTERPRISE — GOOGLE GEMINI CLIENT (NODE.JS)
 * ====================================================
 * Unified, enterprise-grade Gemini integration with:
 * 1. Multi-Key Rotation Pool: key2 -> key3 -> GEMINI_API_KEYS -> GEMINI_API_KEY
 * 2. Cascading Models: gemini-2.5-flash -> gemini-2.5-flash-lite -> gemini-3.6-flash -> gemini-3.5-flash
 * 3. Official @google/genai SDK (v1beta) compatible with standard & AQ. keys
 * 4. General-Purpose AI Assistant (ChatGPT/Claude/Gemini Grade across all knowledge domains)
 * 5. Deep Specialized SPBE & Indonesian Regulatory Intelligence
 * 6. Multi-Cognitive Brain Routing (Gemini Pro, Gemini Flash, Claude-Style, GPT-Style)
 * 7. Real-Time Web Grounding (Google Search)
 */

const path = require('path');
const fs = require('fs');
const { getApiKeyPool } = require('./apiKeyPool');

const BASE_DIR = path.resolve(__dirname, '..', '..');

let GoogleGenAI = null;
try {
  const genaiPkg = require('@google/genai');
  GoogleGenAI = genaiPkg.GoogleGenAI;
} catch (e) {
  console.warn('[@google/genai import warning in geminiClient]:', e.message);
}

class GeminiClient {
  /**
   * Resolve appropriate model identifier based on cognitive mode / tier
   */
  static resolveModel(cognitiveMode = 'gemini-2.5-flash') {
    const mode = (cognitiveMode || 'gemini-2.5-flash').toLowerCase();
    if (mode === 'gemini-2.5-pro' || mode.includes('pro') || mode.includes('architect') || mode.includes('deep')) {
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
${cognitiveGuidance}

[KAPABILITAS SISTEM & STANDAR TANGGAPAN]
1. Anda adalah asisten kecerdasan buatan tingkat enterprise yang menguasai seluruh spektrum pengetahuan (pemrograman fullstack, arsitektur sistem, sains data, hukum, manajemen bisnis, dan kebijakan publik).
2. Jawaban wajib substantif, langsung ke inti permasalahan, dan menyajikan solusi konkret (termasuk kode lengkap jika diminta).
3. Untuk konteks tata kelola pemerintahan Indonesia, patuhi ketentuan Perpres No. 95/2018 (SPBE), Perpres No. 39/2019 (Satu Data Indonesia), dan UU No. 27/2022 (Pelindungan Data Pribadi).
4. Gunakan bahasa Indonesia baku, lugas, dan profesional sesuai standar KBBI dan EYD V.
5. Bila menghasilkan diagram sistem atau alur proses, gunakan format fenced code block \`\`\`mermaid ... \`\`\`.`;
  }

  /**
   * Main Chat Dispatcher: Uses official @google/genai SDK (v1beta) with Multi-Key Pool & Model Cascade
   */
  static async chat({ prompt, agent = 'ARKA', tier = 'gemini-2.5-flash', cognitive_brain = 'gemini-2.5-flash', history = [], enable_grounding = false }) {
    if (!prompt || !prompt.trim()) {
      throw new Error('Prompt input tidak boleh kosong.');
    }

    const keyPool = getApiKeyPool();
    if (!keyPool.length) {
      throw new Error('Tidak ada API Key Gemini yang terkonfigurasi pada server (key2, key3, GEMINI_API_KEYS, GEMINI_API_KEY).');
    }

    const selectedMode = cognitive_brain || tier || 'gemini-2.5-flash';
    const primaryModel = GeminiClient.resolveModel(selectedMode);
    const systemPrompt = GeminiClient.buildSystemPrompt(agent, selectedMode);
    const isWebReq = /buatkan\s+web|website|landing\s+page|bengkel|portofolio|aplikasi\s+web|buat\s+web|tampilan\s+web/i.test(prompt);

    const modelCascade = [
      primaryModel,
      'gemini-2.5-flash',
      'gemini-2.5-flash-lite',
      'gemini-3.6-flash',
      'gemini-3.5-flash'
    ].filter((m, i, arr) => arr.indexOf(m) === i);

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

    let lastError = null;

    for (const model of modelCascade) {
      for (let keyIdx = 0; keyIdx < keyPool.length; keyIdx++) {
        const currentApiKey = keyPool[keyIdx];

        try {
          if (GoogleGenAI) {
            const ai = new GoogleGenAI({ apiKey: currentApiKey, apiVersion: 'v1beta' });
            const configObj = {
              systemInstruction: { parts: [{ text: systemPrompt }] },
              temperature: (selectedMode.includes('pro') || selectedMode.includes('claude')) ? 0.3 : 0.7,
              maxOutputTokens: 8192
            };
            if (enable_grounding) {
              configObj.tools = [{ googleSearch: {} }];
            }

            const response = await ai.models.generateContent({
              model: model,
              contents: contents,
              config: configObj
            });

            const replyText = response.text || (response.candidates?.[0]?.content?.parts?.[0]?.text) || '';
            if (replyText) {
              const cand = response.candidates?.[0] || {};
              const groundingChunks = cand.groundingMetadata?.groundingChunks || [];
              const searchQueries = cand.groundingMetadata?.webSearchQueries || [];
              const usage = response.usageMetadata || {};
              const totalToks = usage.totalTokenCount || 0;

              return GeminiClient.formatSuccessResponse({
                text: replyText,
                agent,
                tier: selectedMode,
                model: model,
                prompt,
                isWebReq,
                groundingChunks,
                searchQueries,
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
          }
        } catch (err) {
          lastError = err;
          const msg = (err.message || String(err)).toLowerCase();
          console.warn(`[GeminiClient Model ${model} | Key #${keyIdx + 1}/${keyPool.length}]:`, err.message);

          if (msg.includes('404') || msg.includes('not found') || msg.includes('no longer available') || msg.includes('not supported')) {
            break; // skip to next model
          }

          continue; // try next key for this model
        }
      }
    }

    throw lastError || new Error('Seluruh kombinasi API Key dan Model dalam pool rotasi gagal memproses permintaan chat.');
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
