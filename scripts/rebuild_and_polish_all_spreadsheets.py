"""
NEXUS AI ENTERPRISE — MASTER EXCEL CLEANING & POLISHING ENGINE
Standardizes every sheet with:
1. Uniform Title, Subtitle, and Header layout
2. Generous column widths (no text cut off horizontally)
3. Dynamic, generous row heights (no text overlapping vertically)
4. Vertical-top alignment for natural reading
5. Soft zebra striping (white and soft cool slate #F8FAFC)
6. Clean, elegant gridlines & borders (#CBD5E1)
"""

import os
import math
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_FILE = os.path.join(BASE_DIR, "knowledge", "google-drive", "reference_report_template.xlsx")
OUTPUT_MASTER = os.path.join(BASE_DIR, "output", "spreadsheets", "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx")
OUTPUT_03C = os.path.join(BASE_DIR, "output", "spreadsheets", "03C_TOBE_ASIS_Kota_Administrasi_Jakarta_Selatan_TERISI.xlsx")
PUBLIC_DL_DIR = os.path.join(BASE_DIR, "public", "downloads")
os.makedirs(PUBLIC_DL_DIR, exist_ok=True)

# Styles
COLOR_HEADER_BLUE = "9BC2E6"
COLOR_HEADER_YELLOW = "FFFF00"
COLOR_TITLE_NAVY = "1E3A8A"
COLOR_ZEBRA = "F8FAFC"
COLOR_BORDER = "CBD5E1"

FILL_HEADER_BLUE = PatternFill(start_color=COLOR_HEADER_BLUE, end_color=COLOR_HEADER_BLUE, fill_type="solid")
FILL_HEADER_YELLOW = PatternFill(start_color=COLOR_HEADER_YELLOW, end_color=COLOR_HEADER_YELLOW, fill_type="solid")
FILL_ZEBRA = PatternFill(start_color=COLOR_ZEBRA, end_color=COLOR_ZEBRA, fill_type="solid")
FILL_WHITE = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

FONT_SHEET_TITLE = Font(name="Segoe UI", size=13, bold=True, color=COLOR_TITLE_NAVY)
FONT_SUBTITLE = Font(name="Segoe UI", size=9.5, italic=True, color="64748B")
FONT_HEADER = Font(name="Segoe UI", size=9.5, bold=True, color="0F172A")
FONT_BODY = Font(name="Segoe UI", size=9.5, color="1E293B")
FONT_BOLD_BODY = Font(name="Segoe UI", size=9.5, bold=True, color="1E293B")

BORDER_CLEAN = Border(
    left=Side(style='thin', color=COLOR_BORDER),
    right=Side(style='thin', color=COLOR_BORDER),
    top=Side(style='thin', color=COLOR_BORDER),
    bottom=Side(style='thin', color=COLOR_BORDER)
)

BORDER_HEADER = Border(
    left=Side(style='thin', color='64748B'),
    right=Side(style='thin', color='64748B'),
    top=Side(style='medium', color=COLOR_TITLE_NAVY),
    bottom=Side(style='medium', color=COLOR_TITLE_NAVY)
)

ALIGN_HEADER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_DATA_TOP_LEFT = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_DATA_TOP_CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)

# -------------------------------------------------------------------------
# BUILD MASTER AUDIT WORKBOOK FROM SCRATCH WITH CLEAN DATA & PERFECT LAYOUT
# -------------------------------------------------------------------------
ref_wb = openpyxl.load_workbook(REF_FILE, data_only=True) if os.path.exists(REF_FILE) else None
new_wb = openpyxl.Workbook()
new_wb.remove(new_wb.active) # Remove default sheet

def add_standard_audit_sheet(wb, title, sheet_type, opd_name, data_rows):
    """
    Adds a standardized sheet:
    sheet_type: 'GAGAL' (5 cols) or 'BELUM_ADA' (3 cols)
    """
    ws = wb.create_sheet(title=title)
    ws.views.sheetView[0].showGridLines = True
    
    # Row 1: Margin
    ws.row_dimensions[1].height = 12
    
    # Row 2: Title
    ws.cell(2, 1, value=f"{title} — {opd_name}").font = FONT_SHEET_TITLE
    ws.row_dimensions[2].height = 26
    
    # Row 3: Subtitle
    if sheet_type == 'GAGAL':
        sub = "Daftar ID data arsitektur SPBE dan rincian kolom mandatory yang belum terisi / gagal simpan"
    else:
        sub = "Daftar domain arsitektur SPBE yang belum dibuat / belum memiliki data (kosong total)"
    ws.cell(3, 1, value=sub).font = FONT_SUBTITLE
    ws.row_dimensions[3].height = 18
    
    # Row 4: Spacer
    ws.row_dimensions[4].height = 8
    
    # Row 5: Table Header
    headers = ["NO", "PERANGKAT DAERAH", "DOMAIN", "ID - Nama Data", "Nama Kolom yang belum terisi"] if sheet_type == 'GAGAL' else ["NO", "PERANGKAT DAERAH", "DOMAIN"]
    ws.row_dimensions[5].height = 28
    
    for ci, h in enumerate(headers, 1):
        c = ws.cell(5, ci, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER_BLUE
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER
        
    # Data Rows starting Row 6
    for idx, row in enumerate(data_rows, 6):
        is_zebra = (idx % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        # Clean cell text
        cleaned_row = [str(item or '').strip() for item in row]
        
        # Calculate row height based on content
        max_lines = 1
        for ci, val in enumerate(cleaned_row, 1):
            if not val:
                continue
            # Newlines count
            nl_count = val.count('\n') + 1
            # Length estimate
            col_limit = 42 if ci in [2, 4] else (68 if ci == 5 else 28)
            wrap_count = max(1, math.ceil(len(val) / col_limit))
            eff = max(nl_count, wrap_count)
            if eff > max_lines:
                max_lines = eff
                
        # Generous row height: 26pt for single line, +16pt per additional line
        row_height = max(26, max_lines * 16.5 + 8)
        ws.row_dimensions[idx].height = min(row_height, 240)
        
        # Populate cells
        for ci, val in enumerate(cleaned_row, 1):
            cell = ws.cell(idx, ci, value=val)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            
            if ci == 1:
                cell.alignment = ALIGN_DATA_TOP_CENTER
            else:
                cell.alignment = ALIGN_DATA_TOP_LEFT
                
    # Column Widths
    if sheet_type == 'GAGAL':
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 44  # Full OPD name fits without wrapping
        ws.column_dimensions['C'].width = 34  # Full Domain name fits
        ws.column_dimensions['D'].width = 52  # ID and data title
        ws.column_dimensions['E'].width = 75  # List of missing columns fits comfortably
    else:
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 44  # Full OPD name fits
        ws.column_dimensions['C'].width = 36  # Domain fits completely

# -------------------------------------------------------------
# 1. TAB: Ringkasan Eksekutif
# -------------------------------------------------------------
ws_exec = new_wb.create_sheet(title='Ringkasan Eksekutif')
ws_exec.views.sheetView[0].showGridLines = True
ws_exec.row_dimensions[1].height = 12

ws_exec.cell(2, 1, value="REKAPITULASI AUDIT KELENGKAPAN DOKUMEN ARSITEKTUR SPBE").font = FONT_SHEET_TITLE
ws_exec.row_dimensions[2].height = 26
ws_exec.cell(3, 1, value="Laporan Forensik Data Gagal Upload & Domain Kosong per Perangkat Daerah Pemprov DKI Jakarta").font = FONT_SUBTITLE
ws_exec.row_dimensions[3].height = 18

# Header Row
headers_exec = ["NO", "NAMA PERANGKAT DAERAH", "STATUS AUDIT LAPANGAN", "RINCIAN TEMUAN DATA GAGAL & DOMAIN KOSONG", "TAB REKAPITULASI TERKAIT"]
ws_exec.row_dimensions[5].height = 28
for ci, h in enumerate(headers_exec, 1):
    c = ws_exec.cell(5, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

opd_exec_data = [
    ("1.0", "Kota Administrasi Jakarta Selatan", "KRITIS (Template Kosong)", "39 baris ProsesBisnis_Upgrade & 21 baris Layanan_Upgrade kolom RAB/RAL kosong", "Data gagal Upload JAKSEL"),
    ("2.0", "Badan Perencanaan Pembangunan Daerah", "GAGAL SIMPAN (Server)", "10 unit server HP Proliant gagal simpan; 6 domain arsitektur belum diunggah", "Data gagal Upload BAPPEDA"),
    ("3.0", "Satuan Polisi Pamong Praja", "KOLOM MANDATORY KOSONG", "Layanan L13258, L12419, Data I2922 belum terisi rincian RAL L3, Potensi Risiko & Mitigasi", "Data gagal Upload SATPOL PP"),
    ("4.0", "Kota Administrasi Jakarta Timur", "KOLOM MANDATORY KOSONG", "Layanan L13349 (Kelurahan) belum terisi atribut RAL L3 & Risiko; 5 domain belum ada", "Data gagal Upload JAKTIM"),
    ("5.0", "Kota Administrasi Jakarta Utara", "7 DOMAIN BELUM ADA", "7 domain belum ada: ProsesBisnis Sesuai/Upgrade/Sunset, Layanan Sesuai/Upgrade/Sunset", "Data yg blm ada JAKUT"),
    ("6.0", "Kota Administrasi Jakarta Barat", "10 DOMAIN BELUM ADA", "10 domain belum ada (Sheet 5): ProsesBisnis, Layanan, Aplikasi, Data Informasi", "Data yg blm ada JAKBAR"),
    ("7.0", "Inspektorat Provinsi DKI Jakarta", "7 DOMAIN BELUM ADA", "7 domain belum ada: ProsesBisnis Upgrade/Sunset, Layanan Upgrade/Sunset, Aplikasi", "Data yg blm ada INSPEKTORAT")
]

for idx, row in enumerate(opd_exec_data, 6):
    ws_exec.row_dimensions[idx].height = 28
    is_zebra = (idx % 2 == 0)
    for ci, val in enumerate(row, 1):
        c = ws_exec.cell(idx, ci, value=val)
        c.font = FONT_BODY
        c.border = BORDER_CLEAN
        c.fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        if ci == 1:
            c.alignment = ALIGN_DATA_TOP_CENTER
        elif ci == 3:
            c.alignment = ALIGN_DATA_TOP_CENTER
            if "KRITIS" in val:
                c.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
            elif "GAGAL" in val:
                c.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
            else:
                c.fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
        else:
            c.alignment = ALIGN_DATA_TOP_LEFT

ws_exec.column_dimensions['A'].width = 8
ws_exec.column_dimensions['B'].width = 44
ws_exec.column_dimensions['C'].width = 28
ws_exec.column_dimensions['D'].width = 72
ws_exec.column_dimensions['E'].width = 32

# -------------------------------------------------------------
# 2. TAB: Data gagal Upload JAKSEL
# -------------------------------------------------------------
jaksel_fail = [
    (1.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB01 - Pengelolaan Administrasi Kependudukan Tingkat Kecamatan/Kelurahan", 
     "Domain\nKategori Arsitektur To-Be\nArsitektur As-Is Terkait\nPerangkat Daerah *\nReferensi Arsitektur Bisnis (RAB) Level 1 (Referensi Nasional) *\nReferensi Arsitektur Bisnis (RAB) Level 2 (Referensi Nasional) *\nReferensi Arsitektur Bisnis (RAB) Level 3 (Referensi Nasional) *"),
    (2.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB02 - Penyelenggaraan Ketenteraman dan Ketertiban Umum Wilayah", 
     "Domain\nKategori Arsitektur To-Be\nArsitektur As-Is Terkait\nPerangkat Daerah *\nReferensi Arsitektur Bisnis (RAB) Level 1 *\nReferensi Arsitektur Bisnis (RAB) Level 2 *\nReferensi Arsitektur Bisnis (RAB) Level 3 *"),
    (3.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB03 - Koordinasi Penanganan Banjir dan Genangan Air Jakarta Selatan", 
     "Domain\nKategori Arsitektur To-Be\nArsitektur As-Is Terkait\nPerangkat Daerah *\nReferensi Arsitektur Bisnis (RAB) Level 1 *\nReferensi Arsitektur Bisnis (RAB) Level 2 *\nReferensi Arsitektur Bisnis (RAB) Level 3 *"),
    (4.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB04 s/d PB39 (36 Entitas Proses Bisnis Kewilayahan Lainnya)", 
     "Seluruh baris template 03C belum terisi data pemetaan RAB Level 1 s/d Level 3"),
    (5.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade", "L01 - Layanan Pendaftaran Penduduk dan Pencatatan Sipil Daring", 
     "Domain\nKategori Arsitektur To-Be\nNama Layanan As-Is Terkait\nPerangkat Daerah *\nReferensi Arsitektur Layanan (RAL) Level 1 *\nReferensi Arsitektur Layanan (RAL) Level 2 *\nKanal Akses Layanan Terintegrasi *"),
    (6.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade", "L02 - Layanan Pengaduan Warga CRM Terintegrasi", 
     "Domain\nKategori Arsitektur To-Be\nNama Layanan As-Is Terkait\nPerangkat Daerah *\nReferensi Arsitektur Layanan (RAL) Level 1 *\nReferensi Arsitektur Layanan (RAL) Level 2 *\nKanal Akses Layanan Terintegrasi *"),
    (7.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade", "L03 s/d L21 (19 Entitas Layanan Publik & Administrasi)", 
     "Seluruh baris template 03C belum terisi data pemetaan RAL Level 1 s/d Level 2")
]
add_standard_audit_sheet(new_wb, "Data gagal Upload JAKSEL", "GAGAL", "Kota Administrasi Jakarta Selatan", jaksel_fail)

# -------------------------------------------------------------
# 3. TAB: Data yg blm ada JAKSEL
# -------------------------------------------------------------
jaksel_none = [
    (1.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade"),
    (2.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Sunset"),
    (3.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade"),
    (4.0, "Kota Administrasi Jakarta Selatan", "Layanan_Sunset"),
    (5.0, "Kota Administrasi Jakarta Selatan", "Aplikasi_Sunset"),
    (6.0, "Kota Administrasi Jakarta Selatan", "DataInformasi_Upgrade"),
    (7.0, "Kota Administrasi Jakarta Selatan", "DataInformasi_Sunset")
]
add_standard_audit_sheet(new_wb, "Data yg blm ada JAKSEL", "BELUM_ADA", "Kota Administrasi Jakarta Selatan", jaksel_none)

# -------------------------------------------------------------
# 4 - 13: EXTRACT & CLEAN DATA FROM REFERENCE WORKBOOK
# -------------------------------------------------------------
if ref_wb:
    sheet_configs = [
        ('Data gagal Upload bappeda ', 'Data gagal Upload BAPPEDA', 'GAGAL', 'Badan Perencanaan Pembangunan Daerah', 5),
        ('Data yang belum ada bappenda', 'Data yg blm ada BAPPEDA', 'BELUM_ADA', 'Badan Perencanaan Pembangunan Daerah', 5),
        ('Data gagal Upload Satuan Polisi', 'Data gagal Upload SATPOL PP', 'GAGAL', 'Satuan Polisi Pamong Praja', 7),
        (' Data yang belum ada  Polisi Pa', 'Data yg blm ada SATPOL PP', 'BELUM_ADA', 'Satuan Polisi Pamong Praja', 5),
        ('Data gagal Upload KOTA ADMINIST', 'Data gagal Upload JAKTIM', 'GAGAL', 'Kota Administrasi Jakarta Timur', 5),
        (' Data yang belum ada KOTA ADMIN', 'Data yg blm ada JAKTIM', 'BELUM_ADA', 'Kota Administrasi Jakarta Timur', 5),
        (' Data yang belum ada KOTA JAKAR', 'Data yg blm ada JAKUT', 'BELUM_ADA', 'Kota Administrasi Jakarta Utara', 5),
        ('Data yang belum ada KOTA JAKART', 'Data yg blm ada JAKUT 2', 'BELUM_ADA', 'Kota Administrasi Jakarta Utara', 5),
        ('Data yang belum ada Inspektorat', 'Data yg blm ada INSPEKTORAT', 'BELUM_ADA', 'Inspektorat', 5),
        ('Sheet5', 'Data yg blm ada JAKBAR', 'BELUM_ADA', 'Kota Administrasi Jakarta Barat', 5)
    ]
    
    for orig_name, new_title, s_type, opd_name, start_row in sheet_configs:
        if orig_name in ref_wb.sheetnames:
            ws_ref = ref_wb[orig_name]
            extracted_rows = []
            col_count = 5 if s_type == 'GAGAL' else 3
            for r in range(start_row, ws_ref.max_row + 1):
                r_vals = [ws_ref.cell(r, c).value for c in range(1, col_count + 1)]
                if any(r_vals) and str(r_vals[0] or '').strip():
                    # Clean trailing newlines from OPD name and ID
                    cleaned = []
                    for ci, v in enumerate(r_vals):
                        s_v = str(v or '').strip()
                        if ci == 0:
                            try:
                                s_v = f"{float(s_v):.1f}"
                            except:
                                pass
                        cleaned.append(s_v)
                    extracted_rows.append(cleaned)
                    
            add_standard_audit_sheet(new_wb, new_title, s_type, opd_name, extracted_rows)

# -------------------------------------------------------------
# 14 & 15: SOLUTION TABS (TERISI LENGKAP SIAP PAKAI)
# -------------------------------------------------------------
from generate_jaksel_spbe_spreadsheet import pb_headers, pb_rows, lay_headers, lay_rows

# Tab 39 Proses
ws_sol_pb = new_wb.create_sheet(title='39 ProsesBisnis (TERISI)')
ws_sol_pb.views.sheetView[0].showGridLines = True
ws_sol_pb.row_dimensions[1].height = 28

for col_idx, h_text in enumerate(pb_headers, 1):
    c = ws_sol_pb.cell(1, col_idx, value=h_text)
    c.font = FONT_HEADER
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER
    c.fill = PatternFill(start_color="D9E1F2" if col_idx <= 3 else "FEF08A", end_color="D9E1F2" if col_idx <= 3 else "FEF08A", fill_type="solid")

for r_idx, (asis_proc, rab_l1, rab_l2, rab_l3) in enumerate(pb_rows, 2):
    ws_sol_pb.row_dimensions[r_idx].height = 24
    is_zebra = (r_idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    vals = ["Proses Bisnis", "Upgrade", asis_proc, "Kota Administrasi Jakarta Selatan", rab_l1, rab_l2, rab_l3]
    for ci, v in enumerate(vals, 1):
        cell = ws_sol_pb.cell(r_idx, ci, value=v)
        cell.font = FONT_BODY
        cell.border = BORDER_CLEAN
        cell.fill = row_fill
        cell.alignment = ALIGN_DATA_TOP_CENTER if ci in [1, 2] else ALIGN_DATA_TOP_LEFT

ws_sol_pb.column_dimensions['A'].width = 16
ws_sol_pb.column_dimensions['B'].width = 24
ws_sol_pb.column_dimensions['C'].width = 50
ws_sol_pb.column_dimensions['D'].width = 40
ws_sol_pb.column_dimensions['E'].width = 28
ws_sol_pb.column_dimensions['F'].width = 36
ws_sol_pb.column_dimensions['G'].width = 48

# Tab 21 Layanan
ws_sol_lay = new_wb.create_sheet(title='21 Layanan (TERISI)')
ws_sol_lay.views.sheetView[0].showGridLines = True
ws_sol_lay.row_dimensions[1].height = 28

for col_idx, h_text in enumerate(lay_headers, 1):
    c = ws_sol_lay.cell(1, col_idx, value=h_text)
    c.font = FONT_HEADER
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER
    c.fill = PatternFill(start_color="D9E1F2" if col_idx <= 3 else "FEF08A", end_color="D9E1F2" if col_idx <= 3 else "FEF08A", fill_type="solid")

for r_idx, (lay_name, ral_l1, ral_l2, kanal) in enumerate(lay_rows, 2):
    ws_sol_lay.row_dimensions[r_idx].height = 24
    is_zebra = (r_idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    vals = ["Layanan", "Upgrade", lay_name, "Kota Administrasi Jakarta Selatan", ral_l1, ral_l2, kanal]
    for ci, v in enumerate(vals, 1):
        cell = ws_sol_lay.cell(r_idx, ci, value=v)
        cell.font = FONT_BODY
        cell.border = BORDER_CLEAN
        cell.fill = row_fill
        cell.alignment = ALIGN_DATA_TOP_CENTER if ci in [1, 2] else ALIGN_DATA_TOP_LEFT

ws_sol_lay.column_dimensions['A'].width = 16
ws_sol_lay.column_dimensions['B'].width = 24
ws_sol_lay.column_dimensions['C'].width = 50
ws_sol_lay.column_dimensions['D'].width = 40
ws_sol_lay.column_dimensions['E'].width = 36
ws_sol_lay.column_dimensions['F'].width = 36
ws_sol_lay.column_dimensions['G'].width = 44

# Save Master Workbook
new_wb.save(OUTPUT_MASTER)
shutil.copyfile(OUTPUT_MASTER, os.path.join(PUBLIC_DL_DIR, "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx"))
print(f"[MASTER POLISH SUCCESS] Saved to {OUTPUT_MASTER}")

# -------------------------------------------------------------
# POLISH 03C JAKARTA SELATAN TEMPLATE AS WELL
# -------------------------------------------------------------
if os.path.exists(OUTPUT_03C):
    wb_03c = openpyxl.load_workbook(OUTPUT_03C)
    for sname in wb_03c.sheetnames:
        ws = wb_03c[sname]
        ws.views.sheetView[0].showGridLines = True
        ws.row_dimensions[1].height = 28
        for c in range(1, ws.max_column + 1):
            ws.cell(1, c).font = FONT_HEADER
            ws.cell(1, c).alignment = ALIGN_HEADER
            ws.cell(1, c).border = BORDER_HEADER
            
        for r in range(2, ws.max_row + 1):
            ws.row_dimensions[r].height = 24
            is_zebra = (r % 2 == 0)
            row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
            for c in range(1, ws.max_column + 1):
                cell = ws.cell(r, c)
                cell.font = FONT_BODY
                cell.border = BORDER_CLEAN
                cell.fill = row_fill
                cell.alignment = ALIGN_DATA_TOP_CENTER if c in [1, 2] else ALIGN_DATA_TOP_LEFT
                
        # Set generous widths
        ws.column_dimensions['A'].width = 16
        ws.column_dimensions['B'].width = 24
        ws.column_dimensions['C'].width = 52
        ws.column_dimensions['D'].width = 42
        ws.column_dimensions['E'].width = 36
        ws.column_dimensions['F'].width = 36
        ws.column_dimensions['G'].width = 48
        
    wb_03c.save(OUTPUT_03C)
    shutil.copyfile(OUTPUT_03C, os.path.join(PUBLIC_DL_DIR, "03C_TOBE_ASIS_Kota_Administrasi_Jakarta_Selatan_TERISI.xlsx"))
    print(f"[03C POLISH SUCCESS] Saved to {OUTPUT_03C}")
