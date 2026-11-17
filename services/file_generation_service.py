"""
NEXUS AI ENTERPRISE — File & Document Generation Service
Engineered by SEKAR (CFO), TARA (CDO), and RAKA (CTO)
Supports true downloadable files: DOCX, XLSX, ZIP, CSV, JSON, and Markdown.
"""

import os
import csv
import json
import zipfile
from datetime import datetime
from typing import Dict, List, Any, Optional

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "public", "downloads")


def ensure_dirs():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)


class FileGenerationService:
    def __init__(self):
        ensure_dirs()

    def generate_docx(
        self,
        title: str,
        subtitle: str,
        metadata: Dict[str, Any],
        sections: List[Dict[str, Any]],
        output_filename: str
    ) -> str:
        """
        Creates a rich, formatted Microsoft Word (.docx) document.
        """
        doc = docx.Document()

        # Adjust margins
        sections_doc = doc.sections
        for s in sections_doc:
            s.top_margin = Inches(0.8)
            s.bottom_margin = Inches(0.8)
            s.left_margin = Inches(0.8)
            s.right_margin = Inches(0.8)

        # Title
        p_title = doc.add_paragraph()
        run_title = p_title.add_run(title)
        run_title.font.name = "Calibri"
        run_title.font.size = Pt(22)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(26, 32, 44)
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Subtitle
        if subtitle:
            p_sub = doc.add_paragraph()
            run_sub = p_sub.add_run(subtitle)
            run_sub.font.name = "Calibri"
            run_sub.font.size = Pt(13)
            run_sub.font.italic = True
            run_sub.font.color.rgb = RGBColor(113, 128, 150)
            p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

        doc.add_paragraph()  # spacer

        # Metadata Table
        if metadata:
            table_meta = doc.add_table(rows=len(metadata) + 1, cols=2)
            table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
            table_meta.style = "Table Grid"

            hdr_cells = table_meta.rows[0].cells
            hdr_cells[0].text = "PARAMETER DOKUMEN"
            hdr_cells[1].text = "NILAI / KETERANGAN RESMI"
            for c in hdr_cells:
                for p in c.paragraphs:
                    for r in p.runs:
                        r.font.bold = True
                        r.font.size = Pt(10)

            for idx, (k, v) in enumerate(metadata.items(), start=1):
                row_cells = table_meta.rows[idx].cells
                row_cells[0].text = str(k)
                row_cells[1].text = str(v)
                for p in row_cells[0].paragraphs:
                    for r in p.runs:
                        r.font.bold = True
                        r.font.size = Pt(9.5)
                for p in row_cells[1].paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9.5)

            doc.add_paragraph()

        # Content Sections
        for sec in sections:
            sec_title = sec.get("title", "")
            sec_content = sec.get("content", "")
            bullets = sec.get("bullets", [])
            table_data = sec.get("table", None)

            if sec_title:
                h = doc.add_heading(sec_title, level=1)
                for r in h.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(14)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(43, 108, 176)

            if sec_content:
                p = doc.add_paragraph(sec_content)
                for r in p.runs:
                    r.font.size = Pt(10.5)

            for b in bullets:
                doc.add_paragraph(b, style="List Bullet")

            if table_data and isinstance(table_data, list) and len(table_data) > 0:
                headers = table_data[0]
                rows = table_data[1:]
                t = doc.add_table(rows=len(rows) + 1, cols=len(headers))
                t.alignment = WD_TABLE_ALIGNMENT.CENTER
                t.style = "Table Grid"

                for col_idx, h_text in enumerate(headers):
                    cell = t.rows[0].cells[col_idx]
                    cell.text = str(h_text)
                    for p in cell.paragraphs:
                        for r in p.runs:
                            r.font.bold = True
                            r.font.size = Pt(9.5)

                for r_idx, row_vals in enumerate(rows, start=1):
                    for c_idx, val in enumerate(row_vals):
                        cell = t.rows[r_idx].cells[c_idx]
                        cell.text = str(val)
                        for p in cell.paragraphs:
                            for r in p.runs:
                                r.font.size = Pt(9)

                doc.add_paragraph()

        # Footer
        p_foot = doc.add_paragraph()
        r_foot = p_foot.add_run(f"Diterbitkan secara otonom oleh NEXUS AI ENTERPRISE • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        r_foot.font.size = Pt(8.5)
        r_foot.font.italic = True
        r_foot.font.color.rgb = RGBColor(160, 174, 192)
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        # Save to reports and downloads
        clean_name = output_filename if output_filename.endswith(".docx") else f"{output_filename}.docx"
        out_report = os.path.join(REPORTS_DIR, clean_name)
        out_download = os.path.join(DOWNLOADS_DIR, clean_name)

        doc.save(out_report)
        doc.save(out_download)
        return out_download

    def generate_xlsx(
        self,
        title: str,
        sheets: List[Dict[str, Any]],
        output_filename: str
    ) -> str:
        """
        Creates a professional multi-sheet Excel spreadsheet (.xlsx).
        """
        wb = openpyxl.Workbook()
        thin_border = Border(
            left=Side(style="thin", color="CBD5E0"),
            right=Side(style="thin", color="CBD5E0"),
            top=Side(style="thin", color="CBD5E0"),
            bottom=Side(style="thin", color="CBD5E0")
        )
        primary_fill = PatternFill(start_color="1A365D", fill_type="solid")
        gold_fill = PatternFill(start_color="D69E2E", fill_type="solid")
        alt_fill = PatternFill(start_color="F7FAFC", fill_type="solid")

        for s_idx, s_data in enumerate(sheets):
            if s_idx == 0:
                ws = wb.active
                ws.title = s_data.get("title", "Sheet1")
            else:
                ws = wb.create_sheet(title=s_data.get("title", f"Sheet{s_idx+1}"))

            ws.views.sheetView[0].showGridLines = True

            sheet_header = s_data.get("header_text", title)
            ws["A1"] = sheet_header
            ws["A1"].font = Font(name="Calibri", size=13, bold=True, color="1A202C")

            headers = s_data.get("columns", [])
            rows = s_data.get("rows", [])

            if headers:
                for c_idx, h in enumerate(headers, start=1):
                    cell = ws.cell(row=3, column=c_idx, value=h)
                    cell.fill = primary_fill if s_idx == 0 else gold_fill
                    cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF" if s_idx == 0 else "000000")
                    cell.border = thin_border

            for r_idx, r_vals in enumerate(rows, start=4):
                for c_idx, val in enumerate(r_vals, start=1):
                    cell = ws.cell(row=r_idx, column=c_idx, value=val)
                    cell.border = thin_border
                    cell.font = Font(name="Calibri", size=10)
                    if r_idx % 2 == 1:
                        cell.fill = alt_fill

            # Auto-fit column widths
            for col in ws.columns:
                max_len = max(len(str(cell.value or "")) for cell in col)
                col_letter = openpyxl.utils.get_column_letter(col[0].column)
                ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

        clean_name = output_filename if output_filename.endswith(".xlsx") else f"{output_filename}.xlsx"
        out_report = os.path.join(REPORTS_DIR, clean_name)
        out_download = os.path.join(DOWNLOADS_DIR, clean_name)

        wb.save(out_report)
        wb.save(out_download)
        return out_download

    def generate_zip_project(
        self,
        source_dir: str,
        output_filename: str,
        extra_files: Optional[List[str]] = None
    ) -> str:
        """
        Compresses an entire project folder into a downloadable .zip archive.
        """
        clean_name = output_filename if output_filename.endswith(".zip") else f"{output_filename}.zip"
        out_report = os.path.join(REPORTS_DIR, clean_name)
        out_download = os.path.join(DOWNLOADS_DIR, clean_name)

        with zipfile.ZipFile(out_download, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.exists(source_dir):
                for root, dirs, files in os.walk(source_dir):
                    # Exclude node_modules or pycache
                    dirs[:] = [d for d in dirs if d not in ["node_modules", ".git", "__pycache__"]]
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, os.path.dirname(source_dir))
                        zf.write(full_path, rel_path)

            if extra_files:
                for ef in extra_files:
                    if os.path.exists(ef):
                        zf.write(ef, os.path.basename(ef))

        # Also copy to reports
        if os.path.exists(out_download):
            with open(out_download, "rb") as f_in, open(out_report, "wb") as f_out:
                f_out.write(f_in.read())

        return out_download

    def generate_csv(self, headers: List[str], rows: List[List[Any]], output_filename: str) -> str:
        clean_name = output_filename if output_filename.endswith(".csv") else f"{output_filename}.csv"
        out_download = os.path.join(DOWNLOADS_DIR, clean_name)
        out_report = os.path.join(REPORTS_DIR, clean_name)

        with open(out_download, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        with open(out_report, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        return out_download

    def generate_json_file(self, data: Any, output_filename: str) -> str:
        clean_name = output_filename if output_filename.endswith(".json") else f"{output_filename}.json"
        out_download = os.path.join(DOWNLOADS_DIR, clean_name)
        out_report = os.path.join(REPORTS_DIR, clean_name)

        with open(out_download, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        with open(out_report, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return out_download


# Global Singleton
file_generator = FileGenerationService()
