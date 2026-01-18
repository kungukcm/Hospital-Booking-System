"""
Appointment Recommendation Engine
Analyzes TCN predictions to recommend optimal slots with congestion categorization
"""

import numpy as np
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from scheduling_model import SchedulingPredictor
import logging

# Set random seeds for deterministic predictions
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(42)
try:
    import tensorflow as tf
    tf.random.set_seed(42)
except ImportError:
    pass

logger = logging.getLogger(__name__)


class CongestionCategory:
    """Congestion level categories with color coding"""
    LOW = {
        'level': 'Low',
        'color': '🟢',
        'emoji': '✅',
        'description': 'Low congestion - minimal wait',
        'threshold_max': 15
    }
    MODERATE = {
        'level': 'Moderate',
        'color': '🟡',
        'emoji': '⚠️',
        'description': 'Moderate congestion - some wait',
        'threshold_min': 15,
        'threshold_max': 30
    }
    HIGH = {
        'level': 'High',
        'color': '🔴',
        'emoji': '❌',
        'description': 'High congestion - significant wait',
        'threshold_min': 30
    }
    
    @staticmethod
    def categorize(wait_time: float) -> Dict:
        """Categorize wait time into congestion level"""
        if wait_time <= CongestionCategory.LOW['threshold_max']:
            return CongestionCategory.LOW
        elif wait_time <= CongestionCategory.MODERATE['threshold_max']:
            return CongestionCategory.MODERATE
        else:
            return CongestionCategory.HIGH


class AppointmentRecommender:
    """
    Intelligent appointment slot recommender using TCN predictions
    """
    
    def __init__(self, model_path: str = "models/tcn_scheduling_model.h5"):
        """Initialize with TCN scheduling model"""
        self.predictor = SchedulingPredictor(
            model_path=model_path,
            framework='tensorflow'
        )
        logger.info("Appointment recommender initialized")
    
    def get_batch_predictions(
        self,
        appointment_type: str,
        date: datetime,
        time_slots: List[datetime] = None,
        interval_minutes: int = 30
    ) -> List[Dict]:
        """
        Get predictions for batch of time slots in a single day
        
        Args:
            appointment_type: Type of appointment
            date: Date to predict for
            time_slots: Specific times to predict (if None, generates 30-min intervals)
            interval_minutes: Interval between generated slots
        
        Returns:
            List of slots with predictions and categorization
        """
        if time_slots is None:
            # Generate 30-min intervals from 9 AM to 5 PM
            time_slots = []
            current = datetime.combine(date.date(), datetime.min.time()).replace(hour=9)
            end = datetime.combine(date.date(), datetime.min.time()).replace(hour=17)
            
            while current < end:
                time_slots.append(current)
                current += timedelta(minutes=interval_minutes)
        
        # Get predictions
        predictions = []
        for slot_time in time_slots:
            wait_time, confidence = self.predictor.predict_waiting_time(appointment_type, slot_time)
            congestion = CongestionCategory.categorize(wait_time)
            
            predictions.append({
                'time': slot_time.strftime('%H:%M'),
                'datetime': slot_time,
                'predicted_wait_minutes': round(wait_time, 1),
                'confidence': round(confidence, 2),
                'congestion_level': congestion['level'],
                'congestion_color': congestion['color'],
                'congestion_emoji': congestion['emoji'],
                'description': congestion['description']
            })
        
        return predictions
    
    def recommend_optimal_slots(
        self,
        appointment_type: str,
        date: datetime,
        num_recommendations: int = 5
    ) -> Tuple[List[Dict], Dict]:
        """
        Recommend optimal slots (lowest TAT) with alternatives
        
        Args:
            appointment_type: Type of appointment
            date: Date for appointment
            num_recommendations: Number of top recommendations
        
        Returns:
            Tuple of (recommended_slots, analytics)
        """
        # Get batch predictions
        batch = self.get_batch_predictions(appointment_type, date)
        
        # Sort by wait time
        sorted_slots = sorted(batch, key=lambda x: x['predicted_wait_minutes'])
        
        # Get recommendations
        recommended = sorted_slots[:num_recommendations]
        
        # Analyze congestion distribution
        analytics = self._analyze_batch(batch)
        
        return recommended, analytics
    
    def suggest_alternatives(
        self,
        appointment_type: str,
        preferred_datetime: datetime,
        num_alternatives: int = 3,
        max_wait_preference: float = None
    ) -> Dict:
        """
        If user selects a congested slot, suggest better alternatives
        
        Args:
            appointment_type: Type of appointment
            preferred_datetime: User's preferred time
            num_alternatives: Number of alternatives to suggest
            max_wait_preference: Max wait time user is willing to accept
        
        Returns:
            Dict with preferred slot analysis and alternatives
        """
        # Analyze preferred slot
        preferred_wait, preferred_conf = self.predictor.predict_waiting_time(
            appointment_type, preferred_datetime
        )
        preferred_congestion = CongestionCategory.categorize(preferred_wait)
        
        result = {
            'preferred': {
                'time': preferred_datetime.strftime('%H:%M'),
                'predicted_wait_minutes': round(preferred_wait, 1),
                'confidence': round(preferred_conf, 2),
                'congestion_level': preferred_congestion['level'],
                'congestion_emoji': preferred_congestion['emoji']
            },
            'recommendation': None,
            'alternatives': []
        }
        
        # If preferred is already low congestion, accept it
        if preferred_congestion['level'] == 'Low':
            result['recommendation'] = 'ACCEPT'
            result['message'] = "Great choice! This time has low congestion."
            return result
        
        # Get batch predictions for the day
        batch = self.get_batch_predictions(appointment_type, preferred_datetime)
        
        # Filter by congestion preference
        if max_wait_preference:
            better_slots = [s for s in batch if s['predicted_wait_minutes'] <= max_wait_preference]
        else:
            # Show low congestion slots
            better_slots = [s for s in batch if s['congestion_level'] == 'Low']
        
        # Sort by wait time
        better_slots = sorted(better_slots, key=lambda x: x['predicted_wait_minutes'])
        
        result['alternatives'] = better_slots[:num_alternatives]
        
        if result['alternatives']:
            best_alt = result['alternatives'][0]
            result['recommendation'] = 'SUGGEST_ALTERNATIVE'
            result['message'] = (
                f"Your preferred time has {preferred_congestion['level']} congestion "
                f"({preferred_wait:.0f} min wait). We recommend {best_alt['time']} "
                f"({best_alt['predicted_wait_minutes']:.0f} min wait) instead."
            )
        else:
            result['recommendation'] = 'NO_BETTER_OPTION'
            result['message'] = (
                f"No better options available. Your preferred time has "
                f"{preferred_wait:.0f} min predicted wait."
            )
        
        return result
    
    def get_least_busy_slots(
        self,
        appointment_type: str,
        date: datetime,
        num_slots: int = 5
    ) -> List[Dict]:
        """Get slots with lowest predicted waiting times"""
        batch = self.get_batch_predictions(appointment_type, date)
        sorted_slots = sorted(batch, key=lambda x: x['predicted_wait_minutes'])
        return sorted_slots[:num_slots]
    
    def get_busiest_slots(
        self,
        appointment_type: str,
        date: datetime,
        num_slots: int = 5
    ) -> List[Dict]:
        """Get slots with highest predicted waiting times (to avoid)"""
        batch = self.get_batch_predictions(appointment_type, date)
        sorted_slots = sorted(batch, key=lambda x: x['predicted_wait_minutes'], reverse=True)
        return sorted_slots[:num_slots]
    
    def _analyze_batch(self, batch: List[Dict]) -> Dict:
        """Analyze congestion statistics for batch of slots"""
        waits = [s['predicted_wait_minutes'] for s in batch]
        
        low_congestion = [s for s in batch if s['congestion_level'] == 'Low']
        moderate = [s for s in batch if s['congestion_level'] == 'Moderate']
        high = [s for s in batch if s['congestion_level'] == 'High']
        
        return {
            'total_slots': len(batch),
            'avg_wait_time': round(np.mean(waits), 1),
            'min_wait_time': round(np.min(waits), 1),
            'max_wait_time': round(np.max(waits), 1),
            'std_dev': round(np.std(waits), 1),
            'low_congestion_slots': len(low_congestion),
            'moderate_congestion_slots': len(moderate),
            'high_congestion_slots': len(high),
            'availability_score': round((len(low_congestion) / len(batch)) * 100, 1)
        }
    
    def generate_slot_display(self, slots: List[Dict]) -> str:
        """Generate formatted display of recommended slots"""
        display = "📅 **Recommended Appointment Slots:**\n\n"
        
        for i, slot in enumerate(slots, 1):
            display += (
                f"{i}. {slot['congestion_emoji']} **{slot['time']}** - "
                f"{slot['congestion_color']} {slot['congestion_level']}\n"
                f"   ⏱️ Est. wait: {slot['predicted_wait_minutes']:.0f} min "
                f"(confidence: {slot['confidence']*100:.0f}%)\n\n"
            )
        
        return display


# Global recommender instance
_recommender = None


def get_recommender() -> AppointmentRecommender:
    """Get or create singleton recommender instance"""
    global _recommender
    if _recommender is None:
        _recommender = AppointmentRecommender()
    return _recommender
