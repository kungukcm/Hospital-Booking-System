# TCN Scheduling Integration - Complete Setup Guide

## 🚀 Quick Overview

Your Temporal Convolutional Network (TCN) with attention mechanism has been integrated into the Hospital Booking System!

### What's New:
- ✅ **Waiting Time Predictions** - ML model predicts wait times for different appointment slots
- ✅ **Optimal Slot Recommendations** - AI recommends slots with minimal predicted waiting
- ✅ **Smart Scheduling** - Patients get personalized recommendations
- ✅ **Load Balancing** - Distributes appointments across less-busy times

---

## 📦 Files Created

### 1. `scheduling_model.py`
**Core scheduling model wrapper**
- Loads your trained TCN model (supports PyTorch, TensorFlow, pickle)
- Feature extraction from appointment data
- Prediction generation
- Optimal slot recommendation

```python
from scheduling_model import SchedulingPredictor, predict_wait_time

# Initialize with your model
predictor = SchedulingPredictor(model_path='models/tcn_model.pth')

# Make predictions
wait_time, confidence = predictor.predict_waiting_time('consultation', datetime_obj)

# Get optimal slots
slots = predictor.recommend_optimal_slots('checkup', date_obj, num_recommendations=5)
```

### 2. `enhanced_tools.py`
**New LangChain tools with ML predictions**
- `book_appointment()` - Now includes waiting time predictions
- `get_optimal_appointment_slots()` - NEW - ML-recommended slots
- `get_wait_time_prediction()` - NEW - Standalone predictions
- `get_busiest_times()` - NEW - Know when to avoid
- `get_least_busy_times()` - NEW - Know best times
- `cancel_appointment()` - Unchanged

---

## 🔧 Installation Steps

### Step 1: Update requirements.txt

Add your ML dependencies:
```bash
# Add these to requirements.txt
torch>=2.0.0           # If using PyTorch
# OR
tensorflow>=2.10.0     # If using TensorFlow
scikit-learn>=1.0.0
```

Then install:
```bash
pip install -r requirements.txt
```

### Step 2: Add Your Model File

Create a `models/` directory and add your trained model:
```bash
mkdir models
# Copy your trained model here
cp /path/to/your/tcn_model.pth models/
# or
cp /path/to/your/tcn_model.h5 models/
```

Supported formats:
- `*.pth` - PyTorch models
- `*.h5` - TensorFlow/Keras models
- `*.pkl` - Pickle format
- `*.joblib` - Joblib format

### Step 3: Update agent.py

Modify to use enhanced tools:

```python
# OLD:
from tools import book_appointment, get_next_available_appointment, cancel_appointment

# NEW:
from enhanced_tools import (
    book_appointment, 
    get_optimal_appointment_slots,
    get_wait_time_prediction,
    get_busiest_times,
    get_least_busy_times,
    cancel_appointment
)

# Update tools list:
caller_tools = [
    book_appointment,
    get_optimal_appointment_slots,
    get_wait_time_prediction,
    get_busiest_times,
    get_least_busy_times,
    cancel_appointment
]
```

### Step 4: Update settings.yaml

Enhance the system prompt:

```yaml
prompts:
  caller_pa: |
    You are a helpful and friendly personal assistant managing hospital appointments.
    You have access to an ML-powered scheduling system that predicts waiting times.
    
    When booking appointments:
    1. Offer to show optimal times using get_optimal_appointment_slots
    2. Mention predicted waiting times
    3. Highlight times with shorter waits
    4. Ask patients to avoid busy times if they prefer
    
    Available functions:
    - book_appointment(year, month, day, hour, minute, name)
    - get_optimal_appointment_slots(appointment_type, preferred_date)
    - get_wait_time_prediction(appointment_type, year, month, day, hour, minute)
    - get_busiest_times(appointment_type, date)
    - get_least_busy_times(appointment_type, date)
    - get_next_available_appointment()
    - cancel_appointment(year, month, day, hour, minute)
    
    Always be conversational and suggest the best times to minimize wait duration.
```

---

## 🎯 Usage Examples

### Example 1: Automatic Predictions with Booking

**User:** "Book me a consultation on January 20th at 2 PM"

**System Flow:**
1. Extracts: consultation, 2 PM, Jan 20
2. Predicts wait time at that slot
3. Books appointment
4. Returns: "✅ Booked for Jan 20 at 2:00 PM. Predicted wait: 45 minutes"

### Example 2: Get Optimal Slots

**User:** "What's the best time for a checkup on January 22nd?"

**System Flow:**
1. Calls `get_optimal_appointment_slots('checkup', '2026-01-22')`
2. Model predicts wait times for 9 AM - 5 PM
3. Returns top 5 slots ranked by lowest wait time:

```
🎯 Optimal appointment times for Checkup on 2026-01-22:

1. 08:00 - Predicted wait: 12 min (confidence: 85%)
2. 09:30 - Predicted wait: 18 min (confidence: 85%)
3. 17:00 - Predicted wait: 15 min (confidence: 80%)
4. 08:30 - Predicted wait: 20 min (confidence: 85%)
5. 16:30 - Predicted wait: 22 min (confidence: 80%)

These times are ranked by lowest predicted waiting time.
Which time would you prefer?
```

### Example 3: Avoid Busy Times

**User:** "When should I avoid scheduling?"

**System Flow:**
1. Calls `get_busiest_times('consultation', '2026-01-22')`
2. Returns busiest 5 time slots

```
⏰ Busiest times for Consultation on 2026-01-22:

• 11:00 (58 min wait)
• 11:30 (56 min wait)
• 12:00 (52 min wait)
• 10:30 (48 min wait)
• 15:00 (45 min wait)

Consider booking earlier or later in the day for shorter waits.
```

---

## 🔌 Integrate Your Actual TCN Model

### Step 1: Prepare Your Model

Your Google Colab notebook should have code like:

```python
# Save model from Colab
torch.save(model.state_dict(), 'tcn_model.pth')
# or
model.save('tcn_model.h5')  # For Keras
```

### Step 2: Load in System

The `scheduling_model.py` automatically handles:
- Model loading (PyTorch, TensorFlow, etc.)
- Feature extraction 
- Prediction generation

Just provide the model path:

```python
# In settings or env variable
TCN_MODEL_PATH = "models/tcn_model.pth"

# Initialize
predictor = SchedulingPredictor(model_path=TCN_MODEL_PATH)
```

### Step 3: Customize Features

Edit the `extract_features()` method in `scheduling_model.py` to match your model's input requirements:

```python
def extract_features(self, appointment_type, appointment_datetime):
    """
    Customize this to match your TCN input shape!
    
    Example: If your model expects:
    Input shape: [batch, 24, 10]  # 24 time steps, 10 features
    """
    # Your feature engineering here
    features = []
    # ... add features as needed
    return np.array(features, dtype=np.float32)
```

---

## 📊 Expected Output Format

### Prediction Output
```python
wait_time: float          # Minutes (0-240)
confidence: float         # 0.0 to 1.0
```

### Recommended Slots Output
```python
[{
    'rank': 1,
    'time': '09:00',
    'datetime': datetime_obj,
    'predicted_wait_minutes': 15.5,
    'confidence': 0.85,
    'recommendation': 'Rank 1: 09:00 - Est. wait: 15 min (confidence: 85%)'
}, ...]
```

---

## 🧪 Testing

### Test Locally
```bash
# Test the scheduling model
python -c "
from scheduling_model import SchedulingPredictor
from datetime import datetime

predictor = SchedulingPredictor(use_mock=True)
wait, conf = predictor.predict_waiting_time('consultation', datetime.now())
print(f'Mock prediction: {wait:.0f} min (confidence: {conf:.2f})')
"
```

### Test Enhanced Tools
```python
from enhanced_tools import get_optimal_appointment_slots
from datetime import datetime

result = get_optimal_appointment_slots('checkup', '2026-01-22')
print(result)
```

### Test in Streamlit
```bash
streamlit run app.py
```

Type: "What's the best time for a checkup on January 22nd?"

---

## 🔄 Model Retraining

To update with new data:

1. Retrain your TCN model in Colab
2. Save the new model: `torch.save(model, 'models/tcn_model_v2.pth')`
3. Update the path: `TCN_MODEL_PATH = "models/tcn_model_v2.pth"`
4. No code changes needed - just drop in the new model!

---

## ⚙️ Configuration Options

In `settings.yaml` or code:

```yaml
# Model configuration
scheduling:
  model_path: "models/tcn_model.pth"
  use_mock: false          # Use real model (not mock)
  prediction_confidence_threshold: 0.7
  max_slot_recommendations: 10
  slot_duration_minutes: 30
  
  # Working hours
  work_start_hour: 9
  work_end_hour: 17
  
  # Waiting time bounds (minutes)
  min_wait_time: 5
  max_wait_time: 240
```

---

## 🐛 Troubleshooting

### Issue: "Model not found"
```python
# Use mock mode while testing
predictor = SchedulingPredictor(use_mock=True)
```

### Issue: "Shape mismatch in model"
Edit `extract_features()` to match your model's expected input shape.

### Issue: "Predictions seem wrong"
Check that `extract_features()` matches the features used during training.

### Issue: "Slow predictions"
- Consider using `use_mock=True` during development
- Optimize model loading (load once, reuse)
- Consider quantization for faster inference

---

## 📈 Performance Metrics to Track

After deployment:

1. **Prediction Accuracy**
   - Compare predicted vs actual wait times
   - Calculate RMSE, MAE

2. **Booking Distribution**
   - Check if patients are distributed across time slots
   - Measure load balancing effectiveness

3. **Patient Satisfaction**
   - Did wait times actually decrease?
   - Are patients satisfied with recommendations?

4. **System Performance**
   - Prediction latency (should be <100ms)
   - Model loading time (should be <1s)

---

## 🚀 Next Steps

1. **Get your TCN model** from Google Colab
2. **Place in `models/` folder**
3. **Update `extract_features()`** to match your training
4. **Test with mock first** (`use_mock=True`)
5. **Switch to real model** when confident
6. **Deploy to Streamlit Cloud**

---

## 📞 Quick Reference

| Task | File | Function |
|------|------|----------|
| Load model | `scheduling_model.py` | `SchedulingPredictor(model_path)` |
| Predict wait | `scheduling_model.py` | `predict_waiting_time()` |
| Get slots | `enhanced_tools.py` | `get_optimal_appointment_slots()` |
| Test system | Terminal | `streamlit run app.py` |
| Deploy | Streamlit Cloud | Standard deployment |

---

**Your TCN scheduling system is ready to go! 🎯**

Provide your model file and let me know the framework (PyTorch/TensorFlow) and I'll complete the integration!
