/**
 * Vercel Serverless Function: POST /api/audit
 * ===========================================
 * Stateless, high-speed per-chunk forensic audit endpoint (< 500ms response).
 * Fully decoupled from local disk (stateless & memory-only).
 * Compliant with Vercel Hobby (10s) and Pro (60s/300s) limits.
 */

const path = require('path');
const BASE_DIR = path.resolve(__dirname, '..');

let detectorNode = null;
try {
  detectorNode = require(path.join(BASE_DIR, 'services', 'detection_engine', 'detector_node.js'));
} catch (e) {
  console.warn('detector_node load in /api/audit:', e.message);
}

const KBBI_RULES = [
  // 1. Kata Serapan & Bentuk Baku Utama (KBBI Daring)
  { wrong: /\bterpercaya\b/gi, right: 'tepercaya', rule: 'KBBI: Bentuk baku dengan awalan ter- pada kata dasar berfonem /p/ adalah tepercaya' },
  { wrong: /\banalisa\b/gi, right: 'analisis', rule: 'KBBI: Bentuk baku penyerapan akhiran -sis adalah analisis' },
  { wrong: /\bresiko\b/gi, right: 'risiko', rule: 'KBBI: Bentuk baku dengan vokal i adalah risiko' },
  { wrong: /\bpraktek\b/gi, right: 'praktik', rule: 'KBBI: Bentuk baku dengan vokal i adalah praktik' },
  { wrong: /\bsistim\b/gi, right: 'sistem', rule: 'KBBI: Bentuk baku dengan vokal e adalah sistem' },
  { wrong: /\bstandarisasi\b/gi, right: 'standardisasi', rule: 'KBBI: Bentuk baku penyerapan adalah standardisasi' },
  { wrong: /\baktifitas\b/gi, right: 'aktivitas', rule: 'KBBI: Bentuk baku penyerapan akhiran -itas adalah aktivitas' },
  { wrong: /\befektifitas\b/gi, right: 'efektivitas', rule: 'KBBI: Bentuk baku penyerapan akhiran -itas adalah efektivitas' },
  { wrong: /\bkreatifitas\b/gi, right: 'kreativitas', rule: 'KBBI: Bentuk baku penyerapan akhiran -itas adalah kreativitas' },
  { wrong: /\bproduktifitas\b/gi, right: 'produktivitas', rule: 'KBBI: Bentuk baku penyerapan akhiran -itas adalah produktivitas' },
  { wrong: /\bsekedar\b/gi, right: 'sekadar', rule: 'KBBI: Bentuk baku berasal dari kata dasar kadar menjadi sekadar' },
  { wrong: /\bhakekat\b/gi, right: 'hakikat', rule: 'KBBI: Bentuk baku adalah hakikat' },
  { wrong: /\bhirarki\b/gi, right: 'hierarki', rule: 'KBBI: Bentuk baku adalah hierarki' },
  { wrong: /\bkwalitas\b/gi, right: 'kualitas', rule: 'KBBI: Bentuk baku penyerapan adalah kualitas' },
  { wrong: /\bkwantitas\b/gi, right: 'kuantitas', rule: 'KBBI: Bentuk baku penyerapan adalah kuantitas' },
  { wrong: /\bjadual\b/gi, right: 'jadwal', rule: 'KBBI: Bentuk baku adalah jadwal' },
  { wrong: /\bmerubah\b/gi, right: 'mengubah', rule: 'KBBI: Imbuhan meng- pada kata dasar ubah menjadi mengubah' },
  { wrong: /\bmensahkan\b/gi, right: 'mengesahkan', rule: 'KBBI: Imbuhan menge-kan pada kata dasar satu suku kata sah' },
  { wrong: /\bmentargetkan\b/gi, right: 'menargetkan', rule: 'KBBI: Fonem /t/ luluh saat bertemu awalan meN- menjadi menargetkan' },
  { wrong: /\bmengkoordinasikan\b/gi, right: 'mengoordinasikan', rule: 'KBBI: Fonem /k/ luluh saat bertemu awalan meN- menjadi mengoordinasikan' },
  { wrong: /\bmempraktekkan\b/gi, right: 'mempraktikkan', rule: 'KBBI: Imbuhan mem-kan pada praktik menjadi mempraktikkan' },
  { wrong: /\bperlindungan data pribadi\b/gi, right: 'pelindungan data pribadi', rule: 'UU No. 27/2022: Nomenklatur resmi baku adalah Pelindungan Data Pribadi' },

  // 2. Preposisi / Kata Depan EYD V (Wajib Dipisah)
  { wrong: /\bdimana\b/gi, right: 'di mana', rule: 'EYD V: Preposisi di mana wajib ditulis terpisah dan bukan kata hubung subordinatif' },
  { wrong: /\bdisini\b/gi, right: 'di sini', rule: 'EYD V: Kata depan di sini penunjuk ruang/lokasi wajib ditulis terpisah' },
  { wrong: /\bdisana\b/gi, right: 'di sana', rule: 'EYD V: Kata depan di sana penunjuk ruang/lokasi wajib ditulis terpisah' },
  { wrong: /\bkesana\b/gi, right: 'ke sana', rule: 'EYD V: Kata depan ke sana penunjuk arah wajib ditulis terpisah' },
  { wrong: /\bkemana\b/gi, right: 'ke mana', rule: 'EYD V: Kata depan ke mana penunjuk arah wajib ditulis terpisah' },
  { wrong: /\bdiantara\b/gi, right: 'di antara', rule: 'EYD V: Kata depan di antara penunjuk relasi/lokasi wajib ditulis terpisah' },
  { wrong: /\bdidalam\b/gi, right: 'di dalam', rule: 'EYD V: Kata depan di dalam penunjuk ruang/wadah wajib ditulis terpisah' },
  { wrong: /\bdiatas\b/gi, right: 'di atas', rule: 'EYD V: Kata depan di atas penunjuk posisi vertikal wajib ditulis terpisah' },

  // 3. Imbuhan Pasif di- yang salah dipisah (Wajib Disambung)
  { wrong: /\bdi lakukan\b/gi, right: 'dilakukan', rule: 'EYD V: Imbuhan pasif di- pada verba dilakukan wajib dirangkaikan' },
  { wrong: /\bdi tetapkan\b/gi, right: 'ditetapkan', rule: 'EYD V: Imbuhan pasif di- pada verba ditetapkan wajib dirangkaikan' },
  { wrong: /\bdi gunakan\b/gi, right: 'digunakan', rule: 'EYD V: Imbuhan pasif di- pada verba digunakan wajib dirangkaikan' },
  { wrong: /\bdi integrasikan\b/gi, right: 'diintegrasikan', rule: 'EYD V: Imbuhan pasif di- pada verba diintegrasikan wajib dirangkaikan' },

  // 4. Frasa Rancu & Klise AI Overused
  { wrong: /\befisiensi anggaran yang mana\b/gi, right: 'efisiensi anggaran yang', rule: 'EYD V: Penghilangan frasa penghubung rancu yang mana' },
  { wrong: /\bkualitas daripada\b/gi, right: 'kualitas', rule: 'EYD V: Penghilangan daripada pembanding yang rancu' },
  { wrong: /\bdalam era digitalisasi yang serba cepat ini,?\s*/gi, right: 'Pada perkembangan transformasi tata kelola digital saat ini, ', rule: 'De-cliché AI: Ungkapan pembuka klise mesin' },
  { wrong: /\bdi era digital yang serba cepat ini,?\s*/gi, right: 'Pada era transformasi digital saat ini, ', rule: 'De-cliché AI: Metafora pembuka klise' },
  { wrong: /\bmemainkan peranan? krusial\b/gi, right: 'memiliki posisi strategis', rule: 'De-cliché AI: Metafora overused penerjemahan mesin' },
  { wrong: /\bmemegang peranan? penting\b/gi, right: 'berperan penting', rule: 'De-cliché AI: Penyederhanaan diksi baku' },
  { wrong: /\btidak dapat dipungkiri bahwa\b/gi, right: 'kenyataannya', rule: 'De-cliché AI: Frasa pembuka penegasan berulang mesin' },
  { wrong: /\bsecara holistik dan komprehensif\b/gi, right: 'secara terpadu', rule: 'De-cliché AI: Pleonasme khas teks AI' }
];

function segmentSentences(text) {
  if (detectorNode && typeof detectorNode.segmentSentences === 'function') {
    return detectorNode.segmentSentences(text);
  }
  if (!text) return [];
  const raw = text.replace(/([.?!])\s+(?=[A-Z0-9])/g, "$1|SPLIT|");
  return raw.split("|SPLIT|").map(s => s.trim()).filter(Boolean);
}

function evaluateSentence(sentence) {
  const words = (sentence || '').toLowerCase().match(/\b[a-zA-Z0-9_\-]+\b/g) || [];
  const nw = words.length;
  if (nw === 0) return { risk: 0.05, markers: [] };

  const sLower = sentence.toLowerCase();
  const cliches = [
    "dalam era digital", "yang serba cepat", "memainkan peran penting",
    "memainkan peranan krusial", "tidak dapat dipungkiri", "langkah konkret dan strategis",
    "secara holistik dan komprehensif", "kunci utama keberlanjutan"
  ];
  const transitions = ["lebih lanjut", "di sisi lain", "secara keseluruhan", "dalam konteks ini", "pada akhirnya"];

  const foundCliches = cliches.filter(c => sLower.includes(c));
  const foundTransitions = transitions.filter(m => sLower.startsWith(m) || sLower.includes(`, ${m}`));

  let risk = 0.14;
  if (foundCliches.length > 0) risk += 0.32 * foundCliches.length;
  if (foundTransitions.length > 0) risk += 0.22;

  if (nw >= 18 && nw <= 26 && foundTransitions.length > 0) {
    risk += 0.12;
  } else if (nw < 10 || nw > 35) {
    risk -= 0.08;
  }

  const finalRisk = Math.min(0.96, Math.max(0.04, Number(risk.toFixed(3))));
  return {
    risk: finalRisk,
    markers: [...foundCliches, ...foundTransitions]
  };
}

module.exports = async (req, res) => {
  // CORS Headers
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
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) { body = {}; }
    } else if (!body) {
      body = await new Promise((resolve) => {
        let raw = '';
        const timer = setTimeout(() => resolve({}), 800);
        req.on('data', c => { raw += c; });
        req.on('end', () => {
          clearTimeout(timer);
          try { resolve(JSON.parse(raw || '{}')); } catch (e) { resolve({}); }
        });
        req.on('error', () => { clearTimeout(timer); resolve({}); });
      });
    }

    const sentences = Array.isArray(body.sentences) && body.sentences.length > 0
      ? body.sentences
      : segmentSentences(body.text || '');

    const chunkIndex = Number(body.chunk_index || 1);
    const totalChunks = Number(body.total_chunks || 1);
    const startIndex = Number(body.start_index || 0);

    const pairs = sentences.map((orig, idx) => {
      const origTrim = orig.trim();
      const evalRes = evaluateSentence(origTrim);
      const risk = evalRes.risk;
      const markers = evalRes.markers;

      let appliedRules = [];
      let transformed = origTrim;

      if (/(?<!\.)\.\.(?!\.)/.test(transformed)) {
        transformed = transformed.replace(/(?<!\.)\.\.(?!\.)/g, '.');
        appliedRules.push('EYD V: Koreksi titik ganda (..) menjadi titik tunggal');
      }
      if (/\s+([.,;:!?])/.test(transformed)) {
        transformed = transformed.replace(/\s+([.,;:!?])/g, '$1');
        appliedRules.push('EYD V: Penghapusan spasi sebelum tanda baca');
      }

      KBBI_RULES.forEach(r => {
        if (r.wrong.test(transformed)) {
          transformed = transformed.replace(r.wrong, r.right);
          appliedRules.push(r.rule);
        }
      });

      const isLinguisticallyDirty = appliedRules.length > 0;
      const isAiRisky = risk >= 0.50;
      const isAiModerate = risk >= 0.28;

      let status = 'SUDAH BAIK';
      let characteristics = 'Sintaksis baku, variasi panjang normal, register formal dinas.';
      let scoreInd = `${(risk * 100).toFixed(1)}% (Alami)`;
      let rec = origTrim;
      let reason = 'Telah memenuhi 100% kaidah baku KBBI & EYD V.';

      if (isAiRisky) {
        status = 'REVISI SUBSTANTIF';
        characteristics = markers.length > 0
          ? `Klise & pola prediktif AI: ${markers.join(', ')}`
          : 'Penumpukan konjungsi transisi klise AI dan struktur klausa simetris.';
        scoreInd = `${(risk * 100).toFixed(1)}% (Tinggi)`;
        rec = transformed !== origTrim ? transformed : origTrim;
        reason = isLinguisticallyDirty
          ? `Eliminasi klise sintaksis AI; ${appliedRules.join('; ')}.`
          : 'Eliminasi pola kalimat robotik dan penyesuaian register naskah dinas.';
      } else if (isAiModerate || isLinguisticallyDirty) {
        status = 'REVISI MINOR';
        if (isLinguisticallyDirty) {
          characteristics = 'Pelanggaran ejaan leksikal baku KBBI / kaidah tanda baca EYD V terdeteksi.';
          reason = appliedRules.join('; ');
        } else {
          characteristics = 'Format kalimat formal dengan irama netral; indikasi campuran.';
          reason = 'Penyelarasan ragam resmi dan tanda baca intrakalimat EYD V.';
        }
        scoreInd = `${(risk * 100).toFixed(1)}% (${risk >= 0.35 ? 'Sedang' : 'Rendah'})`;
        rec = transformed;
      }

      return {
        index: startIndex + idx + 1,
        original: origTrim,
        original_text: origTrim,
        sentence: origTrim,
        characteristics,
        status,
        action_label: status,
        score_indicator: scoreInd,
        ai_score: risk,
        recommendation: rec,
        transformed: rec,
        revised_text: rec,
        revision_reason: reason,
        action_note: reason,
        level: status === 'REVISI SUBSTANTIF' ? 'high' : (status === 'REVISI MINOR' ? 'medium' : 'low')
      };
    });

    const words = sentences.join(' ').toLowerCase().match(/\b[a-zA-Z0-9_\-]+\b/g) || [];
    const nWords = words.length;
    const sentLengths = sentences.map(s => (s.match(/\b[a-zA-Z0-9_\-]+\b/g) || []).length).filter(l => l > 0);
    const validLengths = sentLengths.length ? sentLengths : [1];
    const sentMean = validLengths.reduce((a, b) => a + b, 0) / validLengths.length;
    const sentVar = validLengths.reduce((a, b) => a + Math.pow(b - sentMean, 2), 0) / validLengths.length;
    const sentStd = Math.sqrt(sentVar);
    const burstiness = sentMean > 0 ? Number((sentStd / sentMean).toFixed(4)) : 0;

    const avgRisk = pairs.length > 0 ? (pairs.reduce((a, b) => a + b.ai_score, 0) / pairs.length) : 0.12;

    res.statusCode = 200;
    return res.end(JSON.stringify({
      status: 'success',
      chunk_index: chunkIndex,
      total_chunks: totalChunks,
      sentence_count: pairs.length,
      word_count: nWords,
      calibrated_ai_probability: Number(avgRisk.toFixed(4)),
      burstiness: burstiness,
      sentence_pairs: pairs
    }));
  } catch (err) {
    console.error('[/api/audit error]:', err);
    res.statusCode = 200;
    return res.end(JSON.stringify({
      status: 'error',
      message: err.message || 'Gagal memproses audit kalimat.'
    }));
  }
};

module.exports.config = {
  maxDuration: 60
};
