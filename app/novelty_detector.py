from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Tuple, Dict
from app.config import EMBEDDING_MODEL, NOVELTY_THRESHOLD, SIMILARITY_THRESHOLD
import json

class NoveltyDetector:
    """Detect novelty in innovations using semantic similarity"""
    
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.embeddings_cache = {}
    
    def extract_innovations(self, text: str) -> List[str]:
        """Extract potential innovations from text using simple heuristics"""
        innovations = []
        
        # Split by common innovation markers
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Look for lines that contain keywords
            innovation_keywords = ['inovasi', 'baru', 'pengembangan', 'strategi', 'program', 
                                 'inisiatif', 'peningkatan', 'implementasi', 'solusi']
            
            if len(line) > 20 and any(keyword in line.lower() for keyword in innovation_keywords):
                innovations.append(line)
        
        return innovations
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text"""
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        embedding = self.model.encode(text)
        self.embeddings_cache[text] = embedding
        return embedding
    
    def calculate_novelty_score(self, new_innovation: str, historical_innovations: List[Dict]) -> float:
        """
        Calculate novelty score for new innovation
        Score 1.0 = completely novel
        Score 0.0 = very similar to existing innovations
        """
        if not historical_innovations:
            return 1.0
        
        new_embedding = self.get_embedding(new_innovation)
        max_similarity = 0.0
        
        for hist_innovation in historical_innovations:
            hist_text = hist_innovation.get('title', '') + ' ' + hist_innovation.get('description', '')
            hist_embedding = self.get_embedding(hist_text)
            
            similarity = cosine_similarity([new_embedding], [hist_embedding])[0][0]
            max_similarity = max(max_similarity, similarity)
        
        novelty_score = 1.0 - max_similarity
        return max(0.0, min(1.0, novelty_score))
    
    def detect_innovations(self, text: str, historical_innovations: List[Dict] = None) -> List[Dict]:
        """Detect innovations in text and calculate novelty scores"""
        if historical_innovations is None:
            historical_innovations = []
        
        extracted = self.extract_innovations(text)
        innovations = []
        
        for innovation_text in extracted:
            novelty_score = self.calculate_novelty_score(innovation_text, historical_innovations)
            is_novel = novelty_score >= NOVELTY_THRESHOLD
            
            innovations.append({
                'title': innovation_text[:100],
                'description': innovation_text,
                'novelty_score': float(novelty_score),
                'is_novel': is_novel,
                'embedding': self.get_embedding(innovation_text).tolist()
            })
        
        return sorted(innovations, key=lambda x: x['novelty_score'], reverse=True)
    
    def find_similar_innovations(self, innovation_text: str, candidates: List[Dict], threshold: float = SIMILARITY_THRESHOLD) -> List[Tuple[Dict, float]]:
        """Find similar innovations from candidates"""
        innovation_embedding = self.get_embedding(innovation_text)
        similar = []
        
        for candidate in candidates:
            candidate_embedding = np.array(candidate.get('embedding', []))
            if len(candidate_embedding) == 0:
                candidate_text = candidate.get('title', '') + ' ' + candidate.get('description', '')
                candidate_embedding = self.get_embedding(candidate_text)
            
            similarity = cosine_similarity([innovation_embedding], [candidate_embedding])[0][0]
            
            if similarity >= threshold:
                similar.append((candidate, float(similarity)))
        
        return sorted(similar, key=lambda x: x[1], reverse=True)
