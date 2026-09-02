# Quick Start Guide - Separated Frontend/Backend Architecture

## 🚀 Quick Start (5 minutes)

### Step 1: Verify Virtual Environment

Ensure your virtual environment is activated:
```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Linux/macOS
source venv/bin/activate
```

### Step 2: Verify Dependencies

The following new dependencies are required:
- `requests` - For frontend/admin to call backend API
- `fastapi` - Backend API (already in requirements)
- `uvicorn` - ASGI server (already in requirements)

To update requirements:
```bash
pip install requests fastapi uvicorn python-multipart
```

### Step 3: Start All Services

**Windows (PowerShell):**
```powershell
.\startup.ps1
```

**Linux/macOS:**
```bash
bash startup.sh
```

This will automatically:
1. Start Backend API on port 8000
2. Start Public Frontend on port 8501
3. Start Admin Dashboard on port 8502

### Step 4: Access Services

Open in your browser:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:8501 | 👥 Public user interface for booking appointments |
| **Admin Dashboard** | http://localhost:8502 | 🔒 Admin interface (requires login) |
| **Backend API** | http://localhost:8000 | 📡 API endpoint |
| **API Docs** | http://localhost:8000/docs | 📖 Interactive API documentation |

### Step 5: Login to Admin Dashboard

1. Go to http://localhost:8502
2. Enter credentials:
   - **Username**: `admin`
   - **Password**: `admin123`

⚠️ **IMPORTANT**: Change password after first login!

---

## 📋 Architecture Overview

The system is now split into 3 separate services:

### 1️⃣ Backend API (FastAPI on port 8000)
- Handles all business logic
- Processes chat requests
- Manages appointments
- Handles admin operations
- Protected admin endpoints require authentication

### 2️⃣ Public Frontend (Streamlit on port 8501)
- User-facing interface
- Public access (no login required)
- Calls backend API for all operations
- Appointment booking and chat

### 3️⃣ Admin Dashboard (Streamlit on port 8502)
- Admin-only interface
- Requires authentication
- Dashboard analytics
- Knowledge base management
- Admin user management

---

## 🔧 Manual Startup (If Automated Script Doesn't Work)

Open 3 separate terminal windows:

**Terminal 1 - Backend API:**
```bash
python backend_api.py
# Expected: "Uvicorn running on http://0.0.0.0:8000"
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend_app.py
# Expected: Streamlit app running on http://localhost:8501
```

**Terminal 3 - Admin Dashboard:**
```bash
streamlit run admin_dashboard.py --server.port 8502
# Expected: Streamlit app running on http://localhost:8502
```

---

## 📝 Common Tasks

### Change Admin Password

1. Login to Admin Dashboard at http://localhost:8502
2. Go to "Users" tab
3. Create a new admin user with new credentials
4. Old default credentials will still work but should be changed

### Rebuild Hospital Knowledge Base

1. Login to Admin Dashboard
2. Go to "System" tab
3. Click "🔨 Rebuild Knowledge Base"
4. Wait for process to complete (may take several minutes)

### View API Documentation

1. Make sure backend is running
2. Open http://localhost:8000/docs
3. See all available endpoints
4. Test endpoints directly in the UI

### Create Appointment via Frontend

1. Go to http://localhost:8501
2. Fill in patient information
3. Select appointment type and date
4. Choose recommended time slot
5. Confirm appointment

### Monitor Appointments via Admin

1. Login to Admin Dashboard
2. Go to "Appointments" tab
3. View all appointments with details
4. Check analytics on "Dashboard" tab

---

## 🆘 Troubleshooting

### "Cannot connect to backend" error

**Solution:**
1. Verify backend is running: `python backend_api.py`
2. Check port 8000 is not in use
3. Verify firewall allows localhost connections

### "Port already in use" error

**Solution - Find and kill process:**

```powershell
# Windows - Find process on port 8000
Get-Process | Where-Object {$_.Name -like "*python*"}

# Kill specific process
Stop-Process -Id <PID> -Force
```

```bash
# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Frontend loads but shows "Service unavailable"

**Solution:**
1. Check backend is running
2. Verify `BACKEND_URL` in frontend_app.py points to http://localhost:8000
3. Check no firewall blocking connections

### Admin dashboard login fails

**Solution:**
1. Verify backend API is running
2. Check credentials (default: admin/admin123)
3. View backend logs for authentication errors

### Streamlit apps won't start

**Solution:**
1. Verify Python 3.8+ installed
2. Verify virtual environment activated
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Check Python path: `which python` (macOS/Linux) or `where python` (Windows)

---

## 📊 System Health Check

To verify everything is working:

1. **Backend Health**: Open http://localhost:8000/health
   - Should show: `{"status":"healthy",...}`

2. **Frontend Access**: Open http://localhost:8501
   - Should load without errors

3. **Admin Access**: Open http://localhost:8502
   - Should show login page

4. **Chat Test**: In frontend, ask "What services are available?"
   - Should get AI response

5. **Appointment Test**: Create test appointment
   - Should see confirmation

---

## 🔐 Security Notes

### Local Development (Current)
- Default admin credentials used
- No HTTPS
- CORS allows all origins
- OK for local/internal use

### Before Production Deployment
- [ ] Change admin credentials
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS for specific domains
- [ ] Set up proper authentication
- [ ] Review and update security settings
- [ ] Set up backup strategy
- [ ] Configure logging

See `ARCHITECTURE_DEPLOYMENT_GUIDE.md` for production deployment details.

---

## 📞 Next Steps

1. ✅ Run services locally with provided scripts
2. 📖 Review `ARCHITECTURE_DEPLOYMENT_GUIDE.md` for deployment info
3. 🧪 Test all features in development environment
4. 🔒 Configure security settings
5. 🚀 Deploy to production environment

---

## 📚 Files Reference

| File | Purpose |
|------|---------|
| `backend_api.py` | FastAPI backend service |
| `frontend_app.py` | Public frontend Streamlit app |
| `admin_dashboard.py` | Admin dashboard Streamlit app |
| `auth.py` | Authentication utilities |
| `startup.ps1` | Windows PowerShell startup script |
| `startup.sh` | Linux/macOS bash startup script |
| `ARCHITECTURE_DEPLOYMENT_GUIDE.md` | Detailed architecture & deployment guide |
| `QUICK_START.md` | This file |

---

**Need help?** Check the detailed guide: `ARCHITECTURE_DEPLOYMENT_GUIDE.md`

Last Updated: 2024
