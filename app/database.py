from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Innovation(Base):
    __tablename__ = "innovations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    year = Column(Integer, nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=True, index=True)
    embedding = Column(String, nullable=True)  # JSON string of embedding vector
    novelty_score = Column(Float, default=0.0)  # 0-1
    freshness_score = Column(Float, default=0.0)  # 0-1
    source_file = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Innovation {self.id}: {self.title}>"

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False, unique=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    file_path = Column(String, nullable=False)
    total_innovations = Column(Integer, default=0)
    processed = Column(Integer, default=0)  # 0=pending, 1=success, -1=failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<DocumentMetadata {self.id}: {self.filename}>"

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
