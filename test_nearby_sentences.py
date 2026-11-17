import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from services.document_intelligence.ai_humanizer import AIHumanizer

h = AIHumanizer()

sample_sentences = [
    "Bab II menetapkan arah dan aturan main pada tingkat provinsi.",
    "Bab ini menurunkannya menjadi arsitektur pada enam domain: proses bisnis, data dan informasi, layanan, aplikasi, infrastruktur, dan keamanan.",
    "Untuk setiap domain, pembahasan menjawab lima pertanyaan: apa tujuan dan ruang lingkupnya, kaidah apa yang berlaku, bagaimana kondisinya menurut dokumen baseline, seperti apa arsitektur targetnya, dan kesenjangan apa yang perlu ditutup.",
    "Setiap domain dibahas dengan pola yang sama agar pembaca dapat membandingkannya.",
    "Tujuan dan ruang lingkup: apa yang dicakup domain dan untuk apa."
]

for s in sample_sentences:
    print("=" * 70)
    an = h.analyze_sentence(s)
    dp = h.dynamic_humanize_paraphrase(s)
    markers = [m.get("phrase") if isinstance(m, dict) else m for m in an.get("markers", [])]
    print(f"ORIGINAL   : {s}")
    print(f"STATUS     : {an.get('status')} ({an.get('ai_probability')}%) | MARKERS: {markers}")
    print(f"RECOMMENDED: {dp}")
    print(f"DIFFERENT  : {s.strip().lower() != dp.strip().lower()}")
