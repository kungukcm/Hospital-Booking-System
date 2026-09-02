# KUTRRH AI Hospital Assistant

## Online deployment

This repository uses a split deployment:

1. Deploy the FastAPI backend to Render using `render.yaml`. Set `GROQ_API_KEY` (and `OPENAI_API_KEY` if required) as private environment variables. Render provides the public API URL, for example `https://kutrrh-assistant-api.onrender.com`.
2. In Streamlit Community Cloud, create an app from `frontend_app.py` on the `main` branch. Add this secret:

```toml
BACKEND_URL = "https://YOUR-RENDER-SERVICE.onrender.com"
```

3. Create a second Streamlit Community Cloud app from `admin_dashboard.py` and add the same `BACKEND_URL` secret. This is the protected management dashboard.

The public app and admin dashboard must be deployed as separate Streamlit apps because Streamlit Community Cloud assigns one entry point and port per app. The backend stores appointments, feedback, users, and chat logs under `/app/data`; the Render disk in `render.yaml` keeps that data across restarts.

For local development, the apps default to `http://localhost:8000`. Start the backend with `venv\Scripts\python.exe backend_api.py`, the public UI on port 8501, and the admin UI on port 8502.

