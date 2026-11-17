"""
Full pipeline test: PDF extraction -> AI Humanizer -> DOCX generation
Tests with max_pages=70 to capture page 62 content (sentence 1226)
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import time
import json

start = time.time()

# Step 1: Extract PDF
from services.document_intelligence.pdf_extractor import PDFExtractor
extractor = PDFExtractor()
pdf_path = "uploads/Arsitektur_SPBE_DKI_Jakarta_2027.pdf"
result = extractor.extract_from_path(pdf_path, max_pages=70)
extract_time = time.time() - start
print(f"[1/3] PDF extracted: {result['processed_pages']}/{result['total_pages']} pages in {extract_time:.2f}s")
print(f"      Text length: {len(result['text'])} chars")

# Step 2: Humanize
from services.document_intelligence.ai_humanizer import AIHumanizer
humanizer = AIHumanizer()

# Check if target sentence exists in extracted text
target_phrase = "menurunkannya menjadi arsitektur pada enam domain"
found = target_phrase in result["text"]
print(f"      Target phrase found: {found}")

humanize_start = time.time()
humanized = humanizer.humanize_and_rephrase(result["text"], mode="formal_spbe", intensity="balanced")
humanize_time = time.time() - humanize_start
print(f"[2/3] Humanized: {humanized['total_sentences']} sentences in {humanize_time:.2f}s")

# Check for sentence 1226 (the target)
target_found = False
for p in humanized["sentence_pairs"]:
    if "menurunkannya menjadi arsitektur" in p["original"]:
        target_found = True
        print(f"\n=== TARGET SENTENCE FOUND (Index {p['index']}) ===")
        print(f"STATUS: {p['status']}")
        print(f"ACTION: {p['action_label']}")
        print(f"AI%:    {p['ai_probability']}")
        print(f"ORIG:   {p['original'][:150]}")
        print(f"TRANS:  {p['transformed'][:150]}")
        print(f"IDENTICAL: {p['original'].strip() == p['transformed'].strip()}")
        break

if not target_found:
    # Search nearby
    for p in humanized["sentence_pairs"]:
        if "enam domain" in p["original"] and "proses bisnis" in p["original"]:
            print(f"\n=== NEAR-MATCH FOUND (Index {p['index']}) ===")
            print(f"ORIG:  {p['original'][:150]}")
            print(f"TRANS: {p['transformed'][:150]}")
            break

# Count distinct vs identical
total = len(humanized["sentence_pairs"])
identical_count = sum(1 for p in humanized["sentence_pairs"] if p["original"].strip() == p["transformed"].strip())
distinct_count = total - identical_count
print(f"\nDistinction stats: {distinct_count}/{total} distinct ({100*distinct_count/total:.1f}%)")
print(f"Identical kept (green): {identical_count}")

# Step 3: Generate DOCX
docx_start = time.time()
docx_path = humanizer.generate_humanized_docx(humanized, filename="test_full_pipeline_v2.docx")
docx_time = time.time() - docx_start
print(f"[3/3] DOCX generated in {docx_time:.2f}s: {docx_path}")

total_time = time.time() - start
print(f"\n=== TOTAL PIPELINE: {total_time:.2f}s ===")
print(f"AI Score Before: {humanized['ai_score_before']}%")
print(f"AI Score After:  {humanized['ai_score_after']}%")
print(f"Score Drop:      {humanized['improvement_score_drop']}")
