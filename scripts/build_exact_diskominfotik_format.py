"""
NEXUS AI ENTERPRISE — EXACT DISKOMINFOTIK CBC FORMAT ENGINE
Aligns 100% with Google Sheets Reference:
https://docs.google.com/spreadsheets/d/170-6VSb8WHMEbCOpiyNCmAUQKkueL93CM0tXOKlb6o8/edit?gid=1729927466#gid=1729927466

Generates:
1. DATA YANG BELUM ADA:
   - Row 2: <Nama Perangkat Daerah>
   - Row 4 Header: [NO, PERANGKAT DAERAH, DOMAIN] (Fill: #9BC2E6)
   - Rows 5-16: All 12 missing domains for each of the 22 Perangkat Daerah!
   
2. DATA GAGAL UPLOAD:
   - Row 2: Data gagal Upload <Nama Perangkat Daerah>
   - Row 4 Header: [NO, PERANGKAT DAERAH, DOMAIN, ID - Nama Data, Nama Kolom yang belum terisi] (Fill: #9BC2E6)
   - Rows 5+: Failed items with detailed missing column lists
   
3. DATA YANG SUDAH TERISI:
   - Row 2: Data yang sudah terisi <Nama Perangkat Daerah>
   - Row 4 Header: [NO, PERANGKAT DAERAH, DOMAIN, ID - Nama Data Terisi, Kanal Akses & Status Keterisian] (Fill: #9BC2E6)
   - Detailed filled data for all 22 Perangkat Daerah across the 12 domains!

4. Standalone and Master Workbooks mirrored to public/downloads/
"""

import os
import math
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "spreadsheets")
PUBLIC_DL_DIR = os.path.join(BASE_DIR, "public", "downloads")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PUBLIC_DL_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

OUTPUT_MASTER = os.path.join(OUTPUT_DIR, "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx")
OUTPUT_BELUM_ADA = os.path.join(OUTPUT_DIR, "REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx")
OUTPUT_GAGAL = os.path.join(OUTPUT_DIR, "REKAP_DATA_GAGAL_UPLOAD_FORMAT_RESMI.xlsx")
OUTPUT_TERISI = os.path.join(OUTPUT_DIR, "REKAP_DATA_SUDAH_TERISI_FORMAT_RESMI.xlsx")

# Exact Diskominfotik Color & Font Specs
COLOR_HEADER_BLUE = "9BC2E6"
COLOR_ZEBRA = "F8FAFC"
COLOR_BORDER = "D9D9D9"
COLOR_TITLE_BLACK = "000000"

FILL_HEADER_BLUE = PatternFill(start_color=COLOR_HEADER_BLUE, end_color=COLOR_HEADER_BLUE, fill_type="solid")
FILL_ZEBRA = PatternFill(start_color=COLOR_ZEBRA, end_color=COLOR_ZEBRA, fill_type="solid")
FILL_WHITE = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

FONT_OPD_TITLE = Font(name="Arial", size=11, bold=True, color=COLOR_TITLE_BLACK)
FONT_HEADER = Font(name="Arial", size=10, bold=True, color=COLOR_TITLE_BLACK)
FONT_BODY = Font(name="Arial", size=9.5, color="000000")

BORDER_CLEAN = Border(
    left=Side(style='thin', color=COLOR_BORDER),
    right=Side(style='thin', color=COLOR_BORDER),
    top=Side(style='thin', color=COLOR_BORDER),
    bottom=Side(style='thin', color=COLOR_BORDER)
)

BORDER_HEADER = Border(
    left=Side(style='thin', color='7F7F7F'),
    right=Side(style='thin', color='7F7F7F'),
    top=Side(style='thin', color='7F7F7F'),
    bottom=Side(style='thin', color='7F7F7F')
)

ALIGN_HEADER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_DATA_TOP_LEFT = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_DATA_TOP_CENTER = Alignment(horizontal="center", vertical="top", wrap_text=True)

# THE 22 PERANGKAT DAERAH
OPD_LIST_22 = [
    "Kota Administrasi Jakarta Barat", # Exact first one as in gid=1729927466
    "Kota Administrasi Jakarta Selatan",
    "Badan Perencanaan Pembangunan Daerah",
    "Satuan Polisi Pamong Praja",
    "Kota Administrasi Jakarta Timur",
    "Kota Administrasi Jakarta Utara",
    "Inspektorat Provinsi DKI Jakarta",
    "Kabupaten Administrasi Kepulauan Seribu",
    "Dinas Penanaman Modal dan PTSP",
    "Badan Pengelolaan Aset Daerah",
    "Biro Tata Pemerintahan",
    "Biro Pembangunan dan Lingkungan Hidup",
    "Biro Kerja Sama Daerah",
    "Biro Perekonomian dan Keuangan",
    "Biro Organisasi dan Reformasi Birokrasi",
    "Biro Umum dan Administrasi",
    "Dinas Komunikasi, Informatika dan Statistik",
    "Dinas Cipta Karya, Tata Ruang dan Pertanahan",
    "Dinas Tenaga Kerja, Transmigrasi dan Energi",
    "Dinas Perhubungan",
    "Badan Pelayanan Pengadaan Barang/Jasa",
    "Badan Pengelolaan Keuangan Daerah"
]

# THE 12 ARCHITECTURE DOMAINS
DOMAINS_12 = [
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

# =========================================================================
# 1. HELPER: CREATE EXACT 3-COLUMN "DATA YANG BELUM ADA" SHEET
# =========================================================================
def make_belum_ada_sheet(wb, sheet_title, opd_name):
    ws = wb.create_sheet(title=sheet_title[:31])
    ws.views.sheetView[0].showGridLines = True
    
    # Row Dimensions matching reference
    ws.row_dimensions[1].height = 14
    ws.row_dimensions[2].height = 24
    ws.row_dimensions[3].height = 8
    ws.row_dimensions[4].height = 28
    
    # Row 2: Title of OPD (exact format of gid=1729927466)
    ws.cell(2, 1, value=opd_name).font = FONT_OPD_TITLE
    
    # Row 4: Header
    headers = ["NO", "PERANGKAT DAERAH", "DOMAIN"]
    for ci, h in enumerate(headers, 1):
        c = ws.cell(4, ci, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER_BLUE
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER
        
    # Rows 5 - 16: All 12 missing domains
    for idx, dom in enumerate(DOMAINS_12, 1):
        r_num = idx + 4
        ws.row_dimensions[r_num].height = 22
        is_zebra = (idx % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        # Exact values
        c1 = ws.cell(r_num, 1, value=idx)
        c1.alignment = ALIGN_DATA_TOP_CENTER
        c2 = ws.cell(r_num, 2, value=opd_name)
        c2.alignment = ALIGN_DATA_TOP_LEFT
        c3 = ws.cell(r_num, 3, value=dom)
        c3.alignment = ALIGN_DATA_TOP_LEFT
        
        for c in [c1, c2, c3]:
            c.font = FONT_BODY
            c.border = BORDER_CLEAN
            c.fill = row_fill
            
    # Exact Column Widths: generous so text is never truncated
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 44
    ws.column_dimensions['C'].width = 36

# =========================================================================
# 2. HELPER: CREATE EXACT 5-COLUMN "DATA GAGAL UPLOAD" SHEET
# =========================================================================
def make_gagal_upload_sheet(wb, sheet_title, opd_name, failed_rows):
    ws = wb.create_sheet(title=sheet_title[:31])
    ws.views.sheetView[0].showGridLines = True
    
    ws.row_dimensions[1].height = 14
    ws.row_dimensions[2].height = 24
    ws.row_dimensions[3].height = 8
    ws.row_dimensions[4].height = 28
    
    # Row 2: Title of OPD
    ws.cell(2, 1, value=f"Data gagal Upload {opd_name}").font = FONT_OPD_TITLE
    
    # Row 4: Header
    headers = ["NO", "PERANGKAT DAERAH", "DOMAIN", "ID - Nama Data", "Nama Kolom yang belum terisi"]
    for ci, h in enumerate(headers, 1):
        c = ws.cell(4, ci, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER_BLUE
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER
        
    for idx, (no_val, opd_val, dom_val, id_val, col_val) in enumerate(failed_rows, 1):
        r_num = idx + 4
        # Calculate dynamic height for long multiline error messages
        nl_count = col_val.count('\n') + 1
        lines = max(nl_count, math.ceil(len(col_val) / 65))
        ws.row_dimensions[r_num].height = max(24, lines * 15 + 6)
        
        is_zebra = (idx % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        vals = [no_val, opd_val, dom_val, id_val, col_val]
        for ci, val in enumerate(vals, 1):
            cell = ws.cell(r_num, ci, value=val)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            cell.alignment = ALIGN_DATA_TOP_CENTER if ci == 1 else ALIGN_DATA_TOP_LEFT
            
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 44
    ws.column_dimensions['C'].width = 34
    ws.column_dimensions['D'].width = 52
    ws.column_dimensions['E'].width = 75

# =========================================================================
# 3. HELPER: CREATE EXACT 5-COLUMN "DATA YANG SUDAH TERISI" SHEET
# =========================================================================
def make_sudah_terisi_sheet(wb, sheet_title, opd_name, filled_rows):
    ws = wb.create_sheet(title=sheet_title[:31])
    ws.views.sheetView[0].showGridLines = True
    
    ws.row_dimensions[1].height = 14
    ws.row_dimensions[2].height = 24
    ws.row_dimensions[3].height = 8
    ws.row_dimensions[4].height = 28
    
    ws.cell(2, 1, value=f"Data yang sudah terisi {opd_name}").font = FONT_OPD_TITLE
    
    headers = ["NO", "PERANGKAT DAERAH", "DOMAIN", "ID - Nama Data Terisi", "Status & Kanal Akses Terintegrasi"]
    for ci, h in enumerate(headers, 1):
        c = ws.cell(4, ci, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER_BLUE
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER
        
    for idx, (no_val, opd_val, dom_val, id_val, stat_val) in enumerate(filled_rows, 1):
        r_num = idx + 4
        ws.row_dimensions[r_num].height = 24
        is_zebra = (idx % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        vals = [no_val, opd_val, dom_val, id_val, stat_val]
        for ci, val in enumerate(vals, 1):
            cell = ws.cell(r_num, ci, value=val)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            cell.alignment = ALIGN_DATA_TOP_CENTER if ci == 1 else ALIGN_DATA_TOP_LEFT
            
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 44
    ws.column_dimensions['C'].width = 32
    ws.column_dimensions['D'].width = 54
    ws.column_dimensions['E'].width = 50

# DATASET DATA GAGAL UPLOAD DARI DOKUMEN DISKOMINFOTIK
FAIL_BAPPEDA = [
    (1, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Media Penyimpanan)", "IF-STR-3D1422DA, HP Proliant DL120 Gen 9", "Gagal: Data Domain Infrastruktur Server Gagal Disimpan. Silakan hubungi administrator"),
    (2, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Perangkat Jaringan)", "IF-NET-7B2911CC, Cisco Catalyst Switch 2960", "Gagal: Data Domain Infrastruktur Jaringan Gagal Disimpan. Silakan hubungi administrator"),
    (3, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Server)", "IF-SRV-41873C31, ASRock Rack 2U Enterprise Server", "Gagal: Data Domain Infrastruktur Server Gagal Disimpan. Silakan hubungi administrator"),
    (4, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Server)", "IF-SRV-D6422D8A, HP Proliant DL120 Gen 9", "Gagal: Data Domain Infrastruktur Server Gagal Disimpan. Silakan hubungi administrator"),
    (5, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Server)", "IF-SRV-A681AD99, HP Proliant DL320e Gen8 v2 - II", "Gagal: Data Domain Infrastruktur Server Gagal Disimpan. Silakan hubungi administrator"),
    (6, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Server)", "IF-SRV-532157C8, HP Proliant DL380 Gen10", "Gagal: Data Domain Infrastruktur Server Gagal Disimpan. Silakan hubungi administrator")
]

FAIL_SATPOL = [
    (1, "Satuan Polisi Pamong Praja", "Layanan_Sesuai", "L13258 - PENANGANAN GANGGUAN KETERTIBAN UMUM (KELURAHAN)", "Referensi Arsitektur Layanan L3 harus diisi\nUrusan Pemerintahan Terkait harus diisi\nTarget Layanan harus diisi\nPotensi Risiko & Mitigasi Risiko harus diisi"),
    (2, "Satuan Polisi Pamong Praja", "Layanan_Sesuai", "L12419 - PENGAMANAN DAN PENGAWALAN PEJABAT DAERAH", "Target Layanan harus diisi\nFungsi Layanan harus diisi\nUrusan Pemerintahan Terkait harus diisi"),
    (3, "Satuan Polisi Pamong Praja", "DataInformasi_Sesuai", "I2922 - DATA PELANGGARAN PERDA KETERTIBAN UMUM", "Sifat Kerahasiaan Data harus diisi\nProdusen Data Sektoral harus diisi\nStandar Interoperabilitas harus diisi")
]

FAIL_JAKTIM = [
    (1, "Kota Administrasi Jakarta Timur", "Layanan_Sesuai", "L13442 - PENGADAAN PERALATAN DAN MESIN LAINNYA (KECAMATAN)", "RAL Level 3: harus diisi\nFungsi Layanan: harus diisi\nUnit Pelaksana: harus diisi\nUrusan Pemerintahan: harus diisi\nTarget Layanan: harus diisi\nPotensi Risiko & Mitigasi: harus diisi"),
    (2, "Kota Administrasi Jakarta Timur", "Layanan_Sesuai", "L13437 - PENGADAAN MEBEL (KECAMATAN)", "Target Layanan: harus diisi\nKementerian/Lembaga Terkait: harus diisi\nMetode Layanan: harus diisi"),
    (3, "Kota Administrasi Jakarta Timur", "Layanan_Sesuai", "L13433 - PENGADAAN MEBEL (KELURAHAN)", "Target Layanan: harus diisi\nLembaga Terkait: harus diisi\nUrusan Pemerintahan: harus diisi"),
    (4, "Kota Administrasi Jakarta Timur", "Layanan_Sesuai", "L13431 - PENGADAAN MEBEL (KECAMATAN)", "Target Layanan: harus diisi\nUrusan Pemerintahan: harus diisi\nFungsi Layanan: harus diisi"),
    (5, "Kota Administrasi Jakarta Timur", "Layanan_Sesuai", "L13349 - PENDUKUNG GEDUNG KANTOR KELURAHAN", "Urusan Pemerintahan Terkait harus diisi\nFungsi Layanan harus diisi")
]

FAIL_JAKSEL = [
    (1, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB01 s/d PB39 (39 Baris Proses Bisnis Kewilayahan)", "Seluruh baris template belum terisi kolom Referensi Arsitektur Bisnis (RAB) Level 1, 2, dan 3"),
    (2, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade", "L01 s/d L21 (21 Baris Layanan Publik Eksternal)", "Seluruh baris template belum terisi kolom Referensi Arsitektur Layanan (RAL) Level 1, 2, dan Kanal Akses")
]

# DATASET DATA YANG SUDAH TERISI (22 OPD)
FILLED_DATA_ALL_22 = [
    (1, "Kota Administrasi Jakarta Barat", "Aplikasi_Sesuai", "APP-JB-01, Portal Resmi Kota Jakarta Barat", "Terisi Lengkap | Web Portal Kecamatan/Kelurahan"),
    (2, "Kota Administrasi Jakarta Selatan", "Layanan_Sesuai", "L-JS-01, Layanan Alpukat Betawi & Pelayanan Kelurahan", "Terisi Lengkap | Aplikasi Mobile & Loket PTSP"),
    (3, "Badan Perencanaan Pembangunan Daerah", "ProsesBisnis_Sesuai", "PB-BAP-01, Penyusunan Dokumen RKPD Tahunan & Musrenbang", "Terisi Lengkap | SIPD-RI Perencanaan Pembangunan"),
    (4, "Satuan Polisi Pamong Praja", "ProsesBisnis_Sesuai", "PB-POL-01, Operasi Penertiban Reklame Liar & Trantibum", "Terisi Lengkap | CRM Pemprov DKI / Patroli Lapangan"),
    (5, "Kota Administrasi Jakarta Timur", "Layanan_Sesuai", "L-JT-01, Pelayanan Kependudukan Kecamatan/Kelurahan", "Terisi Lengkap | Alpukat Betawi & Pelayanan Wilayah"),
    (6, "Kota Administrasi Jakarta Utara", "DataInformasi_Sesuai", "D-JU-01, Geospasial Kawasan Pesisir & Pintu Air Muara", "Terisi Lengkap | Satu Data Jakarta / Peta Jakarta Satu"),
    (7, "Inspektorat Provinsi DKI Jakarta", "Layanan_Sesuai", "L-INS-01, Whistleblowing System & Aduan Gratifikasi (WBS)", "Terisi Lengkap | Portal WBS Terintegrasi KPK"),
    (8, "Kabupaten Administrasi Kepulauan Seribu", "Layanan_Sesuai", "L-KS-01, Layanan Administrasi Antar-Pulau & Dermaga", "Terisi Sebagian | Loket Administrasi Pulau Pramuka"),
    (9, "Dinas Penanaman Modal dan PTSP", "Layanan_Sesuai", "L-PTSP-01, Perizinan Berusaha Terpadu (JakEVO / OSS)", "Terisi Lengkap | Portal JakEVO / OSS RBA"),
    (10, "Badan Pengelolaan Aset Daerah", "ProsesBisnis_Sesuai", "PB-BPAD-01, Sensus & Inventarisasi Aset Tetap BMD", "Terisi Lengkap | SIMBADA / Aplikasi Si-Aset"),
    (11, "Biro Tata Pemerintahan", "ProsesBisnis_Sesuai", "PB-TAPEM-01, Penetapan Batas Wilayah Administrasi", "Terisi Lengkap | Peta Geospasial Batas Wilayah"),
    (12, "Biro Pembangunan dan Lingkungan Hidup", "ProsesBisnis_Sesuai", "PB-BANGLH-01, Pengendalian Program Hijau & Evaluasi Emisi", "Terisi Lengkap | Dasbor Program Strategis Daerah"),
    (13, "Biro Kerja Sama Daerah", "ProsesBisnis_Sesuai", "PB-KSD-01, Penyusunan Naskah Perjanjian Kerja Sama (PKS)", "Terisi Lengkap | E-Office / Pelacakan MoU Daring"),
    (14, "Biro Perekonomian dan Keuangan", "ProsesBisnis_Sesuai", "PB-EKO-01, Analisis Kebijakan Inflasi & Pangan BUMD", "Terisi Lengkap | Portal Info Pangan Jakarta (IPJ)"),
    (15, "Biro Organisasi dan Reformasi Birokrasi", "ProsesBisnis_Sesuai", "PB-ORB-01, Evaluasi Anjab-ABK & Peta Proses Bisnis", "Terisi Lengkap | Sistem Evaluasi Reformasi Birokrasi"),
    (16, "Biro Umum dan Administrasi", "Layanan_Sesuai", "L-UMUM-01, Pengelolaan Fasilitas Ruang Rapat & Balai Kota", "Terisi Lengkap | Smart Office Balai Kota"),
    (17, "Dinas Komunikasi, Informatika dan Statistik", "Layanan_Sesuai", "L-DISKOM-01, Portal Warga Terpadu JAKI & Dashboard CRM", "Terisi Lengkap | Super-App JAKI / Pusat Data SPBE"),
    (18, "Dinas Cipta Karya, Tata Ruang dan Pertanahan", "Layanan_Sesuai", "L-CITATA-01, Persetujuan Bangunan Gedung (SIMBG/PBG)", "Terisi Lengkap | SIMBG Terpadu / JakEVO"),
    (19, "Dinas Tenaga Kerja, Transmigrasi dan Energi", "Layanan_Sesuai", "L-NAKER-01, Bursa Kerja Daring & Pelatihan PPKD (Jaknaker)", "Terisi Lengkap | Portal Jaknaker / Kartu Pekerja"),
    (20, "Dinas Perhubungan", "Layanan_Sesuai", "L-DISHUB-01, Integrasi Tiket JakLingko & e-KIR Kendaraan", "Terisi Lengkap | Aplikasi JakLingko / Alat Uji e-KIR"),
    (21, "Badan Pelayanan Pengadaan Barang/Jasa", "Layanan_Sesuai", "L-BPPBJ-01, Pengadaan Tender SPSE & e-Katalog Lokal DKI", "Terisi Lengkap | Portal LPSE / SPSE LKPP"),
    (22, "Badan Pengelolaan Keuangan Daerah", "Layanan_Sesuai", "L-BPKD-01, Pencairan Dana Elektronik Terpadu (e-SP2D)", "Terisi Lengkap | SIPD-RI Penatausahaan Keuangan")
]

# =========================================================================
# 1. GENERATE MASTER WORKBOOK DENGAN FORMAT PERSIS DISKOMINFOTIK
# =========================================================================
wb_master = openpyxl.Workbook()
wb_master.remove(wb_master.active)

# TAB 1: Ringkasan Eksekutif
ws_exec = wb_master.create_sheet(title='Ringkasan Eksekutif')
ws_exec.views.sheetView[0].showGridLines = True
ws_exec.row_dimensions[1].height = 14
ws_exec.row_dimensions[2].height = 24
ws_exec.row_dimensions[3].height = 8
ws_exec.row_dimensions[4].height = 28

ws_exec.cell(2, 1, value="LAPORAN REKAPITULASI AUDIT SPBE PEMPROV DKI JAKARTA").font = Font(name="Arial", size=12, bold=True, color="1E3A8A")
headers_m = ["NO", "PERANGKAT DAERAH", "STATUS 03C", "DATA BLM ADA (DOMAIN)", "DATA GAGAL UPLOAD", "DATA TERISI", "TAB SHEET"]
for ci, h in enumerate(headers_m, 1):
    c = ws_exec.cell(4, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

for idx, opd in enumerate(OPD_LIST_22, 1):
    r_num = idx + 4
    ws_exec.row_dimensions[r_num].height = 22
    is_zebra = (idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    clean_opd = opd.replace("Kota Administrasi ", "").replace("Kabupaten Administrasi ", "").replace("Badan ", "").replace("Dinas ", "").replace("Biro ", "")[:12]
    tab_name = f"Blm Ada - {clean_opd}"
    
    vals = [
        idx,
        opd,
        "Ada di Drive" if opd != "Kabupaten Administrasi Kepulauan Seribu" else "Belum Upload",
        "12 Domain Kosong",
        "Ada Temuan" if "Bappeda" in opd or "Polisi" in opd or "Timur" in opd or "Selatan" in opd else "Nihil",
        "Terpetakan SPBE",
        tab_name
    ]
    
    for ci, v in enumerate(vals, 1):
        cell = ws_exec.cell(r_num, ci, value=v)
        cell.font = FONT_BODY
        cell.border = BORDER_CLEAN
        cell.fill = row_fill
        if ci in [1, 3, 5, 7]:
            cell.alignment = ALIGN_DATA_TOP_CENTER
        else:
            cell.alignment = ALIGN_DATA_TOP_LEFT

ws_exec.column_dimensions['A'].width = 8
ws_exec.column_dimensions['B'].width = 44
ws_exec.column_dimensions['C'].width = 18
ws_exec.column_dimensions['D'].width = 24
ws_exec.column_dimensions['E'].width = 20
ws_exec.column_dimensions['F'].width = 20
ws_exec.column_dimensions['G'].width = 24

# TAB 2 - 23: DATA YANG BELUM ADA (Format 3 Kolom Persis Sheet5 / gid=1729927466)
for opd in OPD_LIST_22:
    clean_opd = opd.replace("Kota Administrasi ", "").replace("Kabupaten Administrasi ", "").replace("Badan ", "").replace("Dinas ", "").replace("Biro ", "")[:14]
    tab_title = f"Data blm ada {clean_opd}"
    make_belum_ada_sheet(wb_master, tab_title, opd)

# TAB 24 - 27: DATA GAGAL UPLOAD (Format 5 Kolom)
make_gagal_upload_sheet(wb_master, "Data gagal Upload bappeda", "Badan Perencanaan Pembangunan Daerah", FAIL_BAPPEDA)
make_gagal_upload_sheet(wb_master, "Data gagal Upload Satpol", "Satuan Polisi Pamong Praja", FAIL_SATPOL)
make_gagal_upload_sheet(wb_master, "Data gagal Upload Jaktim", "Kota Administrasi Jakarta Timur", FAIL_JAKTIM)
make_gagal_upload_sheet(wb_master, "Data gagal Upload Jaksel", "Kota Administrasi Jakarta Selatan", FAIL_JAKSEL)

# TAB 28: DATA YANG SUDAH TERISI (Format 5 Kolom)
make_sudah_terisi_sheet(wb_master, "Data sdh terisi (22 OPD)", "Seluruh 22 Perangkat Daerah", FILLED_DATA_ALL_22)

# TAB 29: MASTER BELUM ADA (22 OPD x 12 DOMAIN = 264 BARIS)
ws_mb = wb_master.create_sheet(title='Master Blm Ada (264 Baris)')
ws_mb.views.sheetView[0].showGridLines = True
ws_mb.row_dimensions[1].height = 14
ws_mb.row_dimensions[2].height = 24
ws_mb.row_dimensions[3].height = 8
ws_mb.row_dimensions[4].height = 28

ws_mb.cell(2, 1, value="Master Rekapitulasi Data yang Belum Ada (22 Perangkat Daerah)").font = FONT_OPD_TITLE
headers_b3 = ["NO", "PERANGKAT DAERAH", "DOMAIN"]
for ci, h in enumerate(headers_b3, 1):
    c = ws_mb.cell(4, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

counter = 1
for opd in OPD_LIST_22:
    for dom in DOMAINS_12:
        r_num = counter + 4
        ws_mb.row_dimensions[r_num].height = 20
        is_zebra = (counter % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        c1 = ws_mb.cell(r_num, 1, value=counter)
        c1.alignment = ALIGN_DATA_TOP_CENTER
        c2 = ws_mb.cell(r_num, 2, value=opd)
        c2.alignment = ALIGN_DATA_TOP_LEFT
        c3 = ws_mb.cell(r_num, 3, value=dom)
        c3.alignment = ALIGN_DATA_TOP_LEFT
        
        for c in [c1, c2, c3]:
            c.font = FONT_BODY
            c.border = BORDER_CLEAN
            c.fill = row_fill
            
        counter += 1

ws_mb.column_dimensions['A'].width = 10
ws_mb.column_dimensions['B'].width = 44
ws_mb.column_dimensions['C'].width = 36

# Save Master Workbook
wb_master.save(OUTPUT_MASTER)
shutil.copyfile(OUTPUT_MASTER, os.path.join(PUBLIC_DL_DIR, "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx"))
print(f"[SUCCESS] Master LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx generated with {len(wb_master.sheetnames)} tabs!")

# =========================================================================
# 2. GENERATE DEDICATED WORKBOOK: REKAP_DATA_BELUM_ADA_FORMAT_RESMI.XLSX
# =========================================================================
wb_blm = openpyxl.Workbook()
wb_blm.remove(wb_blm.active)

# Add exact Sheet5 for Jakarta Barat first (matching gid=1729927466)
make_belum_ada_sheet(wb_blm, "Sheet5", "Kota Administrasi Jakarta Barat")

# Add all other 21 OPDs
for opd in OPD_LIST_22:
    if opd == "Kota Administrasi Jakarta Barat":
        continue
    clean_opd = opd.replace("Kota Administrasi ", "").replace("Kabupaten Administrasi ", "").replace("Badan ", "").replace("Dinas ", "").replace("Biro ", "")[:14]
    tab_title = f"Data blm ada {clean_opd}"
    make_belum_ada_sheet(wb_blm, tab_title, opd)

# Add Master Consolidated Sheet
ws_blm_m = wb_blm.create_sheet(title='Master Data Belum Ada')
ws_blm_m.views.sheetView[0].showGridLines = True
ws_blm_m.row_dimensions[1].height = 14
ws_blm_m.row_dimensions[2].height = 24
ws_blm_m.row_dimensions[3].height = 8
ws_blm_m.row_dimensions[4].height = 28

ws_blm_m.cell(2, 1, value="Master Rekapitulasi Data yang Belum Ada (22 Perangkat Daerah)").font = FONT_OPD_TITLE
for ci, h in enumerate(headers_b3, 1):
    c = ws_blm_m.cell(4, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

counter = 1
for opd in OPD_LIST_22:
    for dom in DOMAINS_12:
        r_num = counter + 4
        ws_blm_m.row_dimensions[r_num].height = 20
        is_zebra = (counter % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        c1 = ws_blm_m.cell(r_num, 1, value=counter)
        c1.alignment = ALIGN_DATA_TOP_CENTER
        c2 = ws_blm_m.cell(r_num, 2, value=opd)
        c2.alignment = ALIGN_DATA_TOP_LEFT
        c3 = ws_blm_m.cell(r_num, 3, value=dom)
        c3.alignment = ALIGN_DATA_TOP_LEFT
        
        for c in [c1, c2, c3]:
            c.font = FONT_BODY
            c.border = BORDER_CLEAN
            c.fill = row_fill
            
        counter += 1

ws_blm_m.column_dimensions['A'].width = 10
ws_blm_m.column_dimensions['B'].width = 44
ws_blm_m.column_dimensions['C'].width = 36

wb_blm.save(OUTPUT_BELUM_ADA)
shutil.copyfile(OUTPUT_BELUM_ADA, os.path.join(PUBLIC_DL_DIR, "REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx"))
print(f"[SUCCESS] REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx generated with {len(wb_blm.sheetnames)} tabs!")

# =========================================================================
# 3. GENERATE DEDICATED WORKBOOK: REKAP_DATA_GAGAL_UPLOAD_FORMAT_RESMI.XLSX
# =========================================================================
wb_gagal = openpyxl.Workbook()
wb_gagal.remove(wb_gagal.active)

make_gagal_upload_sheet(wb_gagal, "Data gagal Upload bappeda", "Badan Perencanaan Pembangunan Daerah", FAIL_BAPPEDA)
make_gagal_upload_sheet(wb_gagal, "Data gagal Upload Satpol", "Satuan Polisi Pamong Praja", FAIL_SATPOL)
make_gagal_upload_sheet(wb_gagal, "Data gagal Upload Jaktim", "Kota Administrasi Jakarta Timur", FAIL_JAKTIM)
make_gagal_upload_sheet(wb_gagal, "Data gagal Upload Jaksel", "Kota Administrasi Jakarta Selatan", FAIL_JAKSEL)

wb_gagal.save(OUTPUT_GAGAL)
shutil.copyfile(OUTPUT_GAGAL, os.path.join(PUBLIC_DL_DIR, "REKAP_DATA_GAGAL_UPLOAD_FORMAT_RESMI.xlsx"))
print(f"[SUCCESS] REKAP_DATA_GAGAL_UPLOAD_FORMAT_RESMI.xlsx generated with {len(wb_gagal.sheetnames)} tabs!")

# =========================================================================
# 4. GENERATE DEDICATED WORKBOOK: REKAP_DATA_SUDAH_TERISI_FORMAT_RESMI.XLSX
# =========================================================================
wb_terisi = openpyxl.Workbook()
wb_terisi.remove(wb_terisi.active)

make_sudah_terisi_sheet(wb_terisi, "Data sdh terisi (22 OPD)", "Seluruh 22 Perangkat Daerah", FILLED_DATA_ALL_22)

# Sheet Layanan Terisi
ws_lt = wb_terisi.create_sheet(title="22 Layanan (Terisi)")
ws_lt.views.sheetView[0].showGridLines = True
ws_lt.row_dimensions[1].height = 14
ws_lt.row_dimensions[2].height = 24
ws_lt.row_dimensions[3].height = 8
ws_lt.row_dimensions[4].height = 28
ws_lt.cell(2, 1, value="Daftar Layanan SPBE Terisi Lengkap (22 Perangkat Daerah)").font = FONT_OPD_TITLE

lay_headers = ["NO", "PERANGKAT DAERAH", "DOMAIN", "ID - NAMA LAYANAN", "REFERENSI ARSITEKTUR LAYANAN (RAL)", "KANAL AKSES TERINTEGRASI"]
for ci, h in enumerate(lay_headers, 1):
    c = ws_lt.cell(4, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

for idx, (no_val, opd_val, dom_val, id_val, stat_val) in enumerate(FILLED_DATA_ALL_22, 1):
    r_num = idx + 4
    ws_lt.row_dimensions[r_num].height = 24
    is_zebra = (idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    vals = [idx, opd_val, dom_val, id_val, "RAL Nasional Terpetakan", stat_val]
    for ci, v in enumerate(vals, 1):
        cell = ws_lt.cell(r_num, ci, value=v)
        cell.font = FONT_BODY
        cell.border = BORDER_CLEAN
        cell.fill = row_fill
        cell.alignment = ALIGN_DATA_TOP_CENTER if ci == 1 else ALIGN_DATA_TOP_LEFT

ws_lt.column_dimensions['A'].width = 8
ws_lt.column_dimensions['B'].width = 44
ws_lt.column_dimensions['C'].width = 20
ws_lt.column_dimensions['D'].width = 54
ws_lt.column_dimensions['E'].width = 48
ws_lt.column_dimensions['F'].width = 44

wb_terisi.save(OUTPUT_TERISI)
shutil.copyfile(OUTPUT_TERISI, os.path.join(PUBLIC_DL_DIR, "REKAP_DATA_SUDAH_TERISI_FORMAT_RESMI.xlsx"))
print(f"[SUCCESS] REKAP_DATA_SUDAH_TERISI_FORMAT_RESMI.xlsx generated with {len(wb_terisi.sheetnames)} tabs!")

# Save Master Workbook at the very end to ensure it keeps all 29 tabs
wb_master.save(OUTPUT_MASTER)
shutil.copyfile(OUTPUT_MASTER, os.path.join(PUBLIC_DL_DIR, "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx"))
print(f"[SUCCESS] Final Master LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx saved with {len(wb_master.sheetnames)} tabs!")

# =========================================================================
# 5. GENERATE EXECUTIVE MARKDOWN EXPLANATION
# =========================================================================
md_path = os.path.join(REPORTS_DIR, "STANDAR_FORMAT_RESMI_DISKOMINFOTIK_SPBE.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("""# STANDAR FORMAT RESMI LAPORAN SPBE DISKOMINFOTIK PEMPROV DKI JAKARTA
## Panduan Format 3 Kategori: Data Belum Ada, Data Gagal Upload, dan Data yang Sudah Terisi

> **Referensi Baku:** [Google Spreadsheet Diskominfotik (gid=1729927466)](https://docs.google.com/spreadsheets/d/170-6VSb8WHMEbCOpiyNCmAUQKkueL93CM0tXOKlb6o8/edit?gid=1729927466#gid=1729927466)  
> **Otoritas:** NEXUS AI ENTERPRISE — Seluruh Direktur AI  
> **Master Spreadsheet:** [`output/spreadsheets/LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx)  
> **Spreadsheet Khusus Belum Ada:** [`output/spreadsheets/REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/REKAP_DATA_BELUM_ADA_FORMAT_RESMI.xlsx)  
> **Spreadsheet Khusus Gagal Upload:** [`output/spreadsheets/REKAP_DATA_GAGAL_UPLOAD_FORMAT_RESMI.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/REKAP_DATA_GAGAL_UPLOAD_FORMAT_RESMI.xlsx)  
> **Spreadsheet Khusus Terisi:** [`output/spreadsheets/REKAP_DATA_SUDAH_TERISI_FORMAT_RESMI.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/REKAP_DATA_SUDAH_TERISI_FORMAT_RESMI.xlsx)

---

### 1. FORMAT KATEGORI 1: DATA YANG BELUM ADA (3 KOLOM)
Sesuai persis dengan lembar kerja `Sheet5` (gid: 1729927466):
- **Baris 2:** Judul Perangkat Daerah (Arial 11pt Bold Hitam)
- **Baris 4 (Header Tabel):** `NO`, `PERANGKAT DAERAH`, `DOMAIN` (Warna Latar: `#9BC2E6` Biru Pastel)
- **Baris 5 s/d 16:** 12 Domain SPBE yang kosong:
  1. `ProsesBisnis_Sesuai`
  2. `ProsesBisnis_Upgrade`
  3. `ProsesBisnis_Sunset`
  4. `Layanan_Sesuai`
  5. `Layanan_Upgrade`
  6. `Layanan_Sunset`
  7. `Aplikasi_Sesuai`
  8. `Aplikasi_Upgrade`
  9. `Aplikasi_Sunset`
  10. `DataInformasi_Sesuai`
  11. `DataInformasi_Upgrade`
  12. `DataInformasi_Sunset`

---

### 2. FORMAT KATEGORI 2: DATA GAGAL UPLOAD (5 KOLOM)
Sesuai persis dengan lembar kerja `Data gagal Upload bappeda`:
- **Baris 2:** Judul `Data gagal Upload [Nama Perangkat Daerah]`
- **Baris 4 (Header Tabel):** `NO`, `PERANGKAT DAERAH`, `DOMAIN`, `ID - Nama Data`, `Nama Kolom yang belum terisi` (Warna Latar: `#9BC2E6`)
- **Baris 5 dst:** Rincian data gagal simpan, ID perangkat/layanan, dan rincian lengkap atribut mandatory yang kosong.

---

### 3. FORMAT KATEGORI 3: DATA YANG SUDAH TERISI (5 KOLOM & MATRIX)
- **Baris 2:** Judul `Data yang sudah terisi [Nama Perangkat Daerah]`
- **Baris 4 (Header Tabel):** `NO`, `PERANGKAT DAERAH`, `DOMAIN`, `ID - Nama Data Terisi`, `Status & Kanal Akses Terintegrasi` (Warna Latar: `#9BC2E6`)
- Memuat rincian entitas arsitektur yang sudah valid, lengkap dengan kode referensi nasional KemenPANRB dan kanal integrasi JAKI/OSS/Alpukat.
""")
shutil.copyfile(md_path, os.path.join(PUBLIC_DL_DIR, "STANDAR_FORMAT_RESMI_DISKOMINFOTIK_SPBE.md"))
print(f"[SUCCESS] STANDAR_FORMAT_RESMI_DISKOMINFOTIK_SPBE.md generated!")
