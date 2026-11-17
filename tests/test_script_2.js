
    let scene, camera, renderer, controls;
    let officeAgents = {}; // Stores agent 3D objects, rigs, and state machines
    let dynamicTextures = {}; // Monitors, LED matrices, charts
    let animatedObjects = []; // Steam particles, blinking lights, clock
    let clock = new THREE.Clock();

    // Expanded Multi-Zone Office Layout (36 x 26 space)
    const officeConfig = {
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

    let serverState = {
      agents: [],
      tasks: [],
      agent_bubbles: {}
    };

    // Initialize 3D Scene
    function init3DOffice() {
      const container = document.getElementById('canvas-container');
      const width = container.clientWidth;
      const height = container.clientHeight;

      // 1. Scene setup
      scene = new THREE.Scene();
      scene.background = new THREE.Color(0x0a0f1d);
      scene.fog = new THREE.FogExp2(0x0a0f1d, 0.018);

      // 2. Camera: True Isometric Angle
      const aspect = width / height;
      camera = new THREE.PerspectiveCamera(38, aspect, 0.1, 1000);
      camera.position.set(28, 30, 36);

      // 3. Renderer with High-End Soft Shadows
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.05;
      container.appendChild(renderer.domElement);

      // 4. Orbit Controls
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.target.set(0, 1.2, 0);
      controls.maxPolarAngle = Math.PI / 2.15; // Prevent camera from going beneath floor
      controls.minDistance = 12;
      controls.maxDistance = 65;

      // 5. Studio Lighting Setup
      setupOfficeLighting();

      // 6. Build Expanded Architectural Floor & Zones
      buildSpaciousOfficeArchitecture();

      // 7. Build High-End Furniture & Equipment
      buildBoardroomCenter();
      buildCoffeeLoungeAndPantry();
      buildTechServerZone();

      // 8. Build 5 Executive Workstations & Living Animated Character Rigs
      buildAllExecutiveWorkstations();

      // 9. Interactive Raycasting
      setupRaycastSelection();

      // 10. Resize Listener
      window.addEventListener('resize', onWindowResize);

      // 11. Run Animation Loop
      animate();
    }

    function setupOfficeLighting() {
      // Ambient Fill
      const ambientLight = new THREE.AmbientLight(0xfff7ed, 0.65);
      scene.add(ambientLight);

      // Main Isometric Sunlight
      const sunLight = new THREE.DirectionalLight(0xfffaed, 0.95);
      sunLight.position.set(24, 38, 20);
      sunLight.castShadow = true;
      sunLight.shadow.mapSize.width = 2048;
      sunLight.shadow.mapSize.height = 2048;
      sunLight.shadow.camera.near = 1;
      sunLight.shadow.camera.far = 90;
      sunLight.shadow.camera.left = -25;
      sunLight.shadow.camera.right = 25;
      sunLight.shadow.camera.top = 25;
      sunLight.shadow.camera.bottom = -25;
      sunLight.shadow.bias = -0.0004;
      scene.add(sunLight);

      // Blue / Cyan Accent Fill from Tech Side
      const techGlow = new THREE.PointLight(0x38bdf8, 1.2, 28);
      techGlow.position.set(12, 6, -6);
      scene.add(techGlow);

      // Warm Amber Light over Coffee Lounge
      const loungeGlow = new THREE.PointLight(0xf59e0b, 1.0, 20);
      loungeGlow.position.set(-13, 5, 8);
      scene.add(loungeGlow);

      // Boardroom Downlight
      const boardroomSpot = new THREE.SpotLight(0xffffff, 0.8, 24, Math.PI / 4, 0.4);
      boardroomSpot.position.set(0, 9, -1);
      boardroomSpot.target.position.set(0, 0, -1);
      scene.add(boardroomSpot);
      scene.add(boardroomSpot.target);
    }

    // 6. Expanded Architecture: 36x26 Space with Multi-Zones & Parquet Wood Flooring
    function buildSpaciousOfficeArchitecture() {
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
    }

    function createGlassPartition(x, z, length, height, isHorizontal) {
      const group = new THREE.Group();
      group.position.set(x, height / 2, z);

      // Aluminum Pillars / Frame
      const frameMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.8, roughness: 0.3 });
      const w = isHorizontal ? length : 0.12;
      const d = isHorizontal ? 0.12 : length;

      // Base & Top Bar
      const baseBar = new THREE.Mesh(new THREE.BoxGeometry(w, 0.1, d), frameMat);
      baseBar.position.y = -height / 2 + 0.05;
      group.add(baseBar);

      const topBar = new THREE.Mesh(new THREE.BoxGeometry(w, 0.1, d), frameMat);
      topBar.position.y = height / 2 - 0.05;
      group.add(topBar);

      // Translucent Tinted Glass Pane
      const glassMat = new THREE.MeshPhysicalMaterial({
        color: 0x93c5fd,
        transparent: true,
        opacity: 0.35,
        roughness: 0.1,
        transmission: 0.7,
        thickness: 0.2
      });
      const glass = new THREE.Mesh(new THREE.BoxGeometry(isHorizontal ? length - 0.2 : 0.04, height - 0.3, isHorizontal ? 0.04 : length - 0.2), glassMat);
      group.add(glass);

      scene.add(group);
    }

    function createWallBanner(x, y, z, w, h, text) {
      const canvas = document.createElement('canvas');
      canvas.width = 1024;
      canvas.height = 128;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, 1024, 128);

      // Gradient border
      const grad = ctx.createLinearGradient(0, 0, 1024, 0);
      grad.addColorStop(0, '#3b82f6');
      grad.addColorStop(0.5, '#8b5cf6');
      grad.addColorStop(1, '#10b981');
      ctx.strokeStyle = grad;
      ctx.lineWidth = 6;
      ctx.strokeRect(4, 4, 1016, 120);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 36px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(text, 512, 64);

      const texture = new THREE.CanvasTexture(canvas);
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: texture }));
      mesh.position.set(x, y, z);
      scene.add(mesh);
    }

    // 7. High-End Central Executive Boardroom / Conference Center
    function buildBoardroomCenter() {
      const group = new THREE.Group();
      group.position.set(0, 0, -1.5);

      // Boardroom Plush Navy Rug
      const rug = new THREE.Mesh(
        new THREE.BoxGeometry(10.5, 0.03, 6.5),
        new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 })
      );
      rug.position.y = 0.015;
      rug.receiveShadow = true;
      group.add(rug);

      // Grand Mahogany Conference Table
      const tableTop = new THREE.Mesh(
        new THREE.CylinderGeometry(4.2, 4.2, 0.14, 32, 1, false),
        new THREE.MeshStandardMaterial({ color: 0x3f2314, roughness: 0.35, metalness: 0.1 })
      );
      tableTop.scale.set(1.1, 1, 0.65); // Oval conference shape
      tableTop.position.set(0, 1.15, 0);
      tableTop.castShadow = true;
      tableTop.receiveShadow = true;
      group.add(tableTop);

      // Chrome Heavy Pedestal Bases
      const baseMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.9, roughness: 0.2 });
      [-2.2, 2.2].forEach(px => {
        const base = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.7, 1.1, 16), baseMat);
        base.position.set(px, 0.55, 0);
        base.castShadow = true;
        group.add(base);
      });

      // Video Conference Puck in Center (With glowing green ring)
      const confPhone = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.05, 16), new THREE.MeshStandardMaterial({ color: 0x0f172a }));
      confPhone.position.set(0, 1.24, 0);
      group.add(confPhone);

      const confLed = new THREE.Mesh(new THREE.RingGeometry(0.18, 0.22, 16), new THREE.MeshBasicMaterial({ color: 0x22c55e, side: THREE.DoubleSide }));
      confLed.rotation.x = -Math.PI / 2;
      confLed.position.set(0, 1.27, 0);
      group.add(confLed);

      // 6 Boardroom Swivel Chairs
      const chairPositions = [
        { x: -2.8, z: -1.6, rot: 0.4 },
        { x: 0,    z: -1.8, rot: 0 },
        { x: 2.8,  z: -1.6, rot: -0.4 },
        { x: -2.8, z: 1.6,  rot: Math.PI - 0.4 },
        { x: 0,    z: 1.8,  rot: Math.PI },
        { x: 2.8,  z: 1.6,  rot: Math.PI + 0.4 }
      ];
      chairPositions.forEach(cp => {
        const chair = createErgonomicChairMesh(0x0f172a);
        chair.position.set(cp.x, 0, cp.z);
        chair.rotation.y = cp.rot;
        group.add(chair);
      });

      // 75-inch Boardroom Presentation Smartboard on Wall
      const screenCanvas = document.createElement('canvas');
      screenCanvas.width = 1024;
      screenCanvas.height = 512;
      const sCtx = screenCanvas.getContext('2d');
      sCtx.fillStyle = '#090d16';
      sCtx.fillRect(0, 0, 1024, 512);

      // Smartboard Header
      sCtx.fillStyle = '#3b82f6';
      sCtx.font = 'bold 34px sans-serif';
      sCtx.fillText('SPBE DKI JAKARTA — PEMETAAN ARSITEKTUR BISNIS & LAYANAN', 40, 60);

      sCtx.fillStyle = '#94a3b8';
      sCtx.font = '22px sans-serif';
      sCtx.fillText('Status Evaluasi: 53 Perangkat Daerah • 48 Dokumen Memerlukan Remediasi', 40, 105);

      // Visual Progress Bars
      sCtx.fillStyle = '#1e293b';
      sCtx.fillRect(40, 140, 944, 40);
      sCtx.fillStyle = '#22c55e';
      sCtx.fillRect(40, 140, 944 * (5 / 53), 40); // 5 complete

      sCtx.fillStyle = '#ffffff';
      sCtx.font = 'bold 18px sans-serif';
      sCtx.fillText('Lengkap 100% (5 OPD)', 55, 166);

      sCtx.fillStyle = '#e2e8f0';
      sCtx.font = '20px sans-serif';
      sCtx.fillText('⚠️ CRITICAL: 03C_TOBE_ASIS Jakarta Selatan - Template Kosong Belum Terisi', 40, 230);
      sCtx.fillText('• 39 Baris ProsesBisnis_Upgrade & 21 Baris Layanan_Upgrade perlu auto-generate', 40, 270);
      sCtx.fillText('• 11 OPD BAST belum masuk (Seribu, DPMPTSP, BPAD, Biro-biro)', 40, 310);
      sCtx.fillText('• Berita Acara BPKD menunggu TTD Kabid; 5 OPD menunggu TTD Eselon 3', 40, 350);

      // Active Agent Working Indicator
      sCtx.fillStyle = '#38bdf8';
      sCtx.fillText('STATUS: Multi-Agent Auto-Remediation Active (ARKA, NAYA, RAKA, SEKAR, DIMAS)', 40, 430);

      const boardTexture = new THREE.CanvasTexture(screenCanvas);
      dynamicTextures.smartboard = { canvas: screenCanvas, ctx: sCtx, texture: boardTexture };

      const smartboardMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(8.5, 4.2),
        new THREE.MeshBasicMaterial({ map: boardTexture })
      );
      smartboardMesh.position.set(0, 2.7, -officeConfig.depth / 2 + 0.22);
      scene.add(smartboardMesh);

      // Smartboard Frame
      const boardFrame = new THREE.Mesh(
        new THREE.BoxGeometry(8.7, 4.4, 0.08),
        new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.3, metalness: 0.8 })
      );
      boardFrame.position.set(0, 2.7, -officeConfig.depth / 2 + 0.18);
      scene.add(boardFrame);

      scene.add(group);
    }

    // 8. Executive Coffee Lounge & Pantry
    function buildCoffeeLoungeAndPantry() {
      const group = new THREE.Group();
      group.position.set(-13, 0, 8);

      // Cozy Wood Tile Mat
      const mat = new THREE.Mesh(
        new THREE.BoxGeometry(6.5, 0.02, 5.5),
        new THREE.MeshStandardMaterial({ color: 0xc2410c, roughness: 0.85 })
      );
      mat.position.y = 0.01;
      mat.receiveShadow = true;
      group.add(mat);

      // Modern Lounge Sofa Couch
      const sofaMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 });
      const sofaBase = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.45, 1.4), sofaMat);
      sofaBase.position.set(0, 0.35, -1.2);
      sofaBase.castShadow = true;
      group.add(sofaBase);

      const sofaBack = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.8, 0.4), sofaMat);
      sofaBack.position.set(0, 0.85, -1.7);
      sofaBack.castShadow = true;
      group.add(sofaBack);

      // Cushions
      const cushionMat = new THREE.MeshStandardMaterial({ color: 0x3b82f6 });
      [-1.0, 0, 1.0].forEach(cx => {
        const c = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.12, 0.9), cushionMat);
        c.position.set(cx, 0.6, -1.2);
        group.add(c);
      });

      // Coffee Table (Marble top)
      const coffeeTable = new THREE.Mesh(
        new THREE.BoxGeometry(2.2, 0.1, 1.1),
        new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.2, metalness: 0.1 })
      );
      coffeeTable.position.set(0, 0.5, 0.2);
      coffeeTable.castShadow = true;
      group.add(coffeeTable);

      // Table Legs
      const tLegMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.8 });
      [[-0.9, -0.4], [0.9, -0.4], [-0.9, 0.4], [0.9, 0.4]].forEach(lp => {
        const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.5, 8), tLegMat);
        leg.position.set(lp[0], 0.25, lp[1] + 0.2);
        group.add(leg);
      });

      // Pantry Counter / Coffee Bar Unit
      const counter = new THREE.Mesh(
        new THREE.BoxGeometry(1.4, 1.1, 3.2),
        new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.5 })
      );
      counter.position.set(2.8, 0.55, -0.5);
      counter.castShadow = true;
      counter.receiveShadow = true;
      group.add(counter);

      // Espresso Coffee Machine
      const coffeeMachine = new THREE.Mesh(
        new THREE.BoxGeometry(0.65, 0.55, 0.65),
        new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.7, roughness: 0.3 })
      );
      coffeeMachine.position.set(2.8, 1.38, -1.2);
      coffeeMachine.castShadow = true;
      group.add(coffeeMachine);

      // Coffee Mug on Counter with Steam Effect
      const pantryMug = new THREE.Mesh(
        new THREE.CylinderGeometry(0.08, 0.08, 0.16, 12),
        new THREE.MeshStandardMaterial({ color: 0xffffff })
      );
      pantryMug.position.set(2.8, 1.18, -0.5);
      group.add(pantryMug);

      // Water Dispenser with inverted blue gallon bottle
      const dispenserBody = new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.1, 0.6), new THREE.MeshStandardMaterial({ color: 0xf1f5f9 }));
      dispenserBody.position.set(2.8, 0.55, 1.3);
      dispenserBody.castShadow = true;
      group.add(dispenserBody);

      const waterBottle = new THREE.Mesh(
        new THREE.CylinderGeometry(0.24, 0.24, 0.7, 16),
        new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.7, roughness: 0.1 })
      );
      waterBottle.position.set(2.8, 1.45, 1.3);
      waterBottle.castShadow = true;
      group.add(waterBottle);

      // Animated Coffee Steam Particles
      const steamGroup = new THREE.Group();
      steamGroup.position.set(2.8, 1.3, -0.5);
      const steamParticles = [];
      const steamMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.4 });
      for (let i = 0; i < 5; i++) {
        const p = new THREE.Mesh(new THREE.SphereGeometry(0.03 + i * 0.015, 8, 8), steamMat);
        p.position.set((Math.random() - 0.5) * 0.05, i * 0.08, (Math.random() - 0.5) * 0.05);
        p.userData = { baseY: p.position.y, speed: 0.5 + Math.random() * 0.5, seed: i };
        steamGroup.add(p);
        steamParticles.push(p);
      }
      group.add(steamGroup);
      animatedObjects.push({ type: 'steam', particles: steamParticles });

      scene.add(group);
    }

    // 9. Tech & AI Server Zone (Blinking LED Racks for RAKA)
    function buildTechServerZone() {
      const group = new THREE.Group();
      group.position.set(14.5, 0, -9.5);

      // Server Racks (Dual 42U Data Center Cabinets)
      [-1.1, 1.1].forEach(px => {
        const rackBody = new THREE.Mesh(
          new THREE.BoxGeometry(1.6, 3.4, 1.2),
          new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.4, metalness: 0.8 })
        );
        rackBody.position.set(px, 1.7, 0);
        rackBody.castShadow = true;
        group.add(rackBody);

        // Blinking LED Array (Procedural Canvas)
        const ledCanvas = document.createElement('canvas');
        ledCanvas.width = 128;
        ledCanvas.height = 256;
        const ledCtx = ledCanvas.getContext('2d');
        const ledTexture = new THREE.CanvasTexture(ledCanvas);

        const ledScreen = new THREE.Mesh(
          new THREE.PlaneGeometry(1.4, 3.1),
          new THREE.MeshBasicMaterial({ map: ledTexture })
        );
        ledScreen.position.set(px, 1.7, 0.61);
        group.add(ledScreen);

        animatedObjects.push({
          type: 'server_leds',
          canvas: ledCanvas,
          ctx: ledCtx,
          texture: ledTexture,
          offset: px
        });
      });

      // Agile Sprint Kanban Whiteboard on Wall (for DIMAS & RAKA)
      const kanbanMesh = createKanbanBoardMesh(4.5, 2.6);
      kanbanMesh.position.set(-2.5, 2.4, -officeConfig.depth / 2 + 0.22);
      scene.add(kanbanMesh);

      scene.add(group);
    }

    function createKanbanBoardMesh(w, h) {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 300;
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = '#f8fafc';
      ctx.fillRect(0, 0, 512, 300);

      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 20px sans-serif';
      ctx.fillText('AGILE SPRINT BOARD — NEXUS 90-DAY MVP', 20, 32);

      // Columns: Backlog, In Progress, Review, Done
      const cols = ['BACKLOG', 'IN PROGRESS', 'AUDIT / QC', 'DONE'];
      cols.forEach((col, idx) => {
        const x = 20 + idx * 120;
        ctx.fillStyle = '#e2e8f0';
        ctx.fillRect(x, 48, 110, 240);

        ctx.fillStyle = '#475569';
        ctx.font = 'bold 12px sans-serif';
        ctx.fillText(col, x + 10, 68);

        // Sticky notes
        const noteColors = ['#fde047', '#67e8f9', '#f472b6', '#86efac'];
        for (let j = 0; j < 3; j++) {
          ctx.fillStyle = noteColors[(idx + j) % 4];
          ctx.fillRect(x + 10, 85 + j * 48, 90, 38);
          ctx.fillStyle = '#1e293b';
          ctx.font = '9px sans-serif';
          ctx.fillText(`TASK #${(idx+1)*10+j}`, x + 16, 102 + j * 48);
        }
      });

      const texture = new THREE.CanvasTexture(canvas);
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: texture }));
      mesh.castShadow = true;
      return mesh;
    }

    // 10. Build All 5 Workstations & Full Living Character Rigs
    function buildAllExecutiveWorkstations() {
      Object.keys(agentPositions).forEach(key => {
        const info = agentPositions[key];
        const group = new THREE.Group();
        const yPos = info.y || 0.0;
        group.position.set(info.x, yPos, info.z);

        // 1. Designer Rug under desk
        const rugGeo = new THREE.BoxGeometry(4.6, 0.03, 4.2);
        const rugMat = new THREE.MeshStandardMaterial({ color: info.rug, roughness: 0.9 });
        const rug = new THREE.Mesh(rugGeo, rugMat);
        rug.position.y = 0.015;
        rug.receiveShadow = true;
        group.add(rug);

        // 2. Modern Executive Desk (Beveled wood top + sleek steel frame)
        const deskTop = new THREE.Mesh(
          new THREE.BoxGeometry(3.0, 0.12, 1.6),
          new THREE.MeshStandardMaterial({ color: 0xfba875, roughness: 0.5, metalness: 0.05 }) // Warm Scandinavian peach wood
        );
        deskTop.position.set(0, 1.18, 0.4);
        deskTop.castShadow = true;
        deskTop.receiveShadow = true;
        group.add(deskTop);

        // Modern Hairpin / Sled Steel Desk Legs
        const legMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.8, roughness: 0.2 });
        [[-1.38, 0.4], [1.38, 0.4]].forEach(lp => {
          const sledLeg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.18, 1.4), legMat);
          sledLeg.position.set(lp[0], 0.59, lp[1]);
          sledLeg.castShadow = true;
          group.add(sledLeg);
        });

        // 3. Dual High-End Ultra-Thin Monitors with Articulated Gas Arms
        const monitorGroup = buildDualMonitorSetup(key);
        monitorGroup.position.set(0, 1.24, 0.85);
        group.add(monitorGroup);

        // 4. Backlit Mechanical Keyboard & Vertical Ergonomic Mouse
        const keyboard = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.03, 0.26), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.4 }));
        keyboard.position.set(0, 1.25, 0.35);
        group.add(keyboard);

        const mouse = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.05, 0.18), new THREE.MeshStandardMaterial({ color: 0x334155 }));
        mouse.position.set(0.65, 1.26, 0.35);
        group.add(mouse);

        // Oversized Desk Mat (Black felt)
        const deskMat = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.015, 0.75), new THREE.MeshStandardMaterial({ color: 0x090d16 }));
        deskMat.position.set(0, 1.245, 0.38);
        group.add(deskMat);

        // Ceramic Coffee Mug
        const mug = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.16, 12), new THREE.MeshStandardMaterial({ color: info.color }));
        mug.position.set(0.95, 1.32, 0.5);
        group.add(mug);

        // Workstation PC Tower under desk (RGB glowing)
        const tower = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.8, 0.7), new THREE.MeshStandardMaterial({ color: 0x090d16 }));
        tower.position.set(1.15, 0.4, 0.4);
        tower.castShadow = true;
        group.add(tower);

        // 5. Herman Miller Aeron Style Ergonomic Office Chair
        const chair = createErgonomicChairMesh(0x0f172a);
        chair.position.set(0, 0, -0.45);
        group.add(chair);

        // 6. Complete Living Animated Humanoid Character Rig
        const characterRig = buildLivingCharacterRig(info);
        characterRig.group.position.set(0, 0, -0.45);
        group.add(characterRig.group);

        // Plant near desk
        const plant = createPottedOfficePlant(1.6, -0.8);
        group.add(plant);

        // Click hit-box & Raycast reference
        group.userData = { agentId: key, agentInfo: info };
        scene.add(group);

        officeAgents[key] = {
          id: key,
          info: info,
          group: group,
          chair: chair,
          rig: characterRig,
          workstationPos: new THREE.Vector3(info.x, info.y || 0.0, info.z),
          state: 'WORKING', // WORKING, THINKING, WALKING, AT_TARGET, WALKING_BACK
          walkProgress: 0,
          walkStartTime: 0,
          currentBubble: ''
        };
      });
    }

    // Dual Curved / Angled Monitor Setup with Animated Screen Display
    function buildDualMonitorSetup(agentId) {
      const group = new THREE.Group();

      // Monitor Stand Base & Gas Arm
      const standMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.85, roughness: 0.2 });
      const base = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.04, 16), standMat);
      base.position.set(0, 0.02, 0);
      group.add(base);

      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.55, 12), standMat);
      pole.position.set(0, 0.28, 0);
      group.add(pole);

      // Screen Canvas: Generates live scrolling code / graphs
      const screenCanvas = document.createElement('canvas');
      screenCanvas.width = 512;
      screenCanvas.height = 256;
      const sCtx = screenCanvas.getContext('2d');
      const screenTexture = new THREE.CanvasTexture(screenCanvas);

      dynamicTextures[`screen_${agentId}`] = {
        canvas: screenCanvas,
        ctx: sCtx,
        texture: screenTexture,
        agentId: agentId
      };

      // Left Monitor
      const leftScreen = new THREE.Mesh(
        new THREE.PlaneGeometry(1.2, 0.68),
        new THREE.MeshBasicMaterial({ map: screenTexture })
      );
      leftScreen.position.set(-0.62, 0.52, 0);
      leftScreen.rotation.y = Math.PI - 0.22; // Angled inward
      group.add(leftScreen);

      const leftBezel = new THREE.Mesh(
        new THREE.BoxGeometry(1.24, 0.72, 0.04),
        new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.3 })
      );
      leftBezel.position.set(-0.62, 0.52, 0.02);
      leftBezel.rotation.y = Math.PI - 0.22;
      group.add(leftBezel);

      // Right Monitor
      const rightScreen = new THREE.Mesh(
        new THREE.PlaneGeometry(1.2, 0.68),
        new THREE.MeshBasicMaterial({ map: screenTexture })
      );
      rightScreen.position.set(0.62, 0.52, 0);
      rightScreen.rotation.y = Math.PI + 0.22; // Angled inward
      group.add(rightScreen);

      const rightBezel = new THREE.Mesh(
        new THREE.BoxGeometry(1.24, 0.72, 0.04),
        new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.3 })
      );
      rightBezel.position.set(0.62, 0.52, 0.02);
      rightBezel.rotation.y = Math.PI + 0.22;
      group.add(rightBezel);

      return group;
    }

    // Ergonomic Swivel Chair Mesh
    function createErgonomicChairMesh(colorHex) {
      const chairGroup = new THREE.Group();

      const mat = new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.6 });
      const chromeMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.85, roughness: 0.2 });

      // 5-Star Caster Base
      for (let i = 0; i < 5; i++) {
        const angle = (i * Math.PI * 2) / 5;
        const spoke = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.04, 0.42), chromeMat);
        spoke.position.set(Math.sin(angle) * 0.21, 0.05, Math.cos(angle) * 0.21);
        spoke.rotation.y = angle;
        chairGroup.add(spoke);
      }

      // Stem
      const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.55, 8), chromeMat);
      stem.position.set(0, 0.32, 0);
      chairGroup.add(stem);

      // Contoured Seat
      const seat = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.08, 0.82), mat);
      seat.position.set(0, 0.65, 0);
      seat.castShadow = true;
      chairGroup.add(seat);

      // Mesh High Backrest
      const back = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.95, 0.08), mat);
      back.position.set(0, 1.15, -0.38);
      back.rotation.x = -0.1;
      back.castShadow = true;
      chairGroup.add(back);

      // Armrests
      [-0.45, 0.45].forEach(ax => {
        const arm = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.32, 0.35), mat);
        arm.position.set(ax, 0.82, -0.05);
        chairGroup.add(arm);
      });

      return chairGroup;
    }

    // Detailed Low-Poly Humanoid Rig with Articulated Limbs
    function buildLivingCharacterRig(info) {
      const root = new THREE.Group();

      const suitMat = new THREE.MeshStandardMaterial({ color: info.suitColor, roughness: 0.7 });
      const shirtMat = new THREE.MeshStandardMaterial({ color: info.color, roughness: 0.6 });
      const skinMat = new THREE.MeshStandardMaterial({ color: info.skinColor, roughness: 0.8 });
      const hairMat = new THREE.MeshStandardMaterial({ color: info.hairColor, roughness: 0.9 });
      const shoeMat = new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.4 });

      // Pelvis / Hips
      const hips = new THREE.Group();
      hips.position.y = 0.65;
      root.add(hips);

      // Torso / Suit Jacket
      const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.44, 0.75, 12), suitMat);
      torso.position.y = 0.42;
      torso.castShadow = true;
      hips.add(torso);

      // Inner Tie / Shirt detail
      const shirt = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.5, 0.1), shirtMat);
      shirt.position.set(0, 0.48, 0.22);
      hips.add(shirt);

      // Head & Neck
      const headGroup = new THREE.Group();
      headGroup.position.set(0, 0.95, 0);
      hips.add(headGroup);

      const head = new THREE.Mesh(new THREE.SphereGeometry(0.32, 16, 16), skinMat);
      head.position.y = 0.15;
      head.castShadow = true;
      headGroup.add(head);

      // Hair
      const hair = new THREE.Mesh(new THREE.SphereGeometry(0.33, 16, 16, 0, Math.PI * 2, 0, Math.PI / 1.7), hairMat);
      hair.position.y = 0.2;
      hair.rotation.x = -0.15;
      headGroup.add(hair);

      // Arms (Shoulder pivots)
      const leftShoulder = new THREE.Group();
      leftShoulder.position.set(-0.48, 0.72, 0.05);
      hips.add(leftShoulder);

      const leftArm = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.55, 0.14), suitMat);
      leftArm.position.y = -0.25;
      leftArm.castShadow = true;
      leftShoulder.add(leftArm);

      const leftHand = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), skinMat);
      leftHand.position.y = -0.55;
      leftShoulder.add(leftHand);

      const rightShoulder = new THREE.Group();
      rightShoulder.position.set(0.48, 0.72, 0.05);
      hips.add(rightShoulder);

      const rightArm = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.55, 0.14), suitMat);
      rightArm.position.y = -0.25;
      rightArm.castShadow = true;
      rightShoulder.add(rightArm);

      const rightHand = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), skinMat);
      rightHand.position.y = -0.55;
      rightShoulder.add(rightHand);

      // Legs (For standing and walking)
      const leftLegGroup = new THREE.Group();
      leftLegGroup.position.set(-0.2, 0, 0);
      hips.add(leftLegGroup);

      const leftLeg = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.65, 0.16), suitMat);
      leftLeg.position.y = -0.32;
      leftLeg.castShadow = true;
      leftLegGroup.add(leftLeg);

      const leftShoe = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.1, 0.28), shoeMat);
      leftShoe.position.set(0, -0.65, 0.06);
      leftLegGroup.add(leftShoe);

      const rightLegGroup = new THREE.Group();
      rightLegGroup.position.set(0.2, 0, 0);
      hips.add(rightLegGroup);

      const rightLeg = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.65, 0.16), suitMat);
      rightLeg.position.y = -0.32;
      rightLeg.castShadow = true;
      rightLegGroup.add(rightLeg);

      const rightShoe = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.1, 0.28), shoeMat);
      rightShoe.position.set(0, -0.65, 0.06);
      rightLegGroup.add(rightShoe);

      return {
        group: root,
        hips: hips,
        headGroup: headGroup,
        leftShoulder: leftShoulder,
        rightShoulder: rightShoulder,
        leftLegGroup: leftLegGroup,
        rightLegGroup: rightLegGroup
      };
    }

    function createPottedOfficePlant(x, z) {
      const pGroup = new THREE.Group();
      pGroup.position.set(x, 0, z);

      // Modern White Ceramic Hex Pot
      const pot = new THREE.Mesh(
        new THREE.CylinderGeometry(0.32, 0.24, 0.6, 8),
        new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 })
      );
      pot.position.y = 0.3;
      pot.castShadow = true;
      pGroup.add(pot);

      // Soil
      const soil = new THREE.Mesh(new THREE.CylinderGeometry(0.29, 0.29, 0.05, 8), new THREE.MeshStandardMaterial({ color: 0x3f2314 }));
      soil.position.y = 0.58;
      pGroup.add(soil);

      // Broad Ficus / Monstera Green Leaves
      const leafMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.6, side: THREE.DoubleSide });
      for (let i = 0; i < 6; i++) {
        const ang = (i * Math.PI * 2) / 6;
        const leaf = new THREE.Mesh(new THREE.SphereGeometry(0.35, 8, 8), leafMat);
        leaf.scale.set(0.4, 1.2, 0.1);
        leaf.position.set(Math.sin(ang) * 0.2, 0.9 + (i % 2) * 0.2, Math.cos(ang) * 0.2);
        leaf.rotation.set(0.4 * Math.cos(ang), ang, 0.4 * Math.sin(ang));
        leaf.castShadow = true;
        pGroup.add(leaf);
      }

      return pGroup;
    }

    // 11. Living Animation Loop: Natural Humanoid Movements & Autonomy
    function animate() {
      requestAnimationFrame(animate);
      const time = clock.getElapsedTime();

      // A. Update Living Animated Agent Rigs
      Object.keys(officeAgents).forEach((key, idx) => {
        const ag = officeAgents[key];
        if (!ag || !ag.rig) return;

        const rig = ag.rig;
        const seed = idx * 1.7;

        if (ag.state === 'WORKING') {
          // Sitting at desk: typing on mechanical keyboard, subtle breathing, head scanning monitors
          rig.hips.position.y = 0.68 + Math.sin(time * 2.5 + seed) * 0.012; // Breathing
          rig.hips.position.z = 0;
          rig.group.position.set(0, 0, -0.45);
          rig.group.rotation.y = 0;

          // Sitting leg pose (bent at 90 degrees)
          rig.leftLegGroup.rotation.x = -Math.PI / 2.2;
          rig.rightLegGroup.rotation.x = -Math.PI / 2.2;

          // Alternating fast keyboard typing
          rig.leftShoulder.rotation.x = 0.75 + Math.sin(time * 14 + seed) * 0.1;
          rig.leftShoulder.rotation.z = -0.2;
          rig.rightShoulder.rotation.x = 0.75 + Math.cos(time * 14 + seed) * 0.1;
          rig.rightShoulder.rotation.z = 0.2;

          // Head gently panning across dual screens
          rig.headGroup.rotation.y = Math.sin(time * 0.9 + seed) * 0.25;
          rig.headGroup.rotation.x = Math.sin(time * 1.5 + seed) * 0.06;

        } else if (ag.state === 'WALKING' || ag.state === 'WALKING_BACK') {
          // Standing & Walking naturally across the office!
          const dur = 6.0; // Seconds for walk
          const elapsed = (time - ag.walkStartTime) % dur;
          const progress = Math.min(elapsed / dur, 1.0);

          const startPos = ag.state === 'WALKING' ? ag.workstationPos : new THREE.Vector3(ag.info.walkTarget.x, 0, ag.info.walkTarget.z);
          const endPos = ag.state === 'WALKING' ? new THREE.Vector3(ag.info.walkTarget.x, 0, ag.info.walkTarget.z) : ag.workstationPos;

          // Interpolate world position
          const currentPos = new THREE.Vector3().lerpVectors(startPos, endPos, progress);
          ag.rig.group.position.copy(currentPos).sub(ag.workstationPos); // Relative to group

          // Face walk direction
          const dir = new THREE.Vector3().subVectors(endPos, startPos).normalize();
          const targetRot = Math.atan2(dir.x, dir.z);
          ag.rig.group.rotation.y = targetRot;

          // Upright standing hips with vertical footfall bounce
          rig.hips.position.y = 0.92 + Math.abs(Math.sin(time * 10)) * 0.08;
          rig.hips.position.z = 0;

          // Alternating leg swing
          rig.leftLegGroup.rotation.x = Math.sin(time * 10) * 0.65;
          rig.rightLegGroup.rotation.x = -Math.sin(time * 10) * 0.65;

          // Natural opposite arm swing
          rig.leftShoulder.rotation.x = -Math.sin(time * 10) * 0.5;
          rig.leftShoulder.rotation.z = -0.1;
          rig.rightShoulder.rotation.x = Math.sin(time * 10) * 0.5;
          rig.rightShoulder.rotation.z = 0.1;

          rig.headGroup.rotation.y = 0;

          // Arrived at destination
          if (progress >= 1.0) {
            if (ag.state === 'WALKING') {
              ag.state = 'AT_TARGET';
              ag.stayStartTime = time;
            } else {
              ag.state = 'WORKING';
            }
          }

        } else if (ag.state === 'AT_TARGET') {
          // Interacting at target (Drinking coffee, checking whiteboard, inspecting server)
          rig.hips.position.y = 0.92;
          rig.leftLegGroup.rotation.x = 0;
          rig.rightLegGroup.rotation.x = 0;

          // Gesturing / inspecting
          rig.rightShoulder.rotation.x = 1.1 + Math.sin(time * 2) * 0.2;
          rig.leftShoulder.rotation.x = 0.3;
          rig.headGroup.rotation.y = Math.sin(time * 1.2) * 0.35;

          // Stay for 4 seconds then walk back
          if (time - ag.stayStartTime > 4.5) {
            ag.state = 'WALKING_BACK';
            ag.walkStartTime = time;
          }
        }
      });

      // B. Update Dynamic Animated Server LEDs
      animatedObjects.forEach(obj => {
        if (obj.type === 'server_leds') {
          const ctx = obj.ctx;
          ctx.fillStyle = '#0a0f1d';
          ctx.fillRect(0, 0, 128, 256);

          for (let y = 10; y < 240; y += 12) {
            for (let x = 12; x < 116; x += 14) {
              const pulse = Math.sin(time * 8 + x * 0.3 + y * 0.2 + obj.offset);
              ctx.fillStyle = pulse > 0.3 ? '#22c55e' : (pulse < -0.4 ? '#38bdf8' : '#1e293b');
              ctx.fillRect(x, y, 7, 7);
            }
          }
          obj.texture.needsUpdate = true;
        } else if (obj.type === 'steam') {
          // Floating coffee steam
          obj.particles.forEach(p => {
            p.position.y += 0.003 * p.userData.speed;
            p.scale.setScalar(1 + (p.position.y - p.userData.baseY) * 2);
            if (p.position.y > p.userData.baseY + 0.35) {
              p.position.y = p.userData.baseY;
              p.scale.setScalar(1);
            }
          });
        }
      });

      // C. Update Dynamic Scrolling Monitor Screens
      if (Math.floor(time * 10) % 3 === 0) {
        Object.keys(dynamicTextures).forEach(key => {
          if (key.startsWith('screen_')) {
            const dt = dynamicTextures[key];
            const ctx = dt.ctx;
            ctx.fillStyle = '#060a12';
            ctx.fillRect(0, 0, 512, 256);

            // Terminal Code Header
            ctx.fillStyle = '#38bdf8';
            ctx.font = 'bold 16px monospace';
            ctx.fillText(`NEXUS-AI OS 2.0 • [${dt.agentId.toUpperCase()}] ACTIVE TASK`, 20, 30);

            // Animated Sine Wave / Candlestick Bars
            ctx.strokeStyle = '#22c55e';
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            for (let px = 20; px < 490; px += 5) {
              const py = 120 + Math.sin((px * 0.04) + time * 5) * 35;
              if (px === 20) ctx.moveTo(px, py);
              else ctx.lineTo(px, py);
            }
            ctx.stroke();

            // Scrolling Log Lines
            ctx.fillStyle = '#94a3b8';
            ctx.font = '12px monospace';
            const logLines = [
              `> [SYNC] data.jakarta.go.id & Google Drive OK`,
              `> [AUDIT] 03C_TOBE_ASIS: Empty rows detected`,
              `> [SPBE] Auto-generating RAB/RAL L1-L3 taxonomy...`,
              `> [CORE] Ready for next corporate mandate.`
            ];
            logLines.forEach((line, lIdx) => {
              ctx.fillText(line, 20, 185 + lIdx * 16);
            });

            dt.texture.needsUpdate = true;
          }
        });
      }

      controls.update();
      renderer.render(scene, camera);

      // Project 2.5D HTML Speech Bubbles in Real-Time
      updateSpeechBubbles2D();
    }

    // Trigger Random Agent to Stand Up, Walk & Roam
    function triggerRandomWalk() {
      const keys = Object.keys(officeAgents);
      const idleAgents = keys.filter(k => officeAgents[k].state === 'WORKING');
      if (idleAgents.length === 0) return;

      const randomKey = idleAgents[Math.floor(Math.random() * idleAgents.length)];
      const ag = officeAgents[randomKey];
      ag.state = 'WALKING';
      ag.walkStartTime = clock.getElapsedTime();

      // Show action speech bubble
      if (serverState.agent_bubbles) {
        serverState.agent_bubbles[randomKey] = {
          text: `Bangkit menuju ${ag.info.walkTarget.label} untuk koordinasi...`,
          action: 'Walking'
        };
      }
    }

    function sendAgentOnMission() {
      const name = document.getElementById('agentName').innerText.toLowerCase();
      if (officeAgents[name]) {
        const ag = officeAgents[name];
        ag.state = 'WALKING';
        ag.walkStartTime = clock.getElapsedTime();
      }
    }

    // Camera Views Presets
    function setCameraView(preset) {
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
    }

    function resetCameraView() {
      setCameraView('iso');
    }

    function focusOnAgent(agentId) {
      const ag = officeAgents[agentId];
      if (!ag) return;
      const pos = ag.workstationPos;
      gsapAnimateCamera(pos.x + 5.5, pos.y + 7.5, pos.z + 8.5, pos.x, pos.y + 1.2, pos.z);
      openAgentDetail(agentId);
    }

    function gsapAnimateCamera(toX, toY, toZ, lookX, lookY, lookZ) {
      let startTime = performance.now();
      let duration = 850;
      let startCam = camera.position.clone();
      let startTarget = controls.target.clone();
      let endCam = new THREE.Vector3(toX, toY, toZ);
      let endTarget = new THREE.Vector3(lookX, lookY, lookZ);

      function step() {
        let elapsed = performance.now() - startTime;
        let progress = Math.min(elapsed / duration, 1);
        let ease = 0.5 - Math.cos(progress * Math.PI) / 2; // Smooth ease in-out

        camera.position.lerpVectors(startCam, endCam, ease);
        controls.target.lerpVectors(startTarget, endTarget, ease);
        controls.update();

        if (progress < 1) {
          requestAnimationFrame(step);
        }
      }
      step();
    }

    // 2.5D Speech Bubbles Projection
    function updateSpeechBubbles2D() {
      const container = document.getElementById('bubbles-layer');
      const w = window.innerWidth;
      const h = window.innerHeight;

      Object.keys(agentPositions).forEach(agentId => {
        let el = document.getElementById(`bubble-${agentId}`);
        const ag = officeAgents[agentId];
        if (!ag) return;

        if (!el) {
          el = document.createElement('div');
          el.id = `bubble-${agentId}`;
          el.className = 'speech-bubble pointer-events-auto cursor-pointer';
          el.onclick = () => focusOnAgent(agentId);
          container.appendChild(el);
        }

        // Get world position of character head
        const headWorldPos = new THREE.Vector3();
        ag.rig.headGroup.getWorldPosition(headWorldPos);
        headWorldPos.y += 0.8; // Elevation above head

        headWorldPos.project(camera);

        if (headWorldPos.z > 1) {
          el.style.display = 'none';
          return;
        }

        const screenX = (headWorldPos.x * 0.5 + 0.5) * w;
        const screenY = (-(headWorldPos.y * 0.5) + 0.5) * h;

        el.style.display = 'block';
        el.style.left = `${screenX}px`;
        el.style.top = `${screenY}px`;

        const bubbleData = (serverState.agent_bubbles && serverState.agent_bubbles[agentId]) || {};
        const defaultTexts = {
          arka: { text: "Memimpin C-Suite & membagi tugas audit SPBE DKI...", action: "CEO Orchestrator" },
          naya: { text: "Mengekstrak data Google Sheets & repositori.jakarta...", action: "Research Intel" },
          raka: { text: "Auto-generate 39 proses bisnis & arsitektur API...", action: "Tech Engineering" },
          sekar: { text: "Memeriksa dokumen kosong & audit BAST 11 OPD...", action: "Compliance Audit" },
          dimas: { text: "Menyiapkan SOP 90 hari & PIC tindak lanjut dinas...", action: "Operations GTM" }
        };

        const currentText = bubbleData.text || defaultTexts[agentId].text;
        const currentAction = bubbleData.action || defaultTexts[agentId].action;
        const info = agentPositions[agentId];

        el.innerHTML = `
          <div class="bg-slate-900/95 backdrop-blur-xl border border-slate-700/80 rounded-2xl p-2.5 shadow-2xl max-w-[260px] text-left transition hover:scale-105 hover:border-blue-400">
            <div class="flex items-center justify-between gap-1.5 mb-1 pb-1 border-b border-slate-800">
              <span class="flex items-center gap-1.5 text-[11px] font-bold text-white">
                <span class="text-xs">${info.avatar}</span>
                <span>${info.name}</span>
                <span class="text-[9px] text-slate-400 font-normal">(${currentAction})</span>
              </span>
              <span class="w-4 h-4 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-[10px] font-bold">!</span>
            </div>
            <p class="text-[11px] text-slate-200 leading-snug line-clamp-3">${currentText}</p>
          </div>
        `;
      });
    }

    // Raycasting for Agent Click
    function setupRaycastSelection() {
      const raycaster = new THREE.Raycaster();
      const mouse = new THREE.Vector2();

      window.addEventListener('click', (e) => {
        if (e.target.closest('header') || e.target.closest('#reportDrawer') || e.target.closest('#agentDetailCard') || e.target.closest('.bottom-5') || e.target.closest('.speech-bubble')) return;

        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(scene.children, true);

        for (let hit of intersects) {
          let curr = hit.object;
          while (curr && curr.parent && curr.parent !== scene) {
            if (curr.userData && curr.userData.agentId) {
              focusOnAgent(curr.userData.agentId);
              return;
            }
            curr = curr.parent;
          }
        }
      });
    }

    function onWindowResize() {
      const container = document.getElementById('canvas-container');
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }

    // Backend Polling & API Communication
    async function pollServerStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        serverState = data;
        renderTasksList();
      } catch (err) {
        console.warn('Status poll warn:', err.message);
      }
    }

    async function dispatchMandate() {
      const input = document.getElementById('mandateInput');
      const mandate = input.value.trim();
      if (!mandate) return;

      const btn = document.getElementById('btnDispatch');
      btn.disabled = true;
      btn.innerHTML = `<i class="fa-solid fa-spinner animate-spin"></i><span>Sedang Mengeksekusi...</span>`;

      try {
        const res = await fetch('/api/run', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ mandate })
        });
        const data = await res.json();
        console.log('Mandat terkirim:', data);
        setTimeout(pollServerStatus, 500);
      } catch (err) {
        alert('Gagal mendispatch mandat: ' + err.message);
      } finally {
        setTimeout(() => {
          btn.disabled = false;
          btn.innerHTML = `<i class="fa-solid fa-paper-plane"></i><span class="hidden sm:inline">Perintahkan Tim</span>`;
        }, 1500);
      }
    }

    function setPrompt(text) {
      document.getElementById('mandateInput').value = text;
    }

    function openAgentDetail(agentId) {
      const card = document.getElementById('agentDetailCard');
      const info = agentPositions[agentId];
      if (!info) return;

      const agentData = (serverState.agents || []).find(a => a.id === agentId) || {};
      const agentTasks = (serverState.tasks || []).filter(t => t.agent === agentId);
      const activeTask = agentTasks.find(t => t.status === 'IN PROGRESS') || agentTasks[agentTasks.length - 1];

      document.getElementById('agentAvatar').innerText = info.avatar;
      document.getElementById('agentName').innerText = info.name;
      document.getElementById('agentTitle').innerText = info.title;

      const bubble = (serverState.agent_bubbles && serverState.agent_bubbles[agentId]) || {};
      document.getElementById('agentBubbleLive').innerText = `"${bubble.text || activeTask?.description || 'Siap mengeksekusi mandat operasional.'}"`;

      const badge = document.getElementById('agentStatusBadge');
      const status = activeTask ? activeTask.status : 'ONLINE & ANIMATED';
      badge.innerText = status;

      const skillsContainer = document.getElementById('agentSkillBadges');
      const skills = agentData.skills || ['system-architecture', 'financial-analysis', 'strategic-planning', 'data-analytics'];
      skillsContainer.innerHTML = skills.slice(0, 4).map(s => 
        `<span class="bg-slate-800 text-slate-300 text-[9px] px-2 py-0.5 rounded border border-slate-700">${s}</span>`
      ).join('');

      card.classList.remove('hidden');
    }

    function closeAgentDetail() {
      document.getElementById('agentDetailCard').classList.add('hidden');
    }

    function toggleReportDrawer() {
      const drawer = document.getElementById('reportDrawer');
      drawer.classList.toggle('translate-x-full');
      if (!drawer.classList.contains('translate-x-full')) {
        loadDocContent();
      }
    }

        function switchDrawerTab(tab) {
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
    }

    async function loadDocContent() {
      const select = document.getElementById('docSelector');
      const filename = select.value;
      const area = document.getElementById('docContentArea');
      area.innerHTML = `
        <div class="flex items-center justify-center gap-2 py-8 text-slate-400">
          <i class="fa-solid fa-spinner animate-spin text-blue-400 text-base"></i>
          <span>Memuat berkas laporan ${escapeHtml(filename)}...</span>
        </div>
      `;

      try {
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
        const text = await res.text();

        if (filename.endsWith('.md')) {
          if (typeof marked !== 'undefined') {
            area.innerHTML = marked.parse(text);
          } else {
            area.innerHTML = `<div class="whitespace-pre-wrap leading-relaxed">${escapeHtml(text)}</div>`;
          }
        } else if (filename.endsWith('.json')) {
          try {
            const parsed = JSON.parse(text);
            area.innerHTML = `<pre class="text-emerald-400 bg-slate-950 p-4 rounded-xl border border-slate-800 text-[11px] overflow-x-auto">${escapeHtml(JSON.stringify(parsed, null, 2))}</pre>`;
          } catch {
            area.innerHTML = `<pre class="text-slate-300 text-[11px]">${escapeHtml(text)}</pre>`;
          }
        } else {
          area.innerHTML = `<div class="whitespace-pre-wrap text-slate-300 leading-relaxed">${escapeHtml(text)}</div>`;
        }
      } catch (e) {
        area.innerHTML = `
          <div class="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400 text-xs flex items-center gap-2">
            <i class="fa-solid fa-circle-exclamation text-base"></i>
            <span>Gagal memuat laporan: ${escapeHtml(e.message)}</span>
          </div>
        `;
      }
    }

    function renderTasksList() {
      const container = document.getElementById('tasksListContainer');
      const tasks = serverState.tasks || [];
      if (tasks.length === 0) {
        container.innerHTML = '<div class="text-center text-slate-500 py-10">Belum ada tugas aktif.</div>';
        return;
      }

      container.innerHTML = tasks.map(t => `
        <div class="bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-white">${t.agent_name || t.agent.toUpperCase()}</span>
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${
              t.status === 'COMPLETED' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
              t.status === 'IN PROGRESS' ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30 animate-pulse' :
              'bg-slate-800 text-slate-400'
            }">${t.status}</span>
          </div>
          <p class="text-slate-300 text-[11px] mb-1">${t.description}</p>
          ${t.result_summary ? `<div class="bg-slate-900 border border-slate-800 rounded p-1.5 text-[10px] text-emerald-300"><i class="fa-solid fa-check text-emerald-400 mr-1"></i>${t.result_summary}</div>` : ''}
        </div>
      `).join('');
    }

    function escapeHtml(str) {
      return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    // Auto-roam cycle every 18 seconds
    setInterval(triggerRandomWalk, 18000);

    // Page Load
    window.onload = () => {
      init3DOffice();
      pollServerStatus();
      setInterval(pollServerStatus, 2500);
    };
  