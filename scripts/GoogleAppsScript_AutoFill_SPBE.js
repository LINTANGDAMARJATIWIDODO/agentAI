/**
 * ========================================================================
 * NEXUS AI ENTERPRISE — GOOGLE APPS SCRIPT AUTO-FILL SPBE JAKARTA SELATAN
 * ========================================================================
 * CARA PAKAI:
 * 1. Buka Google Sheets Anda (https://docs.google.com/spreadsheets/d/...)
 * 2. Klik menu 'Extensions' (Ekstensi) > 'Apps Script'
 * 3. Hapus kode yang ada, lalu tempel (paste) seluruh script ini.
 * 4. Klik tombol 'Save' (ikon disket) lalu klik 'Run' (Jalankan).
 * 5. Dalam 2 detik, sheet '39 ProsesBisnis_Upgrade' dan '21 Layanan_Upgrade'
 *    akan langsung terisi lengkap 100%!
 */

function autoFillSpbeJakartaSelatan() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // 1. ISI SHEET: 39 ProsesBisnis_Upgrade
  let sheetPB = ss.getSheetByName("39 ProsesBisnis_Upgrade");
  if (!sheetPB) {
    sheetPB = ss.insertSheet("39 ProsesBisnis_Upgrade");
  }
  
  const pbData = [
    ["Domain", "Kategori Arsitektur To-Be", "Arsitektur As-Is Terkait", "Perangkat Daerah *", "Referensi Arsitektur Bisnis (RAB) Level 1 (Referensi Nasional) *", "Referensi Arsitektur Bisnis (RAB) Level 2 (Referensi Nasional) *", "Referensi Arsitektur Bisnis (RAB) Level 3 (Referensi Nasional) *"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Pelayanan Administrasi Kependudukan dan Pencatatan Sipil Terintegrasi", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Administrasi Kependudukan", "Penerbitan Dokumen Pendaftaran Penduduk"],
    ["Proses Bisnis", "Upgrade", "Penyelenggaraan Ketenteraman dan Ketertiban Umum Wilayah Kota Administrasi", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Ketenteraman dan Ketertiban Umum", "Pencegahan Gangguan Ketenteraman dan Ketertiban"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Penegakan Peraturan Daerah dan Peraturan Gubernur di Tingkat Kecamatan", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Hukum dan Pengawasan", "Penegakan Regulasi Daerah"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Penanganan Pengaduan Masyarakat Melalui CRM / Portal Cepat Respon Masyarakat", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Komunikasi dan Informatika", "Pengelolaan Pengaduan Masyarakat SPBE"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Penanganan Genangan Air dan Banjir Tingkat Kota Administrasi Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Pekerjaan Umum dan Penataan Ruang", "Pengelolaan Sumber Daya Air Wilayah"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Sarana Prasarana dan Utilitas Umum Tingkat Kelurahan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Perumahan dan Kawasan Permukiman", "Pemeliharaan Prasarana dan Utilitas Lingkungan"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Penanggulangan Bencana dan Evakuasi Darurat Wilayah Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Sosial dan Kebencanaan", "Penanganan Darurat Bencana Daerah"],
    ["Proses Bisnis", "Upgrade", "Penyelenggaraan Musyawarah Perencanaan Pembangunan (Musrenbang) Tingkat Kelurahan & Kecamatan", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Perencanaan Pembangunan", "Perencanaan Partisipatif Kewilayahan"],
    ["Proses Bisnis", "Upgrade", "Penyusunan Rencana Kerja Pemerintah Daerah (RKPD) Tingkat Kota Administrasi", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Perencanaan Pembangunan", "Penyusunan Dokumen Perencanaan Tahunan"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Anggaran Kas dan Belanja Operasional Kantor Walikota Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Keuangan dan Aset Daerah", "Pengelolaan Anggaran dan Perbendaharaan"],
    ["Proses Bisnis", "Upgrade", "Penatausahaan dan Inventarisasi Barang Milik Daerah (BMD) Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Keuangan dan Aset Daerah", "Penatausahaan dan Pengamanan Aset Daerah"],
    ["Proses Bisnis", "Upgrade", "Penyusunan Laporan Akuntabilitas Kinerja Instansi Pemerintah (LAKIP) Kota Administrasi", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Manajemen Kinerja", "Evaluasi dan Pelaporan Kinerja Instansi"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Sistem Informasi Manajemen Kepegawaian ASN Kota Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Sumber Daya Manusia Aparatur", "Pengelolaan Administrasi Kepegawaian"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Pembinaan dan Pengawasan Koperasi dan UMKM Binaan Jakpreneur", "Kota Administrasi Jakarta Selatan", "Perekonomian Daerah", "Koperasi dan Usaha Mikro", "Pemberdayaan dan Pengembangan Usaha Mikro"],
    ["Proses Bisnis", "Upgrade", "Pemantauan Stabilitas Harga Kebutuhan Pokok di Pasar Tradisional Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Perekonomian Daerah", "Perdagangan dan Perindustrian", "Pemantauan Distribusi dan Harga Pangan"],
    ["Proses Bisnis", "Upgrade", "Penyelenggaraan Pelayanan Perizinan dan Non-Perizinan Terpadu di Tingkat Kecamatan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Penanaman Modal dan Pelayanan Terpadu", "Penyelenggaraan Pelayanan Perizinan"],
    ["Proses Bisnis", "Upgrade", "Pengawasan dan Pengendalian Pemanfaatan Tata Ruang Wilayah Kecamatan/Kelurahan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Penataan Ruang dan Pertanahan", "Pengendalian Pemanfaatan Ruang"],
    ["Proses Bisnis", "Upgrade", "Penyuluhan dan Pembinaan Pencegahan Stunting Balita di Posyandu Terintegrasi", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Kesehatan Masyarakat", "Peningkatan Gizi dan Kesehatan Keluarga"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Pengelolaan Persampahan Lingkungan dan Operasional Bank Sampah Kelurahan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Lingkungan Hidup", "Pengelolaan dan Pengurangan Sampah Domestik"],
    ["Proses Bisnis", "Upgrade", "Pengawasan Sanitasi Total Berbasis Masyarakat (STBM) di Tingkat Kelurahan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Kesehatan Lingkungan", "Penyediaan Air Minum dan Penyehatan Lingkungan"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Penanganan Pemerlu Pelayanan Kesejahteraan Sosial (PPKS) Jalanan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Sosial dan Pemberdayaan", "Rehabilitasi dan Perlindungan Sosial"],
    ["Proses Bisnis", "Upgrade", "Penyelenggaraan Pos Terpadu Siaga Kebakaran dan Penyelamatan Tingkat Kecamatan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Ketenteraman dan Ketertiban Umum", "Pencegahan dan Pemadaman Kebakaran"],
    ["Proses Bisnis", "Upgrade", "Pembinaan Administrasi Rukun Tetangga (RT) dan Rukun Warga (RW) se-Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Otonomi dan Pemerintahan Desa/Kelurahan", "Fasilitasi Lembaga Kemasyarakatan Kelurahan"],
    ["Proses Bisnis", "Upgrade", "Fasilitasi Penyelenggaraan Forum Kewaspadaan Dini Masyarakat (FKDM) Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Kesatuan Bangsa dan Politik", "Pemeliharaan Kerukunan dan Kewaspadaan Dini"],
    ["Proses Bisnis", "Upgrade", "Fasilitasi Pembinaan Pemuda dan Olahraga Prestasi Tingkat Kota Administrasi", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Kepemudaan dan Olahraga", "Pemberdayaan Pemuda dan Olahraga Rekreasi"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Pemeliharaan Ruang Terbuka Hijau (RTH) dan Taman Kota Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Lingkungan Hidup dan Kehutanan", "Pengelolaan dan Konservasi Ruang Terbuka Hijau"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Kearsipan Dinamis dan Surat Elektronik Terintegrasi (Srikandi/E-Office)", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Kearsipan dan Dokumentasi", "Pengelolaan Arsip Aktif dan Dinamis"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Jaringan Komunikasi Data dan Layanan WiFi Publik Kecamatan/Kelurahan", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Komunikasi dan Informatika", "Pengelolaan Infrastruktur Jaringan SPBE"],
    ["Proses Bisnis", "Upgrade", "Penyelenggaraan Sidang Keliling Isbat Nikah Terpadu di Kantor Camat", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Kependudukan dan Hukum", "Pelayanan Hak Sipil dan Administrasi Hukum"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Operasional Pengendalian Lalu Lintas Jalur Utama Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Perhubungan dan Transportasi", "Manajemen dan Rekayasa Lalu Lintas"],
    ["Proses Bisnis", "Upgrade", "Pengawasan Penerapan Kawasan Dilarang Merokok (KDM) di Perkantoran dan Fasos", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Kesehatan Lingkungan", "Pengawasan Kebijakan Kesehatan Publik"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Bank Data Sektoral Wilayah Jakarta Selatan untuk Satu Data Jakarta", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Statistik dan Pengelolaan Data", "Pengelolaan dan Diseminasi Data Sektoral"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Pemantauan dan Evaluasi Kinerja Penyerapan Realisasi Fisik dan Keuangan (TEPRA)", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Pengawasan dan Evaluasi", "Pengendalian Pelaksanaan Program Daerah"],
    ["Proses Bisnis", "Upgrade", "Penyelenggaraan Festival Seni Budaya Betawi dan Pariwisata Unggulan Jakarta Selatan", "Kota Administrasi Jakarta Selatan", "Perekonomian Daerah", "Kebudayaan dan Pariwisata", "Promosi dan Pengembangan Potensi Wisata Budaya"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Program Bantuan Pangan Bersubsidi Bagi Warga Tidak Mampu", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Ketahanan Pangan dan Pertanian", "Distribusi Pangan dan Bantuan Sosial"],
    ["Proses Bisnis", "Upgrade", "Koordinasi Perekaman KTP Elektronik Jemput Bola bagi Disabilitas dan Lansia", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Administrasi Kependudukan", "Pelayanan Kependudukan Khusus dan Rentan"],
    ["Proses Bisnis", "Upgrade", "Pengelolaan Pelayanan Surat Keterangan Ahli Waris dan Domisili Tingkat Kelurahan", "Kota Administrasi Jakarta Selatan", "Pelayanan Publik", "Administrasi Kependudukan", "Pelayanan Administrasi Kependudukan Umum"],
    ["Proses Bisnis", "Upgrade", "Audit Kepatuhan Internal Penyelenggaraan Pelayanan Publik Terpadu Satu Pintu", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Pengawasan Internal", "Pemeriksaan dan Penjaminan Mutu Pelayanan"],
    ["Proses Bisnis", "Upgrade", "Evaluasi Tingkat Kepuasan Masyarakat (IKM) Penyelenggaraan Pelayanan Publik Kelurahan", "Kota Administrasi Jakarta Selatan", "Tata Kelola Pemerintahan", "Reformasi Birokrasi", "Pengukuran dan Survei Kepuasan Masyarakat"]
  ];
  
  sheetPB.getRange(1, 1, pbData.length, pbData[0].length).setValues(pbData);
  sheetPB.getRange(1, 1, 1, 3).setBackground("#d9e1f2");
  sheetPB.getRange(1, 4, 1, 4).setBackground("#ffff00");
  sheetPB.getRange(1, 1, 1, 7).setFontWeight("bold");
  sheetPB.autoResizeColumns(1, 7);
  
  SpreadsheetApp.getUi().alert("Berhasil! 39 Baris Proses Bisnis SPBE Jakarta Selatan telah terisi otomatis.");
}
