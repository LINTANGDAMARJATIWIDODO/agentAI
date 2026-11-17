import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from services.document_intelligence.ai_humanizer import AIHumanizer

h = AIHumanizer()
test = "Bab ini menurunkannya menjadi arsitektur pada enam domain: proses bisnis, data dan informasi, layanan, aplikasi, infrastruktur, dan keamanan."

# 1. Analyze the sentence
a = h.analyze_sentence(test)
print("=== ANALYZE SENTENCE ===")
print(f"STATUS: {a.get('status')}")
print(f"AI%: {a.get('ai_probability')}")
print(f"IS_HEADING: {a.get('is_heading')}")
print(f"MARKERS: {a.get('markers', [])}")
print(f"COLOR: {a.get('color')}")

# 2. Run humanize_and_rephrase
r = h.humanize_and_rephrase(test)
print("\n=== HUMANIZE RESULTS ===")
for p in r["sentence_pairs"]:
    print(f"\nIDX: {p['index']}")
    print(f"STATUS: {p['status']}")
    print(f"ACTION: {p['action_label']}")
    print(f"AI_PROB: {p['ai_probability']}")
    print(f"ORIGINAL:    {p['original']}")
    print(f"TRANSFORMED: {p['transformed']}")
    print(f"REPLACEMENT: {p['replacement_text']}")
    same = p['original'].strip() == p['transformed'].strip()
    print(f"IDENTICAL: {same}")

# 3. Also test dynamic_humanize_paraphrase directly
print("\n=== DIRECT PARAPHRASE ===")
dp = h.dynamic_humanize_paraphrase(test)
print(f"INPUT:  {test}")
print(f"OUTPUT: {dp}")
print(f"IDENTICAL: {test.strip() == dp.strip()}")

# 4. Test after marker replacement
import re
after_markers = test
for marker, replacement, _ in h.ROBOTIC_AI_MARKERS_ID:
    pattern = re.compile(re.escape(marker), re.IGNORECASE)
    after_markers = pattern.sub(replacement, after_markers)
print(f"\n=== AFTER MARKER REPLACEMENT ===")
print(f"RESULT: {after_markers}")
dp2 = h.dynamic_humanize_paraphrase(after_markers)
print(f"AFTER PARAPHRASE: {dp2}")
print(f"IDENTICAL TO ORIG: {test.strip() == dp2.strip()}")
