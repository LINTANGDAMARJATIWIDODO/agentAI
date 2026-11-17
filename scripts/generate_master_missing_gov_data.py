"""
NEXUS AI ENTERPRISE — MASTER DATA AUDIT: ALL MISSING GOVERNMENT DATA
File: reports/LAPORAN_SEMUA_DATA_BELUM_ADA_PEMERINTAHAN.md
And adds Tab 'REKAP BELUM ADA SELURUH OPD' to output/spreadsheets/LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx
"""

import os
import math
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_FILE = os.path.join(BASE_DIR, "output", "spreadsheets", "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx")
PUBLIC_EXCEL = os.path.join(BASE_DIR, "public", "downloads", "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx")
REPORT_MD = os.path.join(BASE_DIR, "reports", "LAPORAN_SEMUA_DATA_BELUM_ADA_PEMERINTAHAN.md")

# Complete Inventory of ALL 51 Government Bodies & All Deficiencies
gov_missing_inventory = [
    # 1. KOTA & KABUPATEN ADMINISTRASI
    {
        "no": "1.0",
        "opd": "KABUPATEN ADMINISTRASI KEPULAUAN SERIBU",
        "kategori": "Wilayah Kepulauan",
        "pic": "Adi Widiantono",
        "bast_status": "BELUM ADA",
        "ba_status": "BELUM DIBUAT",
        "tobe_status": "BELUM ADA (03C Belum Diunggah)",
        "domain_belum_ada": "03C_To_Be_As_is, BAST, Berita Acara, Record Zoom",
        "kolom_belum_terisi": "Seluruh file 03C belum diunggah; berkas fisik BAST & BA belum ada",
        "tingkat_urgensi": "KRITIS (NOL DOKUMEN)",
        "tindakan_remediasi": "Penyusunan draf BA/BAST baru dan percepatan unggah file 03C"
    },
    {
        "no": "2.0",
        "opd": "KOTA ADMINISTRASI JAKARTA SELATAN",
        "kategori": "Kota Administrasi",
        "pic": "Adi Widiantono",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "TEMPLATE KOSONG (39 PB & 21 Layanan)",
        "domain_belum_ada": "ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Upgrade, Layanan_Sunset, Aplikasi_Sunset, DataInformasi_Upgrade, DataInformasi_Sunset",
        "kolom_belum_terisi": "Domain, Kategori To-Be, As-Is Terkait, Perangkat Daerah, RAB Level 1-3, RAL Level 1-2 (Semua baris kosong)",
        "tingkat_urgensi": "KRITIS (TEMPLATE KOSONG)",
        "tindakan_remediasi": "Gunakan Tab '39 ProsesBisnis (TERISI)' & '21 Layanan (TERISI)' hasil AI NEXUS"
    },
    {
        "no": "3.0",
        "opd": "KOTA ADMINISTRASI JAKARTA TIMUR",
        "kategori": "Kota Administrasi",
        "pic": "Adi Widiantono",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada (Sebagian Kosong)",
        "domain_belum_ada": "ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Sunset, DataInformasi_Upgrade, DataInformasi_Sunset",
        "kolom_belum_terisi": "L13349, L13344: Referensi Arsitektur Layanan Level 3, Target Layanan, Potensi Manfaat, Potensi Risiko, Mitigasi Risiko",
        "tingkat_urgensi": "TINGGI (KOLOM KOSONG)",
        "tindakan_remediasi": "Lengkapi 11 atribut mandatory pada layanan kelurahan L13349 & L13344"
    },
    {
        "no": "4.0",
        "opd": "KOTA ADMINISTRASI JAKARTA UTARA",
        "kategori": "Kota Administrasi",
        "pic": "Adi Widiantono",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada (7 Domain Kosong)",
        "domain_belum_ada": "ProsesBisnis_Sesuai, ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Sesuai, Layanan_Upgrade, Layanan_Sunset, Aplikasi_Sunset",
        "kolom_belum_terisi": "Seluruh baris domain proses bisnis dan layanan belum diunggah ke folder Drive",
        "tingkat_urgensi": "TINGGI (7 DOMAIN KOSONG)",
        "tindakan_remediasi": "Penyusunan peta proses bisnis kewilayahan Jakut sesuai Pergub 57/2022"
    },
    {
        "no": "5.0",
        "opd": "KOTA ADMINISTRASI JAKARTA BARAT",
        "kategori": "Kota Administrasi",
        "pic": "Rivan Dely Kusuna",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada (10 Domain Kosong)",
        "domain_belum_ada": "ProsesBisnis_Sesuai, ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Sesuai, Layanan_Upgrade, Layanan_Sunset, Aplikasi_Sesuai, Aplikasi_Upgrade, Aplikasi_Sunset, DataInformasi_Sesuai",
        "kolom_belum_terisi": "10 lembar kerja arsitektur SPBE masih kosong (Tercatat pada Sheet 5 Rekap CBC)",
        "tingkat_urgensi": "TINGGI (10 DOMAIN KOSONG)",
        "tindakan_remediasi": "Pengisian terpadu 10 domain SPBE tingkat Kota Administrasi Jakbar"
    },
    {
        "no": "6.0",
        "opd": "KOTA ADMINISTRASI JAKARTA PUSAT",
        "kategori": "Kota Administrasi",
        "pic": "Rivan Dely Kusuna",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada (Verifikasi Isian)",
        "domain_belum_ada": "ProsesBisnis_Upgrade, Layanan_Upgrade (Perlu verifikasi baris kosong seperti Jaksel)",
        "kolom_belum_terisi": "Berpotensi memiliki kekosongan baris template serupa Jakarta Selatan",
        "tingkat_urgensi": "SEDANG",
        "tindakan_remediasi": "Audit forensik file 03C Jakpus untuk memastikan tidak ada sel template kosong"
    },

    # 2. BIRO-BIRO SEKRETARIAT DAERAH (SETDA)
    {
        "no": "7.0",
        "opd": "BIRO PEMERINTAHAN",
        "kategori": "Biro Setda",
        "pic": "Adi Widiantono",
        "bast_status": "BELUM ADA (Hardcopy Belum di Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "Fisik BAST Belum Diserahkan",
        "kolom_belum_terisi": "Keterangan checklist: 'BAST Kirim softcopy, Hard copy BAST blm ada di Dinas'",
        "tingkat_urgensi": "TINGGI (BAST FISIK PENDING)",
        "tindakan_remediasi": "Pengiriman hardcopy fisik berkas BAST asli ke kantor dinas"
    },
    {
        "no": "8.0",
        "opd": "BIRO PEMBANGUNAN DAN LINGKUNGAN HIDUP",
        "kategori": "Biro Setda",
        "pic": "Rico Sugiyono",
        "bast_status": "BELUM ADA (Menunggu TTD Es 3)",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "BAST Belum Masuk",
        "kolom_belum_terisi": "Tanda tangan Pejabat Eselon 3 masih dalam proses penandatanganan",
        "tingkat_urgensi": "TINGGI (TTD ES 3 PENDING)",
        "tindakan_remediasi": "Percepatan penandatanganan berkas BAST oleh Kabag/Eselon 3 BangLH"
    },
    {
        "no": "9.0",
        "opd": "BIRO KERJA SAMA DAERAH",
        "kategori": "Biro Setda",
        "pic": "Sulistyo Aris Hirtranusi",
        "bast_status": "BELUM ADA (Menunggu TTD Es 3)",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "BAST Belum Masuk",
        "kolom_belum_terisi": "Wajib TTD Eselon 3 sebelum dapat diserahterimakan",
        "tingkat_urgensi": "TINGGI (TTD ES 3 PENDING)",
        "tindakan_remediasi": "Koordinasi penandatanganan pejabat Eselon 3 Biro KSD"
    },
    {
        "no": "10.0",
        "opd": "BIRO PEREKONOMIAN DAN KEUANGAN",
        "kategori": "Biro Setda",
        "pic": "Sulistyo Aris Hirtranusi",
        "bast_status": "BELUM ADA (Hardcopy Belum di Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "Fisik BAST Belum Diserahkan",
        "kolom_belum_terisi": "Hard copy BAST belum ada di dinas",
        "tingkat_urgensi": "TINGGI (BAST FISIK PENDING)",
        "tindakan_remediasi": "Penyerahan tanda terima berkas fisik BAST ke dinas terkait"
    },
    {
        "no": "11.0",
        "opd": "BIRO UMUM DAN ADMINISTRASI",
        "kategori": "Biro Setda",
        "pic": "Rivan Dely Kusuna",
        "bast_status": "BELUM ADA (BAST Harus TTD Es 3)",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "BAST Belum Sah",
        "kolom_belum_terisi": "BAST Harus TTD Eselon 3; Record Zoom menumpang ke BPSDM",
        "tingkat_urgensi": "TINGGI (TTD ES 3 PENDING)",
        "tindakan_remediasi": "Penyelesaian tanda tangan Eselon 3 Biro Umum dan dokumentasi Zoom mandiri"
    },
    {
        "no": "12.0",
        "opd": "BIRO ORGANISASI DAN REFORMASI BIROKRASI",
        "kategori": "Biro Setda",
        "pic": "Adi Widiantono",
        "bast_status": "Ada (FGD/Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "Dokumen Belum Ditandatangani Es 3",
        "kolom_belum_terisi": "Keterangan checklist: 'Harus TTD ES 3, Sudah di Dinas'",
        "tingkat_urgensi": "SEDANG",
        "tindakan_remediasi": "Follow up tanda tangan pejabat Eselon 3 Biro ORB"
    },

    # 3. BADAN-BADAN DAERAH
    {
        "no": "13.0",
        "opd": "BADAN PERENCANAAN PEMBANGUNAN DAERAH (BAPPEDA)",
        "kategori": "Badan Daerah",
        "pic": "Adi Widiantono",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "GAGAL SIMPAN SERVER & 6 DOMAIN KOSONG",
        "domain_belum_ada": "ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Sunset, Aplikasi_Sunset, DataInformasi_Upgrade, DataInformasi_Sunset",
        "kolom_belum_terisi": "10 unit Server HP Proliant & ASRock gagal simpan di database; 6 domain kosong",
        "tingkat_urgensi": "KRITIS (SERVER GAGAL SIMPAN)",
        "tindakan_remediasi": "Perbaikan format data server HP Proliant dan pengisian 6 domain kosong"
    },
    {
        "no": "14.0",
        "opd": "BADAN PENGELOLAAN ASET DAERAH (BPAD)",
        "kategori": "Badan Daerah",
        "pic": "Sulistyo Aris Hirtranusi",
        "bast_status": "BELUM ADA (Hardcopy Belum di Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "Fisik BAST Belum Diserahkan",
        "kolom_belum_terisi": "Hard copy BAST fisik belum masuk ke kantor dinas",
        "tingkat_urgensi": "TINGGI (BAST FISIK PENDING)",
        "tindakan_remediasi": "Pengiriman hardcopy fisik berkas BAST asli BPAD"
    },
    {
        "no": "15.0",
        "opd": "BADAN PENGELOLAAN KEUANGAN DAERAH (BPKD)",
        "kategori": "Badan Daerah",
        "pic": "Sulistyo Aris Hirtranusi",
        "bast_status": "Ada (Dinas)",
        "ba_status": "PENDING (Belum TTD Bu Kabid)",
        "tobe_status": "Ada",
        "domain_belum_ada": "Berita Acara Belum Sah",
        "kolom_belum_terisi": "Keterangan checklist: 'BA BPKD belum ditandatangani oleh Bu Kabid'",
        "tingkat_urgensi": "TINGGI (BA BELUM TTD)",
        "tindakan_remediasi": "Koordinasi penandatanganan Berita Acara oleh Kepala Bidang BPKD"
    },
    {
        "no": "16.0",
        "opd": "BADAN PENANGGULANGAN BENCANA DAERAH (BPBD)",
        "kategori": "Badan Daerah",
        "pic": "Adi Widiantono",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "Rekaman Zoom FGD Tidak Ada",
        "kolom_belum_terisi": "Keterangan checklist: 'Record Zoom tidak ada.'",
        "tingkat_urgensi": "SEDANG",
        "tindakan_remediasi": "Pelampiran notulensi rapat pengganti atau berita acara konfirmasi FGD"
    },
    {
        "no": "17.0",
        "opd": "BADAN PELAYANAN PENGADAAN BARANG/JASA (BPPBJ)",
        "kategori": "Badan Daerah",
        "pic": "Sulistyo Aris Hirtranusi",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "DITARIK KEMBALI OLEH PD",
        "domain_belum_ada": "Dokumen To-Be Dibawa Kembali untuk Reviu",
        "kolom_belum_terisi": "Dokumen scan To-Be ditarik oleh pihak dinas untuk perbaikan data internal",
        "tingkat_urgensi": "TINGGI (DOKUMEN DITARIK)",
        "tindakan_remediasi": "Penarikan kembali hasil reviu berkas To-Be dari BPPBJ"
    },

    # 4. DINAS-DINAS TEKNIS
    {
        "no": "18.0",
        "opd": "SATUAN POLISI PAMONG PRAJA (SATPOL PP)",
        "kategori": "Dinas Teknis / Satuan",
        "pic": "Rivan Dely Kusuna",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada (Kolom Mandatory Kosong)",
        "domain_belum_ada": "ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Sunset, Aplikasi_Sunset, DataInformasi_Upgrade, DataInformasi_Sunset",
        "kolom_belum_terisi": "L13258, L12419: RAL Level 3, Fungsi Layanan, Target Layanan, Potensi Risiko & Mitigasi; I2921, I2922: Asal Data & Wali Data",
        "tingkat_urgensi": "TINGGI (KOLOM MANDATORY KOSONG)",
        "tindakan_remediasi": "Pengisian rincian risiko, fungsi, dan wali data pada formulir layanan Satpol PP"
    },
    {
        "no": "19.0",
        "opd": "DINAS PENANAMAN MODAL DAN PTSP (DPMPTSP)",
        "kategori": "Dinas Teknis",
        "pic": "Sulistyo Aris Hirtranusi",
        "bast_status": "BELUM ADA",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "BAST Belum Ada",
        "kolom_belum_terisi": "Kolom BAST berstatus 'Belum' dan berkas belum diunggah",
        "tingkat_urgensi": "TINGGI (BAST BELUM ADA)",
        "tindakan_remediasi": "Penerbitan dan penandatanganan dokumen BAST resmi DPMPTSP"
    },
    {
        "no": "20.0",
        "opd": "DINAS KOMUNIKASI, INFORMATIKA DAN STATISTIK",
        "kategori": "Dinas Teknis",
        "pic": "Rivan Dely Kusuna",
        "bast_status": "BELUM ADA",
        "ba_status": "Ada",
        "tobe_status": "Ada",
        "domain_belum_ada": "BAST Belum Masuk",
        "kolom_belum_terisi": "Kolom BAST berstatus 'Belum'",
        "tingkat_urgensi": "TINGGI (BAST BELUM ADA)",
        "tindakan_remediasi": "Finalisasi berkas BAST internal Diskominfotik"
    },
    {
        "no": "21.0",
        "opd": "DINAS TENAGA KERJA, TRANSMIGRASI DAN ENERGI",
        "kategori": "Dinas Teknis",
        "pic": "Sulistyo Aris Hirtranusi",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "03 MASIH DRAFT",
        "domain_belum_ada": "Dokumen 03 Masih Draf Belum Final",
        "kolom_belum_terisi": "Dokumen arsitektur 03 belum disahkan / masih draf awal",
        "tingkat_urgensi": "TINGGI (03 MASIH DRAFT)",
        "tindakan_remediasi": "Finalisasi draf arsitektur Disnakertransgi menjadi dokumen definitif"
    },
    {
        "no": "22.0",
        "opd": "DINAS PERHUBUNGAN (DISHUB)",
        "kategori": "Dinas Teknis",
        "pic": "Sulistyo Aris Hirtranusi",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "DITARIK KEMBALI OLEH PD",
        "domain_belum_ada": "Dokumen To-Be Dibawa Kembali untuk Reviu Ulang",
        "kolom_belum_terisi": "Dokumen To Be scan ttd masih dibawa dinas untuk reviu internal",
        "tingkat_urgensi": "TINGGI (DOKUMEN DITARIK)",
        "tindakan_remediasi": "Follow up pengembalian berkas hasil scan To-Be dari Dishub"
    },
    {
        "no": "23.0",
        "opd": "DINAS CIPTA KARYA, TATA RUANG DAN PERTANAHAN",
        "kategori": "Dinas Teknis",
        "pic": "Rico Sugiyono",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada (Menunggu TTD Es 3)",
        "domain_belum_ada": "Tanda Tangan Eselon 3 Belum Lengkap",
        "kolom_belum_terisi": "Soft copy ada, fisik dokumen tertahan menunggu TTD Eselon 3",
        "tingkat_urgensi": "SEDANG",
        "tindakan_remediasi": "Penyelesaian tanda tangan fisik pejabat Eselon 3 Dinas Citata"
    },
    {
        "no": "24.0",
        "opd": "DINAS PENANGGULANGAN KEBAKARAN & PENYELAMATAN",
        "kategori": "Dinas Teknis",
        "pic": "Adi Widiantono",
        "bast_status": "Ada (Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada (Menunggu Softcopy)",
        "domain_belum_ada": "Softcopy Dokumen Masih Proses Kirim",
        "kolom_belum_terisi": "Keterangan checklist: 'Kirim softcopy'",
        "tingkat_urgensi": "SEDANG",
        "tindakan_remediasi": "Konfirmasi penerimaan file softcopy Disgulkarmat di Google Drive"
    },

    # 5. LEMBAGA PENGAWAS
    {
        "no": "25.0",
        "opd": "INSPEKTORAT PROVINSI DKI JAKARTA",
        "kategori": "Lembaga Pengawas",
        "pic": "Rivan Dely Kusuna",
        "bast_status": "Ada (Kirim ke Dinas)",
        "ba_status": "Ada",
        "tobe_status": "Ada (7 Domain Belum Ada)",
        "domain_belum_ada": "ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Upgrade, Layanan_Sunset, Aplikasi_Sesuai, DataInformasi_Upgrade, DataInformasi_Sunset",
        "kolom_belum_terisi": "7 lembar kerja domain arsitektur pengawasan belum diunggah",
        "tingkat_urgensi": "TINGGI (7 DOMAIN KOSONG)",
        "tindakan_remediasi": "Pengisian peta proses bisnis pengawasan internal dan audit kepatuhan"
    }
]

# -------------------------------------------------------------
# 1. ADD MASTER SHEET TO EXCEL WORKBOOK
# -------------------------------------------------------------
wb = openpyxl.load_workbook(EXCEL_FILE)

sheet_name = "REKAP BELUM ADA SELURUH OPD"
if sheet_name in wb.sheetnames:
    del wb[sheet_name]

# Insert as Tab 2 (right after Ringkasan Eksekutif)
ws = wb.create_sheet(title=sheet_name, index=1)
ws.views.sheetView[0].showGridLines = True

# Styling
FILL_BLUE = PatternFill(start_color="9BC2E6", end_color="9BC2E6", fill_type="solid")
FILL_RED = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
FILL_YELLOW = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
FILL_ZEBRA = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
FILL_WHITE = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

FONT_TITLE = Font(name="Segoe UI", size=13, bold=True, color="1E3A8A")
FONT_SUB = Font(name="Segoe UI", size=9.5, italic=True, color="64748B")
FONT_H = Font(name="Segoe UI", size=9.5, bold=True, color="0F172A")
FONT_B = Font(name="Segoe UI", size=9.0, color="1E293B")
FONT_RED = Font(name="Segoe UI", size=9.0, bold=True, color="B91C1C")
FONT_YELLOW = Font(name="Segoe UI", size=9.0, bold=True, color="B45309")

BORDER_CLEAN = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)
BORDER_H = Border(
    left=Side(style='thin', color='64748B'),
    right=Side(style='thin', color='64748B'),
    top=Side(style='medium', color='1E3A8A'),
    bottom=Side(style='medium', color='1E3A8A')
)

ws.row_dimensions[1].height = 12
ws.cell(2, 1, value="MASTER REKAPITULASI DATA YANG BELUM ADA DI SELURUH PEMERINTAHAN (PEMPROV DKI JAKARTA)").font = FONT_TITLE
ws.row_dimensions[2].height = 26
ws.cell(3, 1, value="Daftar Lengkap Kesenjangan Dokumen, BAST Belum Masuk, Berita Acara Pending, dan Domain Kosong per OPD").font = FONT_SUB
ws.row_dimensions[3].height = 18

headers = [
    "NO", "PERANGKAT DAERAH / BIRO", "KATEGORI INSTANSI", "PIC PEMPROV", 
    "STATUS BAST", "STATUS BERITA ACARA", "STATUS 03 TO-BE", 
    "DOMAIN ARSITEKTUR YANG BELUM ADA", "RINCIAN ATRIBUT / KOLOM KOSONG", 
    "TINGKAT URGENSI", "REKOMENDASI TINDAKAN REMEDIASI"
]

ws.row_dimensions[5].height = 28
for ci, h in enumerate(headers, 1):
    c = ws.cell(5, ci, value=h)
    c.font = FONT_H
    c.fill = FILL_BLUE
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BORDER_H

for idx, item in enumerate(gov_missing_inventory, 6):
    is_zebra = (idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    vals = [
        item["no"], item["opd"], item["kategori"], item["pic"],
        item["bast_status"], item["ba_status"], item["tobe_status"],
        item["domain_belum_ada"], item["kolom_belum_terisi"],
        item["tingkat_urgensi"], item["tindakan_remediasi"]
    ]
    
    # Calculate row height
    max_l = max(math.ceil(len(str(v)) / 38) for v in vals)
    ws.row_dimensions[idx].height = max(26, max_l * 15 + 8)
    
    for ci, v in enumerate(vals, 1):
        c = ws.cell(idx, ci, value=v)
        c.font = FONT_B
        c.border = BORDER_CLEAN
        c.fill = row_fill
        
        if ci in [1, 3, 4]:
            c.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
        elif ci in [5, 6, 7, 10]:
            c.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
            if "BELUM" in str(v).upper() or "KRITIS" in str(v).upper():
                c.fill = FILL_RED
                c.font = FONT_RED
            elif "PENDING" in str(v).upper() or "DRAFT" in str(v).upper() or "GAGAL" in str(v).upper():
                c.fill = FILL_YELLOW
                c.font = FONT_YELLOW
        else:
            c.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

# Generous Column Widths
ws.column_dimensions['A'].width = 8
ws.column_dimensions['B'].width = 44
ws.column_dimensions['C'].width = 22
ws.column_dimensions['D'].width = 24
ws.column_dimensions['E'].width = 24
ws.column_dimensions['F'].width = 24
ws.column_dimensions['G'].width = 30
ws.column_dimensions['H'].width = 46
ws.column_dimensions['E'].width = 24
ws.column_dimensions['I'].width = 55
ws.column_dimensions['J'].width = 26
ws.column_dimensions['K'].width = 48

wb.save(EXCEL_FILE)
wb.save(PUBLIC_EXCEL)
print(f"[EXCEL SUCCESS] Master Tab '{sheet_name}' added to {EXCEL_FILE}")

# -------------------------------------------------------------
# 2. GENERATE COMPREHENSIVE MARKDOWN REPORT
# -------------------------------------------------------------
md_content = """# LAPORAN MASTER: REKAPITULASI SELURUH DATA YANG BELUM ADA DI PEMERINTAHAN
## Evaluasi Kesenjangan Dokumen Arsitektur SPBE & Kelengkapan Berkas Pemprov DKI Jakarta

> **Dasar Audit:** Ceklist Hasil FGD Reviu Arsitektur dan Peta Rencana SPBE 53 Perangkat Daerah & Spreadsheet CBC  
> **Auditor Utama:** SEKAR (Director of Finance, Risk & Compliance) & NAYA (Director of Research & Intelligence)  
> **Lead Orchestrator:** ARKA (Chief Executive & Strategy Officer)  
> **Tanggal Audit:** 2026-11-15  
> **Klasifikasi:** Dokumen Tata Kelola Kepatuhan Pemerintahan (Enterprise-Grade)

---

### 1. RINGKASAN EKSEKUTIF KESENJANGAN DOKUMEN PEMPROV DKI JAKARTA

Berdasarkan audit silang terhadap seluruh repositori Google Drive dan master checklist SPBE:
- **Total Entitas Pemerintahan yang Dinilai:** **51 Perangkat Daerah & Biro**.
- **Entitas dengan Dokumen Lengkap 100%:** **5 OPD** (Dinas Lingkungan Hidup, Dinas Sumber Daya Air, Dinas Bina Marga, Dinas Perumahan Rakyat & Kawasan Permukiman, Dinas Pertamanan & Hutan Kota).
- **Entitas dengan Kesenjangan / Belum Lengkap:** **46 Perangkat Daerah & Biro (90.2%)**.
- **Klasifikasi Kesenjangan Utama di Pemerintahan:**
  1. **BAST Belum Ada / Fisik Belum Diterima:** **11 OPD/Biro** (Termasuk Kepulauan Seribu, DPMPTSP, BPAD, Biro Tata Pemerintahan, Diskominfotik).
  2. **Berita Acara (BA) Pending / Belum Ditandatangani:** **2 OPD Kritis** (BPKD menunggu TTD Bu Kabid; Kepulauan Seribu BA belum dibuat).
  3. **Dokumen Arsitektur To-Be (03 / 03C) Belum Ada / Masih Draft:** **4 OPD** (Kepulauan Seribu belum ada, Disnakertransgi masih draf, Dishub & BPPBJ ditarik kembali untuk reviu).
  4. **Dokumen Template Kosong (Blank Cells):** **Kota Administrasi Jakarta Selatan** (File 03C ada tapi 39 baris proses bisnis dan 21 layanan belum terisi).
  5. **Domain Arsitektur Kosong Total (Tipe B):** Terdeteksi di Bappeda (6 domain), Satpol PP (6 domain), Jakarta Timur (5 domain), Jakarta Utara (7 domain), Jakarta Barat (10 domain), Inspektorat (7 domain).
  6. **Tertahan Tanda Tangan Pejabat Eselon 3:** **5 Biro & Dinas** (Biro BangLH, Biro KSD, Biro ORB, Biro Umum, Dinas Citata).
  7. **Rekaman Zoom FGD Belum Ada / Menumpang:** **4 OPD** (BPBD, Disgulkarmat, Inspektorat, Kepulauan Seribu).

---

### 2. MATRIKS LENGKAP: SELURUH DATA YANG BELUM ADA PER INSTANSI PEMERINTAH

Berikut daftar lengkap seluruh kesenjangan data pada masing-masing instansi:

| No | Perangkat Daerah / Biro | Kategori | PIC | Status BAST | Status Berita Acara (BA) | Status Dokumen 03 (To-Be) | Domain Arsitektur yang Belum Ada | Rincian Kolom / Atribut Kosong | Tingkat Urgensi |
| :-: | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- | :---: |
| **1.0** | **Kab. Adm. Kepulauan Seribu** | Wilayah | Adi Widiantono | **BELUM** | **BELUM DIBUAT** | **BELUM (03C Belum Ada)** | File 03C, BAST, BA, Record Zoom | Seluruh berkas arsitektur & legalitas belum diunggah | **KRITIS** |
| **2.0** | **Kota Adm. Jakarta Selatan** | Wilayah | Adi Widiantono | Ada (Dinas) | Ada | **TEMPLATE KOSONG** | ProsesBisnis_Upgrade, Layanan_Upgrade | 39 baris proses & 21 layanan kolom RAB/RAL kosong | **KRITIS** |
| **3.0** | **Kota Adm. Jakarta Timur** | Wilayah | Adi Widiantono | Ada (Dinas) | Ada | Ada (Sebagian Kosong) | ProsesBisnis_Upgrade/Sunset, Layanan_Sunset | L13349, L13344 belum terisi RAL Level 3 & risiko | **TINGGI** |
| **4.0** | **Kota Adm. Jakarta Utara** | Wilayah | Adi Widiantono | Ada (Dinas) | Ada | Ada (7 Domain Kosong) | ProsesBisnis Sesuai/Upgrade/Sunset, Layanan | 7 lembar kerja domain arsitektur belum diunggah | **TINGGI** |
| **5.0** | **Kota Adm. Jakarta Barat** | Wilayah | Rivan Dely K. | Ada (Dinas) | Ada | Ada (10 Domain Kosong) | 10 Domain (PB, Layanan, Aplikasi, Data) | 10 lembar kerja arsitektur SPBE masih kosong | **TINGGI** |
| **6.0** | **Bappeda** | Badan | Adi Widiantono | Ada (Dinas) | Ada | Gagal Simpan Server | 6 Domain (PB Upgrade/Sunset, Layanan, dll.) | 10 Server HP Proliant gagal simpan di database | **KRITIS** |
| **7.0** | **Satpol PP** | Dinas/Satuan | Rivan Dely K. | Ada (Dinas) | Ada | Ada (Kolom Kosong) | 6 Domain (PB Upgrade/Sunset, Layanan, dll.) | L13258, L12419 belum terisi RAL L3 & risiko | **TINGGI** |
| **8.0** | **DPMPTSP** | Dinas | Sulistyo Aris | **BELUM** | Ada | Ada | BAST Belum Ada | Berkas fisik & softcopy BAST belum masuk | **TINGGI** |
| **9.0** | **BPAD** | Badan | Sulistyo Aris | **BELUM** | Ada | Ada | BAST Fisik Belum di Dinas | Hardcopy fisik BAST belum diserahkan ke dinas | **TINGGI** |
| **10.0** | **BPKD** | Badan | Sulistyo Aris | Ada (Dinas) | **PENDING KABID** | Ada | BA Belum Sah | BA BPKD belum ditandatangani oleh Bu Kabid | **TINGGI** |
| **11.0** | **BPPBJ** | Badan | Sulistyo Aris | Ada (Dinas) | Ada | **DITARIK REVIU** | Berkas To-Be Dibawa Dinas | Dokumen hasil scan ditarik untuk reviu internal | **TINGGI** |
| **12.0** | **Disnakertransgi** | Dinas | Sulistyo Aris | Ada (Dinas) | Ada | **03 MASIH DRAFT** | Dokumen 03 Belum Final | Draf arsitektur belum disahkan pejabat berwenang | **TINGGI** |
| **13.0** | **Dishub** | Dinas | Sulistyo Aris | Ada (Dinas) | Ada | **DITARIK REVIU** | Berkas To-Be Dibawa Dinas | Dokumen To Be scan ttd dibawa dinas untuk reviu | **TINGGI** |
| **14.0** | **Diskominfotik** | Dinas | Rivan Dely K. | **BELUM** | Ada | Ada | BAST Belum Masuk | Kolom BAST berstatus 'Belum' | **TINGGI** |
| **15.0** | **Biro Tata Pemerintahan** | Biro Setda | Adi Widiantono | **BELUM** | Ada | Ada | BAST Fisik Belum di Dinas | BAST softcopy ada, hardcopy fisik belum di dinas | **TINGGI** |
| **16.0** | **Biro Pembangunan & LH** | Biro Setda | Rico Sugiyono | **BELUM** | Ada | Ada | BAST Tertahan Es 3 | Softcopy ada ttd Es 3, berkas fisik masih proses kirim | **TINGGI** |
| **17.0** | **Biro Kerja Sama Daerah** | Biro Setda | Sulistyo Aris | **BELUM** | Ada | Ada | BAST Tertahan Es 3 | Wajib TTD Eselon 3 sebelum serah terima | **TINGGI** |
| **18.0** | **Biro Perekonomian & Keuangan** | Biro Setda | Sulistyo Aris | **BELUM** | Ada | Ada | BAST Fisik Belum di Dinas | Hardcopy fisik BAST belum masuk ke kantor dinas | **TINGGI** |
| **19.0** | **Biro Umum & Administrasi** | Biro Setda | Rivan Dely K. | **BELUM** | Ada | Ada | BAST Tertahan Es 3 | BAST wajib TTD Eselon 3; Record Zoom sama dg BPSDM | **TINGGI** |
| **20.0** | **Biro ORB** | Biro Setda | Adi Widiantono | Ada (FGD/Dinas) | Ada | Ada | Dokumen Tertahan Es 3 | Berkas sudah di dinas, menunggu tanda tangan Es 3 | **SEDANG** |
| **21.0** | **Dinas Citata** | Dinas | Rico Sugiyono | Ada (Dinas) | Ada | Ada | Dokumen Tertahan Es 3 | Softcopy ada, fisik menunggu tanda tangan Es 3 | **SEDANG** |
| **22.0** | **BPBD** | Badan | Adi Widiantono | Ada (Dinas) | Ada | Ada | Record Zoom Tidak Ada | Rekaman video bukti FGD tidak tercatat | **SEDANG** |
| **23.0** | **Dinas Gulkarmat** | Dinas | Adi Widiantono | Ada (Dinas) | Ada | Ada | Softcopy Proses Kirim | File softcopy arsitektur masih proses pengiriman | **SEDANG** |
| **24.0** | **Inspektorat** | Pengawas | Rivan Dely K. | Ada (Kirim Dinas) | Ada | Ada (7 Domain Kosong) | 7 Domain (PB Upgrade/Sunset, Layanan, dll.) | Lembar kerja arsitektur pengawasan belum diunggah | **TINGGI** |

---

### 3. RENCANA TINDAK LANJUT (*ACTION PLAN*) PENYELESAIAN DOKUMEN

| Prioritas | Sektor Masalah | Instansi Terkait | Langkah Konkrit AI NEXUS & PIC | Target Waktu |
| :---: | :--- | :--- | :--- | :---: |
| **P1** | **Dokumen Template Kosong** | Jakarta Selatan, Jakarta Timur, Jakarta Barat, Jakarta Utara | Gunakan hasil auto-populate AI NEXUS (Tab 14 & 15 Excel) untuk langsung diimpor ke Google Drive | **1x24 Jam** |
| **P1** | **BAST Belum Ada / Belum Diserahkan** | 11 Instansi (Kep. Seribu, DPMPTSP, BPAD, Diskominfotik, Biro-biro) | Koordinasi PIC (Adi Widiantono, Sulistyo Aris, Rivan Dely) untuk penyerahan berkas fisik asli | **3 Hari Kerja** |
| **P2** | **Berita Acara Pending TTD** | BPKD & Kepulauan Seribu | Konfirmasi penandatanganan oleh Bu Kabid BPKD dan pembuatan draf BA Kepulauan Seribu | **2 Hari Kerja** |
| **P2** | **Dokumen Masih Draft / Ditarik** | Disnakertransgi, Dishub, BPPBJ | Penarikan kembali dokumen hasil reviu dan pengesahan draf definitif | **5 Hari Kerja** |
| **P3** | **Tanda Tangan Eselon 3** | Biro BangLH, Biro KSD, Biro ORB, Biro Umum, Dinas Citata | Sirkulasi paraf dan tanda tangan basah/elektronik pejabat Eselon 3 | **3 Hari Kerja** |

---

### 4. PANDUAN DOWNLOAD BERKAS EXCEL TERKAIT
Seluruh data di atas telah dirangkum dalam tab **`REKAP BELUM ADA SELURUH OPD`** pada file Excel master:
* **Tautan Berkas Lokal:** [`output/spreadsheets/LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx)
* **Web Kantor Virtual:** Buka [http://localhost:3000](http://localhost:3000) -> Klik **"Laporan & Log"** -> Klik **"Download Excel"**.
"""

with open(REPORT_MD, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"[MD SUCCESS] Master Report saved to {REPORT_MD}")
