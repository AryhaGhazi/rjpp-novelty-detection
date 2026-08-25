from datetime import datetime, timedelta
from typing import List, Dict
import math
from app.config import RECENCY_WEIGHT, FREQUENCY_WEIGHT, TREND_WEIGHT

class FreshnessScorer:
    """Calculate freshness score for innovations"""
    
    def __init__(self):
        self.current_year = datetime.now().year
    
    def calculate_recency_score(self, year: int) -> float:
        """
        Score based on how recent the innovation is
        Most recent = 1.0, older = lower score
        """
        years_ago = self.current_year - year
        # Exponential decay: recent innovations get high score
        if years_ago < 0:
            return 1.0
        recency = math.exp(-0.1 * years_ago)
        return max(0.0, min(1.0, recency))
    
    def calculate_frequency_score(self, historical_occurrences: int, max_occurrences: int = 10) -> float:
        """
        Score based on frequency in historical data
        Lower frequency = higher freshness (more novel)
        Higher frequency = lower freshness (more common)
        """
        if max_occurrences == 0:
            return 1.0
        
        frequency_ratio = historical_occurrences / max_occurrences
        # Inverse: rare ideas are fresher
        frequency_score = 1.0 - min(1.0, frequency_ratio)
        return max(0.0, frequency_score)
    
    def calculate_trend_score(self, year_introduced: int, yearly_mentions: Dict[int, int]) -> float:
        """
        Score based on trend - if idea is newly introduced, score is high
        If idea appeared in previous years and disappeared, lower score
        """
        years_since_intro = self.current_year - year_introduced
        
        if years_since_intro < 0:
            return 1.0
        
        if years_since_intro == 0:
            # Brand new innovation
            return 1.0
        
        # Check if trend is growing or declining
        if year_introduced in yearly_mentions and (year_introduced + 1) in yearly_mentions:
            prev_count = yearly_mentions.get(year_introduced, 1)
            curr_count = yearly_mentions.get(year_introduced + 1, prev_count)
            
            # Growing trend = higher freshness
            if curr_count > prev_count:
                trend_score = 0.8
            else:
                trend_score = 0.4
        else:
            trend_score = 0.6
        
        # Apply decay for older introductions
        trend_score *= math.exp(-0.05 * years_since_intro)
        return max(0.0, min(1.0, trend_score))
    
    def calculate_freshness_score(self, 
                                 innovation: Dict,
                                 year: int,
                                 historical_data: List[Dict] = None) -> float:
        """
        Calculate overall freshness score (0-1)
        Combines recency, frequency, and trend scores
        
        Args:
            innovation: Innovation data dict
            year: Year of RJPP document
            historical_data: Historical innovations for comparison
        
        Returns:
            float: Freshness score between 0-1
        """
        if historical_data is None:
            historical_data = []
        
        # Calculate component scores
        recency = self.calculate_recency_score(year)
        
        # Count occurrences in history
        historical_count = sum(1 for item in historical_data 
                             if item.get('title', '').lower() == innovation.get('title', '').lower())
        frequency = self.calculate_frequency_score(historical_count)
        
        # Analyze trend
        yearly_mentions = {}
        for item in historical_data:
            item_year = item.get('year', year)
            yearly_mentions[item_year] = yearly_mentions.get(item_year, 0) + 1
        
        trend = self.calculate_trend_score(year, yearly_mentions)
        
        # Weighted combination
        freshness = (
            RECENCY_WEIGHT * recency +
            FREQUENCY_WEIGHT * frequency +
            TREND_WEIGHT * trend
        )
        
        return max(0.0, min(1.0, freshness))
    
    def categorize_freshness(self, score: float) -> str:
        """Categorize freshness score into levels"""
        if score >= 0.8:
            return "SANGAT FRESH"
        elif score >= 0.6:
            return "FRESH"
        elif score >= 0.4:
            return "CUKUP FRESH"
        else:
            return "KURANG FRESH"
    
    def get_freshness_report(self, innovations: List[Dict], year: int, historical_data: List[Dict] = None) -> List[Dict]:
        """Generate freshness report for list of innovations"""
        if historical_data is None:
            historical_data = []
        
        report = []
        for innovation in innovations:
            score = self.calculate_freshness_score(innovation, year, historical_data)
            category = self.categorize_freshness(score)
            
            report.append({
                'innovation': innovation.get('title', ''),
                'freshness_score': score,
                'freshness_category': category,
                'year': year,
                'recency': self.calculate_recency_score(year),
                'novelty_score': innovation.get('novelty_score', 0.0)
            })
        
        return sorted(report, key=lambda x: x['freshness_score'], reverse=True)
