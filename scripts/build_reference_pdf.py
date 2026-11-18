import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.document_intelligence.pdf_forensic_generator import generate_forensic_audit_pdf

sample_data = {
    'doc_title': 'Audit Forensik Naskah SPBE dan Penyelenggaraan Tata Kelola Digital',
    'doc_name': 'Arsitektur_SPBE_DKI_Jakarta_2027.pdf',
    'classification': 'HUMAN-LIKE',
    'probability': '15.4% (Terkalibrasi)',
    'confidence': 'Tinggi (High Certainty)',
    'statistics': {
        'sentence_count': 17,
        'paragraph_count': 5,
        'word_count': 382,
        'burstiness': 0.1684,
        'ttr': 0.884,
        'yules_k': 24.12,
        'shannon_entropy': 6.42
    },
    'sentence_pairs': [
        {
            'index': 1,
            'original': 'Pemanfaatan teknologi informasi dan komunikasi dalam penyelenggaraan pemerintahan di Indonesia telah berkembang dari upaya digitalisasi yang bersifat parsial menjadi agenda transformasi tata kelola yang terstruktur.',
            'characteristics': 'Sintaksis baku, variasi panjang klausa wajar, ragam formal.',
            'status': 'SUDAH BAIK',
            'score_indicator': '12.0% (Alami)',
            'recommendation': 'SUDAH BAIK — TIDAK MEMERLUKAN REVISI.',
            'revision_reason': 'Sesuai kaidah KBBI & EYD V.'
        },
        {
            'index': 2,
            'original': 'Perpres Nomor 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik (SPBE) hadir untuk memastikan keterpaduan layanan dan efisiensi belanja infrastruktur TIK nasional.',
            'characteristics': 'Rujukan regulasi presisi, struktur kalimat efektif.',
            'status': 'SUDAH BAIK',
            'score_indicator': '8.5% (Alami)',
            'recommendation': 'SUDAH BAIK — TIDAK MEMERLUKAN REVISI.',
            'revision_reason': 'Sesuai kaidah KBBI & EYD V.'
        },
        {
            'index': 3,
            'original': 'Dalam era digitalisasi yang serba cepat ini, implementasi arsitektur SPBE memegang peranan krusial bagi kemajuan birokrasi pemerintahan daerah.',
            'characteristics': 'Klise AI pembuka kalimat, metafora overused.',
            'status': 'REVISI SUBSTANTIF',
            'score_indicator': '86.2% (Tinggi)',
            'recommendation': 'Pada perkembangan transformasi tata kelola digital saat ini, implementasi arsitektur SPBE memiliki posisi strategis bagi peningkatan kinerja birokrasi pemerintah daerah.',
            'revision_reason': 'Eliminasi ungkapan klise mesin; penyesuaian register naskah dinas.'
        },
        {
            'index': 4,
            'original': 'Selain itu efisiensi anggaran yang mana telah ditetapkan pada regulasi harus diwujudkan secara nyata.',
            'characteristics': 'Koma intrakalimat hilang; kata penghubung rancu "yang mana".',
            'status': 'REVISI MINOR',
            'score_indicator': '34.0% (Sedang)',
            'recommendation': 'Selain itu, efisiensi anggaran yang telah ditetapkan pada regulasi harus diwujudkan secara nyata.',
            'revision_reason': 'Tanda koma wajib setelah konjungsi antarkalimat "Selain itu"; hapus "yang mana".'
        },
        {
            'index': 5,
            'original': 'Oleh karena itu, penguatan arsitektur SPBE pada tingkat pemerintah daerah menjadi kebutuhan mendesak.',
            'characteristics': 'Konjungsi antarkalimat sah, penalaran logis.',
            'status': 'SUDAH BAIK',
            'score_indicator': '11.0% (Alami)',
            'recommendation': 'SUDAH BAIK — TIDAK MEMERLUKAN REVISI.',
            'revision_reason': 'Sesuai kaidah KBBI & EYD V.'
        },
        {
            'index': 6,
            'original': 'Pemerintah daerah perlu melakukan praktek integrasi data antarperangkat daerah secara konsisten.',
            'characteristics': 'Kata nonbaku KBBI "praktek".',
            'status': 'REVISI MINOR',
            'score_indicator': '18.0% (Rendah)',
            'recommendation': 'Pemerintah daerah perlu melakukan praktik integrasi data antarperangkat daerah secara konsisten.',
            'revision_reason': 'KBBI: bentuk baku adalah "praktik", bukan "praktek".'
        },
        {
            'index': 7,
            'original': 'Dengan demikian, pelayanan publik dapat diselenggarakan secara lebih transparan, akuntabel, dan berkeadilan.',
            'characteristics': 'Konjungsi kesimpulan sah dengan tanda koma EYD V.',
            'status': 'SUDAH BAIK',
            'score_indicator': '9.0% (Alami)',
            'recommendation': 'SUDAH BAIK — TIDAK MEMERLUKAN REVISI.',
            'revision_reason': 'Sesuai kaidah KBBI & EYD V.'
        }
    ]
}

out = generate_forensic_audit_pdf(sample_data)
print('Generated comprehensive reference PDF:', out, 'Bytes:', os.path.getsize(out))
