# Download TCN Model from Google Colab

## Step 1: Export Model from Colab

In your Google Colab notebook, add this code at the end:

```python
# Save your trained TensorFlow model
model.save('tcn_scheduling_model.h5')

# Or if using TensorFlow 2.x SavedModel format:
model.save('tcn_scheduling_model')

# Download to your computer
from google.colab import files
files.download('tcn_scheduling_model.h5')
```

## Step 2: Upload to GitHub

Once downloaded to your computer:

```bash
# Create models directory
mkdir models

# Move model to directory
mv tcn_scheduling_model.h5 models/

# Commit and push to GitHub
git add models/tcn_scheduling_model.h5
git commit -m "Add trained TCN scheduling model"
git push origin main
```

**Or** use GitHub's web interface to upload the file directly.

## Step 3: Streamlit Cloud Setup

When you deploy to Streamlit Cloud:
1. Your model will be automatically downloaded from GitHub
2. Placed in `models/` folder
3. Loaded on first app startup

## Alternative: Use Colab Drive

If file is too large for GitHub:

```python
# In Colab: Mount and save to Drive
from google.colab import drive
drive.mount('/content/drive')

# Save model to Drive
model.save('/content/drive/My Drive/Hospital Booking/tcn_model.h5')
```

Then in your app:
```python
# Use google-colab auth
from google.colab import drive
drive.mount('/content/drive')
model_path = '/content/drive/My Drive/Hospital Booking/tcn_model.h5'
```

## Expected Model Output Format

Your model should output recommended slots. Example:

### Input:
```python
{
    'appointment_type': 'consultation',
    'date': '2026-01-22',
    'num_recommendations': 5
}
```

### Output:
```python
[
    {
        'time': '09:00',
        'predicted_wait_minutes': 15.5,
        'confidence': 0.85
    },
    {
        'time': '09:30',
        'predicted_wait_minutes': 18.0,
        'confidence': 0.85
    },
    # ... more slots
]
```

## Model Input Shape (Common)

If your model expects:
- Input: `[batch_size, sequence_length, num_features]`
- Example: `[1, 24, 10]` - one sample, 24 hours, 10 features

The `scheduling_model.py` will handle feature extraction automatically.

## Next: Configure in System

Once you have the model file, update:

```python
# In app.py or settings
TCN_MODEL_PATH = "models/tcn_scheduling_model.h5"
TCN_FRAMEWORK = "tensorflow"  # Important!

# Initialize
from scheduling_model import SchedulingPredictor
predictor = SchedulingPredictor(
    model_path=TCN_MODEL_PATH,
    framework="tensorflow"
)
```

---

**Ready to integrate!** Let me know when you have the model downloaded.
