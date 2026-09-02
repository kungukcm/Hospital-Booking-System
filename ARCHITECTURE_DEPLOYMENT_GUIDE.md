# Hospital Appointment System - Architecture & Deployment Guide

## Overview

The system has been separated into **frontend** and **backend** components to enable live deployment and better security. This guide explains the new architecture, how to run it locally, and how to deploy to production.

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Public Users                            │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
         ┌───▼────────────┐          ┌────────▼──────────┐
         │ Frontend App   │          │  Admin Dashboard  │
         │ (Streamlit)    │          │  (Streamlit)      │
         │ Port: 8501     │          │  Port: 8502       │
         └───┬────────────┘          └────────┬──────────┘
             │                                │
             └────────────────┬───────────────┘
                              │ (API Calls)
                     ┌────────▼──────────┐
                     │  Backend API      │
                     │  (FastAPI)        │
                     │  Port: 8000       │
                     └───┬─────────────┬─┘
                         │             │
                    ┌────▼──┐    ┌────▼──────┐
                    │ Chat  │    │Appts DB   │
                    │Agent  │    │Hospital KB│
                    └───────┘    └───────────┘
```

### Services

1. **Backend API (FastAPI)** - Port 8000
   - Core business logic
   - Chat/AI agent processing
   - Appointment management
   - Admin operations (with authentication)
   - Runs: `python backend_api.py`

2. **Public Frontend (Streamlit)** - Port 8501
   - User-facing appointment booking interface
   - Chat with AI assistant
   - No authentication required
   - Calls backend API for all operations
   - Runs: `streamlit run frontend_app.py`

3. **Admin Dashboard (Streamlit)** - Port 8502
   - Administrative interface (requires authentication)
   - Dashboard analytics
   - Knowledge base management
   - Appointment management
   - User management
   - Runs: `streamlit run admin_dashboard.py --server.port 8502`

## Local Development Setup

### Prerequisites

- Python 3.8+
- Virtual environment (venv or conda)
- All dependencies in requirements.txt

### Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (create `.env` if needed)
   ```
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=admin123
   GROQ_API_KEY=your_api_key_here
   ```

### Running Locally

**Option 1: Automated Startup (Recommended)**

Using startup script:
```bash
# On Linux/macOS
bash startup.sh

# On Windows (PowerShell)
.\startup.ps1
```

This starts all three services in new windows.

**Option 2: Manual Startup**

Open 3 separate terminals:

Terminal 1 (Backend):
```bash
python backend_api.py
```

Terminal 2 (Frontend):
```bash
streamlit run frontend_app.py
```

Terminal 3 (Admin Dashboard):
```bash
streamlit run admin_dashboard.py --server.port 8502
```

### Accessing Services Locally

- **Public Frontend**: http://localhost:8501
- **Admin Dashboard**: http://localhost:8502
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

**Default Admin Credentials**:
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT**: Change default password on first login in production!

## Production Deployment

### Deployment Architecture

For live deployment, you can use various hosting platforms:

```
┌──────────────────────────────────────────────────┐
│              Production Environment              │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────────────────────────────────┐    │
│  │        Cloud Platform                   │    │
│  │  (AWS, GCP, Azure, Heroku, etc.)       │    │
│  │                                         │    │
│  │  ┌──────────────────────────────────┐  │    │
│  │  │ Backend API (Uvicorn)            │  │    │
│  │  │ - FastAPI service                │  │    │
│  │  │ - Stateless (can scale)          │  │    │
│  │  │ - Environment-based config       │  │    │
│  │  └──────────────────────────────────┘  │    │
│  │                                         │    │
│  │  ┌──────────────────────────────────┐  │    │
│  │  │ Frontend (Streamlit Cloud)       │  │    │
│  │  │ - Public-facing app              │  │    │
│  │  │ - Points to backend API          │  │    │
│  │  └──────────────────────────────────┘  │    │
│  │                                         │    │
│  │  ┌──────────────────────────────────┐  │    │
│  │  │ Admin Dashboard (Streamlit)      │  │    │
│  │  │ - Protected with authentication  │  │    │
│  │  │ - Behind firewall/VPN (optional) │  │    │
│  │  └──────────────────────────────────┘  │    │
│  │                                         │    │
│  └─────────────────────────────────────────┘    │
│                                                   │
└──────────────────────────────────────────────────┘
```

### Backend Deployment (FastAPI + Uvicorn)

**Option 1: Docker**

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "backend_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t hospital-api .
docker run -p 8000:8000 hospital-api
```

**Option 2: Cloud Platforms (Heroku, AWS, GCP)**

For Heroku:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

Update `Procfile`:
```
web: uvicorn backend_api:app --host 0.0.0.0 --port $PORT
```

### Frontend Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect GitHub repository
4. Deploy `frontend_app.py`
5. Configure secrets (API endpoint, credentials) in Streamlit Cloud dashboard

### Admin Dashboard Deployment

Deploy on secure internal infrastructure:
- Use Streamlit Cloud with VPN access
- Or deploy behind reverse proxy with authentication
- Or use internal container service (Kubernetes, ECS)

Configuration for admin dashboard:
```bash
streamlit run admin_dashboard.py \
  --server.port 8502 \
  --server.address internal-only \
  --logger.level info
```

## API Endpoints

### Public Endpoints (No Auth Required)

- `GET /health` - Health check
- `POST /chat` - Chat with AI assistant
- `GET /appointments` - List appointments
- `GET /appointments/{id}` - Get appointment details
- `POST /appointments` - Create appointment
- `GET /recommendations/slots` - Get recommended time slots

### Admin Endpoints (Requires Authentication)

- `POST /admin/login` - Admin authentication
- `POST /admin/rebuild-kb` - Rebuild knowledge base
- `GET /admin/appointments` - Get appointments analytics
- `GET /admin/system-status` - Get system status
- `POST /admin/create-user` - Create new admin user

### API Authentication

Send admin token in Authorization header:
```
Authorization: Bearer <token>
```

Example:
```bash
curl -H "Authorization: Bearer abc123..." http://localhost:8000/admin/system-status
```

## Configuration

### Environment Variables

Create `.env` file:
```env
# Admin credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# LLM Configuration
GROQ_API_KEY=your_groq_api_key

# Backend
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Frontend
FRONTEND_PORT=8501
BACKEND_URL=http://localhost:8000

# Admin Dashboard
ADMIN_PORT=8502
BACKEND_URL=http://localhost:8000
```

### Production Environment Variables

```env
# Use strong passwords
ADMIN_USERNAME=admin_prod
ADMIN_PASSWORD=very_strong_password_here

# API configuration
GROQ_API_KEY=your_production_key

# Security
DEBUG=false
LOG_LEVEL=info

# Database (if using external)
DATABASE_URL=postgresql://user:pass@host/db

# CORS settings
ALLOWED_ORIGINS=https://yourdomain.com,https://admin.yourdomain.com
```

## Security Considerations

### Production Security Checklist

- [ ] Change default admin credentials
- [ ] Use strong passwords (min 12 characters)
- [ ] Enable HTTPS/SSL for all services
- [ ] Configure CORS properly (specify allowed origins)
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting on API
- [ ] Add request validation
- [ ] Set up proper logging and monitoring
- [ ] Use database authentication
- [ ] Implement backup strategy
- [ ] Configure firewall rules
- [ ] Use VPN for admin dashboard access
- [ ] Regular security audits
- [ ] Keep dependencies updated

### CORS Configuration

Update `backend_api.py` for production:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "https://admin.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## Monitoring & Logging

### Backend Logs

Logs are written to console and file. Configure in `logger.py`:
```python
logger = setup_logger(__name__)
```

### Frontend/Admin Logs

Streamlit logs are stored in `~/.streamlit/logs/`

### Production Monitoring

Recommended tools:
- **Sentry** - Error tracking
- **Datadog** - Infrastructure monitoring
- **New Relic** - Performance monitoring
- **ELK Stack** - Log aggregation
- **Prometheus** - Metrics collection

## Scaling Strategies

### Horizontal Scaling

1. **Backend API** - Stateless, easily scalable
   - Deploy multiple instances behind load balancer
   - Use environment variables for configuration

2. **Frontend** - Stateless
   - Deploy on Streamlit Cloud (auto-scales)
   - Or use multiple instances behind CDN

3. **Admin Dashboard** - Limited concurrency
   - Deploy single instance or 2-3 behind load balancer
   - Consider internal-only access

### Database Scaling

- Use external database service (PostgreSQL, MongoDB)
- Implement caching (Redis)
- Consider document storage for large data

### Knowledge Base Scaling

- Store vector embeddings in Pinecone or Weaviate
- Cache frequently accessed data
- Consider periodic reindexing strategy

## Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process on port
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Frontend can't connect to backend

1. Verify backend is running
2. Check firewall/network rules
3. Verify API URL in frontend
4. Check CORS configuration

### Admin dashboard login fails

1. Check admin credentials in `data/admin_users.json`
2. Verify backend is accessible
3. Check authentication token expiration
4. Review logs in backend

### Knowledge base issues

1. Verify hospital documents are in correct location
2. Check disk space for vector store
3. Monitor rebuild process in logs
4. Consider manual deletion of `hospital_vector_store/`

## Support & Maintenance

### Regular Maintenance Tasks

- Weekly: Check logs for errors
- Monthly: Review and rotate admin credentials
- Quarterly: Update dependencies
- Yearly: Security audit and penetration testing

### Backup Strategy

- Daily database backups
- Weekly full system backups
- Test restore procedures regularly
- Store backups in secure location

### Updates & Deployment

1. Test updates in development environment
2. Create backup before production update
3. Deploy during low-traffic period
4. Monitor system after deployment
5. Keep rollback procedure ready

## Support Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Streamlit Documentation**: https://docs.streamlit.io
- **API Documentation**: http://localhost:8000/docs (when backend is running)

---

**Last Updated**: 2024
**Version**: 2.0 (Separated Frontend/Backend)
