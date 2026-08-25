from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config import API_HOST, API_PORT, API_DEBUG
from app.routes import router
from app.database import Base, engine

# Create app instance
app = FastAPI(
    title="RJPP Novelty Detection API",
    description="Sistem deteksi inovasi dokumen RJPP dengan freshness scoring",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RJPP Novelty Detection API",
        "status": "running",
        "version": "1.0.0",
        "docs": "http://127.0.0.1:8000/docs",
        "redoc": "http://127.0.0.1:8000/redoc"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "RJPP Novelty Detection"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        debug=API_DEBUG,
        log_level="info"
    )
