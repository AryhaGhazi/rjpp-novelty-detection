from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os
from pathlib import Path
from app.database import get_db, Innovation, DocumentMetadata
from app.pdf_processor import PDFProcessor
from app.novelty_detector import NoveltyDetector
from app.freshness_scorer import FreshnessScorer
from app.config import UPLOAD_DIR, MAX_FILE_SIZE
from datetime import datetime
import uuid

router = APIRouter(prefix="/api", tags=["innovations"])

pdf_processor = PDFProcessor()
novelty_detector = NoveltyDetector()
freshness_scorer = FreshnessScorer()

@router.post("/upload")
async def upload_rjpp(file: UploadFile = File(...), year: int = None, db: Session = Depends(get_db)):
    """Upload RJPP PDF and process for innovations"""
    
    # Validate file
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")
    
    try:
        # Save file
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
        
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Extract year from filename if not provided
        if year is None:
            import re
            year_match = re.search(r'(\d{4})', file.filename)
            year = int(year_match.group(1)) if year_match else datetime.now().year
        
        # Process PDF
        pdf_processor.load_pdf(str(file_path))
        text_content = pdf_processor.get_text()
        
        # Get historical innovations for comparison
        historical_innovations = db.query(Innovation).filter(Innovation.year < year).all()
        historical_data = [
            {
                'id': inn.id,
                'title': inn.title,
                'description': inn.description,
                'year': inn.year,
                'novelty_score': inn.novelty_score,
                'embedding': inn.embedding
            }
            for inn in historical_innovations
        ]
        
        # Detect innovations
        detected_innovations = novelty_detector.detect_innovations(text_content, historical_data)
        
        # Save document metadata
        doc_metadata = DocumentMetadata(
            filename=file.filename,
            year=year,
            file_path=str(file_path),
            total_innovations=len(detected_innovations),
            processed=1
        )
        db.add(doc_metadata)
        db.commit()
        
        # Save innovations to database
        saved_innovations = []
        for innovation in detected_innovations:
            freshness_score = freshness_scorer.calculate_freshness_score(
                innovation, year, historical_data
            )
            
            db_innovation = Innovation(
                year=year,
                title=innovation['title'],
                description=innovation['description'],
                category='general',
                embedding=str(innovation['embedding']),
                novelty_score=innovation['novelty_score'],
                freshness_score=freshness_score,
                source_file=file.filename
            )
            db.add(db_innovation)
            saved_innovations.append(db_innovation)
        
        db.commit()
        
        return {
            'status': 'success',
            'message': f'Uploaded {file.filename} for year {year}',
            'file_id': file_id,
            'year': year,
            'innovations_detected': len(detected_innovations),
            'innovations': [
                {
                    'title': inn.title,
                    'novelty_score': inn.novelty_score,
                    'freshness_score': inn.freshness_score,
                    'freshness_category': freshness_scorer.categorize_freshness(inn.freshness_score)
                }
                for inn in saved_innovations
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@router.get("/innovations")
async def get_all_innovations(db: Session = Depends(get_db)):
    """Get all detected innovations"""
    innovations = db.query(Innovation).order_by(Innovation.created_at.desc()).all()
    
    return {
        'total': len(innovations),
        'innovations': [
            {
                'id': inn.id,
                'year': inn.year,
                'title': inn.title,
                'description': inn.description[:200],
                'novelty_score': inn.novelty_score,
                'freshness_score': inn.freshness_score,
                'freshness_category': freshness_scorer.categorize_freshness(inn.freshness_score),
                'source_file': inn.source_file,
                'created_at': inn.created_at.isoformat()
            }
            for inn in innovations
        ]
    }

@router.get("/innovations/year/{year}")
async def get_innovations_by_year(year: int, db: Session = Depends(get_db)):
    """Get innovations for specific year"""
    innovations = db.query(Innovation).filter(Innovation.year == year).order_by(Innovation.novelty_score.desc()).all()
    
    return {
        'year': year,
        'total': len(innovations),
        'innovations': [
            {
                'id': inn.id,
                'title': inn.title,
                'description': inn.description[:200],
                'novelty_score': inn.novelty_score,
                'freshness_score': inn.freshness_score,
                'freshness_category': freshness_scorer.categorize_freshness(inn.freshness_score),
                'source_file': inn.source_file
            }
            for inn in innovations
        ]
    }

@router.get("/innovations/{innovation_id}")
async def get_innovation_detail(innovation_id: str, db: Session = Depends(get_db)):
    """Get detailed information about specific innovation"""
    innovation = db.query(Innovation).filter(Innovation.id == innovation_id).first()
    
    if not innovation:
        raise HTTPException(status_code=404, detail="Innovation not found")
    
    # Find similar innovations
    similar = novelty_detector.find_similar_innovations(
        innovation.title + ' ' + innovation.description,
        [
            {
                'id': inn.id,
                'title': inn.title,
                'description': inn.description,
                'year': inn.year,
                'embedding': eval(inn.embedding) if inn.embedding else []
            }
            for inn in db.query(Innovation).filter(Innovation.id != innovation_id).all()
        ]
    )
    
    return {
        'id': innovation.id,
        'year': innovation.year,
        'title': innovation.title,
        'description': innovation.description,
        'category': innovation.category,
        'novelty_score': innovation.novelty_score,
        'freshness_score': innovation.freshness_score,
        'freshness_category': freshness_scorer.categorize_freshness(innovation.freshness_score),
        'source_file': innovation.source_file,
        'created_at': innovation.created_at.isoformat(),
        'similar_innovations': [
            {
                'id': sim[0]['id'],
                'title': sim[0]['title'],
                'year': sim[0]['year'],
                'similarity_score': sim[1]
            }
            for sim in similar[:5]
        ]
    }

@router.get("/comparison")
async def compare_years(db: Session = Depends(get_db)):
    """Compare innovations across years"""
    innovations = db.query(Innovation).all()
    
    # Group by year
    by_year = {}
    for inn in innovations:
        if inn.year not in by_year:
            by_year[inn.year] = {
                'count': 0,
                'avg_novelty': 0,
                'avg_freshness': 0,
                'innovations': []
            }
        
        by_year[inn.year]['count'] += 1
        by_year[inn.year]['innovations'].append({
            'title': inn.title,
            'novelty_score': inn.novelty_score,
            'freshness_score': inn.freshness_score
        })
    
    # Calculate averages
    for year in by_year:
        inns = by_year[year]['innovations']
        by_year[year]['avg_novelty'] = sum(i['novelty_score'] for i in inns) / len(inns) if inns else 0
        by_year[year]['avg_freshness'] = sum(i['freshness_score'] for i in inns) / len(inns) if inns else 0
    
    return {
        'comparison': by_year,
        'years': sorted(by_year.keys())
    }

@router.get("/documents")
async def get_documents(db: Session = Depends(get_db)):
    """Get list of uploaded documents"""
    documents = db.query(DocumentMetadata).order_by(DocumentMetadata.created_at.desc()).all()
    
    return {
        'total': len(documents),
        'documents': [
            {
                'id': doc.id,
                'filename': doc.filename,
                'year': doc.year,
                'total_innovations': doc.total_innovations,
                'processed': doc.processed,
                'created_at': doc.created_at.isoformat(),
                'processed_at': doc.processed_at.isoformat() if doc.processed_at else None
            }
            for doc in documents
        ]
    }

@router.post("/freshness-report")
async def generate_freshness_report(year: int = None, db: Session = Depends(get_db)):
    """Generate freshness report for specific year or all years"""
    if year:
        innovations = db.query(Innovation).filter(Innovation.year == year).all()
    else:
        innovations = db.query(Innovation).all()
    
    innovation_dicts = [
        {
            'id': inn.id,
            'title': inn.title,
            'description': inn.description,
            'year': inn.year,
            'novelty_score': inn.novelty_score
        }
        for inn in innovations
    ]
    
    historical_data = db.query(Innovation).all()
    
    report = freshness_scorer.get_freshness_report(
        innovation_dicts,
        year or datetime.now().year,
        [{'title': h.title, 'year': h.year} for h in historical_data]
    )
    
    return {
        'year': year,
        'total_innovations': len(report),
        'report': report
    }
