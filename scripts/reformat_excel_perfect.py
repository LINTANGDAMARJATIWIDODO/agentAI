"""
NEXUS AI ENTERPRISE — PROFESSIONAL EXCEL REFORMATTING ENGINE
Fixes all row-height overlapping, cramped column widths, text clipping, and alignment issues.
Produces a beautiful, clean, modern, and easily readable spreadsheet report.
"""

import os
import math
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "output", "spreadsheets", "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "spreadsheets", "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx")
PUBLIC_FILE = os.path.join(BASE_DIR, "public", "downloads", "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx")

# Palette
HEADER_FILL = PatternFill(start_color="9BC2E6", end_color="9BC2E6", fill_type="solid") # Official Pastel Blue
HEADER_FILL_YELLOW = PatternFill(start_color="FEF08A", end_color="FEF08A", fill_type="solid")
TITLE_BG = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Navy
ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid") # Soft tint
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

TITLE_FONT = Font(name="Segoe UI", size=13, bold=True, color="FFFFFF")
SHEET_TITLE_FONT = Font(name="Segoe UI", size=12, bold=True, color="1E3A8A")
HEADER_FONT = Font(name="Segoe UI", size=9.5, bold=True, color="0F172A")
BODY_FONT = Font(name="Segoe UI", size=9.5, color="1E293B")
BOLD_BODY_FONT = Font(name="Segoe UI", size=9.5, bold=True, color="1E293B")
NOTE_FONT = Font(name="Segoe UI", size=9, italic=True, color="64748B")

THIN_BORDER = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

HEADER_BORDER = Border(
    left=Side(style='thin', color='64748B'),
    right=Side(style='thin', color='64748B'),
    top=Side(style='medium', color='1E3A8A'),
    bottom=Side(style='medium', color='1E3A8A')
)

ALIGN_HEADER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_DATA_TOP_LEFT = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_DATA_TOP_CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)

def reformat_workbook(wb_path):
    wb = openpyxl.load_workbook(wb_path)
    
    for sname in wb.sheetnames:
        ws = wb[sname]
        ws.views.sheetView[0].showGridLines = True
        
        # 1. Identify Header Row (usually row 4 or row 1 or row 6)
        header_row_idx = None
        for r in range(1, min(ws.max_row + 1, 8)):
            first_val = str(ws.cell(r, 1).value or '').strip().upper()
            if first_val in ['NO', 'DOMAIN']:
                header_row_idx = r
                break
        
        if not header_row_idx:
            header_row_idx = 1
            
        # Determine column structure
        max_col = ws.max_column
        is_5_col = (max_col >= 5 and 'GAGAL' in sname.upper()) or 'GAGAL' in sname.upper()
        
        # Format sheet title if present above header
        for r in range(1, header_row_idx):
            cell_val = str(ws.cell(r, 1).value or '').strip()
            if cell_val:
                ws.cell(r, 1).font = SHEET_TITLE_FONT
                ws.row_dimensions[r].height = 28
            else:
                ws.row_dimensions[r].height = 14
        
        # Format Header Row
        ws.row_dimensions[header_row_idx].height = 28
        for c in range(1, max_col + 1):
            cell = ws.cell(header_row_idx, c)
            cell.font = HEADER_FONT
            if cell.fill.start_color.rgb not in ['FFFFFF00', 'D9E1F2']:
                cell.fill = HEADER_FILL
            cell.alignment = ALIGN_HEADER
            cell.border = HEADER_BORDER
            
        # Format Data Rows
        for r in range(header_row_idx + 1, ws.max_row + 1):
            row_has_data = any(ws.cell(r, c).value for c in range(1, max_col + 1))
            if not row_has_data:
                continue
                
            is_zebra = (r % 2 == 0)
            row_fill = ZEBRA_FILL if is_zebra else WHITE_FILL
            
            # Calculate required row height
            max_lines_in_row = 1
            for c in range(1, max_col + 1):
                cell = ws.cell(r, c)
                val_str = str(cell.value or '').strip()
                if not val_str:
                    continue
                
                # Count explicit newlines
                explicit_lines = val_str.count('\n') + 1
                
                # Estimate wrapped lines based on estimated col width
                col_w = 40 if c in [2, 4] else (65 if c == 5 else 25)
                wrapped_lines = max(1, math.ceil(len(val_str) / col_w))
                
                effective_lines = max(explicit_lines, wrapped_lines)
                if effective_lines > max_lines_in_row:
                    max_lines_in_row = effective_lines
                    
            # Set generous row height: min 24pt, +14pt per additional line + padding
            calculated_height = max(24, max_lines_in_row * 15.5 + 8)
            ws.row_dimensions[r].height = min(calculated_height, 220) # cap to prevent huge blank rows
            
            # Style each cell in the row
            for c in range(1, max_col + 1):
                cell = ws.cell(r, c)
                cell.font = BODY_FONT
                cell.border = THIN_BORDER
                
                # Preserve special status fills (green, red, yellow) if already present
                existing_color = cell.fill.start_color.rgb if cell.fill else ''
                if existing_color in ['DCFCE7', 'FEE2E2', 'FEF3C7']:
                    pass
                else:
                    cell.fill = row_fill
                
                # Alignment
                if c == 1:
                    cell.alignment = ALIGN_DATA_TOP_CENTER
                elif c == 3 and not is_5_col:
                    cell.alignment = ALIGN_DATA_TOP_LEFT
                else:
                    cell.alignment = ALIGN_DATA_TOP_LEFT
                    
        # Set Optimized Column Widths (Generous, no text clipping)
        if is_5_col:
            # 5 Columns: NO, PERANGKAT DAERAH, DOMAIN, ID - Nama Data, Nama Kolom yang belum terisi
            ws.column_dimensions['A'].width = 8
            ws.column_dimensions['B'].width = 44
            ws.column_dimensions['C'].width = 32
            ws.column_dimensions['D'].width = 50
            ws.column_dimensions['E'].width = 70
        elif max_col == 3:
            # 3 Columns: NO, PERANGKAT DAERAH, DOMAIN
            ws.column_dimensions['A'].width = 8
            ws.column_dimensions['B'].width = 44
            ws.column_dimensions['C'].width = 38
        else:
            # General sheet
            for c in range(1, max_col + 1):
                col_letter = get_column_letter(c)
                max_len = 0
                for r in range(header_row_idx, ws.max_row + 1):
                    val = str(ws.cell(r, c).value or '')
                    # for multiline, check max line length
                    line_lens = [len(l) for l in val.split('\n')]
                    m_line = max(line_lens) if line_lens else 0
                    if m_line > max_len:
                        max_len = m_line
                ws.column_dimensions[col_letter].width = min(max(max_len + 4, 14), 55)

    wb.save(wb_path)
    print(f"[REFORMAT SUCCESS] {wb_path} reformatted with generous row heights and column widths!")

PUBLIC_DL_DIR = os.path.join(BASE_DIR, "public", "downloads")

if __name__ == "__main__":
    # Reformat Master Report
    reformat_workbook(INPUT_FILE)

    # Copy to public/downloads
    import shutil
    shutil.copyfile(INPUT_FILE, PUBLIC_FILE)

    # Reformat 03C Jaksel Template as well
    file_03c = os.path.join(BASE_DIR, "output", "spreadsheets", "03C_TOBE_ASIS_Kota_Administrasi_Jakarta_Selatan_TERISI.xlsx")
    if os.path.exists(file_03c):
        reformat_workbook(file_03c)
        shutil.copyfile(file_03c, os.path.join(PUBLIC_DL_DIR, "03C_TOBE_ASIS_Kota_Administrasi_Jakarta_Selatan_TERISI.xlsx"))
