import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rjpp_novelty.db")

# NLP Model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
LANGUAGE = os.getenv("LANGUAGE", "id")

# Thresholds
NOVELTY_THRESHOLD = float(os.getenv("NOVELTY_THRESHOLD", 0.7))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.6))

# Freshness Scoring Weights
RECENCY_WEIGHT = float(os.getenv("RECENCY_WEIGHT", 0.4))
FREQUENCY_WEIGHT = float(os.getenv("FREQUENCY_WEIGHT", 0.3))
TREND_WEIGHT = float(os.getenv("TREND_WEIGHT", 0.3))

# API Configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))
API_DEBUG = os.getenv("API_DEBUG", "True") == "True"

# Upload Configuration
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 52428800))  # 50MB
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads/"))
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "pdf").split(",")

# Ensure upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
