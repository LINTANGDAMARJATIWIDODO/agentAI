import csv
import json

with open('knowledge/google-drive/spbe_documents.csv', 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    rows = list(reader)

data_rows = rows[4:]
results = []
summary = {
    'total_opd': 0,
    'missing_bast': [],
    'missing_ba': [],
    'missing_record': [],
    'missing_notulensi': [],
    'draft_status': [],
    'ttd_eselon3_pending': [],
    'hardcopy_missing_in_dinas': []
}

for r in data_rows:
    if len(r) < 17:
        r += [''] * (17 - len(r))
    opd = r[3].strip()
    if not opd:
        continue

    summary['total_opd'] += 1
    pic = r[4].strip()
    dok = r[5].strip()
    record = r[6].strip()
    notulensi = r[7].strip()
    ba = r[8].strip()
    bast = r[9].strip()
    lokasi_bast = r[10].strip()
    tobe = r[11].strip()
    kondisi_tobe = r[12].strip()
    tobe_baru = r[13].strip()
    tobe_asis = r[14].strip()
    folder = r[15].strip()
    ket = r[16].strip()

    item_issues = []

    # Check BAST
    if bast.lower() in ['belum', 'blm', '???', '']:
        item_issues.append({'field': 'BAST', 'status': bast or 'KOSONG', 'detail': ket})
        summary['missing_bast'].append({'opd': opd, 'pic': pic, 'status': bast, 'ket': ket})
    elif 'belum' in ket.lower() and 'bast' in ket.lower():
        item_issues.append({'field': 'BAST', 'status': 'Pending TTD/Fisik', 'detail': ket})
        summary['missing_bast'].append({'opd': opd, 'pic': pic, 'status': 'Catatan Khusus', 'ket': ket})

    # Check Berita Acara
    if ba.lower() in ['belum', 'blm', '']:
        item_issues.append({'field': 'Berita Acara (BA)', 'status': ba or 'KOSONG', 'detail': ket})
        summary['missing_ba'].append({'opd': opd, 'pic': pic, 'status': ba, 'ket': ket})

    # Check Record Zoom
    if record.lower() in ['belum', 'blm', '']:
        item_issues.append({'field': 'Record Zoom', 'status': record or 'KOSONG', 'detail': ket})
        summary['missing_record'].append({'opd': opd, 'pic': pic, 'status': record, 'ket': ket})

    # Check Notulensi
    if notulensi.lower() in ['belum', 'blm', '']:
        item_issues.append({'field': 'Notulensi', 'status': notulensi or 'KOSONG', 'detail': ket})
        summary['missing_notulensi'].append({'opd': opd, 'pic': pic, 'status': notulensi})

    # Check Draft status / Still under review
    if 'draft' in ket.lower() or 'review kembali' in ket.lower():
        item_issues.append({'field': 'Status Dokumen', 'status': 'Masih Draft/Review', 'detail': ket})
        summary['draft_status'].append({'opd': opd, 'ket': ket})

    # Check TTD Eselon 3
    if 'ttd es 3' in ket.lower() or 'ttd es. 3' in ket.lower():
        item_issues.append({'field': 'Pengesahan', 'status': 'Menunggu TTD Eselon 3', 'detail': ket})
        summary['ttd_eselon3_pending'].append({'opd': opd, 'ket': ket})

    # Check Hardcopy
    if 'hard copy bast blm ada' in ket.lower() or 'hardcopy belum' in ket.lower():
        summary['hardcopy_missing_in_dinas'].append({'opd': opd, 'ket': ket})

    if item_issues:
        results.append({
            'opd': opd,
            'pic': pic,
            'folder': folder,
            'issues': item_issues,
            'keterangan': ket
        })

print(f"Total OPD teranalisis: {summary['total_opd']}")
print(f"Jumlah OPD dengan isu/dokumen belum lengkap: {len(results)}")
print(f"- BAST Belum / Bermasalah: {len(summary['missing_bast'])}")
print(f"- Berita Acara Belum Ada: {len(summary['missing_ba'])}")
print(f"- Record Zoom Belum Ada: {len(summary['missing_record'])}")
print(f"- Notulensi Kosong: {len(summary['missing_notulensi'])}")
print(f"- Dokumen Masih Draft / Review Kembali: {len(summary['draft_status'])}")
print(f"- Butuh Tanda Tangan Eselon 3: {len(summary['ttd_eselon3_pending'])}")

with open('reports/audit_spbe_google_drive.json', 'w', encoding='utf-8') as f:
    json.dump({'summary': summary, 'incomplete_opd': results}, f, indent=2, ensure_ascii=False)

print("\nHasil audit lengkap tersimpan di reports/audit_spbe_google_drive.json")
