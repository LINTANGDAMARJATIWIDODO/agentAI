"""
NEXUS AI ENTERPRISE — DOCUMENT INTELLIGENCE CLI DISPATCHER (JUSTDONE AI ENGINE)
Handles standard input requests for PDF extraction, JustDone AI detector,
multi-tone humanizer, and DOCX document export.
"""

import sys
import os
import json

# Force UTF-8 encoding across stdin/stdout/stderr to prevent Windows charmap encoding errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.document_intelligence.pdf_extractor import pdf_extractor
from services.document_intelligence.ai_humanizer import ai_humanizer

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"status": "error", "message": "Empty stdin payload"}))
            sys.exit(1)

        payload = json.loads(raw_input)
        action = payload.get("action", "humanize")

        if action == "extract_pdf":
            pdf_path = payload.get("pdf_path", "")
            res = pdf_extractor.extract_from_path(pdf_path)
            print(json.dumps(res, ensure_ascii=False))

        elif action == "detect_ai":
            text = payload.get("text", "")
            res = ai_humanizer.detect_ai_markers(text)
            res["status"] = "success"
            print(json.dumps(res, ensure_ascii=False))

        elif action == "humanize":
            text = payload.get("text", "")
            mode = payload.get("mode", "formal_spbe")
            intensity = payload.get("intensity", "balanced")
            title = payload.get("title", "DOKUMEN_HASIL_HUMANISASI_PARAFRASE_AI")
            res = ai_humanizer.humanize_and_rephrase(text, mode=mode, intensity=intensity)
            
            # Generate styled Word document & Rebuilt PDF
            docx_file = ai_humanizer.generate_humanized_docx(
                original_text=text,
                humanized_text=res["humanized_text"],
                doc_title=title,
                markers_info=res
            )
            pdf_file = ai_humanizer.generate_humanized_pdf(
                original_text=text,
                humanized_text=res["humanized_text"],
                doc_title=title,
                markers_info=res
            )
            res["download_url"] = f"/api/download/{docx_file}"
            res["filename"] = docx_file
            res["pdf_download_url"] = f"/api/download/{pdf_file}"
            res["pdf_filename"] = pdf_file
            print(json.dumps(res, ensure_ascii=False))

        elif action == "process_pdf_and_humanize":
            pdf_path = payload.get("pdf_path", "")
            mode = payload.get("mode", "formal_spbe")
            intensity = payload.get("intensity", "balanced")
            max_pages = payload.get("max_pages", 70)
            ext_res = pdf_extractor.extract_from_path(pdf_path, max_pages=max_pages)
            if ext_res.get("status") != "success":
                print(json.dumps(ext_res, ensure_ascii=False))
                sys.exit(0)

            extracted_text = ext_res.get("clean_prose_text") or ext_res.get("text", "")
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            title = f"HUMANIZED_{base_name}"
            
            h_res = ai_humanizer.humanize_and_rephrase(extracted_text, mode=mode, intensity=intensity)
            docx_file = ai_humanizer.generate_humanized_docx(
                original_text=extracted_text,
                humanized_text=h_res["humanized_text"],
                doc_title=title,
                markers_info=h_res
            )
            pdf_file = ai_humanizer.generate_humanized_pdf(
                original_text=extracted_text,
                humanized_text=h_res["humanized_text"],
                doc_title=title,
                markers_info=h_res
            )
            h_res["pdf_metadata"] = ext_res.get("metadata")
            h_res["total_pages"] = ext_res.get("total_pages")
            h_res["processed_pages"] = ext_res.get("processed_pages")
            h_res["is_truncated"] = ext_res.get("is_truncated", False)
            h_res["truncation_notice"] = ext_res.get("truncation_notice", "")
            h_res["download_url"] = f"/api/download/{docx_file}"
            h_res["filename"] = docx_file
            h_res["pdf_download_url"] = f"/api/download/{pdf_file}"
            h_res["pdf_filename"] = pdf_file

            # Optimization for UI: Smart-sort sentence pairs — flagged first, then green
            all_pairs = h_res.get("sentence_pairs", [])
            h_res["total_sentence_count"] = len(all_pairs)
            if len(all_pairs) > 500:
                flagged = [p for p in all_pairs if p.get("status") in ("ai", "mixed") or p.get("action_label") in ("WAJIB DIGANTI", "PERTIMBANGKAN REVISI", "REVISI BAKU KBBI")]
                green = [p for p in all_pairs if p not in flagged]
                remaining_slots = max(0, 500 - len(flagged))
                smart_pairs = flagged + green[:remaining_slots]
                # Re-sort by original index for display consistency
                smart_pairs.sort(key=lambda x: x.get("index", 0))
                h_res["sentence_pairs"] = smart_pairs
                h_res["ui_sentence_limit"] = 500
                h_res["ui_flagged_count"] = len(flagged)

            print(json.dumps(h_res, ensure_ascii=False))

        elif action in ["grammar_check", "grammar"]:
            text = payload.get("text", "")
            res = ai_humanizer.grammar_check(text)
            print(json.dumps(res, ensure_ascii=False))

        elif action in ["plagiarism_check", "plagiarism"]:
            text = payload.get("text", "")
            res = ai_humanizer.check_plagiarism(text)
            print(json.dumps(res, ensure_ascii=False))

        elif action in ["paraphrase", "paraphraser"]:
            text = payload.get("text", "")
            mode = payload.get("mode", "formal_spbe")
            intensity = payload.get("intensity", "balanced")
            res = ai_humanizer.humanize_and_rephrase(text, mode=mode, intensity=intensity)
            print(json.dumps(res, ensure_ascii=False))

        elif action in ["summarize", "summarizer"]:
            text = payload.get("text", "")
            ratio = payload.get("ratio", "medium")
            res = ai_humanizer.summarize_text(text, ratio=ratio)
            print(json.dumps(res, ensure_ascii=False))

        elif action in ["explain_topic", "explain"]:
            topic = payload.get("topic", payload.get("text", ""))
            audience = payload.get("audience", "executive")
            res = ai_humanizer.explain_topic(topic, audience=audience)
            print(json.dumps(res, ensure_ascii=False))

        elif action in ["citations", "citations_tool"]:
            title = payload.get("title", "Judul Rujukan")
            author = payload.get("author", "Kementerian / Penulis")
            year = payload.get("year", "2024")
            publisher = payload.get("publisher", "Penerbit Resmi")
            url = payload.get("url", "")
            res = ai_humanizer.generate_citations(title, author, year, publisher, url)
            print(json.dumps(res, ensure_ascii=False))

        elif action in ["organize_notes", "notes"]:
            notes = payload.get("notes", payload.get("text", ""))
            res = ai_humanizer.organize_notes(notes)
            print(json.dumps(res, ensure_ascii=False))

        elif action in ["study_planner", "study_plan", "study-plan", "planner"]:
            topic = payload.get("topic", payload.get("text", "Tata Kelola SPBE"))
            duration = payload.get("duration", "7_days")
            res = ai_humanizer.generate_study_plan(topic, duration)
            print(json.dumps(res, ensure_ascii=False))

        else:
            print(json.dumps({"status": "error", "message": f"Aksi tidak dikenal: '{action}'"}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
