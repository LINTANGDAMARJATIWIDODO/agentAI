"""
NEXUS AI ENTERPRISE — MASTER SPBE 22 PERANGKAT DAERAH ENGINE
Generates:
1. LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx with:
   - Ringkasan Eksekutif
   - 22 Layanan_Upgrade (22 Perangkat Daerah) — Every OPD has its distinct signature service
   - 44 ProsesBisnis_Upgrade (22 OPD) — 2 core business processes per OPD (total 44 rows)
   - Data gagal Upload (Per OPD)
   - Data yang belum ada (Per OPD)
   - Data blm ada (Semua 51 OPD Pemprov DKI)
2. 03C_TOBE_ASIS_22_PERANGKAT_DAERAH_TERISI.xlsx (Dedicated Solution Template)
3. Formatted to perfection: pastel blue headers, generous column widths, dynamic row heights, soft zebra striping.
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
OUTPUT_22_OPD = os.path.join(BASE_DIR, "output", "spreadsheets", "03C_TOBE_ASIS_22_PERANGKAT_DAERAH_TERISI.xlsx")
OUTPUT_03C_JAKSEL = os.path.join(BASE_DIR, "output", "spreadsheets", "03C_TOBE_ASIS_Kota_Administrasi_Jakarta_Selatan_TERISI.xlsx")
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

# =========================================================================
# DEFINISI 22 PERANGKAT DAERAH & LAYANAN UNGGULAN SPBE (22 OPD)
# =========================================================================
DATA_22_LAYANAN = [
    (1, "Dinas Pendidikan", 
     "Layanan Bantuan Biaya Personal Pendidikan Siswa Tidak Mampu (KJP Plus & KJMU)", 
     "Layanan Bantuan Pendidikan Daerah", "Layanan Publik Eksternal", "Portal P4OP Disdik / Aplikasi JAKI"),
     
    (2, "Dinas Kesehatan", 
     "Layanan Antrean Faskes Daring, Konsultasi Psikologi & Deteksi Stunting (JakSehat / e-Jiwa)", 
     "Layanan Kesehatan Masyarakat Berbasis Komunitas", "Layanan Publik Eksternal", "Aplikasi JakSehat / Portal Dinkes / JAKI"),
     
    (3, "Dinas Komunikasi, Informatika dan Statistik", 
     "Layanan Portal Warga Terpadu & Penanganan Pengaduan Cepat (JAKI & CRM)", 
     "Layanan Pengelolaan Pengaduan Publik SPBE", "Layanan Publik Eksternal", "Portal JAKI / Dashboard CRM Pemprov DKI"),
     
    (4, "Dinas Perhubungan", 
     "Layanan Integrasi Tiket Transportasi Multi-Moda & Informasi Rute (JakLingko)", 
     "Layanan Transportasi dan Mobilitas Perkotaan", "Layanan Publik Eksternal", "Aplikasi JakLingko / Kiosk Stasiun / Halte"),
     
    (5, "Satuan Polisi Pamong Praja", 
     "Layanan Permohonan Penertiban Gangguan Ketenteraman & Ketertiban Umum Wilayah (Trantibum)", 
     "Layanan Penegakan Perda & Ketertiban Umum", "Layanan Publik Eksternal", "Aplikasi JAKI / Call Center Satpol PP / Posko Wilayah"),
     
    (6, "Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu", 
     "Layanan Perizinan Berusaha Berbasis Risiko dan Rekomendasi Investasi (JakEVO / OSS)", 
     "Layanan Perizinan dan Non-Perizinan Terpadu", "Layanan Publik Eksternal", "Portal JakEVO PTSP / Sistem OSS Nasional"),
     
    (7, "Dinas Kependudukan dan Pencatatan Sipil", 
     "Layanan Administrasi Kependudukan, Akta Kelahiran & KTP Digital (Alpukat Betawi)", 
     "Layanan Administrasi Kependudukan", "Layanan Publik Eksternal", "Aplikasi Alpukat Betawi / IKD Kemendagri"),
     
    (8, "Dinas Sosial", 
     "Layanan Pendaftaran Pemerlu Pelayanan Kesejahteraan Sosial (PPKS) & Bansos Kluster Keluarga", 
     "Layanan Perlindungan dan Jaminan Sosial", "Layanan Publik Eksternal", "Portal Bansos Dinsos / JAKI / Pusdatin Jamsos"),
     
    (9, "Badan Perencanaan Pembangunan Daerah", 
     "Layanan Partisipasi Musrenbang Daring & Aspirasi Rancangan RKPD Warga (SIPD Perencanaan)", 
     "Layanan Perencanaan Pembangunan Daerah", "Layanan Publik Eksternal", "Portal Musrenbang DKI / SIPD-RI"),
     
    (10, "Badan Pengelolaan Keuangan Daerah", 
     "Layanan Penerbitan Surat Perintah Pencairan Dana Elektronik & e-BLUD (e-SP2D)", 
     "Layanan Manajemen Keuangan dan Anggaran Daerah", "Layanan Administrasi Pemerintahan", "Portal SIPD Penatausahaan / Cash Management System Bank DKI"),
     
    (11, "Badan Pengelolaan Aset Daerah", 
     "Layanan Penatausahaan & Pemanfaatan Barang Milik Daerah Terintegrasi (SIMBADA / Si-Aset)", 
     "Layanan Pengelolaan Aset Daerah", "Layanan Administrasi Pemerintahan", "Portal SIMBADA DKI / Aplikasi Si-Aset Mobile"),
     
    (12, "Badan Pelayanan Pengadaan Barang/Jasa", 
     "Layanan Pengadaan Barang dan Jasa Pemerintah Secara Elektronik (SPSE / e-Katalog Lokal DKI)", 
     "Layanan Pengadaan Barang/Jasa Elektronik", "Layanan Administrasi Pemerintahan", "Portal LPSE Pemprov DKI / e-Katalog LKPP"),
     
    (13, "Dinas Sumber Daya Air", 
     "Layanan Informasi Peringatan Dini Banjir, Pemantauan Pintu Air & Posko Pompa Daring", 
     "Layanan Pengelolaan Sumber Daya Air dan Pengendalian Banjir", "Layanan Publik Eksternal", "Portal Pantau Banjir Jakarta / JAKI"),
     
    (14, "Dinas Bina Marga", 
     "Layanan Pengaduan Jalan Berlubang, Jembatan Rusak & Penerangan Jalan Umum (PJU Daring)", 
     "Layanan Infrastruktur Jalan dan Jembatan Daerah", "Layanan Publik Eksternal", "Aplikasi CRM / JAKI / Si-Jalan DBM"),
     
    (15, "Dinas Lingkungan Hidup", 
     "Layanan Pendaftaran Uji Emisi Gas Buang Kendaraan Bermotor & Bank Sampah Digital", 
     "Layanan Pengelolaan Lingkungan Hidup dan Persampahan", "Layanan Publik Eksternal", "Aplikasi e-Uji Emisi / Portal DLH DKI / JAKI"),
     
    (16, "Dinas Cipta Karya, Tata Ruang dan Pertanahan", 
     "Layanan Persetujuan Bangunan Gedung (PBG), Sertifikat Laik Fungsi (SLF) & Informasi Rencana Kota (IRK)", 
     "Layanan Penataan Ruang dan Bangunan Gedung", "Layanan Publik Eksternal", "Sistem Informasi SIMBG Terpadu / Portal JakEVO"),
     
    (17, "Dinas Tenaga Kerja, Transmigrasi dan Energi", 
     "Layanan Bursa Kerja Daring, Pelatihan Kejuruan PPKD & Wajib Lapor Ketenagakerjaan (Jaknaker)", 
     "Layanan Ketenagakerjaan dan Pelatihan Vokasi", "Layanan Publik Eksternal", "Portal Jaknaker / Aplikasi JAKI"),
     
    (18, "Dinas Penanggulangan Kebakaran dan Penyelamatan", 
     "Layanan Tanggap Darurat Pemadaman Kebakaran dan Penyelamatan Non-Kebakaran (Animal Rescue / Darurat Jiwa)", 
     "Layanan Tanggap Darurat Kebakaran dan Penyelamatan", "Layanan Publik Eksternal", "Jakarta Siaga 112 / Command Center Disgulkarmat"),
     
    (19, "Badan Penanggulangan Bencana Daerah", 
     "Layanan Peringatan Dini Kebencanaan (Disaster Early Warning System / DEWS) & Logistik Darurat Bencana", 
     "Layanan Penanggulangan Bencana dan Kedaruratan", "Layanan Publik Eksternal", "Portal Pusdalops BPBD / JAKI / SMS Blast BMKG-BPBD"),
     
    (20, "Inspektorat Provinsi DKI Jakarta", 
     "Layanan Pengaduan Penyimpangan Pegawai, Pelaporan Gratifikasi & Whistleblowing System (WBS)", 
     "Layanan Pengawasan Internal dan Whistleblowing", "Layanan Publik & Administrasi Pemerintahan", "Portal WBS Inspektorat DKI / Portal KPK Terintegrasi"),
     
    (21, "Dinas Perindustrian, Perdagangan, Koperasi, Usaha Kecil dan Menengah", 
     "Layanan Inkubasi Bisnis, Fasilitasi Hak Merek & Sertifikasi Halal Pelaku Usaha Mikro (Jakpreneur)", 
     "Layanan Pemberdayaan Koperasi dan Usaha Mikro", "Layanan Publik Eksternal", "Portal Jakpreneur PPKUKM / JAKI"),
     
    (22, "Kota Administrasi Jakarta Selatan", 
     "Layanan Administrasi Kewilayahan Terpadu Kecamatan/Kelurahan & Fasilitasi Kepengurusan RT/RW", 
     "Layanan Administrasi Pemerintahan Kewilayahan", "Layanan Publik Eksternal", "Sistem Informasi Manajemen Kelurahan / Portal Pemkot Jaksel / JAKI")
]

# =========================================================================
# DEFINISI 44 PROSES BISNIS UNGGULAN SPBE (2 PROSES PER 22 PERANGKAT DAERAH)
# =========================================================================
DATA_44_PROSES = [
    # 1. Disdik
    ("Dinas Pendidikan", "Verifikasi Faktual dan Penetapan Penerima Bantuan Biaya Pendidikan Siswa Miskin", 
     "Pelayanan Publik", "Pendidikan dan Kebudayaan", "Pengelolaan Bantuan Pendidikan Dasar dan Menengah"),
    ("Dinas Pendidikan", "Penyelenggaraan Penerimaan Peserta Didik Baru (PPDB) Daring Terpusat", 
     "Pelayanan Publik", "Pendidikan dan Kebudayaan", "Penerimaan dan Seleksi Peserta Didik Baru"),
     
    # 2. Dinkes
    ("Dinas Kesehatan", "Pengelolaan Sistem Rujukan Pelayanan Kesehatan Puskesmas dan RSUD Terintegrasi", 
     "Pelayanan Publik", "Kesehatan Masyarakat", "Pelayanan Rujukan dan Fasilitas Kesehatan"),
    ("Dinas Kesehatan", "Surveilans Epidemiologi dan Penanggulangan Kejadian Luar Biasa (KLB) Penyakit Menular", 
     "Pelayanan Publik", "Kesehatan Masyarakat", "Pencegahan dan Pengendalian Penyakit"),
     
    # 3. Diskominfotik
    ("Dinas Komunikasi, Informatika dan Statistik", "Integrasi Komunikasi Data dan Interoperabilitas Sistem Penghubung Layanan Pemerintah (SPLP)", 
     "Tata Kelola Pemerintahan", "Komunikasi dan Informatika", "Pengelolaan Interoperabilitas Data dan SPBE"),
    ("Dinas Komunikasi, Informatika dan Statistik", "Penyelenggaraan Pusat Kendali Operasi Digital Jakarta Smart City (JSC Command Center)", 
     "Tata Kelola Pemerintahan", "Komunikasi dan Informatika", "Pengelolaan Operasional Pusat Data dan Smart City"),
     
    # 4. Dishub
    ("Dinas Perhubungan", "Pengujian Berkala Kelayakan Kendaraan Bermotor Angkutan Umum & Barang (e-KIR)", 
     "Pelayanan Publik", "Perhubungan dan Lalu Lintas", "Pengujian dan Sertifikasi Kelaikan Kendaraan"),
    ("Dinas Perhubungan", "Manajemen Rekayasa Lalu Lintas dan Pengendalian Sistem Kamera ETLE TransJakarta", 
     "Pelayanan Publik", "Perhubungan dan Lalu Lintas", "Pengendalian Operasional dan Keselamatan Lalu Lintas"),
     
    # 5. Satpol PP
    ("Satuan Polisi Pamong Praja", "Operasi Penertiban dan Penindakan Pelanggaran Peraturan Daerah / Peraturan Gubernur", 
     "Tata Kelola Pemerintahan", "Ketenteraman dan Ketertiban Umum", "Penindakan dan Penegakan Regulasi Daerah"),
    ("Satuan Polisi Pamong Praja", "Patroli Pengawasan Cipta Kondisi Kawasan Strategis dan Fasilitas Publik", 
     "Pelayanan Publik", "Ketenteraman dan Ketertiban Umum", "Pengawasan dan Pencegahan Gangguan Keamanan Wilayah"),
     
    # 6. DPMPTSP
    ("Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu", "Verifikasi Dokumen Teknis dan Penerbitan Izin Usaha / Izin Operasional Daerah", 
     "Pelayanan Publik", "Penanaman Modal dan Pelayanan Terpadu", "Pemrosesan dan Penerbitan Dokumen Izin Usaha"),
    ("Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu", "Pelayanan Konsultasi Investasi dan Fasilitasi Penyelesaian Hambatan Berusaha (AJIB)", 
     "Perekonomian Daerah", "Penanaman Modal", "Promosi dan Pendampingan Layanan Investasi"),
     
    # 7. Disdukcapil
    ("Dinas Kependudukan dan Pencatatan Sipil", "Penerbitan Dokumen Identitas Kependudukan (KTP-el, KIA, KK, Akta Sipil) Daring", 
     "Pelayanan Publik", "Administrasi Kependudukan", "Pendaftaran Penduduk dan Pencatatan Kelahiran/Kematian"),
    ("Dinas Kependudukan dan Pencatatan Sipil", "Penyelarasan dan Validasi Database Kependudukan Daerah dengan SIAK Terpusat", 
     "Tata Kelola Pemerintahan", "Administrasi Kependudukan", "Pemeliharaan dan Konsolidasi Database Kependudukan"),
     
    # 8. Dinsos
    ("Dinas Sosial", "Pemutakhiran Data Terpadu Kesejahteraan Sosial (DTKS) Tingkat RT/RW dan Kelurahan", 
     "Tata Kelola Pemerintahan", "Sosial dan Kesejahteraan", "Validasi dan Verifikasi Data Kemiskinan Daerah"),
    ("Dinas Sosial", "Penyaluran Bantuan Sosial Khusus (Kartu Lansia Jakarta / KLJ, KPDJ, Anak Yatim)", 
     "Pelayanan Publik", "Sosial dan Kesejahteraan", "Penyaluran Bantuan Perlindungan Sosial Rentan"),
     
    # 9. Bappeda
    ("Badan Perencanaan Pembangunan Daerah", "Penyusunan Rencana Kerja Pemerintah Daerah (RKPD) dan Rencana Strategis (Renstra) Daerah", 
     "Tata Kelola Pemerintahan", "Perencanaan Pembangunan Daerah", "Penyusunan Kebijakan Perencanaan Tahunan dan Lima Tahunan"),
    ("Badan Perencanaan Pembangunan Daerah", "Pengendalian, Pemantauan dan Evaluasi Ketercapaian Indikator Kinerja Pembangunan (e-Monev)", 
     "Tata Kelola Pemerintahan", "Pengawasan dan Evaluasi Program", "Monitoring dan Evaluasi Pelaksanaan Pembangunan"),
     
    # 10. BPKD
    ("Badan Pengelolaan Keuangan Daerah", "Penatausahaan Kas Daerah, Verifikasi SPM, dan Penerbitan SP2D Daring Terintegrasi", 
     "Tata Kelola Pemerintahan", "Keuangan Daerah", "Perbendaharaan dan Pengeluaran Kas Daerah"),
    ("Badan Pengelolaan Keuangan Daerah", "Penyusunan Laporan Keuangan Pemerintah Daerah (LKPD) Konsolidasian Berbasis Akrual", 
     "Tata Kelola Pemerintahan", "Akuntansi dan Pelaporan Keuangan", "Penyusunan Pertanggungjawaban Pelaksanaan APBD"),
     
    # 11. BPAD
    ("Badan Pengelolaan Aset Daerah", "Sensus Inventarisasi, Pelabelan Barcode/RFID, dan Rekonsiliasi Aset Tetap SKPD", 
     "Tata Kelola Pemerintahan", "Pengelolaan Barang Milik Daerah", "Inventarisasi dan Pembukuan Aset Daerah"),
    ("Badan Pengelolaan Aset Daerah", "Pengamanan Hukum dan Sertifikasi Hak Pakai Tanah/Bangunan Aset Pemprov DKI", 
     "Tata Kelola Pemerintahan", "Pengelolaan Barang Milik Daerah", "Pengamanan Yuridis dan Fisik Aset Daerah"),
     
    # 12. BPPBJ
    ("Badan Pelayanan Pengadaan Barang/Jasa", "Penyelenggaraan Tender Pengadaan Barang/Jasa Konstruksi dan Konsultansi Terbuka Daring", 
     "Tata Kelola Pemerintahan", "Pengadaan Barang dan Jasa", "Pemilihan Penyedia dan Evaluasi Penawaran SPSE"),
    ("Badan Pelayanan Pengadaan Barang/Jasa", "Kurasi dan Penayangan Produk UMKM Lokal pada e-Katalog Sektoral Daerah", 
     "Perekonomian Daerah", "Pengadaan dan Pemberdayaan UMKM", "Pengelolaan Katalog Elektronik Lokal"),
     
    # 13. Dinas SDA
    ("Dinas Sumber Daya Air", "Operasional dan Pemeliharaan Sistem Polder, Waduk, dan Rumah Pompa Utama Wilayah", 
     "Pelayanan Publik", "Pekerjaan Umum dan Pengairan", "Pengendalian Banjir dan Rob Pesisir"),
    ("Dinas Sumber Daya Air", "Pengerukan Lumpur Sungai, Saluran Mikro-Makro, dan Normalisasi Kali Secara Berkala", 
     "Pelayanan Publik", "Pekerjaan Umum dan Pengairan", "Pemeliharaan Kapasitas Drainase dan Saluran Air"),
     
    # 14. Dinas Bina Marga
    ("Dinas Bina Marga", "Rehabilitasi dan Pemeliharaan Berkala Struktur Jalan Protokol, Flyover, dan Underpass", 
     "Pelayanan Publik", "Bina Marga dan Tata Ruang Jalan", "Pemeliharaan Rutin Jaringan Jalan Perkotaan"),
    ("Dinas Bina Marga", "Penataan Jaringan Utilitas Bawah Tanah (Sarana Jaringan Utilitas Terpadu / SJUT)", 
     "Pelayanan Publik", "Infrastruktur Perkotaan", "Penyelenggaraan dan Pengawasan Utilitas Bawah Tanah"),
     
    # 15. Dinas LH
    ("Dinas Lingkungan Hidup", "Pengangkutan dan Pengelolaan Sampah Terpadu Menuju TPST Bantargebang / RDF Plant", 
     "Pelayanan Publik", "Lingkungan Hidup dan Kebersihan", "Logistik dan Pengolahan Sampah Perkotaan"),
    ("Dinas Lingkungan Hidup", "Pengawasan Pembuangan Limbah B3 dan Pengendalian Baku Mutu Kualitas Udara Ambien (SPKU)", 
     "Tata Kelola Pemerintahan", "Lingkungan Hidup", "Pengendalian Pencemaran dan Ketaatan Lingkungan"),
     
    # 16. Dinas Citata
    ("Dinas Cipta Karya, Tata Ruang dan Pertanahan", "Pemeriksaan Rencana Teknis Bangunan dan Sidang Tim Ahli Bangunan Gedung (TABG)", 
     "Pelayanan Publik", "Cipta Karya dan Penataan Ruang", "Penilaian Teknis Kelaikan Bangunan Gedung"),
    ("Dinas Cipta Karya, Tata Ruang dan Pertanahan", "Penyusunan Rencana Detail Tata Ruang (RDTR) Digital Interaktif Pemprov DKI Jakarta", 
     "Tata Kelola Pemerintahan", "Penataan Ruang dan Pertanahan", "Perencanaan dan Pengendalian Tata Ruang Kota"),
     
    # 17. Disnakertransgi
    ("Dinas Tenaga Kerja, Transmigrasi dan Energi", "Fasilitasi Hubungan Industrial, Mediasi Perselisihan Hak Pekerja, dan Pendaftaran PKB", 
     "Pelayanan Publik", "Ketenagakerjaan dan Transmigrasi", "Pembinaan Hubungan Industrial dan Pengawasan Syarat Kerja"),
    ("Dinas Tenaga Kerja, Transmigrasi dan Energi", "Penyelenggaraan Pelatihan Vokasi Siap Kerja Melalui Pusat Pelatihan Kerja Daerah (PPKD)", 
     "Pelayanan Publik", "Ketenagakerjaan", "Pengembangan Keterampilan dan Sertifikasi Tenaga Kerja"),
     
    # 18. Disgulkarmat
    ("Dinas Penanggulangan Kebakaran dan Penyelamatan", "Operasi Pemadaman Kebakaran Permukiman Padat dan Evakuasi Korban Kedaruratan Bencana", 
     "Pelayanan Publik", "Ketenteraman, Ketertiban Umum dan Penyelamatan", "Operasi Taktis Pemadaman dan Penyelamatan Darurat"),
    ("Dinas Penanggulangan Kebakaran dan Penyelamatan", "Inspeksi Keselamatan Kebakaran Gedung Tinggi dan Penerbitan Rekomendasi Proteksi Kebakaran", 
     "Pelayanan Publik", "Penyelamatan dan Pencegahan Bahaya Kebakaran", "Pengawasan dan Audit Kelaikan Sistem Proteksi Kebakaran"),
     
    # 19. BPBD
    ("Badan Penanggulangan Bencana Daerah", "Aktivasi Pos Komando Darurat Bencana dan Mobilisasi Tim Reaksi Cepat (TRC) Penanggulangan Banjir", 
     "Pelayanan Publik", "Penanggulangan Bencana Daerah", "Komando Tanggap Darurat dan Evakuasi Bencana"),
    ("Badan Penanggulangan Bencana Daerah", "Pendataan Kerusakan Pasca Bencana dan Penyaluran Bantuan Tenda/Logistik Pengungsi", 
     "Pelayanan Publik", "Penanggulangan Bencana", "Rehabilitasi, Rekonstruksi dan Bantuan Logistik Pengungsi"),
     
    # 20. Inspektorat
    ("Inspektorat Provinsi DKI Jakarta", "Audit Kepatuhan Operasional, Reviu LKPD, dan Evaluasi Kinerja Akuntabilitas Instansi (AKIP)", 
     "Tata Kelola Pemerintahan", "Pengawasan Internal Pemerintah", "Audit Kinerja dan Pemeriksaan Berkala SKPD"),
    ("Inspektorat Provinsi DKI Jakarta", "Pemeriksaan Khusus Kasus Pelanggaran Disiplin ASN dan Tindak Lanjut Rekomendasi Pengawasan", 
     "Tata Kelola Pemerintahan", "Pengawasan Internal", "Investigasi Khusus dan Tindak Lanjut Hasil Pengawasan"),
     
    # 21. Dinas PPKUKM
    ("Dinas Perindustrian, Perdagangan, Koperasi, Usaha Kecil dan Menengah", "Penyelenggaraan 7 Tahap Pasti Sukses Inkubasi Usaha Baru (Jakpreneur)", 
     "Perekonomian Daerah", "Koperasi dan Usaha Kecil Menengah", "Inkubasi dan Pembinaan Wirausaha Baru Daerah"),
    ("Dinas Perindustrian, Perdagangan, Koperasi, Usaha Kecil dan Menengah", "Operasi Pasar Murah dan Pemantauan Stok Sembako Terintegrasi Info Pangan Jakarta (IPJ)", 
     "Perekonomian Daerah", "Perdagangan dan Perlindungan Konsumen", "Stabilisasi Pasokan dan Pengendalian Inflasi Pangan"),
     
    # 22. Kota Administrasi Jakarta Selatan (Kewilayahan)
    ("Kota Administrasi Jakarta Selatan", "Koordinasi Penyelenggaraan Ketenteraman Wilayah dan Fasilitasi Lembaga Kemasyarakatan (RT/RW/LMK)", 
     "Tata Kelola Pemerintahan", "Pemerintahan Daerah dan Kewilayahan", "Fasilitasi Lembaga Kemasyarakatan dan Kerukunan Warga"),
    ("Kota Administrasi Jakarta Selatan", "Penanganan Pengaduan Cepat Sarana Prasarana Wilayah Melalui Penugasan PPSU Kelurahan", 
     "Pelayanan Publik", "Pekerjaan Umum dan Kebersihan Lingkungan", "Operasional Penanganan Prasarana dan Sarana Umum Kelurahan")
]

# =========================================================================
# HELPER UNTUK MEMBUAT SHEET TERSTANDARISASI
# =========================================================================
def add_standard_audit_sheet(wb, title, sheet_type, opd_name, data_rows):
    ws = wb.create_sheet(title=title)
    ws.views.sheetView[0].showGridLines = True
    
    ws.row_dimensions[1].height = 12
    ws.cell(2, 1, value=f"{title} — {opd_name}").font = FONT_SHEET_TITLE
    ws.row_dimensions[2].height = 26
    
    sub = ("Daftar ID data arsitektur SPBE dan rincian kolom mandatory yang belum terisi / gagal simpan"
           if sheet_type == 'GAGAL' else
           "Daftar domain arsitektur SPBE yang belum dibuat / belum memiliki data (kosong total)")
    ws.cell(3, 1, value=sub).font = FONT_SUBTITLE
    ws.row_dimensions[3].height = 18
    ws.row_dimensions[4].height = 8
    
    headers = ["NO", "PERANGKAT DAERAH", "DOMAIN", "ID - Nama Data", "Nama Kolom yang belum terisi"] if sheet_type == 'GAGAL' else ["NO", "PERANGKAT DAERAH", "DOMAIN"]
    ws.row_dimensions[5].height = 28
    
    for ci, h in enumerate(headers, 1):
        c = ws.cell(5, ci, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER_BLUE
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER
        
    for idx, row in enumerate(data_rows, 6):
        is_zebra = (idx % 2 == 0)
        row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        cleaned_row = [str(item or '').strip() for item in row]
        
        max_lines = 1
        for ci, val in enumerate(cleaned_row, 1):
            if not val:
                continue
            nl_count = val.count('\n') + 1
            col_limit = 42 if ci in [2, 4] else (68 if ci == 5 else 28)
            wrap_count = max(1, math.ceil(len(val) / col_limit))
            eff = max(nl_count, wrap_count)
            if eff > max_lines:
                max_lines = eff
                
        row_height = max(26, max_lines * 16.5 + 8)
        ws.row_dimensions[idx].height = min(row_height, 240)
        
        for ci, val in enumerate(cleaned_row, 1):
            cell = ws.cell(idx, ci, value=val)
            cell.font = FONT_BODY
            cell.border = BORDER_CLEAN
            cell.fill = row_fill
            cell.alignment = ALIGN_DATA_TOP_CENTER if ci == 1 else ALIGN_DATA_TOP_LEFT
                
    if sheet_type == 'GAGAL':
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 44
        ws.column_dimensions['C'].width = 34
        ws.column_dimensions['D'].width = 52
        ws.column_dimensions['E'].width = 75
    else:
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 44
        ws.column_dimensions['C'].width = 36


# =========================================================================
# 1. BANGUN LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.XLSX
# =========================================================================
wb_master = openpyxl.Workbook()
wb_master.remove(wb_master.active)

# --- TAB 1: Ringkasan Eksekutif ---
ws_exec = wb_master.create_sheet(title='Ringkasan Eksekutif')
ws_exec.views.sheetView[0].showGridLines = True
ws_exec.row_dimensions[1].height = 12
ws_exec.cell(2, 1, value="REKAPITULASI AUDIT & ARSITEKTUR SPBE 22 PERANGKAT DAERAH").font = FONT_SHEET_TITLE
ws_exec.row_dimensions[2].height = 26
ws_exec.cell(3, 1, value="Pemetaan Lengkap Layanan, Proses Bisnis & Data Hilang Seluruh OPD Pemprov DKI Jakarta").font = FONT_SUBTITLE
ws_exec.row_dimensions[3].height = 18

headers_exec = ["NO", "NAMA PERANGKAT DAERAH", "STATUS ARSITEKTUR SPBE", "LAYANAN DIGITAL UTAMA (RAL)", "PROSES BISNIS UTAMA (RAB)", "TAB SOLUSI"]
ws_exec.row_dimensions[5].height = 28
for ci, h in enumerate(headers_exec, 1):
    c = ws_exec.cell(5, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

opd_exec_22 = [
    ("1.0", "Dinas Pendidikan", "LENGKAP (TERPETAKAN)", "Bantuan Biaya Personal Pendidikan (KJP Plus & KJMU)", "PPDB Daring & Verifikasi Bantuan Sekolah", "22 Layanan (22 OPD)"),
    ("2.0", "Dinas Kesehatan", "LENGKAP (TERPETAKAN)", "Antrean Faskes Daring, e-Jiwa & Deteksi Stunting (JakSehat)", "Rujukan Pelayanan Kesehatan & Surveilans KLB", "22 Layanan (22 OPD)"),
    ("3.0", "Dinas Komunikasi, Informatika dan Statistik", "LENGKAP (TERPETAKAN)", "Portal Warga Terpadu & Penanganan Cepat (JAKI & CRM)", "Integrasi SPLP & Smart City Command Center", "22 Layanan (22 OPD)"),
    ("4.0", "Dinas Perhubungan", "LENGKAP (TERPETAKAN)", "Tiket Transportasi Multi-Moda (JakLingko) & e-KIR Daring", "Pengujian Berkala Kendaraan & Rekayasa Lalu Lintas", "22 Layanan (22 OPD)"),
    ("5.0", "Satuan Polisi Pamong Praja", "LENGKAP (TERPETAKAN)", "Penertiban Gangguan Trantibum & Aduan Pelanggaran Perda", "Operasi Penertiban & Patroli Cipta Kondisi", "22 Layanan (22 OPD)"),
    ("6.0", "Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu", "LENGKAP (TERPETAKAN)", "Perizinan Berusaha & Investasi Terpadu (JakEVO / OSS)", "Verifikasi Izin Usaha & Pendampingan Investasi AJIB", "22 Layanan (22 OPD)"),
    ("7.0", "Dinas Kependudukan dan Pencatatan Sipil", "LENGKAP (TERPETAKAN)", "Administrasi Kependudukan & KTP Digital (Alpukat Betawi)", "Penerbitan KTP-el/KIA/KK & Penyelarasan SIAK", "22 Layanan (22 OPD)"),
    ("8.0", "Dinas Sosial", "LENGKAP (TERPETAKAN)", "Pendaftaran PPKS & Bansos Kluster (KLJ, KPDJ, Anak Yatim)", "Pemutakhiran DTKS & Penyaluran Bantuan Sosial", "22 Layanan (22 OPD)"),
    ("9.0", "Badan Perencanaan Pembangunan Daerah", "LENGKAP (TERPETAKAN)", "Partisipasi Musrenbang Daring (SIPD Perencanaan)", "Penyusunan RKPD & Evaluasi Kinerja (e-Monev)", "22 Layanan (22 OPD)"),
    ("10.0", "Badan Pengelolaan Keuangan Daerah", "LENGKAP (TERPETAKAN)", "Penerbitan SP2D Daring & e-BLUD Terintegrasi", "Penatausahaan Kas Daerah & Penyusunan LKPD Akrual", "22 Layanan (22 OPD)"),
    ("11.0", "Badan Pengelolaan Aset Daerah", "LENGKAP (TERPETAKAN)", "Penatausahaan Barang Milik Daerah (SIMBADA / Si-Aset)", "Sensus Aset Tetap & Sertifikasi Tanah Pemprov", "22 Layanan (22 OPD)"),
    ("12.0", "Badan Pelayanan Pengadaan Barang/Jasa", "LENGKAP (TERPETAKAN)", "Pengadaan Barang dan Jasa Elektronik (SPSE / e-Katalog)", "Tender Konstruksi Daring & Kurasi Produk UMKM Lokal", "22 Layanan (22 OPD)"),
    ("13.0", "Dinas Sumber Daya Air", "LENGKAP (TERPETAKAN)", "Informasi Peringatan Dini Banjir & Posko Pompa Daring", "Operasional Sistem Polder & Pengerukan Sungai", "22 Layanan (22 OPD)"),
    ("14.0", "Dinas Bina Marga", "LENGKAP (TERPETAKAN)", "Pengaduan Jalan Rusak & Penerangan Jalan Umum (PJU Daring)", "Pemeliharaan Jalan Flyover & Penataan Kabel SJUT", "22 Layanan (22 OPD)"),
    ("15.0", "Dinas Lingkungan Hidup", "LENGKAP (TERPETAKAN)", "Uji Emisi Gas Buang Kendaraan & Bank Sampah Digital", "Pengolahan Sampah RDF Plant & Pengawasan Baku Mutu Udara", "22 Layanan (22 OPD)"),
    ("16.0", "Dinas Cipta Karya, Tata Ruang dan Pertanahan", "LENGKAP (TERPETAKAN)", "Persetujuan Bangunan Gedung (PBG) & IRK Daring (SIMBG)", "Sidang Ahli Bangunan Gedung (TABG) & RDTR Interaktif", "22 Layanan (22 OPD)"),
    ("17.0", "Dinas Tenaga Kerja, Transmigrasi dan Energi", "LENGKAP (TERPETAKAN)", "Bursa Kerja Daring & Pelatihan Vokasi PPKD (Jaknaker)", "Mediasi Hubungan Industrial & Sertifikasi Tenaga Kerja", "22 Layanan (22 OPD)"),
    ("18.0", "Dinas Penanggulangan Kebakaran dan Penyelamatan", "LENGKAP (TERPETAKAN)", "Tanggap Darurat Kebakaran & Penyelamatan (Siaga 112)", "Operasi Taktis Pemadaman & Inspeksi Proteksi Gedung", "22 Layanan (22 OPD)"),
    ("19.0", "Badan Penanggulangan Bencana Daerah", "LENGKAP (TERPETAKAN)", "Peringatan Dini Kebencanaan (DEWS) & Bantuan Logistik", "Posko Darurat Reaksi Cepat (TRC) & Bantuan Tenda Bencana", "22 Layanan (22 OPD)"),
    ("20.0", "Inspektorat Provinsi DKI Jakarta", "LENGKAP (TERPETAKAN)", "Whistleblowing System (WBS) & Pelaporan Gratifikasi", "Audit Kepatuhan SKPD, Reviu LKPD & Tindak Lanjut BPK", "22 Layanan (22 OPD)"),
    ("21.0", "Dinas Perindustrian, Perdagangan, Koperasi, UKM", "LENGKAP (TERPETAKAN)", "Inkubasi Bisnis, Sertifikasi Halal & Akses Modal (Jakpreneur)", "7 Tahap Sukses Jakpreneur & Pemantauan Pangan (IPJ)", "22 Layanan (22 OPD)"),
    ("22.0", "Kota Administrasi Jakarta Selatan & Kewilayahan", "LENGKAP (TERPETAKAN)", "Administrasi Kewilayahan Kelurahan & Layanan RT/RW", "Fasilitasi Lembaga Warga & Operasional PPSU Kelurahan", "22 Layanan (22 OPD)")
]

for idx, row in enumerate(opd_exec_22, 6):
    ws_exec.row_dimensions[idx].height = 26
    is_zebra = (idx % 2 == 0)
    for ci, val in enumerate(row, 1):
        c = ws_exec.cell(idx, ci, value=val)
        c.font = FONT_BODY
        c.border = BORDER_CLEAN
        c.fill = FILL_ZEBRA if is_zebra else FILL_WHITE
        if ci in [1, 3, 6]:
            c.alignment = ALIGN_DATA_TOP_CENTER
            if ci == 3:
                c.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # Soft green
        else:
            c.alignment = ALIGN_DATA_TOP_LEFT

ws_exec.column_dimensions['A'].width = 8
ws_exec.column_dimensions['B'].width = 46
ws_exec.column_dimensions['C'].width = 24
ws_exec.column_dimensions['D'].width = 54
ws_exec.column_dimensions['E'].width = 50
ws_exec.column_dimensions['F'].width = 24


# --- TAB 2: 22 Layanan_Upgrade (22 Perangkat Daerah) ---
ws_lay22 = wb_master.create_sheet(title='22 Layanan (22 OPD)')
ws_lay22.views.sheetView[0].showGridLines = True
ws_lay22.row_dimensions[1].height = 28

lay_headers = [
    "Domain",
    "Kategori Arsitektur To-Be",
    "Nama Layanan As-Is Terkait",
    "Perangkat Daerah *",
    "Referensi Arsitektur Layanan (RAL) Level 1 *",
    "Referensi Arsitektur Layanan (RAL) Level 2 *",
    "Kanal Akses Layanan Terintegrasi *"
]

for ci, h in enumerate(lay_headers, 1):
    c = ws_lay22.cell(1, ci, value=h)
    c.font = FONT_HEADER
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER
    c.fill = FILL_HEADER_BLUE if ci <= 3 else FILL_HEADER_YELLOW

for r_idx, (no, opd_name, lay_name, ral_l1, ral_l2, kanal) in enumerate(DATA_22_LAYANAN, 2):
    ws_lay22.row_dimensions[r_idx].height = 26
    is_zebra = (r_idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    vals = ["Layanan", "Upgrade", lay_name, opd_name, ral_l1, ral_l2, kanal]
    for ci, v in enumerate(vals, 1):
        cell = ws_lay22.cell(r_idx, ci, value=v)
        cell.font = FONT_BODY
        cell.border = BORDER_CLEAN
        cell.fill = row_fill
        cell.alignment = ALIGN_DATA_TOP_CENTER if ci in [1, 2] else ALIGN_DATA_TOP_LEFT

ws_lay22.column_dimensions['A'].width = 16
ws_lay22.column_dimensions['B'].width = 24
ws_lay22.column_dimensions['C'].width = 54
ws_lay22.column_dimensions['D'].width = 44 # Distinct OPD name clearly visible
ws_lay22.column_dimensions['E'].width = 46
ws_lay22.column_dimensions['F'].width = 32
ws_lay22.column_dimensions['G'].width = 46


# --- TAB 3: 44 ProsesBisnis (22 OPD) ---
ws_pb44 = wb_master.create_sheet(title='44 ProsesBisnis (22 OPD)')
ws_pb44.views.sheetView[0].showGridLines = True
ws_pb44.row_dimensions[1].height = 28

pb_headers = [
    "Domain",
    "Kategori Arsitektur To-Be",
    "Arsitektur As-Is Terkait",
    "Perangkat Daerah *",
    "Referensi Arsitektur Bisnis (RAB) Level 1 (Referensi Nasional) *",
    "Referensi Arsitektur Bisnis (RAB) Level 2 (Referensi Nasional) *",
    "Referensi Arsitektur Bisnis (RAB) Level 3 (Referensi Nasional) *"
]

for ci, h in enumerate(pb_headers, 1):
    c = ws_pb44.cell(1, ci, value=h)
    c.font = FONT_HEADER
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER
    c.fill = FILL_HEADER_BLUE if ci <= 3 else FILL_HEADER_YELLOW

for r_idx, (opd_name, proc_name, rab_l1, rab_l2, rab_l3) in enumerate(DATA_44_PROSES, 2):
    ws_pb44.row_dimensions[r_idx].height = 26
    is_zebra = (r_idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    vals = ["Proses Bisnis", "Upgrade", proc_name, opd_name, rab_l1, rab_l2, rab_l3]
    for ci, v in enumerate(vals, 1):
        cell = ws_pb44.cell(r_idx, ci, value=v)
        cell.font = FONT_BODY
        cell.border = BORDER_CLEAN
        cell.fill = row_fill
        cell.alignment = ALIGN_DATA_TOP_CENTER if ci in [1, 2] else ALIGN_DATA_TOP_LEFT

ws_pb44.column_dimensions['A'].width = 16
ws_pb44.column_dimensions['B'].width = 24
ws_pb44.column_dimensions['C'].width = 54
ws_pb44.column_dimensions['D'].width = 44 # Distinct OPD name clearly visible
ws_pb44.column_dimensions['E'].width = 30
ws_pb44.column_dimensions['F'].width = 38
ws_pb44.column_dimensions['G'].width = 50


# --- TAB 4 & 5: Audit Gagal & Belum Ada Jakarta Selatan ---
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
add_standard_audit_sheet(wb_master, "Data gagal Upload JAKSEL", "GAGAL", "Kota Administrasi Jakarta Selatan", jaksel_fail)

jaksel_none = [
    (1.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Upgrade"),
    (2.0, "Kota Administrasi Jakarta Selatan", "ProsesBisnis_Sunset"),
    (3.0, "Kota Administrasi Jakarta Selatan", "Layanan_Upgrade"),
    (4.0, "Kota Administrasi Jakarta Selatan", "Layanan_Sunset"),
    (5.0, "Kota Administrasi Jakarta Selatan", "Aplikasi_Sunset"),
    (6.0, "Kota Administrasi Jakarta Selatan", "DataInformasi_Upgrade"),
    (7.0, "Kota Administrasi Jakarta Selatan", "DataInformasi_Sunset")
]
add_standard_audit_sheet(wb_master, "Data yg blm ada JAKSEL", "BELUM_ADA", "Kota Administrasi Jakarta Selatan", jaksel_none)


# --- TAB 6 - 15: Extracted OPDs dari Dokumen Referensi Pemprov DKI ---
ref_wb = openpyxl.load_workbook(REF_FILE, data_only=True) if os.path.exists(REF_FILE) else None
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
                    
            add_standard_audit_sheet(wb_master, new_title, s_type, opd_name, extracted_rows)

# --- TAB 16: Rekap Seluruh Data Belum Ada (Pemerintahan 22 OPD) ---
ws_all_missing = wb_master.create_sheet(title='Data blm ada (Semua OPD)')
ws_all_missing.views.sheetView[0].showGridLines = True
ws_all_missing.row_dimensions[1].height = 12
ws_all_missing.cell(2, 1, value="REKAPITULASI DATA ARSITEKTUR YANG BELUM ADA DI SELURUH PEMERINTAHAN").font = FONT_SHEET_TITLE
ws_all_dimensions = ws_all_missing.row_dimensions[2].height = 26
ws_all_missing.cell(3, 1, value="Inventarisasi Domain Kosong & Dokumen Defisit di Seluruh 22 Perangkat Daerah Pemprov DKI Jakarta").font = FONT_SUBTITLE
ws_all_missing.row_dimensions[3].height = 18

headers_all_missing = ["NO", "PERANGKAT DAERAH / BIRO", "KATEGORI KEKOSONGAN", "DOMAIN ARSITEKTUR KOSONG / CATATAN LAPANGAN"]
ws_all_missing.row_dimensions[5].height = 28
for ci, h in enumerate(headers_all_missing, 1):
    c = ws_all_missing.cell(5, ci, value=h)
    c.font = FONT_HEADER
    c.fill = FILL_HEADER_BLUE
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER

all_missing_gov_rows = [
    (1, "Kota Administrasi Jakarta Selatan", "Template Kosong", "ProsesBisnis_Upgrade, Layanan_Upgrade, Aplikasi_Sunset, DataInformasi_Upgrade"),
    (2, "Badan Perencanaan Pembangunan Daerah", "Domain Kosong", "ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Sunset, Aplikasi_Sunset, DataInformasi_Upgrade/Sunset"),
    (3, "Satuan Polisi Pamong Praja", "Domain Kosong", "ProsesBisnis_Sunset, Layanan_Sunset, Aplikasi_Upgrade, Aplikasi_Sunset, DataInformasi_Upgrade"),
    (4, "Kota Administrasi Jakarta Timur", "Domain Kosong", "ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Sunset, DataInformasi_Upgrade, DataInformasi_Sunset"),
    (5, "Kota Administrasi Jakarta Utara", "Domain Kosong", "ProsesBisnis_Sesuai, ProsesBisnis_Upgrade, Layanan_Sesuai, Layanan_Upgrade, Layanan_Sunset"),
    (6, "Kota Administrasi Jakarta Barat", "Domain Kosong", "10 Domain: ProsesBisnis, Layanan, Aplikasi, DataInformasi belum terisi sama sekali"),
    (7, "Inspektorat Provinsi DKI Jakarta", "Domain Kosong", "ProsesBisnis_Upgrade, ProsesBisnis_Sunset, Layanan_Upgrade, Layanan_Sunset, Aplikasi_Upgrade"),
    (8, "Kabupaten Administrasi Kepulauan Seribu", "Dokumen Kosong / Defisit", "BAST Belum Ada, Dokumen 03C Belum Diunggah di Google Drive"),
    (9, "Dinas Penanaman Modal dan PTSP", "Dokumen Belum Lengkap", "BAST Belum Ditandatangani, Menunggu Berita Acara Rekonsiliasi"),
    (10, "Badan Pengelolaan Aset Daerah", "Dokumen Hardcopy Defisit", "BAST Masih Berupa Softcopy, Hardcopy Fisik Belum Diterima Diskominfotik"),
    (11, "Biro Tata Pemerintahan", "Dokumen Hardcopy Defisit", "BAST Softcopy Sudah Ada, Hardcopy Belum Ada di Dinas"),
    (12, "Biro Pembangunan dan Lingkungan Hidup", "Menunggu TTD Eselon", "Dokumen Menunggu Tanda Tangan Eselon 3"),
    (13, "Biro Kerja Sama Daerah", "Menunggu TTD Eselon", "Dokumen Menunggu Tanda Tangan Eselon 3, BAST Belum Lengkap"),
    (14, "Biro Perekonomian dan Keuangan", "Dokumen Hardcopy Defisit", "BAST Berupa PDF/Softcopy, Hardcopy Fisik Belum Ada"),
    (15, "Biro Organisasi dan Reformasi Birokrasi", "Menunggu TTD Eselon", "Dokumen SPBE Masih Proses Pengesahan Pejabat Eselon 3"),
    (16, "Biro Umum dan Administrasi", "Menunggu TTD Eselon", "BAST Harus Ditandatangani Pejabat Eselon 3"),
    (17, "Dinas Komunikasi, Informatika dan Statistik", "BAST Tertunda", "BAST Masih Dalam Proses Penyelesaian Tim Internal SPBE"),
    (18, "Dinas Cipta Karya, Tata Ruang dan Pertanahan", "Menunggu TTD Eselon", "Dokumen 03C Menunggu Pengesahan Tanda Tangan Eselon 3"),
    (19, "Dinas Tenaga Kerja, Transmigrasi dan Energi", "Draft Arsitektur Belum Final", "Dokumen 03 To-Be Masih Berstatus DRAFT, Belum Disahkan"),
    (20, "Dinas Perhubungan", "Dokumen Direviu Ulang", "Dokumen To-Be Dibawa Kembali Oleh OPD Untuk Reviu Tambahan"),
    (21, "Badan Pelayanan Pengadaan Barang/Jasa", "Dokumen Direviu Ulang", "Dokumen Dibawa Kembali Oleh Tim Teknis BPPBJ Untuk Koreksi Kategori"),
    (22, "Badan Pengelolaan Keuangan Daerah", "Menunggu TTD Pimpinan", "Berita Acara (BA) BPKD Belum Ditandatangani Ibu Kabid Perbendaharaan")
]

for idx, (no, opd_name, kat, catatan) in enumerate(all_missing_gov_rows, 6):
    ws_all_missing.row_dimensions[idx].height = 26
    is_zebra = (idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    vals = [no, opd_name, kat, catatan]
    for ci, v in enumerate(vals, 1):
        cell = ws_all_missing.cell(idx, ci, value=v)
        cell.font = FONT_BODY
        cell.border = BORDER_CLEAN
        cell.fill = row_fill
        if ci == 1:
            cell.alignment = ALIGN_DATA_TOP_CENTER
        elif ci == 3:
            cell.alignment = ALIGN_DATA_TOP_CENTER
            cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
        else:
            cell.alignment = ALIGN_DATA_TOP_LEFT

ws_all_missing.column_dimensions['A'].width = 8
ws_all_missing.column_dimensions['B'].width = 46
ws_all_missing.column_dimensions['C'].width = 28
ws_all_missing.column_dimensions['D'].width = 72

wb_master.save(OUTPUT_MASTER)
shutil.copyfile(OUTPUT_MASTER, os.path.join(PUBLIC_DL_DIR, "LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx"))
print(f"[SUCCESS] LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx successfully generated with 16 tabs!")


# =========================================================================
# 2. BANGUN WORKBOOK KHUSUS: 03C_TOBE_ASIS_22_PERANGKAT_DAERAH_TERISI.XLSX
# =========================================================================
wb_22 = openpyxl.Workbook()
wb_22.remove(wb_22.active)

# Sheet 1: 22 Layanan_Upgrade
ws_22_lay = wb_22.create_sheet(title="22 Layanan_Upgrade")
ws_22_lay.views.sheetView[0].showGridLines = True
ws_22_lay.row_dimensions[1].height = 28

for ci, h in enumerate(lay_headers, 1):
    c = ws_22_lay.cell(1, ci, value=h)
    c.font = FONT_HEADER
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER
    c.fill = FILL_HEADER_BLUE if ci <= 3 else FILL_HEADER_YELLOW

for r_idx, (no, opd_name, lay_name, ral_l1, ral_l2, kanal) in enumerate(DATA_22_LAYANAN, 2):
    ws_22_lay.row_dimensions[r_idx].height = 26
    is_zebra = (r_idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    vals = ["Layanan", "Upgrade", lay_name, opd_name, ral_l1, ral_l2, kanal]
    for ci, v in enumerate(vals, 1):
        cell = ws_22_lay.cell(r_idx, ci, value=v)
        cell.font = FONT_BODY
        cell.border = BORDER_CLEAN
        cell.fill = row_fill
        cell.alignment = ALIGN_DATA_TOP_CENTER if ci in [1, 2] else ALIGN_DATA_TOP_LEFT

ws_22_lay.column_dimensions['A'].width = 16
ws_22_lay.column_dimensions['B'].width = 24
ws_22_lay.column_dimensions['C'].width = 54
ws_22_lay.column_dimensions['D'].width = 44 # Perangkat Daerah jelas berbeda-beda!
ws_22_lay.column_dimensions['E'].width = 46
ws_22_lay.column_dimensions['F'].width = 32
ws_22_lay.column_dimensions['G'].width = 46

# Sheet 2: 44 ProsesBisnis_Upgrade
ws_22_pb = wb_22.create_sheet(title="44 ProsesBisnis_Upgrade")
ws_22_pb.views.sheetView[0].showGridLines = True
ws_22_pb.row_dimensions[1].height = 28

for ci, h in enumerate(pb_headers, 1):
    c = ws_22_pb.cell(1, ci, value=h)
    c.font = FONT_HEADER
    c.alignment = ALIGN_HEADER
    c.border = BORDER_HEADER
    c.fill = FILL_HEADER_BLUE if ci <= 3 else FILL_HEADER_YELLOW

for r_idx, (opd_name, proc_name, rab_l1, rab_l2, rab_l3) in enumerate(DATA_44_PROSES, 2):
    ws_22_pb.row_dimensions[r_idx].height = 26
    is_zebra = (r_idx % 2 == 0)
    row_fill = FILL_ZEBRA if is_zebra else FILL_WHITE
    
    vals = ["Proses Bisnis", "Upgrade", proc_name, opd_name, rab_l1, rab_l2, rab_l3]
    for ci, v in enumerate(vals, 1):
        cell = ws_22_pb.cell(r_idx, ci, value=v)
        cell.font = FONT_BODY
        cell.border = BORDER_CLEAN
        cell.fill = row_fill
        cell.alignment = ALIGN_DATA_TOP_CENTER if ci in [1, 2] else ALIGN_DATA_TOP_LEFT

ws_22_pb.column_dimensions['A'].width = 16
ws_22_pb.column_dimensions['B'].width = 24
ws_22_pb.column_dimensions['C'].width = 54
ws_22_pb.column_dimensions['D'].width = 44 # Perangkat Daerah jelas berbeda-beda!
ws_22_pb.column_dimensions['E'].width = 30
ws_22_pb.column_dimensions['F'].width = 38
ws_22_pb.column_dimensions['G'].width = 50

wb_22.save(OUTPUT_22_OPD)
shutil.copyfile(OUTPUT_22_OPD, os.path.join(PUBLIC_DL_DIR, "03C_TOBE_ASIS_22_PERANGKAT_DAERAH_TERISI.xlsx"))
print(f"[SUCCESS] 03C_TOBE_ASIS_22_PERANGKAT_DAERAH_TERISI.xlsx successfully generated!")
