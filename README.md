# RJPP Novelty Detection System

Sistem deteksi inovasi untuk dokumen RJPP dengan kemampuan tracking inovasi historis dan penilaian freshness ide.

## Fitur Utama

### 1. **PDF Upload & Processing**
- Upload dokumen RJPP dalam format PDF
- Ekstraksi teks otomatis dari PDF
- Parsing dokumen untuk identifikasi inovasi

### 2. **Novelty Detection**
- Identifikasi inovasi baru berdasarkan perbandingan dengan dokumen sebelumnya
- Deteksi tren inovasi historis
- Kategorisasi inovasi per tahun

### 3. **Freshness Scoring**
- Scoring otomatis untuk mengukur seberapa baru suatu ide
- Baseline comparison dengan inovasi tahun-tahun sebelumnya
- Timeline tracking untuk setiap inovasi

### 4. **Innovation Database**
- Database terpusat untuk menyimpan semua inovasi yang terdeteksi
- Historical tracking dengan timestamp
- Metadata inovasi (kategori, deskripsi, tahun, novelty score)

## Tech Stack

- **Backend**: Python (FastAPI)
- **PDF Processing**: PyPDF2, pdfplumber
- **NLP**: sentence-transformers, FAISS
- **Database**: SQLite/PostgreSQL
- **API**: FastAPI with async support
- **Frontend**: Streamlit (untuk UI sederhana)

## Workflow

```
PDF Upload
    ↓
Text Extraction
    ↓
Innovation Extraction (NLP)
    ↓
Novelty Detection (Similarity Matching)
    ↓
Freshness Scoring
    ↓
Store to Database
    ↓
Dashboard Report
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### API Mode
```bash
python -m uvicorn app.main:app --reload
```

### Streamlit UI
```bash
streamlit run app/ui.py
```

## API Endpoints

- `POST /upload` - Upload PDF dokumen RJPP
- `GET /innovations` - Dapatkan daftar semua inovasi
- `GET /innovations/{year}` - Dapatkan inovasi per tahun
- `GET /freshness-score/{innovation_id}` - Dapatkan skor freshness
- `GET /comparison` - Bandingkan inovasi antar tahun

## Database Schema

### innovations table
- id (UUID)
- year (Integer)
- title (String)
- description (Text)
- category (String)
- embedding (Vector)
- novelty_score (Float 0-1)
- freshness_score (Float 0-1)
- created_at (Timestamp)
- source_file (String)

## Algoritma

### Novelty Detection
Menggunakan semantic similarity dengan sentence transformers untuk membandingkan inovasi baru dengan database historis.

### Freshness Scoring
- Berbasis recency: inovasi terbaru mendapat skor lebih tinggi
- Berbasis frequency: ide yang jarang muncul di tahun lalu mendapat skor tinggi
- Berbasis trend: inovasi yang baru pertama kali muncul = freshness maksimal

## Deployment

Siap untuk deployment ke:
- Docker container
- AWS Lambda
- Google Cloud Run
- Heroku

---

**Status**: Under Development
**Last Updated**: 2026-08-25
