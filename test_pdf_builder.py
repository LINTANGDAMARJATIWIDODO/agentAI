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
        self.drawString(40, 805, "NEXUS AI ENTERPRISE — Audit Forensik & Naskah Humanisasi KBBI")
        # Footer line
        self.line(40, 45, 555, 45)
        self.drawString(40, 32, "Dokumen Resmi SPBE / Naskah Dinas Terverifikasi KBBI & EYD V")
        page_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(555, 32, page_text)
        self.restoreState()

def escape_xml(text):
    if not text:
        return ""
    text = str(text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text

def build_pdf(original_text, humanized_text, markers_info, filename="test_output.pdf"):
    out_dir = "public/downloads"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1, # Center
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#64748B'),
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyTextJustified',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        alignment=4 # Justified
    )

    table_header_style = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Title
    story.append(Paragraph("NEXUS AI ENTERPRISE — AUDIT FORENSIK AI & NASKAH HASIL HUMANISASI", title_style))
    story.append(Paragraph("Laporan Deteksi Multi-Vektor & Naskah Resmi Berstandar Baku KBBI (Pedoman EYD V)", subtitle_style))

    # Summary box
    b_score = markers_info.get("ai_score_before", 55.0)
    a_score = markers_info.get("ai_score_after", 3.2)
    sentence_pairs = markers_info.get("sentence_pairs", [])
    cnt_ai = sum(1 for s in sentence_pairs if s.get("status") == "ai")
    cnt_mixed = sum(1 for s in sentence_pairs if s.get("status") == "mixed")
    cnt_human = sum(1 for s in sentence_pairs if s.get("status") == "human")
    total_s = len(sentence_pairs)

    summary_data = [
        [
            Paragraph(f"<b>📊 SKOR PROBABILITAS AI:</b><br/>• Sebelum: <b>{b_score}%</b> (Terdeteksi Mesin)<br/>• Sesudah: <b>{a_score}%</b> (Alami Manusia)<br/>• Penurunan: <b>-{round(max(0, b_score - a_score), 1)}%</b> (Bypass Sukses)", table_cell_style),
            Paragraph(f"<b>🎯 STANDAR LINGUISTIK:</b><br/>• Standar: <b>Kamus Besar Bahasa Indonesia (KBBI)</b><br/>• Ejaan: <b>EYD V (Tanda Baca & Koma Rujukan)</b><br/>• Waktu: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}", table_cell_style)
        ],
        [
            Paragraph(f"<b>🔍 RINCIAN STATUS AUDIT:</b><br/>• 🔴 Wajib Diganti: <b>{cnt_ai}</b> kalimat<br/>• 🟡 Pertimbangkan Revisi: <b>{cnt_mixed}</b> kalimat<br/>• 🟢 Dipertahankan: <b>{cnt_human}</b> kalimat", table_cell_style),
            Paragraph(f"<b>💡 PETUNJUK RESMI:</b><br/>1. Tabel Matriks menunjukkan kalimat yang direvisi.<br/>2. Bagian 2 memuat naskah utuh siap cetak.", table_cell_style)
        ]
    ]

    summary_table = Table(summary_data, colWidths=[255, 255])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1E3A8A')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))

    # Section 1: Matrix
    story.append(Paragraph("1. Matriks Audit Komparasi: Rekomendasi Kalimat Baku KBBI", h1_style))
    story.append(Paragraph("<i>Tabel di bawah ini menguraikan perbandingan kalimat asli vs rekomendasi resmi berstandar baku KBBI & EYD V.</i>", subtitle_style))

    # Build Table Rows
    display_pairs = sentence_pairs[:200] if len(sentence_pairs) > 200 else sentence_pairs
    matrix_data = [
        [
            Paragraph("<b>No.</b>", table_header_style),
            Paragraph("<b>Naskah Asli & Ciri Klise</b>", table_header_style),
            Paragraph("<b>Status & Skor AI</b>", table_header_style),
            Paragraph("<b>Rekomendasi Naskah Baku KBBI</b>", table_header_style)
        ]
    ]

    for idx, p in enumerate(display_pairs):
        st = p.get("status", "human")
        act = p.get("action_label", "DIPERTAHANKAN")
        prob = p.get("ai_probability", 5.0)

        # Style based on status
        if st == "ai":
            status_text = f"<font color='#DC2626'><b>🔴 WAJIB DIGANTI</b></font><br/>Skor AI: {prob}%"
            rec_text = f"<b>{escape_xml(p.get('transformed', p.get('replacement_text', '')))}</b>"
        elif st == "mixed" or "REVISI" in act:
            status_text = f"<font color='#D97706'><b>🟡 REVISI DISARANKAN</b></font><br/>Skor AI: {prob}%"
            rec_text = f"<b>{escape_xml(p.get('transformed', p.get('replacement_text', '')))}</b>"
        else:
            status_text = f"<font color='#059669'><b>🟢 DIPERTAHANKAN</b></font><br/>Skor AI: {prob}% (Aman)"
            rec_text = f"<font color='#475569'>{escape_xml(p.get('original', ''))}</font>"

        orig_disp = escape_xml(p.get("original", "")[:300])
        matrix_data.append([
            Paragraph(str(p.get("index", idx + 1)), table_cell_style),
            Paragraph(orig_disp, table_cell_style),
            Paragraph(status_text, table_cell_style),
            Paragraph(rec_text, table_cell_style)
        ])

    matrix_table = Table(matrix_data, colWidths=[25, 175, 110, 200], repeatRows=1)
    matrix_style = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1E3A8A')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]

    for r_idx in range(1, len(matrix_data)):
        if r_idx % 2 == 0:
            matrix_style.append(('BACKGROUND', (0, r_idx), (-1, r_idx), colors.HexColor('#F8FAFC')))

    matrix_table.setStyle(TableStyle(matrix_style))
    story.append(matrix_table)
    story.append(Spacer(1, 14))

    # Section 2: Rebuilt Full Text
    story.append(PageBreak())
    story.append(Paragraph("2. Naskah Lengkap Final Hasil Humanisasi (Standar Baku KBBI & Siap Pakai)", h1_style))
    story.append(Paragraph("<i>Naskah berikut merupakan dokumen utuh yang telah diselaraskan dengan tata bahasa resmi, eliminasi pola kalimat robotik, dan perbaikan tanda baca sesuai pedoman EYD V.</i>", subtitle_style))
    story.append(Spacer(1, 8))

    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', humanized_text) if p.strip()]
    for p_block in paragraphs:
        for line in p_block.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            is_heading = not re.search(r'[.!?]$', line_str) and (len(line_str.split()) <= 10 or re.match(r'^(?:Bab|[0-9]+(?:\.[0-9]+)*)\b', line_str, re.IGNORECASE))
            if is_heading:
                h_style = ParagraphStyle(
                    'SubH',
                    parent=styles['Heading3'],
                    fontName='Helvetica-Bold',
                    fontSize=10.5,
                    leading=14,
                    textColor=colors.HexColor('#1E3A8A'),
                    spaceBefore=8,
                    spaceAfter=3
                )
                story.append(Paragraph(escape_xml(line_str), h_style))
            else:
                story.append(Paragraph(escape_xml(line_str), body_style))
                story.append(Spacer(1, 4))
        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {out_path} (Size: {os.path.getsize(out_path)} bytes)")
    return filename

if __name__ == "__main__":
    from services.document_intelligence.ai_humanizer import AIHumanizer
    h = AIHumanizer()
    sample = "Bab ini menurunkannya menjadi arsitektur pada enam domain: proses bisnis, data dan informasi, layanan, aplikasi, infrastruktur, dan keamanan. Bab II menetapkan arah dan aturan main pada tingkat provinsi."
    res = h.humanize_and_rephrase(sample)
    build_pdf(sample, res["humanized_text"], res, "test_sample_built.pdf")
