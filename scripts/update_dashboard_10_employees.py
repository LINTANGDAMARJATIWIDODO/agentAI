"""
NEXUS AI ENTERPRISE — Update Dashboard to 10 Employees & 14 Facilities
Integrates:
- Laporan Audit
- Skill Matrix & Proof (10 Employees)
- Employee Directory (10 Employees with filters & manifests)
- Organization Structure (Interactive visual hierarchy)
- Department Management (14 Virtual Office Facilities)
- Project Management (Integrated project pipelines)
- Office Workspace (Virtual office floor map & facility detailer)
- Performance Analytics (Workforce metrics & competency distributions)
- Status Tugas
- Drive & SPBE
"""

import os
import re

INDEX_PATH = r"C:\Users\LENOVO\.gemini\antigravity\scratch\NEXUS-AI-ENTERPRISE\public\index.html"

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Subtitle in Header (Pusat Laporan & Bukti Dokumen)
html = html.replace(
    'Hasil audit real-time 5 Direktur AI',
    'Hasil audit & tata kelola 10 Karyawan Profesional AI (14 Fasilitas Kantor)'
)

# 2. Replace Tab Selector
old_tab_selector = '''    <!-- Tab Selector -->
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
    </div>'''

new_tab_selector = '''    <!-- Tab Selector: 10 Executive Tabs (Scrollable) -->
    <div class="flex border-b border-slate-800 bg-slate-950 text-xs overflow-x-auto whitespace-nowrap scrollbar-thin px-2 py-1 gap-1">
      <button onclick="switchDrawerTab('report')" id="tabBtnReport" class="px-3 py-2 text-center font-bold text-blue-400 border-b-2 border-blue-500 flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-solid fa-file-lines"></i><span>Laporan Audit</span>
      </button>
      <button onclick="switchDrawerTab('employees')" id="tabBtnEmployees" class="px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-solid fa-user-check"></i><span>Skill Matrix & Proof (10)</span>
      </button>
      <button onclick="switchDrawerTab('directory')" id="tabBtnDirectory" class="px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-solid fa-address-book"></i><span>Employee Directory</span>
      </button>
      <button onclick="switchDrawerTab('org')" id="tabBtnOrg" class="px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-solid fa-sitemap"></i><span>Organization Structure</span>
      </button>
      <button onclick="switchDrawerTab('departments')" id="tabBtnDepartments" class="px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-solid fa-building"></i><span>Department Management (14)</span>
      </button>
      <button onclick="switchDrawerTab('projects')" id="tabBtnProjects" class="px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-solid fa-diagram-project"></i><span>Project Management</span>
      </button>
      <button onclick="switchDrawerTab('workspace')" id="tabBtnWorkspace" class="px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-solid fa-network-wired"></i><span>Office Workspace</span>
      </button>
      <button onclick="switchDrawerTab('analytics')" id="tabBtnAnalytics" class="px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-solid fa-chart-pie"></i><span>Performance Analytics</span>
      </button>
      <button onclick="switchDrawerTab('tasks')" id="tabBtnTasks" class="px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-solid fa-list-check"></i><span>Status Tugas</span>
      </button>
      <button onclick="switchDrawerTab('drive')" id="tabBtnDrive" class="px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition">
        <i class="fa-brands fa-google-drive"></i><span>Drive & SPBE</span>
      </button>
    </div>'''

if old_tab_selector in html:
    html = html.replace(old_tab_selector, new_tab_selector)
    print("Replaced Tab Selector Bar.")
else:
    print("Warning: old_tab_selector not exact match, using regex replacement.")
    html = re.sub(r'<!-- Tab Selector -->.*?</div>\s*<!-- Drawer Body -->', new_tab_selector + '\n\n    <!-- Drawer Body -->', html, flags=re.DOTALL)

# 3. Create the Complete 10-Employee Skill Matrix Cards & The New Tabs HTML
expanded_tabs_html = '''
      <!-- Tab: Employee Skill Matrix & Proof-of-Competency Dashboard (10 EMPLOYEES) -->
      <div id="drawerTabEmployees" class="space-y-4 hidden">
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-500/30 rounded-2xl p-4 shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-xs font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-award text-amber-400"></i>
                <span>Employee Skill Matrix & Proof-of-Competency (10 Karyawan Profesional)</span>
              </h3>
              <p class="text-[11px] text-slate-300 mt-0.5">Sistem evaluasi kinerja empiris & bukti nyata hasil kerja 10 Karyawan AI NEXUS (Level 5 Expert & Level 4 Senior)</p>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-[10px] bg-blue-500/20 text-blue-300 border border-blue-500/40 px-2.5 py-1 rounded-full font-bold">5 LEVEL 5 EXPERTS</span>
              <span class="text-[10px] bg-purple-500/20 text-purple-300 border border-purple-500/40 px-2.5 py-1 rounded-full font-bold">5 LEVEL 4 SENIORS</span>
            </div>
          </div>
        </div>

        <!-- 10 Employee Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <!-- 1. ARKA Card -->
          <div class="bg-slate-900 border border-blue-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">👔</span>
                <div>
                  <h4 class="font-bold text-white">ARKA</h4>
                  <p class="text-[10px] text-blue-400 font-semibold">Chief Executive & Strategic Director</p>
                </div>
              </div>
              <span class="text-[9px] bg-blue-500/20 text-blue-300 border border-blue-500/30 px-2 py-0.5 rounded font-bold">Level 5 (4.92 / 5.0)</span>
            </div>
            <p class="text-[11px] text-slate-300">Kepemimpinan eksekutif, orkestrasi multi-agen 10 staf, gatekeeping 7-stage quality lifecycle, dan sintesis keputusan strategis.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-amber-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-shield-halved"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Mengevaluasi hasil kerja 9 divisi, merekonsiliasi biaya server RAKA dengan budget SEKAR, dan menerbitkan Memorandum Keputusan Direksi.</p>
            </div>
          </div>

          <!-- 2. NAYA Card -->
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">🔬</span>
                <div>
                  <h4 class="font-bold text-white">NAYA</h4>
                  <p class="text-[10px] text-emerald-400 font-semibold">Director of Research & Business Intelligence</p>
                </div>
              </div>
              <span class="text-[9px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded font-bold">Level 5 (4.95 / 5.0)</span>
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

          <!-- 3. RAKA Card -->
          <div class="bg-slate-900 border border-purple-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">⚡</span>
                <div>
                  <h4 class="font-bold text-white">RAKA</h4>
                  <p class="text-[10px] text-purple-400 font-semibold">Chief Technology & Engineering Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-purple-500/20 text-purple-300 border border-purple-500/30 px-2 py-0.5 rounded font-bold">Level 5 (4.98 / 5.0)</span>
            </div>
            <p class="text-[11px] text-slate-300">Arsitektur sistem enterprise, rekayasa perangkat lunak full-stack, distributed API gateway, dan pengujian otomatis CI/CD.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-amber-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-code"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Aplikasi Enterprise Gateway microservice berjalan nyata (6/6 unit test lulus 100% dalam 0.12s, HMAC SHA256 auth, token bucket rate limiter).</p>
            </div>
          </div>

          <!-- 4. SEKAR Card -->
          <div class="bg-slate-900 border border-rose-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">⚖️</span>
                <div>
                  <h4 class="font-bold text-white">SEKAR</h4>
                  <p class="text-[10px] text-rose-400 font-semibold">Chief Financial, Risk & Compliance Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-rose-500/20 text-rose-300 border border-rose-500/30 px-2 py-0.5 rounded font-bold">Level 5 (4.90 / 5.0)</span>
            </div>
            <p class="text-[11px] text-slate-300">Audit forensik keuangan, pemodelan 3-laporan keuangan, mitigasi risiko enterprise (ERM), dan kepatuhan regulasi SPBE.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-amber-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-file-invoice-dollar"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Engine audit forensik mendeteksi ketidakseimbangan neraca $450k, salah saji EBITDA $350k, dan defisit runway kas dalam uji stres likuiditas.</p>
            </div>
          </div>

          <!-- 5. DIMAS Card -->
          <div class="bg-slate-900 border border-amber-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">📈</span>
                <div>
                  <h4 class="font-bold text-white">DIMAS</h4>
                  <p class="text-[10px] text-amber-400 font-semibold">Chief Operations & Business Growth Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded font-bold">Level 5 (4.94 / 5.0)</span>
            </div>
            <p class="text-[11px] text-slate-300">Operasional bisnis enterprise, matriks akuntabilitas RACI lintas departemen, roadmap WBS 90 hari, dan eksekusi pertumbuhan.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-amber-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-list-check"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Roadmap WBS 90 hari & RACI matrix dengan 12 deliverable terukur tanpa celah bottleneck operasional.</p>
            </div>
          </div>

          <!-- 6. ADITYA Card (NEW) -->
          <div class="bg-slate-900 border border-pink-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">🎨</span>
                <div>
                  <h4 class="font-bold text-white">ADITYA</h4>
                  <p class="text-[10px] text-pink-400 font-semibold">Chief Product Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-pink-500/20 text-pink-300 border border-pink-500/30 px-2 py-0.5 rounded font-bold">Level 4 (4.65 / 5.0)</span>
            </div>
            <p class="text-[11px] text-slate-300">Product management, arsitektur UI/UX design systems, Figma token synchronization, dan standar aksesibilitas WCAG 2.1 AA/AAA.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-pink-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-palette"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Validator Design System & WCAG contrast engine mengevaluasi 6 token antarmuka (rasio 17.5:1 Text-to-Surface, 6/6 Uji Lulus di `proofs/aditya_product_proof/`).</p>
            </div>
          </div>

          <!-- 7. BIMA Card (NEW) -->
          <div class="bg-slate-900 border border-red-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">🛡️</span>
                <div>
                  <h4 class="font-bold text-white">BIMA</h4>
                  <p class="text-[10px] text-red-400 font-semibold">Chief Information Security Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-red-500/20 text-red-300 border border-red-500/30 px-2 py-0.5 rounded font-bold">Level 4 (4.70 / 5.0)</span>
            </div>
            <p class="text-[11px] text-slate-300">Tata kelola keamanan siber, pemodelan ancaman STRIDE, audit OWASP Top 10, SAST code scanner, dan kepatuhan UU PDP.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-red-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-shield-virus"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">SAST Security Auditor mendeteksi 3 kerentanan OWASP (Hardcoded Secret, SQL Injection, Permissive CORS) dengan 0 false positives di `proofs/bima_security_proof/`.</p>
            </div>
          </div>

          <!-- 8. TARA Card (NEW) -->
          <div class="bg-slate-900 border border-teal-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">🗄️</span>
                <div>
                  <h4 class="font-bold text-white">TARA</h4>
                  <p class="text-[10px] text-teal-400 font-semibold">Chief Data Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-teal-500/20 text-teal-300 border border-teal-500/30 px-2 py-0.5 rounded font-bold">Level 4 (4.68 / 5.0)</span>
            </div>
            <p class="text-[11px] text-slate-300">Data engineering, arsitektur database PostgreSQL/MySQL, data warehouse dimensional Star Schema, dan validasi Great Expectations.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-teal-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-database"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Pipeline ETL mentransformasi data mentah ke Star Schema Mart dan meluluskan 4/4 Uji Kualitas Data (Uniqueness, Non-null, Referential Integrity) di `proofs/tara_data_proof/`.</p>
            </div>
          </div>

          <!-- 9. KIRANA Card (NEW) -->
          <div class="bg-slate-900 border border-yellow-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">📢</span>
                <div>
                  <h4 class="font-bold text-white">KIRANA</h4>
                  <p class="text-[10px] text-yellow-400 font-semibold">Chief Marketing Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-yellow-500/20 text-yellow-300 border border-yellow-500/30 px-2 py-0.5 rounded font-bold">Level 4 (4.58 / 5.0)</span>
            </div>
            <p class="text-[11px] text-slate-300">Pemasaran digital terpadu, semantic SEO, branding korporat, pemodelan unit ekonomi CAC/LTV, dan akuisisi pelanggan multichannel.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-yellow-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-bullhorn"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Model Atribusi Pertumbuhan Multi-Kanal mengoptimalkan rasio LTV:CAC mencapai >3.0x pada Organic SEO & Referral di `proofs/kirana_marketing_proof/`.</p>
            </div>
          </div>

          <!-- 10. FARREL Card (NEW) -->
          <div class="bg-slate-900 border border-violet-500/40 rounded-xl p-3.5 space-y-2">
            <div class="flex items-start justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">🔬</span>
                <div>
                  <h4 class="font-bold text-white">FARREL</h4>
                  <p class="text-[10px] text-violet-400 font-semibold">Chief Quality Assurance Officer</p>
                </div>
              </div>
              <span class="text-[9px] bg-violet-500/20 text-violet-300 border border-violet-500/30 px-2 py-0.5 rounded font-bold">Level 4 (4.72 / 5.0)</span>
            </div>
            <p class="text-[11px] text-slate-300">Otomasi pengujian perangkat lunak, Playwright E2E, verifikasi kontrak API, continuous regression testing, dan defect severity triage.</p>
            <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[10px] space-y-1">
              <div class="text-violet-400 font-bold flex items-center gap-1">
                <i class="fa-solid fa-vial-circle-check"></i>
                <span>Bukti Nyata Kemampuan:</span>
              </div>
              <p class="text-slate-300">Automated Test Harness mengeksekusi 8/8 uji regresi API (100% Pass, SLA latency p95 <50ms, zero blocker) di `proofs/farrel_qa_proof/`.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab: Employee Directory -->
      <div id="drawerTabDirectory" class="space-y-4 hidden">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
          <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
            <div>
              <h3 class="text-xs font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-address-book text-blue-400"></i>
                <span>NEXUS Employee Directory (10 Tenaga Ahli Profesional)</span>
              </h3>
              <p class="text-[11px] text-slate-400">Daftar lengkap seluruh karyawan AI beserta departemen, kontak internal, dan spesialisasi.</p>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="bg-blue-600/20 text-blue-300 border border-blue-500/30 px-2.5 py-1 rounded-lg font-mono font-bold">TOTAL: 10 STAF</span>
            </div>
          </div>
        </div>

        <div class="overflow-x-auto rounded-xl border border-slate-800">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-950 text-slate-400 border-b border-slate-800">
              <tr>
                <th class="p-3">KARYAWAN</th>
                <th class="p-3">JABATAN</th>
                <th class="p-3">DEPARTEMEN</th>
                <th class="p-3">LEVEL</th>
                <th class="p-3">SKOR</th>
                <th class="p-3">STATUS</th>
                <th class="p-3">MANIFEST</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/60 bg-slate-900/60 text-slate-300" id="directoryTableBody">
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">👔</span> ARKA</td>
                <td class="p-3 text-blue-400 font-semibold">Chief Executive & Strategic Director</td>
                <td class="p-3">Executive Office (#1)</td>
                <td class="p-3"><span class="bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 5 Expert</span></td>
                <td class="p-3 font-mono font-bold text-white">4.92</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/ARKA_SKILL_MANIFEST.md" target="_blank" class="text-blue-400 hover:underline">ARKA.md</a></td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">🔬</span> NAYA</td>
                <td class="p-3 text-emerald-400 font-semibold">Director of Research & BI</td>
                <td class="p-3">Research & Intelligence Center (#2)</td>
                <td class="p-3"><span class="bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 5 Expert</span></td>
                <td class="p-3 font-mono font-bold text-white">4.95</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/NAYA_SKILL_MANIFEST.md" target="_blank" class="text-emerald-400 hover:underline">NAYA.md</a></td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">⚡</span> RAKA</td>
                <td class="p-3 text-purple-400 font-semibold">Chief Technology Officer</td>
                <td class="p-3">Technology & Engineering (#3)</td>
                <td class="p-3"><span class="bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 5 Expert</span></td>
                <td class="p-3 font-mono font-bold text-white">4.98</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/RAKA_SKILL_MANIFEST.md" target="_blank" class="text-purple-400 hover:underline">RAKA.md</a></td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">⚖️</span> SEKAR</td>
                <td class="p-3 text-rose-400 font-semibold">Chief Financial & Compliance Off.</td>
                <td class="p-3">Finance & Risk Management (#4)</td>
                <td class="p-3"><span class="bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 5 Expert</span></td>
                <td class="p-3 font-mono font-bold text-white">4.90</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/SEKAR_SKILL_MANIFEST.md" target="_blank" class="text-rose-400 hover:underline">SEKAR.md</a></td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">📈</span> DIMAS</td>
                <td class="p-3 text-amber-400 font-semibold">Chief Operations Officer</td>
                <td class="p-3">Business Operations Dept (#5)</td>
                <td class="p-3"><span class="bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 5 Expert</span></td>
                <td class="p-3 font-mono font-bold text-white">4.94</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/DIMAS_SKILL_MANIFEST.md" target="_blank" class="text-amber-400 hover:underline">DIMAS.md</a></td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">🎨</span> ADITYA</td>
                <td class="p-3 text-pink-400 font-semibold">Chief Product Officer</td>
                <td class="p-3">Product Design Studio (#6)</td>
                <td class="p-3"><span class="bg-pink-500/20 text-pink-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 4 Senior</span></td>
                <td class="p-3 font-mono font-bold text-white">4.65</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/ADITYA_SKILL_MANIFEST.md" target="_blank" class="text-pink-400 hover:underline">ADITYA.md</a></td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">🛡️</span> BIMA</td>
                <td class="p-3 text-red-400 font-semibold">Chief Information Security Off.</td>
                <td class="p-3">Cybersecurity Operations Center (#7)</td>
                <td class="p-3"><span class="bg-red-500/20 text-red-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 4 Senior</span></td>
                <td class="p-3 font-mono font-bold text-white">4.70</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/BIMA_SKILL_MANIFEST.md" target="_blank" class="text-red-400 hover:underline">BIMA.md</a></td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">🗄️</span> TARA</td>
                <td class="p-3 text-teal-400 font-semibold">Chief Data Officer</td>
                <td class="p-3">Data Engineering Center (#8)</td>
                <td class="p-3"><span class="bg-teal-500/20 text-teal-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 4 Senior</span></td>
                <td class="p-3 font-mono font-bold text-white">4.68</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/TARA_SKILL_MANIFEST.md" target="_blank" class="text-teal-400 hover:underline">TARA.md</a></td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">📢</span> KIRANA</td>
                <td class="p-3 text-yellow-400 font-semibold">Chief Marketing Officer</td>
                <td class="p-3">Marketing & Branding Studio (#9)</td>
                <td class="p-3"><span class="bg-yellow-500/20 text-yellow-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 4 Senior</span></td>
                <td class="p-3 font-mono font-bold text-white">4.58</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/KIRANA_SKILL_MANIFEST.md" target="_blank" class="text-yellow-400 hover:underline">KIRANA.md</a></td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white flex items-center gap-2"><span class="text-lg">🔬</span> FARREL</td>
                <td class="p-3 text-violet-400 font-semibold">Chief Quality Assurance Officer</td>
                <td class="p-3">Quality Assurance Laboratory (#10)</td>
                <td class="p-3"><span class="bg-violet-500/20 text-violet-300 px-2 py-0.5 rounded text-[10px] font-bold">Level 4 Senior</span></td>
                <td class="p-3 font-mono font-bold text-white">4.72</td>
                <td class="p-3"><span class="text-emerald-400 font-semibold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ACTIVE</span></td>
                <td class="p-3"><a href="/FARREL_SKILL_MANIFEST.md" target="_blank" class="text-violet-400 hover:underline">FARREL.md</a></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab: Organization Structure -->
      <div id="drawerTabOrg" class="space-y-4 hidden">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
          <h3 class="text-xs font-bold text-white flex items-center gap-2">
            <i class="fa-solid fa-sitemap text-blue-400"></i>
            <span>NEXUS AI Enterprise Organization Structure</span>
          </h3>
          <p class="text-[11px] text-slate-400 mt-0.5">Bagan tata kelola eksekutif dan pembagian 3 pilar operasional korporat.</p>
        </div>

        <div class="bg-slate-950 p-6 rounded-2xl border border-slate-800 flex flex-col items-center space-y-6 text-xs">
          <!-- Tier 1: Board of Directors / Human -->
          <div class="bg-gradient-to-r from-amber-950/60 to-slate-900 border-2 border-amber-500/60 rounded-xl px-6 py-2.5 text-center shadow-lg">
            <div class="text-[10px] font-bold text-amber-400 uppercase tracking-wider">BOARD OF DIRECTORS / USER</div>
            <div class="font-bold text-white text-sm">Human Supervisory Authority</div>
          </div>

          <div class="w-0.5 h-6 bg-slate-700"></div>

          <!-- Tier 2: ARKA (CEO) -->
          <div class="bg-gradient-to-r from-blue-950 to-slate-900 border-2 border-blue-500 rounded-2xl p-4 text-center max-w-sm shadow-xl space-y-1">
            <div class="text-3xl">👔</div>
            <div class="font-bold text-white text-sm">ARKA</div>
            <div class="text-blue-400 font-semibold text-xs">Chief Executive & Strategic Director</div>
            <p class="text-[10px] text-slate-300">Pusat orkestrasi 10 karyawan, resolusi konflik, dan penjamin mutu 7-stage lifecycle.</p>
          </div>

          <div class="w-full border-t border-slate-800 relative">
            <div class="absolute left-1/2 -top-3 -translate-x-1/2 bg-slate-900 px-3 text-[10px] text-slate-400 font-mono">TIGA DIVISI EKSEKUTIF</div>
          </div>

          <!-- Tier 3: Three Divisions -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
            <!-- Division 1 -->
            <div class="bg-slate-900/90 border border-purple-500/40 rounded-xl p-3.5 space-y-3">
              <div class="text-purple-400 font-bold border-b border-purple-500/20 pb-1.5 flex items-center justify-between">
                <span>PRODUCT & ENGINEERING</span>
                <i class="fa-solid fa-laptop-code"></i>
              </div>
              <div class="space-y-2">
                <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 flex items-center gap-2">
                  <span class="text-xl">🎨</span>
                  <div>
                    <div class="font-bold text-white text-[11px]">ADITYA</div>
                    <div class="text-pink-400 text-[10px]">Chief Product Officer</div>
                  </div>
                </div>
                <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 flex items-center gap-2">
                  <span class="text-xl">⚡</span>
                  <div>
                    <div class="font-bold text-white text-[11px]">RAKA</div>
                    <div class="text-purple-400 text-[10px]">Chief Technology Officer</div>
                  </div>
                </div>
                <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 flex items-center gap-2">
                  <span class="text-xl">🗄️</span>
                  <div>
                    <div class="font-bold text-white text-[11px]">TARA</div>
                    <div class="text-teal-400 text-[10px]">Chief Data Officer</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Division 2 -->
            <div class="bg-slate-900/90 border border-amber-500/40 rounded-xl p-3.5 space-y-3">
              <div class="text-amber-400 font-bold border-b border-amber-500/20 pb-1.5 flex items-center justify-between">
                <span>GROWTH & OPERATIONS</span>
                <i class="fa-solid fa-chart-line"></i>
              </div>
              <div class="space-y-2">
                <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 flex items-center gap-2">
                  <span class="text-xl">📈</span>
                  <div>
                    <div class="font-bold text-white text-[11px]">DIMAS</div>
                    <div class="text-amber-400 text-[10px]">Chief Operations Officer</div>
                  </div>
                </div>
                <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 flex items-center gap-2">
                  <span class="text-xl">📢</span>
                  <div>
                    <div class="font-bold text-white text-[11px]">KIRANA</div>
                    <div class="text-yellow-400 text-[10px]">Chief Marketing Officer</div>
                  </div>
                </div>
                <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 flex items-center gap-2">
                  <span class="text-xl">🔬</span>
                  <div>
                    <div class="font-bold text-white text-[11px]">NAYA</div>
                    <div class="text-emerald-400 text-[10px]">Director of Research & BI</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Division 3 -->
            <div class="bg-slate-900/90 border border-rose-500/40 rounded-xl p-3.5 space-y-3">
              <div class="text-rose-400 font-bold border-b border-rose-500/20 pb-1.5 flex items-center justify-between">
                <span>GOVERNANCE & ASSURANCE</span>
                <i class="fa-solid fa-shield-check"></i>
              </div>
              <div class="space-y-2">
                <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 flex items-center gap-2">
                  <span class="text-xl">⚖️</span>
                  <div>
                    <div class="font-bold text-white text-[11px]">SEKAR</div>
                    <div class="text-rose-400 text-[10px]">Chief Financial & Compliance Off.</div>
                  </div>
                </div>
                <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 flex items-center gap-2">
                  <span class="text-xl">🛡️</span>
                  <div>
                    <div class="font-bold text-white text-[11px]">BIMA</div>
                    <div class="text-red-400 text-[10px]">Chief Info Security Officer</div>
                  </div>
                </div>
                <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 flex items-center gap-2">
                  <span class="text-xl">🔬</span>
                  <div>
                    <div class="font-bold text-white text-[11px]">FARREL</div>
                    <div class="text-violet-400 text-[10px]">Chief QA Officer</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab: Department Management (14 Facilities) -->
      <div id="drawerTabDepartments" class="space-y-4 hidden">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex items-center justify-between">
          <div>
            <h3 class="text-xs font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-building text-blue-400"></i>
              <span>14 Facilities & Department Management</span>
            </h3>
            <p class="text-[11px] text-slate-400 mt-0.5">Tata kelola seluruh ruangan kantor virtual, PIC penanggung jawab, Key KPI, dan dokumen SOP resmi.</p>
          </div>
          <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2.5 py-1 rounded-lg text-xs font-mono font-bold">14 FASILITAS AKTIF</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs" id="departmentsListContainer">
          <!-- 14 Facility Cards generated statically & hydrated dynamically -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">👔</span> #1 Executive Office</span>
              <span class="text-[10px] bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded font-bold">PIC: ARKA</span>
            </div>
            <p class="text-[11px] text-slate-300">Executive governance, board assemblies, strategic resource allocation, and multi-agent orchestration.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: Alignment 100%</span>
              <span class="text-blue-400 font-mono">SOP-EXEC-001</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">🔬</span> #2 Research & Intelligence Center</span>
              <span class="text-[10px] bg-teal-500/20 text-teal-300 px-2 py-0.5 rounded font-bold">PIC: NAYA</span>
            </div>
            <p class="text-[11px] text-slate-300">Data intelligence, empirical statistical modeling, competitive benchmarking, and source verification.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: Source Accuracy 100%</span>
              <span class="text-teal-400 font-mono">SOP-RES-002</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">⚡</span> #3 Technology & Engineering</span>
              <span class="text-[10px] bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded font-bold">PIC: RAKA</span>
            </div>
            <p class="text-[11px] text-slate-300">Core backend engineering, system architecture, API gateway microservices, and CI/CD pipelines.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: p95 &lt;50ms</span>
              <span class="text-indigo-400 font-mono">SOP-ENG-003</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">⚖️</span> #4 Finance & Risk Management</span>
              <span class="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-bold">PIC: SEKAR</span>
            </div>
            <p class="text-[11px] text-slate-300">Financial forensic audits, statutory compliance, BAST document verification, and risk matrices.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: 0 Balance Variance</span>
              <span class="text-purple-400 font-mono">SOP-FIN-004</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">📈</span> #5 Business Operations</span>
              <span class="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded font-bold">PIC: DIMAS</span>
            </div>
            <p class="text-[11px] text-slate-300">Operational execution, cross-departmental RACI matrices, 90-day WBS roadmaps, and growth milestones.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: WBS On-Time &gt;95%</span>
              <span class="text-amber-400 font-mono">SOP-OPS-005</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">🎨</span> #6 Product Design Studio</span>
              <span class="text-[10px] bg-pink-500/20 text-pink-300 px-2 py-0.5 rounded font-bold">PIC: ADITYA</span>
            </div>
            <p class="text-[11px] text-slate-300">Product strategy, UI/UX prototyping, design token systems, and WCAG accessibility standards.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: WCAG 2.1 AA 100%</span>
              <span class="text-pink-400 font-mono">SOP-PRD-006</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">🛡️</span> #7 Cybersecurity Operations Center</span>
              <span class="text-[10px] bg-red-500/20 text-red-300 px-2 py-0.5 rounded font-bold">PIC: BIMA</span>
            </div>
            <p class="text-[11px] text-slate-300">Threat hunting, SAST/DAST vulnerability assessments, OWASP auditing, and Zero-Trust network security.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: Zero Critical CVEs</span>
              <span class="text-red-400 font-mono">SOP-SEC-007</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">🗄️</span> #8 Data Engineering Center</span>
              <span class="text-[10px] bg-teal-500/20 text-teal-300 px-2 py-0.5 rounded font-bold">PIC: TARA</span>
            </div>
            <p class="text-[11px] text-slate-300">Relational schema modeling, database administration, idempotent ETL/ELT pipelines, and data quality tests.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: Pass Rate &gt;99.5%</span>
              <span class="text-teal-400 font-mono">SOP-DAT-008</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">📢</span> #9 Marketing & Branding Studio</span>
              <span class="text-[10px] bg-yellow-500/20 text-yellow-300 px-2 py-0.5 rounded font-bold">PIC: KIRANA</span>
            </div>
            <p class="text-[11px] text-slate-300">Digital marketing campaigns, technical & semantic SEO, brand positioning, and CAC/LTV analytics.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: LTV:CAC &gt;3.0x</span>
              <span class="text-yellow-400 font-mono">SOP-MKT-009</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">🔬</span> #10 Quality Assurance Laboratory</span>
              <span class="text-[10px] bg-violet-500/20 text-violet-300 px-2 py-0.5 rounded font-bold">PIC: FARREL</span>
            </div>
            <p class="text-[11px] text-slate-300">Automated E2E Playwright testing, REST API contract suites, continuous regression matrices, and defect triage.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: Regression 100% Pass</span>
              <span class="text-violet-400 font-mono">SOP-QAS-010</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">🏛️</span> #11 Enterprise Conference Room</span>
              <span class="text-[10px] bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded font-bold">PIC: All (ARKA)</span>
            </div>
            <p class="text-[11px] text-slate-300">All-hands company assemblies, strategic alignment summits, and executive board reviews.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: Strategy Sync 100%</span>
              <span class="text-blue-400 font-mono">SOP-ALL-011</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">📋</span> #12 Project Management Office</span>
              <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold">PIC: DIMAS & ARKA</span>
            </div>
            <p class="text-[11px] text-slate-300">Enterprise project portfolio governance, sprint tracking, multi-agent dependency mapping, and resource planning.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: Blocker Resolution &lt;24h</span>
              <span class="text-emerald-400 font-mono">SOP-PMO-012</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">📚</span> #13 Central Knowledge Repository</span>
              <span class="text-[10px] bg-slate-500/20 text-slate-300 px-2 py-0.5 rounded font-bold">PIC: NAYA & TARA</span>
            </div>
            <p class="text-[11px] text-slate-300">Enterprise documentation hub, SPBE master registers, data dictionaries, and architectural guidelines.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: Freshness Index &gt;98%</span>
              <span class="text-slate-400 font-mono">SOP-KNW-013</span>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-white flex items-center gap-2"><span class="text-lg">🚀</span> #14 Innovation & Development</span>
              <span class="text-[10px] bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded font-bold">PIC: RAKA & ADITYA</span>
            </div>
            <p class="text-[11px] text-slate-300">Sandbox prototyping, next-gen AI experimentation, design lab sprints, and proof-of-concept incubations.</p>
            <div class="text-[10px] text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800">
              <span>KPI: PoC-to-Prod Velocity</span>
              <span class="text-cyan-400 font-mono">SOP-INN-014</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab: Project Management -->
      <div id="drawerTabProjects" class="space-y-4 hidden">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
          <h3 class="text-xs font-bold text-white flex items-center gap-2">
            <i class="fa-solid fa-diagram-project text-blue-400"></i>
            <span>Integrated Multi-Agent Project Pipelines</span>
          </h3>
          <p class="text-[11px] text-slate-400 mt-0.5">Pemantauan alur kolaborasi 10 karyawan pada proyek strategis korporat.</p>
        </div>

        <div class="space-y-3 text-xs">
          <!-- Project 1 -->
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-4 space-y-3">
            <div class="flex items-center justify-between">
              <div>
                <span class="text-[9px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-2 py-0.5 rounded font-bold">SELESAI & TERVERIFIKASI</span>
                <h4 class="font-bold text-white text-sm mt-1">Audit Forensik 3C SPBE 22 Perangkat Daerah DKI Jakarta</h4>
              </div>
              <span class="font-mono text-emerald-400 font-bold text-sm">100%</span>
            </div>
            <p class="text-[11px] text-slate-300">Audit kelengkapan 42 kolom (Domain, RAB L1-L7, RAL L3, Gap Analysis, Baris Sumber) untuk seluruh 22 OPD, disertai 28 sheet rekap domain belum ada tanpa fabrikasi.</p>
            <div class="grid grid-cols-2 gap-2 text-[10px]">
              <div class="bg-slate-950 p-2 rounded border border-slate-800 text-slate-300">
                <span class="text-slate-400 block font-semibold">Orkestrator:</span> ARKA
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 text-slate-300">
                <span class="text-slate-400 block font-semibold">Kolaborator:</span> NAYA, RAKA, SEKAR, DIMAS, TARA, FARREL
              </div>
            </div>
          </div>

          <!-- Project 2 (10-Step Lifecycle) -->
          <div class="bg-slate-900 border border-blue-500/40 rounded-xl p-4 space-y-3">
            <div class="flex items-center justify-between">
              <div>
                <span class="text-[9px] bg-blue-500/20 text-blue-300 border border-blue-500/40 px-2 py-0.5 rounded font-bold">SEDANG BERJALAN</span>
                <h4 class="font-bold text-white text-sm mt-1">Sistem Kolaborasi Siklus Hidup Aplikasi Web (10 Karyawan)</h4>
              </div>
              <span class="font-mono text-blue-400 font-bold text-sm">85%</span>
            </div>
            <p class="text-[11px] text-slate-300">Demonstrasi alur berantai 10 karyawan dari analisa kebutuhan hingga peluncuran:</p>
            
            <div class="space-y-1.5 text-[10px]">
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">1. Analisis Kebutuhan Bisnis (DIMAS)</span>
                <span class="text-emerald-400 font-bold">SELESAI ✓</span>
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">2. Konsep Produk, PRD & UI/UX Figma Tokens (ADITYA)</span>
                <span class="text-emerald-400 font-bold">SELESAI ✓</span>
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">3. Rekayasa Frontend, Backend & Gateway (RAKA)</span>
                <span class="text-emerald-400 font-bold">SELESAI ✓</span>
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">4. Database PostgreSQL & Star Schema ETL (TARA)</span>
                <span class="text-emerald-400 font-bold">SELESAI ✓</span>
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">5. Audit Keamanan Siber & SAST OWASP Top 10 (BIMA)</span>
                <span class="text-emerald-400 font-bold">SELESAI ✓</span>
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">6. Pengujian Otomatis Playwright & API Testing (FARREL)</span>
                <span class="text-emerald-400 font-bold">SELESAI ✓</span>
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">7. Analisis Data & Evaluasi Statistik (NAYA)</span>
                <span class="text-emerald-400 font-bold">SELESAI ✓</span>
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">8. Pemeriksaan Anggaran & Mitigasi Risiko (SEKAR)</span>
                <span class="text-emerald-400 font-bold">SELESAI ✓</span>
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">9. Strategi Pemasaran & Peluncuran SEO (KIRANA)</span>
                <span class="text-amber-400 font-bold">IN PROGRESS ⏳</span>
              </div>
              <div class="bg-slate-950 p-2 rounded border border-slate-800 flex items-center justify-between">
                <span class="text-white">10. Koordinasi Akhir & Evaluasi Eksekutif (ARKA)</span>
                <span class="text-amber-400 font-bold">IN PROGRESS ⏳</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab: Office Workspace (14 Facilities Map) -->
      <div id="drawerTabWorkspace" class="space-y-4 hidden">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex items-center justify-between">
          <div>
            <h3 class="text-xs font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-network-wired text-blue-400"></i>
              <span>NEXUS Virtual Office Floor Layout</span>
            </h3>
            <p class="text-[11px] text-slate-400 mt-0.5">Pemetaan 14 ruangan kerja interaktif, status keterisian, dan terminal kerja.</p>
          </div>
          <span class="bg-blue-500/20 text-blue-300 border border-blue-500/30 px-2.5 py-1 rounded-lg text-xs font-mono font-bold">ALL 14 ROOMS OCCUPIED</span>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5 text-xs">
          <!-- Room 1 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-blue-500/50 space-y-1.5 hover:border-blue-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">👔</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 1: Executive Office</div>
            <div class="text-[10px] text-blue-400 font-semibold">ARKA (CEO)</div>
            <div class="text-[9px] text-slate-400">Command & Control Desk</div>
          </div>

          <!-- Room 2 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-teal-500/50 space-y-1.5 hover:border-teal-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">🔬</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 2: Research Center</div>
            <div class="text-[10px] text-teal-400 font-semibold">NAYA (BI)</div>
            <div class="text-[9px] text-slate-400">Data Analytics Cluster</div>
          </div>

          <!-- Room 3 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-indigo-500/50 space-y-1.5 hover:border-indigo-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">⚡</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 3: Technology Lab</div>
            <div class="text-[10px] text-indigo-400 font-semibold">RAKA (CTO)</div>
            <div class="text-[9px] text-slate-400">CI/CD Build Servers</div>
          </div>

          <!-- Room 4 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-purple-500/50 space-y-1.5 hover:border-purple-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">⚖️</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 4: Finance & Risk</div>
            <div class="text-[10px] text-purple-400 font-semibold">SEKAR (CFO)</div>
            <div class="text-[9px] text-slate-400">Forensic Audit Workstation</div>
          </div>

          <!-- Room 5 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-amber-500/50 space-y-1.5 hover:border-amber-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">📈</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 5: Operations Room</div>
            <div class="text-[10px] text-amber-400 font-semibold">DIMAS (COO)</div>
            <div class="text-[9px] text-slate-400">WBS Agile Scrum Board</div>
          </div>

          <!-- Room 6 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-pink-500/50 space-y-1.5 hover:border-pink-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">🎨</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 6: Design Studio</div>
            <div class="text-[10px] text-pink-400 font-semibold">ADITYA (CPO)</div>
            <div class="text-[9px] text-slate-400">Figma Token Canvas</div>
          </div>

          <!-- Room 7 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-red-500/50 space-y-1.5 hover:border-red-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">🛡️</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 7: Security SOC</div>
            <div class="text-[10px] text-red-400 font-semibold">BIMA (CISO)</div>
            <div class="text-[9px] text-slate-400">Threat Matrix Wall</div>
          </div>

          <!-- Room 8 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-teal-500/50 space-y-1.5 hover:border-teal-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">🗄️</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 8: Data Center</div>
            <div class="text-[10px] text-teal-400 font-semibold">TARA (CDO)</div>
            <div class="text-[9px] text-slate-400">PostgreSQL Star Schemas</div>
          </div>

          <!-- Room 9 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-yellow-500/50 space-y-1.5 hover:border-yellow-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">📢</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 9: Marketing Studio</div>
            <div class="text-[10px] text-yellow-400 font-semibold">KIRANA (CMO)</div>
            <div class="text-[9px] text-slate-400">SEO & Growth Dashboard</div>
          </div>

          <!-- Room 10 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-violet-500/50 space-y-1.5 hover:border-violet-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">🔬</span>
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 10: QA Laboratory</div>
            <div class="text-[10px] text-violet-400 font-semibold">FARREL (QA)</div>
            <div class="text-[9px] text-slate-400">Playwright Test Runners</div>
          </div>

          <!-- Room 11 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-blue-400/40 space-y-1.5 hover:border-blue-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">🏛️</span>
              <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 11: Conference Hall</div>
            <div class="text-[10px] text-blue-300 font-semibold">Assembly (All)</div>
            <div class="text-[9px] text-slate-400">Executive Round Table</div>
          </div>

          <!-- Room 12 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-emerald-400/40 space-y-1.5 hover:border-emerald-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">📋</span>
              <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 12: PMO Office</div>
            <div class="text-[10px] text-emerald-300 font-semibold">DIMAS & ARKA</div>
            <div class="text-[9px] text-slate-400">Portfolio Delivery Hub</div>
          </div>

          <!-- Room 13 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-500/50 space-y-1.5 hover:border-slate-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">📚</span>
              <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 13: Knowledge Repo</div>
            <div class="text-[10px] text-slate-300 font-semibold">NAYA & TARA</div>
            <div class="text-[9px] text-slate-400">Living Architecture Hub</div>
          </div>

          <!-- Room 14 -->
          <div class="bg-slate-950 p-3 rounded-xl border border-cyan-500/50 space-y-1.5 hover:border-cyan-400 transition">
            <div class="flex items-center justify-between">
              <span class="text-xl">🚀</span>
              <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            </div>
            <div class="font-bold text-white text-[11px]">Room 14: Innovation Lab</div>
            <div class="text-[10px] text-cyan-300 font-semibold">RAKA & ADITYA</div>
            <div class="text-[9px] text-slate-400">Next-Gen Prototyping</div>
          </div>
        </div>
      </div>

      <!-- Tab: Performance Analytics -->
      <div id="drawerTabAnalytics" class="space-y-4 hidden">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
          <h3 class="text-xs font-bold text-white flex items-center gap-2">
            <i class="fa-solid fa-chart-pie text-blue-400"></i>
            <span>Performance Analytics & Workforce Competency Distribution</span>
          </h3>
          <p class="text-[11px] text-slate-400 mt-0.5">Analisis empiris skor kompetensi rata-rata dan distribusi pencapaian 10 karyawan AI.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center space-y-1">
            <div class="text-2xl font-bold text-blue-400 font-mono">4.80 / 5.0</div>
            <div class="text-white font-bold text-xs">Rata-rata Skor Tenaga Ahli</div>
            <p class="text-[10px] text-slate-400">Dihitung dari hasil uji pembuktian nyata tanpa penggelembungan angka.</p>
          </div>
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center space-y-1">
            <div class="text-2xl font-bold text-emerald-400 font-mono">100%</div>
            <div class="text-white font-bold text-xs">Validitas Bukti Pekerjaan</div>
            <p class="text-[10px] text-slate-400">10 dari 10 karyawan memiliki skrip pembuktian kemampuan di folder `proofs/`.</p>
          </div>
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 text-center space-y-1">
            <div class="text-2xl font-bold text-purple-400 font-mono">14 / 14</div>
            <div class="text-white font-bold text-xs">Fasilitas Kantor Beroperasi</div>
            <p class="text-[10px] text-slate-400">Seluruh ruangan kantor virtual memiliki PIC dan SOP terdefinisi.</p>
          </div>
        </div>

        <!-- Competency Distribution Progress Bars -->
        <div class="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-3 text-xs">
          <div class="font-bold text-white text-xs border-b border-slate-800 pb-2">Komparasi Skor Kompetensi 10 Karyawan</div>
          <div class="space-y-2">
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">RAKA (CTO) — System Architecture</span>
                <span class="text-purple-400 font-mono font-bold">4.98 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-purple-500 h-2 rounded-full" style="width: 99.6%"></div></div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">NAYA (BI) — Research Methodology</span>
                <span class="text-emerald-400 font-mono font-bold">4.95 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-emerald-500 h-2 rounded-full" style="width: 99.0%"></div></div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">DIMAS (COO) — Agile Operations</span>
                <span class="text-amber-400 font-mono font-bold">4.94 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-amber-500 h-2 rounded-full" style="width: 98.8%"></div></div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">ARKA (CEO) — Executive Leadership</span>
                <span class="text-blue-400 font-mono font-bold">4.92 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-blue-500 h-2 rounded-full" style="width: 98.4%"></div></div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">SEKAR (CFO) — Forensic Accounting</span>
                <span class="text-rose-400 font-mono font-bold">4.90 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-rose-500 h-2 rounded-full" style="width: 98.0%"></div></div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">FARREL (QA) — Automated Testing</span>
                <span class="text-violet-400 font-mono font-bold">4.72 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-violet-500 h-2 rounded-full" style="width: 94.4%"></div></div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">BIMA (CISO) — Cybersecurity & OWASP</span>
                <span class="text-red-400 font-mono font-bold">4.70 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-red-500 h-2 rounded-full" style="width: 94.0%"></div></div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">TARA (CDO) — Data Warehousing</span>
                <span class="text-teal-400 font-mono font-bold">4.68 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-teal-500 h-2 rounded-full" style="width: 93.6%"></div></div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">ADITYA (CPO) — Product & Design Systems</span>
                <span class="text-pink-400 font-mono font-bold">4.65 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-pink-500 h-2 rounded-full" style="width: 93.0%"></div></div>
            </div>
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-300">KIRANA (CMO) — Growth Marketing & SEO</span>
                <span class="text-yellow-400 font-mono font-bold">4.58 / 5.0</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2"><div class="bg-yellow-500 h-2 rounded-full" style="width: 91.6%"></div></div>
            </div>
          </div>
        </div>
      </div>
'''

# Replace old drawerTabEmployees with expanded_tabs_html
old_emp_tab_pattern = r'<div id="drawerTabEmployees".*?<!-- Tab 2: Task Ledger -->'
match = re.search(old_emp_tab_pattern, html, flags=re.DOTALL)
if match:
    html = html[:match.start()] + expanded_tabs_html + '\n      <!-- Tab 2: Task Ledger -->' + html[match.end():]
    print("Replaced and expanded drawerTabEmployees and inserted all 6 new tabs!")
else:
    print("Error: Could not find old drawerTabEmployees block to replace!")

# 4. Update switchDrawerTab JavaScript function to handle all 10 tabs
old_switch_fn = '''    function switchDrawerTab(tab) {
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
          if (t.name === tab) {
            btn.className = 'flex-1 py-3 text-center font-bold text-blue-400 border-b-2 border-blue-500';
          } else {
            btn.className = 'flex-1 py-3 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent';
          }
        }
      });
    }'''

new_switch_fn = '''    function switchDrawerTab(tab) {
      const allTabs = [
        { paneId: 'drawerTabReport', btnId: 'tabBtnReport', name: 'report' },
        { paneId: 'drawerTabEmployees', btnId: 'tabBtnEmployees', name: 'employees' },
        { paneId: 'drawerTabDirectory', btnId: 'tabBtnDirectory', name: 'directory' },
        { paneId: 'drawerTabOrg', btnId: 'tabBtnOrg', name: 'org' },
        { paneId: 'drawerTabDepartments', btnId: 'tabBtnDepartments', name: 'departments' },
        { paneId: 'drawerTabProjects', btnId: 'tabBtnProjects', name: 'projects' },
        { paneId: 'drawerTabWorkspace', btnId: 'tabBtnWorkspace', name: 'workspace' },
        { paneId: 'drawerTabAnalytics', btnId: 'tabBtnAnalytics', name: 'analytics' },
        { paneId: 'drawerTabTasks', btnId: 'tabBtnTasks', name: 'tasks' },
        { paneId: 'drawerTabDrive', btnId: 'tabBtnDrive', name: 'drive' }
      ];

      allTabs.forEach(t => {
        const pane = document.getElementById(t.paneId);
        if (pane) {
          pane.classList.toggle('hidden', t.name !== tab);
        }
        const btn = document.getElementById(t.btnId);
        if (btn) {
          if (t.name === tab) {
            btn.className = 'px-3 py-2 text-center font-bold text-blue-400 border-b-2 border-blue-500 flex items-center gap-1.5 shrink-0 transition bg-slate-900/50';
          } else {
            btn.className = 'px-3 py-2 text-center font-semibold text-slate-400 hover:text-white border-b-2 border-transparent flex items-center gap-1.5 shrink-0 transition';
          }
        }
      });
    }'''

if old_switch_fn in html:
    html = html.replace(old_switch_fn, new_switch_fn)
    print("Updated switchDrawerTab function to support all 10 tabs.")
else:
    print("Warning: old switchDrawerTab function not found directly, checking regex replacement.")
    html = re.sub(r'function switchDrawerTab\(tab\)\s*\{.*?tabs\.forEach.*?\}\s*\};?', new_switch_fn, html, flags=re.DOTALL)

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Updated {INDEX_PATH} successfully! Total size: {len(html)} bytes.")
