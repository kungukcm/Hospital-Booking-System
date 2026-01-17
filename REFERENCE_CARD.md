# 🚀 Hospital Booking System - Reference Card

## ⚡ Quick Commands

### Start Local Server
```bash
.\venv\Scripts\activate
streamlit run app.py
```
🔗 Access at: `http://localhost:8501`

### Start with Docker
```bash
docker-compose up --build
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### View Logs
```bash
tail -f app.log          # macOS/Linux
Get-Content app.log -Tail 20 -Wait  # Windows PowerShell
```

---

## 📋 File Locations & Purposes

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `agent.py` | AI agent logic using LangGraph |
| `tools.py` | Appointment management tools |
| `config.py` | Configuration loader |
| `settings.yaml` | LLM prompts and settings |
| `.env` | **YOUR API KEYS** (keep secret!) |
| `.streamlit/config.toml` | Streamlit UI configuration |
| `Dockerfile` | Docker container definition |
| `docker-compose.yml` | Local Docker setup |

---

## 🔑 Required Setup

### 1. Get Groq API Key
Visit: https://console.groq.com → Create API Key

### 2. Add to .env File
```
GROQ_API_KEY=your_key_here
```

### 3. Run Application
```bash
streamlit run app.py
```

---

## 📚 Documentation Map

```
START HERE ↓
│
├─ QUICK_START.md
│  └─ Read this first! 5-minute guide
│
├─ SETUP_COMPLETE.md
│  └─ What was built, how to use it
│
├─ DEPLOYMENT.md
│  └─ 4 cloud deployment options:
│     • Streamlit Cloud (easiest)
│     • AWS EC2 (most control)
│     • Heroku (simple)
│     • Google Cloud Run (serverless)
│
└─ BUILD_SUMMARY.md
   └─ Technical details & checklists
```

---

## 🌐 Deployment Paths

### Path 1: Streamlit Cloud (5 min, Free)
```bash
git push origin main
→ Go to streamlit.io/cloud
→ Click "New app"
→ Connect your repo → Deploy
```

### Path 2: Docker (3 min)
```bash
docker-compose up --build
→ Open http://localhost:8501
```

### Path 3: Heroku (10 min, Free-$7/mo)
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku config:set GROQ_API_KEY="your_key"
```

### Path 4: AWS EC2 (30 min, ~$5-50/mo)
See DEPLOYMENT.md for detailed steps

---

## 🆘 Common Issues

| Issue | Fix |
|-------|-----|
| "GROQ_API_KEY not set" | Add to `.env` file |
| Port 8501 in use | `streamlit run app.py --server.port 8502` |
| ModuleNotFoundError | Activate venv first |
| Docker fails | Ensure `.env` exists in root |
| Cloud deployment error | Check `.env` is in `.gitignore` |

---

## 🎯 Project Structure

```
Hospital Booking System/
├── 📱 app.py              ← Start here!
├── 🤖 agent.py            ← AI logic
├── 🛠️  tools.py            ← Appointment functions
├── ⚙️  config.py, settings.yaml
├── 🔐 .env                ← Your API keys
├── 🐳 Dockerfile, docker-compose.yml
└── 📖 *.md files          ← Guides
```

---

## 🔄 Development Workflow

```
1. Modify code (agent.py, tools.py, app.py)
   ↓
2. Streamlit auto-reloads (if using streamlit run)
   ↓
3. Test in chat interface
   ↓
4. Check logs in right panel
   ↓
5. Debug using app.log
```

---

## 📊 Architecture Flow

```
User Input (Chat)
     ↓
Streamlit UI (app.py)
     ↓
Agent (agent.py)
     ↓
Groq LLM (ChatGroq)
     ↓
Tools (tools.py)
  ├─ book_appointment()
  ├─ get_next_available()
  └─ cancel_appointment()
     ↓
Session State
     ↓
Display Results
```

---

## 🔐 Security Quick Reference

✅ DO:
- Keep `.env` file secret
- Use `.env.example` as template
- Rotate API keys regularly
- Use environment variables in production

❌ DON'T:
- Commit `.env` to Git
- Share API keys in code
- Hardcode sensitive data
- Use production keys in development

---

## 📦 Key Dependencies

| Package | What It Does |
|---------|-------------|
| `streamlit` | Web interface |
| `langchain` | LLM framework |
| `langchain-groq` | Groq LLM support |
| `langgraph` | Workflow orchestration |
| `loguru` | Advanced logging |
| `fastapi` | API framework (future use) |

---

## 💻 Environment Setup

### Requirements
- Python 3.10+ ✅
- Virtual environment ✅
- Groq API key ✅
- 2GB RAM minimum ✅

### Check Setup
```bash
python --version        # Should be 3.10+
pip list | grep streamlit
type .env               # Should exist with API key
```

---

## 🎓 Key Concepts

### Agent
AI-powered assistant that understands natural language appointment requests

### Tools
Functions available to the agent:
- `book_appointment()` - Create appointment
- `get_next_available_appointment()` - Find open slot
- `cancel_appointment()` - Remove appointment

### LangGraph
Orchestrates the agent flow with conditional logic

### Groq LLM
Fast, free LLM model for understanding user intent

---

## 📈 Performance Tips

1. **Clear session regularly** to free memory
2. **Use smaller LLM models** for faster responses
3. **Cache API responses** where possible
4. **Monitor logs** for errors affecting performance
5. **Scale horizontally** with load balancer in production

---

## 🔗 Useful Links

| Resource | URL |
|----------|-----|
| Groq Console | https://console.groq.com |
| Streamlit Docs | https://docs.streamlit.io |
| LangChain Docs | https://python.langchain.com |
| Docker Hub | https://hub.docker.com |

---

## 📞 Getting Help

1. **Check logs:** `tail -f app.log`
2. **Read docs:** See documentation map above
3. **Debug mode:** Right panel in Streamlit shows state
4. **Try again:** Many issues resolve after restart

---

## ✨ Pro Tips

- Use `st.write()` to debug in Streamlit
- Check `app.log` for detailed error messages
- Session state persists during development
- Streamlit reruns on every interaction
- Docker isolates dependencies perfectly

---

## 🚀 Deployment Checklist

Before deploying:
- [ ] API key works (test locally)
- [ ] All files committed to Git (except `.env`)
- [ ] `.env` in `.gitignore`
- [ ] `requirements.txt` is complete
- [ ] No hardcoded secrets in code
- [ ] Tested locally first
- [ ] Documentation is current

---

## 📋 Post-Deployment

After deploying:
- [ ] Test the deployed app
- [ ] Check logs for errors
- [ ] Monitor API usage
- [ ] Set up monitoring/alerts
- [ ] Document deployment details
- [ ] Share access with team
- [ ] Plan next features

---

## 🎯 Quick Start (TL;DR)

```bash
# 1. Get API key from https://console.groq.com
# 2. Add to .env file
# 3. Run:
.\venv\Scripts\activate
streamlit run app.py

# 4. Open: http://localhost:8501
# 5. To deploy: Read QUICK_START.md or DEPLOYMENT.md
```

---

**Last Updated:** January 17, 2026  
**Version:** 1.0  
**Status:** ✅ Production Ready
