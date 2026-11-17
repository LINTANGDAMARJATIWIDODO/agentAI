"""
NEXUS AI ENTERPRISE — Upgrade 3D Virtual Office to 2-Level Multi-Story Corporate HQ
Expands the 3D visual workspace to:
1. Multi-Level 2-Story Architecture:
   - Ground Floor (Lantai 1): Spacious 48x34 layout with Grand Boardroom, Server Lab, Coffee Lounge, and 5 Engineering/Ops Workstations.
   - Mezzanine (Lantai 2): Elevated at y=4.2 with modern steel pillars, glass balustrade railing, floating oak staircase, and 5 Executive/Creative Workstations.
2. All 10 Professional AI Employees fully animated in 3D:
   - Lantai 2: ARKA (CEO), NAYA (BI), SEKAR (CFO), ADITYA (CPO), KIRANA (CMO)
   - Lantai 1: RAKA (CTO), TARA (CDO), BIMA (CISO), FARREL (QA), DIMAS (COO)
3. Camera presets for Floor 1, Floor 2, and 2-Story Overview.
"""

import os
import re
import subprocess

INDEX_PATH = r"C:\Users\LENOVO\.gemini\antigravity\scratch\NEXUS-AI-ENTERPRISE\public\index.html"

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Header Title & Status Badge
html = html.replace(
    'KANTOR VIRTUAL AKTIF (5 DIREKTUR)',
    'KANTOR VIRTUAL 2 TINGKAT AKTIF (10 KARYAWAN)'
)
html = html.replace(
    'Markas Besar Otonom AI Multi-Agent • Living 3D Corporate HQ',
    'Markas Besar Otonom AI Multi-Agent • Living 3D Corporate HQ (2 Lantai & 14 Fasilitas)'
)

# 2. Update Header Camera Buttons to include Floor 1 & Floor 2 Presets
old_cam_buttons = '''        <button onclick="resetCameraView()" class="px-2.5 py-1 rounded-lg bg-blue-600/30 text-blue-300 hover:bg-blue-600/50 hover:text-white transition font-medium" title="Sudut Pandang Utama Isometric">
          <i class="fa-solid fa-cube mr-1"></i>Overview
        </button>
        <button onclick="setCameraView('boardroom')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition" title="Ruang Rapat Direksi">
          <i class="fa-solid fa-users-rectangle"></i>
        </button>
        <button onclick="setCameraView('tech')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition" title="Lab Teknologi & Server">
          <i class="fa-solid fa-server"></i>
        </button>
        <button onclick="setCameraView('lounge')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition" title="Coffee Lounge & Pantry">
          <i class="fa-solid fa-mug-hot"></i>
        </button>'''

new_cam_buttons = '''        <button onclick="setCameraView('overview')" class="px-2.5 py-1 rounded-lg bg-blue-600/30 text-blue-300 hover:bg-blue-600/50 hover:text-white transition font-medium text-xs" title="Sudut Pandang Utama Isometric 2 Tingkat">
          <i class="fa-solid fa-layer-group mr-1"></i>Overview (2 Tingkat)
        </button>
        <button onclick="setCameraView('floor2')" class="px-2 py-1 rounded-lg bg-purple-600/20 text-purple-300 hover:bg-purple-600/40 hover:text-white transition font-medium text-xs" title="Lantai 2: Mezzanine Eksekutif & Desain">
          <i class="fa-solid fa-stairs mr-1"></i>Lantai 2 (Mezzanine)
        </button>
        <button onclick="setCameraView('floor1')" class="px-2 py-1 rounded-lg bg-emerald-600/20 text-emerald-300 hover:bg-emerald-600/40 hover:text-white transition font-medium text-xs" title="Lantai 1: Ground Floor, Boardroom & Lab">
          <i class="fa-solid fa-building mr-1"></i>Lantai 1 (Ground)
        </button>
        <button onclick="setCameraView('boardroom')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition" title="Ruang Rapat Direksi">
          <i class="fa-solid fa-users-rectangle"></i>
        </button>
        <button onclick="setCameraView('tech')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition" title="Lab Teknologi & Server">
          <i class="fa-solid fa-server"></i>
        </button>
        <button onclick="setCameraView('lounge')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition" title="Coffee Lounge & Pantry">
          <i class="fa-solid fa-mug-hot"></i>
        </button>'''

if old_cam_buttons in html:
    html = html.replace(old_cam_buttons, new_cam_buttons)
    print("Replaced Header Camera Buttons.")
else:
    print("Warning: old_cam_buttons not found directly, checking regex replacement.")
    html = re.sub(r'<button onclick="resetCameraView\(\)".*?title="Coffee Lounge & Pantry">\s*<i class="fa-solid fa-mug-hot"></i>\s*</button>', new_cam_buttons, html, flags=re.DOTALL)

# 3. Replace officeConfig & agentPositions in main script
old_config_pattern = r'const officeConfig = \{.*?let serverState = \{'

new_config_block = '''const officeConfig = {
      width: 48,
      depth: 34,
      wallHeight: 9.0,
      mezzanineHeight: 4.2
    };

    // 10 Professional AI Employee Workstations (Two-Level Multi-Story Layout)
    const agentPositions = {
      // --- LANTAI 2 (MEZZANINE DECK, Y = 4.2) ---
      arka: {
        x: -16.0, y: 4.2, z: -10.0,
        color: 0x1e40af, suitColor: 0x0f172a, hairColor: 0x1f2937, skinColor: 0x8d5524,
        rug: 0x1e3a8a, name: 'ARKA', avatar: '👔', title: 'Chief Executive & Strategic Director',
        floor: 'Lantai 2 (Mezzanine)', zone: 'Executive C-Suite Suite',
        walkTarget: { x: -4.0, y: 4.2, z: -6.0, label: 'Mezzanine Balcony Overlook' }
      },
      naya: {
        x: -8.0, y: 4.2, z: -10.0,
        color: 0x0d9488, suitColor: 0x064e3b, hairColor: 0x3f1e09, skinColor: 0xe0ac69,
        rug: 0x042f2e, name: 'NAYA', avatar: '🔬', title: 'Director of Research & Business Intelligence',
        floor: 'Lantai 2 (Mezzanine)', zone: 'Research & Open Data Pod',
        walkTarget: { x: -4.0, y: 4.2, z: -10.0, label: 'Data Science Wall' }
      },
      sekar: {
        x: -1.0, y: 4.2, z: -10.0,
        color: 0x7c3aed, suitColor: 0x3b0764, hairColor: 0x18181b, skinColor: 0xf1c27d,
        rug: 0x4c1d95, name: 'SEKAR', avatar: '⚖️', title: 'Chief Financial, Risk & Compliance Officer',
        floor: 'Lantai 2 (Mezzanine)', zone: 'Governance & Audit Deck',
        walkTarget: { x: -1.0, y: 4.2, z: -5.0, label: 'Statutory Compliance Board' }
      },
      aditya: {
        x: -16.0, y: 4.2, z: -2.0,
        color: 0xec4899, suitColor: 0x831843, hairColor: 0x27272a, skinColor: 0xc68642,
        rug: 0x9d174d, name: 'ADITYA', avatar: '🎨', title: 'Chief Product Officer',
        floor: 'Lantai 2 (Mezzanine)', zone: 'Product Design Studio',
        walkTarget: { x: -10.0, y: 4.2, z: -2.0, label: 'Figma Design Token Studio' }
      },
      kirana: {
        x: -8.0, y: 4.2, z: -2.0,
        color: 0xd97706, suitColor: 0x78350f, hairColor: 0x1c1917, skinColor: 0xf1c27d,
        rug: 0x92400e, name: 'KIRANA', avatar: '📢', title: 'Chief Marketing Officer',
        floor: 'Lantai 2 (Mezzanine)', zone: 'Marketing & Growth Studio',
        walkTarget: { x: -4.0, y: 4.2, z: -2.0, label: 'SEO & Acquisition Matrix' }
      },

      // --- LANTAI 1 (GROUND FLOOR, Y = 0.0) ---
      raka: {
        x: 10.0, y: 0.0, z: -6.0,
        color: 0x6366f1, suitColor: 0x312e81, hairColor: 0x111827, skinColor: 0xc68642,
        rug: 0x3730a3, name: 'RAKA', avatar: '⚡', title: 'Chief Technology & Engineering Officer',
        floor: 'Lantai 1 (Ground Floor)', zone: 'Tech & AI Cloud Lab',
        walkTarget: { x: 18.0, y: 0.0, z: -11.0, label: 'Server Racks Inspection' }
      },
      tara: {
        x: 10.0, y: 0.0, z: 4.5,
        color: 0x059669, suitColor: 0x064e3b, hairColor: 0x27272a, skinColor: 0xe0ac69,
        rug: 0x065f46, name: 'TARA', avatar: '🗄️', title: 'Chief Data Officer',
        floor: 'Lantai 1 (Ground Floor)', zone: 'Data Engineering Center',
        walkTarget: { x: 14.0, y: 0.0, z: 4.5, label: 'PostgreSQL Mart Cluster' }
      },
      bima: {
        x: 18.0, y: 0.0, z: -5.0,
        color: 0xdc2626, suitColor: 0x7f1d1d, hairColor: 0x09090b, skinColor: 0x8d5524,
        rug: 0x991b1b, name: 'BIMA', avatar: '🛡️', title: 'Chief Information Security Officer',
        floor: 'Lantai 1 (Ground Floor)', zone: 'Cybersecurity SOC Deck',
        walkTarget: { x: 18.0, y: 0.0, z: -9.0, label: 'Threat Hunting Console' }
      },
      farrel: {
        x: 18.0, y: 0.0, z: 6.0,
        color: 0x8b5cf6, suitColor: 0x4c1d95, hairColor: 0x18181b, skinColor: 0xf1c27d,
        rug: 0x5b21b6, name: 'FARREL', avatar: '🔬', title: 'Chief Quality Assurance Officer',
        floor: 'Lantai 1 (Ground Floor)', zone: 'Quality Assurance Lab',
        walkTarget: { x: 14.0, y: 0.0, z: 9.0, label: 'Playwright Test Matrix' }
      },
      dimas: {
        x: -16.0, y: 0.0, z: 10.0,
        color: 0xf59e0b, suitColor: 0x78350f, hairColor: 0x27272a, skinColor: 0x8d5524,
        rug: 0xb45309, name: 'DIMAS', avatar: '📈', title: 'Chief Operations & Growth Officer',
        floor: 'Lantai 1 (Ground Floor)', zone: 'Agile Operations Center',
        walkTarget: { x: 0.0, y: 0.0, z: -1.5, label: 'Boardroom Presentation' }
      }
    };

    let serverState = {'''

match_cfg = re.search(old_config_pattern, html, flags=re.DOTALL)
if match_cfg:
    html = html[:match_cfg.start()] + new_config_block + html[match_cfg.end():]
    print("Replaced officeConfig and added all 10 agentPositions.")
else:
    print("Error: Could not find old officeConfig block!")

# 4. Replace buildSpaciousOfficeArchitecture to build Mezzanine & Stairs
old_arch_pattern = r'function buildSpaciousOfficeArchitecture\(\) \{.*?\n    \}'

new_arch_function = '''function buildSpaciousOfficeArchitecture() {
      // Procedural Parquet Texture Generator
      const floorCanvas = document.createElement('canvas');
      floorCanvas.width = 1024;
      floorCanvas.height = 1024;
      const ctx = floorCanvas.getContext('2d');

      // Light Scandinavian Oak Plank Pattern
      ctx.fillStyle = '#e8decb';
      ctx.fillRect(0, 0, 1024, 1024);

      ctx.fillStyle = '#dfd4be';
      const plankW = 128;
      const plankH = 32;
      for (let y = 0; y < 1024; y += plankH) {
        const offset = (y / plankH) % 2 === 0 ? 0 : plankW / 2;
        for (let x = -offset; x < 1024; x += plankW) {
          ctx.strokeRect(x, y, plankW, plankH);
          ctx.strokeStyle = '#cfc1a5';
          ctx.lineWidth = 1.5;
          if ((x + y) % 3 === 0) {
            ctx.fillStyle = 'rgba(215, 201, 175, 0.35)';
            ctx.fillRect(x, y, plankW, plankH);
          }
        }
      }

      const floorTexture = new THREE.CanvasTexture(floorCanvas);
      floorTexture.wrapS = THREE.RepeatWrapping;
      floorTexture.wrapT = THREE.RepeatWrapping;
      floorTexture.repeat.set(8, 6);

      // --- LANTAI 1: Ground Floor (48x34) ---
      const floorGeo = new THREE.BoxGeometry(officeConfig.width, 0.5, officeConfig.depth);
      const floorMat = new THREE.MeshStandardMaterial({
        map: floorTexture,
        roughness: 0.45,
        metalness: 0.05
      });
      const floor = new THREE.Mesh(floorGeo, floorMat);
      floor.position.y = -0.25;
      floor.receiveShadow = true;
      scene.add(floor);

      // Baseboards on ground floor
      const skirtingMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.6 });
      const skirting1 = new THREE.Mesh(new THREE.BoxGeometry(officeConfig.width, 0.25, 0.1), skirtingMat);
      skirting1.position.set(0, 0.125, -officeConfig.depth / 2 + 0.05);
      scene.add(skirting1);

      const skirting2 = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.25, officeConfig.depth), skirtingMat);
      skirting2.position.set(-officeConfig.width / 2 + 0.05, 0.125, 0);
      scene.add(skirting2);

      // High Modern Architecture Half-Walls (Wall height = 9.0)
      const wallMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.85 });

      // Back Wall (North)
      const backWall = new THREE.Mesh(new THREE.BoxGeometry(officeConfig.width, officeConfig.wallHeight, 0.4), wallMat);
      backWall.position.set(0, officeConfig.wallHeight / 2, -officeConfig.depth / 2);
      backWall.receiveShadow = true;
      scene.add(backWall);

      // Left Wall (West)
      const leftWall = new THREE.Mesh(new THREE.BoxGeometry(0.4, officeConfig.wallHeight, officeConfig.depth), wallMat);
      leftWall.position.set(-officeConfig.width / 2, officeConfig.wallHeight / 2, 0);
      leftWall.receiveShadow = true;
      scene.add(leftWall);

      // --- LANTAI 2: MEZZANINE EXECUTIVE & CREATIVE DECK (Y = 4.2) ---
      const mezzWidth = 24.0;
      const mezzDepth = 17.0;
      const mezzGeo = new THREE.BoxGeometry(mezzWidth, 0.35, mezzDepth);
      const mezzFloorMat = new THREE.MeshStandardMaterial({
        map: floorTexture,
        roughness: 0.4,
        metalness: 0.05
      });
      const mezzanine = new THREE.Mesh(mezzGeo, mezzFloorMat);
      mezzanine.position.set(-officeConfig.width / 2 + mezzWidth / 2, officeConfig.mezzanineHeight - 0.175, -officeConfig.depth / 2 + mezzDepth / 2);
      mezzanine.receiveShadow = true;
      mezzanine.castShadow = true;
      scene.add(mezzanine);

      // 6 Modern Black Steel Support Columns for Lantai 2
      const colMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.85, roughness: 0.25 });
      const colPositions = [
        [-officeConfig.width / 2 + 1.0, -officeConfig.depth / 2 + 1.0],
        [-officeConfig.width / 2 + mezzWidth / 2, -officeConfig.depth / 2 + 1.0],
        [-officeConfig.width / 2 + mezzWidth - 0.5, -officeConfig.depth / 2 + 1.0],
        [-officeConfig.width / 2 + 1.0, -officeConfig.depth / 2 + mezzDepth - 0.5],
        [-officeConfig.width / 2 + mezzWidth / 2, -officeConfig.depth / 2 + mezzDepth - 0.5],
        [-officeConfig.width / 2 + mezzWidth - 0.5, -officeConfig.depth / 2 + mezzDepth - 0.5]
      ];

      colPositions.forEach(cp => {
        const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, officeConfig.mezzanineHeight, 16), colMat);
        pillar.position.set(cp[0], officeConfig.mezzanineHeight / 2, cp[1]);
        pillar.castShadow = true;
        scene.add(pillar);
      });

      // Glass Balustrade (Railing Kaca Tempered) along Lantai 2 open edges
      const glassMat = new THREE.MeshStandardMaterial({
        color: 0x93c5fd,
        transparent: true,
        opacity: 0.45,
        roughness: 0.1,
        metalness: 0.15
      });
      const handrailMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.15 });

      // Edge 1: Along East Edge of Mezzanine (facing central atrium)
      const railEast = new THREE.Mesh(new THREE.BoxGeometry(0.06, 1.1, mezzDepth), glassMat);
      railEast.position.set(-officeConfig.width / 2 + mezzWidth, officeConfig.mezzanineHeight + 0.55, -officeConfig.depth / 2 + mezzDepth / 2);
      scene.add(railEast);

      const capEast = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.08, mezzDepth), handrailMat);
      capEast.position.set(-officeConfig.width / 2 + mezzWidth, officeConfig.mezzanineHeight + 1.1, -officeConfig.depth / 2 + mezzDepth / 2);
      scene.add(capEast);

      // Edge 2: Along South Edge of Mezzanine (facing front)
      const railSouth = new THREE.Mesh(new THREE.BoxGeometry(mezzWidth - 4.0, 1.1, 0.06), glassMat);
      railSouth.position.set(-officeConfig.width / 2 + (mezzWidth - 4.0) / 2, officeConfig.mezzanineHeight + 0.55, -officeConfig.depth / 2 + mezzDepth);
      scene.add(railSouth);

      const capSouth = new THREE.Mesh(new THREE.BoxGeometry(mezzWidth - 4.0, 0.08, 0.12), handrailMat);
      capSouth.position.set(-officeConfig.width / 2 + (mezzWidth - 4.0) / 2, officeConfig.mezzanineHeight + 1.1, -officeConfig.depth / 2 + mezzDepth);
      scene.add(capSouth);

      // Modern Floating Oak Staircase connecting Lantai 1 and Lantai 2
      const stepCount = 14;
      const stairStartX = -officeConfig.width / 2 + mezzWidth - 1.5;
      const stairStartZ = -officeConfig.depth / 2 + mezzDepth + 6.0;
      const stairEndZ = -officeConfig.depth / 2 + mezzDepth;
      const stepMat = new THREE.MeshStandardMaterial({ color: 0xdfd4be, roughness: 0.4 });

      for (let s = 0; s < stepCount; s++) {
        const stepProgress = s / (stepCount - 1);
        const stepY = stepProgress * officeConfig.mezzanineHeight;
        const stepZ = stairStartZ - stepProgress * (stairStartZ - stairEndZ);

        const stepMesh = new THREE.Mesh(new THREE.BoxGeometry(3.0, 0.12, 0.65), stepMat);
        stepMesh.position.set(stairStartX, stepY, stepZ);
        stepMesh.castShadow = true;
        stepMesh.receiveShadow = true;
        scene.add(stepMesh);
      }

      // Warm LED strip under mezzanine edge
      const warmMezzLight = new THREE.PointLight(0xfef08a, 1.1, 24);
      warmMezzLight.position.set(-officeConfig.width / 2 + mezzWidth / 2, officeConfig.mezzanineHeight - 0.5, -officeConfig.depth / 2 + mezzDepth / 2);
      scene.add(warmMezzLight);
    }'''

match_arch = re.search(old_arch_pattern, html, flags=re.DOTALL)
if match_arch:
    html = html[:match_arch.start()] + new_arch_function + html[match_arch.end():]
    print("Replaced buildSpaciousOfficeArchitecture with 2-level mezzanine & floating staircase.")
else:
    print("Error: Could not find old buildSpaciousOfficeArchitecture function!")

# 5. Update buildAllExecutiveWorkstations to support y-elevation
old_workstation_iter = '''      Object.keys(agentPositions).forEach(key => {
        const info = agentPositions[key];
        const group = new THREE.Group();
        group.position.set(info.x, 0, info.z);'''

new_workstation_iter = '''      Object.keys(agentPositions).forEach(key => {
        const info = agentPositions[key];
        const group = new THREE.Group();
        const yPos = info.y || 0.0;
        group.position.set(info.x, yPos, info.z);'''

if old_workstation_iter in html:
    html = html.replace(old_workstation_iter, new_workstation_iter)
    print("Updated workstation group elevation to use info.y.")
else:
    print("Warning: old_workstation_iter not found directly, checking regex replacement.")
    html = re.sub(r'Object\.keys\(agentPositions\)\.forEach\(key\s*=>\s*\{\s*const info = agentPositions\[key\];\s*const group = new THREE\.Group\(\);\s*group\.position\.set\(info\.x,\s*0,\s*info\.z\);', new_workstation_iter, html)

# 6. Update officeAgents registration to use Vector3(info.x, info.y || 0, info.z)
old_office_agent_reg = '''          workstationPos: new THREE.Vector3(info.x, 0, info.z),'''
new_office_agent_reg = '''          workstationPos: new THREE.Vector3(info.x, info.y || 0.0, info.z),'''

if old_office_agent_reg in html:
    html = html.replace(old_office_agent_reg, new_office_agent_reg)
    print("Updated officeAgents workstationPos to support y elevation.")

# 7. Update setCameraView to support 2-Level views
old_camera_views = '''    function setCameraView(preset) {
      if (preset === 'iso') {
        gsapAnimateCamera(28, 30, 36, 0, 1.2, 0);
      } else if (preset === 'boardroom') {
        gsapAnimateCamera(0, 12, 14, 0, 1.5, -1.5);
      } else if (preset === 'tech') {
        gsapAnimateCamera(16, 12, 4, 12, 2.5, -7);
      } else if (preset === 'lounge') {
        gsapAnimateCamera(-12, 11, 19, -12, 1.5, 8);
      }
    }'''

new_camera_views = '''    function setCameraView(preset) {
      if (preset === 'iso' || preset === 'overview') {
        gsapAnimateCamera(36, 38, 44, 0, 2.5, 0);
      } else if (preset === 'floor2') {
        gsapAnimateCamera(-4, 18, 12, -10, 5.0, -6);
      } else if (preset === 'floor1') {
        gsapAnimateCamera(24, 20, 28, 6, 1.2, 2);
      } else if (preset === 'boardroom') {
        gsapAnimateCamera(0, 12, 14, 0, 1.5, -1.5);
      } else if (preset === 'tech') {
        gsapAnimateCamera(22, 12, 4, 14, 2.0, -4);
      } else if (preset === 'lounge') {
        gsapAnimateCamera(-14, 11, 22, -14, 1.5, 8);
      }
    }'''

if old_camera_views in html:
    html = html.replace(old_camera_views, new_camera_views)
    print("Updated setCameraView for 2-Level multi-story presets.")
else:
    print("Warning: old_camera_views not found directly, checking regex replacement.")
    html = re.sub(r'function setCameraView\(preset\)\s*\{.*?\}\s*function resetCameraView', new_camera_views + '\n\n    function resetCameraView', html, flags=re.DOTALL)

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html with 2-Level Multi-Story Corporate HQ and 10 Employees!")
