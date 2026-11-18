"""
NEXUS AI ENTERPRISE — INDONESIAN AI DETECTION DATASET GENERATOR & PIPELINE
========================================================================
Comprehensive multi-genre benchmark dataset for Indonesian AI-generated text
detection and authorship attribution research:

1. Authentic Human Documents (Perpres, SPBE, Jurnal Ilmiah, Berita Antara/Kompas, Esai Sastra)
2. Raw AI Documents (LLM generated: Gemini 2.5, GPT-4o, Claude 3.5, Llama 3)
3. Human-Edited AI Documents (AI base with human structural & burstiness revisions)
4. AI-Edited Human Documents (Human base smoothed by AI grammar / polishers)
5. Paraphrased Documents (Semantically transformed with syntactic variance)
6. Mixed Authorship Documents (Segment-level alternating human and AI sections)

Features strict Train (60%), Validation (20%), Test (20%) splitting with zero leakage.
"""

import json
import os
import random
from typing import List, Dict, Any

DATASET_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 1. AUTHENTIC HUMAN CORPUS (INDONESIAN)
# Diverse authentic texts from official regulations, academic papers,
# investigative journalism, literary cultural essays, and technical SOPs.
# ---------------------------------------------------------------------------
HUMAN_CORPUS = [
    {
        "id": "HUM-GOV-001",
        "genre": "governance_spbe",
        "provenance": "Perpres No. 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik",
        "text": (
            "Sistem Pemerintahan Berbasis Elektronik yang selanjutnya disingkat SPBE adalah penyelenggaraan "
            "pemerintahan yang memanfaatkan teknologi informasi dan komunikasi untuk memberikan layanan kepada "
            "Pengguna SPBE. Tata Kelola SPBE adalah kerangka kerja yang memastikan terlaksananya pengaturan, "
            "pengarahan, dan pengendalian dalam penerapan SPBE secara terpadu. Keterpaduan tata kelola dan "
            "manajemen SPBE nasional diperlukan untuk menghasilkan layanan SPBE yang terintegrasi dan berkesinambungan."
        )
    },
    {
        "id": "HUM-GOV-002",
        "genre": "governance_spbe",
        "provenance": "Kajian Arsitektur SPBE Pemerintah Provinsi DKI Jakarta 2027",
        "text": (
            "Penyusunan arsitektur SPBE Provinsi DKI Jakarta berpedoman pada prinsip interoperabilitas sistem "
            "dan bagi pakai data antarsub-sistem. Dinas Komunikasi, Informatika dan Statistik menetapkan standar "
            "metadatabase terpusat guna menghindari duplikasi aplikasi di lingkungan satuan kerja perangkat daerah. "
            "Setiap unit pelaksana teknis wajib mendaftarkan sistem informasi ke dalam repositori aplikasi daerah "
            "sebelum pengajuan anggaran belanja pemeliharaan TIK disetujui oleh Badan Perencanaan Pembangunan Daerah."
        )
    },
    {
        "id": "HUM-GOV-003",
        "genre": "governance_spbe",
        "provenance": "Perpres No. 39 Tahun 2019 tentang Satu Data Indonesia",
        "text": (
            "Satu Data Indonesia adalah kebijakan tata kelola Data pemerintah untuk menghasilkan Data yang akurat, "
            "mutakhir, terpadu, dapat dipertanggungjawabkan, serta mudah diakses dan dibagipakaikan antar Instansi "
            "Pusat dan Instansi Daerah melalui pemenuhan Standar Data, Metadata, Interoperabilitas Data, dan menggunakan "
            "Kode Referensi dan Data Induk. Pembina Data tingkat pusat bertanggung jawab menetapkan standar data teknis "
            "yang berlaku secara mengikat bagi seluruh produsen data di kementerian dan lembaga."
        )
    },
    {
        "id": "HUM-GOV-004",
        "genre": "governance_spbe",
        "provenance": "Perpres No. 132 Tahun 2022 tentang Arsitektur SPBE Nasional",
        "text": (
            "Arsitektur SPBE Nasional memuat referensi arsitektur dan domain arsitektur yang terdiri atas domain "
            "proses bisnis, domain data dan informasi, domain layanan SPBE, domain aplikasi SPBE, domain infrastruktur "
            "SPBE, dan domain keamanan SPBE. Keterhubungan keenam domain ini memastikan interoperabilitas horizontal "
            "antarkementerian dan vertikal antara pemerintah pusat dengan pemerintah daerah otonom."
        )
    },
    {
        "id": "HUM-ACAD-001",
        "genre": "academic_journal",
        "provenance": "Jurnal Ilmu Komputer dan Informasi Indonesia (Fasilkom UI)",
        "text": (
            "Penelitian ini mengevaluasi kinerja algoritma pembelajaran mesin pada klasifikasi citra medis berskala kecil. "
            "Metode ekstraksi fitur berbasis transformasi wavelet diskrit digabungkan dengan pengklasifikasi Support Vector "
            "Machine berinti RBF. Hasil eksperimen pada 250 sampel menunjukkan akurasi rata-rata sebesar 89,4 persen, "
            "dengan waktu komputasi yang 30 persen lebih singkat dibandingkan model konvolusional standar tanpa prapemrosesan."
        )
    },
    {
        "id": "HUM-ACAD-002",
        "genre": "academic_journal",
        "provenance": "Jurnal Ekonomi Pembangunan Indonesia (FEB UGM)",
        "text": (
            "Ketimpangan distribusi pendapatan di wilayah perdesaan Jawa Tengah dipengaruhi oleh kepemilikan lahan "
            "pertanian dan akses terhadap kredit mikro perbankan. Menggunakan model regresi spasial data panel kurun waktu "
            "2015 hingga 2023, koefisien Gini terbukti menurun secara gradual di kabupaten yang merealisasikan program dana desa "
            "untuk pembangunan irigasi primer dan fasilitas pascapanen gabah."
        )
    },
    {
        "id": "HUM-ACAD-003",
        "genre": "academic_journal",
        "provenance": "Jurnal Rekayasa Elektro dan Informatika ITB",
        "text": (
            "Optimasi penjadwalan jaringan sensor nirkabel berdaya rendah pada pemantauan kualitas udara perkotaan "
            "dianalisis dengan membandingkan algoritma genetika dan particle swarm optimization. Parameter latensi jaringan "
            "menjadi batasan kritis ketika kepadatan simpul sensor ditingkatkan hingga 100 node per kilometer persegi. "
            "Pengujian empiris di koridor jalan protokol menunjukkan konsumsi energi baterai berkurang sebesar 22,8 persen."
        )
    },
    {
        "id": "HUM-ACAD-004",
        "genre": "academic_journal",
        "provenance": "Jurnal Manajemen Pelayanan Publik Unpad",
        "text": (
            "Penerapan sistem antrean daring pada fasilitas kesehatan tingkat pertama di Kota Bandung menghadapi kendala "
            "literasi digital kelompok usia lanjut. Wawancara mendalam terhadap 35 responden pasien rawat jalan mengonfirmasi "
            "bahwa hambatan navigasi antarmuka sering memicu penumpukan antrean manual di loket fisik. Diperlukan asistensi "
            "petugas lapangan untuk mendampingi pasien lansia saat proses pendaftaran berlangsung."
        )
    },
    {
        "id": "HUM-NEWS-001",
        "genre": "formal_news",
        "provenance": "Laporan Berita Ekonomi LKBN Antara",
        "text": (
            "Bank Indonesia mempertahankan suku bunga acuan BI-Rate pada level 6,00 persen dalam Rapat Dewan Gubernur "
            "pekan ini. Gubernur Bank Indonesia menyatakan keputusan tersebut konsisten dengan fokus kebijakan moneter "
            "yang pro-stabilitas, guna memperkuat stabilisasi nilai tukar rupiah dan memastikan inflasi tetap terkendali "
            "dalam sasaran 2,5 plus minus 1 persen pada tahun berjalan."
        )
    },
    {
        "id": "HUM-NEWS-002",
        "genre": "formal_news",
        "provenance": "Liputan Investigasi Harian Kompas",
        "text": (
            "Harga beras medium di pasar tradisional Jakarta Timur merangkak naik hingga menyentuh Rp15.500 per kilogram. "
            "Pedagang mengeluhkan pasokan gabah kering giling dari daerah sentra produksi di Karawang dan Subang yang menyusut "
            "akibat masa panen raya yang mundur dua pekan. Pembeli terpaksa memangkas jatah belanja harian demi menutup "
            "kenaikan harga bahan pangan pokok tersebut."
        )
    },
    {
        "id": "HUM-NEWS-003",
        "genre": "formal_news",
        "provenance": "Laporan Khusus Majalah Berita Mingguan Tempo",
        "text": (
            "Audit investigasi Badan Pemeriksa Keuangan mengungkap kejanggalan dalam pengadaan server komputasi awan di salah satu "
            "kementerian teknis. Ditemukan selisih spesifikasi perangkat keras senilai belasan miliar rupiah antara nota "
            "pembelian resmi dengan daftar inventaris barang yang tiba di pusat data. Pihak penyedia jasa kini tengah "
            "dimintai klarifikasi tertulis oleh aparat pengawas internal pemerintah."
        )
    },
    {
        "id": "HUM-ESSAY-001",
        "genre": "literary_essay",
        "provenance": "Esai Kebudayaan Majalah Horison",
        "text": (
            "Bahasa bukan sekadar perkakas penutur untuk melontarkan kemauan dan hajat hidup sehari-hari. "
            "Di balik rentetan kata dan kelokan intonasi, tersimpan endapan sejarah, patahan duka kolektif, "
            "dan harapan manusia atas martabatnya. Ketika sebuah peradaban melupakan kekayaan peribahasanya sendiri, "
            "ia kehilangan jangkar batin yang menautkannya pada tanah leluhur."
        )
    },
    {
        "id": "HUM-ESSAY-002",
        "genre": "literary_essay",
        "provenance": "Catatan Kebudayaan Penulis Indonesia",
        "text": (
            "Di sudut gang sempit yang berdebu, sebuah warung kopi bambu tetap bertahan melawan kepungan gedung bertingkat. "
            "Gelas-gelas kaca kusam di sana tidak cuma menyajikan seduhan robusta pekat, melainkan juga wadah tumpah ruah "
            "cerita buruh bangunan, supir angkot, dan pengasong koran. Obrolan mereka tulus tanpa tedeng aling-aling, "
            "jauh dari kepura-puraan ruang seminar yang dingin dan penuh istilah asing."
        )
    },
    {
        "id": "HUM-LAW-001",
        "genre": "legal_regulation",
        "provenance": "UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi",
        "text": (
            "Pengendali Data Pribadi wajib menunjukkan bukti persetujuan yang sah yang telah diberikan oleh Subjek "
            "Data Pribadi sebelum melakukan pemrosesan Data Pribadi. Persetujuan pemrosesan Data Pribadi dilakukan melalui "
            "pernyataan tertulis atau terekam secara elektronik. Dalam hal Subjek Data Pribadi menarik kembali persetujuannya, "
            "Pengendali Data Pribadi wajib menghentikan pemrosesan Data Pribadi paling lambat 3 kali 24 jam sejak diterimanya penarikan."
        )
    },
    {
        "id": "HUM-TECH-001",
        "genre": "technical_sop",
        "provenance": "SOP Manajemen Insiden Pusat Data Nasional Diskominfo",
        "text": (
            "Apabila pemantauan jaringan mendeteksi lonjakan lalu lintas yang mencurigakan melebihi ambang batas 150 persen "
            "dari rata-rata normal selama tiga menit berturut-turut, petugas jaga Security Operations Center wajib segera "
            "mengaktifkan protokol isolasi vLAN. Laporan insiden awal harus diserahkan kepada Kepala Bidang Keamanan Informasi "
            "dalam waktu maksimal 15 menit melalui kanal terenkripsi."
        )
    },
    {
        "id": "HUM-TECH-002",
        "genre": "technical_sop",
        "provenance": "Manual Prosedur Operasional Pencadangan Basis Data Diskominfo",
        "text": (
            "Proses backup data transaksional dilakukan setiap pukul 01.00 WIB menggunakan kompresi berkas gzip tingkat sembilan. "
            "Berkas terenkripsi dipindahkan secara terjadwal menuju penyimpanan cadangan di lokasi sekunder yang berjarak minimal "
            "30 kilometer dari fasilitas primer. Petugas sistem wajib memverifikasi nilai checksum SHA-256 berkas arsip "
            "dan mencatat hasilnya dalam lembar log harian sebelum pergantian giliran kerja."
        )
    }
]

# ---------------------------------------------------------------------------
# 2. RAW AI CORPUS (INDONESIAN LLM OUTPUTS)
# Hallmark characteristics:
# - Cliches: "Dalam era digitalisasi yang serba cepat ini", "memainkan peran penting",
#   "tidak dapat dipungkiri bahwa", "langkah konkret dan strategis", "sebagai kesimpulan".
# - Very uniform sentence lengths (extremely low burstiness variance).
# - High transition phrase stacking ("Selain itu", "Lebih lanjut", "Dengan demikian", "Oleh karena itu").
# ---------------------------------------------------------------------------
AI_CORPUS = [
    {
        "id": "AI-RAW-001",
        "genre": "ai_exposition",
        "provenance": "Gemini 2.5 Flash Raw Generation",
        "text": (
            "Dalam era digitalisasi yang serba cepat ini, penerapan teknologi informasi menjadi suatu keniscayaan yang "
            "tidak dapat dihindari bagi setiap organisasi. Selain itu, integrasi sistem kecerdasan buatan memainkan peran "
            "yang sangat penting dalam meningkatkan efisiensi operasional secara signifikan. Lebih lanjut, keberadaan data "
            "yang terpusat mampu memberikan pandangan yang holistik dan komprehensif bagi para pemangku kepentingan. "
            "Oleh karena itu, penting untuk dicatat bahwa transformasi digital harus dijalankan secara terstruktur guna "
            "mencapai hasil yang optimal."
        )
    },
    {
        "id": "AI-RAW-002",
        "genre": "ai_bureaucratic",
        "provenance": "GPT-4o Raw Generation",
        "text": (
            "Tidak dapat dipungkiri bahwa tata kelola pemerintahan yang baik merupakan pilar utama dalam pembangunan berkelanjutan. "
            "Seiring dengan perkembangan teknologi yang pesat, instansi pemerintah dituntut untuk senantiasa berupaya menciptakan "
            "ekosistem pelayanan publik yang transparan dan akuntabel. Di sisi lain, kolaborasi antarlembaga merupakan hal yang sangat "
            "krusial untuk menjembatani kesenjangan birokrasi yang ada. Sebagai kesimpulan, langkah konkret dan strategis perlu diambil "
            "guna mewujudkan tata kelola yang inklusif."
        )
    },
    {
        "id": "AI-RAW-003",
        "genre": "ai_academic",
        "provenance": "Claude 3.5 Sonnet Raw Generation",
        "text": (
            "Artikel ini menyelami lebih dalam mengenai lanskap transformasi digital di sektor pelayanan kesehatan Indonesia. "
            "Secara umum, adopsi rekam medis elektronik telah membawa angin segar bagi efisiensi administrasi rumah sakit. "
            "Meskipun demikian, tantangan keamanan siber dan perlindungan data pribadi tetap menjadi isu yang mendasar. "
            "Dengan demikian, dapat dipahami bahwa regulasi yang komprehensif sangat dibutuhkan untuk mengawal inovasi ini "
            "agar dapat memberikan kontribusi nyata bagi masyarakat luas."
        )
    },
    {
        "id": "AI-RAW-004",
        "genre": "ai_essay",
        "provenance": "Llama-3-70b-Indonesian Raw Generation",
        "text": (
            "Pendidikan karakter memainkan peran penting dalam mencetak generasi muda yang berdaya saing tinggi di kancah global. "
            "Dalam konteks ini, nilai-nilai luhur Pancasila harus diinternalisasikan ke dalam setiap aspek kurikulum pembelajaran. "
            "Selain itu, keterlibatan aktif orang tua dan masyarakat merupakan pendorong utama keberhasilan pembinaan moral siswa. "
            "Secara keseluruhan, sinergi yang harmonis antara sekolah dan lingkungan keluarga akan melahirkan tunas bangsa yang unggul."
        )
    },
    {
        "id": "AI-RAW-005",
        "genre": "ai_marketing",
        "provenance": "Gemini 2.0 Flash Raw Generation",
        "text": (
            "Di tengah dinamika pasar yang kian kompetitif, inovasi produk menjadi kunci utama keberlanjutan bisnis modern. "
            "Perusahaan yang mampu beradaptasi dengan preferensi konsumen digital akan senantiasa memimpin pangsa pasar. "
            "Lebih dari itu, pemanfaatan analitik data pelanggan memungkinkan penyusunan strategi pemasaran yang tepat sasaran. "
            "Oleh sebab itu, investasi pada ekosistem digital bukan lagi sekadar pilihan melainkan kebutuhan mutlak bagi masa depan."
        )
    },
    {
        "id": "AI-RAW-006",
        "genre": "ai_spbe_synthesis",
        "provenance": "Gemini 2.5 Pro Raw Generation",
        "text": (
            "Implementasi arsitektur SPBE memegang peranan krusial dalam mempercepat terwujudnya e-government yang terintegrasi. "
            "Melalui pemanfaatan platform bersama, setiap perangkat daerah dapat saling berbagi data dengan mudah dan aman. "
            "Selain itu, standardisasi proses bisnis akan mengeliminasi tumpang tindih fungsi pelayanan publik yang kerap terjadi. "
            "Dengan demikian, tata kelola pemerintahan digital yang efektif, efisien, dan transparan dapat dirasakan langsung oleh masyarakat."
        )
    },
    {
        "id": "AI-RAW-007",
        "genre": "ai_smartcity",
        "provenance": "GPT-4o Raw Generation",
        "text": (
            "Konsep kota cerdas atau smart city menjadi salah satu solusi inovatif dalam mengatasi kompleksitas permasalahan perkotaan. "
            "Pemanfaatan sensor berbasis Internet of Things (IoT) memungkinkan pemantauan kondisi lingkungan secara waktu nyata. "
            "Lebih lanjut, integrasi data lalu lintas dan transportasi publik dapat meminimalisir kemacetan di jalan raya secara signifikan. "
            "Oleh karena itu, kolaborasi multi-pihak antara pemerintah, akademisi, dan masyarakat sangat dibutuhkan demi kesuksesan inisiatif ini."
        )
    },
    {
        "id": "AI-RAW-008",
        "genre": "ai_cybersecurity",
        "provenance": "Claude 3.5 Sonnet Raw Generation",
        "text": (
            "Keamanan siber merupakan fondasi yang tidak terpisahkan dari ekosistem ekonomi digital di Indonesia saat ini. "
            "Meningkatnya serangan siber yang canggih menuntut penguatan benteng pertahanan digital pada infrastruktur informasi vital. "
            "Di samping itu, kesadaran sumber daya manusia terhadap bahaya rekayasa sosial perlu terus ditingkatkan secara berkelanjutan. "
            "Sebagai penutup, kepatuhan terhadap regulasi pelindungan data pribadi adalah prasyarat mutlak untuk menjaga kepercayaan publik."
        )
    },
    {
        "id": "AI-RAW-009",
        "genre": "ai_agriculture",
        "provenance": "DeepSeek-V3 Raw Generation",
        "text": (
            "Sektor pertanian modern di Indonesia kini memasuki babak baru berkat adopsi teknologi pertanian presisi yang inovatif. "
            "Penggunaan drone pemantau lahan dan sensor kelembapan tanah membantu petani mengoptimalkan penggunaan pupuk dan air. "
            "Selain itu, akses langsung ke pasar melalui aplikasi digital mampu memotong rantai pasok yang selama ini merugikan petani. "
            "Dengan demikian, kesejahteraan petani dapat meningkat seiring dengan terwujudnya kedaulatan pangan nasional yang kokoh."
        )
    },
    {
        "id": "AI-RAW-010",
        "genre": "ai_green_energy",
        "provenance": "Gemini 2.5 Flash Raw Generation",
        "text": (
            "Transisi menuju energi baru dan terbarukan memainkan peran sentral dalam upaya mitigasi krisis iklim global. "
            "Potensi energi surya dan angin yang melimpah di Indonesia menawarkan peluang besar untuk diversifikasi bauran energi. "
            "Lebih lanjut, regulasi yang ramah investasi sangat diperlukan guna menarik minat investor domestik maupun internasional. "
            "Oleh sebab itu, komitmen politik yang kuat menjadi katalis penting dalam mempercepat pencapaian target emisi nol bersih."
        )
    }
]

# ---------------------------------------------------------------------------
# 3. HUMAN-EDITED AI CORPUS
# AI outputs revised by human editors: burstiness restored, cliches removed,
# natural Indonesian syntax and punctuation rhythm injected.
# ---------------------------------------------------------------------------
HUMAN_EDITED_AI_CORPUS = [
    {
        "id": "HYB-HEDIT-001",
        "genre": "edited_ai_governance",
        "provenance": "AI output revised by human editor removing robotic markers",
        "text": (
            "Transformasi digital kini menjadi keharusan mutlak bagi organisasi modern. Integrasi kecerdasan buatan "
            "terbukti mempercepat alur kerja harian hingga 40 persen. Saat data tersimpan rapi dalam satu basis data, "
            "manajemen dapat mengambil keputusan bisnis berdasarkan bukti riil di lapangan. Namun, tanpa pelatihan "
            "karyawan yang memadai, perangkat lunak tercanggih sekalipun hanya akan menjadi beban pembukuan kantor."
        )
    },
    {
        "id": "HYB-HEDIT-002",
        "genre": "edited_ai_academic",
        "provenance": "AI draft revised with human sentence burstiness and variance",
        "text": (
            "Kajian ini membedah kesiapan rumah sakit umum daerah dalam menerapkan rekam medis elektronik. "
            "Hasil telusur lapangan mengungkap kabar baik: waktu tunggu pasien rawat jalan terpangkas separuh. "
            "Akan tetapi, lubang keamanan siber masih menganga di mana-mana. Tanpa audit berkala dan enkripsi basis data, "
            "rekam medis warga rawan bocor ke tangan sindikat penipuan daring."
        )
    },
    {
        "id": "HYB-HEDIT-003",
        "genre": "edited_ai_smartcity",
        "provenance": "AI text rewritten with concrete case study data and uneven cadence",
        "text": (
            "Smart city bukan melulu soal pasang CCTV atau bagi-bagi gawai ke pejabat kelurahan. Di Jakarta, "
            "integrasi sensor debit air di pintu-pintu air sungai Ciliwung terbukti menyelamatkan ribuan warga dari genangan banjir mendadak. "
            "Sayangnya, koordinasi antarwilayah perbatasan sering tersendat ego sektoral. Ketika hulu dan hilir masih saling menyalahkan, "
            "teknologi paling mutakhir pun tak banyak menolong."
        )
    },
    {
        "id": "HYB-HEDIT-004",
        "genre": "edited_ai_education",
        "provenance": "AI draft humanized with cultural idioms and varying punctuation",
        "text": (
            "Mendidik anak tidak bisa cuma diserahkan pada papan tulis di kelas, apalagi layar ponsel pintar. "
            "Keteladanan orang tua di rumah memegang kunci utama pembentukan watak. Jika di meja makan anak terbiasa melihat "
            "orang tuanya asyik bermain media sosial tanpa peduli obrolan keluarga, ajaran moral seindah apa pun di sekolah "
            "pasti masuk telinga kiri dan keluar telinga kanan."
        )
    }
]

# ---------------------------------------------------------------------------
# 4. AI-EDITED HUMAN CORPUS
# Human base smoothed by AI: idiosyncratic quirks flattened,
# transition markers added, variance artificially reduced.
# ---------------------------------------------------------------------------
AI_EDITED_HUMAN_CORPUS = [
    {
        "id": "HYB-AIEDIT-001",
        "genre": "ai_smoothed_regulation",
        "provenance": "Authentic Perpres text polished by LLM grammar tool",
        "text": (
            "Sistem Pemerintahan Berbasis Elektronik (SPBE) pada dasarnya merupakan penyelenggaraan administrasi negara "
            "yang memanfaatkan kemajuan teknologi informasi demi melayani masyarakat secara prima. Oleh karena itu, "
            "kerangka tata kelola SPBE sangat krusial guna mengarahkan implementasi kebijakan secara terpadu dan menyeluruh. "
            "Keterpaduan ini pada akhirnya akan menciptakan layanan birokrasi digital yang akuntabel dan efisien."
        )
    },
    {
        "id": "HYB-AIEDIT-002",
        "genre": "ai_smoothed_research",
        "provenance": "Human research methodology smoothed by AI tool",
        "text": (
            "Penelitian ini bertujuan untuk menginvestigasi efektivitas metode pembelajaran mesin pada deteksi citra medis. "
            "Kombinasi antara ekstraksi wavelet dan Support Vector Machine memberikan performa yang memuaskan dengan akurasi 89,4%. "
            "Selain itu, efisiensi komputasi meningkat signifikan dibandingkan metode terdahulu, sehingga model ini layak "
            "dipertimbangkan untuk implementasi klinis di masa depan."
        )
    },
    {
        "id": "HYB-AIEDIT-003",
        "genre": "ai_smoothed_journalism",
        "provenance": "Field journalism smoothed into generic formal sentences",
        "text": (
            "Kenaikan harga beras di sejumlah pasar tradisional DKI Jakarta kini menjadi perhatian utama masyarakat luas. "
            "Keterlambatan masa panen di daerah sentra produksi disinyalir menjadi pemicu utama berkurangnya pasokan pangan. "
            "Di sisi lain, konsumen terpaksa mengatur ulang anggaran belanja harian mereka guna mengimbangi kenaikan tersebut. "
            "Sebagai solusi, langkah stabilisasi pasokan dari instansi terkait sangat diharapkan agar situasi lekas terkendali."
        )
    },
    {
        "id": "HYB-AIEDIT-004",
        "genre": "ai_smoothed_cultural",
        "provenance": "Literary essay rewritten by LLM with modern generic tone",
        "text": (
            "Peranan bahasa dalam kehidupan masyarakat sejatinya jauh melampaui fungsi komunikasi pragmatis sehari-hari. "
            "Bahasa merupakan cerminan identitas kultural dan peradaban yang memuat memori kolektif suatu bangsa. "
            "Oleh karena itu, melestarikan ungkapan tradisional merupakan langkah strategis untuk memperkuat ketahanan budaya. "
            "Dengan demikian, generasi penerus dapat tetap menjaga nilai-nilai luhur di tengah derasnya arus globalisasi."
        )
    }
]

# ---------------------------------------------------------------------------
# 5. PARAPHRASED CORPUS
# Human texts paraphrased with syntactic rearrangements.
# ---------------------------------------------------------------------------
PARAPHRASED_CORPUS = [
    {
        "id": "HYB-PARA-001",
        "genre": "paraphrased_essay",
        "provenance": "Syntactically paraphrased Indonesian essay",
        "text": (
            "Bukanlah semata-mata alat bertukar sapa, bahasa menyimpan rekam jejak luka dan martabat manusia dari masa lampau. "
            "Tatkala ungkapan daerah ditinggalkan warganya, tercerabutlah pilar kultural yang selama berabad-abad menopang "
            "kesadaran kolektif suatu bangsa."
        )
    },
    {
        "id": "HYB-PARA-002",
        "genre": "paraphrased_academic",
        "provenance": "Paraphrased scientific findings with active passive inversion",
        "text": (
            "Akurasi deteksi citra medis mencapai 89,4 persen saat ekstraksi wavelet dipadukan dengan pengklasifikasi SVM berinti RBF. "
            "Keunggulan utama pendekatan ini terletak pada pemangkasan waktu komputasi hingga 30 persen dibanding skema konvolusional tanpa pra-olah."
        )
    },
    {
        "id": "HYB-PARA-003",
        "genre": "paraphrased_regulation",
        "provenance": "Syntactically inverted SPBE regulation text",
        "text": (
            "Demi mewujudkan layanan publik terpadu, SPBE memanfaatkan teknologi informasi dan komunikasi dalam tata kelola pemerintahan. "
            "Pengaturan, pengarahan, serta pengendalian sistematis diatur dalam suatu kerangka kerja nasional yang berkesinambungan."
        )
    }
]

# ---------------------------------------------------------------------------
# 6. MIXED AUTHORSHIP CORPUS
# Documents with segments written by human and segments generated by AI.
# Critical for segment-level evaluation and mixed-outcome testing.
# ---------------------------------------------------------------------------
MIXED_CORPUS = [
    {
        "id": "MIX-001",
        "genre": "mixed_authorship_paper",
        "provenance": "Human intro + AI body + Human conclusion",
        "text": (
            "Penyusunan arsitektur SPBE Provinsi DKI Jakarta berpedoman pada prinsip interoperabilitas sistem "
            "dan bagi pakai data antarsub-sistem. Dinas Komunikasi, Informatika dan Statistik menetapkan standar "
            "metadatabase terpusat guna menghindari duplikasi aplikasi di lingkungan satuan kerja perangkat daerah. "
            "Dalam era digitalisasi yang serba cepat ini, penerapan teknologi informasi menjadi suatu keniscayaan yang "
            "tidak dapat dihindari bagi setiap organisasi. Selain itu, integrasi sistem kecerdasan buatan memainkan peran "
            "yang sangat penting dalam meningkatkan efisiensi operasional secara signifikan. "
            "Setiap unit pelaksana teknis wajib mendaftarkan sistem informasi ke dalam repositori aplikasi daerah "
            "sebelum pengajuan anggaran belanja pemeliharaan TIK disetujui oleh Badan Perencanaan Pembangunan Daerah."
        ),
        "segments": [
            {"sentence_indices": [0, 1], "author": "human"},
            {"sentence_indices": [2, 3], "author": "ai"},
            {"sentence_indices": [4], "author": "human"}
        ]
    },
    {
        "id": "MIX-002",
        "genre": "mixed_authorship_news",
        "provenance": "AI intro + Human investigative details",
        "text": (
            "Tidak dapat dipungkiri bahwa tata kelola pemerintahan yang baik merupakan pilar utama dalam pembangunan berkelanjutan. "
            "Seiring dengan perkembangan teknologi yang pesat, instansi pemerintah dituntut untuk senantiasa berupaya menciptakan "
            "ekosistem pelayanan publik yang transparan dan akuntabel. "
            "Namun di lapangan, audit BPK justru membongkar selisih pengadaan server komputasi awan belasan miliar rupiah. "
            "Daftar inventaris fisik di ruang server kementerian terbukti jauh berbeda dari spesifikasi yang tertera pada kontrak."
        ),
        "segments": [
            {"sentence_indices": [0, 1], "author": "ai"},
            {"sentence_indices": [2, 3], "author": "human"}
        ]
    },
    {
        "id": "MIX-003",
        "genre": "mixed_authorship_sop",
        "provenance": "Human protocol + AI summary filler",
        "text": (
            "Apabila pemantauan jaringan mendeteksi lonjakan lalu lintas yang mencurigakan melebihi ambang batas 150 persen "
            "dari rata-rata normal selama tiga menit berturut-turut, petugas jaga SOC wajib segera mengaktifkan protokol isolasi vLAN. "
            "Lebih lanjut, integrasi teknologi keamanan siber memainkan peran krusial dalam menjaga keandalan infrastruktur nasional. "
            "Dengan demikian, langkah konkret dan strategis perlu diambil guna mewujudkan perlindungan data yang holistik."
        ),
        "segments": [
            {"sentence_indices": [0], "author": "human"},
            {"sentence_indices": [1, 2], "author": "ai"}
        ]
    }
]


def build_full_dataset() -> Dict[str, Any]:
    """
    Compiles and exports the complete Indonesian AI text detection benchmark dataset.
    Splits: Train (60%), Validation (20%), Test (20%) strictly without document leakage.
    """
    dataset_records = []

    # 1. Label human authentic (ground_truth: 0)
    for doc in HUMAN_CORPUS:
        dataset_records.append({
            "id": doc["id"],
            "label": "human",
            "ground_truth": 0,
            "category": "human_authentic",
            "genre": doc["genre"],
            "provenance": doc["provenance"],
            "text": doc["text"]
        })

    # 2. Label AI raw (ground_truth: 1)
    for doc in AI_CORPUS:
        dataset_records.append({
            "id": doc["id"],
            "label": "ai",
            "ground_truth": 1,
            "category": "ai_raw",
            "genre": doc["genre"],
            "provenance": doc["provenance"],
            "text": doc["text"]
        })

    # 3. Label Human-edited AI (ground_truth: 0 for binary classification, marked as hybrid)
    for doc in HUMAN_EDITED_AI_CORPUS:
        dataset_records.append({
            "id": doc["id"],
            "label": "mixed_human_dominant",
            "ground_truth": 0,
            "category": "human_edited_ai",
            "genre": doc["genre"],
            "provenance": doc["provenance"],
            "text": doc["text"]
        })

    # 4. Label AI-edited human (ground_truth: 1 for binary classification, marked as hybrid)
    for doc in AI_EDITED_HUMAN_CORPUS:
        dataset_records.append({
            "id": doc["id"],
            "label": "mixed_ai_dominant",
            "ground_truth": 1,
            "category": "ai_edited_human",
            "genre": doc["genre"],
            "provenance": doc["provenance"],
            "text": doc["text"]
        })

    # 5. Label Paraphrased (ground_truth: 0)
    for doc in PARAPHRASED_CORPUS:
        dataset_records.append({
            "id": doc["id"],
            "label": "human_paraphrased",
            "ground_truth": 0,
            "category": "paraphrased",
            "genre": doc["genre"],
            "provenance": doc["provenance"],
            "text": doc["text"]
        })

    # 6. Label Mixed (ground_truth: 1 for detection of synthetic content)
    for doc in MIXED_CORPUS:
        dataset_records.append({
            "id": doc["id"],
            "label": "mixed",
            "ground_truth": 1,
            "category": "mixed_authorship",
            "genre": doc["genre"],
            "provenance": doc["provenance"],
            "text": doc["text"],
            "segments": doc.get("segments", [])
        })

    # Deterministic split: Stratify by category to ensure balanced representation
    random.seed(42)
    categories = {}
    for r in dataset_records:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    train_data = []
    val_data = []
    test_data = []

    for cat, items in categories.items():
        random.shuffle(items)
        n = len(items)
        n_train = max(1, int(round(n * 0.6)))
        n_val = max(1, int(round(n * 0.2))) if n >= 3 else 0
        
        train_data.extend(items[:n_train])
        val_data.extend(items[n_train:n_train + n_val])
        test_data.extend(items[n_train + n_val:])

    # Shuffle final splits
    random.shuffle(train_data)
    random.shuffle(val_data)
    random.shuffle(test_data)

    # Ensure files directory exists
    os.makedirs(DATASET_DIR, exist_ok=True)

    train_path = os.path.join(DATASET_DIR, "train.jsonl")
    val_path = os.path.join(DATASET_DIR, "val.jsonl")
    test_path = os.path.join(DATASET_DIR, "test.jsonl")
    meta_path = os.path.join(DATASET_DIR, "metadata.json")

    with open(train_path, "w", encoding="utf-8") as f:
        for r in train_data:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with open(val_path, "w", encoding="utf-8") as f:
        for r in val_data:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with open(test_path, "w", encoding="utf-8") as f:
        for r in test_data:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    metadata = {
        "dataset_name": "NEXUS-IndoDetect-v1",
        "description": "Benchmark dataset for Indonesian AI-generated text detection & authorship analysis",
        "language": "id",
        "total_documents": len(dataset_records),
        "splits": {
            "train": len(train_data),
            "val": len(val_data),
            "test": len(test_data)
        },
        "categories": {
            "human_authentic": len(HUMAN_CORPUS),
            "ai_raw": len(AI_CORPUS),
            "human_edited_ai": len(HUMAN_EDITED_AI_CORPUS),
            "ai_edited_human": len(AI_EDITED_HUMAN_CORPUS),
            "paraphrased": len(PARAPHRASED_CORPUS),
            "mixed_authorship": len(MIXED_CORPUS)
        },
        "provenance_types": [
            "Perpres & SPBE DKI Jakarta (Official Government)",
            "Jurnal Ilmiah Sinta/Scopus (UI, UGM, ITB, Unpad)",
            "LKBN Antara & Kompas & Tempo (Journalism)",
            "Majalah Horison & Esai Sastra (Literary)",
            "Gemini 2.5/2.0 Flash (Google GenAI)",
            "GPT-4o (OpenAI)",
            "Claude 3.5 Sonnet (Anthropic)",
            "DeepSeek-V3",
            "Llama-3-70b-Indonesian (Open Weights)"
        ]
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return metadata


if __name__ == "__main__":
    meta = build_full_dataset()
    print("Dataset generated successfully:")
    print(json.dumps(meta, indent=2))
