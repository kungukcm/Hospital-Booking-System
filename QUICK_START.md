# Hospital Chat Assistant - Quick Start Guide 🚀

## Status: ✅ KNOWLEDGE BASE READY

Your hospital chat assistant now has:
- ✅ 21 hospital documents indexed
- ✅ Hospital website content scraped
- ✅ Semantic search enabled
- ✅ Appointment booking (still works!)

---

## Get Started in 30 Seconds

### Step 1: Start the Application
```powershell
cd "C:\Users\ckmat\OneDrive\Documents\Masters ICT Policy\Thesis\Thesis Project\AI Assistant"
streamlit run app.py
```

### Step 2: Browser Opens Automatically
The app opens at `http://localhost:8501`

### Step 3: Start Chatting!

---

## Try These Queries

### Hospital Information
- "Tell me about KUTRRH services"
- "What are your contact numbers?"
- "What is the hospital's vision?"
- "How can I visit the hospital?"
- "Do you have an ICU?"

### Appointment Booking
- "I want to book an appointment"
- "Schedule me for next Tuesday at 2 PM"
- "When can I see a doctor?"

---

## What's New vs Before

| Before | After |
|--------|-------|
| ❌ Only appointment booking | ✅ Hospital info + appointments |
| ❌ No context about hospital | ✅ Answers from 21 documents |
| ❌ Generic responses | ✅ Source-attributed answers |
| ❌ Limited knowledge | ✅ Semantic search capability |

---

## Knowledge Base Status

```
📁 Documents: hospital_docs/
   ✅ 21 PDFs indexed
   
🌐 Website: https://www.kutrrh.go.ke
   ✅ 3 pages scraped
   
🔍 Vector Store: hospital_vector_store/
   ✅ 0.11 MB (fully indexed)
   
📊 Total Content: 44 chunks
   ✅ Ready for queries
```

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't start | `pip install -r requirements.txt` then retry |
| Knowledge base empty | `python initialize_knowledge_base.py` |
| Want to add docs | Place PDFs in `hospital_docs/` then reinitialize |
| Slow responses | Wait 20 seconds for first query (caching) |

---

## Environment

- **Python**: 3.13.7 ✅
- **API**: Groq (llama-3.3-70b) ✅
- **Storage**: FAISS Vector Store ✅
- **Documents**: 21 PDFs + Website ✅

---

## Features

🏥 **Hospital Information**
- Semantic search of documents
- Website content integration
- Source attribution for all answers

📅 **Appointment Booking**
- Schedule appointments
- View existing appointments
- Appointment reminders

🔄 **Smart Routing**
- Automatically detects intent
- Routes to appropriate tool
- Seamless conversation flow

---

## Next Steps

1. ▶️ Run `streamlit run app.py`
2. ❓ Ask a hospital question
3. 📅 Test appointment booking
4. 📄 Add more documents if needed

---

**See Also**: 
- `KNOWLEDGE_BASE_READY.md` - Detailed technical info
- `hospital_docs/` - Your indexed documents
- `hospital_vector_store/` - Vector embeddings

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
