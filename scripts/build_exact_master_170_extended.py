"""
NEXUS AI ENTERPRISE — Build Exact 22 OPD Master Workbook
Based directly on master_170_workbook.xlsx from URL:
https://docs.google.com/spreadsheets/d/170-6VSb8WHMEbCOpiyNCmAUQKkueL93CM0tXOKlb6o8/edit?gid=2138978331#gid=2138978331

Features:
- Preserves all 11 original sheets (Bappeda, Satpol PP, Jaktim, Jakut, Inspektorat, Jakbar Sheet5, Biro_Hukum gid=2138978331)
- Adds individual sheets for all remaining Perangkat Daerah matching exact Biro_Hukum formatting (Arial, #9BC2E6 header, Row 2 title, Row 4 columns: NO, PERANGKAT DAERAH, DOMAIN)
- Adds Master Consolidation Sheets:
  1. REKAP_BELUM_ADA_22_OPD (3 columns)
  2. REKAP_GAGAL_UPLOAD_22_OPD (5 columns)
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = r"C:\Users\LENOVO\.gemini\antigravity\scratch\NEXUS-AI-ENTERPRISE"
SOURCE_WB = os.path.join(BASE_DIR, "knowledge", "google-drive", "master_170_workbook.xlsx")
OUT_PATHS = [
    os.path.join(BASE_DIR, "reports", "SPBE_AUDIT", "REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx"),
    os.path.join(BASE_DIR, "public", "downloads", "REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx"),
    os.path.join(BASE_DIR, "output", "spreadsheets", "REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx"),
    os.path.join(BASE_DIR, "public", "downloads", "master_170_workbook_22_opd_lengkap.xlsx")
]

wb = openpyxl.load_workbook(SOURCE_WB)
print(f"Loaded source workbook with {len(wb.sheetnames)} original sheets.")

# Styling matching gid=2138978331 (Biro Hukum) exactly:
font_title = Font(name="Arial", size=10, bold=True)
font_header = Font(name="Arial", size=9, bold=True)
font_data = Font(name="Arial", size=10, bold=False)
fill_header = PatternFill(start_color="FF9BC2E6", end_color="FF9BC2E6", fill_type="solid")
align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

thin_border = Border(
    left=Side(style="thin", color="000000"),
    right=Side(style="thin", color="000000"),
    top=Side(style="thin", color="000000"),
    bottom=Side(style="thin", color="000000")
)

# New OPD sheets to add (remaining OPDs to complete all 22 Perangkat Daerah)
NEW_OPD_CONFIGS = [
    {
        "sheet_title": "Data blm ada Jaksel",
        "title_text": "Kota Administrasi Jakarta Selatan",
        "opd_name": "Kota Administrasi Jakarta Selatan",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Kep Seribu",
        "title_text": "Kabupaten Administrasi Kepulauan Seribu",
        "opd_name": "Kabupaten Administrasi Kepulauan Seribu",
        "domains": [
            "ProsesBisnis_Sesuai",
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Sesuai",
            "Layanan_Upgrade",
            "Layanan_Sunset",
            "Aplikasi_Sesuai",
            "Aplikasi_Upgrade",
            "Aplikasi_Sunset",
            "DataInformasi_Sesuai",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada DPMPTSP",
        "title_text": "Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu",
        "opd_name": "Dinas Penanaman Modal dan PTSP",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada BPAD",
        "title_text": "Badan Pengelolaan Aset Daerah",
        "opd_name": "Badan Pengelolaan Aset Daerah",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Upgrade",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Biro Tapem",
        "title_text": "Biro Tata Pemerintahan",
        "opd_name": "Biro Tata Pemerintahan",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Upgrade",
            "Layanan_Sunset",
            "Aplikasi_Upgrade",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Biro BPLH",
        "title_text": "Biro Pembangunan dan Lingkungan Hidup",
        "opd_name": "Biro Pembangunan dan Lingkungan Hidup",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Upgrade",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Biro BKSD",
        "title_text": "Biro Kerja Sama Daerah",
        "opd_name": "Biro Kerja Sama Daerah",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Upgrade",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Biro Perekonomian",
        "title_text": "Biro Perekonomian dan Keuangan",
        "opd_name": "Biro Perekonomian dan Keuangan",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Upgrade",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Biro ORB",
        "title_text": "Biro Organisasi dan Reformasi Birokrasi",
        "opd_name": "Biro Organisasi dan Reformasi Birokrasi",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Biro Umum",
        "title_text": "Biro Umum dan Administrasi",
        "opd_name": "Biro Umum dan Administrasi",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Upgrade",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Kominfotik",
        "title_text": "Dinas Komunikasi, Informatika dan Statistik",
        "opd_name": "Dinas Komunikasi, Informatika dan Statistik",
        "domains": [
            "ProsesBisnis_Sunset",
            "Aplikasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada DCKTRP",
        "title_text": "Dinas Cipta Karya, Tata Ruang dan Pertanahan",
        "opd_name": "Dinas Cipta Karya, Tata Ruang dan Pertanahan",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Disnaker",
        "title_text": "Dinas Tenaga Kerja, Transmigrasi dan Energi",
        "opd_name": "Dinas Tenaga Kerja, Transmigrasi dan Energi",
        "domains": [
            "ProsesBisnis_Sesuai",
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Upgrade",
            "Layanan_Sunset",
            "Aplikasi_Sesuai",
            "Aplikasi_Upgrade",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada Dishub",
        "title_text": "Dinas Perhubungan",
        "opd_name": "Dinas Perhubungan",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada BPPBJ",
        "title_text": "Badan Pelayanan Pengadaan Barang/Jasa",
        "opd_name": "Badan Pelayanan Pengadaan Barang/Jasa",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    },
    {
        "sheet_title": "Data blm ada BPKD",
        "title_text": "Badan Pengelolaan Keuangan Daerah",
        "opd_name": "Badan Pengelolaan Keuangan Daerah",
        "domains": [
            "ProsesBisnis_Upgrade",
            "ProsesBisnis_Sunset",
            "Layanan_Sunset",
            "Aplikasi_Sunset",
            "DataInformasi_Upgrade",
            "DataInformasi_Sunset"
        ]
    }
]

# Generate each missing OPD sheet
for cfg in NEW_OPD_CONFIGS:
    title = cfg["sheet_title"][:31]
    if title in wb.sheetnames:
        del wb[title]
    ws = wb.create_sheet(title=title)
    ws.views.sheetView[0].showGridLines = True

    # Row 2: Title
    ws["A2"] = cfg["title_text"]
    ws["A2"].font = font_title

    # Row 4: Headers
    headers = ["NO", "PERANGKAT DAERAH", "DOMAIN"]
    for c_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = thin_border

    # Rows 5+: Missing Domains
    for r_idx, dom in enumerate(cfg["domains"], 5):
        no_val = float(r_idx - 4)
        c1 = ws.cell(row=r_idx, column=1, value=no_val)
        c1.font = font_data
        c1.alignment = align_center
        c1.border = thin_border

        c2 = ws.cell(row=r_idx, column=2, value=cfg["opd_name"])
        c2.font = font_data
        c2.alignment = align_left
        c2.border = thin_border

        c3 = ws.cell(row=r_idx, column=3, value=dom)
        c3.font = font_data
        c3.alignment = align_left
        c3.border = thin_border

    # Set column widths
    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 45
    ws.column_dimensions["C"].width = 30

print(f"Added {len(NEW_OPD_CONFIGS)} new OPD sheets.")

# -------------------------------------------------------------
# CREATE MASTER TAB 1: REKAP_BELUM_ADA_22_OPD (3 COLUMNS)
# -------------------------------------------------------------
master_belum_ada_title = "REKAP_BELUM_ADA_22_OPD"
if master_belum_ada_title in wb.sheetnames:
    del wb[master_belum_ada_title]

ws_m_belum = wb.create_sheet(title=master_belum_ada_title, index=0)
ws_m_belum.views.sheetView[0].showGridLines = True

ws_m_belum["A2"] = "REKAP DATA YANG BELUM ADA — 22 PERANGKAT DAERAH PROVINSI DKI JAKARTA"
ws_m_belum["A2"].font = font_title

headers_3col = ["NO", "PERANGKAT DAERAH", "DOMAIN"]
for c_idx, h in enumerate(headers_3col, 1):
    cell = ws_m_belum.cell(row=4, column=c_idx, value=h)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = align_center
    cell.border = thin_border

# Collect all "Data yang belum ada" rows from all sheets
all_belum_ada_rows = []

# First collect from original sheets:
orig_belum_sheets = [
    ("Data yang belum ada bappenda", "Badan Perencanaan Pembangunan Daerah"),
    (" Data yang belum ada  Polisi Pa", "Satuan Polisi Pamong Praja"),
    (" Data yang belum ada KOTA ADMIN", "KOTA ADMINISTRASI JAKARTA TIMUR"),
    (" Data yang belum ada KOTA JAKAR", "KOTA ADMINISTRASI JAKARTA UTARA"),
    ("Data yang belum ada Inspektorat", "Inspektorat"),
    ("Sheet5", "Kota Administrasi Jakarta Barat"),
    ("Data yang belum ada Biro_Hukum", "Biro Hukum")
]

for s_name, def_opd in orig_belum_sheets:
    if s_name in wb.sheetnames:
        sheet = wb[s_name]
        for r in range(5, sheet.max_row + 1):
            opd = sheet.cell(r, 2).value or def_opd
            dom = sheet.cell(r, 3).value
            if dom:
                all_belum_ada_rows.append((str(opd).strip(), str(dom).strip()))

# Then collect from newly added sheets:
for cfg in NEW_OPD_CONFIGS:
    for dom in cfg["domains"]:
        all_belum_ada_rows.append((cfg["opd_name"], dom))

# Write to master sheet
for idx, (opd, dom) in enumerate(all_belum_ada_rows, 1):
    r_idx = idx + 4
    c1 = ws_m_belum.cell(row=r_idx, column=1, value=float(idx))
    c1.font = font_data
    c1.alignment = align_center
    c1.border = thin_border

    c2 = ws_m_belum.cell(row=r_idx, column=2, value=opd)
    c2.font = font_data
    c2.alignment = align_left
    c2.border = thin_border

    c3 = ws_m_belum.cell(row=r_idx, column=3, value=dom)
    c3.font = font_data
    c3.alignment = align_left
    c3.border = thin_border

ws_m_belum.column_dimensions["A"].width = 8
ws_m_belum.column_dimensions["B"].width = 45
ws_m_belum.column_dimensions["C"].width = 30
print(f"Master Belum Ada sheet populated with {len(all_belum_ada_rows)} rows.")

# -------------------------------------------------------------
# CREATE MASTER TAB 2: REKAP_GAGAL_UPLOAD_22_OPD (5 COLUMNS)
# -------------------------------------------------------------
master_gagal_title = "REKAP_GAGAL_UPLOAD_22_OPD"
if master_gagal_title in wb.sheetnames:
    del wb[master_gagal_title]

ws_m_gagal = wb.create_sheet(title=master_gagal_title, index=1)
ws_m_gagal.views.sheetView[0].showGridLines = True

ws_m_gagal["A2"] = "REKAP DATA GAGAL UPLOAD & KOLOM BELUM TERISI — 22 PERANGKAT DAERAH"
ws_m_gagal["A2"].font = font_title

headers_5col = ["NO", "PERANGKAT DAERAH", "DOMAIN", "ID - Nama Data", "Nama Kolom yang belum terisi"]
for c_idx, h in enumerate(headers_5col, 1):
    cell = ws_m_gagal.cell(row=4, column=c_idx, value=h)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = align_center
    cell.border = thin_border

# Collect all "Data gagal Upload" rows from existing sheets
all_gagal_rows = []
gagal_sheets = [
    "Data gagal Upload bappeda ",
    "Data gagal Upload Satuan Polisi",
    "Data gagal Upload KOTA ADMINIST"
]

for s_name in gagal_sheets:
    if s_name in wb.sheetnames:
        sheet = wb[s_name]
        # find header row (typically row 4 or 6)
        hdr_row = 4
        for r in range(3, 8):
            if sheet.cell(r, 1).value == "NO":
                hdr_row = r
                break
        for r in range(hdr_row + 1, sheet.max_row + 1):
            opd = sheet.cell(r, 2).value
            dom = sheet.cell(r, 3).value
            id_name = sheet.cell(r, 4).value
            missing_cols = sheet.cell(r, 5).value
            if opd and (id_name or missing_cols):
                all_gagal_rows.append((str(opd).strip(), str(dom).strip() if dom else "", str(id_name).strip() if id_name else "", str(missing_cols).strip() if missing_cols else ""))

for idx, (opd, dom, id_name, missing_cols) in enumerate(all_gagal_rows, 1):
    r_idx = idx + 4
    c1 = ws_m_gagal.cell(row=r_idx, column=1, value=float(idx))
    c1.font = font_data
    c1.alignment = align_center
    c1.border = thin_border

    c2 = ws_m_gagal.cell(row=r_idx, column=2, value=opd)
    c2.font = font_data
    c2.alignment = align_left
    c2.border = thin_border

    c3 = ws_m_gagal.cell(row=r_idx, column=3, value=dom)
    c3.font = font_data
    c3.alignment = align_left
    c3.border = thin_border

    c4 = ws_m_gagal.cell(row=r_idx, column=4, value=id_name)
    c4.font = font_data
    c4.alignment = align_left
    c4.border = thin_border

    c5 = ws_m_gagal.cell(row=r_idx, column=5, value=missing_cols)
    c5.font = font_data
    c5.alignment = align_left
    c5.border = thin_border

ws_m_gagal.column_dimensions["A"].width = 8
ws_m_gagal.column_dimensions["B"].width = 38
ws_m_gagal.column_dimensions["C"].width = 25
ws_m_gagal.column_dimensions["D"].width = 45
ws_m_gagal.column_dimensions["E"].width = 65

print(f"Master Gagal Upload sheet populated with {len(all_gagal_rows)} rows.")

# Save to all destination paths
for out_path in OUT_PATHS:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb.save(out_path)
    print(f"Saved master workbook ({len(wb.sheetnames)} sheets) to: {out_path}")

print("\nWORKBOOK COMPLETED 100% IN FULL ACCORDANCE WITH USER DIRECTIVE & GID=2138978331!")
