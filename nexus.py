"""
NEXUS AI ENTERPRISE — Interactive CLI Management Tool
Provides CLI commands to inspect agent rosters, check activity logs,
trigger corporate mandates, and read executive reports.
"""

import sys
import os
import json
from orchestrator import NexusOrchestrator, load_json, LOGS_FILE, REPORT_JSON, CONFIG_DIR


def print_banner():
    print(r"""
========================================================================
    _   ________________  ______   ___    ____   _______   ________
   / | / / ____/  _/ __ \/ ____/  /   |  /  _/  / ____/ | / /_  __/
  /  |/ / __/  / // / / / /      / /| |  / /   / __/ /  |/ / / /   
 / /|  / /____/ // /_/ / /___   / ___ |_/ /   / /___/ /|  / / /    
/_/ |_/_____/___/\____/\____/  /_/  |_/___/  /_____/_/ |_/ /_/     
                   ENTERPRISE MULTI-AGENT WORKFORCE
========================================================================
""")


def show_roster():
    agents_data = load_json(os.path.join(CONFIG_DIR, "agents_config.json")).get("enterprise_roster", [])
    print("\n--- DEWAN DIREKSI AI (EXECUTIVE ROSTER) ---")
    for a in agents_data:
        print(f"{a['avatar']} {a['name']} — {a['title']}")
        print(f"   Domain: {a['role']}")
        print(f"   Skills: {', '.join(a['skills'])}")
        print(f"   Tools : {', '.join(a['tools'])}\n")


def show_status():
    log_data = load_json(LOGS_FILE)
    print("\n--- STATUS AKTIVITAS KERJA MULTI-AGENT ---")
    mandate = log_data.get("active_mandate")
    if mandate:
        print(f"Mandat Aktif   : {mandate.get('instruction')}")
        print(f"Status Mandat  : {mandate.get('status')}")
        print(f"Dimulai Sejak  : {mandate.get('initiated_at')}\n")
    else:
        print("Belum ada mandat aktif yang sedang berjalan.\n")

    tasks = log_data.get("tasks", [])
    if tasks:
        print("Daftar Tugas Divisional:")
        for t in tasks:
            status_symbol = "[v]" if t["status"] == "COMPLETED" else "[*]" if t["status"] == "IN PROGRESS" else "[-]"
            print(f" {status_symbol} [{t['status']}] {t['task_id']} ({t['agent_name']}): {t['domain']}")
            if t.get("result_summary"):
                print(f"     Hasil: {t['result_summary']}")
    print()


def show_report():
    laporan = load_json(REPORT_JSON)
    print("\n--- RINGKASAN EKSEKUTIF (LAPORAN.JSON) ---")
    print(f"Sistem           : {laporan.get('system')} v{laporan.get('version')}")
    print(f"Status           : {laporan.get('status')}")
    print(f"Dewan Rekomendasi: {laporan.get('board_recommendation')}")
    print(f"Executive Summary: {laporan.get('executive_summary')}\n")

    metrics = laporan.get("metrics")
    if metrics:
        print("Metrik Kelayakan Kunci:")
        print(f"  - CAPEX Kebutuhan Awal : Rp {metrics.get('capex_idr', 0):,}")
        print(f"  - Estimasi OPEX Bulanan: Rp {metrics.get('monthly_opex_idr', 0):,}")
        print(f"  - Break-Even Point     : Bulan ke-{metrics.get('bep_months')}")
        print(f"  - Internal Rate of Ret.: {metrics.get('irr_percent')}%")
        print(f"  - Net Present Value    : Rp {metrics.get('npv_idr', 0):,}")
        print(f"  - Target Uptime SLA    : {metrics.get('sla_uptime_percent')}%\n")


def main():
    print_banner()
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "roster":
            show_roster()
        elif cmd == "status":
            show_status()
        elif cmd == "report":
            show_report()
        elif cmd == "run":
            instruction = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Analisis kelayakan bisnis untuk membuka perusahaan teknologi AI Enterprise di Indonesia"
            orchestrator = NexusOrchestrator()
            orchestrator.run_full_pipeline(instruction)
        else:
            print(f"Perintah tidak dikenal: {cmd}")
            print("Perintah tersedia: roster, status, report, run <instruksi>")
    else:
        print("Perintah CLI yang dapat digunakan:")
        print("  python nexus.py roster          (Lihat daftar 5 Direktur AI & skill)")
        print("  python nexus.py status          (Lihat status aktivitas terkini)")
        print("  python nexus.py report          (Lihat intisari laporan.json)")
        print("  python nexus.py run <mandat>    (Jalankan orkestrasi kolaborasi 5 agent)")
        print("\nMenampilkan status terkini secara otomatis:")
        show_roster()
        show_status()
        show_report()


if __name__ == "__main__":
    main()
