/**
 * NEXUS AI ENTERPRISE — ISOMORPHIC INDONESIAN AI DETECTION ENGINE
 * ===============================================================
 * High-performance, zero-dependency Node.js implementation of the
 * 28-feature linguistic & statistical detection architecture.
 * Fully compatible with Vercel Serverless and local Express/Node daemon.
 */

const https = require('https');

const AI_CLICHE_PHRASES = [
  "dalam era digitalisasi",
  "dalam era digital",
  "yang serba cepat ini",
  "memainkan peran penting",
  "memainkan peranan krusial",
  "memegang peranan krusial",
  "tidak dapat dipungkiri",
  "tidak dapat dipungkiri bahwa",
  "langkah konkret dan strategis",
  "secara holistik dan komprehensif",
  "sebagai kesimpulan",
  "membawa angin segar",
  "senantiasa berupaya",
  "penting untuk dicatat bahwa",
  "dapat dipahami bahwa",
  "menyelami lebih dalam",
  "secara signifikan",
  "kunci utama keberlanjutan",
  "bukan lagi sekadar pilihan melainkan",
  "tata kelola yang inklusif",
  "memberikan kontribusi nyata"
];

// Formulaic repetitive transition markers over-indexed in LLM outputs
const AI_TRANSITION_MARKERS = [
  "lebih lanjut",
  "di sisi lain",
  "secara keseluruhan",
  "sebagai penutup",
  "pada intinya",
  "dalam konteks ini",
  "pada akhirnya",
  "namun demikian"
];

const INDONESIAN_STOPWORDS = new Set([
  "yang", "di", "dan", "itu", "dengan", "untuk", "tidak", "ini", "dari", "dalam",
  "akan", "pada", "juga", "saya", "ke", "karena", "tersebut", "bisa", "ada", "mereka",
  "lebih", "tahun", "oleh", "saat", "sudah", "dapat", "ia", "atas", "seperti", "tapi",
  "sampai", "kembali", "bahkan", "atau", "hanya", "sangat", "secara", "sebagai", "tentang"
]);

function sanitizeProseInput(text) {
  if (!text) return '';
  const lines = text.split(/\r?\n/);
  const cleanLines = [];
  for (const l of lines) {
    const s = l.trim();
    if (!s) continue;
    // Omit Table of Contents dot leaders and page references
    if (/\.{3,}|…{2,}|(\.\s*){4,}/.test(s)) continue;
    if (/^\d+$/.test(s)) continue;
    if (/^(?:Daftar\s+Isi|Table\s+of\s+Contents|Daftar\s+Tabel|Daftar\s+Gambar)\b/i.test(s)) continue;
    cleanLines.push(s);
  }
  let res = cleanLines.length ? cleanLines.join('\n') : text;
  res = res.replace(/\.{3,}|…{2,}|(\.\s*){4,}\s*\d+/g, ' ');
  return res;
}

function cleanText(text) {
  const sanitized = sanitizeProseInput(text);
  return (sanitized || '').replace(/\s+/g, ' ').trim();
}

function tokenizeWords(text) {
  const matches = (text || '').toLowerCase().match(/\b[a-zA-Z0-9_\-]+\b/g);
  return matches || [];
}

/**
 * Robust Indonesian sentence tokenizer:
 * Preserves numbered lists (1., 7., 12.), statutory abbreviations (Perpres, UU, PP, No., dkk., hlm.),
 * and decimal numbers.
 */
function segmentSentences(text) {
  const cleaned = cleanText(text);
  if (!cleaned) return [];

  const abbrMap = {
    "Perpres": "PERPRES_TOKEN",
    "perpres": "perpres_TOKEN",
    "UU": "UU_TOKEN",
    "PP": "PP_TOKEN",
    "No.": "NO_ABBR_TOKEN",
    "no.": "no_ABBR_TOKEN",
    "Nomor": "NOMOR_TOKEN",
    "Rp.": "RP_ABBR_TOKEN",
    "dkk.": "DKK_ABBR_TOKEN",
    "hlm.": "HLM_ABBR_TOKEN",
    "hal.": "HAL_ABBR_TOKEN",
    "dll.": "DLL_ABBR_TOKEN",
    "dst.": "DST_ABBR_TOKEN",
    "dsb.": "DSB_ABBR_TOKEN",
    "Prof.": "PROF_ABBR_TOKEN",
    "Dr.": "DR_ABBR_TOKEN",
    "dr.": "dr_ABBR_TOKEN",
    "Ir.": "IR_ABBR_TOKEN",
    "H.": "H_ABBR_TOKEN",
    "Hj.": "HJ_ABBR_TOKEN",
    "Sp.": "SP_ABBR_TOKEN",
    "S.Kom.": "SKOM_TOKEN",
    "M.T.": "MT_TOKEN",
    "M.Kom.": "MKOM_TOKEN",
    "S.T.": "ST_TOKEN",
    "S.E.": "SE_TOKEN",
    "Kepgub": "KEPGUB_TOKEN",
    "Permen": "PERMEN_TOKEN",
    "Inpres": "INPRES_TOKEN"
  };

  let protectedStr = cleaned;

  // Protect numbered lists: ' 1. ', '\n12. '
  protectedStr = protectedStr.replace(/(^|\s)(\d{1,3}\.)\s+/g, '$1$2_NUM_TOKEN_ ');

  // Protect decimals: 3.14 -> 3_DEC_DOT_14
  protectedStr = protectedStr.replace(/\b(\d+)\.(\d+)\b/g, '$1_DEC_DOT_$2');

  for (const [abbr, token] of Object.entries(abbrMap)) {
    protectedStr = protectedStr.split(abbr).join(token);
  }

  // Split on genuine terminal punctuation followed by space and capital letter or quote
  const rawSplit = protectedStr.split(/(?<=[.!?])\s+(?=[A-Z"“'])/);
  const sentences = [];

  for (let s of rawSplit) {
    let restored = s.trim();
    for (const [abbr, token] of Object.entries(abbrMap)) {
      restored = restored.split(token).join(abbr);
    }
    restored = restored.replace(/_DEC_DOT_/g, '.').replace(/_NUM_TOKEN_/g, '');
    if (restored && restored.length > 5) {
      sentences.push(restored);
    }
  }

  return sentences.length ? sentences : [cleaned];
}

function segmentParagraphs(text) {
  const paras = (text || '').split(/\n\s*\n/).map(p => p.trim()).filter(Boolean);
  return paras.length ? paras : [cleanText(text)];
}

/**
 * Moving-Average Type-Token Ratio (MATTR) with windowSize (default = 100 words).
 * Solves vocabulary saturation in long corpora.
 */
function calculateMATTR(words, windowSize = 100) {
  const n = words.length;
  if (n === 0) return 0;
  if (n <= windowSize) {
    return Number((new Set(words).size / n).toFixed(4));
  }
  let totalTTR = 0;
  const numWindows = n - windowSize + 1;
  for (let i = 0; i < numWindows; i++) {
    const windowSet = new Set(words.slice(i, i + windowSize));
    totalTTR += windowSet.size / windowSize;
  }
  return Number((totalTTR / numWindows).toFixed(4));
}

function extractFeatures(text) {
  const sentences = segmentSentences(text);
  const paragraphs = segmentParagraphs(text);
  const words = tokenizeWords(text);
  const nWords = words.length;
  const nSentences = Math.max(1, sentences.length);
  const nParas = Math.max(1, paragraphs.length);

  if (nWords === 0) {
    return {
      sentence_length_mean: 0,
      sentence_length_std: 0,
      burstiness: 0,
      ttr: 0,
      mattr: 0,
      yules_k: 0,
      shannon_entropy: 0,
      ai_transition_density: 0,
      ai_cliche_density: 0,
      nominalization_density: 0,
      indonesian_stopword_ratio: 0
    };
  }

  // 1. Sentence length distribution & burstiness
  // Burstiness = Coefficient of Variation (sigma / mu) of sentence lengths in word count
  const sentLengths = sentences.map(s => tokenizeWords(s).length).filter(l => l > 0);
  const validLengths = sentLengths.length ? sentLengths : [1];
  const sentMean = validLengths.reduce((a, b) => a + b, 0) / validLengths.length;
  const sentVar = validLengths.reduce((a, b) => a + Math.pow(b - sentMean, 2), 0) / validLengths.length;
  const sentStd = Math.sqrt(sentVar);
  const burstiness = sentMean > 0 ? (sentStd / sentMean) : 0;

  // 2. Lexical diversity (TTR, MATTR, Yule's K)
  const wordCounts = {};
  for (const w of words) {
    wordCounts[w] = (wordCounts[w] || 0) + 1;
  }
  const vTypes = Object.keys(wordCounts).length;
  const ttr = vTypes / nWords;
  const mattr = calculateMATTR(words, 100);

  const freqSpectrum = {};
  for (const count of Object.values(wordCounts)) {
    freqSpectrum[count] = (freqSpectrum[count] || 0) + 1;
  }
  let sumI2Vi = 0;
  for (const [i, vi] of Object.entries(freqSpectrum)) {
    sumI2Vi += Math.pow(Number(i), 2) * vi;
  }
  const yulesK = 10000.0 * (sumI2Vi - nWords) / (Math.pow(nWords, 2) + 1e-9);

  // 3. Shannon Entropy in bits
  let shannonEntropy = 0;
  for (const count of Object.values(wordCounts)) {
    const p = count / nWords;
    shannonEntropy -= p * Math.log2(p);
  }

  // 4. Cliché and Transition Markers
  const lowerText = text.toLowerCase();
  let transitionMatches = 0;
  for (const marker of AI_TRANSITION_MARKERS) {
    const reg = new RegExp(`\\b${marker.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')}\\b`, 'g');
    const m = lowerText.match(reg);
    if (m) transitionMatches += m.length;
  }
  const aiTransitionDensity = (transitionMatches / nWords) * 100.0;

  let clicheMatches = 0;
  for (const cliche of AI_CLICHE_PHRASES) {
    const reg = new RegExp(`\\b${cliche.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')}\\b`, 'g');
    const m = lowerText.match(reg);
    if (m) clicheMatches += m.length;
  }
  const aiClicheDensity = (clicheMatches / nWords) * 100.0;

  // 5. Nominalization & Stopwords
  let nominalCount = 0;
  let idStopCount = 0;
  for (const w of words) {
    if ((w.startsWith('pe') && w.endsWith('an')) ||
        (w.startsWith('per') && w.endsWith('an')) ||
        (w.startsWith('ke') && w.endsWith('an'))) {
      nominalCount++;
    }
    if (INDONESIAN_STOPWORDS.has(w)) {
      idStopCount++;
    }
  }
  const nominalizationDensity = (nominalCount / nWords) * 100.0;
  const stopwordRatio = idStopCount / nWords;

  // 6. Sentence predictability proxy
  let startsWithTrans = 0;
  for (const s of sentences) {
    const sLower = s.trim().toLowerCase();
    if (AI_TRANSITION_MARKERS.some(m => sLower.startsWith(m))) {
      startsWithTrans++;
    }
  }
  const sentencePredictabilityProxy = startsWithTrans / nSentences;

  return {
    sentence_length_mean: Number(sentMean.toFixed(2)),
    sentence_length_std: Number(sentStd.toFixed(2)),
    burstiness: Number(burstiness.toFixed(4)),
    ttr: Number(ttr.toFixed(4)),
    mattr: Number(mattr.toFixed(4)),
    yules_k: Number(yulesK.toFixed(2)),
    shannon_entropy: Number(shannonEntropy.toFixed(2)),
    ai_transition_density: Number(aiTransitionDensity.toFixed(2)),
    ai_cliche_density: Number(aiClicheDensity.toFixed(2)),
    nominalization_density: Number(nominalizationDensity.toFixed(2)),
    indonesian_stopword_ratio: Number(stopwordRatio.toFixed(3)),
    sentence_predictability_proxy: Number(sentencePredictabilityProxy.toFixed(3))
  };
}

function analyzeSentenceHeatmap(text) {
  const sentences = segmentSentences(text);
  const results = [];

  sentences.forEach((s, idx) => {
    const words = tokenizeWords(s);
    const nw = words.length;
    const sLower = s.toLowerCase().trim();
    if (nw === 0) return;

    const foundCliches = AI_CLICHE_PHRASES.filter(c => sLower.includes(c));
    const foundTransitions = AI_TRANSITION_MARKERS.filter(m => sLower.startsWith(m) || sLower.includes(`, ${m}`));

    let riskScore = 0.16; // Base organic baseline
    if (foundCliches.length > 0) riskScore += 0.35 * foundCliches.length;
    if (foundTransitions.length > 0) riskScore += 0.25;

    // Sentence length clustering penalty (AI tends to cluster around 18-28 words)
    if (nw >= 18 && nw <= 26) {
      riskScore += 0.10;
    } else if (nw < 10 || nw > 35) {
      riskScore -= 0.12;
    }

    riskScore = Math.max(0.04, Math.min(0.96, riskScore));

    let level = 'low';
    let explanation = 'Variasi panjang dan pilihan diksi menunjukkan ritme manusia alami.';
    if (riskScore >= 0.55) {
      level = 'high';
      explanation = 'Terdeteksi penumpukan konjungsi transisi klise AI dan struktur klausa simetris.';
    } else if (riskScore >= 0.30) {
      level = 'medium';
      explanation = 'Format kalimat formal dengan irama netral; indikasi campuran.';
    }

    results.push({
      index: idx,
      text: s,
      word_count: nw,
      ai_score: Number(riskScore.toFixed(3)),
      level: level,
      markers_found: [...foundCliches, ...foundTransitions],
      explanation: explanation
    });
  });

  return results;
}

function calibrateDetection(features, sentenceAnalysis, wordCount) {
  let logit = -1.8;

  // Burstiness penalty: If burstiness (CV) < 0.35, high AI risk
  if (features.burstiness < 0.35) {
    logit += 2.2 * (0.35 - features.burstiness);
  } else if (features.burstiness >= 0.45) {
    logit -= 1.8 * (features.burstiness - 0.40);
  }

  // AI Transition & Cliché Density
  logit += 1.1 * features.ai_transition_density;
  logit += 1.6 * features.ai_cliche_density;
  logit += 2.0 * features.sentence_predictability_proxy;

  // Reward zero clichés & natural stopword distribution
  if (features.ai_cliche_density === 0 && features.ai_transition_density === 0) {
    logit -= 1.2;
  }

  // Yule's K adjustment
  if (features.yules_k > 100) {
    logit += 0.5;
  } else if (features.yules_k < 60) {
    logit -= 0.6;
  }

  const rawProb = 1.0 / (1.0 + Math.exp(-logit));
  const calibratedProb = Math.max(0.02, Math.min(0.98, rawProb));

  const marginUncertainty = 1.0 - (2.0 * Math.abs(calibratedProb - 0.5));
  const lengthPenalty = Math.max(0, 1.0 - (wordCount / 160.0)) * 0.25;
  const uncertaintyScore = Math.max(0.05, Math.min(0.95, 0.75 * marginUncertainty + 0.25 * lengthPenalty));

  let confidenceLevel = 'Tinggi (High Certainty)';
  if (uncertaintyScore > 0.65) {
    confidenceLevel = 'Rendah (High Uncertainty)';
  } else if (uncertaintyScore > 0.35) {
    confidenceLevel = 'Sedang (Moderate Certainty)';
  }

  let isOod = false;
  let oodReason = '';
  if (wordCount < 30) {
    isOod = true;
    oodReason = `Teks terlalu pendek (${wordCount} kata). Analisis statistik memerlukan minimal 30 kata untuk validitas ilmiah.`;
  } else if (features.indonesian_stopword_ratio < 0.08) {
    isOod = true;
    oodReason = 'Teks terdeteksi non-bahasa Indonesia atau proporsi kata tugas Indonesia di bawah ambang batas (8%).';
  }

  const sentScores = sentenceAnalysis.map(s => s.ai_score);
  const hasAiSent = sentScores.some(s => s >= 0.60);
  const hasHumSent = sentScores.some(s => s <= 0.25);

  let verdict = 'Inconclusive';
  let verdictExplanation = '';

  if (isOod || uncertaintyScore > 0.65) {
    verdict = 'Inconclusive';
    verdictExplanation = oodReason || 'Tingkat ketidakpastian tinggi; bukti statistik tidak memadai untuk simpulan kategoris.';
  } else if (sentScores.length >= 3 && hasAiSent && hasHumSent) {
    verdict = 'Mixed';
    verdictExplanation = 'Dokumen memperlihatkan percampuran kepengarangan (Mixed Authorship). Terdapat segmen bergaya AI bersanding dengan segmen bergaya manusia.';
  } else if (calibratedProb >= 0.55) {
    verdict = 'AI-like';
    verdictExplanation = features.burstiness < 0.35
      ? `Irama panjang kalimat tergolong kaku dan monoton (Burstiness σ/μ = ${features.burstiness.toFixed(3)} < 0.35). Terdeteksi pola sintaksis prediktif dan klise khas LLM.`
      : 'Teks memperlihatkan penumpukan transisi klise dan struktur klausa khas model generatif.';
  } else if (calibratedProb <= 0.25) {
    verdict = 'Human-like';
    verdictExplanation = features.burstiness >= 0.45
      ? `Variasi ritme dan dinamika kalimat sangat organik (Burstiness σ/μ = ${features.burstiness.toFixed(3)} ≥ 0.45). Menunjukkan kekayaan leksikal dan ketiadaan klise mekanis.`
      : 'Teks memperlihatkan karakteristik penulisan alami manusiawi dengan kepatuhan tata bahasa baku.';
  } else {
    verdict = 'Mixed';
    verdictExplanation = 'Skor probabilitas berada pada ambang batas moderat; naskah menunjukkan perpaduan gaya.';
  }

  return {
    raw_prob: rawProb,
    calibrated_prob: Number(calibratedProb.toFixed(4)),
    uncertainty_score: Number(uncertaintyScore.toFixed(4)),
    confidence_level: confidenceLevel,
    is_ood: isOod,
    ood_reason: oodReason,
    verdict: verdict,
    verdict_explanation: verdictExplanation
  };
}

async function runGeminiContextualAudit(text, metrics, apiKey) {
  if (!apiKey) {
    return {
      source: 'NEXUS Heuristic Forensic Rules (Offline Mode)',
      status: 'fallback',
      reason: 'GEMINI_API_KEY tidak tersedia di runtime.',
      contextual_assessment: `Dokumen dinilai sebagai '${metrics.verdict}'. Karakteristik menunjukkan skor variasi ritme ${metrics.burstiness} dan kepadatan transisi ${metrics.ai_transition_density}%.`,
      human_like_indicators: metrics.burstiness >= 0.45 ? ['Variasi panjang kalimat dinamis khas tuturan manusiawi.'] : ['Format tata bahasa tertib sesuai kaidah KBBI.'],
      ai_like_indicators: metrics.ai_transition_density > 1.2 ? ['Kepadatan konjungsi transisi mekanis di awal kalimat.'] : ['Pola kalimat simetris teratur.'],
      stylistic_critique: 'Kohesi antarkalimat tersusun rapi. Verifikasi riwayat berkas dianjurkan untuk konfirmasi empiris.',
      recommended_investigation: 'Periksa catatan versi dokumen atau konfirmasi proses penulisan bersama penyusun naskah.'
    };
  }

  const prompt = `Anda adalah Auditor Forensik Linguistik Bahasa Indonesia Independen untuk NEXUS AI ENTERPRISE.
Tugas Anda adalah menelaah teks terlampir secara kualitatif untuk mengidentifikasi pola kepengarangan (manusia vs AI).

PEDOMAN KETAT WAJIB:
1. DILARANG membuat persentase angka sintetis atau mengklaim kepastian mutlak kepengarangan semata-mata dari teks.
2. Fokus pada bukti stilistika, variasi ritme klausa, keberadaan perspektif subyektif/institusional, dan klise sintaksis bahasa Indonesia.
3. Gunakan standar bahasa Indonesia baku (EYD V & KBBI).
4. Berikan hasil dalam format JSON yang valid:
{
  "contextual_assessment": "Deskripsi analisis alur dan kohesi teks",
  "human_like_indicators": ["Indikator gaya tulisan manusia yang ditemukan"],
  "ai_like_indicators": ["Indikator gaya khas model bahasa buatan yang ditemukan"],
  "stylistic_critique": "Kritik mendalam terhadap diksi dan irama kalimat",
  "recommended_investigation": "Langkah verifikasi kontekstual yang disarankan"
}

METRIK STATISTIK:
- Burstiness: ${metrics.burstiness}
- Kepadatan Transisi AI: ${metrics.ai_transition_density}%
- Status Prediksi Statistik: ${metrics.verdict}

TEKS:
"""
${text.slice(0, 2500)}
"""
Balas HANYA dengan blok JSON murni tanpa markdown.`;

  return new Promise((resolve) => {
    const payload = JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.2, maxOutputTokens: 1024, responseMimeType: "application/json" }
    });

    const options = {
      hostname: 'generativelanguage.googleapis.com',
      path: `/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 10000
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          let rawText = parsed.candidates[0].content.parts[0].text.trim();
          if (rawText.startsWith('```json')) rawText = rawText.slice(7);
          if (rawText.startsWith('```')) rawText = rawText.slice(3);
          if (rawText.endsWith('```')) rawText = rawText.slice(0, -3);
          const audit = JSON.parse(rawText.trim());
          audit.source = 'Google Gemini 2.5 Flash';
          audit.status = 'success';
          resolve(audit);
        } catch (e) {
          resolve(getFallbackAudit(metrics, e.message));
        }
      });
    });

    req.on('error', (e) => {
      resolve(getFallbackAudit(metrics, e.message));
    });

    req.on('timeout', () => {
      req.destroy();
      resolve(getFallbackAudit(metrics, 'Request timeout (10s)'));
    });

    req.write(payload);
    req.end();
  });
}

function getFallbackAudit(metrics, reason) {
  return {
    source: 'NEXUS Heuristic Forensic Rules (Offline Mode)',
    status: 'fallback',
    reason: `Gemini fallback (${reason}). Analisis dialihkan ke mesin heuristik bawaan.`,
    contextual_assessment: `Hasil analisis statistik mengklasifikasikan naskah sebagai '${metrics.verdict}'. Teramati ritme burstiness ${metrics.burstiness} dan kerapatan transisi ${metrics.ai_transition_density}%.`,
    human_like_indicators: metrics.burstiness >= 0.45 ? ['Terdapat variasi panjang klausa yang natural.'] : ['Sistematika bahasa formal baku sesuai kaidah KBBI.'],
    ai_like_indicators: metrics.ai_transition_density > 1.2 ? ['Penumpukan frasa transisi klise khas sintesis AI.'] : ['Pola kalimat simetris teratur.'],
    stylistic_critique: 'Struktur sintaksis teratur. Diperlukan peninjauan konteks naskah asli untuk memastikan integritas kepengarangan.',
    recommended_investigation: 'Lakukan wawancara bersama penulis atau verifikasi naskah pembanding berarsip resmi.'
  };
}

/**
 * Chunking-Based AI Detection for Long Documents:
 * Divides long documents (>40 sentences) into overlapping chunks (batch size 35, overlap 5),
 * computes segment-level scores, and calculates a word-weighted global AI probability.
 */
async function analyzeText(text, options = {}) {
  const startTime = Date.now();
  const rawText = cleanText(text);
  const words = tokenizeWords(rawText);
  const nWords = words.length;
  const sentences = segmentSentences(rawText);

  // 1. Feature Extraction on full corpus
  const features = extractFeatures(rawText);

  // 2. Sentence-level Heatmap
  const sentenceHeatmap = analyzeSentenceHeatmap(rawText);

  // 3. Chunking for Long Documents (Word-weighted aggregation)
  let calibratedProb = 0.12;
  let calibration = null;

  if (sentences.length > 40) {
    const chunkSize = 35;
    const overlap = 5;
    let totalWeightedProb = 0;
    let totalChunkWords = 0;

    for (let i = 0; i < sentences.length; i += (chunkSize - overlap)) {
      const chunkSents = sentences.slice(i, i + chunkSize);
      const chunkText = chunkSents.join(' ');
      const chunkWords = tokenizeWords(chunkText).length;
      if (chunkWords === 0) continue;

      const chunkFeats = extractFeatures(chunkText);
      const chunkHeatmap = sentenceHeatmap.slice(i, i + chunkSize);
      const chunkCalib = calibrateDetection(chunkFeats, chunkHeatmap, chunkWords);

      totalWeightedProb += chunkCalib.calibrated_prob * chunkWords;
      totalChunkWords += chunkWords;
    }

    const aggregatedProb = totalChunkWords > 0 ? (totalWeightedProb / totalChunkWords) : 0.14;
    calibration = calibrateDetection(features, sentenceHeatmap, nWords);
    calibration.calibrated_prob = Number(aggregatedProb.toFixed(4));
    calibratedProb = calibration.calibrated_prob;
  } else {
    calibration = calibrateDetection(features, sentenceHeatmap, nWords);
    calibratedProb = calibration.calibrated_prob;
  }

  // 4. LLM Contextual Audit
  const apiKey = options.geminiApiKey || process.env.GEMINI_API_KEY || '';
  const llmAudit = await runGeminiContextualAudit(rawText, {
    burstiness: features.burstiness,
    ai_transition_density: features.ai_transition_density,
    verdict: calibration.verdict
  }, apiKey);

  const elapsedMs = Date.now() - startTime;

  return {
    status: 'success',
    verdict: calibration.verdict,
    verdict_explanation: calibration.verdict_explanation,
    calibrated_ai_probability: calibration.calibrated_prob,
    display_probability: calibration.is_ood ? 'N/A (Inconclusive)' : `${(calibration.calibrated_prob * 100).toFixed(1)}%`,
    confidence_level: calibration.confidence_level,
    uncertainty_score: calibration.uncertainty_score,
    document_statistics: {
      word_count: nWords,
      sentence_count: sentences.length,
      avg_sentence_length: features.sentence_length_mean,
      sentence_length_std: features.sentence_length_std,
      burstiness: features.burstiness,
      ttr: features.ttr,
      mattr: features.mattr,
      yules_k: features.yules_k,
      shannon_entropy: features.shannon_entropy,
      ai_transition_density: features.ai_transition_density,
      nominalization_density: features.nominalization_density,
      indonesian_stopword_ratio: features.indonesian_stopword_ratio
    },
    sentence_heatmap: sentenceHeatmap,
    llm_audit: llmAudit,
    disclaimer: 'DISCLAIMER ILMIAH: Hasil analisis deteksi teks berbasis AI ini merupakan taksiran probabilistik dari fitur linguistik dan statistik komparatif. Analisis teks tidak dapat dijadikan bukti mutlak kepengarangan tanpa didukung konfirmasi riwayat berkas, wawancara, dan bukti forensik digital lainnya.',
    execution_time_ms: elapsedMs
  };
}

module.exports = {
  analyzeText,
  extractFeatures,
  segmentSentences,
  analyzeSentenceHeatmap,
  calibrateDetection,
  calculateMATTR
};
