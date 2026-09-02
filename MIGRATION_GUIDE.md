# Migration Guide: Monolithic to Separated Frontend/Backend Architecture

## Overview

Your system has been successfully refactored from a monolithic Streamlit application to a separated frontend/backend architecture. This guide explains what changed and how to use the new system.

## What Changed?

### Before: Monolithic Architecture
```
┌─────────────────────────────────┐
│   Streamlit App (app.py)        │
│                                 │
│  ├─ Chat Interface             │
│  ├─ Appointment Booking        │
│  ├─ Dashboard                  │
│  ├─ Admin Functions            │
│  │                             │
│  └─ Database/KB Direct Access  │
└─────────────────────────────────┘
```

**Issues with monolithic approach:**
- Difficult to scale independently
- Dashboards accessible to all users
- Can't deploy frontend and backend separately
- Admin functions mixed with user interface
- Hard to maintain security separation

### After: Separated Architecture
```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Public Frontend │  │  Admin Dashboard │  │  Backend API     │
│   (Streamlit)    │  │  (Streamlit)      │  │   (FastAPI)      │
│   Port: 8501     │  │   Port: 8502      │  │   Port: 8000     │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ • Chat interface │  │ • Dashboard      │  │ • Business logic │
│ • Booking form   │  │ • Analytics      │  │ • Chat agent     │
│ • Public access  │  │ • Admin login    │  │ • Auth system    │
│ • No auth needed │  │ • KB management  │  │ • Database ops   │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                    │                     │
         └────────────────────┴─────────────────────┘
                API Calls (HTTP/JSON)
```

**Benefits:**
- ✅ Each component scales independently
- ✅ Dashboards protected behind authentication
- ✅ Separate deployment pipelines
- ✅ Better security through API layer
- ✅ Easier to maintain and test
- ✅ Can use different hosting for each service

## File Organization

### Old Structure (Monolithic)
```
AI Assistant/
├── app.py              # Everything in one file
├── agent.py
├── appointments_db.py
├── hospital_setup.py
└── ... other files
```

### New Structure (Separated)
```
AI Assistant/
├── backend_api.py          # Backend API
├── frontend_app.py         # Public frontend
├── admin_dashboard.py      # Admin dashboard
├── auth.py                 # Authentication
│
├── startup.ps1             # Windows startup script
├── startup.sh              # Linux/macOS startup script
│
├── agent.py                # Still here (used by backend)
├── appointments_db.py      # Still here (used by backend)
├── hospital_setup.py       # Still here (used by backend)
│
├── QUICK_START_SEPARATED.md        # Quick start guide
├── ARCHITECTURE_DEPLOYMENT_GUIDE.md # Detailed guide
└── ... other files
```

## Migration Path

### Old Way: Running Single App
```bash
streamlit run app.py
```
This started everything on port 8501.

### New Way: Running All Services

**Recommended (Automatic):**
```bash
# Windows
.\startup.ps1

# Linux/macOS  
bash startup.sh
```

**Manual (3 separate terminals):**

Terminal 1:
```bash
python backend_api.py
```

Terminal 2:
```bash
streamlit run frontend_app.py
```

Terminal 3:
```bash
streamlit run admin_dashboard.py --server.port 8502
```

## Key Differences

### API Calls

**Before:** All logic in Streamlit session state
```python
# In app.py (monolithic)
conversation = []
receive_message_from_caller(message, conversation)
```

**After:** Frontend calls backend API
```python
# In frontend_app.py (separated)
response_data = call_backend(
    "/chat",
    method="POST",
    data={
        "message": user_input,
        "conversation_history": st.session_state.conversation
    }
)
```

### Admin Access

**Before:** Admin button visible to everyone
```python
# In app.py - Rebuild KB button accessible to all
with st.sidebar:
    if st.button("Rebuild Hospital Knowledge Base"):
        setup_hospital_knowledge_base()
```

**After:** Admin functions require authentication
```python
# In admin_dashboard.py - Protected by login
def show_admin_dashboard():
    # Requires valid token from verify_admin_auth()
    ...
```

### Database/Backend Access

**Before:** Direct access from frontend
```python
# In app.py (monolithic)
appointments = get_appointments()  # Direct function call
```

**After:** API endpoint calls
```python
# In frontend_app.py (separated)
appointments_response = call_backend("/appointments")
```

## Backward Compatibility

⚠️ **Important**: The old `app.py` file is still present but **not recommended** for use with this architecture.

### Original app.py
- Still exists for reference
- Still has the monolithic code
- Can still run standalone if needed: `streamlit run app.py`
- But **should not be used** with the new separated architecture

### Recommendation
- Use the new separated architecture (`frontend_app.py`, `backend_api.py`, `admin_dashboard.py`)
- Keep `app.py` for reference only
- Delete or rename `app.py` if migrating completely

## Accessing Different Interfaces

### Public Users (No Authentication)
Go to: **http://localhost:8501** (Frontend)
- View appointments
- Book appointments
- Chat with AI
- No login required

### System Administrators
Go to: **http://localhost:8502** (Admin Dashboard)
- Login with admin credentials
- View analytics
- Manage appointments
- Rebuild knowledge base
- Create new admin users

### Developers/API Integration
Access: **http://localhost:8000** (Backend API)
- View API docs: http://localhost:8000/docs
- Make direct API calls
- Integrate with other systems

## Configuration Migration

### Environment Variables (New)

Create `.env` file:
```env
# Admin credentials (CHANGE IN PRODUCTION)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# LLM Configuration
GROQ_API_KEY=your_key_here

# Logging
LOG_LEVEL=info
DEBUG=false
```

### Settings Files

Your existing `settings.yaml` and configuration files continue to work with the new architecture.

## API Authentication

### Admin Token-Based Auth

Get token:
```bash
curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Response:
```json
{
  "token": "abc123...",
  "message": "Welcome admin!"
}
```

Use token in requests:
```bash
curl -H "Authorization: Bearer abc123..." \
  http://localhost:8000/admin/rebuild-kb
```

## Deployment Changes

### Local Development (No Changes Needed)
- Still use `startup.ps1` or `startup.sh`
- Same environment setup
- Same database files

### Cloud Deployment (New Capabilities)

**Before:** Deploy single monolithic app
- Limited scalability
- All functions on same server
- Hard to secure admin features

**After:** Deploy services independently
- Scale backend separately from frontend
- Frontend on Streamlit Cloud
- Backend on cloud platform (AWS, GCP, Heroku, etc.)
- Admin dashboard on internal infrastructure

See `ARCHITECTURE_DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

## Testing the Migration

### Quick Verification Checklist

- [ ] Backend starts: `python backend_api.py`
  - Opens http://0.0.0.0:8000
  - Shows "Uvicorn running"

- [ ] Frontend starts: `streamlit run frontend_app.py`
  - Opens http://localhost:8501
  - Can see chat interface and appointment booking

- [ ] Admin dashboard starts: `streamlit run admin_dashboard.py --server.port 8502`
  - Opens http://localhost:8502
  - Shows login page

- [ ] Can login to admin: default admin / admin123
  - Shows dashboard after login
  - Can see appointments and analytics

- [ ] Can create appointment from frontend
  - Type name, patient ID, phone, email
  - Select appointment type and date
  - Get recommended slots
  - Confirm appointment

- [ ] Can chat with AI from frontend
  - Ask "What services are available?"
  - Get response from backend

- [ ] API documentation available
  - Open http://localhost:8000/docs
  - See all endpoints

### Test Scenarios

**Scenario 1: Patient User**
1. Open http://localhost:8501
2. Chat with AI about services
3. Book an appointment
4. View appointment confirmation

**Scenario 2: Admin User**
1. Open http://localhost:8502
2. Login (admin/admin123)
3. View dashboard analytics
4. Check appointments list
5. Try rebuild knowledge base button

**Scenario 3: API Integration**
1. Use backend API directly
2. Create appointment via API
3. Query appointments
4. Admin operations with authentication token

## Troubleshooting Migration Issues

### Issue: "Cannot connect to backend"

**Check:**
1. Is backend running? `python backend_api.py`
2. Check port 8000 is available
3. Verify no firewall blocking
4. Check `BACKEND_URL` in frontend code

### Issue: "Admin login not working"

**Check:**
1. Is backend running?
2. Verify admin credentials in `data/admin_users.json`
3. Check authentication endpoint works:
   ```bash
   curl -X POST http://localhost:8000/admin/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}'
   ```

### Issue: "Monolithic app still running"

**Solution:** Stop old app before running new system
```bash
# Find and kill old process
ps aux | grep streamlit
kill -9 <PID>
```

## Benefits Realized

✅ **Security:**
- Admin functions protected behind authentication
- Separate API layer with token-based auth
- Public frontend has no access to admin operations

✅ **Scalability:**
- Backend can scale independently
- Frontend can be deployed to multiple regions
- Database can be external and shared

✅ **Maintainability:**
- Smaller, focused codebases
- Clear separation of concerns
- Easier to test individual components

✅ **Deployment:**
- Can deploy each service separately
- Different platforms for different services
- Independent update and rollback capabilities

## Next Steps

1. ✅ Review this migration guide
2. ✅ Run `startup.ps1` (Windows) or `startup.sh` (Linux/macOS)
3. ✅ Test public frontend at http://localhost:8501
4. ✅ Test admin dashboard at http://localhost:8502
5. 📖 Read `ARCHITECTURE_DEPLOYMENT_GUIDE.md` for production deployment
6. 🔐 Change default admin credentials for production
7. 🚀 Deploy to production infrastructure

## Support

For detailed information:
- **Architecture & Deployment**: `ARCHITECTURE_DEPLOYMENT_GUIDE.md`
- **Quick Start**: `QUICK_START_SEPARATED.md`
- **API Documentation**: http://localhost:8000/docs (when backend running)

---

**Migration Complete!** 🎉

Your system is now using the modern separated frontend/backend architecture, enabling better security, scalability, and deployment flexibility.

Last Updated: 2024
