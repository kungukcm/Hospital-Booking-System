import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    try:
        import streamlit as st
        GROQ_API_KEY = st.secrets.get('GROQ_API_KEY')
    except Exception:
        GROQ_API_KEY = None
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not configured. Add it to Streamlit secrets or the server environment.")