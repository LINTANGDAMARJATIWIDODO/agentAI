"""
NEXUS AI ENTERPRISE — INDONESIAN LINGUISTIC INTELLIGENCE ENGINE
==============================================================
Audits Indonesian sentences against standard KBBI and EYD V rules.
Strictly implements the 4-decision protocol:
1. SUDAH BAIK: "Tidak diperlukan perubahan. Kalimat telah memenuhi kaidah bahasa Indonesia dalam konteks penggunaannya."
2. REVISI MINOR: Ejaan KBBI, tanda baca koma/titik, huruf kapital.
3. REVISI SUBSTANTIF: Struktur gramatikal cacat (tanpa predikat, anak kalimat tanpa induk).
4. PERLU VERIFIKASI: Kalimat terpotong atau konteks tidak mencukupi.

PROHIBITED BEHAVIORS ENFORCED:
- NEVER replace "Selain itu" with "Di samping itu".
- NEVER replace "Oleh karena itu" with "Oleh sebab itu".
- NEVER replace "dapat" with "bisa".
- NEVER insert "Secara substantif".
- NEVER add comma before "dan" in 2-element clauses.
- NEVER change correct academic sentences merely to create variation.
"""

import re
from typing import Dict, List, Any, Optional

# Authoritative KBBI Non-Standard to Standard Baku Dictionary
KBBI_CORRECTIONS = {
    "analisa": ("analisis", "Kata baku menurut KBBI adalah 'analisis' (penyerapan dari bahasa Belanda/Inggris -sis)."),
    "sistim": ("sistem", "Bentuk baku KBBI adalah 'sistem' dengan vokal 'e'."),
    "aktifitas": ("aktivitas", "Bentuk baku menggunakan huruf 'v' karena diserap dari activity -> aktivitas."),
    "efektifitas": ("efektivitas", "Bentuk baku menggunakan huruf 'v' (efektivitas)."),
    "kreatifitas": ("kreativitas", "Bentuk baku menggunakan huruf 'v' (kreativitas)."),
    "produktivitas": ("produktivitas", "Bentuk baku KBBI."),
    "praktek": ("praktik", "Bentuk baku KBBI adalah 'praktik' dengan huruf 'i'."),
    "tehnik": ("teknik", "Bentuk baku KBBI tanpa huruf 'h' (teknik)."),
    "obyek": ("objek", "Bentuk baku KBBI menggunakan 'j' (objek)."),
    "subyek": ("subjek", "Bentuk baku KBBI menggunakan 'j' (subjek)."),
    "proyek": ("proyek", "Bentuk baku KBBI."),
    "metodholigi": ("metodologi", "Bentuk baku KBBI adalah 'metodologi'."),
    "metodologi": ("metodologi", "Bentuk baku KBBI."),
    "standarisasi": ("standardisasi", "Bentuk baku KBBI adalah 'standardisasi' (mempertahankan morfem 'standard')."),
    "hirarki": ("hierarki", "Bentuk baku KBBI adalah 'hierarki'."),
    "jadwal": ("jadwal", "Bentuk baku KBBI."),
    "jadual": ("jadwal", "Bentuk baku KBBI adalah 'jadwal'."),
    "kualitas": ("kualitas", "Bentuk baku KBBI."),
    "kwalitas": ("kualitas", "Bentuk baku KBBI adalah 'kualitas'."),
    "kuantitas": ("kuantitas", "Bentuk baku KBBI."),
    "kwantitas": ("kuantitas", "Bentuk baku KBBI adalah 'kuantitas'."),
    "ijazah": ("ijazah", "Bentuk baku KBBI."),
    "ijasah": ("ijazah", "Bentuk baku KBBI adalah 'ijazah' dengan huruf 'z'."),
    "azas": ("asas", "Bentuk baku KBBI adalah 'asas' dengan huruf 's'."),
    "resiko": ("risiko", "Bentuk baku KBBI adalah 'risiko' dengan huruf 'i'."),
    "antri": ("antre", "Bentuk baku KBBI adalah 'antre' dengan vokal 'e'."),
    "antrian": ("antrean", "Bentuk baku KBBI adalah 'antrean'."),
    "legalisir": ("legalisasi", "Bentuk baku KBBI untuk proses pengesahan adalah 'legalisasi'."),
    "merubah": ("mengubah", "Bentuk baku berasal dari kata dasar 'ubah' diberi awalan meN- menjadi 'mengubah'."),
    "mensahkan": ("mengesahkan", "Kata dasar 'sah' yang bersuku kata satu luluh menjadi 'mengesahkan'."),
    "mentargetkan": ("menargetkan", "Fonem /t/ luluh saat bertemu awalan meN- menjadi 'menargetkan'."),
    "mengkoordinasikan": ("mengoordinasikan", "Fonem /k/ luluh saat bertemu awalan meN- menjadi 'mengoordinasikan'."),
    "mempraktekkan": ("mempraktikkan", "Kata dasar 'praktik' diberi imbuhan me-kan menjadi 'mempraktikkan'.")
}

# Incomplete sentence markers / trailing prepositions
TRUNCATED_INDICATORS = [
    "berdasarkan evaluasi terhadap implementasi",
    "sehubungan dengan pelaksanaan dari",
    "terkait dengan perumusan",
    "dalam rangka untuk",
    "yang mana bahwa",
    "sebagaimana yang telah di"
]


class IndonesianLinguisticAuditor:
    """
    Academic Indonesian Linguistic Auditor for KBBI, EYD V, and sentence effectiveness.
    """

    def audit_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        Audits a single Indonesian sentence according to strict KBBI & EYD V protocols.
        Returns exact decision (SUDAH BAIK, REVISI MINOR, REVISI SUBSTANTIF, PERLU VERIFIKASI)
        and formatted report.
        """
        s_clean = sentence.strip()
        if not s_clean:
            return {
                "decision": "PERLU VERIFIKASI",
                "original_sentence": sentence,
                "findings": "Kalimat kosong.",
                "error_category": "Struktur Kosong",
                "recommended_revision": "",
                "reason_for_revision": "Konteks tidak mencukupi.",
                "rule_reference": "EYD V",
                "is_changed": False
            }

        # 1. Check for Truncated / Incomplete Sentence (PERLU VERIFIKASI)
        # Conditions: ends without punctuation, ends with preposition/conjunction, or matches truncated fragment
        s_lower = s_clean.lower()
        is_truncated = False
        truncated_reason = ""

        if not re.search(r'[.!?]$', s_clean):
            # No terminal punctuation and length is short or ends with dangling connector
            words = s_clean.split()
            last_word = words[-1].lower().strip(",;:") if words else ""
            dangling_words = {"dan", "yang", "pada", "untuk", "dengan", "dari", "dalam", "terhadap", "sebagaimana", "serta"}
            if last_word in dangling_words or len(words) < 6:
                is_truncated = True
                truncated_reason = f"Kalimat berakhir menggantung pada kata tugas '{last_word}' tanpa penutup tanda baca akhir."

        for fragment in TRUNCATED_INDICATORS:
            if s_lower == fragment or s_lower.startswith(fragment) and len(s_clean.split()) <= 6 and not re.search(r'[.!?]$', s_clean):
                is_truncated = True
                truncated_reason = "Kalimat terpotong di tengah anak kalimat sebelum induk kalimat dinyatakan."

        if is_truncated:
            return {
                "decision": "PERLU VERIFIKASI",
                "original_sentence": s_clean,
                "findings": "Kalimat terindikasi terpotong atau tidak tuntas.",
                "error_category": "Kalimat Menggantung / Tidak Lengkap",
                "recommended_revision": s_clean + " ... [Lengkapi kelanjutan anak/induk kalimat]",
                "reason_for_revision": truncated_reason or "Konteks tersedia belum mencukupi untuk membuat perbaikan andal tanpa mengubah maksud penulis.",
                "rule_reference": "Tata Bahasa Baku Bahasa Indonesia (TBBBI) - Keutuhan Klausa",
                "is_changed": False
            }

        # 2. Check for Grammatical Structure Failure (REVISI SUBSTANTIF)
        # Example: Sentence consists entirely of a prepositional subordinate clause without main predicate
        # e.g., "Mengenai implementasi arsitektur SPBE yang mana telah dibahas pada rapat dinas."
        substantive_finding = ""
        substantive_revision = ""
        substantive_reason = ""

        # Pattern: Subordinatif tanpa induk: Kalimat diawali "Bahwa..." atau "Sehingga..." tanpa induk kalimat
        if re.match(r'^(Sehingga|Bahwa|Sedangkan|Padahal)\b', s_clean):
            substantive_finding = f"Konjungsi intrakalimat '{s_clean.split()[0]}' digunakan sebagai pembuka kalimat mandiri tanpa induk kalimat."
            error_word = s_clean.split()[0]
            if error_word.lower() == "sehingga":
                substantive_revision = re.sub(r'^Sehingga\b', 'Oleh karena itu,', s_clean, flags=re.IGNORECASE)
                substantive_reason = "Konjungsi subordinatif 'sehingga' tidak boleh mengawali kalimat tunggal; diganti konjungsi antarkalimat yang sah seperti 'Oleh karena itu,'."
            elif error_word.lower() == "bahwa":
                substantive_revision = re.sub(r'^Bahwa\b\s*', '', s_clean, flags=re.IGNORECASE)
                substantive_reason = "Kata 'bahwa' di awal kalimat membatalkan posisi subjek utama menjadikannya anak kalimat tanpa induk."
            elif error_word.lower() in ["sedangkan", "padahal"]:
                substantive_revision = re.sub(r'^(Sedangkan|Padahal)\b', 'Akan tetapi,', s_clean, flags=re.IGNORECASE)
                substantive_reason = f"Konjungsi pertentangan intrakalimat '{error_word}' tidak boleh mengawali kalimat; diganti konjungsi antarkalimat 'Akan tetapi,'."

        if substantive_finding:
            return {
                "decision": "REVISI SUBSTANTIF",
                "original_sentence": s_clean,
                "findings": substantive_finding,
                "error_category": "Struktur Sintaksis / Ketiadaan Induk Kalimat",
                "recommended_revision": substantive_revision,
                "reason_for_revision": substantive_reason,
                "rule_reference": "EYD V Bab IV (Penulisan Konjungsi) & TBBBI Edisi IV",
                "is_changed": True
            }

        # 3. Check for KBBI Spelling Errors (REVISI MINOR)
        # Search word by word
        words_raw = re.findall(r'\b[a-zA-Z\-]+\b', s_clean)
        kbbi_hits = []
        revised_text = s_clean

        for w in words_raw:
            w_lower = w.lower()
            if w_lower in KBBI_CORRECTIONS:
                correct_form, expl = KBBI_CORRECTIONS[w_lower]
                if w_lower != correct_form.lower():
                    # Preserve title case if word was capitalized
                    repl = correct_form.capitalize() if w.istitle() else correct_form
                    pattern = re.compile(rf'\b{re.escape(w)}\b')
                    revised_text = pattern.sub(repl, revised_text)
                    kbbi_hits.append({
                        "original": w,
                        "corrected": repl,
                        "explanation": expl
                    })

        # 4. Check Punctuation Errors (REVISI MINOR)
        punct_findings = []

        # Check: Missing comma after inter-sentence conjunctions at sentence start
        # Legitimate inter-sentence conjunctions that MUST be followed by comma:
        inter_conjunctions = [
            "Selain itu", "Oleh karena itu", "Oleh sebab itu", "Dengan demikian",
            "Namun", "Akan tetapi", "Meskipun demikian", "Di samping itu"
        ]
        for conj in inter_conjunctions:
            # Matches conj at start not followed by comma
            pattern = re.compile(rf'^{re.escape(conj)}(?!\s*,)\b', re.IGNORECASE)
            if pattern.search(revised_text):
                revised_text = pattern.sub(f"{conj},", revised_text)
                punct_findings.append(f"Konjungsi antarkalimat '{conj}' wajib diikuti tanda baca koma.")

        # Check: Prohibited misplaced comma before 'dan' in 2-element clause
        # If someone wrote "pria, dan wanita", remove the illegal comma before "dan"
        # Rule: comma before 'dan' is ONLY valid in serial lists with 3+ items: "A, B, dan C"
        two_item_dan_pattern = re.compile(r'(?<!,)\s+([a-zA-Z0-9_\-]+),\s+dan\s+([a-zA-Z0-9_\-]+)(?=[.,;!?\s]|$)', re.IGNORECASE)
        # Let's check if there is an erroneous comma before 'dan' where preceding has no other comma
        if re.search(r'^[^,]+,\s+dan\s+[^,]+[.!?]?$', s_clean):
            # Only one comma in entire sentence and it's right before 'dan' in a 2-element list!
            revised_text = re.sub(r',\s+dan\s+', ' dan ', revised_text)
            punct_findings.append("Tanda baca koma sebelum kata 'dan' tidak diperlukan karena hanya menggabungkan dua unsur setara.")

        # Check: Missing comma before contrastive conjunctions (, tetapi, , melainkan, , sedangkan)
        for contrast in ["tetapi", "melainkan", "sedangkan"]:
            pat = re.compile(rf'(?<!,)\s+\b({contrast})\b', re.IGNORECASE)
            if pat.search(revised_text) and not revised_text.strip().lower().startswith(contrast):
                revised_text = pat.sub(rf', \1', revised_text)
                punct_findings.append(f"Klausa pertentangan yang didahului konjungsi '{contrast}' wajib didahului tanda koma.")

        # Ensure sentence has terminal punctuation
        if not re.search(r'[.!?]$', revised_text):
            revised_text += "."
            punct_findings.append("Kalimat formal wajib diakhiri tanda baca titik.")

        # Clean spaces around punctuation
        revised_text = re.sub(r'\s+([.,;:!?])', r'\1', revised_text)
        revised_text = re.sub(r'\s+', ' ', revised_text).strip()

        # Decision synthesis
        if kbbi_hits or punct_findings:
            findings_list = [f"{h['original']} -> {h['corrected']} ({h['explanation']})" for h in kbbi_hits]
            findings_list.extend(punct_findings)
            category = "Ejaan Baku KBBI" if kbbi_hits and not punct_findings else ("Tanda Baca EYD V" if punct_findings and not kbbi_hits else "Ejaan KBBI & Tanda Baca EYD V")
            return {
                "decision": "REVISI MINOR",
                "original_sentence": s_clean,
                "findings": "; ".join(findings_list),
                "error_category": category,
                "recommended_revision": revised_text,
                "reason_for_revision": "Menyesuaikan ejaan kata tidak baku ke rujukan resmi KBBI dan/atau menyempurnakan kaidah tanda baca EYD V.",
                "rule_reference": "Kamus Besar Bahasa Indonesia (KBBI VI) & Pedoman Umum Ejaan Bahasa Indonesia (EYD V)",
                "is_changed": True
            }

        # 5. NO ERRORS FOUND -> STRICTLY SUDAH BAIK!
        # Do not alter a single word. Do not substitute "Selain itu" with "Di samping itu". Do not insert "Secara substantif".
        return {
            "decision": "SUDAH BAIK",
            "original_sentence": s_clean,
            "findings": "Tidak ditemukan kesalahan ejaan, tanda baca, atau struktur sintaksis.",
            "error_category": "Nihil",
            "recommended_revision": s_clean,
            "reason_for_revision": "Tidak diperlukan perubahan. Kalimat telah memenuhi kaidah bahasa Indonesia dalam konteks penggunaannya.",
            "rule_reference": "KBBI & EYD V (Sesuai Standar)",
            "is_changed": False
        }

    def audit_document(self, text: str) -> Dict[str, Any]:
        """
        Audits an entire document sentence by sentence, respecting paragraph boundaries.
        Returns aggregate stats, per-sentence audit cards, and counts.
        """
        # Segment into sentences
        from services.detection_engine.feature_extractor import segment_sentences
        sentences = segment_sentences(text)

        audited_sentences = []
        decision_counts = {
            "SUDAH BAIK": 0,
            "REVISI MINOR": 0,
            "REVISI SUBSTANTIF": 0,
            "PERLU VERIFIKASI": 0
        }

        for idx, s in enumerate(sentences):
            audit_res = self.audit_sentence(s)
            audit_res["index"] = idx
            decision_counts[audit_res["decision"]] += 1
            audited_sentences.append(audit_res)

        total_s = max(1, len(audited_sentences))
        sound_percentage = round((decision_counts["SUDAH BAIK"] / total_s) * 100.0, 1)

        return {
            "status": "success",
            "total_sentences": len(audited_sentences),
            "sound_percentage": sound_percentage,
            "decision_counts": decision_counts,
            "sentences": audited_sentences
        }


if __name__ == "__main__":
    auditor = IndonesianLinguisticAuditor()
    print("Testing Indonesian Linguistic Auditor...")

    test_cases = [
        # 1. Correct sentence with 'Selain itu,' -> Must be SUDAH BAIK!
        "Selain itu, integrasi sistem kecerdasan buatan memainkan peran penting dalam meningkatkan efisiensi operasional.",
        # 2. Correct academic sentence -> Must be SUDAH BAIK!
        "Penyusunan arsitektur SPBE Provinsi DKI Jakarta berpedoman pada prinsip interoperabilitas sistem.",
        # 3. 2-element clause with illegal comma before 'dan' -> Must fix comma, REVISI MINOR
        "Dinas Komunikasi, dan Informatika menetapkan standar metadatabase terpusat.",
        # 4. Non-baku KBBI words ('analisa sistim') -> Must fix spelling, REVISI MINOR
        "Hasil analisa sistim menunjukkan bahwa efektifitas kerja meningkat pesat.",
        # 5. Missing comma after 'Oleh karena itu' -> REVISI MINOR
        "Oleh karena itu penting bagi setiap unit pelaksana untuk mendaftarkan aplikasinya.",
        # 6. Truncated sentence -> PERLU VERIFIKASI
        "Berdasarkan evaluasi terhadap implementasi",
        # 7. Subordinate without main clause -> REVISI SUBSTANTIF
        "Sehingga penerapan SPBE dapat berjalan secara optimal di seluruh unit."
    ]

    for tc in test_cases:
        res = auditor.audit_sentence(tc)
        print(f"\n[{res['decision']}] Original: {tc}")
        print(f"  Findings : {res['findings']}")
        print(f"  Revision : {res['recommended_revision']}")
        print(f"  Reason   : {res['reason_for_revision']}")
