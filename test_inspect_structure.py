import os
import re
from pypdf import PdfReader

pdf_path = r"C:\Users\LENOVO\.gemini\antigravity\scratch\NEXUS-AI-ENTERPRISE\uploads\Arsitektur_SPBE_DKI_Jakarta_2027.pdf"
reader = PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

# Let's inspect page 1 to 25
for page_num in range(min(25, len(reader.pages))):
    text = reader.pages[page_num].extract_text()
    first_line = text.splitlines()[0] if text.splitlines() else "EMPTY"
    has_dots = bool(re.search(r'\.{4,}|…{2,}', text))
    has_bab = bool(re.search(r'Bab\s+[IVXLCDM0-9]+', text, re.IGNORECASE))
    print(f"Page {page_num+1}: len={len(text)}, has_dots={has_dots}, has_bab={has_bab}, first_line={first_line[:50]}")
    if has_bab:
        for l in text.splitlines()[:10]:
            if "bab" in l.lower() or "latar" in l.lower() or "1.1" in l:
                print(f"   -> {l}")
