# LAPORAN PEMETAAN ARSITEKTUR SPBE 22 PERANGKAT DAERAH PEMPROV DKI JAKARTA
## Integrasi Layanan Publik, Tata Kelola Pemerintahan, dan Proses Bisnis Lintas 22 OPD

> **Otoritas Pelaksana:** NEXUS AI ENTERPRISE (ARKA, RAKA, SEKAR, DIMAS, NAYA)  
> **Status Dokumen:** SELESAI & TERVERIFIKASI (100% Terisi Seluruh 22 Perangkat Daerah)  
> **Format Output:** Microsoft Excel Standar Nasional KemenPANRB (`.xlsx`) & Dasbor Eksekutif  
> **Lokasi File:** [`output/spreadsheets/LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/LAPORAN_AUDIT_LENGKAP_SPBE_DKI_JAKARTA.xlsx)  
> **Template Khusus 22 OPD:** [`output/spreadsheets/03C_TOBE_ASIS_22_PERANGKAT_DAERAH_TERISI.xlsx`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/NEXUS-AI-ENTERPRISE/output/spreadsheets/03C_TOBE_ASIS_22_PERANGKAT_DAERAH_TERISI.xlsx)

---

### 1. LATAR BELAKANG PENYESUAIAN ARSITEKTUR
Berdasarkan arahan pimpinan, pemetaan arsitektur layanan SPBE To-Be tidak boleh terkonsentrasi hanya pada satu wilayah administratif (seperti Kota Administrasi Jakarta Selatan), melainkan **wajib mencakup seluruh 22 Perangkat Daerah (Dinas, Badan, Biro, dan Satuan Kerja Wilayah)** di lingkungan Pemerintah Provinsi DKI Jakarta.

Setiap Perangkat Daerah memiliki tugas pokok dan fungsi (tupoksi) yang berbeda serta portofolio layanan digital spesifik yang wajib dipetakan ke dalam:
1. **Referensi Arsitektur Layanan (RAL) Nasional Level 1 & 2** (PermenPANRB No. 59/2020)
2. **Referensi Arsitektur Bisnis (RAB) Nasional Level 1, 2, & 3** (KepmenPANRB SPBE)
3. **Kanal Akses Layanan Terintegrasi** (JAKI, JakEVO, Alpukat Betawi, Srikandi, SIPD, dsb.)

---

### 2. MATRIKS 22 PERANGKAT DAERAH & LAYANAN DIGITAL UNGGULAN (RAL)
Seluruh 22 entitas berikut kini telah terisi secara mandiri dan jelas di Kolom D (*Perangkat Daerah \**) pada lembar kerja **`22 Layanan (22 OPD)`**:

| No | Perangkat Daerah | Nama Layanan As-Is Terkait | Referensi Arsitektur Layanan (RAL) L1 | Kanal Akses Terintegrasi |
|:--:|:---|:---|:---|:---|
| 1 | **Dinas Pendidikan** | Layanan Bantuan Biaya Personal Pendidikan Siswa (KJP Plus & KJMU) | Layanan Bantuan Pendidikan Daerah | Portal P4OP Disdik / JAKI |
| 2 | **Dinas Kesehatan** | Layanan Antrean Faskes Daring, e-Jiwa & Deteksi Stunting (JakSehat) | Layanan Kesehatan Masyarakat Berbasis Komunitas | Aplikasi JakSehat / Portal Dinkes / JAKI |
| 3 | **Dinas Komunikasi, Informatika dan Statistik** | Layanan Portal Warga Terpadu & Penanganan Cepat (JAKI & CRM) | Layanan Pengelolaan Pengaduan Publik SPBE | Portal JAKI / CRM Pemprov DKI |
| 4 | **Dinas Perhubungan** | Layanan Integrasi Tiket Transportasi Multi-Moda (JakLingko) | Layanan Transportasi dan Mobilitas Perkotaan | Aplikasi JakLingko / Kiosk Stasiun |
| 5 | **Satuan Polisi Pamong Praja** | Layanan Permohonan Penertiban Gangguan Ketenteraman & Ketertiban (Trantibum) | Layanan Penegakan Perda & Ketertiban Umum | Aplikasi JAKI / Call Center Satpol PP |
| 6 | **Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu** | Layanan Perizinan Berusaha Berbasis Risiko & Investasi (JakEVO / OSS) | Layanan Perizinan dan Non-Perizinan Terpadu | Portal JakEVO PTSP / OSS Nasional |
| 7 | **Dinas Kependudukan dan Pencatatan Sipil** | Layanan Administrasi Kependudukan, Akta & KTP Digital (Alpukat Betawi) | Layanan Administrasi Kependudukan | Aplikasi Alpukat Betawi / IKD Kemendagri |
| 8 | **Dinas Sosial** | Layanan Pendaftaran PPKS & Bansos Kluster (KLJ, KPDJ, Anak Yatim) | Layanan Perlindungan dan Jaminan Sosial | Portal Bansos Dinsos / JAKI |
| 9 | **Badan Perencanaan Pembangunan Daerah** | Layanan Partisipasi Musrenbang Daring & Aspirasi RKPD Warga | Layanan Perencanaan Pembangunan Daerah | Portal Musrenbang DKI / SIPD-RI |
| 10 | **Badan Pengelolaan Keuangan Daerah** | Layanan Penerbitan SP2D Elektronik & e-BLUD Terintegrasi | Layanan Manajemen Keuangan dan Anggaran Daerah | Portal SIPD Penatausahaan / Bank DKI CMS |
| 11 | **Badan Pengelolaan Aset Daerah** | Layanan Penatausahaan & Pemanfaatan Barang Milik Daerah (SIMBADA / Si-Aset) | Layanan Pengelolaan Aset Daerah | Portal SIMBADA DKI / Si-Aset Mobile |
| 12 | **Badan Pelayanan Pengadaan Barang/Jasa** | Layanan Pengadaan Barang dan Jasa Pemerintah Secara Elektronik (SPSE) | Layanan Pengadaan Barang/Jasa Elektronik | Portal LPSE Pemprov DKI / e-Katalog |
| 13 | **Dinas Sumber Daya Air** | Layanan Peringatan Dini Banjir, Pintu Air & Posko Pompa Daring | Layanan Sumber Daya Air & Pengendalian Banjir | Portal Pantau Banjir Jakarta / JAKI |
| 14 | **Dinas Bina Marga** | Layanan Pengaduan Jalan Berlubang & Penerangan Jalan Umum (PJU Daring) | Layanan Infrastruktur Jalan dan Jembatan | Aplikasi CRM / JAKI / Si-Jalan DBM |
| 15 | **Dinas Lingkungan Hidup** | Layanan Pendaftaran Uji Emisi Kendaraan Bermotor & Bank Sampah Digital | Layanan Pengelolaan Lingkungan Hidup | Aplikasi e-Uji Emisi / Portal DLH |
| 16 | **Dinas Cipta Karya, Tata Ruang dan Pertanahan** | Layanan Persetujuan Bangunan Gedung (PBG) & IRK Daring (SIMBG) | Layanan Penataan Ruang dan Bangunan Gedung | Sistem SIMBG Terpadu / JakEVO |
| 17 | **Dinas Tenaga Kerja, Transmigrasi dan Energi** | Layanan Bursa Kerja Daring & Pelatihan Vokasi PPKD (Jaknaker) | Layanan Ketenagakerjaan dan Pelatihan Vokasi | Portal Jaknaker / Aplikasi JAKI |
| 18 | **Dinas Penanggulangan Kebakaran dan Penyelamatan** | Layanan Tanggap Darurat Pemadaman Kebakaran & Penyelamatan Non-Kebakaran | Layanan Tanggap Darurat Kebakaran | Jakarta Siaga 112 / Command Center |
| 19 | **Badan Penanggulangan Bencana Daerah** | Layanan Peringatan Dini Kebencanaan (DEWS) & Bantuan Logistik Bencana | Layanan Penanggulangan Bencana & Kedaruratan | Portal Pusdalops BPBD / JAKI |
| 20 | **Inspektorat Provinsi DKI Jakarta** | Layanan Pengaduan Penyimpangan Pegawai & Whistleblowing System (WBS) | Layanan Pengawasan Internal & Whistleblowing | Portal WBS Inspektorat / Portal KPK |
| 21 | **Dinas Perindustrian, Perdagangan, Koperasi, UKM** | Layanan Inkubasi Bisnis, Sertifikasi Halal & Akses Modal (Jakpreneur) | Layanan Pemberdayaan Koperasi & Usaha Mikro | Portal Jakpreneur PPKUKM / JAKI |
| 22 | **Kota Administrasi Jakarta Selatan & Kewilayahan** | Layanan Administrasi Kewilayahan Terpadu Kelurahan & Layanan RT/RW | Layanan Administrasi Pemerintahan Kewilayahan | SIM Kelurahan / Portal Pemkot / JAKI |

---

### 3. MATRIKS 44 PROSES BISNIS LINTAS 22 PERANGKAT DAERAH (RAB)
Pada lembar kerja **`44 ProsesBisnis (22 OPD)`**, masing-masing dari 22 Perangkat Daerah telah memiliki 2 proses bisnis strategis:
1. **Dinas Pendidikan:** Verifikasi Penerima Bantuan Sekolah & Penyelenggaraan PPDB Daring Terpusat.
2. **Dinas Kesehatan:** Pengelolaan Sistem Rujukan Puskesmas-RSUD & Surveilans Epidemiologi KLB Penyakit.
3. **Diskominfotik:** Integrasi Interoperabilitas SPLP & Pengelolaan JSC Command Center SPBE.
4. **Dinas Perhubungan:** Pengujian Berkala Kelaikan Kendaraan (e-KIR) & Rekayasa Lalu Lintas ETLE.
5. **Satpol PP:** Operasi Penertiban Perda/Pergub & Patroli Cipta Kondisi Kawasan Publik.
6. **DPMPTSP:** Pemrosesan Izin Usaha Risiko & Fasilitasi Investasi Antar Jemput Izin Berusaha (AJIB).
7. **Disdukcapil:** Penerbitan KTP-el/KIA/Akta Sipil Daring & Penyelarasan Database SIAK Terpusat.
8. **Dinas Sosial:** Pemutakhiran DTKS RT/RW/Kelurahan & Penyaluran Bansos Perlindungan Lansia/Anak.
9. **Bappeda:** Penyusunan Dokumen RKPD/Renstra Daerah & Evaluasi Kinerja Pembangunan (e-Monev).
10. **BPKD:** Penatausahaan Kas Daerah (SP2D Daring) & Penyusunan LKPD Akrual Konsolidasian.
11. **BPAD:** Sensus Inventarisasi Aset Tetap SKPD & Pengamanan Yuridis Aset Pemprov DKI.
12. **BPPBJ:** Penyelenggaraan Tender Pengadaan SPSE Daring & Kurasi Produk UMKM e-Katalog Lokal.
13. **Dinas Sumber Daya Air:** Operasional Sistem Polder/Rumah Pompa & Pengerukan Normalisasi Sungai.
14. **Dinas Bina Marga:** Pemeliharaan Rutin Flyover/Underpass & Penataan Kabel Bawah Tanah SJUT.
15. **Dinas Lingkungan Hidup:** Logistik Pengolahan Sampah RDF Plant & Pengawasan Baku Mutu Udara Ambien.
16. **Dinas Citata:** Sidang Tim Ahli Bangunan Gedung (TABG) & Penyusunan RDTR Digital Interaktif.
17. **Disnakertransgi:** Mediasi Perselisihan Hak Pekerja & Pelatihan Sertifikasi Kerja Kejuruan PPKD.
18. **Disgulkarmat:** Operasi Taktis Pemadaman Kebakaran Permukiman & Audit Sistem Proteksi Kebakaran Gedung.
19. **BPBD:** Mobilisasi Tim Reaksi Cepat (TRC) Bencana & Penyaluran Logistik Tenda Pengungsian.
20. **Inspektorat:** Audit Kepatuhan AKIP SKPD & Pemeriksaan Khusus Tindak Lanjut Rekomendasi BPK.
21. **Dinas PPKUKM:** 7 Tahap Inkubasi Usaha Jakpreneur & Operasi Pasar Murah Stabilisasi Pangan.
22. **Kota Administrasi & Wilayah:** Fasilitasi Kerukunan Warga RT/RW/FKDM & Operasional Pasukan Oranye (PPSU).

---

### 4. PENJELASAN DESAIN SPREADSHEET (STANDAR RAPI & NYAMAN DIBACA)
1. **Lebar Kolom Proporsional (Anti-Terpotong):**
   - Kolom Perangkat Daerah: Lebar `44` (nama instansi utuh terbaca).
   - Kolom Nama Layanan / Proses Bisnis: Lebar `54` (rincian kegiatan tidak terpotong).
   - Kolom Referensi Arsitektur: Lebar `30 - 50` (kode taksonomi nasional nyaman dilihat).
2. **Tinggi Baris Dinamis (Anti-Tumpang Tindih):**
   - Setiap baris memiliki tinggi minimal `26pt` hingga `120pt` sesuai kalkulasi pembungkusan teks (*text wrap*), memastikan tidak ada teks yang menimpa garis batas sel.
3. **Perataan Vertikal Top (*Top-Aligned*):**
   - Semua sel data diatur rata atas (*vertical top*), sesuai standar baca dokumen hukum dan audit pemerintah.
4. **Zebra Striping Elegan:**
   - Baris genap menggunakan warna lembut `#F8FAFC` (Cool Slate) dan baris ganjil putih bersih `#FFFFFF` untuk kenyamanan visual pimpinan saat memeriksa dokumen panjang.
5. **Header Berwarna Pastel:**
   - Header biru pastel (`#9BC2E6`) dan kuning pastel (`#FEF08A`) dengan teks hitam tebal kontras tinggi.

---

### 5. STATUS GUARDRAIL DAN VERIFIKASI KEAMANAN
- Seluruh data yang digenerasikan **tersimpan secara aman di repositori lokal** dan diekspor ke Microsoft Excel resmi.
- Sistem mematuhi **Zero-Mutation Guardrail**: tidak melakukan modifikasi atau penghapusan data pada tautan Google Drive / Google Sheets online milik pemerintah.
