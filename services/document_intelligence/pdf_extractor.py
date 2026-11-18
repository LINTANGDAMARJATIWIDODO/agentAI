"""
NEXUS AI ENTERPRISE — HIGH-FIDELITY PDF EXTRACTION & PROSE FILTERING ENGINE
=============================================================================
Layout-aware PDF extraction and intelligent prose-table separation:
1. Layout-Aware Filtering: Separates narrative prose from table matrices, code catalogs, and appendices.
2. Artifact Normalization: Unbreaks hyphenated line breaks, cleans raw LaTeX ($...$), normalizes UTF-8 encoding.
3. Robust Sentence Tokenization: Preserves numbered lists (1., 7., 12.), statutory abbreviations
   (Perpres, UU, PP, No., dkk., hlm.), decimal points, and suppresses running headers/footers.
"""

import os
import re
from typing import Dict, Any, List, Optional, Tuple


class PDFExtractor:
    # Common Indonesian statutory & academic abbreviations that should NOT trigger sentence breaks
    ABBREVIATIONS = [
        "Perpres", "perpres", "UU", "PP", "No.", "no.", "Nomor", "dkk.", "hlm.", "hal.",
        "Prof.", "Dr.", "dr.", "Ir.", "Drs.", "Dra.", "dst.", "dll.", "dsb.",
        "S.Kom.", "M.T.", "M.Kom.", "S.T.", "S.E.", "M.M.", "S.H.", "M.H.",
        "Rp.", "a.n.", "u.b.", "d/a", "Kec.", "Kel.", "Kab.", "Prov.",
        "Kepgub", "Permen", "Inpres", "Kepmen", "SE", "Juknis", "Juklak"
    ]

    @staticmethod
    def clean_extraction_artifacts(text: str) -> str:
        """
        Cleans typical PDF extraction artifacts:
        - Normalizes corrupted UTF-8 byte sequences (e.g. â€” -> —, â€œ/â€ -> ", â€™ -> ')
        - Unbreaks hyphenated line-wrapped words (e.g. 'perang- kat' -> 'perangkat')
        - Cleans residual LaTeX markup (e.g. $...$)
        - Normalizes non-breaking spaces and excessive vertical whitespace
        """
        if not text:
            return ""

        s = text
        # 1. Normalize encoding glitches
        replacements = {
            'â€”': '—',
            'â€“': '–',
            'â€œ': '"',
            'â€': '"',
            'â€˜': "'",
            'â€™': "'",
            'â€¦': '...',
            '\xa0': ' ',
            '\u200b': '',
            '\ufeff': ''
        }
        for bad, good in replacements.items():
            s = s.replace(bad, good)

        # 2. Unbreak hyphenated line breaks (e.g. "perang-\nkat" or "perang- kat" -> "perangkat")
        s = re.sub(r'([a-zA-Z]{2,})-\s*\n\s*([a-zA-Z]{2,})', r'\1\2', s)
        s = re.sub(r'([a-zA-Z]{2,})-\s+([a-zA-Z]{2,})', r'\1\2', s)

        # 3. Clean raw LaTeX / Math symbols ($...$)
        s = re.sub(r'\$[^$\n]+\$', ' ', s)

        # 4. Remove control characters
        s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', s)

        return s

    @classmethod
    def is_header_or_footer(cls, line: str) -> bool:
        """Detects running headers, footers, and page number lines."""
        s = line.strip()
        if not s:
            return True

        # Pure numbers (e.g. page numbers)
        if re.match(r'^\d{1,4}$', s):
            return True

        # Page X of Y or Halaman X dari Y
        if re.search(r'^(?:Halaman|Page|Hal\.)\s+\d+(?:\s+(?:dari|of)\s+\d+)?$', s, re.IGNORECASE):
            return True
        if re.search(r'^\d+\s*\|\s*(?:Halaman|Page)\b', s, re.IGNORECASE):
            return True

        # Common running header phrases
        header_patterns = [
            r'^Arsitektur\s+SPBE\s+Provinsi\s+DKI\s+Jakarta(?:\s+2027)?$',
            r'^DOKUMEN\s+KONSULTASI\s+PUBLIK$',
            r'^NEXUS\s+AI\s+ENTERPRISE\b',
            r'^BAB\s+[IVXLCDM0-9]+\s*[-–—]\s*HALAMAN\b'
        ]
        for pat in header_patterns:
            if re.match(pat, s, re.IGNORECASE):
                return True

        return False

    @classmethod
    def is_table_or_matrix_line(cls, line: str) -> bool:
        """
        Detects lines that belong to tabular matrices, metadata tables, or catalog appendices
        rather than continuous narrative prose.
        """
        s = line.strip()
        if not s:
            return False

        # Table row with pipe delimiters
        if s.startswith('|') and s.endswith('|'):
            return True
        if s.count('|') >= 2:
            return True

        # Table of contents dot leaders
        if re.search(r'\.{3,}|…{2,}|(\.\s*){4,}', s):
            return True

        # Multiple tab-separated or column-spaced values
        if '\t' in s and len(s.split('\t')) >= 3:
            return True

        # Technical matrix codes: DAB-xx, DAD-xx, DAL-xx, INI-xx, G-xx, P1-P10, S1-S6
        if re.match(r'^(?:DAB|DAD|DAL|DAA|DAP|DAS|INI|GAP|P\d+|S\d+)[-_0-9.]*\s+(?:Proses|Data|Layanan|Aplikasi|Infrastruktur)', s, re.IGNORECASE):
            return True

        # Purely numeric or percentage data row (e.g., "1  24.5%  65.2%  10.3%")
        tokens = s.split()
        num_count = sum(1 for t in tokens if re.match(r'^[\d.,%+-]+$', t))
        if len(tokens) >= 3 and (num_count / len(tokens)) > 0.6:
            return True

        return False

    @classmethod
    def is_auditable_prose(cls, line: str) -> bool:
        """
        Audits whether a line is authentic prose suitable for stylistic analysis.
        Rejects headers, footers, standalone titles, and table rows.
        """
        s = line.strip()
        if not s:
            return False

        if cls.is_header_or_footer(s):
            return False

        if cls.is_table_or_matrix_line(s):
            return False

        # Standalone chapter or section titles (e.g., "Bab I Pendahuluan")
        if re.match(r'^(?:Bab\s+[IVXLCDM0-9]+|\d+(?:\.\d+)*)\s+[A-Z][a-zA-Z\s]{0,50}$', s) and not re.search(r'[.!?]$', s):
            return False

        # Standalone regulatory citations without verb/predicate
        if re.match(r'^(?:Undang-Undang|UU|Peraturan Pemerintah|PP|Peraturan Presiden|Perpres|Peraturan Menteri|Permen|Keputusan Gubernur|Kepgub)\s+Nomor\s+\d+\s+Tahun\s+\d+;?$', s, re.IGNORECASE):
            return False

        # Minimum length threshold: must have at least 6 words
        words = s.split()
        if len(words) < 6:
            return False

        return True

    @classmethod
    def segment_sentences(cls, text: str) -> List[str]:
        """
        Robust Indonesian sentence tokenizer:
        - NEVER breaks numbered lists (1., 7., 12.)
        - NEVER breaks statutory abbreviations (Perpres, UU, PP, No., dkk., hlm.)
        - NEVER breaks decimals (3.14) or single dots
        """
        cleaned = cls.clean_extraction_artifacts(text)
        if not cleaned:
            return []

        # Token replacement map for protecting boundaries
        token_map = {}
        counter = 0

        def get_placeholder(val: str) -> str:
            nonlocal counter
            ph = f"___ABBR_TOKEN_{counter}___"
            counter += 1
            token_map[ph] = val
            return ph

        protected = cleaned

        # 1. Protect abbreviations FIRST
        for abbr in cls.ABBREVIATIONS:
            pat = re.compile(rf'\b{re.escape(abbr)}', re.IGNORECASE)
            matches = list(pat.finditer(protected))
            for m in reversed(matches):
                val = m.group(0)
                ph = get_placeholder(val)
                protected = protected[:m.start()] + ph + protected[m.end():]

        # 2. Protect decimals
        def protect_decimal(m):
            return get_placeholder(m.group(0))
        protected = re.sub(r'\b\d+\.\d+\b', protect_decimal, protected)

        # 3. Protect numbered list items (e.g. ' 1. ', ' 2. ') so their '.' is not a sentence terminator
        def protect_num_dot(m):
            return m.group(1) + m.group(2) + get_placeholder('.') + m.group(3)
        protected = re.sub(r'(^|\s)(\d{1,3})\.(\s+)', protect_num_dot, protected)

        # 4. Now split on real terminal punctuation followed by whitespace
        raw_splits = re.split(r'(?<=[.!?])\s+', protected)

        sentences = []
        for s in raw_splits:
            full_s = s.strip()
            if not full_s:
                continue

            # Restore all protected tokens
            for ph, orig in token_map.items():
                full_s = full_s.replace(ph, orig)

            if cls.is_auditable_prose(full_s):
                sentences.append(full_s)

        if not sentences and cleaned.strip():
            # If strict filter yielded empty, restore protected tokens for fallback
            restored_fallback = protected
            for ph, orig in token_map.items():
                restored_fallback = restored_fallback.replace(ph, orig)
            sentences = [restored_fallback.strip()]

        return sentences

    def extract_from_path(self, pdf_path: str, max_pages: Optional[int] = None) -> Dict[str, Any]:
        """Extracts text, metadata, separates tables, and prepares clean prose for analysis."""
        if not os.path.exists(pdf_path):
            return {
                "status": "error",
                "message": f"File PDF tidak ditemukan di: {pdf_path}",
                "text": "",
                "clean_prose_text": "",
                "pages": []
            }

        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)
            pages_to_extract = min(num_pages, max_pages) if (max_pages is not None and max_pages > 0) else num_pages

            pages_content = []
            full_raw_text = []
            clean_prose_lines = []

            for idx in range(pages_to_extract):
                page = reader.pages[idx]
                raw_page_text = page.extract_text() or ""
                clean_page_text = self.clean_extraction_artifacts(raw_page_text)

                pages_content.append({
                    "page_number": idx + 1,
                    "character_count": len(clean_page_text),
                    "word_count": len(clean_page_text.split()),
                    "text": clean_page_text
                })

                if clean_page_text:
                    full_raw_text.append(clean_page_text)
                    for line in clean_page_text.splitlines():
                        s = line.strip()
                        if self.is_auditable_prose(s):
                            clean_prose_lines.append(s)

            full_text = "\n\n".join(full_raw_text)
            clean_prose_text = "\n".join(clean_prose_lines) if clean_prose_lines else full_text
            metadata = reader.metadata or {}

            # Sentence segmentation
            segmented_sentences = self.segment_sentences(clean_prose_text)

            return {
                "status": "success",
                "filename": os.path.basename(pdf_path),
                "total_pages": num_pages,
                "processed_pages": pages_to_extract,
                "is_truncated": num_pages > pages_to_extract,
                "total_characters": len(clean_prose_text),
                "total_words": len(clean_prose_text.split()),
                "total_sentences": len(segmented_sentences),
                "metadata": {
                    "title": str(metadata.get("/Title", "")),
                    "author": str(metadata.get("/Author", "")),
                    "creator": str(metadata.get("/Creator", "")),
                    "producer": str(metadata.get("/Producer", ""))
                },
                "text": clean_prose_text,
                "clean_prose_text": clean_prose_text,
                "raw_unfiltered_text": full_text,
                "sentences": segmented_sentences,
                "pages": pages_content
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Gagal mengekstrak PDF: {str(e)}",
                "text": "",
                "clean_prose_text": "",
                "pages": []
            }


pdf_extractor = PDFExtractor()
