# STANDAR OPERASIONAL LAPORAN AUDIT SPBE DKI JAKARTA
## Format Baku Rekapitulasi Data Gagal Upload & Data yang Belum Ada per Perangkat Daerah

> **Dasar Standar:** Format Resmi Diskominfotik & SPBE CBC DKI Jakarta ([Google Spreadsheet Referensi](https://docs.google.com/spreadsheets/d/170-6VSb8WHMEbCOpiyNCmAUQKkueL93CM0tXOKlb6o8))  
> **Mandat:** ARKA (CEO Orchestrator) & SEKAR (Director of Compliance)  
> **Klasifikasi:** Standard Audit Output Schema

---

### 1. STRUKTUR FORMAT LAPORAN BAKU

Setiap Perangkat Daerah / Biro yang diaudit kelengkapan dokumen arsitektur SPBE-nya **wajib disajikan dalam 2 tipe tabel granular**:

#### Tipe A: "Data Gagal Upload [Nama Perangkat Daerah]"
Menjelaskan secara presisi entitas data apa yang gagal diunggah atau belum lengkap atributnya:

| Kolom | Nama Kolom Header | Tipe Data | Keterangan & Standar Isian |
| :---: | :--- | :---: | :--- |
| **A** | `NO` | Numerik | Nomor urut (1.0, 2.0, ...) |
| **B** | `PERANGKAT DAERAH` | Teks | Nama lengkap instansi / OPD / Biro |
| **C** | `DOMAIN` | Teks | Domain arsitektur (`Layanan_Upgrade`, `Infrastruktur_Sesuai`, `DataInformasi_Sesuai`, `ProsesBisnis_Upgrade`, dll.) |
| **D** | `ID - Nama Data` | Teks | Kode ID entitas dan nama dokumen/layanan/server/aset terkait |
| **E** | `Nama Kolom yang belum terisi` | Teks Multi-line | **Daftar spesifik kolom-kolom wajib yang masih kosong** (misal: *Referensi Arsitektur Layanan Level 3*, *Target Layanan*, *Potensi Risiko*, *Mitigasi Risiko*) |

*Format Warna Header:* Pastel Blue (`#9BC2E6`), Font Arial 9pt Bold.

---

#### Tipe B: "Data yang Belum Ada [Nama Perangkat Daerah]"
Menjelaskan secara presisi domain arsitektur mana saja yang **kosong total / belum dibuatkan sama sekali**:

| Kolom | Nama Kolom Header | Tipe Data | Keterangan & Standar Isian |
| :---: | :--- | :---: | :--- |
| **A** | `NO` | Numerik | Nomor urut (1.0, 2.0, ...) |
| **B** | `PERANGKAT DAERAH` | Teks | Nama lengkap instansi / OPD / Biro |
| **C** | `DOMAIN` | Teks | Nama lembar kerja / domain yang belum ada (`ProsesBisnis_Upgrade`, `ProsesBisnis_Sunset`, `Layanan_Upgrade`, `Layanan_Sunset`, `Aplikasi_Sunset`, `DataInformasi_Upgrade`, `DataInformasi_Sunset`) |

*Format Warna Header:* Pastel Blue (`#9BC2E6`), Font Arial 9pt Bold.

---

### 2. PROTOKOL EKSEKUSI OTONOM 5 AGENT NEXUS

1. **NAYA (Research & Intelligence):** Melakukan ekstraksi *read-only* dari Google Drive & Google Spreadsheet untuk mendeteksi sel kosong dan domain yang hilang.
2. **SEKAR (Compliance & Risk):** Mengelompokkan temuan ke dalam Tipe A (Kolom belum terisi) dan Tipe B (Domain belum ada).
3. **RAKA (Technology & Engineering):** Mengompilasi data ke dalam berkas Excel resmi `.xlsx` multi-tab menggunakan styling identik `#9BC2E6`.
4. **DIMAS (Operations):** Menyusun matriks PIC tindak lanjut penyelesaian berkas per dinas.
5. **ARKA (Chief Executive):** Melakukan review validasi akhir sebelum diterbitkan ke eksekutif.
