import os
import re
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        # Header line
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 800, 555, 800)
        self.drawString(40, 805, "NEXUS AI ENTERPRISE — Audit Forensik & Rekayasa Humanisasi KBBI")
        # Footer line
        self.line(40, 45, 555, 45)
        self.drawString(40, 32, "Dokumen Resmi SPBE / Naskah Dinas Terverifikasi KBBI & EYD V")
        page_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(555, 32, page_text)
        self.restoreState()

print("NumberedCanvas ready")
