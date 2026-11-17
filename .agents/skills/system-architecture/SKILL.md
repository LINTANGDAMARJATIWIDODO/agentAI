---
name: system-architecture
description: Design scalable cloud architectures, microservices topologies, database schemas, and zero-trust security postures. Use when architecting enterprise systems or evaluating technical infrastructure.
---

# SKILL: Enterprise System Architecture & Cloud Infrastructure

## 1. Nama Skill
**Enterprise System Architecture & Cloud Infrastructure (High-Availability Design)**

## 2. Deskripsi
Skill arsitektur teknologi tingkat Principal untuk merancang topologi sistem terdistribusi, perancangan skema database tingkat lanjut, infrastruktur cloud multi-region, pipeline CI/CD, dan model keamanan Zero-Trust untuk skala perusahaan besar.

## 3. Tujuan
- Merancang arsitektur sistem yang memenuhi standar ketersediaan tinggi (High Availability: 99.99%), toleransi kegagalan (Fault Tolerance), dan elastisitas beban.
- Memilih stack teknologi dan pola arsitektur yang paling hemat biaya (cost-efficient) tanpa mengorbankan performa.
- Menyediakan cetak biru arsitektur visual (Mermaid diagrams) dan spesifikasi teknis lengkap bagi tim pengembang.

## 4. Ruang Lingkup
- Topologi arsitektur sistem (Microservices, Event-Driven Architecture, Serverless, Modular Monolith).
- Desain arsitektur data (Relational, Document, Key-Value, Vector Search, Data Warehouses).
- Cloud Infrastructure (AWS / GCP / Azure topologies, VPC, Subnets, Load Balancers, CDN).
- Keamanan infrastruktur (Zero Trust, WAF, DDoS mitigation, RBAC, Secrets Management).
- Perencanaan kapasitas dan kalkulasi footprint komputasi.

## 5. Metodologi Kerja
- **The Twelve-Factor App Methodology:** Standar best-practice aplikasi cloud-native modern.
- **Well-Architected Framework (AWS/GCP):** Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability.
- **C4 Model Architecture Diagramming:** Context, Containers, Components, and Code level representations.

## 6. Langkah Pelaksanaan
1. **Analisis Beban & Karakteristik Beban:** Menentukan target throughput (RPS), target latency p99, dan volume data per hari.
2. **Pola Desain Sistem:** Memilih pola komunikasi sinkron (gRPC / REST) vs. asinkron (Kafka / RabbitMQ / Cloud PubSub).
3. **Desain Lapisan Data & Strategi Caching:** Menentukan master-replica replication, partisi sharding, dan lapisan Redis cache.
4. **Perancangan Keamanan Jaringan & Akses:** Menetapkan segmentasi jaringan, TLS termination, dan Zero-Trust identity perimeter.
5. **Kalkulasi Estimasi Resource Komputasi:** Menghitung jumlah vCPU, RAM, dan storage terdistribusi untuk diserahkan ke SEKAR.
6. **Pembuatan Diagram Arsitektur Mermaid:** Merender diagram alur data dan interkoneksi komponen secara visual.

## 7. Standar Kualitas
- Setiap komponen dalam diagram arsitektur harus memiliki alasan pemilihan yang terjustifikasi secara teknis dan finansial.
- Wajib memiliki skema Single Point of Failure (SPOF) identification dan mitigasinya.
- Diagram arsitektur menggunakan sintaks Mermaid standar yang valid.

## 8. Format Output
- **High-Level Architecture Overview**
- **C4 / Component Architecture Diagram (Mermaid)**
- **Data Flow & Communication Protocol Specification**
- **Security & Network Topology Blueprint**
- **Disaster Recovery (DR) & RPO/RTO Targets**
- **Infrastructure Bill of Materials (BOM) for SEKAR**

## 9. Contoh Penggunaan
RAKA menggunakan skill ini untuk: *"Merancang arsitektur backend perbankan berbasis microservices yang mampu menangani 25.000 transaksi per detik dengan latensi p99 < 50ms."*

## 10. Batasan dan Hal yang Tidak Boleh Dilakukan
- DILARANG merekomendasikan teknologi kompleks tanpa mempertimbangkan kurva pembelajaran tim dan biaya pemeliharaan.
- DILARANG mengabaikan estimasi tagihan cloud bulanan (wajib koordinasi dengan SEKAR).
- DILARANG merancang sistem tanpa lapisan backup, redundansi, dan recovery plan.
