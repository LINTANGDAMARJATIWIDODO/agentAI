import json

with open('reports/audit_spbe_google_drive.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

summary = data['summary']

print('=== 1. DAFTAR OPD DENGAN BAST BELUM ADA / BERMASALAH ===')
for item in summary['missing_bast']:
    print(f"- {item['opd']} (PIC: {item['pic']}) | Status: {item['status']} | Ket: {item['ket']}")

print('\n=== 2. DAFTAR OPD DENGAN BERITA ACARA BELUM ADA / PENDING ===')
for item in summary['missing_ba']:
    print(f"- {item['opd']} (PIC: {item['pic']}) | Status: {item['status']} | Ket: {item['ket']}")

print('\n=== 3. DAFTAR OPD DENGAN PERLU TTD ESELON 3 / MASIH DRAFT ===')
for item in summary['ttd_eselon3_pending']:
    print(f"- {item['opd']} | Catatan: {item['ket']}")
for item in summary['draft_status']:
    print(f"- {item['opd']} | Catatan: {item['ket']}")

print('\n=== 4. DAFTAR OPD DENGAN RECORD ZOOM BELUM ADA ===')
for item in summary['missing_record']:
    print(f"- {item['opd']} (PIC: {item['pic']}) | Status: {item['status']} | Ket: {item['ket']}")
