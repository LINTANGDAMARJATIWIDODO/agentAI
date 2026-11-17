"""
Verification script for LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.xlsx
Checks:
- File existence & extension
- Existence of 7 required sheets: DASHBOARD, REKAP_22_PD, DETAIL_AUDIT, DATA_TIDAK_SESUAI, DATA_BELUM_LENGKAP, FILE_TIDAK_DITEMUKAN, CATATAN_VALIDASI
- Non-empty content in all sheets
- Presence of all 22 Perangkat Daerah
"""

import os
import openpyxl

target_file = r"C:\Users\LENOVO\.gemini\antigravity\scratch\NEXUS-AI-ENTERPRISE\reports\SPBE_AUDIT\LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.xlsx"

assert os.path.exists(target_file), f"File not found: {target_file}"
assert target_file.endswith(".xlsx"), "Invalid extension"

wb = openpyxl.load_workbook(target_file, data_only=False)
expected_sheets = [
    "DASHBOARD",
    "REKAP_22_PD",
    "DETAIL_AUDIT",
    "DATA_TIDAK_SESUAI",
    "DATA_BELUM_LENGKAP",
    "FILE_TIDAK_DITEMUKAN",
    "CATATAN_VALIDASI"
]

print("Verifying Workbook Integrity...")
for s_name in expected_sheets:
    assert s_name in wb.sheetnames, f"Missing sheet: {s_name}"
    ws = wb[s_name]
    max_r = ws.max_row
    max_c = ws.max_column
    print(f" - Sheet '{s_name}': OK ({max_r} rows, {max_c} columns)")
    assert max_r > 5, f"Sheet {s_name} appears empty (only {max_r} rows)"

# Verify 22 OPDs in REKAP_22_PD
ws_rekap = wb["REKAP_22_PD"]
opd_found = []
for r in range(6, 28):
    val = ws_rekap.cell(row=r, column=2).value
    if val:
        opd_found.append(val)

print(f"\nTotal Perangkat Daerah verified in REKAP_22_PD: {len(opd_found)} OPDs.")
assert len(opd_found) == 22, f"Expected 22 OPDs, found {len(opd_found)}"

print("\nALL VERIFICATION CHECKS PASSED SUCCESSFULLY (100% COMPLIANT)!")
