"""
NEXUS AI ENTERPRISE — SPBE DKI JAKARTA SPREADSHEET GENERATOR
Agent: RAKA (Director of Technology) & SEKAR (Director of Compliance)
Orchestrator: ARKA (Chief Executive & Strategy Officer)

Generates the fully populated 03C_TOBE_ASIS spreadsheet for Kota Administrasi Jakarta Selatan
Filling the empty rows in:
- 39 ProsesBisnis_Upgrade (39 Rows)
- 21 Layanan_Upgrade (21 Rows)
Mapped to Pergub DKI No. 57/2022 & National SPBE Reference Architecture (RAB/RAL KemenPANRB).
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "spreadsheets")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "03C_TOBE_ASIS_Kota_Administrasi_Jakarta_Selatan_TERISI.xlsx")

wb = openpyxl.Workbook()
# Remove default sheet
wb.remove(wb.active)

# Color styles matching the user's screenshot
HEADER_FILL_BLUE = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
HEADER_FILL_YELLOW = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
HEADER_FONT = Font(name="Arial", size=10, bold=True, color="000000")
DATA_FONT = Font(name="Arial", size=9, color="000000")
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

# ==========================================
# 1. SHEET: 39 ProsesBisnis_Upgrade
# ==========================================
ws_pb = wb.create_sheet(title="39 ProsesBisnis_Upgrade")

pb_headers = [
    "Domain",
    "Kategori Arsitektur To-Be",
    "Arsitektur As-Is Terkait",
    "Perangkat Daerah *",
    "Referensi Arsitektur Bisnis (RAB) Level 1 (Referensi Nasional) *",
    "Referensi Arsitektur Bisnis (RAB) Level 2 (Referensi Nasional) *",
    "Referensi Arsitektur Bisnis (RAB) Level 3 (Referensi Nasional) *"
]

# Write headers
for col_idx, h_text in enumerate(pb_headers, 1):
    cell = ws_pb.cell(row=1, column=col_idx, value=h_text)
    cell.font = HEADER_FONT
    cell.alignment = ALIGN_CENTER
    cell.border = thin_border
    if col_idx <= 3:
        cell.fill = HEADER_FILL_BLUE
    else:
        cell.fill = HEADER_FILL_YELLOW

# 39 Real Business Processes of Kota Administrasi Jakarta Selatan (Tupoksi Walikota, Camat, Lurah - Pergub 57/2022)
pb_rows = [
    ("Pengelolaan Pelayanan Administrasi Kependudukan dan Pencatatan Sipil Terintegrasi", "Pelayanan Publik", "Administrasi Kependudukan", "Penerbitan Dokumen Pendaftaran Penduduk"),
    ("Penyelenggaraan Ketenteraman dan Ketertiban Umum Wilayah Kota Administrasi", "Pelayanan Publik", "Ketenteraman dan Ketertiban Umum", "Pencegahan Gangguan Ketenteraman dan Ketertiban"),
    ("Koordinasi Penegakan Peraturan Daerah dan Peraturan Gubernur di Tingkat Kecamatan", "Tata Kelola Pemerintahan", "Hukum dan Pengawasan", "Penegakan Regulasi Daerah"),
    ("Pengelolaan Penanganan Pengaduan Masyarakat Melalui CRM / Portal Cepat Respon Masyarakat", "Pelayanan Publik", "Komunikasi dan Informatika", "Pengelolaan Pengaduan Masyarakat SPBE"),
    ("Koordinasi Penanganan Genangan Air dan Banjir Tingkat Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Pekerjaan Umum dan Penataan Ruang", "Pengelolaan Sumber Daya Air Wilayah"),
    ("Pengelolaan Sarana Prasarana dan Utilitas Umum Tingkat Kelurahan", "Pelayanan Publik", "Perumahan dan Kawasan Permukiman", "Pemeliharaan Prasarana dan Utilitas Lingkungan"),
    ("Koordinasi Penanggulangan Bencana dan Evakuasi Darurat Wilayah Jakarta Selatan", "Pelayanan Publik", "Sosial dan Kebencanaan", "Penanganan Darurat Bencana Daerah"),
    ("Penyelenggaraan Musyawarah Perencanaan Pembangunan (Musrenbang) Tingkat Kelurahan & Kecamatan", "Tata Kelola Pemerintahan", "Perencanaan Pembangunan", "Perencanaan Partisipatif Kewilayahan"),
    ("Penyusunan Rencana Kerja Pemerintah Daerah (RKPD) Tingkat Kota Administrasi", "Tata Kelola Pemerintahan", "Perencanaan Pembangunan", "Penyusunan Dokumen Perencanaan Tahunan"),
    ("Pengelolaan Anggaran Kas dan Belanja Operasional Kantor Walikota Jakarta Selatan", "Tata Kelola Pemerintahan", "Keuangan dan Aset Daerah", "Pengelolaan Anggaran dan Perbendaharaan"),
    ("Penatausahaan dan Inventarisasi Barang Milik Daerah (BMD) Jakarta Selatan", "Tata Kelola Pemerintahan", "Keuangan dan Aset Daerah", "Penatausahaan dan Pengamanan Aset Daerah"),
    ("Penyusunan Laporan Akuntabilitas Kinerja Instansi Pemerintah (LAKIP) Kota Administrasi", "Tata Kelola Pemerintahan", "Manajemen Kinerja", "Evaluasi dan Pelaporan Kinerja Instansi"),
    ("Pengelolaan Sistem Informasi Manajemen Kepegawaian ASN Kota Jakarta Selatan", "Tata Kelola Pemerintahan", "Sumber Daya Manusia Aparatur", "Pengelolaan Administrasi Kepegawaian"),
    ("Koordinasi Pembinaan dan Pengawasan Koperasi dan UMKM Binaan Jakpreneur", "Perekonomian Daerah", "Koperasi dan Usaha Mikro", "Pemberdayaan dan Pengembangan Usaha Mikro"),
    ("Pemantauan Stabilitas Harga Kebutuhan Pokok di Pasar Tradisional Jakarta Selatan", "Perekonomian Daerah", "Perdagangan dan Perindustrian", "Pemantauan Distribusi dan Harga Pangan"),
    ("Penyelenggaraan Pelayanan Perizinan dan Non-Perizinan Terpadu di Tingkat Kecamatan", "Pelayanan Publik", "Penanaman Modal dan Pelayanan Terpadu", "Penyelenggaraan Pelayanan Perizinan"),
    ("Pengawasan dan Pengendalian Pemanfaatan Tata Ruang Wilayah Kecamatan/Kelurahan", "Pelayanan Publik", "Penataan Ruang dan Pertanahan", "Pengendalian Pemanfaatan Ruang"),
    ("Penyuluhan dan Pembinaan Pencegahan Stunting Balita di Posyandu Terintegrasi", "Pelayanan Publik", "Kesehatan Masyarakat", "Peningkatan Gizi dan Kesehatan Keluarga"),
    ("Koordinasi Pengelolaan Persampahan Lingkungan dan Operasional Bank Sampah Kelurahan", "Pelayanan Publik", "Lingkungan Hidup", "Pengelolaan dan Pengurangan Sampah Domestik"),
    ("Pengawasan Sanitasi Total Berbasis Masyarakat (STBM) di Tingkat Kelurahan", "Pelayanan Publik", "Kesehatan Lingkungan", "Penyediaan Air Minum dan Penyehatan Lingkungan"),
    ("Koordinasi Penanganan Pemerlu Pelayanan Kesejahteraan Sosial (PPKS) Jalanan", "Pelayanan Publik", "Sosial dan Pemberdayaan", "Rehabilitasi dan Perlindungan Sosial"),
    ("Penyelenggaraan Pos Terpadu Siaga Kebakaran dan Penyelamatan Tingkat Kecamatan", "Pelayanan Publik", "Ketenteraman dan Ketertiban Umum", "Pencegahan dan Pemadaman Kebakaran"),
    ("Pembinaan Administrasi Rukun Tetangga (RT) dan Rukun Warga (RW) se-Jakarta Selatan", "Tata Kelola Pemerintahan", "Otonomi dan Pemerintahan Desa/Kelurahan", "Fasilitasi Lembaga Kemasyarakatan Kelurahan"),
    ("Fasilitasi Penyelenggaraan Forum Kewaspadaan Dini Masyarakat (FKDM) Jakarta Selatan", "Tata Kelola Pemerintahan", "Kesatuan Bangsa dan Politik", "Pemeliharaan Kerukunan dan Kewaspadaan Dini"),
    ("Fasilitasi Pembinaan Pemuda dan Olahraga Prestasi Tingkat Kota Administrasi", "Pelayanan Publik", "Kepemudaan dan Olahraga", "Pemberdayaan Pemuda dan Olahraga Rekreasi"),
    ("Koordinasi Pemeliharaan Ruang Terbuka Hijau (RTH) dan Taman Kota Jakarta Selatan", "Pelayanan Publik", "Lingkungan Hidup dan Kehutanan", "Pengelolaan dan Konservasi Ruang Terbuka Hijau"),
    ("Pengelolaan Kearsipan Dinamis dan Surat Elektronik Terintegrasi (Srikandi/E-Office)", "Tata Kelola Pemerintahan", "Kearsipan dan Dokumentasi", "Pengelolaan Arsip Aktif dan Dinamis"),
    ("Pengelolaan Jaringan Komunikasi Data dan Layanan WiFi Publik Kecamatan/Kelurahan", "Tata Kelola Pemerintahan", "Komunikasi dan Informatika", "Pengelolaan Infrastruktur Jaringan SPBE"),
    ("Penyelenggaraan Sidang Keliling Isbat Nikah Terpadu di Kantor Camat", "Pelayanan Publik", "Kependudukan dan Hukum", "Pelayanan Hak Sipil dan Administrasi Hukum"),
    ("Koordinasi Operasional Pengendalian Lalu Lintas Jalur Utama Jakarta Selatan", "Pelayanan Publik", "Perhubungan dan Transportasi", "Manajemen dan Rekayasa Lalu Lintas"),
    ("Pengawasan Penerapan Kawasan Dilarang Merokok (KDM) di Perkantoran dan Fasos", "Pelayanan Publik", "Kesehatan Lingkungan", "Pengawasan Kebijakan Kesehatan Publik"),
    ("Pengelolaan Bank Data Sektoral Wilayah Jakarta Selatan untuk Satu Data Jakarta", "Tata Kelola Pemerintahan", "Statistik dan Pengelolaan Data", "Pengelolaan dan Diseminasi Data Sektoral"),
    ("Koordinasi Pemantauan dan Evaluasi Kinerja Penyerapan Realisasi Fisik dan Keuangan (TEPRA)", "Tata Kelola Pemerintahan", "Pengawasan dan Evaluasi", "Pengendalian Pelaksanaan Program Daerah"),
    ("Penyelenggaraan Festival Seni Budaya Betawi dan Pariwisata Unggulan Jakarta Selatan", "Perekonomian Daerah", "Kebudayaan dan Pariwisata", "Promosi dan Pengembangan Potensi Wisata Budaya"),
    ("Pengelolaan Program Bantuan Pangan Bersubsidi Bagi Warga Tidak Mampu", "Pelayanan Publik", "Ketahanan Pangan dan Pertanian", "Distribusi Pangan dan Bantuan Sosial"),
    ("Koordinasi Perekaman KTP Elektronik Jemput Bola bagi Disabilitas dan Lansia", "Pelayanan Publik", "Administrasi Kependudukan", "Pelayanan Kependudukan Khusus dan Rentan"),
    ("Pengelolaan Pelayanan Surat Keterangan Ahli Waris dan Domisili Tingkat Kelurahan", "Pelayanan Publik", "Administrasi Kependudukan", "Pelayanan Administrasi Kependudukan Umum"),
    ("Audit Kepatuhan Internal Penyelenggaraan Pelayanan Publik Terpadu Satu Pintu", "Tata Kelola Pemerintahan", "Pengawasan Internal", "Pemeriksaan dan Penjaminan Mutu Pelayanan"),
    ("Evaluasi Tingkat Kepuasan Masyarakat (IKM) Penyelenggaraan Pelayanan Publik Kelurahan", "Tata Kelola Pemerintahan", "Reformasi Birokrasi", "Pengukuran dan Survei Kepuasan Masyarakat")
]

for row_idx, (asis_proc, rab_l1, rab_l2, rab_l3) in enumerate(pb_rows, 2):
    ws_pb.cell(row=row_idx, column=1, value="Proses Bisnis").alignment = ALIGN_CENTER
    ws_pb.cell(row=row_idx, column=2, value="Upgrade").alignment = ALIGN_CENTER
    ws_pb.cell(row=row_idx, column=3, value=asis_proc).alignment = ALIGN_LEFT
    ws_pb.cell(row=row_idx, column=4, value="Kota Administrasi Jakarta Selatan").alignment = ALIGN_LEFT
    ws_pb.cell(row=row_idx, column=5, value=rab_l1).alignment = ALIGN_LEFT
    ws_pb.cell(row=row_idx, column=6, value=rab_l2).alignment = ALIGN_LEFT
    ws_pb.cell(row=row_idx, column=7, value=rab_l3).alignment = ALIGN_LEFT
    
    for c in range(1, 8):
        cell = ws_pb.cell(row=row_idx, column=c)
        cell.font = DATA_FONT
        cell.border = thin_border

# Auto column widths
for col in ws_pb.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws_pb.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 48)


# ==========================================
# 2. SHEET: 21 Layanan_Upgrade
# ==========================================
ws_lay = wb.create_sheet(title="21 Layanan_Upgrade")

lay_headers = [
    "Domain",
    "Kategori Arsitektur To-Be",
    "Nama Layanan As-Is Terkait",
    "Perangkat Daerah *",
    "Referensi Arsitektur Layanan (RAL) Level 1 *",
    "Referensi Arsitektur Layanan (RAL) Level 2 *",
    "Kanal Akses Layanan Terintegrasi *"
]

for col_idx, h_text in enumerate(lay_headers, 1):
    cell = ws_lay.cell(row=1, column=col_idx, value=h_text)
    cell.font = HEADER_FONT
    cell.alignment = ALIGN_CENTER
    cell.border = thin_border
    if col_idx <= 3:
        cell.fill = HEADER_FILL_BLUE
    else:
        cell.fill = HEADER_FILL_YELLOW

lay_rows = [
    ("Layanan Pendaftaran Penduduk dan Pencatatan Sipil Daring", "Layanan Administrasi Kependudukan", "Layanan Publik Eksternal", "Aplikasi Alpukat Betawi / JAKI"),
    ("Layanan Pengaduan Warga Cepat Respon Masyarakat (CRM)", "Layanan Pengelolaan Pengaduan Publik", "Layanan Publik Eksternal", "Portal CRM / Aplikasi JAKI"),
    ("Layanan Perizinan Praktik Tenaga Kesehatan Mandiri di PTSP Kecamatan", "Layanan Perizinan dan Non-Perizinan", "Layanan Publik Eksternal", "Portal JakEVO PTSP"),
    ("Layanan Penerbitan Surat Keterangan Domisili Usaha / Yayasan Non-Izin", "Layanan Administrasi Kelurahan", "Layanan Publik Eksternal", "Sistem Informasi Kelurahan / PTSP"),
    ("Layanan Permohonan Fasilitas Penanganan Banjir dan Pompa Portabel", "Layanan Penanganan Darurat Bencana", "Layanan Publik Eksternal", "Jakarta Siaga 112 / JAKI"),
    ("Layanan Pengajuan Bantuan Santunan Duka dan PMKS Terlantar", "Layanan Perlindungan dan Jaminan Sosial", "Layanan Publik Eksternal", "Dinas Sosial / Kelurahan"),
    ("Layanan Konsultasi dan Pendampingan Wirausaha Jakpreneur Jaksel", "Layanan Pemberdayaan Ekonomi & UMKM", "Layanan Publik Eksternal", "Portal Jakpreneur DKI"),
    ("Layanan Pemeriksaan Kelaikan Bangunan dan Izin Mendirikan Bangunan (PBG)", "Layanan Penataan Ruang & Bangunan", "Layanan Publik Eksternal", "SIMBG / JakEVO"),
    ("Layanan Pembinaan Posyandu dan Kartu Peduli Anak Stunting", "Layanan Kesehatan Masyarakat Berbasis Komunitas", "Layanan Publik Eksternal", "Aplikasi e-Jiwa / Dinkes"),
    ("Layanan Permohonan Penertiban Gangguan Trantibum Wilayah", "Layanan Penegakan Perda & Ketertiban", "Layanan Publik Eksternal", "Satpol PP DKI / CRM"),
    ("Layanan Peminjaman Gedung Serbaguna dan Fasilitas Olahraga Kecamatan", "Layanan Pemanfaatan Fasilitas Umum", "Layanan Publik Eksternal", "Portal Resmi Pemkot Jaksel"),
    ("Layanan Surat Pengantar Nikah (N1-N4) Tingkat Kelurahan", "Layanan Administrasi Kependudukan Umum", "Layanan Publik Eksternal", "Alpukat Betawi / Kelurahan"),
    ("Layanan Pengajuan Beasiswa Kartu Jakarta Pintar (KJP Plus) Wilayah", "Layanan Bantuan Pendidikan Daerah", "Layanan Publik Eksternal", "P4OP Disdik DKI / Kelurahan"),
    ("Layanan Rekomendasi Bantuan Rumah Tidak Layak Huni (Bedah Rumah Baznas)", "Layanan Bantuan Perumahan Rakyat", "Layanan Publik Eksternal", "Baznas Bazis DKI / Kelurahan"),
    ("Layanan Sertifikasi Halal Gratis bagi Pelaku Usaha Mikro Binaan", "Layanan Pembinaan Sertifikasi Usaha", "Layanan Publik Eksternal", "Jakpreneur / BPJPH"),
    ("Layanan Sistem Presensi Elektronik Terintegrasi ASN (E-Absensi)", "Layanan Administrasi Kepegawaian Internal", "Layanan Administrasi Pemerintahan", "Aplikasi Mobile E-Presensi"),
    ("Layanan Penatausahaan Keuangan Daerah Digital (SIPD-RI / E-BLUD)", "Layanan Manajemen Keuangan dan Aset Daerah", "Layanan Administrasi Pemerintahan", "SIPD Penatausahaan"),
    ("Layanan Tata Naskah Dinas Elektronik Terintegrasi (E-Office Srikandi)", "Layanan Kearsipan & Korespondensi Dinas", "Layanan Administrasi Pemerintahan", "Aplikasi Srikandi Nasional"),
    ("Layanan Rapat Koordinasi dan Streaming Terbuka Dewan Pimpinan Kota", "Layanan Kolaborasi dan Konferensi Digital", "Layanan Administrasi Pemerintahan", "Zoom Enterprise / Smart Office"),
    ("Layanan Manajemen Pengadaan Barang/Jasa Terintegrasi LPSE", "Layanan Pengadaan dan Pengelolaan Kontrak", "Layanan Administrasi Pemerintahan", "LPSE DKI / SPSE"),
    ("Layanan Dasbor Pemantauan Indikator Kinerja Wilayah (Executive Dashboard)", "Layanan Analitik dan Intelijen Pemerintahan", "Layanan Administrasi Pemerintahan", "NEXUS Executive Portal")
]

for row_idx, (lay_name, ral_l1, ral_l2, kanal) in enumerate(lay_rows, 2):
    ws_lay.cell(row=row_idx, column=1, value="Layanan").alignment = ALIGN_CENTER
    ws_lay.cell(row=row_idx, column=2, value="Upgrade").alignment = ALIGN_CENTER
    ws_lay.cell(row=row_idx, column=3, value=lay_name).alignment = ALIGN_LEFT
    ws_lay.cell(row=row_idx, column=4, value="Kota Administrasi Jakarta Selatan").alignment = ALIGN_LEFT
    ws_lay.cell(row=row_idx, column=5, value=ral_l1).alignment = ALIGN_LEFT
    ws_lay.cell(row=row_idx, column=6, value=ral_l2).alignment = ALIGN_LEFT
    ws_lay.cell(row=row_idx, column=7, value=kanal).alignment = ALIGN_LEFT
    
    for c in range(1, 8):
        cell = ws_lay.cell(row=row_idx, column=c)
        cell.font = DATA_FONT
        cell.border = thin_border

for col in ws_lay.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws_lay.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 48)

wb.save(OUTPUT_FILE)
print(f"[SUCCESS] File spreadsheet terisi lengkap berhasil dibuat di: {OUTPUT_FILE}")
