---
name: software-engineering
description: Enterprise software engineering, production code development, testing frameworks, and secure coding practices across Python, TypeScript, and backend architectures. Use when building, debugging, or reviewing production software.
---

# SKILL: Enterprise Software Engineering & Production Development

## 1. Nama Skill
**Enterprise Software Engineering & Production Development (Full-Stack & Robust Coding)**

## 2. Deskripsi
Skill rekayasa perangkat lunak standar industri untuk merancang, menulis, menguji, dan memelihara kode program yang modular, bersih, berperforma tinggi, dan aman pada berbagai ekosistem (Python, TypeScript/JavaScript, REST APIs, SQL/NoSQL).

## 3. Tujuan
- Menghasilkan kode aplikasi kelas produksi dengan penanganan error komprehensif, logging terstruktur, dan type safety.
- Menjamin maintainability dan scalability kode sesuai prinsip SOLID, DRY, dan Clean Architecture.
- Mengimplementasikan pengujian otomatis (unit testing, integration testing) dengan code coverage memadai.

## 4. Ruang Lingkup
- Backend API development (FastAPI, Express.js, Django, NestJS).
- Frontend application architecture (React, Next.js, modern state management).
- Database querying & ORM modeling (PostgreSQL, Prisma, SQLAlchemy).
- Unit & integration testing suites (pytest, Jest, Vitest).
- Refactoring, debugging, dan automated code review.

## 5. Metodologi Kerja
- **Prinsip SOLID & Clean Code:** Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion.
- **Test-Driven / Test-First Approach:** Menulis test case untuk skenario ideal, edge case, dan failure mode.
- **Defensive Programming:** Validasi ketat terhadap input eksternal, deserialisasi aman, dan graceful degradation saat error.

## 6. Langkah Pelaksanaan
1. **Analisis Kebutuhan Fungsional & Non-Fungsional:** Memetakan input/output, latency requirement, dan batas beban sistem.
2. **Desain Modul & Interface Contract:** Menentukan skema data (Pydantic / TypeScript Interfaces) sebelum menulis logika bisnis.
3. **Implementasi Logika Bisnis:** Menulis kode bersih dengan penamaan variabel deklaratif dan dokumentasi docstring/JSDoc.
4. **Error Handling & Structured Logging:** Memastikan setiap titik kegagalan loggable dan terisolasi tanpa menyebabkan server crash.
5. **Penulisan Automated Tests:** Membuat test suite mencakup skenario sukses dan skenario error.
6. **Code Review & Security Linting:** Memeriksa potensi kerentanan keamanan (injection, prototype pollution, memory leaks).

## 7. Standar Kualitas
- Kode wajib dapat dieksekusi secara nyata (tidak ada placeholder `// implement here later` pada fungsi krusial).
- Seluruh fungsi memiliki type annotation lengkap dan validasi error eksplisit.
- Lolos uji linter dan pengujian otomatis tanpa failure.

## 8. Format Output
- **Production Code Blocks:** Kode lengkap, terstruktur, disertai komentar fungsional.
- **Unit Test Suite:** Kode pengujian siap dijalankan dengan framework testing terkait.
- **Setup & Execution Instructions:** Perintah instalasi dependensi dan eksekusi lokal.

## 9. Contoh Penggunaan
RAKA menggunakan skill ini untuk: *"Membangun service autentikasi multi-tenant dengan JWT, refresh token rotation, dan rate limiter berbasis Redis di TypeScript."*

## 10. Batasan dan Hal yang Tidak Boleh Dilakukan
- DILARANG menulis kredensial atau API key hardcoded di dalam source code.
- DILARANG menelan error secara diam-diam (empty `catch {}` atau `except: pass`).
- DILARANG memproduksi kode monolitik spaghetti tanpa modularitas yang jelas.
