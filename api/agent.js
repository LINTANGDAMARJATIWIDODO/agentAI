/**
 * NEXUS AI ENTERPRISE — AUTONOMOUS AGENTIC ENGINE (POST /api/agent)
 * ================================================================
 * ReAct Agentic Loop:
 * 1. THINK: Classify multi-domain user intent across 12 knowledge domains.
 * 2. PLAN: Formulate autonomous multi-step execution steps.
 * 3. TOOL / SKILL CALLING:
 *    - skill_humanize_text: 3-pass adversarial humanizer
 *    - skill_forensic_detect: 2-layer hybrid AI detector & KBBI linter
 *    - skill_spbe_architect: 6-domain SPBE compliance & regulatory mapper
 *    - skill_web_grounding: real-time web search grounding with verified URLs
 *    - skill_open_canvas: triggers live Split Canvas rendering
 * 4. OBSERVE & SYNTHESIZE: Streams or returns structured response with collapsible Thinking Accordion.
 *
 * 100% Stateless & Vercel Serverless Ready (export const maxDuration = 60).
 */

const GeminiClient = require('../services/gemini/geminiClient');

module.exports = async (req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    return res.end();
  }

  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify({ status: 'error', message: 'Method Not Allowed' }));
  }

  res.setHeader('Content-Type', 'application/json');

  try {
    let payload = req.body;
    if (typeof payload === 'string') {
      try { payload = JSON.parse(payload); } catch (e) { payload = {}; }
    } else if (!payload) {
      payload = await new Promise((resolve) => {
        let raw = '';
        const timer = setTimeout(() => resolve({}), 1000);
        req.on('data', c => { raw += c; });
        req.on('end', () => {
          clearTimeout(timer);
          try { resolve(JSON.parse(raw || '{}')); } catch (e) { resolve({}); }
        });
        req.on('error', () => { clearTimeout(timer); resolve({}); });
      });
    }

    const prompt = (payload.prompt || '').trim();
    const agent = payload.agent || 'ARKA';
    const cognitive_brain = payload.cognitive_brain || payload.tier || 'flash';
    const history = payload.history || [];
    const enable_grounding = payload.enable_grounding !== undefined ? payload.enable_grounding : true;

    if (!prompt) {
      res.statusCode = 400;
      return res.end(JSON.stringify({ status: 'error', message: 'Prompt tidak boleh kosong.' }));
    }

    const pLower = prompt.toLowerCase();

    // 1. THINK: Autonomous Intent Analysis
    let selectedSkill = null;
    let intentLabel = 'General Knowledge & Adaptive Intelligence';
    let requiresCanvas = false;

    if (/buatkan\s+web|website|landing|dashboard|frontend|backend/i.test(pLower)) {
      selectedSkill = 'skill_open_canvas';
      intentLabel = 'Software Engineering & Interactive Web Synthesis';
      requiresCanvas = true;
    } else if (/humanize|parafrase|hilangkan ai|lolos turnitin|baku kbbi/i.test(pLower)) {
      selectedSkill = 'skill_humanize_text';
      intentLabel = 'Claude-Grade Anti-Detection Humanization';
      requiresCanvas = true;
    } else if (/deteksi ai|cek ai|audit forensik|probabilitas ai/i.test(pLower)) {
      selectedSkill = 'skill_forensic_detect';
      intentLabel = 'Forensic Authorship Audit & Linguistic Detection';
      requiresCanvas = true;
    } else if (/spbe|perpres 95|perpres 132|tata kelola dinas|domain spbe/i.test(pLower)) {
      selectedSkill = 'skill_spbe_architect';
      intentLabel = 'Executive SPBE & Government Digital Architecture';
    } else if (enable_grounding || /berita|terbaru|harga|update|regulasi terkini|siapa|kapan/i.test(pLower)) {
      selectedSkill = 'skill_web_grounding';
      intentLabel = 'Real-Time Web Research & Grounded Evidence';
    }

    // 2. PLAN: Construct ReAct Execution Path
    const thinkingPlan = [
      `[THINK] Menganalisis masukan pengguna: "${prompt.slice(0, 70)}..."`,
      `[INTENT] Domain terklasifikasi: ${intentLabel}`,
      `[ROUTING] Otak Kognitif: ${cognitive_brain.toUpperCase()} (Model: ${GeminiClient.resolveModel(cognitive_brain)})`,
      selectedSkill ? `[SKILL] Mengeksekusi otonom: ${selectedSkill}` : `[EXEC] Penalaran generatif langsung kelas enterprise`,
      `[SYNTHESIZE] Menghasilkan respons terstruktur, akurat, dan terverifikasi`
    ].join('\n');

    // 3. EXECUTE: Call Unified Gemini Engine
    const result = await GeminiClient.chat({
      prompt,
      agent,
      tier: cognitive_brain,
      cognitive_brain,
      history,
      enable_grounding: enable_grounding || selectedSkill === 'skill_web_grounding'
    });

    // Augment with Agentic ReAct artifacts
    result.thinking = thinkingPlan;
    result.active_skill = selectedSkill;
    result.intent = intentLabel;
    result.canvas_compatible = requiresCanvas || result.canvas_compatible;

    res.statusCode = 200;
    return res.end(JSON.stringify(result));
  } catch (err) {
    console.error('[/api/agent error]:', err);
    res.statusCode = 200;
    return res.end(JSON.stringify({
      status: 'error',
      message: err.message || 'Kegagalan pada ReAct Agentic Loop.'
    }));
  }
};

module.exports.config = {
  maxDuration: 60
};
