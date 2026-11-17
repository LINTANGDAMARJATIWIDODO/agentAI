"""
NEXUS AI ENTERPRISE — MASTER DETAILED SPBE AUDIT SPREADSHEET GENERATOR
Adopts the EXACT standard of Diskominfotik / SPBE CBC DKI Jakarta
Source Reference: https://docs.google.com/spreadsheets/d/170-6VSb8WHMEbCOpiyNCmAUQKkueL93CM0tXOKlb6o8

Structure:
1. Ringkasan Eksekutif & Dashboard
2. Data gagal Upload JAKSEL (39 Proses Bisnis & 21 Layanan Kolom Kosong)
3. Data yang belum ada JAKSEL (Domain-domain yang belum ada)
4. Data gagal Upload bappeda (From Reference)
5. Data yang belum ada bappenda (From Reference)
6. Data gagal Upload Satuan Polisi (From Reference)
7. Data yang belum ada Polisi Pamong Praja (From Reference)
8. Data gagal Upload KOTA ADMINIST (Jakarta Timur - From Reference)
9. Data yang belum ada KOTA ADMIN (Jakarta Timur - From Reference)
10. Data yang belum ada KOTA JAKARTA UTARA (From Reference)
11. Data yang belum ada Inspektorat (From Reference)
12. Data yang belum ada JAKARTA BARAT (From Reference)
13. 39 ProsesBisnis_Upgrade (SOLUSI TERISI SIAP PAKAI)
14. 21 Layanan_Upgrade (SOLUSI TERISI SIAP PAKAI)
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_FILE = os.path.join(BASE_DIR, "knowledge", "google-drive", "reference_report_template.xlsx")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "spreadsheets")
PUBLIC_DL_DIR = os.path.join(BASE_DIR, "public", "downloads")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PUBLIC_DL_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx")

# Official Pastel Blue Header Fill matching reference
PASTEL_BLUE_FILL = PatternFill(start_color="9BC2E6", end_color="9BC2E6", fill_type="solid")
DARK_NAVY_FILL = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
GREEN_ACCENT = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
YELLOW_ACCENT = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
RED_ACCENT = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")

TITLE_FONT = Font(name="Arial", size=13, bold=True, color="000000")
HEADER_FONT = Font(name="Arial", size=9, bold=True, color="000000")
BODY_FONT = Font(name="Arial", size=9, color="000000")
BOLD_BODY_FONT = Font(name="Arial", size=9, bold=True, color="000000")
WHITE_BOLD_FONT = Font(name="Arial", size=11, bold=True, color="FFFFFF")

THIN_BORDER = Border(
    left=Side(style='thin', color='BFBFBF'),
    right=Side(style='thin', color='BFBFBF'),
    top=Side(style='thin', color='BFBFBF'),
    bottom=Side(style='thin', color='BFBFBF')
)

ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

# 1. Load Reference Workbook if available, or create new
if os.path.exists(REF_FILE):
    wb = openpyxl.load_workbook(REF_FILE)
else:
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

# Ensure sheets in reference are nicely named
rename_map = {
    'Data gagal Upload bappeda ': 'Data gagal Upload BAPPEDA',
    'Data yang belum ada bappenda': 'Data yg blm ada BAPPEDA',
    'Data gagal Upload Satuan Polisi': 'Data gagal Upload SATPOL PP',
    ' Data yang belum ada  Polisi Pa': 'Data yg blm ada SATPOL PP',
    'Data gagal Upload KOTA ADMINIST': 'Data gagal Upload JAKTIM',
    ' Data yang belum ada KOTA ADMIN': 'Data yg blm ada JAKTIM',
    ' Data yang belum ada KOTA JAKAR': 'Data yg blm ada JAKUT',
    'Data yang belum ada KOTA JAKART': 'Data yg blm ada JAKUT 2',
    'Data yang belum ada Inspektorat': 'Data yg blm ada INSPEKTORAT',
    'Sheet5': 'Data yg blm ada JAKBAR'
}
for sname in list(wb.sheetnames):
    if sname in rename_map:
        wb[sname].title = rename_map[sname]

# -------------------------------------------------------------
# CREATE / PREPEND: TAB 1: Ringkasan Eksekutif
# -------------------------------------------------------------
if 'Ringkasan Eksekutif' in wb.sheetnames:
    del wb['Ringkasan Eksekutif']
ws_exec = wb.create_sheet(title='Ringkasan Eksekutif', index=0)
ws_exec.views.sheetView[0].showGridLines = True

ws_exec.merge_cells("A1:G1")
ws_exec["A1"] = "REKAPITULASI LAPORAN DATA GAGAL UPLOAD & DATA YANG BELUM ADA"
ws_exec["A1"].font = TITLE_FONT
ws_exec["A1"].alignment = ALIGN_CENTER
ws_exec.row_dimensions[1].height = 28

ws_exec.merge_cells("A2:G2")
ws_exec["A2"] = "Pemerintah Provinsi DKI Jakarta — Arsitektur & Peta Rencana SPBE Terintegrasi"
ws_exec["A2"].font = Font(name="Arial", size=10, italic=True, color="555555")
ws_exec["A2"].alignment = ALIGN_CENTER
ws_exec.row_dimensions[2].height = 20

# KPI Box
kpis = [
    ("A4:B5", "53 OPD / BIRO", "Total Perangkat Daerah Diperiksa", PASTEL_BLUE_FILL),
    ("C4:C5", "5 OPD (9.4%)", "Dokumen Lengkap 100%", GREEN_ACCENT),
    ("D4:D5", "48 OPD (90.6%)", "Ada Data Gagal / Belum Lengkap", RED_ACCENT),
    ("E4:E5", "JAKARTA SELATAN", "39 Proses & 21 Layanan Kosong", RED_ACCENT),
    ("F4:G5", "STANDAR CBC", "Format Rekap Detail Kolom Belum Terisi", PASTEL_BLUE_FILL)
]
for crange, val1, val2, fill_c in kpis:
    s_cell = crange.split(":")[0]
    ws_exec.merge_cells(crange)
    ws_exec[s_cell] = f"{val1}\n{val2}"
    ws_exec[s_cell].font = BOLD_BODY_FONT
    ws_exec[s_cell].fill = fill_c
    ws_exec[s_cell].alignment = ALIGN_CENTER

ws_exec.row_dimensions[4].height = 24
ws_exec.row_dimensions[5].height = 24

# Daftar Sheet Granular
ws_exec["A7"] = "NO"
ws_exec["B7"] = "NAMA PERANGKAT DAERAH"
ws_exec["C7"] = "STATUS AUDIT LAPANGAN"
ws_exec.merge_cells("D7:F7")
ws_exec["D7"] = "RINCIAN DATA GAGAL UPLOAD / DOMAIN BELUM ADA"
ws_exec["G7"] = "TAB SPREADSHEET TERKAIT"

for c in ["A", "B", "C", "D", "E", "F", "G"]:
    cell = ws_exec[f"{c}7"]
    cell.font = HEADER_FONT
    cell.fill = PASTEL_BLUE_FILL
    cell.alignment = ALIGN_CENTER
    cell.border = THIN_BORDER
ws_exec.row_dimensions[7].height = 24

opd_summaries = [
    ("1.0", "Kota Administrasi Jakarta Selatan", "KRITIS (Template Kosong)", "39 baris ProsesBisnis_Upgrade & 21 baris Layanan_Upgrade seluruh kolom RAB/RAL kosong", "Data gagal Upload JAKSEL"),
    ("2.0", "Badan Perencanaan Pembangunan Daerah (Bappeda)", "GAGAL SIMPAN", "10 entitas Server HP Proliant gagal simpan; 6 domain arsitektur belum ada", "Data gagal Upload BAPPEDA"),
    ("3.0", "Satuan Polisi Pamong Praja (Satpol PP)", "KOLOM KOSONG", "Layanan L13258, L12419, Data I2922 belum terisi rincian RAL L3, Potensi Risiko & Mitigasi", "Data gagal Upload SATPOL PP"),
    ("4.0", "Kota Administrasi Jakarta Timur", "KOLOM KOSONG", "Layanan L13349, L13344 belum terisi RAL L3, Potensi Risiko; 5 domain belum ada", "Data gagal Upload JAKTIM"),
    ("5.0", "Kota Administrasi Jakarta Utara", "DOMAIN BELUM ADA", "7 domain belum ada: ProsesBisnis Sesuai/Upgrade/Sunset, Layanan Sesuai/Upgrade/Sunset", "Data yg blm ada JAKUT"),
    ("6.0", "Kota Administrasi Jakarta Barat", "DOMAIN BELUM ADA", "10 domain belum ada (Sheet 5): ProsesBisnis, Layanan, Aplikasi, Data Informasi", "Data yg blm ada JAKBAR"),
    ("7.0", "Inspektorat Provinsi DKI Jakarta", "DOMAIN BELUM ADA", "7 domain belum ada: ProsesBisnis Upgrade/Sunset, Layanan Upgrade/Sunset, Aplikasi", "Data yg blm ada INSPEKTORAT")
]

for r_i, (no, opd, stat, rinc, tab_link) in enumerate(opd_summaries, 8):
    ws_exec[f"A{r_i}"] = no
    ws_exec[f"B{r_i}"] = opd
    ws_exec[f"C{r_i}"] = stat
    ws_exec.merge_cells(f"D{r_i}:F{r_i}")
    ws_exec[f"D{r_i}"] = rinc
    ws_exec[f"G{r_i}"] = tab_link
    
    ws_exec[f"A{r_i}"].alignment = ALIGN_CENTER
    ws_exec[f"B{r_i}"].alignment = ALIGN_LEFT
    ws_exec[f"C{r_i}"].alignment = ALIGN_CENTER
    ws_exec[f"D{r_i}"].alignment = ALIGN_LEFT
    ws_exec[f"G{r_i}"].alignment = ALIGN_CENTER
    
    if "KRITIS" in stat:
        ws_exec[f"C{r_i}"].fill = RED_ACCENT
    elif "GAGAL" in stat:
        ws_exec[f"C{r_i}"].fill = YELLOW_ACCENT
    else:
        ws_exec[f"C{r_i}"].fill = PASTEL_BLUE_FILL
        
    for c in ["A", "B", "C", "D", "E", "F", "G"]:
        ws_exec[f"{c}{r_i}"].border = THIN_BORDER
        if c != "C":
            ws_exec[f"{c}{r_i}"].font = BODY_FONT
    ws_exec.row_dimensions[r_i].height = 30

ws_exec.column_dimensions["A"].width = 6
ws_exec.column_dimensions["B"].width = 38
ws_exec.column_dimensions["C"].width = 24
ws_exec.column_dimensions["D"].width = 30
ws_exec.column_dimensions["E"].width = 30
ws_exec.column_dimensions["F"].width = 30
ws_exec.column_dimensions["G"].width = 28


# -------------------------------------------------------------
# TAB: Data gagal Upload JAKSEL (Format Detail Sesuai Referensi)
# -------------------------------------------------------------
if 'Data gagal Upload JAKSEL' in wb.sheetnames:
    del wb['Data gagal Upload JAKSEL']
ws_js_fail = wb.create_sheet(title='Data gagal Upload JAKSEL', index=1)
ws_js_fail.views.sheetView[0].showGridLines = True

ws_js_fail["A2"] = "Data gagal Upload Kota Administrasi Jakarta Selatan"
ws_js_fail["A2"].font = TITLE_FONT

headers_fail = ["NO", "PERANGKAT DAERAH", "DOMAIN", "ID - Nama Data", "Nama Kolom yang belum terisi"]
for ci, h_txt in enumerate(headers_fail, 1):
    c = ws_js_fail.cell(row=4, column=ci, value=h_txt)
    c.font = HEADER_FONT
    c.fill = PASTEL_BLUE_FILL
    c.alignment = ALIGN_CENTER
    c.border = THIN_BORDER
ws_js_fail.row_dimensions[4].height = 24

missing_cols_pb = (
    "Domain\n"
    "Kategori Arsitektur To-Be\n"
    "Arsitektur As-Is Terkait\n"
    "Perangkat Daerah *\n"
    "Referensi Arsitektur Bisnis (RAB) Level 1 (Referensi Nasional) *\n"
    "Referensi Arsitektur Bisnis (RAB) Level 2 (Referensi Nasional) *\n"
    "Referensi Arsitektur Bisnis (RAB) Level 3 (Referensi Nasional) *"
)

missing_cols_lay = (
    "Domain\n"
    "Kategori Arsitektur To-Be\n"
    "Nama Layanan As-Is Terkait\n"
    "Perangkat Daerah *\n"
    "Referensi Arsitektur Layanan (RAL) Level 1 *\n"
    "Referensi Arsitektur Layanan (RAL) Level 2 *\n"
    "Kanal Akses Layanan Terintegrasi *"
)

jaksel_fail_rows = [
    (1.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB01 - Pengelolaan Administrasi Kependudukan Tingkat Kecamatan/Kelurahan", missing_cols_pb),
    (2.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB02 - Penyelenggaraan Ketenteraman dan Ketertiban Umum Wilayah", missing_cols_pb),
    (3.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB03 - Koordinasi Penanganan Banjir dan Genangan Air Jakarta Selatan", missing_cols_pb),
    (4.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB04 - Penanganan Pengaduan Masyarakat CRM / Cepat Respon Masyarakat", missing_cols_pb),
    (5.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB05 - Penyelenggaraan Musrenbang Tingkat Kelurahan & Kecamatan", missing_cols_pb),
    (6.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB06 s/d PB39 (34 Proses Bisnis Kewilayahan Lainnya)", "Seluruh baris template 03C belum terisi (Blank Cells)"),
    (7.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade", "L01 - Layanan Pendaftaran Penduduk dan Pencatatan Sipil Daring", missing_cols_lay),
    (8.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade", "L02 - Layanan Pengaduan Warga CRM Terintegrasi", missing_cols_lay),
    (9.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade", "L03 - Layanan Perizinan dan Non-Perizinan PTSP Kecamatan", missing_cols_lay),
    (10.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade", "L04 s/d L21 (18 Layanan Publik dan Administrasi Lainnya)", "Seluruh baris template 03C belum terisi (Blank Cells)")
]

for r_i, (no, opd, dom, id_name, unk) in enumerate(jaksel_fail_rows, 5):
    ws_js_fail.cell(row=r_i, column=1, value=no).alignment = ALIGN_CENTER
    ws_js_fail.cell(row=r_i, column=2, value=opd).alignment = ALIGN_LEFT
    ws_js_fail.cell(row=r_i, column=3, value=dom).alignment = ALIGN_LEFT
    ws_js_fail.cell(row=r_i, column=4, value=id_name).alignment = ALIGN_LEFT
    ws_js_fail.cell(row=r_i, column=5, value=unk).alignment = ALIGN_LEFT
    
    for c in range(1, 6):
        cell = ws_js_fail.cell(row=r_i, column=c)
        cell.font = BODY_FONT
        cell.border = THIN_BORDER
    ws_js_fail.row_dimensions[r_i].height = 48 if "\n" in unk else 24

ws_js_fail.column_dimensions["A"].width = 8
ws_js_fail.column_dimensions["B"].width = 38
ws_js_fail.column_dimensions["C"].width = 24
ws_js_fail.column_dimensions["D"].width = 46
ws_js_fail.column_dimensions["E"].width = 54


# -------------------------------------------------------------
# TAB: Data yg blm ada JAKSEL
# -------------------------------------------------------------
if 'Data yg blm ada JAKSEL' in wb.sheetnames:
    del wb['Data yg blm ada JAKSEL']
ws_js_none = wb.create_sheet(title='Data yg blm ada JAKSEL', index=2)
ws_js_none.views.sheetView[0].showGridLines = True

ws_js_none["A2"] = "Kota Administrasi Jakarta Selatan"
ws_js_none["A2"].font = TITLE_FONT

for ci, h_txt in enumerate(["NO", "PERANGKAT DAERAH", "DOMAIN"], 1):
    c = ws_js_none.cell(row=4, column=ci, value=h_txt)
    c.font = HEADER_FONT
    c.fill = PASTEL_BLUE_FILL
    c.alignment = ALIGN_CENTER
    c.border = THIN_BORDER
ws_js_none.row_dimensions[4].height = 24

jaksel_missing_domains = [
    "ProsesBisnis_Upgrade",
    "ProsesBisnis_Sunset",
    "Layanan_Upgrade",
    "Layanan_Sunset",
    "Aplikasi_Sunset",
    "DataInformasi_Upgrade",
    "DataInformasi_Sunset"
]
for r_i, dom in enumerate(jaksel_missing_domains, 5):
    ws_js_none.cell(row=r_i, column=1, value=float(r_i - 4)).alignment = ALIGN_CENTER
    ws_js_none.cell(row=r_i, column=2, value="Kota Administrasi Jakarta Selatan").alignment = ALIGN_LEFT
    ws_js_none.cell(row=r_i, column=3, value=dom).alignment = ALIGN_LEFT
    for c in range(1, 4):
        cell = ws_js_none.cell(row=r_i, column=c)
        cell.font = BODY_FONT
        cell.border = THIN_BORDER
    ws_js_none.row_dimensions[r_i].height = 22

ws_js_none.column_dimensions["A"].width = 8
ws_js_none.column_dimensions["B"].width = 38
ws_js_none.column_dimensions["C"].width = 28


# -------------------------------------------------------------
# TABS SOLUSI: 39 ProsesBisnis_Upgrade (TERISI) & 21 Layanan_Upgrade (TERISI)
# -------------------------------------------------------------
from generate_jaksel_spbe_spreadsheet import pb_headers, pb_rows, lay_headers, lay_rows

# Tab 39 Proses Terisi
if '39 ProsesBisnis (TERISI)' in wb.sheetnames:
    del wb['39 ProsesBisnis (TERISI)']
ws_sol_pb = wb.create_sheet(title='39 ProsesBisnis (TERISI)')
ws_sol_pb.views.sheetView[0].showGridLines = True

for col_idx, h_text in enumerate(pb_headers, 1):
    c = ws_sol_pb.cell(row=1, column=col_idx, value=h_text)
    c.font = HEADER_FONT
    c.alignment = ALIGN_CENTER
    c.border = THIN_BORDER
    c.fill = PatternFill(start_color="D9E1F2" if col_idx <= 3 else "FFFF00", end_color="D9E1F2" if col_idx <= 3 else "FFFF00", fill_type="solid")
ws_sol_pb.row_dimensions[1].height = 28

for row_idx, (asis_proc, rab_l1, rab_l2, rab_l3) in enumerate(pb_rows, 2):
    ws_sol_pb.cell(row=row_idx, column=1, value="Proses Bisnis").alignment = ALIGN_CENTER
    ws_sol_pb.cell(row=row_idx, column=2, value="Upgrade").alignment = ALIGN_CENTER
    ws_sol_pb.cell(row=row_idx, column=3, value=asis_proc).alignment = ALIGN_LEFT
    ws_sol_pb.cell(row=row_idx, column=4, value="Kota Administrasi Jakarta Selatan").alignment = ALIGN_LEFT
    ws_sol_pb.cell(row=row_idx, column=5, value=rab_l1).alignment = ALIGN_LEFT
    ws_sol_pb.cell(row=row_idx, column=6, value=rab_l2).alignment = ALIGN_LEFT
    ws_sol_pb.cell(row=row_idx, column=7, value=rab_l3).alignment = ALIGN_LEFT
    for c in range(1, 8):
        ws_sol_pb.cell(row=row_idx, column=c).font = BODY_FONT
        ws_sol_pb.cell(row=row_idx, column=c).border = THIN_BORDER
    ws_sol_pb.row_dimensions[row_idx].height = 22

for col in ws_sol_pb.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws_sol_pb.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 48)

# Tab 21 Layanan Terisi
if '21 Layanan (TERISI)' in wb.sheetnames:
    del wb['21 Layanan (TERISI)']
ws_sol_lay = wb.create_sheet(title='21 Layanan (TERISI)')
ws_sol_lay.views.sheetView[0].showGridLines = True

for col_idx, h_text in enumerate(lay_headers, 1):
    c = ws_sol_lay.cell(row=1, column=col_idx, value=h_text)
    c.font = HEADER_FONT
    c.alignment = ALIGN_CENTER
    c.border = THIN_BORDER
    c.fill = PatternFill(start_color="D9E1F2" if col_idx <= 3 else "FFFF00", end_color="D9E1F2" if col_idx <= 3 else "FFFF00", fill_type="solid")
ws_sol_lay.row_dimensions[1].height = 28

for row_idx, (lay_name, ral_l1, ral_l2, kanal) in enumerate(lay_rows, 2):
    ws_sol_lay.cell(row=row_idx, column=1, value="Layanan").alignment = ALIGN_CENTER
    ws_sol_lay.cell(row=row_idx, column=2, value="Upgrade").alignment = ALIGN_CENTER
    ws_sol_lay.cell(row=row_idx, column=3, value=lay_name).alignment = ALIGN_LEFT
    ws_sol_lay.cell(row=row_idx, column=4, value="Kota Administrasi Jakarta Selatan").alignment = ALIGN_LEFT
    ws_sol_lay.cell(row=row_idx, column=5, value=ral_l1).alignment = ALIGN_LEFT
    ws_sol_lay.cell(row=row_idx, column=6, value=ral_l2).alignment = ALIGN_LEFT
    ws_sol_lay.cell(row=row_idx, column=7, value=kanal).alignment = ALIGN_LEFT
    for c in range(1, 8):
        ws_sol_lay.cell(row=row_idx, column=c).font = BODY_FONT
        ws_sol_lay.cell(row=row_idx, column=c).border = THIN_BORDER
    ws_sol_lay.row_dimensions[row_idx].height = 22

for col in ws_sol_lay.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws_sol_lay.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 48)

# Save to output and public/downloads
wb.save(OUTPUT_FILE)
wb.save(os.path.join(PUBLIC_DL_DIR, "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx"))

print(f"[SUCCESS] Berkas laporan rinci berhasil dibuat di: {OUTPUT_FILE}")
print(f"Total Sheet: {len(wb.sheetnames)} -> {wb.sheetnames}")
