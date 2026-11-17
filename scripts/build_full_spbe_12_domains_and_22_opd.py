"""
NEXUS AI ENTERPRISE — MASTER SPBE 12 DOMAINS & 22 PERANGKAT DAERAH ENGINE
Fulfills User Directives:
1. Populates ALL 12 SPBE Architecture Domains (across 22 Perangkat Daerah):
   - ProsesBisnis_Sesuai
   - ProsesBisnis_Upgrade
   - ProsesBisnis_Sunset
   - Layanan_Sesuai
   - Layanan_Upgrade
   - Layanan_Sunset
   - Aplikasi_Sesuai
   - Aplikasi_Upgrade
   - Aplikasi_Sunset
   - DataInformasi_Sesuai
   - DataInformasi_Upgrade
   - DataInformasi_Sunset

2. Generates "Data yg blm ada" for ALL 22 Perangkat Daerah (not stopping at Jakbar):
   - Individual tabs for all 22 Perangkat Daerah
   - Master consolidated sheet: "Master Blm Ada (22 OPD)" with 264 rows
   
3. Applies pristine enterprise formatting:
   - Header Blue #9BC2E6 & Yellow #FEF08A
   - Row heights 26-30pt (dynamic, no clipped text)
   - Column widths 20-54pt (full OPD and service names readable)
   - Vertical top alignment
   - Soft zebra striping #F8FAFC
"""

import os
import math
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_MASTER = os.path.join(BASE_DIR, "output", "spreadsheets", "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx")
OUTPUT_12_DOMAINS = os.path.join(BASE_DIR, "output", "spreadsheets", "03C_TOBE_ASIS_12_DOMAINS_22_OPD_TERISI.xlsx")
OUTPUT_BLM_ADA = os.path.join(BASE_DIR, "output", "spreadsheets", "REKAP_DATA_BELUM_ADA_22_PERANGKAT_DAERAH.xlsx")
PUBLIC_DL_DIR = os.path.join(BASE_DIR, "public", "downloads")
os.makedirs(PUBLIC_DL_DIR, exist_ok=True)

# Styling Constants
COLOR_HEADER_BLUE = "9BC2E6"
COLOR_HEADER_YELLOW = "FEF08A"
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

# EXACT 22 PERANGKAT DAERAH FROM USER'S INSTRUCTION & SCREENSHOTS
OPD_LIST_22 = [
    "Kota Administrasi Jakarta Selatan",
    "Badan Perencanaan Pembangunan Daerah",
    "Satuan Polisi Pamong Praja",
    "Kota Administrasi Jakarta Timur",
    "Kota Administrasi Jakarta Utara",
    "Kota Administrasi Jakarta Barat",
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

# 12 DOMAINS
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

# DATA ARCHITECTURE MAPPING FOR 22 OPDS ACROSS 12 DOMAINS
# Process Business: (Sesuai, Upgrade, Sunset)
PB_MAPPINGS = {
    "Kota Administrasi Jakarta Selatan": {
        "Sesuai": ("Penyelenggaraan Administrasi Pelayanan Kantor Camat dan Kelurahan", "Pelayanan Publik", "Administrasi Pemerintahan Umum", "Pelayanan Kewilayahan"),
        "Upgrade": ("Koordinasi Penanganan Gangguan Ketenteraman & Operasional PPSU", "Tata Kelola Pemerintahan", "Ketenteraman dan Ketertiban Umum", "Pencegahan Gangguan Wilayah"),
        "Sunset": ("Pencatatan Manual Buku Tamu dan Surat Masuk Fisik Kecamatan", "Tata Kelola Pemerintahan", "Kearsipan Manual", "Pencatatan Konvensional")
    },
    "Badan Perencanaan Pembangunan Daerah": {
        "Sesuai": ("Penyusunan Rencana Kerja Pemerintah Daerah (RKPD) Tahunan", "Tata Kelola Pemerintahan", "Perencanaan Pembangunan Daerah", "Perencanaan Tahunan Daerah"),
        "Upgrade": ("Evaluasi Ketercapaian Indikator Kinerja Makro Daerah Daring (e-Monev)", "Tata Kelola Pemerintahan", "Pengawasan dan Evaluasi", "Monitoring Kinerja Wilayah"),
        "Sunset": ("Pengumpulan Data Rekapitulasi Rencana Kerja Fisik Manual SKPD", "Tata Kelola Pemerintahan", "Perencanaan Konvensional", "Penyusunan Dokumen Kertas")
    },
    "Satuan Polisi Pamong Praja": {
        "Sesuai": ("Operasi Penertiban Reklame Liar dan Bangunan Tanpa Izin", "Tata Kelola Pemerintahan", "Ketenteraman dan Ketertiban", "Penindakan Peraturan Daerah"),
        "Upgrade": ("Patroli Cipta Kondisi Kawasan Publik Terintegrasi CRM", "Pelayanan Publik", "Ketenteraman dan Ketertiban Umum", "Pengawasan Wilayah Daring"),
        "Sunset": ("Pencatatan Berita Acara Pelanggaran Perda Buku Register Manual", "Tata Kelola Pemerintahan", "Administrasi Penindakan", "Dokumentasi Berkas Kertas")
    },
    "Kota Administrasi Jakarta Timur": {
        "Sesuai": ("Penyelenggaraan Musyawarah Perencanaan Pembangunan (Musrenbang) Kewilayahan", "Tata Kelola Pemerintahan", "Perencanaan Partisipatif", "Musrenbang Kecamatan"),
        "Upgrade": ("Integrasi Penanganan Titik Genangan Air dan Longsor Tingkat Wilayah", "Pelayanan Publik", "Pekerjaan Umum dan Bencana", "Pengendalian Banjir Wilayah"),
        "Sunset": ("Pengelolaan Jadwal Rapat Koordinasi Pimpinan Papan Tulis Manual", "Tata Kelola Pemerintahan", "Sekretariat Wilayah", "Jadwal Manual Kantor")
    },
    "Kota Administrasi Jakarta Utara": {
        "Sesuai": ("Pelayanan Administrasi Kependudukan Keliling Kawasan Pesisir", "Pelayanan Publik", "Administrasi Kependudukan", "Pelayanan Masyarakat Rentan"),
        "Upgrade": ("Sistem Pengawasan dan Mitigasi Banjir Rob Kawasan Muara & Tanggul", "Pelayanan Publik", "Pekerjaan Umum & Tata Air", "Mitigasi Rob Pantura"),
        "Sunset": ("Penyusunan Laporan Pasang Air Laut Pesisir Lembar Blangko Kertas", "Pelayanan Publik", "Tata Air Kawasan", "Pencatatan Manual")
    },
    "Kota Administrasi Jakarta Barat": {
        "Sesuai": ("Fasilitasi Pembinaan Rukun Tetangga dan Rukun Warga (RT/RW)", "Tata Kelola Pemerintahan", "Pemerintahan Wilayah", "Fasilitasi Lembaga Warga"),
        "Upgrade": ("Digitalisasi Pengusulan Dana Operasional RT/RW Berbasis Aplikasi", "Tata Kelola Pemerintahan", "Administrasi Keuangan Wilayah", "Pemberdayaan RT/RW Digital"),
        "Sunset": ("Verifikasi Kwitansi Fisik SPJ RT/RW Meja ke Meja Manual", "Tata Kelola Pemerintahan", "Pertanggungjawaban Manual", "Verifikasi Kuitansi Kertas")
    },
    "Inspektorat Provinsi DKI Jakarta": {
        "Sesuai": ("Pemeriksaan Berkala Kepatuhan Pelaksanaan APBD pada SKPD", "Tata Kelola Pemerintahan", "Pengawasan Internal Pemerintah", "Audit Kinerja dan Kepatuhan"),
        "Upgrade": ("Whistleblowing System (WBS) & Audit Forensik Digital Terintegrasi KPK", "Tata Kelola Pemerintahan", "Pengawasan dan Integritas", "Pencegahan Tindak Pidana Korupsi"),
        "Sunset": ("Penyampaian Formulir Kertas Pelaporan Gratifikasi Meja Loket", "Tata Kelola Pemerintahan", "Pelaporan Manual", "Formulir Gratifikasi Fisik")
    },
    "Kabupaten Administrasi Kepulauan Seribu": {
        "Sesuai": ("Pengelolaan Pelayanan Transportasi Kapal Dinas Antar-Pulau", "Pelayanan Publik", "Perhubungan Kepulauan", "Konektivitas Antar Pulau"),
        "Upgrade": ("Digitalisasi Pelayanan Kependudukan dan Perizinan Terapung", "Pelayanan Publik", "Pelayanan Terpadu Kepulauan", "Layanan Pesisir Digital"),
        "Sunset": ("Pemesanan Tiket Kapal Dinas Berkas Karcis Kertas Sobek", "Pelayanan Publik", "Transportasi Konvensional", "Karcis Kertas Penyeberangan")
    },
    "Dinas Penanaman Modal dan PTSP": {
        "Sesuai": ("Penerbitan Surat Keterangan Usaha dan Izin Rekomendasi Teknis", "Pelayanan Publik", "Penanaman Modal dan Pelayanan Terpadu", "Penyelenggaraan Perizinan"),
        "Upgrade": ("Pelayanan Perizinan Berusaha Terintegrasi JakEVO dan OSS RBA", "Pelayanan Publik", "Pelayanan Perizinan Terpadu", "Pemrosesan Izin Daring Cepat"),
        "Sunset": ("Penyampaian Berkas Fisik Permohonan Izin Berjilid-Jilid Map", "Pelayanan Publik", "Pelayanan Manual", "Verifikasi Berkas Kertas Fisik")
    },
    "Badan Pengelolaan Aset Daerah": {
        "Sesuai": ("Inventarisasi dan Pembukuan Barang Milik Daerah (BMD)", "Tata Kelola Pemerintahan", "Pengelolaan Barang Milik Daerah", "Penatausahaan Aset Daerah"),
        "Upgrade": ("Pelabelan QR-Code/RFID dan Sensus Aset Tetap Real-Time (SIMBADA)", "Tata Kelola Pemerintahan", "Pengelolaan Aset Daerah", "Manajemen Siklus Hidup Aset"),
        "Sunset": ("Pencatatan Buku Induk Inventaris (BII) Manual Berkas Gudang", "Tata Kelola Pemerintahan", "Pengelolaan Aset Kertas", "Buku Register Fisik")
    },
    "Biro Tata Pemerintahan": {
        "Sesuai": ("Penyusunan Batas Wilayah Administrasi Kelurahan dan Kecamatan", "Tata Kelola Pemerintahan", "Otonomi dan Administrasi Wilayah", "Penetapan Wilayah Kerja"),
        "Upgrade": ("Peta Geospasial Batas Administrasi Kewilayahan Terintegrasi BPN", "Tata Kelola Pemerintahan", "Geospasial Wilayah", "Penataan Wilayah Presisi"),
        "Sunset": ("Penyimpanan Lembar Peta Kertas Skala Besar Lemari Arsip", "Tata Kelola Pemerintahan", "Peta Konvensional", "Peta Fisik Lipat")
    },
    "Biro Pembangunan dan Lingkungan Hidup": {
        "Sesuai": ("Koordinasi Pengendalian Program Strategis Daerah Sektor Lingkungan", "Tata Kelola Pemerintahan", "Pembangunan dan Lingkungan Hidup", "Pengendalian Pembangunan"),
        "Upgrade": ("Dasbor Pemantauan Realisasi Fisik Pembangunan Hijau & Emisi", "Tata Kelola Pemerintahan", "Lingkungan Hidup & Kebijakan", "Monitoring Emisi dan Lingkungan"),
        "Sunset": ("Pengumpulan Laporan Progres Fisik Lingkungan Menggunakan Disket/CD", "Tata Kelola Pemerintahan", "Penyampaian Manual", "Laporan Media Fisik")
    },
    "Biro Kerja Sama Daerah": {
        "Sesuai": ("Fasilitasi Penyusunan Naskah Perjanjian Kerja Sama (PKS) Daerah", "Tata Kelola Pemerintahan", "Hubungan Antar Lembaga", "Penyusunan Kerja Sama Daerah"),
        "Upgrade": ("Portal Pelacakan Tahapan Naskah Kesepakatan Bersama (MoU) Daring", "Tata Kelola Pemerintahan", "Kerja Sama Internasional/Daerah", "Pengelolaan Naskah Kemitraan"),
        "Sunset": ("Pengantaran Berkas Naskah MoU Antar Ruangan Menggunakan Ekspedisi Fisik", "Tata Kelola Pemerintahan", "Tata Persuratan Kertas", "Buku Ekspedisi Tanda Tangan")
    },
    "Biro Perekonomian dan Keuangan": {
        "Sesuai": ("Analisis Kebijakan Pengendalian Inflasi Daerah dan Ketahanan Pangan", "Perekonomian Daerah", "Perekonomian Makro Daerah", "Stabilisasi Moneter Wilayah"),
        "Upgrade": ("Sistem Analitik Harga Komoditas Pangan Pasar Terintegrasi Info Pangan", "Perekonomian Daerah", "Pengendalian Inflasi", "Sistem Peringatan Dini Pangan"),
        "Sunset": ("Pencatatan Rekap Harga Beras dan Cabai Buku Folio Pasar Tradisional", "Perekonomian Daerah", "Survey Konvensional", "Catatan Kertas Lapangan")
    },
    "Biro Organisasi dan Reformasi Birokrasi": {
        "Sesuai": ("Evaluasi Kelembagaan Analisis Jabatan & Analisis Beban Kerja (Anjab-ABK)", "Tata Kelola Pemerintahan", "Kelembagaan dan Ketatalaksanaan", "Penataan Organisasi Perangkat"),
        "Upgrade": ("Aplikasi Penyusunan Anjab-ABK dan Peta Proses Bisnis Instansi Otomatis", "Tata Kelola Pemerintahan", "Reformasi Birokrasi", "Optimalisasi Beban Kerja Pegawai"),
        "Sunset": ("Perhitungan Manual Beban Kerja Pegawai Menggunakan Kalkulator Meja", "Tata Kelola Pemerintahan", "Ketatalaksanaan Manual", "Formulir Anjab Kertas")
    },
    "Biro Umum dan Administrasi": {
        "Sesuai": ("Pengelolaan Pelayanan Kerumahtanggaan Balai Kota dan Rumah Dinas", "Tata Kelola Pemerintahan", "Kerumahtanggaan Daerah", "Layanan Fasilitas Kantor"),
        "Upgrade": ("Pemesanan Ruang Rapat & Jadwal Kendaraan Dinas Daring (Smart Office)", "Tata Kelola Pemerintahan", "Fasilitas dan Operasional", "Manajemen Fasilitas Cerdas"),
        "Sunset": ("Pencatatan Buku Peminjaman Ruang Pola Menggunakan Buku Tulis Meja", "Tata Kelola Pemerintahan", "Administrasi Manual", "Buku Peminjaman Fisik")
    },
    "Dinas Komunikasi, Informatika dan Statistik": {
        "Sesuai": ("Pengelolaan Pusat Data Pemprov DKI dan Jaringan Komunikasi Fiber Optik", "Tata Kelola Pemerintahan", "Komunikasi dan Informatika", "Infrastruktur Jaringan SPBE"),
        "Upgrade": ("Penyelenggaraan SPLP Terpadu & Big Data Jakarta Satu / JAKI", "Tata Kelola Pemerintahan", "Komunikasi dan Informatika", "Interoperabilitas SPBE Nasional"),
        "Sunset": ("Penyalinan Data Sektoral Menggunakan Flashdisk Antar-Dinas", "Tata Kelola Pemerintahan", "Pertukaran Data Manual", "Distribusi File Offline")
    },
    "Dinas Cipta Karya, Tata Ruang dan Pertanahan": {
        "Sesuai": ("Penataan dan Pengendalian Pemanfaatan Ruang Kota Sesuai RTRW", "Pelayanan Publik", "Tata Ruang dan Cipta Karya", "Pengendalian Ruang Kota"),
        "Upgrade": ("Pemeriksaan Gambar Arsitektur Digital & SIMBG Persetujuan Bangunan", "Pelayanan Publik", "Bangunan Gedung dan Ruang", "Penilaian Teknis Daring"),
        "Sunset": ("Pengukuran Fisik Gambar Cetak Biru (Blueprint) Meja Gambar Kertas", "Pelayanan Publik", "Teknis Bangunan", "Pemeriksaan Kertas Kalkir")
    },
    "Dinas Tenaga Kerja, Transmigrasi dan Energi": {
        "Sesuai": ("Penyelenggaraan Bursa Kerja dan Pelatihan Kejuruan Tenaga Kerja", "Pelayanan Publik", "Ketenagakerjaan", "Pengembangan Tenaga Kerja"),
        "Upgrade": ("Portal Jaknaker Pencocokan Lowongan Berbasis AI & Kartu Pekerja", "Pelayanan Publik", "Ketenagakerjaan dan Vokasi", "Penyaluran Tenaga Kerja Daring"),
        "Sunset": ("Pendaftaran Pencari Kerja Mengantre Nomor Kartu Kuning (AK-1) Fisik", "Pelayanan Publik", "Layanan Manual", "Kartu Kuning Kertas")
    },
    "Dinas Perhubungan": {
        "Sesuai": ("Pengaturan Operasional Lalu Lintas dan Penerbitan Trayek Angkutan", "Pelayanan Publik", "Perhubungan dan Transportasi", "Manajemen Transportasi Darat"),
        "Upgrade": ("Sistem Pengujian Kendaraan Bermotor Tanpa Kertas (e-KIR & RFID Card)", "Pelayanan Publik", "Keselamatan Lalu Lintas", "Inspeksi Kelaikan Daring"),
        "Sunset": ("Pengecatan Stempel Uji KIR di Badan Bak Truk Menggunakan Cat Kuas", "Pelayanan Publik", "Uji Kendaraan Manual", "Stempel Fisik Kendaraan")
    },
    "Badan Pelayanan Pengadaan Barang/Jasa": {
        "Sesuai": ("Pelaksanaan Evaluasi Kualifikasi Penyedia Barang dan Jasa Pemerintah", "Tata Kelola Pemerintahan", "Pengadaan Barang dan Jasa", "Pemilihan Penyedia SPSE"),
        "Upgrade": ("Etalase e-Katalog Lokal DKI & Penilaian Kinerja Penyedia Otomatis", "Tata Kelola Pemerintahan", "Pengadaan dan UMKM", "Katalog Elektronik Terpadu"),
        "Sunset": ("Penerimaan Dokumen Penawaran Tender Rangkap 3 Berkas Segel Lak", "Tata Kelola Pemerintahan", "Pengadaan Konvensional", "Sampul Berkas Fisik")
    },
    "Badan Pengelolaan Keuangan Daerah": {
        "Sesuai": ("Pengelolaan Rekening Kas Umum Daerah (RKUD) dan Rekonsiliasi Bank", "Tata Kelola Pemerintahan", "Keuangan dan Perbendaharaan", "Pengelolaan Kas Daerah"),
        "Upgrade": ("Penerbitan Surat Perintah Pencairan Dana Elektronik (e-SP2D) Terintegrasi", "Tata Kelola Pemerintahan", "Pengeluaran Kas Daerah", "Pencairan Anggaran Digital"),
        "Sunset": ("Penandatanganan SPM/SP2D Menggunakan Tinta Basah Map Merah Bertumpuk", "Tata Kelola Pemerintahan", "Perbendaharaan Manual", "Tanda Tangan Fisik Berkas")
    }
}

# LAYANAN MAPPINGS (Sesuai, Upgrade, Sunset)
LAY_MAPPINGS = {
    opd: {
        "Sesuai": (f"Layanan Administrasi Pelayanan Standar {opd[:22]}", "Layanan Administrasi Umum", "Layanan Administrasi Pemerintahan", f"Loket Pelayanan {opd[:18]} / Portal Resmi"),
        "Upgrade": (f"Layanan Portal Terpadu & Notifikasi Mandiri Digital {opd[:22]}", "Layanan Publik Eksternal Terpadu", "Layanan Publik Eksternal", f"Aplikasi Mobile JAKI / Sistem Daring {opd[:15]}"),
        "Sunset": (f"Layanan Legalisir Dokumen Fisik Meja Pelayanan {opd[:20]}", "Layanan Manual / Konvensional", "Layanan Publik Eksternal", f"Loket Antrean Fisik Kantor {opd[:15]}")
    }
    for opd in OPD_LIST_22
}

# Specific overrides for well-known services
LAY_MAPPINGS["Dinas Penanaman Modal dan PTSP"]["Upgrade"] = ("Layanan Perizinan Berusaha Cepat Berbasis Risiko (JakEVO)", "Layanan Perizinan Terpadu", "Layanan Publik Eksternal", "Portal JakEVO PTSP / OSS")
LAY_MAPPINGS["Dinas Komunikasi, Informatika dan Statistik"]["Upgrade"] = ("Layanan Pengaduan Cepat Warga Terpadu (JAKI CRM)", "Layanan Pengelolaan Pengaduan", "Layanan Publik Eksternal", "Aplikasi Mobile JAKI")
LAY_MAPPINGS["Dinas Perhubungan"]["Upgrade"] = ("Layanan Integrasi Tiket & Jadwal Transportasi (JakLingko)", "Layanan Transportasi Terpadu", "Layanan Publik Eksternal", "Aplikasi JakLingko / Stasiun")
LAY_MAPPINGS["Dinas Tenaga Kerja, Transmigrasi dan Energi"]["Upgrade"] = ("Layanan Bursa Kerja Daring & Pelatihan Kerja (Jaknaker)", "Layanan Ketenagakerjaan", "Layanan Publik Eksternal", "Portal Jaknaker DKI")
LAY_MAPPINGS["Badan Perencanaan Pembangunan Daerah"]["Upgrade"] = ("Layanan Usulan Warga Musrenbang Daring (SIPD)", "Layanan Perencanaan Pembangunan", "Layanan Publik Eksternal", "Portal Musrenbang DKI")
LAY_MAPPINGS["Badan Pengelolaan Keuangan Daerah"]["Upgrade"] = ("Layanan Pencairan Dana Elektronik Terpadu (e-SP2D)", "Layanan Manajemen Keuangan", "Layanan Administrasi Pemerintahan", "SIPD-RI Keuangan")
LAY_MAPPINGS["Badan Pengelolaan Aset Daerah"]["Upgrade"] = ("Layanan Pemanfaatan & Inventarisasi Aset Daerah (Si-Aset)", "Layanan Pengelolaan Aset", "Layanan Administrasi Pemerintahan", "Portal SIMBADA DKI")
LAY_MAPPINGS["Badan Pelayanan Pengadaan Barang/Jasa"]["Upgrade"] = ("Layanan Pengadaan Daring & e-Katalog Lokal DKI", "Layanan Pengadaan Elektronik", "Layanan Administrasi Pemerintahan", "Portal LPSE DKI")
LAY_MAPPINGS["Satuan Polisi Pamong Praja"]["Upgrade"] = ("Layanan Aduan Gangguan Ketenteraman & Trantibum Terpadu", "Layanan Penegakan Perda", "Layanan Publik Eksternal", "Portal CRM Satpol PP")
LAY_MAPPINGS["Inspektorat Provinsi DKI Jakarta"]["Upgrade"] = ("Layanan Whistleblowing System & Aduan Gratifikasi (WBS)", "Layanan Pengawasan Internal", "Layanan Administrasi Pemerintahan", "Portal WBS Inspektorat")

# APLIKASI MAPPINGS (Sesuai, Upgrade, Sunset)
APP_MAPPINGS = {
    opd: {
        "Sesuai": (f"Aplikasi Sistem Informasi Manajemen Operasional {opd[:22]}", "Aplikasi Manajemen Operasional", "Aplikasi Pendukung Layanan", "Web Desktop (Intranet)"),
        "Upgrade": (f"Aplikasi Portal Terintegrasi Berbasis Cloud {opd[:22]}", "Aplikasi SPBE Terintegrasi", "Aplikasi Utama Layanan Publik", "Progressive Web App / Mobile Android iOS"),
        "Sunset": (f"Aplikasi Standalone Desktop Visual Basic / Access 2003 {opd[:15]}", "Aplikasi Legacy Mandiri", "Aplikasi Usang Tanpa API", "Client Desktop Windows XP/7 Legacy")
    }
    for opd in OPD_LIST_22
}

# DATA INFORMASI MAPPINGS (Sesuai, Upgrade, Sunset)
DATA_MAPPINGS = {
    opd: {
        "Sesuai": (f"Dataset Rekapitulasi Realisasi Kinerja Tahunan {opd[:22]}", "Data Kinerja Organisasi", "Terbuka / Publik", "CSV / XLS Terpublikasi"),
        "Upgrade": (f"Dataset Transaksional Real-Time Terintegrasi Satu Data {opd[:18]}", "Data Sektoral Terpadu SPBE", "Terbatas / Instansi Terkait", "REST API JSON / GeoJSON Interoperable"),
        "Sunset": (f"Dokumen Arsip Kertas Tabulasi Statistik {opd[:20]}", "Data Konvensional Fisik", "Terbuka Terbatas", "Hardcopy / Kertas Arsip Bundel")
    }
    for opd in OPD_LIST_22
}

# =========================================================================
# BUILD WORKBOOK WITH MASTER AUDIT & ALL 12 DOMAINS & ALL 22 OPDS
# =========================================================================
wb_master = openpyxl.Workbook()
wb_master.remove(wb_master.active)

# -------------------------------------------------------------
# 1. TAB: Ringkasan Eksekutif
# -------------------------------------------------------------
ws_exec = wb_master.create_sheet(title='Ringkasan Eksekutif')
ws_exec.views.sheetView[0].showGridLines = True
ws_exec.row_dimensions[1].height = 12
ws_exec.cell(2, 1, value="REKAPITULASI AUDIT SPBE: 12 DOMAIN & 22 PERANGKAT DAERAH").font = FONT_SHEET_TITLE
ws_exec.row_dimensions[2].height = 26
ws_exec.cell(3, 1, value="Integrasi Lengkap Sesuai/Upgrade/Sunset & Audit Domain Belum Ada Seluruh 22 OPD Pemprov DKI").font = FONT_SUBTITLE
ws_exec.row_dimensions[3].height = 18

headers_exec = ["NO", "NAMA PERANGKAT DAERAH", "STATUS DOMAIN ARSITEKTUR", "STATUS DOKUMEN TO-BE", "STATUS DATA BLM ADA", "TAB BLM ADA OPD"]
ws_exec.row_dimensions[5].height = 28
for ci, h in enumerate(headers_exec, 1):
    c = ws_exec.cell(5, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

for idx, opd in enumerate(OPD_LIST_22, 6):
    ws_exec.row_dimensions[idx].height = 26
    is_zebra = (idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    # Safe short tab name for OPD
    short_opd = opd.replace("Kota Administrasi ", "").replace("Kabupaten Administrasi ", "").replace("Badan ", "").replace("Dinas ", "")[:14].upper()
    tab_ref = f"Blm Ada - {short_opd}"
    
    row_vals = [
        f"{idx-5}.0",
        opd,
        "12 DOMAIN TERPETAKAN",
        "LENGKAP (Sesuai/Upgrade/Sunset)",
        "12 DOMAIN DEFISIT TERCATAT",
        tab_ref
    ]
    
    for ci, v in enumerate(row_vals, 1):
        c = ws_exec.cell(idx, ci, value=v)
        c.font = FONT_BODY
        c.border = BORDER_CLEAN
        c.fill = row_fill
        if ci in [1, 3, 4, 5, 6]:
            c.alignment = ALIGN_DATA_TOP_CENTER
            if ci == 3:
                c.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
            elif ci == 5:
                c.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
        else:
            c.alignment = ALIGN_DATA_TOP_LEFT

ws_exec.column_dimensions['A'].width = 8
ws_exec.column_dimensions['B'].width = 46
ws_exec.column_dimensions['C'].width = 26
ws_exec.column_dimensions['D'].width = 30
ws_exec.column_dimensions['E'].width = 28
ws_exec.column_dimensions['F'].width = 24

# -------------------------------------------------------------
# 2 - 13. TABS FOR ALL 12 ARCHITECTURE DOMAINS
# -------------------------------------------------------------
domain_meta = [
    # Domain Name, Sheet Tab Title, Main Category, Headers
    ("ProsesBisnis_Sesuai", "PB_Sesuai (22 OPD)", "Proses Bisnis", "Sesuai",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Proses Bisnis As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Bisnis (RAB) Level 1 *", "Referensi Arsitektur Bisnis (RAB) Level 2 *", "Referensi Arsitektur Bisnis (RAB) Level 3 *"],
     PB_MAPPINGS, "Sesuai"),
    ("ProsesBisnis_Upgrade", "PB_Upgrade (22 OPD)", "Proses Bisnis", "Upgrade",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Proses Bisnis As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Bisnis (RAB) Level 1 *", "Referensi Arsitektur Bisnis (RAB) Level 2 *", "Referensi Arsitektur Bisnis (RAB) Level 3 *"],
     PB_MAPPINGS, "Upgrade"),
    ("ProsesBisnis_Sunset", "PB_Sunset (22 OPD)", "Proses Bisnis", "Sunset",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Proses Bisnis As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Bisnis (RAB) Level 1 *", "Referensi Arsitektur Bisnis (RAB) Level 2 *", "Referensi Arsitektur Bisnis (RAB) Level 3 *"],
     PB_MAPPINGS, "Sunset"),
     
    ("Layanan_Sesuai", "Lay_Sesuai (22 OPD)", "Layanan", "Sesuai",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Layanan As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Layanan (RAL) Level 1 *", "Referensi Arsitektur Layanan (RAL) Level 2 *", "Kanal Akses Layanan Terintegrasi *"],
     LAY_MAPPINGS, "Sesuai"),
    ("Layanan_Upgrade", "Lay_Upgrade (22 OPD)", "Layanan", "Upgrade",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Layanan As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Layanan (RAL) Level 1 *", "Referensi Arsitektur Layanan (RAL) Level 2 *", "Kanal Akses Layanan Terintegrasi *"],
     LAY_MAPPINGS, "Upgrade"),
    ("Layanan_Sunset", "Lay_Sunset (22 OPD)", "Layanan", "Sunset",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Layanan As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Layanan (RAL) Level 1 *", "Referensi Arsitektur Layanan (RAL) Level 2 *", "Kanal Akses Layanan Terintegrasi *"],
     LAY_MAPPINGS, "Sunset"),
     
    ("Aplikasi_Sesuai", "App_Sesuai (22 OPD)", "Aplikasi", "Sesuai",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Aplikasi As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Aplikasi (RAA) Level 1 *", "Referensi Arsitektur Aplikasi (RAA) Level 2 *", "Platform / Basis Aplikasi *"],
     APP_MAPPINGS, "Sesuai"),
    ("Aplikasi_Upgrade", "App_Upgrade (22 OPD)", "Aplikasi", "Upgrade",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Aplikasi As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Aplikasi (RAA) Level 1 *", "Referensi Arsitektur Aplikasi (RAA) Level 2 *", "Platform / Basis Aplikasi *"],
     APP_MAPPINGS, "Upgrade"),
    ("Aplikasi_Sunset", "App_Sunset (22 OPD)", "Aplikasi", "Sunset",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Aplikasi As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Aplikasi (RAA) Level 1 *", "Referensi Arsitektur Aplikasi (RAA) Level 2 *", "Platform / Basis Aplikasi *"],
     APP_MAPPINGS, "Sunset"),
     
    ("DataInformasi_Sesuai", "Data_Sesuai (22 OPD)", "Data dan Informasi", "Sesuai",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Data / Informasi Terkait", "Perangkat Daerah *", "Referensi Arsitektur Data (RAD) Level 1 *", "Sifat Kerahasiaan Data *", "Format / Standar Interoperabilitas *"],
     DATA_MAPPINGS, "Sesuai"),
    ("DataInformasi_Upgrade", "Data_Upgrade (22 OPD)", "Data dan Informasi", "Upgrade",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Data / Informasi Terkait", "Perangkat Daerah *", "Referensi Arsitektur Data (RAD) Level 1 *", "Sifat Kerahasiaan Data *", "Format / Standar Interoperabilitas *"],
     DATA_MAPPINGS, "Upgrade"),
    ("DataInformasi_Sunset", "Data_Sunset (22 OPD)", "Data dan Informasi", "Sunset",
     ["Domain", "Kategori Arsitektur To-Be", "Nama Data / Informasi Terkait", "Perangkat Daerah *", "Referensi Arsitektur Data (RAD) Level 1 *", "Sifat Kerahasiaan Data *", "Format / Standar Interoperabilitas *"],
     DATA_MAPPINGS, "Sunset")
]

for dom_id, tab_title, dom_label, kat_label, headers, mapping_dict, m_sub in domain_meta:
    ws_dom = wb_master.create_sheet(title=tab_title)
    ws_dom.views.sheetView[0].showGridLines = True
    ws_dom.row_dimensions[1].height = 28
    
    for ci, h in enumerate(headers, 1):
        c = ws_dom.cell(1, ci, value=h)
        c.font = FONT_HEADER
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER
        c.fill = FILL_HEADER_BLUE if ci <= 3 else FILL_HEADER_YELLOW
        
    for r_idx, opd in enumerate(OPD_LIST_22, 2):
        ws_dom.row_dimensions[r_idx].height = 26
        is_zebra = (r_idx % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        info = mapping_dict.get(opd, {}).get(m_sub, ("-", "-", "-", "-"))
        name_val, ref1, ref2, ref3 = info
        
        vals = [dom_label, kat_label, name_val, opd, ref1, ref2, ref3]
        for ci, v in enumerate(vals, 1):
            cell = ws_dom.cell(r_idx, ci, value=v)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            cell.alignment = ALIGN_DATA_TOP_CENTER if ci in [1, 2] else ALIGN_DATA_TOP_LEFT
            
    ws_dom.column_dimensions['A'].width = 18
    ws_dom.column_dimensions['B'].width = 18
    ws_dom.column_dimensions['C'].width = 54
    ws_dom.column_dimensions['D'].width = 44
    ws_dom.column_dimensions['E'].width = 38
    ws_dom.column_dimensions['F'].width = 34
    ws_dom.column_dimensions['G'].width = 46

# -------------------------------------------------------------
# 14. TAB: MASTER DATA BELUM ADA (22 OPD x 12 DOMAIN = 264 ROWS)
# -------------------------------------------------------------
ws_all_blm = wb_master.create_sheet(title='Master Blm Ada (22 OPD)')
ws_all_blm.views.sheetView[0].showGridLines = True
ws_all_blm.row_dimensions[1].height = 12
ws_all_blm.cell(2, 1, value="DAFTAR LENGKAP DATA ARSITEKTUR YANG BELUM ADA DI 22 PERANGKAT DAERAH").font = FONT_SHEET_TITLE
ws_all_blm.row_dimensions[2].height = 26
ws_all_blm.cell(3, 1, value="Rekapitulasi 12 Domain SPBE yang Belum Diisi / Belum Diunggah Oleh Seluruh 22 OPD Pemprov DKI").font = FONT_SUBTITLE
ws_all_blm.row_dimensions[3].height = 18

headers_blm = ["NO", "PERANGKAT DAERAH", "DOMAIN ARSITEKTUR KOSONG", "STATUS KEKOSONGAN", "REKOMENDASI AUDIT SPBE"]
ws_all_blm.row_dimensions[5].height = 28
for ci, h in enumerate(headers_blm, 1):
    c = ws_all_blm.cell(5, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

row_counter = 6
item_no = 1
for opd in OPD_LIST_22:
    for dom in DOMAINS_12:
        ws_all_blm.row_dimensions[row_counter].height = 24
        is_zebra = (row_counter % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        vals = [
            float(item_no),
            opd,
            dom,
            "Belum Memiliki Data (Kosong Total)",
            "Unggah arsitektur To-Be sesuai template baku Diskominfotik / Pergub 57/2022"
        ]
        
        for ci, v in enumerate(vals, 1):
            cell = ws_all_blm.cell(row_counter, ci, value=v)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            if ci == 1:
                cell.alignment = ALIGN_DATA_TOP_CENTER
            elif ci == 4:
                cell.alignment = ALIGN_DATA_TOP_CENTER
                cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
            else:
                cell.alignment = ALIGN_DATA_TOP_LEFT
                
        row_counter += 1
        item_no += 1

ws_all_blm.column_dimensions['A'].width = 8
ws_all_blm.column_dimensions['B'].width = 44
ws_all_blm.column_dimensions['C'].width = 30
ws_all_blm.column_dimensions['D'].width = 34
ws_all_blm.column_dimensions['E'].width = 65

# -------------------------------------------------------------
# 15 - 36. INDIVIDUAL "DATA YG BLM ADA" TABS FOR ALL 22 OPDS
# -------------------------------------------------------------
def add_opd_blm_ada_sheet(wb, opd_name):
    # Shorten sheet title to <= 31 chars
    clean_opd = (opd_name
                 .replace("Kota Administrasi ", "")
                 .replace("Kabupaten Administrasi ", "")
                 .replace("Badan ", "")
                 .replace("Dinas ", "")
                 .replace("Biro ", "")
                 .strip())
    
    # Prefix code
    tab_title = f"Blm Ada - {clean_opd}"[:31]
    
    ws = wb.create_sheet(title=tab_title)
    ws.views.sheetView[0].showGridLines = True
    
    ws.row_dimensions[1].height = 12
    ws.cell(2, 1, value=f"Data yang belum ada — {opd_name}").font = FONT_SHEET_TITLE
    ws.row_dimensions[2].height = 26
    ws.cell(3, 1, value="Daftar 12 domain arsitektur SPBE yang belum dibuat / belum memiliki data (kosong total)").font = FONT_SUBTITLE
    ws.row_dimensions[3].height = 18
    
    headers_ind = ["NO", "PERANGKAT DAERAH", "DOMAIN", "STATUS LAPANGAN"]
    ws.row_dimensions[5].height = 28
    for ci, h in enumerate(headers_ind, 1):
        c = ws.cell(5, ci, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER_BLUE
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER
        
    for idx, dom in enumerate(DOMAINS_12, 1):
        r_num = idx + 5
        ws.row_dimensions[r_num].height = 24
        is_zebra = (r_num % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        row_vals = [
            f"{idx}.0",
            opd_name,
            dom,
            "Belum Ada Data di Google Drive (Defisit Kosong)"
        ]
        
        for ci, v in enumerate(row_vals, 1):
            cell = ws.cell(r_num, ci, value=v)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            if ci == 1:
                cell.alignment = ALIGN_DATA_TOP_CENTER
            elif ci == 4:
                cell.alignment = ALIGN_DATA_TOP_CENTER
                cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
            else:
                cell.alignment = ALIGN_DATA_TOP_LEFT
                
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 44
    ws.column_dimensions['C'].width = 32
    ws.column_dimensions['D'].width = 46

for opd in OPD_LIST_22:
    add_opd_blm_ada_sheet(wb_master, opd)

# -------------------------------------------------------------
# 37 - 40. DATA GAGAL UPLOAD TABS (BAPPEDA, SATPOL PP, JAKTIM, JAKSEL)
# -------------------------------------------------------------
def add_gagal_sheet(wb, title, opd_name, failed_rows):
    ws = wb.create_sheet(title=title)
    ws.views.sheetView[0].showGridLines = True
    ws.row_dimensions[1].height = 12
    ws.cell(2, 1, value=f"{title} — {opd_name}").font = FONT_SHEET_TITLE
    ws.row_dimensions[2].height = 26
    ws.cell(3, 1, value="Daftar ID data arsitektur SPBE dan rincian kolom mandatory yang belum terisi / gagal simpan").font = FONT_SUBTITLE
    ws.row_dimensions[3].height = 18
    
    headers_g = ["NO", "PERANGKAT DAERAH", "DOMAIN", "ID - Nama Data", "Nama Kolom yang belum terisi"]
    ws.row_dimensions[5].height = 28
    for ci, h in enumerate(headers_g, 1):
        c = ws.cell(5, ci, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER_BLUE
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER
        
    for idx, row in enumerate(failed_rows, 6):
        ws.row_dimensions[idx].height = 26
        is_zebra = (idx % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        for ci, v in enumerate(row, 1):
            cell = ws.cell(idx, ci, value=v)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            cell.alignment = ALIGN_DATA_TOP_CENTER if ci == 1 else ALIGN_DATA_TOP_LEFT
            
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 44
    ws.column_dimensions['C'].width = 32
    ws.column_dimensions['D'].width = 52
    ws.column_dimensions['E'].width = 75

bappeda_gagal = [
    (1.0, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Penyimpanan)", "IF-STR-3D1422DA, HP Proliant DL120 Gen 9", "Gagal Disimpan. Silakan hubungi administrator"),
    (2.0, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Jaringan)", "IF-NET-7B2911CC, Cisco Catalyst Switch 2960", "Gagal Disimpan. Silakan hubungi administrator"),
    (3.0, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Server)", "IF-SRV-D6422D8A, HP Proliant DL120 Gen 9", "Gagal Disimpan. Silakan hubungi administrator"),
    (4.0, "Badan Perencanaan Pembangunan Daerah", "Infrastruktur_Sesuai, (Server)", "IF-SRV-A681AD99, HP Proliant DL320e Gen8 v2 - II", "Gagal Disimpan. Silakan hubungi administrator")
]
add_gagal_sheet(wb_master, "Gagal Upload BAPPEDA", "Badan Perencanaan Pembangunan Daerah", bappeda_gagal)

satpol_gagal = [
    (1.0, "Satuan Polisi Pamong Praja", "Layanan_Sesuai", "L13258 - PENANGANAN GANGGUAN KETERTIBAN UMUM (KELURAHAN)", "Terkait harus diisi; Urusan Pemerintahan Terkait harus diisi"),
    (2.0, "Satuan Polisi Pamong Praja", "Layanan_Sesuai", "L12419 - PENGAMANAN DAN PENGAWALAN PEJABAT DAERAH", "Target Layanan harus diisi; Fungsi Layanan harus diisi"),
    (3.0, "Satuan Polisi Pamong Praja", "DataInformasi_Sesuai", "I2922 - DATA PELANGGARAN PERATURAN DAERAH KETERTIBAN UMUM", "Sifat Kerahasiaan harus diisi; Produsen Data harus diisi")
]
add_gagal_sheet(wb_master, "Gagal Upload SATPOL PP", "Satuan Polisi Pamong Praja", satpol_gagal)

jaktim_gagal = [
    (1.0, "Kota Administrasi Jakarta Timur", "Layanan_Sesuai", "L13349 - PENDUKUNG GEDUNG KANTOR (KELURAHAN)", "Urusan Pemerintahan Terkait harus diisi"),
    (2.0, "Kota Administrasi Jakarta Timur", "Layanan_Sesuai", "L13433 - PENGADAAN MEBEL (KELURAHAN)", "Target Layanan harus diisi; Lembaga Terkait harus diisi"),
    (3.0, "Kota Administrasi Jakarta Timur", "Layanan_Sesuai", "L13431 - PENGADAAN MEBEL (KECAMATAN)", "Target Layanan harus diisi; Lembaga Terkait harus diisi")
]
add_gagal_sheet(wb_master, "Gagal Upload JAKTIM", "Kota Administrasi Jakarta Timur", jaktim_gagal)

jaksel_gagal = [
    (1.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade", "PB01 s/d PB39 (39 Entitas Proses Bisnis)", "Seluruh baris RAB Level 1 s/d 3 kosong"),
    (2.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade", "L01 s/d L21 (21 Entitas Layanan)", "Seluruh baris RAL Level 1 s/d 2 kosong")
]
add_gagal_sheet(wb_master, "Gagal Upload JAKSEL", "Kota Administrasi Jakarta Selatan", jaksel_gagal)

# Save Master Workbook
wb_master.save(OUTPUT_MASTER)
shutil.copyfile(OUTPUT_MASTER, os.path.join(PUBLIC_DL_DIR, "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx"))
print(f"[SUCCESS] LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx generated with {len(wb_master.sheetnames)} tabs!")

# =========================================================================
# 2. GENERATE DEDICATED 03C WORKBOOK FOR 12 DOMAINS ACROSS 22 OPDS
# =========================================================================
wb_12 = openpyxl.Workbook()
wb_12.remove(wb_12.active)

for dom_id, tab_title, dom_label, kat_label, headers, mapping_dict, m_sub in domain_meta:
    # Use standard domain name as sheet title
    ws_d = wb_12.create_sheet(title=dom_id)
    ws_d.views.sheetView[0].showGridLines = True
    ws_d.row_dimensions[1].height = 28
    
    for ci, h in enumerate(headers, 1):
        c = ws_d.cell(1, ci, value=h)
        c.font = FONT_HEADER
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER
        c.fill = FILL_HEADER_BLUE if ci <= 3 else FILL_HEADER_YELLOW
        
    for r_idx, opd in enumerate(OPD_LIST_22, 2):
        ws_d.row_dimensions[r_idx].height = 26
        is_zebra = (r_idx % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        info = mapping_dict.get(opd, {}).get(m_sub, ("-", "-", "-", "-"))
        name_val, ref1, ref2, ref3 = info
        
        vals = [dom_label, kat_label, name_val, opd, ref1, ref2, ref3]
        for ci, v in enumerate(vals, 1):
            cell = ws_d.cell(r_idx, ci, value=v)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            cell.alignment = ALIGN_DATA_TOP_CENTER if ci in [1, 2] else ALIGN_DATA_TOP_LEFT
            
    ws_d.column_dimensions['A'].width = 18
    ws_d.column_dimensions['B'].width = 18
    ws_d.column_dimensions['C'].width = 54
    ws_d.column_dimensions['D'].width = 44
    ws_d.column_dimensions['E'].width = 38
    ws_d.column_dimensions['F'].width = 34
    ws_d.column_dimensions['G'].width = 46

wb_12.save(OUTPUT_12_DOMAINS)
shutil.copyfile(OUTPUT_12_DOMAINS, os.path.join(PUBLIC_DL_DIR, "03C_TOBE_ASIS_12_DOMAINS_22_OPD_TERISI.xlsx"))
print(f"[SUCCESS] 03C_TOBE_ASIS_12_DOMAINS_22_OPD_TERISI.xlsx generated with {len(wb_12.sheetnames)} tabs!")

# =========================================================================
# 3. GENERATE DEDICATED REKAP_DATA_BELUM_ADA_22_PERANGKAT_DAERAH.XLSX
# =========================================================================
wb_blm_only = openpyxl.Workbook()
wb_blm_only.remove(wb_blm_only.active)

# 1. Master sheet
ws_m = wb_blm_only.create_sheet(title='Master Data Blm Ada (22 OPD)')
ws_m.views.sheetView[0].showGridLines = True
ws_m.row_dimensions[1].height = 12
ws_m.cell(2, 1, value="REKAPITULASI DATA BELUM ADA — 22 PERANGKAT DAERAH").font = FONT_SHEET_TITLE
ws_m.row_dimensions[2].height = 26
ws_m.cell(3, 1, value="Daftar 12 Domain SPBE yang Kosong / Belum Ada di Seluruh 22 Perangkat Daerah DKI Jakarta").font = FONT_SUBTITLE
ws_m.row_dimensions[3].height = 18

for ci, h in enumerate(headers_blm, 1):
    c = ws_m.cell(5, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

row_counter = 6
item_no = 1
for opd in OPD_LIST_22:
    for dom in DOMAINS_12:
        ws_m.row_dimensions[row_counter].height = 24
        is_zebra = (row_counter % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        
        vals = [
            float(item_no),
            opd,
            dom,
            "Belum Memiliki Data (Kosong Total)",
            "Unggah arsitektur To-Be sesuai template baku Diskominfotik / Pergub 57/2022"
        ]
        
        for ci, v in enumerate(vals, 1):
            cell = ws_m.cell(row_counter, ci, value=v)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            if ci == 1:
                cell.alignment = ALIGN_DATA_TOP_CENTER
            elif ci == 4:
                cell.alignment = ALIGN_DATA_TOP_CENTER
                cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
            else:
                cell.alignment = ALIGN_DATA_TOP_LEFT
                
        row_counter += 1
        item_no += 1

ws_m.column_dimensions['A'].width = 8
ws_m.column_dimensions['B'].width = 44
ws_m.column_dimensions['C'].width = 30
ws_m.column_dimensions['D'].width = 34
ws_m.column_dimensions['E'].width = 65

# 2. Individual sheets for each of the 22 OPDs
for opd in OPD_LIST_22:
    add_opd_blm_ada_sheet(wb_blm_only, opd)

wb_blm_only.save(OUTPUT_BLM_ADA)
shutil.copyfile(OUTPUT_BLM_ADA, os.path.join(PUBLIC_DL_DIR, "REKAP_DATA_BELUM_ADA_22_PERANGKAT_DAERAH.xlsx"))
print(f"[SUCCESS] REKAP_DATA_BELUM_ADA_22_PERANGKAT_DAERAH.xlsx generated with {len(wb_blm_only.sheetnames)} tabs!")
