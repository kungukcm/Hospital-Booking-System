import streamlit as st
import requests
import os
from logger import setup_logger

logger = setup_logger(__name__)

# Backend API configuration - override with BACKEND_URL env var in deployment
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit", "kutrrh_logo.png")

CUSTOM_CSS = """
<style>
    .block-container {
        max-width: 820px;
        padding-top: 2rem;
    }
    #kutrrh-header {
        text-align: center;
        margin-bottom: 0.5rem;
    }
    #kutrrh-header h1 {
        font-size: 1.9rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1f4788, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    #kutrrh-header p {
        color: #6b7280;
        font-size: 0.95rem;
        margin: 0;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 0.25rem 0.5rem;
    }
    div[data-testid="stChatInput"] textarea {
        border-radius: 14px;
    }
</style>
"""


def call_backend(endpoint: str, method: str = "GET", data: dict = None, params: dict = None):
    """Call the backend API and return parsed JSON, or None on failure."""
    url = f"{BACKEND_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Backend API error calling {endpoint}: {str(e)}")
        st.error(f"❌ Service error: {str(e)}")
        return None


def initialize_session_state():
    """Initialize session state variables"""
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []  # list of {"role": "user"|"assistant", "content": str}


def main():
    initialize_session_state()

    st.set_page_config(
        layout="centered",
        page_title="KUTRRH - AI Chat Assistant",
        page_icon="💬"
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Check backend connectivity
    try:
        requests.get(f"{BACKEND_URL}/health", timeout=5)
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to the hospital assistant service. Please try again shortly.")
        st.stop()

    # Header with logo and friendly welcome
    if os.path.exists(LOGO_PATH):
        logo_col1, logo_col2, logo_col3 = st.columns([1, 1.4, 1])
        with logo_col2:
            st.image(LOGO_PATH, width="stretch")

    st.markdown("""
    <div id="kutrrh-header">
        <h1>Welcome to our AI Chat Assistant</h1>
        <p>Ask about hospital services, contacts, payments, or book an appointment</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Display conversation, with a friendly opening message when empty
    if not st.session_state.conversation:
        st.chat_message("assistant").write(
            "👋 Hi there! I'm your KUTRRH assistant. I can help you book an appointment, "
            "answer questions about our services, or share contact and payment details. "
            "How can I help you today?"
        )

    for message in st.session_state.conversation:
        role = "user" if message["role"] == "user" else "assistant"
        st.chat_message(role).write(message["content"])

    # User input
    user_input = st.chat_input("Ask about appointments, hospital services, or payments...")
    if user_input:
        logger.debug(f"Received user input: {user_input}")
        st.session_state.conversation.append({"role": "user", "content": user_input})

        result = call_backend(
            "/chat",
            method="POST",
            data={
                "message": user_input,
                "conversation_history": st.session_state.conversation
            }
        )
        if result:
            st.session_state.conversation = result["conversation_history"]
        st.rerun()


if __name__ == "__main__":
    main()
