---
name: google-drive-connector
description: Search, retrieve, inspect, and parse files, spreadsheets, and documents from Google Drive. Use when checking Google Drive documents, reading shared company folders, or ingesting Drive spreadsheets.
---

# SKILL: Google Drive Enterprise Connector & Document Inspector

> **Origin:** NEXUS Enterprise Integration Suite  
> **Classification:** Enterprise Cloud Storage Connector  
> **Author:** NEXUS Technology & Intelligence Board  
> **Target Owner:** Shared (NAYA for Intelligence, RAKA for Data Pipeline, SEKAR for Financial Audit)

---

## 1. PURPOSE & OBJECTIVE
To enable NEXUS AI agents to securely connect to Google Drive, list directory contents, locate specific business documents (PDF, DOCX, XLSX, Google Docs, Google Sheets), extract textual data and tables, and ingest them directly into agent analytical workflows.

## 2. SCOPE
- Google Drive v3 REST API, service account integration, local Google Drive desktop sync folder inspection (`knowledge/google-drive/`), file metadata queries, full-text document search, and spreadsheet table extraction.

## 3. INTEGRATION ARCHITECTURES
1. **Local Synced Folder Mode (Zero Config / Offline):**
   - Agents monitor `knowledge/google-drive/` where users place or sync Google Drive files.
   - Any document dropped here is automatically indexed with timestamp and metadata.
2. **Google Drive API Mode (Cloud Direct):**
   - Agents utilize OAuth 2.0 or Service Account credentials (`GOOGLE_APPLICATION_CREDENTIALS`).
   - Query format: `q="mimeType='application/vnd.google-apps.document' and fullText contains 'XYZ'"`

## 4. STEP-BY-STEP PROCEDURE
1. **Search & Locate:**
   - Execute query targeting file name or full-text keywords.
   - Return list of matching files: `{ file_id, name, mimeType, modifiedTime, webViewLink }`.
2. **Permission & Security Gate:**
   - Verify file classification (Public vs. Internal Confidential).
   - Ensure no PII or sensitive tokens are leaked without encryption.
3. **Download / Read Content:**
   - For Google Docs: Export as plain text or Markdown.
   - For Google Sheets: Export as CSV or structured JSON matrix.
   - For PDFs: Extract text using PDF parser and extract tabular figures.
4. **Digest & Hand-off:**
   - Pass extracted text to NAYA (for market/regulatory analysis) or SEKAR (for budget verification).
   - Log document hash and retrieval timestamp in `logs/activity_log.json`.

## 5. QUALITY STANDARDS & ACCEPTANCE CRITERIA
- Extracted tables must preserve column headers and row alignments.
- Document provenance (Drive File ID, last modified date, author) must be explicitly cited in the final deliverable.

## 6. SECURITY GUARDRAIL & ACCESS POLICY (STRICT READ-ONLY)

> [!CAUTION]
> **ZERO-MUTATION & READ-ONLY ENFORCEMENT POLICY**  
> Seluruh agen NEXUS AI ENTERPRISE (ARKA, NAYA, RAKA, SEKAR, DIMAS) **DILARANG KERAS** melakukan aksi *WRITE*, *EDIT*, *UPDATE*, *OVERWRITE*, *CELL MUTATION*, atau *DELETE* pada berkas Google Drive maupun Google Spreadsheet online (termasuk spreadsheet master `1ERr04A8w2GjeeTt12JlJd7GCvOUqUcIC`).

### Ruang Lingkup yang Diizinkan (*Permitted Scope*):
1. **Pengecekan Dokumen Kosong (*Empty Document Inspection*):** Mendeteksi sel baris kosong, template mentah yang belum terisi (*unpopulated rows*), dan tab spreadsheet yang belum memiliki data.
2. **Audit Kelengkapan Administratif (*Compliance Audit*):** Mengecek ada/tidaknya dokumen fisik atau softcopy seperti BAST, Berita Acara (BA), dan rekaman Zoom FGD.
3. **Penyusunan Laporan Audit Lokal (*Local Reporting*):** Hasil temuan dan rekomendasi hanya disimpan dan diekspor ke file lokal di workspace (`reports/` dan `output/spreadsheets/`), **tanpa menyentuh atau merusak berkas asli di Google Drive**.

### Tindakan Terlarang (*Prohibited Operations*):
- ❌ Mengedit atau mengubah nilai sel pada Google Spreadsheet online.
- ❌ Menghapus atau memindahkan file di Google Drive.
- ❌ Menimpa (*overwrite*) dokumen yang ada di Google Drive.
