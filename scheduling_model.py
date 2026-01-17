"""
Scheduling Model Integration
Integrates TCN-based scheduling system with Hospital Booking System
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, List, Dict
import json
import logging

logger = logging.getLogger(__name__)


class SchedulingPredictor:
    """
    Wrapper for TCN scheduling model
    Predicts waiting times and recommends optimal booking slots
    """
    
    def __init__(self, model_path: str = None, use_mock: bool = False, framework: str = "auto"):
        """
        Initialize scheduling predictor
        
        Args:
            model_path: Path to trained TCN model
            use_mock: Use mock predictions if model not available (for testing)
            framework: 'pytorch', 'tensorflow', 'auto' (default)
        """
        self.model_path = model_path
        self.model = None
        self.use_mock = use_mock
        self.scaler = None
        self.framework = framework
        
        if model_path:
            try:
                self.load_model(model_path, framework=framework)
                self.use_mock = False
                logger.info(f"TCN model loaded successfully from {model_path}")
            except Exception as e:
                logger.warning(f"Failed to load TCN model from {model_path}: {e}. Using mock predictions.")
                self.use_mock = True
        else:
            logger.info("No model path provided. Using mock predictions.")
    
    def load_model(self, model_path: str, framework: str = "auto"):
        """
        Load trained TCN model
        Supports PyTorch (.pth), TensorFlow (.h5/.pb), SavedModel, and pickle formats
        
        Args:
            model_path: Path to model file or directory
            framework: 'pytorch', 'tensorflow', 'auto' (default)
        """
        try:
            if framework == "auto":
                if model_path.endswith('.pth'):
                    framework = "pytorch"
                elif model_path.endswith(('.h5', '.pb')) or model_path.endswith('saved_model.pb'):
                    framework = "tensorflow"
                else:
                    framework = "tensorflow"  # Default to TensorFlow
            
            if framework.lower() == "pytorch":
                import torch
                self.model = torch.load(model_path, map_location='cpu')
                self.model.eval()
                logger.info("PyTorch model loaded")
            
            elif framework.lower() == "tensorflow":
                from tensorflow import keras
                try:
                    # Try loading as SavedModel (directory)
                    self.model = keras.models.load_model(model_path)
                except:
                    # Fallback to .h5 file
                    self.model = keras.models.load_model(model_path)
                logger.info("TensorFlow model loaded")
                self.framework = "tensorflow"
            
            elif framework.lower() in ["pickle", "pkl"]:
                import pickle
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info("Pickle model loaded")
            
            else:
                raise ValueError(f"Unsupported framework: {framework}")
        
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def extract_features(self, appointment_type: str, appointment_datetime: datetime) -> np.ndarray:
        """
        Extract features from appointment info for model prediction
        
        Args:
            appointment_type: Type of appointment (e.g., 'consultation', 'surgery')
            appointment_datetime: Requested appointment datetime
        
        Returns:
            Feature vector for model prediction
        """
        features = []
        
        # Temporal features
        features.append(appointment_datetime.hour)  # Hour of day (0-23)
        features.append(appointment_datetime.weekday())  # Day of week (0-6)
        features.append(appointment_datetime.day)  # Day of month
        features.append(appointment_datetime.month)  # Month
        
        # Encode appointment type
        appointment_types = {
            'consultation': 0,
            'checkup': 1,
            'emergency': 2,
            'surgery': 3,
            'follow-up': 4
        }
        features.append(appointment_types.get(appointment_type.lower(), 0))
        
        # Add cyclical encoding for time (sine/cosine)
        hour_sin = np.sin(2 * np.pi * appointment_datetime.hour / 24)
        hour_cos = np.cos(2 * np.pi * appointment_datetime.hour / 24)
        day_sin = np.sin(2 * np.pi * appointment_datetime.weekday() / 7)
        day_cos = np.cos(2 * np.pi * appointment_datetime.weekday() / 7)
        
        features.extend([hour_sin, hour_cos, day_sin, day_cos])
        
        return np.array(features, dtype=np.float32)
    
    def predict_waiting_time(self, appointment_type: str, appointment_datetime: datetime) -> Tuple[float, float]:
        """
        Predict waiting time for a given appointment
        
        Args:
            appointment_type: Type of appointment
            appointment_datetime: Requested appointment datetime
        
        Returns:
            Tuple of (predicted_waiting_time_minutes, confidence_score)
        """
        if self.use_mock:
            return self._mock_predict(appointment_type, appointment_datetime)
        
        try:
            features = self.extract_features(appointment_type, appointment_datetime)
            features = np.expand_dims(features, axis=0)  # Add batch dimension
            
            # Make prediction
            if self.model.__class__.__module__.startswith('torch'):
                import torch
                with torch.no_grad():
                    features_tensor = torch.from_numpy(features).float()
                    prediction = self.model(features_tensor)
                    waiting_time = prediction.item()
            else:
                # TensorFlow or other framework
                prediction = self.model.predict(features, verbose=0)
                waiting_time = float(prediction[0][0])
            
            # Ensure reasonable bounds
            waiting_time = max(5, min(240, waiting_time))  # 5 to 240 minutes
            confidence = self._calculate_confidence(appointment_datetime)
            
            return waiting_time, confidence
        
        except Exception as e:
            logger.error(f"Error predicting waiting time: {e}")
            return self._mock_predict(appointment_type, appointment_datetime)
    
    def _mock_predict(self, appointment_type: str, appointment_datetime: datetime) -> Tuple[float, float]:
        """
        Generate mock predictions for testing (when model unavailable)
        In production, this will be replaced with actual model predictions
        """
        hour = appointment_datetime.hour
        day_of_week = appointment_datetime.weekday()
        
        # Mock logic: busier during business hours and weekdays
        base_wait = 20  # minutes
        
        # Peak hours: 9-12, 14-16
        if 9 <= hour < 12 or 14 <= hour < 16:
            base_wait += 30
        elif 12 <= hour < 14:  # Lunch rush
            base_wait += 25
        elif hour < 9 or hour >= 17:  # Off-hours
            base_wait -= 10
        
        # Weekday vs weekend
        if day_of_week < 5:  # Weekday
            base_wait += 15
        else:  # Weekend
            base_wait -= 10
        
        # Add type-specific wait time
        type_multipliers = {
            'consultation': 1.0,
            'checkup': 0.8,
            'emergency': 1.5,
            'surgery': 2.0,
            'follow-up': 0.6
        }
        multiplier = type_multipliers.get(appointment_type.lower(), 1.0)
        base_wait *= multiplier
        
        # Add some randomness
        base_wait += np.random.normal(0, 5)
        base_wait = max(5, min(240, base_wait))
        
        confidence = 0.75 + np.random.uniform(-0.1, 0.1)
        
        return base_wait, confidence
    
    def _calculate_confidence(self, appointment_datetime: datetime) -> float:
        """Calculate confidence score based on prediction freshness"""
        now = datetime.now()
        days_ahead = (appointment_datetime - now).days
        
        # Higher confidence for nearer predictions
        if days_ahead <= 7:
            confidence = 0.85
        elif days_ahead <= 30:
            confidence = 0.75
        else:
            confidence = 0.65
        
        return confidence
    
    def recommend_optimal_slots(
        self, 
        appointment_type: str, 
        date: datetime,
        num_recommendations: int = 5,
        slot_duration_minutes: int = 30
    ) -> List[Dict]:
        """
        Recommend optimal appointment slots that minimize waiting time
        
        Supports two modes:
        1. Direct model output: If your TCN outputs recommended slots directly
        2. Predicted waiting times: If using per-slot predictions
        
        Args:
            appointment_type: Type of appointment
            date: Date to recommend slots for
            num_recommendations: Number of slots to recommend
            slot_duration_minutes: Duration between slots
        
        Returns:
            List of recommended slots with waiting time predictions
        """
        if self.use_mock:
            return self._mock_recommend_slots(appointment_type, date, num_recommendations)
        
        try:
            # Try direct model output first (your TensorFlow model output)
            slots = self._get_model_recommendations(appointment_type, date, num_recommendations)
            if slots:
                return slots
        except Exception as e:
            logger.warning(f"Failed to get direct model recommendations: {e}")
        
        # Fallback to per-slot prediction
        return self._predict_per_slot_recommendations(appointment_type, date, num_recommendations, slot_duration_minutes)
    
    def _get_model_recommendations(self, appointment_type: str, date: datetime, num_recommendations: int) -> List[Dict]:
        """
        Get recommendations directly from your TCN model
        Expected model output format:
        [
            {'time': '09:00', 'predicted_wait_minutes': 15.5, 'confidence': 0.85},
            {'time': '09:30', 'predicted_wait_minutes': 18.0, 'confidence': 0.85},
            ...
        ]
        """
        features = self.extract_features(appointment_type, datetime.combine(date, datetime.min.time()).replace(hour=9))
        features = np.expand_dims(features, axis=0)
        
        if self.framework == "tensorflow":
            # TensorFlow model - returns recommended slots
            predictions = self.model.predict(features, verbose=0)
            
            # Parse model output (adjust based on your model's output structure)
            formatted_slots = []
            if isinstance(predictions, (list, tuple)):
                # Model outputs list of slot recommendations
                for i, pred in enumerate(predictions[:num_recommendations], 1):
                    if isinstance(pred, dict):
                        slot = pred
                    else:
                        # Convert numpy array to slot dict
                        slot = {
                            'time': f"{int(pred[0]):02d}:{int((pred[0] % 1) * 60):02d}",
                            'predicted_wait_minutes': float(pred[1]) if len(pred) > 1 else 20.0,
                            'confidence': float(pred[2]) if len(pred) > 2 else 0.8
                        }
                    
                    # Create datetime object
                    time_parts = slot['time'].split(':')
                    slot_datetime = datetime.combine(date, datetime.min.time()).replace(
                        hour=int(time_parts[0]),
                        minute=int(time_parts[1])
                    )
                    
                    formatted_slots.append({
                        'rank': i,
                        'time': slot['time'],
                        'datetime': slot_datetime,
                        'predicted_wait_minutes': slot.get('predicted_wait_minutes', 20.0),
                        'confidence': slot.get('confidence', 0.8),
                        'score': slot.get('predicted_wait_minutes', 20.0),
                        'recommendation': f"Rank {i}: {slot['time']} - Est. wait: {slot.get('predicted_wait_minutes', 20):.0f} min (confidence: {slot.get('confidence', 0.8)*100:.0f}%)"
                    })
            else:
                # Model outputs array of slots
                if hasattr(predictions, 'shape') and len(predictions.shape) > 1:
                    for i in range(min(num_recommendations, predictions.shape[0])):
                        pred = predictions[i]
                        hour = int(pred[0]) if len(pred) > 0 else 9 + i
                        minute = int((pred[0] % 1) * 60) if len(pred) > 0 else 0
                        wait = float(pred[1]) if len(pred) > 1 else 20.0
                        conf = float(pred[2]) if len(pred) > 2 else 0.8
                        
                        slot_datetime = datetime.combine(date, datetime.min.time()).replace(hour=hour, minute=minute)
                        
                        formatted_slots.append({
                            'rank': i + 1,
                            'time': f"{hour:02d}:{minute:02d}",
                            'datetime': slot_datetime,
                            'predicted_wait_minutes': wait,
                            'confidence': conf,
                            'score': wait,
                            'recommendation': f"Rank {i+1}: {hour:02d}:{minute:02d} - Est. wait: {wait:.0f} min (confidence: {conf*100:.0f}%)"
                        })
            
            return formatted_slots
        
        return []
    
    def _predict_per_slot_recommendations(
        self, 
        appointment_type: str, 
        date: datetime, 
        num_recommendations: int,
        slot_duration_minutes: int
    ) -> List[Dict]:
        """
        Fallback: Generate recommendations by predicting each slot
        """
        # Generate candidate time slots (9 AM to 5 PM)
        candidate_slots = []
        current_time = datetime.combine(date, datetime.min.time()).replace(hour=9)
        end_time = datetime.combine(date, datetime.min.time()).replace(hour=17)
        
        while current_time < end_time:
            candidate_slots.append(current_time)
            current_time += timedelta(minutes=slot_duration_minutes)
        
        # Predict waiting time for each slot
        slot_predictions = []
        for slot_time in candidate_slots:
            wait_time, confidence = self.predict_waiting_time(appointment_type, slot_time)
            slot_predictions.append({
                'time': slot_time,
                'waiting_time_minutes': round(wait_time, 1),
                'confidence': round(confidence, 2),
                'score': wait_time
            })
        
        # Sort by predicted waiting time (ascending)
        optimal_slots = sorted(slot_predictions, key=lambda x: x['score'])[:num_recommendations]
        
        # Format for display
        formatted_slots = []
        for i, slot in enumerate(optimal_slots, 1):
            formatted_slots.append({
                'rank': i,
                'time': slot['time'].strftime('%H:%M'),
                'datetime': slot['time'],
                'predicted_wait_minutes': slot['waiting_time_minutes'],
                'confidence': slot['confidence'],
                'recommendation': f"Rank {i}: {slot['time'].strftime('%H:%M')} - Est. wait: {slot['waiting_time_minutes']:.0f} min (confidence: {slot['confidence']})"
            })
        
        return formatted_slots
    
    def _mock_recommend_slots(self, appointment_type: str, date: datetime, num_recommendations: int) -> List[Dict]:
        """Generate mock recommendations for testing"""
        formatted_slots = []
        hour = 9
        
        for i in range(num_recommendations):
            slot_time = datetime.combine(date, datetime.min.time()).replace(hour=hour, minute=0)
            wait_time, confidence = self._mock_predict(appointment_type, slot_time)
            
            formatted_slots.append({
                'rank': i + 1,
                'time': f"{hour:02d}:00",
                'datetime': slot_time,
                'predicted_wait_minutes': round(wait_time, 1),
                'confidence': round(confidence, 2),
                'recommendation': f"Rank {i+1}: {hour:02d}:00 - Est. wait: {wait_time:.0f} min (confidence: {confidence*100:.0f}%)"
            })
            
            hour += 1
            if hour >= 17:
                hour = 9  # Loop back
        
        return formatted_slots
    
    def get_busiest_times(self, appointment_type: str, date: datetime) -> List[str]:
        """Get busiest (highest waiting time) appointment times"""
        slots = self.recommend_optimal_slots(
            appointment_type, date, 
            num_recommendations=24,  # Get all slots
            slot_duration_minutes=60
        )
        
        # Reverse sort to get busiest times
        busiest = sorted(slots, key=lambda x: x['predicted_wait_minutes'], reverse=True)[:5]
        return [f"{s['time']} ({s['predicted_wait_minutes']:.0f} min wait)" for s in busiest]
    
    def get_least_busy_times(self, appointment_type: str, date: datetime) -> List[str]:
        """Get least busy (lowest waiting time) appointment times"""
        slots = self.recommend_optimal_slots(appointment_type, date, num_recommendations=5)
        return [s['recommendation'] for s in slots]


# Global instance
_predictor = None


def get_predictor(model_path: str = None) -> SchedulingPredictor:
    """Get or create global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = SchedulingPredictor(model_path=model_path)
    return _predictor


def predict_wait_time(appointment_type: str, appointment_datetime: datetime) -> str:
    """
    Convenience function to predict wait time
    Returns human-readable string
    """
    predictor = get_predictor()
    wait_time, confidence = predictor.predict_waiting_time(appointment_type, appointment_datetime)
    return f"Estimated wait: {wait_time:.0f} minutes (confidence: {confidence*100:.0f}%)"


def recommend_best_times(appointment_type: str, date: datetime) -> str:
    """
    Convenience function to get best appointment times
    Returns formatted string with recommendations
    """
    predictor = get_predictor()
    slots = predictor.recommend_optimal_slots(appointment_type, date)
    
    result = f"🏥 Best appointment times for {date.strftime('%B %d, %Y')}:\n\n"
    for slot in slots:
        result += f"{slot['recommendation']}\n"
    
    return result


# Example usage
if __name__ == "__main__":
    # Test the predictor
    predictor = SchedulingPredictor(use_mock=True)
    
    # Example 1: Predict waiting time
    test_time = datetime(2026, 1, 20, 10, 0)  # 10 AM on Jan 20
    wait, conf = predictor.predict_waiting_time('consultation', test_time)
    print(f"Wait time at {test_time}: {wait:.1f} min (confidence: {conf:.2f})")
    
    # Example 2: Get optimal slots
    test_date = datetime(2026, 1, 20).date()
    optimal_slots = predictor.recommend_optimal_slots('consultation', test_date)
    print("\nOptimal slots:")
    for slot in optimal_slots:
        print(f"  {slot['recommendation']}")
    
    # Example 3: Convenience functions
    print("\n" + recommend_best_times('checkup', datetime.now().date()))
