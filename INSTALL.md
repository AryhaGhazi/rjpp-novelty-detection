# RJPP Novelty Detection System - Installation & Setup Guide

## Prasyarat Instalasi
- Python 3.8+
- pip (Python package manager)
- File manager untuk upload PDF

## Langkah-Langkah Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/AryhaGhazi/rjpp-novelty-detection.git
cd rjpp-novelty-detection
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Buat file `.env` di root folder:
```bash
cp .env.example .env
```

Edit `.env` sesuai kebutuhan Anda (opsional, sudah ada default value)

### 5. Jalankan Aplikasi

#### Opsi A: Menggunakan Python direktly
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Opsi B: Menggunakan Script
```bash
# Linux/Mac
bash run.sh

# Windows
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Akses Aplikasi

Setelah server berjalan, buka browser dan akses:

- **Interface Web**: http://127.0.0.1:8000/interface
- **API Documentation**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## Penggunaan Aplikasi

### Upload RJPP Document
1. Buka Interface Web: http://127.0.0.1:8000/interface
2. Klik area upload atau drag-drop file PDF
3. (Opsional) Masukkan tahun RJPP, jika tidak, akan otomatis dari filename
4. Klik tombol "Upload & Proses"
5. Tunggu hingga proses selesai

### Melihat Inovasi Terdeteksi
- Tab "Semua": Lihat semua inovasi dari semua dokumen
- Tab "Per Tahun": Filter inovasi berdasarkan tahun
- Tab "Perbandingan": Lihat perbandingan statistik antar tahun
- Tab "Dokumen": Lihat daftar dokumen yang telah diupload

## API Endpoints

### Upload Document
```
POST /api/upload
Content-Type: multipart/form-data

Parameters:
- file: PDF file (required)
- year: Tahun RJPP (optional, auto-detect dari filename)

Response:
{
    "status": "success",
    "message": "...",
    "file_id": "...",
    "year": 2024,
    "innovations_detected": 15,
    "innovations": [...]
}
```

### Get All Innovations
```
GET /api/innovations

Response:
{
    "total": 50,
    "innovations": [...]
}
```

### Get Innovations by Year
```
GET /api/innovations/year/{year}

Response:
{
    "year": 2024,
    "total": 15,
    "innovations": [...]
}
```

### Get Innovation Detail
```
GET /api/innovations/{innovation_id}

Response:
{
    "id": "...",
    "title": "...",
    "novelty_score": 0.85,
    "freshness_score": 0.75,
    "similar_innovations": [...]
}
```

### Compare Years
```
GET /api/comparison

Response:
{
    "comparison": {
        2023: { "count": 20, "avg_novelty": 0.7, "avg_freshness": 0.65 },
        2024: { "count": 15, "avg_novelty": 0.8, "avg_freshness": 0.75 }
    },
    "years": [2023, 2024]
}
```

### Get Documents
```
GET /api/documents

Response:
{
    "total": 2,
    "documents": [...]
}
```

### Generate Freshness Report
```
POST /api/freshness-report
JSON Body: { "year": 2024 } (optional)

Response:
{
    "year": 2024,
    "total_innovations": 15,
    "report": [...]
}
```

## Konfigurasi

Edit file `.env` untuk mengatur:

### Database
```
DATABASE_URL=sqlite:///./rjpp_novelty.db
# Atau PostgreSQL: postgresql://user:password@localhost/rjpp_novelty
```

### NLP Model
```
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
LANGUAGE=id
```

### Thresholds
```
NOVELTY_THRESHOLD=0.7        # 70% = considered novel
SIMILARITY_THRESHOLD=0.6     # 60% = considered similar
```

### Freshness Scoring Weights
```
RECENCY_WEIGHT=0.4           # 40% dari total score
FREQUENCY_WEIGHT=0.3         # 30% dari total score
TREND_WEIGHT=0.3             # 30% dari total score
```

### API Configuration
```
API_HOST=127.0.0.1
API_PORT=8000
API_DEBUG=True
```

### File Upload
```
MAX_FILE_SIZE=52428800       # 50MB
UPLOAD_DIR=uploads/
ALLOWED_EXTENSIONS=pdf
```

## Struktur Project

```
rjpp-novelty-detection/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database models & connection
│   ├── routes.py            # API endpoints
│   ├── pdf_processor.py     # PDF extraction logic
│   ├── novelty_detector.py  # Novelty detection engine
│   ├── freshness_scorer.py  # Freshness scoring logic
│   └── html_interface.py    # HTML UI code
├── uploads/                 # Uploaded PDF files directory
├── rjpp_novelty.db         # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── README.md               # This file
└── INSTALL.md             # This file
```

## Troubleshooting

### Error: ModuleNotFoundError
Pastikan Anda sudah install semua dependensi:
```bash
pip install -r requirements.txt
```

### Error: Port 8000 already in use
Gunakan port lain:
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

### Error: Database lock
Pastikan tidak ada instance lain yang mengakses database, atau gunakan PostgreSQL untuk production.

### Error: PDF tidak ter-upload
- Pastikan file adalah PDF valid
- Pastikan ukuran file < 50MB
- Cek folder `uploads/` memiliki write permission

## Performance Tips

1. **Untuk PDF besar**: Split dokumen menjadi bagian-bagian lebih kecil
2. **Untuk banyak dokumen**: Jalankan proses upload secara bersamaan di tab browser berbeda
3. **Database**: Migrasi ke PostgreSQL untuk production use

## Lisensi

MIT License - Bebas untuk digunakan dan dimodifikasi

## Support & Kontribusi

Jika ada pertanyaan atau saran, silakan buat issue di repository GitHub.

---

**Version**: 1.0.0  
**Last Updated**: 2026-08-25
