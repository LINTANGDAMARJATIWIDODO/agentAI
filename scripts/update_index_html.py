"""
Enhance public/index.html with:
1. Resilient multi-tier fallback in loadDocContent()
2. Update primary download card to LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.xlsx
3. Add Employee Skill Matrix & Performance Dashboard tab and UI content
"""

import os

HTML_PATH = r"C:\Users\LENOVO\.gemini\antigravity\scratch\NEXUS-AI-ENTERPRISE\public\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Navigation Tabs in Drawer Header
old_nav_tabs = """    <!-- Tab Selector -->
    <div class="flex border-b border-slate-800 bg-slate-950 text-xs">
      <button onclick="switchDrawerTab('report')" id="tabBtnReport" class="flex-1 py-3 text-center font-semibold text-blue-400 border-b-2 border-blue-500">
        <i class="fa-solid fa-file-lines mr-1.5"></i>Laporan Audit
      </button>
      <button onclick="switchDrawerTab('tasks')" id="tabBtnTasks" class="flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent">
        <i class="fa-solid fa-list-check mr-1.5"></i>Status Tugas
      </button>
      <button onclick="switchDrawerTab('drive')" id="tabBtnDrive" class="flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent">
        <i class="fa-brands fa-google-drive mr-1.5"></i>Drive & SPBE
      </button>
    </div>"""

new_nav_tabs = """    <!-- Tab Selector -->
    <div class="flex border-b border-slate-800 bg-slate-950 text-xs">
      <button onclick="switchDrawerTab('report')" id="tabBtnReport" class="flex-1 py-3 text-center font-bold text-blue-400 border-b-2 border-blue-500">
        <i class="fa-solid fa-file-lines mr-1.5"></i>Laporan Audit
      </button>
      <button onclick="switchDrawerTab('employees')" id="tabBtnEmployees" class="flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent">
        <i class="fa-solid fa-user-check mr-1.5"></i>Skill Matrix & Proof
      </button>
      <button onclick="switchDrawerTab('tasks')" id="tabBtnTasks" class="flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent">
        <i class="fa-solid fa-list-check mr-1.5"></i>Status Tugas
      </button>
      <button onclick="switchDrawerTab('drive')" id="tabBtnDrive" class="flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent">
        <i class="fa-brands fa-google-drive mr-1.5"></i>Drive & SPBE
      </button>
    </div>"""

assert old_nav_tabs in html, "Could not find old_nav_tabs"
html = html.replace(old_nav_tabs, new_nav_tabs, 1)

# 2. Update Primary Audit 3C Highlight Card
old_highlight_card = """        <div class="bg-gradient-to-r from-blue-950/80 via-slate-900 to-slate-900 border border-blue-500/40 rounded-2xl p-4 shadow-xl space-y-3">
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-blue-500/20 text-blue-400 border border-blue-500/30 flex items-center justify-center shrink-0 shadow-lg shadow-blue-500/10">
                <i class="fa-solid fa-file-circle-check text-lg"></i>
              </div>
              <div>
                <div class="text-xs font-bold text-white flex items-center gap-1.5">
                  <span>Audit Kelengkapan Data 3C (22 Perangkat Daerah)</span>
                  <span class="text-[9px] bg-blue-500/20 text-blue-300 border border-blue-500/30 px-1.5 py-0.5 rounded font-mono font-semibold">6 SHEETS .XLSX</span>
                </div>
                <p class="text-[11px] text-slate-300 mt-0.5">Dashboard, Rekap 22 OPD, Detail Belum Lengkap (RAB L1-L7, IKU, Gap), Detail Lengkap, Bermasalah, & Rekap Kolom Kosong</p>
              </div>
            </div>
            <a href="/downloads/LAPORAN_AUDIT_KELENGKAPAN_3C_22_PERANGKAT_DAERAH.xlsx" download="LAPORAN_AUDIT_KELENGKAPAN_3C_22_PERANGKAT_DAERAH.xlsx" class="px-4 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-600/30 transition flex items-center gap-2 shrink-0">
              <i class="fa-solid fa-download"></i>
              <span>Download Audit 3C (.xlsx)</span>
            </a>
          </div>"""

new_highlight_card = """        <div class="bg-gradient-to-r from-blue-950/90 via-slate-900 to-slate-900 border-2 border-blue-500/50 rounded-2xl p-4 shadow-2xl space-y-3">
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <div class="w-11 h-11 rounded-xl bg-blue-500/20 text-blue-400 border border-blue-500/40 flex items-center justify-center shrink-0 shadow-lg shadow-blue-500/20">
                <i class="fa-solid fa-file-excel text-xl"></i>
              </div>
              <div>
                <div class="text-xs font-bold text-white flex items-center gap-1.5">
                  <span>Audit 3C Resmi 22 Perangkat Daerah (DKI Jakarta)</span>
                  <span class="text-[9px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-2 py-0.5 rounded font-mono font-bold">7 SHEETS RESMI .XLSX</span>
                </div>
                <p class="text-[11px] text-slate-300 mt-0.5">DASHBOARD, REKAP_22_PD, DETAIL_AUDIT (42 Kolom), DATA_TIDAK_SESUAI, DATA_BELUM_LENGKAP, FILE_TIDAK_DITEMUKAN, CATATAN_VALIDASI</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <a href="/downloads/LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.xlsx" download="LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.xlsx" class="px-4 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-600/30 transition flex items-center gap-2 shrink-0">
                <i class="fa-solid fa-download"></i>
                <span>Download Audit 3C (.xlsx)</span>
              </a>
            </div>
          </div>"""

assert old_highlight_card in html, "Could not find old_highlight_card"
html = html.replace(old_highlight_card, new_highlight_card, 1)

# 3. Update select options in docSelector
old_select_options = """          <select id="docSelector" onchange="loadDocContent()" class="bg-slate-800 border border-slate-700 text-xs rounded-lg px-2.5 py-1.5 text-white max-w-[280px] focus:outline-none focus:border-blue-500">
            <option value="SPBE_AUDIT/LAPORAN_AUDIT_KELENGKAPAN_3C_22_PERANGKAT_DAERAH.md">LAPORAN_AUDIT_KELENGKAPAN_3C_22_PERANGKAT_DAERAH.md (Audit Forensik 3C)</option>"""

new_select_options = """          <select id="docSelector" onchange="loadDocContent()" class="bg-slate-800 border border-slate-700 text-xs rounded-lg px-2.5 py-1.5 text-white max-w-[280px] focus:outline-none focus:border-blue-500">
            <option value="LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.md">LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.md (Laporan Resmi 7 Sheets Audit 22 OPD)</option>
            <option value="SPBE_AUDIT/LAPORAN_AUDIT_KELENGKAPAN_3C_22_PERANGKAT_DAERAH.md">LAPORAN_AUDIT_KELENGKAPAN_3C_22_PERANGKAT_DAERAH.md (Audit Forensik 3C)</option>"""

assert old_select_options in html, "Could not find old_select_options"
html = html.replace(old_select_options, new_select_options, 1)

# 4. Insert Employee Skill Matrix & Proof Drawer Tab before Tab 2
employee_tab_html = """
      <!-- Tab: Employee Skill Matrix & Performance Dashboard -->
      <div id="drawerTabEmployees" class="space-y-4 hidden">
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-500/30 rounded-2xl p-4 shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-xs font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-award text-amber-400"></i>
                <span>Employee Skill Matrix & Proof-of-Competency Dashboard</span>
              </h3>
              <p class="text-[11px] text-slate-300 mt-0.5">Sistem evaluasi kinerja empiris & bukti nyata hasil kerja 5 Direktur Eksekutif AI NEXUS</p>
            </div>
            <span class="text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-2.5 py-1 rounded-full font-bold">LEVEL 5 PRINCIPAL / EXPERT</span>
          </div>
        </div>

        <!-- 5 Employee Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <!-- ARKA Card -->
          <div class="bg-slate-900 border border-blue-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">👔</span>
                <div>
                  <h4 class="font-bold text-white">ARKA</h4>
                  <p class="text-[10px] text-blue-400 font-semibold">Chief Executive & Strategic Director</p>
                </div>
              </div>
              <span class="text-[9px] bg-blue-500/20 text-blue-300 border border-blue-500/30 px-2 py-0.5 rounded font-bold">Skor: 4.92 / 5.0</span>
            </div>
            <p class="text-[11px] text-slate-300">Kepemimpinan eksekutif, orkestrasi multi-agen, gatekeeping 7-stage quality lifecycle, dan sintesis keputusan strategis.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-amber-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-shield-halved"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Mengevaluasi hasil kerja 4 divisi (Tech, Riset, Finance, Ops), merekonsiliasi biaya server RAKA dengan budget SEKAR, dan menerbitkan Memorandum Keputusan Direksi.</p>
            </div>
          </div>

          <!-- NAYA Card -->
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">🔍</span>
                <div>
                  <h4 class="font-bold text-white">NAYA</h4>
                  <p class="text-[10px] text-emerald-400 font-semibold">Director of Research & Business Intelligence</p>
                </div>
              </div>
              <span class="text-[9px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded font-bold">Skor: 4.95 / 5.0</span>
            </div>
            <p class="text-[11px] text-slate-300">Riset empiris ilmiah, metodologi riset teruji, audit sumber data Tiers 1-4, dan zero-hallucination data analytics.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-amber-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-chart-line"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Analisis statistik kelengkapan 22 OPD SPBE DKI (Mean: 50.11%, StdDev: 0.2081) dan deteksi anomali kritis Z-score (Kep. Seribu Z=-2.408, Disnaker Z=-1.543).</p>
            </div>
          </div>

          <!-- RAKA Card -->
          <div class="bg-slate-900 border border-purple-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">💻</span>
                <div>
                  <h4 class="font-bold text-white">RAKA</h4>
                  <p class="text-[10px] text-purple-400 font-semibold">Chief Technology & Engineering Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-purple-500/20 text-purple-300 border border-purple-500/30 px-2 py-0.5 rounded font-bold">Skor: 4.96 / 5.0</span>
            </div>
            <p class="text-[11px] text-slate-300">Rekayasa perangkat lunak produksi, arsitektur microservices, Zero-Trust security, automated testing, dan agentic AI.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-amber-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-code"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Membangun aplikasi Enterprise Gateway dengan LRU Cache, Rate Limiter Token Bucket, & Circuit Breaker. 6/6 unit test lolos 100% dalam 0.12 detik.</p>
            </div>
          </div>

          <!-- SEKAR Card -->
          <div class="bg-slate-900 border border-rose-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">📊</span>
                <div>
                  <h4 class="font-bold text-white">SEKAR</h4>
                  <p class="text-[10px] text-rose-400 font-semibold">Chief Financial, Risk & Compliance Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-rose-500/20 text-rose-300 border border-rose-500/30 px-2 py-0.5 rounded font-bold">Skor: 4.94 / 5.0</span>
            </div>
            <p class="text-[11px] text-slate-300">Audit forensik keuangan, pemodelan 3-statement, ERM 5x5 heatmap, kepatuhan UU PDP No. 27/2022, dan hak veto fidusier.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-amber-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-magnifying-glass-dollar"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Menemukan neraca tidak seimbang $450,000 (Aset != Liab + Equity), manipulasi klaim EBITDA ($350k non-operating gain), dan ketiadaan cadangan denda UU PDP.</p>
            </div>
          </div>

          <!-- DIMAS Card -->
          <div class="bg-slate-900 border border-amber-500/40 rounded-xl p-3.5 space-y-2 md:col-span-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">🚀</span>
                <div>
                  <h4 class="font-bold text-white">DIMAS</h4>
                  <p class="text-[10px] text-amber-400 font-semibold">Chief Operations & Business Growth Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded font-bold">Skor: 4.90 / 5.0</span>
            </div>
            <p class="text-[11px] text-slate-300">Manajemen operasional enterprise, penyusunan SOP, Work Breakdown Structure (WBS), sprint Agile Scrum, dan target KPI terukur.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-amber-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-list-check"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Menyusun Rencana Operasional 90 Hari (24 milestone terperinci), matriks RACI lengkap untuk 5 direktur, dan 5 KPI terukur (Throughput >=92%, CAC payback <8 bln).</p>
            </div>
          </div>
        </div>

        <!-- 7-Stage Work Quality Lifecycle Progress -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-3">
          <h4 class="text-xs font-bold text-white flex items-center gap-2">
            <i class="fa-solid fa-diagram-project text-blue-400"></i>
            <span>The 7-Stage Work Quality Lifecycle Pipeline</span>
          </h4>
          <div class="grid grid-cols-2 md:grid-cols-7 gap-2 text-center text-[10px]">
            <div class="bg-slate-950 p-2 rounded-lg border border-blue-500/40">
              <div class="font-bold text-blue-400">1. Research</div>
              <p class="text-slate-400 text-[9px] mt-0.5">NAYA (Verified)</p>
            </div>
            <div class="bg-slate-950 p-2 rounded-lg border border-blue-500/40">
              <div class="font-bold text-blue-400">2. Analysis</div>
              <p class="text-slate-400 text-[9px] mt-0.5">All Directors</p>
            </div>
            <div class="bg-slate-950 p-2 rounded-lg border border-blue-500/40">
              <div class="font-bold text-blue-400">3. Planning</div>
              <p class="text-slate-400 text-[9px] mt-0.5">ARKA & DIMAS</p>
            </div>
            <div class="bg-slate-950 p-2 rounded-lg border border-blue-500/40">
              <div class="font-bold text-blue-400">4. Execution</div>
              <p class="text-slate-400 text-[9px] mt-0.5">RAKA / Specialists</p>
            </div>
            <div class="bg-slate-950 p-2 rounded-lg border border-blue-500/40">
              <div class="font-bold text-blue-400">5. Validation</div>
              <p class="text-slate-400 text-[9px] mt-0.5">Peer Review</p>
            </div>
            <div class="bg-slate-950 p-2 rounded-lg border border-blue-500/40">
              <div class="font-bold text-blue-400">6. Quality Ctrl</div>
              <p class="text-slate-400 text-[9px] mt-0.5">ARKA & SEKAR</p>
            </div>
            <div class="bg-slate-950 p-2 rounded-lg border border-emerald-500/60 bg-emerald-950/20">
              <div class="font-bold text-emerald-400">7. Reporting</div>
              <p class="text-emerald-300 text-[9px] mt-0.5">ARKA (Boardroom)</p>
            </div>
          </div>
        </div>
      </div>
"""

old_tab_tasks = '      <!-- Tab 2: Task Ledger -->'
assert old_tab_tasks in html, "Could not find old_tab_tasks"
html = html.replace(old_tab_tasks, employee_tab_html + "\n" + old_tab_tasks, 1)

# 5. Update switchDrawerTab implementation
old_switch_fn = """    function switchDrawerTab(tab) {
      document.getElementById('drawerTabReport').classList.toggle('hidden', tab !== 'report');
      document.getElementById('drawerTabTasks').classList.toggle('hidden', tab !== 'tasks');
      document.getElementById('drawerTabDrive').classList.toggle('hidden', tab !== 'drive');

      document.getElementById('tabBtnReport').className = tab === 'report' ? 
        'flex-1 py-3 text-center font-semibold text-blue-400 border-b-2 border-blue-500' :
        'flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent';
      document.getElementById('tabBtnTasks').className = tab === 'tasks' ? 
        'flex-1 py-3 text-center font-semibold text-blue-400 border-b-2 border-blue-500' :
        'flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent';
      document.getElementById('tabBtnDrive').className = tab === 'drive' ? 
        'flex-1 py-3 text-center font-semibold text-blue-400 border-b-2 border-blue-500' :
        'flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent';
    }"""

new_switch_fn = """    function switchDrawerTab(tab) {
      document.getElementById('drawerTabReport').classList.toggle('hidden', tab !== 'report');
      const empTab = document.getElementById('drawerTabEmployees');
      if (empTab) empTab.classList.toggle('hidden', tab !== 'employees');
      document.getElementById('drawerTabTasks').classList.toggle('hidden', tab !== 'tasks');
      document.getElementById('drawerTabDrive').classList.toggle('hidden', tab !== 'drive');

      const tabs = [
        { id: 'tabBtnReport', name: 'report' },
        { id: 'tabBtnEmployees', name: 'employees' },
        { id: 'tabBtnTasks', name: 'tasks' },
        { id: 'tabBtnDrive', name: 'drive' }
      ];

      tabs.forEach(t => {
        const btn = document.getElementById(t.id);
        if (btn) {
          btn.className = tab === t.name ?
            'flex-1 py-3 text-center font-bold text-blue-400 border-b-2 border-blue-500' :
            'flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent';
        }
      });
    }"""

assert old_switch_fn in html, "Could not find old_switch_fn"
html = html.replace(old_switch_fn, new_switch_fn, 1)

# 6. Update loadDocContent to have resilient multi-tier fallback
old_load_doc = """      try {
        const res = await fetch(`/api/report/${encodeURIComponent(filename)}`);
        if (!res.ok) throw new Error('File tidak ditemukan di server');
        const text = await res.text();"""

new_load_doc = """      try {
        let res = await fetch(`/api/report/${encodeURIComponent(filename)}`);
        if (!res.ok) {
          // Fallback 1: strip folder prefix
          const baseName = filename.split('/').pop();
          res = await fetch(`/api/report/${encodeURIComponent(baseName)}`);
        }
        if (!res.ok) {
          // Fallback 2: master audit report
          res = await fetch(`/api/report/LAPORAN_AUDIT_3C_22_PERANGKAT_DAERAH.md`);
        }
        if (!res.ok) throw new Error('File tidak ditemukan di server');
        const text = await res.text();"""

assert old_load_doc in html, "Could not find old_load_doc"
html = html.replace(old_load_doc, new_load_doc, 1)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("public/index.html successfully updated with Employee Skill Matrix tab and resilient loadDocContent()!")
