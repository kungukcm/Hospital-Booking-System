"""
Admin Dashboard for Hospital Appointment System
Protected admin interface for management and analytics
Requires authentication to access
"""

import streamlit as st
import requests
import logging
import os
from datetime import datetime
from urllib.parse import quote

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
try:
    BACKEND_URL = st.secrets.get("BACKEND_URL", BACKEND_URL).rstrip("/")
except Exception:
    pass
if BACKEND_URL in {"https://example.onrender.com", "https://YOUR-RENDER-SERVICE.onrender.com"}:
    BACKEND_URL = "http://localhost:8000"
LOGO_PATH = os.path.join(os.path.dirname(__file__), ".streamlit", "kutrrh_logo.png")

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="KUTRRH Admin Dashboard",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Authentication Management
# ============================================================================

def call_backend_auth(endpoint: str, method: str = "GET", data: dict = None, token: str = None) -> dict:
    """Call backend API with optional authentication"""
    url = f"{BACKEND_URL}{endpoint}"
    headers = {}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Backend API error: {str(e)}")
        st.error(f"❌ Service error: {str(e)}")
        return None


def initialize_session_state():
    """Initialize session state"""
    if 'admin_token' not in st.session_state:
        st.session_state.admin_token = None
    if 'admin_username' not in st.session_state:
        st.session_state.admin_username = None


def login_admin(username: str, password: str) -> bool:
    """Authenticate admin user"""
    response = call_backend_auth(
        "/admin/login",
        method="POST",
        data={"username": username, "password": password}
    )
    
    if response and "token" in response:
        st.session_state.admin_token = response["token"]
        st.session_state.admin_username = username
        logger.info(f"Admin login successful: {username}")
        return True
    
    logger.warning(f"Admin login failed for user: {username}")
    return False


def logout_admin():
    """Logout admin user"""
    st.session_state.admin_token = None
    st.session_state.admin_username = None
    logger.info("Admin logout")


# ============================================================================
# Login Page
# ============================================================================

def show_login_page():
    """Display login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if os.path.exists(LOGO_PATH):
            logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
            with logo_col2:
                st.image(LOGO_PATH, width=250)
        st.markdown("""
        <div style="text-align: center;">
            <h3 style="color: #2196F3;">Admin Dashboard</h3>
            <p style="color: #666;">Secure Authentication Required</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("🔐 Admin Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", placeholder="Enter your password", type="password")
            
            submitted = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                elif login_admin(username, password):
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        
        st.markdown("---")
        st.info("ℹ️ Default credentials: admin / admin123\n\n⚠️ Change default password after first login!")


# ============================================================================
# Admin Dashboard
# ============================================================================

def show_admin_dashboard():
    """Display admin dashboard"""
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.admin_username}")
        st.markdown(f"*Logged in as Admin*")
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_admin()
            st.rerun()
    
    # Header
    header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
    with header_col2:
        if os.path.exists(LOGO_PATH):
            logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
            with logo_col2:
                st.image(LOGO_PATH, width=220)
        st.markdown("""
        <div style="text-align: center;">
            <h3 style="color: #2196F3;">Admin Dashboard</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Tabs for different admin functions
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard",
        "📅 Appointments",
        "⚙️ System",
        "👥 Users",
        "📝 Feedback",
        "💬 Chat Logs"
    ])
    
    # ====================================================================
    # Dashboard Tab
    # ====================================================================
    with tab1:
        st.subheader("📊 System Overview")
        
        # Get system status
        status_data = call_backend_auth(
            "/admin/system-status",
            token=st.session_state.admin_token
        )
        
        if status_data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "System Status",
                    status_data.get('status', 'N/A').upper(),
                    delta="🟢 Operational"
                )
            
            with col2:
                kb_status = "✅ Initialized" if status_data.get('knowledge_base', {}).get('initialized') else "❌ Not Initialized"
                st.metric("Knowledge Base", kb_status)
            
            with col3:
                db_status = "✅ Ready" if status_data.get('database', {}).get('initialized') else "❌ Not Ready"
                st.metric("Database", db_status)
            
            st.info(f"Last updated: {status_data.get('timestamp', 'N/A')}")
        
        st.divider()
        
        # Get appointments analytics
        st.subheader("📈 Appointments Analytics")
        
        apt_data = call_backend_auth(
            "/admin/appointments",
            token=st.session_state.admin_token
        )
        
        if apt_data:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Appointments", apt_data.get('total_appointments', 0))
            
            with col2:
                st.metric("Confirmed", apt_data.get('confirmed', 0))
            
            with col3:
                st.metric("Pending", apt_data.get('pending', 0))
            
            with col4:
                st.metric("Services", len(apt_data.get('by_type', {})))

            feedback_data = call_backend_auth("/admin/feedback", token=st.session_state.admin_token) or []
            chat_data = call_backend_auth("/admin/chat-logs", token=st.session_state.admin_token) or []
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Feedback submissions", len(feedback_data))
            with col2:
                st.metric("Chat interactions", len(chat_data))
            with col3:
                st.metric("Unique chat IPs", len({row.get('ip_address') for row in chat_data if row.get('ip_address')}))
            
            st.divider()
            
            # Appointments by type
            st.subheader("Appointments by Service Type")
            by_type = apt_data.get('by_type', {})
            if by_type:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.bar_chart(data=by_type)
                
                with col2:
                    type_details = ""
                    for service_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
                        type_details += f"• **{service_type}**: {count} appointments\n"
                    st.markdown(type_details)

            status_counts = {
                "Confirmed": apt_data.get('confirmed', 0),
                "Pending": apt_data.get('pending', 0),
                "Other": max(0, apt_data.get('total_appointments', 0) - apt_data.get('confirmed', 0) - apt_data.get('pending', 0)),
            }
            st.subheader("Appointment Status Dashboard")
            st.bar_chart(status_counts)
    
    # ====================================================================
    # Appointments Tab
    # ====================================================================
    with tab2:
        st.subheader("📅 Appointments Management")
        
        # Get appointments
        apt_data = call_backend_auth(
            "/admin/appointments",
            token=st.session_state.admin_token
        )
        
        if apt_data:
            appointments = apt_data.get('appointments', [])
            
            if appointments:
                st.info(f"Showing {len(appointments)} most recent appointments")
                
                # Display appointments in a table
                for apt in appointments[:20]:  # Show first 20
                    with st.container(border=True):
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                        
                        with col1:
                            st.markdown(f"**{apt.get('name', 'N/A')}**")
                            st.caption(f"ID: {apt.get('id', 'N/A')} | Patient ID: {apt.get('patient_id', 'N/A')}")
                        
                        with col2:
                            st.caption(f"🏥 {apt.get('type', 'N/A')}")
                        
                        with col3:
                            st.caption(f"📅 {apt.get('datetime', 'N/A')}")
                        
                        with col4:
                            status_color = "🟢" if apt.get('status') == 'confirmed' else "🟡"
                            st.caption(f"{status_color} {apt.get('status', 'N/A').upper()}")
            else:
                st.info("No appointments found")
    
    # ====================================================================
    # System Tab
    # ====================================================================
    with tab3:
        st.subheader("⚙️ System Management")
        
        # Get system status
        status_data = call_backend_auth(
            "/admin/system-status",
            token=st.session_state.admin_token
        )
        
        if status_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("System Components")
                st.json(status_data)
        
        st.divider()
        
        # Rebuild Knowledge Base
        st.subheader("🔄 Rebuild Hospital Knowledge Base")
        st.warning("⚠️ This will delete the current knowledge base and rebuild from source documents. This may take several minutes.")
        
        if st.button("🔨 Rebuild Knowledge Base", use_container_width=True, type="primary"):
            with st.spinner("Building hospital knowledge base from documents..."):
                result = call_backend_auth(
                    "/admin/rebuild-kb",
                    method="POST",
                    token=st.session_state.admin_token
                )
                
                if result and result.get('success'):
                    st.success("✅ Knowledge base rebuilt successfully!")
                    st.json(result)
                elif result:
                    st.warning(f"⚠️ {result.get('message', 'Rebuild completed with warnings')}")
                    st.json(result)
                else:
                    st.error("❌ Rebuild failed. Please check the backend logs.")
    
    # ====================================================================
    # Users Tab
    # ====================================================================
    with tab4:
        st.subheader("👥 Admin User Management")
        
        st.info("Manage admin accounts and permissions")
        
        with st.form("create_admin_form"):
            st.markdown("#### Create Dashboard User")
            
            new_username = st.text_input("Username", placeholder="Enter username")
            new_password = st.text_input("Password", placeholder="Enter password", type="password")
            confirm_password = st.text_input("Confirm Password", placeholder="Confirm password", type="password")
            new_role = st.selectbox(
                "Access level",
                ["viewer", "support", "scheduler", "analyst", "systems_manager", "admin"],
                format_func=lambda role: role.replace("_", " ").title(),
            )
            
            submitted = st.form_submit_button("➕ Create Admin User", use_container_width=True)
            
            if submitted:
                if not new_username or not new_password:
                    st.error("❌ Username and password are required")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    result = call_backend_auth(
                        f"/admin/create-user?username={quote(new_username)}&password={quote(new_password)}&role={quote(new_role)}",
                        method="POST",
                        token=st.session_state.admin_token
                    )
                    
                    if result and result.get('success'):
                        st.success(f"✅ {result.get('message', 'User created successfully')}")
                    else:
                        st.error("❌ Failed to create user")
        
        st.divider()
        users = call_backend_auth("/admin/users", token=st.session_state.admin_token)
        if users:
            st.dataframe(users, use_container_width=True, hide_index=True)
        st.info("✓ Use strong passwords for all dashboard users\n✓ Assign the least access required for each role")

    with tab5:
        st.subheader("📝 User Feedback")
        feedback = call_backend_auth("/admin/feedback", token=st.session_state.admin_token)
        if feedback:
            st.dataframe(feedback, use_container_width=True, hide_index=True)
        else:
            st.info("No feedback submitted yet.")

    with tab6:
        st.subheader("💬 Chat Audit Log")
        st.caption("Chat records are retained with the originating client IP address for system monitoring.")
        ip_filter = st.text_input("Filter by IP address", key="chat_log_ip")
        endpoint = "/admin/chat-logs"
        if ip_filter.strip():
            endpoint += f"?ip_address={quote(ip_filter.strip())}"
        logs = call_backend_auth(endpoint, token=st.session_state.admin_token)
        if logs:
            st.dataframe(logs, use_container_width=True, hide_index=True)
        else:
            st.info("No chat logs found.")


# ============================================================================
# Main Application
# ============================================================================

def main():
    initialize_session_state()
    
    # Check backend connectivity
    try:
        health = requests.get(f"{BACKEND_URL}/health", timeout=2).json()
    except:
        st.error("❌ Cannot connect to backend API. Make sure the backend is running on port 8000.")
        st.stop()
    
    # Show login page if not authenticated
    if not st.session_state.admin_token:
        show_login_page()
    else:
        show_admin_dashboard()


if __name__ == "__main__":
    main()
