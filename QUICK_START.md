# Hospital Booking System - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Get Your Groq API Key
1. Visit https://console.groq.com
2. Sign up or log in
3. Create an API key
4. Copy your API key

### Step 2: Setup Local Environment

```bash
# Navigate to project directory
cd "path/to/Hospital Booking System"

# Create virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# Create virtual environment (macOS/Linux)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure API Key

**Option A - Using .env file (Recommended for local development):**
```bash
# Create or edit .env file
# Add your API key:
GROQ_API_KEY=your_groq_api_key_here
```

**Option B - Environment variable (Windows):**
```powershell
$env:GROQ_API_KEY = "your_groq_api_key_here"
```

**Option B - Environment variable (macOS/Linux):**
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will open automatically at `http://localhost:8501`

---

## 📝 Using the Application

### Chat Interface (Left Panel)
- Type your appointment requests in natural language
- The AI assistant will understand and help you with:
  - **Booking appointments**: "I want to book a doctor's appointment on January 20th at 2 PM"
  - **Checking availability**: "What's the next available time?"
  - **Canceling appointments**: "Cancel my appointment on January 15th"

### Debug Panel (Right Panel)
- View session state contents
- See booked appointments
- Manually create appointments using the form

---

## 🐳 Using Docker (Optional)

### Quick Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or use Docker directly
docker build -t hospital-booking .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key hospital-booking
```

---

## ☁️ Deploy to Cloud (Choose One)

### Option 1: Streamlit Cloud (Easiest)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/Hospital-Booking-System
   git push -u origin main
   ```

2. **Deploy:**
   - Go to https://streamlit.io/cloud
   - Click "New app" → Select your repository
   - Choose `main` branch and `app.py`
   - Deploy!

3. **Add API Key:**
   - Go to App settings → Secrets
   - Add: `GROQ_API_KEY = "your_key"`

### Option 2: AWS EC2

```bash
# 1. Launch Ubuntu instance
# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-ip

# 3. Setup on instance
sudo apt-get update && sudo apt-get install -y python3-pip python3-venv git
git clone https://github.com/YOUR_USERNAME/Hospital-Booking-System
cd Hospital-Booking-System
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Create .env with your API key
nano .env

# 5. Run with systemd service (for persistence)
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Option 3: Heroku

```bash
# 1. Install Heroku CLI
# 2. Login
heroku login

# 3. Create app
heroku create your-app-name

# 4. Set environment variable
heroku config:set GROQ_API_KEY="your_key"

# 5. Deploy
git push heroku main
```

### Option 4: Google Cloud Run

```bash
# Build and push Docker image
docker build -t gcr.io/YOUR_PROJECT/hospital-booking .
docker push gcr.io/YOUR_PROJECT/hospital-booking

# Deploy
gcloud run deploy hospital-booking \
  --image gcr.io/YOUR_PROJECT/hospital-booking \
  --platform managed \
  --region us-central1 \
  --set-env-vars GROQ_API_KEY=your_key
```

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| "GROQ_API_KEY is not set" | Check `.env` file exists and has valid key |
| Port 8501 already in use | Run: `streamlit run app.py --server.port 8502` |
| Module not found error | Ensure venv is activated and `pip install -r requirements.txt` was run |
| Docker won't start | Check `.env` file is in project root |
| Cloud deployment fails | Ensure all files are committed to git (except `.env`) |

---

## 📚 Project Structure

```
Hospital Booking System/
├── app.py                 # Main Streamlit app
├── agent.py               # AI agent logic
├── tools.py               # Booking tools
├── config.py              # Configuration
├── constants.py           # Constants
├── utils.py               # Utility functions
├── logger.py              # Logging setup
├── requirements.txt       # Python dependencies
├── .env                   # API keys (don't commit!)
├── .env.example           # Example env file
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Docker Compose config
├── Procfile               # Heroku deployment
├── runtime.txt            # Python version for Heroku
├── DEPLOYMENT.md          # Detailed deployment guide
├── design_docs/           # Architecture diagrams
└── README.md              # Project documentation
```

---

## 🎓 Next Steps

1. **Customize the AI prompt**: Edit the `CALLER_PA_PROMPT` in `settings.yaml`
2. **Add database**: Integrate PostgreSQL for persistent appointments
3. **Add authentication**: Implement user login/authentication
4. **Custom branding**: Modify colors and UI in `.streamlit/config.toml`
5. **API backend**: Use FastAPI (already installed) to create a REST API

---

## 📞 Support

- Check `app.log` for error messages
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for detailed options
- Visit [Streamlit Docs](https://docs.streamlit.io)
- Check [Groq API Docs](https://console.groq.com)

---

## ✅ What's Included

✅ AI-powered appointment booking system  
✅ Real-time chat interface  
✅ Session management  
✅ Docker support  
✅ Multiple deployment options  
✅ Comprehensive logging  
✅ Production-ready code  

Happy deploying! 🎉
