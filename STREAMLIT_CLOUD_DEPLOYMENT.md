# Streamlit Cloud Deployment - Step-by-Step Guide

## Overview
Streamlit Cloud is the easiest way to deploy your Hospital Booking System. It's free, requires minimal setup, and handles scaling automatically.

**Time to deploy:** 5-10 minutes  
**Cost:** Free (with optional paid tiers)  
**Skill level:** Beginner-friendly

---

## Prerequisites

1. ✅ Project code (you have this)
2. ✅ Groq API key (you have this in .env)
3. ⏳ GitHub account (free at github.com)
4. ⏳ Streamlit account (free, uses your GitHub login)

---

## Step 1: Create GitHub Repository

### Option A: Using Command Line

```bash
cd "c:\Users\ckmat\OneDrive\Documents\Masters ICT Policy\Thesis\Journals\Hospital Booking System\Hospital Booking System"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Hospital Booking System"

# Create main branch
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/Hospital-Booking-System.git

# Push to GitHub
git push -u origin main
```

### Option B: Using GitHub Web Interface

1. Go to **github.com** and login
2. Click **"+"** → **"New repository"**
3. Name: `Hospital-Booking-System`
4. Description: `AI-powered appointment booking system`
5. Make it **Public** (required for free Streamlit Cloud)
6. Click **"Create repository"**
7. Follow the instructions to push existing code

---

## Step 2: Verify GitHub Setup

Your repository should have:
```
Hospital-Booking-System/
├── app.py ✅
├── agent.py ✅
├── tools.py ✅
├── requirements.txt ✅
├── .env (should NOT be here - check .gitignore)
└── [other files]
```

**Verify .env is NOT committed:**
```bash
git status  # Should NOT show .env
```

**Verify .gitignore includes .env:**
```bash
cat .gitignore | findstr ".env"  # Should show .env
```

---

## Step 3: Deploy to Streamlit Cloud

### 3.1 Go to Streamlit Cloud Dashboard
1. Open: **https://streamlit.io/cloud**
2. Click **"Sign up"** or **"Log in"**
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit to access your GitHub

### 3.2 Create New App
1. Click **"New app"** button
2. Fill in the form:

| Field | Value |
|-------|-------|
| **Repository** | YOUR_USERNAME/Hospital-Booking-System |
| **Branch** | main |
| **Main file path** | app.py |

3. Click **"Deploy!"**

### 3.3 Streamlit Deploys
- You'll see a loading screen
- First deployment takes 2-3 minutes
- You'll get a URL like: `https://your-app-name.streamlit.app`

---

## Step 4: Add Environment Variables (CRITICAL!)

Your app won't work without the Groq API key!

### 4.1 Access Secrets
In Streamlit Cloud dashboard:
1. Find your deployed app
2. Click **"..."** (three dots) → **"Settings"**
3. Click **"Secrets"** tab

### 4.2 Add Your API Key
In the secrets editor, paste:
```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

**Important:** 
- Use this format (with quotes)
- No `=` signs or special characters inside the key
- Keep the exact formatting

### 4.3 Save and Reboot
1. Click **"Save"**
2. App automatically restarts
3. Check the logs to verify it's working

---

## Step 5: Test Your Deployment

1. Open your Streamlit Cloud URL (e.g., `https://your-app.streamlit.app`)
2. Wait for app to load (first visit takes a moment)
3. You should see:
   - Chat interface on the left
   - Backend debug panel on the right
4. Try typing something like: "Book me an appointment tomorrow at 2pm"

---

## 🎉 You're Live!

Your Hospital Booking System is now deployed to Streamlit Cloud!

**Your app URL:** `https://your-app-name.streamlit.app`

Share this link with:
- Friends
- Team members
- Stakeholders
- Anyone!

---

## Common Issues & Solutions

### Issue 1: App Keeps Crashing
**Symptom:** Red error box immediately on load

**Solution:**
1. Check Streamlit Cloud logs (bottom right)
2. Most common: Missing GROQ_API_KEY in Secrets
3. Go to Settings → Secrets → Add your key
4. App auto-restarts

### Issue 2: "GROQ_API_KEY not set"
**Symptom:** Error message about missing API key

**Solution:**
```toml
# In Streamlit Cloud Secrets, use exact format:
GROQ_API_KEY = "gsk_abc123xyz..."  # Your actual key
```

### Issue 3: App is Slow
**Symptom:** Takes long time to respond

**Solution:**
- First request may be slower (cold start)
- Streamlit Cloud has generous free tier
- Responses should be <5 seconds after that

### Issue 4: Chat Not Responding
**Symptom:** Messages disappear but no response

**Solution:**
1. Check browser console for errors
2. Check Streamlit Cloud logs
3. Verify Groq API key is valid
4. Try different prompt (simpler request)

### Issue 5: Can't Find "Secrets" Option
**Symptom:** No secrets editor visible

**Solution:**
1. Make sure you're logged in to Streamlit Cloud
2. Click the app name (top right)
3. Go to "Settings"
4. Look for "Secrets" tab

---

## How Streamlit Cloud Works

```
Your Code on GitHub
        ↓
    Streamlit Cloud
        ↓
    Automatic Deployment
        ↓
    Live App URL
        ↓
    (Scale automatically!)
```

**Key features:**
- ✅ Automatic updates (push to GitHub → auto-deploys)
- ✅ Free SSL/HTTPS
- ✅ Custom domain support (paid)
- ✅ Email alerts
- ✅ Analytics & logs
- ✅ 1GB memory, generous limits

---

## Making Changes After Deployment

### To Update Your App:
1. Make changes to code locally
2. Test with `streamlit run app.py`
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your change description"
   git push origin main
   ```
4. Streamlit Cloud automatically redeploys!

### To Update AI Prompts:
1. Edit `settings.yaml` locally
2. Push to GitHub
3. App redeployed automatically

---

## Monitoring Your Deployed App

### Check App Status
In Streamlit Cloud dashboard:
- Green dot = app is running
- Yellow = deploying
- Red = error

### View Logs
1. Click your app
2. Scroll down to see logs
3. Shows errors and debug info

### Check Analytics (Optional)
Click your app → "Analytics" tab to see:
- View count
- User count
- Performance metrics

---

## Performance Tips

1. **First request slower:** App "wakes up" from sleep
2. **Subsequent requests faster:** Usually <2 seconds
3. **Session persistence:** User session stays alive during use
4. **Restart after 1 hour:** If no activity, app goes to sleep

---

## Security Checklist

✅ `.env` is in `.gitignore`  
✅ API key NOT in code  
✅ API key in Streamlit Cloud Secrets  
✅ Repository is public (required for free tier)  
✅ No secrets in README or comments  

---

## Upgrading to Paid Tier

Streamlit Cloud offers paid plans if you want:
- More compute
- Custom domains
- Priority support
- Higher limits

For now, **free tier is perfect** for testing!

---

## Sharing Your App

### Share the URL
Simply share: `https://your-app-name.streamlit.app`

### Make App Discoverable
Optional - list in Streamlit Gallery:
1. Streamlit Cloud dashboard
2. Click your app → Settings
3. Check "List in gallery"

### Get Statistics
Track usage in Analytics tab

---

## Next Steps After Deployment

### Immediate
- [ ] Test all features
- [ ] Gather user feedback
- [ ] Monitor logs for errors

### Short-term
- [ ] Add more appointment types
- [ ] Improve AI prompts
- [ ] Customize styling

### Medium-term
- [ ] Add database (PostgreSQL)
- [ ] User authentication
- [ ] REST API backend

---

## Troubleshooting Commands

If you need to rebuild/redeploy:

```bash
# Pull latest code
git pull origin main

# Check app status
git log --oneline  # Shows recent commits

# To force redeployment
git commit --allow-empty -m "Force redeploy"
git push origin main
```

---

## Support Resources

| Resource | Link |
|----------|------|
| Streamlit Docs | https://docs.streamlit.io |
| Streamlit Cloud Help | https://docs.streamlit.io/streamlit-cloud |
| Community Forum | https://discuss.streamlit.io |

---

## 🎊 Success Indicators

When deployment is successful, you'll see:

✅ App loads at `https://your-app.streamlit.app`  
✅ Chat interface visible  
✅ Can type messages  
✅ Backend panel shows debug info  
✅ No error messages  
✅ App responds to requests  

---

## Pro Tips

1. **Keep README updated** - Explain what your app does
2. **Add instructions** - Help users understand features
3. **Test thoroughly** - Before sharing link
4. **Monitor logs** - Catch bugs early
5. **Update regularly** - Push improvements to GitHub

---

## Rollback (If Something Breaks)

If an update breaks the app:

```bash
# See recent commits
git log --oneline -5

# Revert to previous version
git revert HEAD
git push origin main

# Streamlit automatically redeploys with old code
```

---

**Congratulations! Your app is live on Streamlit Cloud! 🎉**

Share the URL and let users book appointments with AI!

---

**Last Updated:** January 17, 2026  
**Status:** ✅ Ready to Deploy
