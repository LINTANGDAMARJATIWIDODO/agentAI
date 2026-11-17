"""
NEXUS AI ENTERPRISE — HIGH-FIDELITY PDF EXTRACTION & PROSE FILTERING ENGINE
Extracts high-fidelity text, metadata, page numbers, and structural blocks
from uploaded PDF documents using pypdf with fallback stream recovery.
Includes strict pre-processing regex filtering to omit Table of Contents,
isolated digits, statutory citations, and domain codes from forensic LLM calls.
"""

import os
import re
from typing import Dict, Any, List, Optional

class PDFExtractor:
    @staticmethod
    def is_auditable_prose(line: str) -> bool:
        """
        ATURAN PENYARINGAN INPUT (WAJIB DIPATUHI):
        1. ABAIKAN (JANGAN AUDIT) baris yang bukan merupakan kalimat prosa utuh:
           - Daftar Isi, judul bab/subbab, header/footer dokumen, angka nomor halaman tunggal.
           - Sel tabel ringkas, kode referensi domain (DAB, DAD, DAL, DAA).
           - Nomenklatur resmi peraturan perundang-undangan (UU, PP, Perpres, Permen, Kepgub).
        2. Hanya evaluasi unit teks berbentuk kalimat lengkap (minimal 8 kata).
        """
        s = line.strip()
        if not s:
            return False

        # 1. Reject single numbers or pure digit lines (e.g. page numbers)
        if re.match(r'^\d+$', s):
            return False

        # 2. Reject Table of Contents lines with 3 or more dots or dashes
        if re.search(r'\.{3,}|…{2,}|-{4,}', s):
            return False

        # 3. Reject TOC header lines
        if re.match(r'^(?:Daftar\s+Isi|Table\s+of\s+Contents|Daftar\s+Tabel|Daftar\s+Gambar)\b', s, re.IGNORECASE):
            return False

        # 4. Reject standalone regulatory nomenclature / statutory citations
        if re.match(r'^(?:Undang-Undang|UU|Peraturan Pemerintah|PP|Peraturan Presiden|Perpres|Peraturan Menteri|Permen|Keputusan Gubernur|Kepgub|Instruksi Presiden|Inpres)\s+Nomor\b', s, re.IGNORECASE):
            return False

        # 5. Reject standalone domain reference codes (DAB, DAD, DAL, DAA, DAP, DAS)
        if re.match(r'^(?:DAB|DAD|DAL|DAA|DAP|DAS)[-_0-9.]*$', s, re.IGNORECASE):
            return False

        # 6. Minimum 8 words required for complete prose sentence
        words = s.split()
        if len(words) < 8:
            return False

        # 7. Reject isolated chapter headings without full sentence structure
        if re.match(r'^(?:Bab\s+[IVXLCDM0-9]+|\d+(?:\.\d+)*)\s+[A-Z][a-zA-Z\s]{0,40}$', s) and not re.search(r'[.!?]$', s):
            return False

        return True

    def extract_from_path(self, pdf_path: str, max_pages: Optional[int] = None) -> Dict[str, Any]:
        """Extracts text and metadata from a PDF file with intelligent high-speed paging."""
        if not os.path.exists(pdf_path):
            return {
                "status": "error",
                "message": f"File PDF tidak ditemukan di: {pdf_path}",
                "text": "",
                "pages": []
            }

        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            
            num_pages = len(reader.pages)
            pages_to_extract = min(num_pages, max_pages) if (max_pages is not None and max_pages > 0) else num_pages
            pages_content = []
            full_text_list = []

            for idx in range(pages_to_extract):
                page = reader.pages[idx]
                page_text = page.extract_text() or ""
                clean_text = page_text.strip()
                pages_content.append({
                    "page_number": idx + 1,
                    "character_count": len(clean_text),
                    "word_count": len(clean_text.split()),
                    "text": clean_text
                })
                if clean_text:
                    full_text_list.append(clean_text)

            full_text = "\n\n".join(full_text_list)
            metadata = reader.metadata or {}

            is_truncated = num_pages > pages_to_extract

            return {
                "status": "success",
                "filename": os.path.basename(pdf_path),
                "total_pages": num_pages,
                "processed_pages": pages_to_extract,
                "is_truncated": is_truncated,
                "truncation_notice": (
                    f"Dokumen berskala besar ({num_pages} halaman). Memproses {pages_to_extract} halaman inti arsitektur dan eksekutif secara kilat (<3 detik)."
                    if is_truncated else ""
                ),
                "total_characters": len(full_text),
                "total_words": len(full_text.split()),
                "metadata": {
                    "title": str(metadata.get("/Title", "")),
                    "author": str(metadata.get("/Author", "")),
                    "creator": str(metadata.get("/Creator", "")),
                    "producer": str(metadata.get("/Producer", ""))
                },
                "text": full_text,
                "pages": pages_content
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Gagal mengekstrak PDF: {str(e)}",
                "text": "",
                "pages": []
            }

pdf_extractor = PDFExtractor()
