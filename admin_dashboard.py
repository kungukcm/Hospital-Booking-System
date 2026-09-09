"""
Admin Dashboard for Hospital Appointment System
Protected admin interface for management and analytics
Requires authentication to access
"""

import streamlit as st
import requests
import logging
import os
import pandas as pd
from html import escape
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


def _report_bar_chart(title: str, values: dict) -> str:
    """Render simple self-contained bars so downloaded reports need no external assets."""
    if not values:
        return f"<section><h2>{escape(title)}</h2><p>No data recorded.</p></section>"
    maximum = max(values.values()) or 1
    bars = "".join(
        f'<div class="bar-row"><span>{escape(str(label))}</span>'
        f'<div class="bar"><i style="width:{(count / maximum) * 100:.0f}%"></i></div>'
        f'<b>{count}</b></div>'
        for label, count in values.items()
    )
    return f"<section><h2>{escape(title)}</h2>{bars}</section>"


def build_system_report_html(report: dict) -> str:
    """Create a portable management report from the complete API snapshot."""
    quality = report.get("chat_quality", {})
    language = report.get("language", {})
    appointments = report.get("appointments", {})
    emails = report.get("email_notifications", [])
    email_counts = {status: sum(item.get("status") == status for item in emails) for status in ("sent", "failed", "skipped")}
    metrics = {
        "Chats": quality.get("total_chats", 0),
        "Flagged chats": quality.get("flagged_count", 0),
        "Appointments": appointments.get("total", 0),
        "Confirmed appointments": appointments.get("confirmed", 0),
        "Feedback submissions": report.get("feedback", {}).get("total_feedback", 0),
        "Unique visitor IPs": len(report.get("visitor_ips", [])),
    }
    metric_cards = "".join(f"<div class=\"metric\"><b>{value}</b><span>{escape(label)}</span></div>" for label, value in metrics.items())
    trend = {item.get("date", "Unknown"): item.get("avg_response_time_ms", 0) for item in quality.get("performance_trend", [])}
    language_success = {
        "English successful": language.get("successful_responses", {}).get("english", 0),
        "Swahili successful": language.get("successful_responses", {}).get("swahili", 0),
    }
    visitor_rows = "".join(
        f"<tr><td>{escape(str(item.get('ip_address', '')))}</td><td>{escape(str(item.get('first_seen', '')))}</td><td>{escape(str(item.get('last_seen', '')))}</td><td>{item.get('hit_count', 0)}</td></tr>"
        for item in report.get("visitor_ips", [])
    ) or "<tr><td colspan=\"4\">No visitor IPs recorded.</td></tr>"
    return f"""<!doctype html><html><head><meta charset=\"utf-8\"><title>System Management Report</title>
    <style>body{{font:14px Arial,sans-serif;color:#152238;margin:36px;background:#f6f8fb}}h1{{margin-bottom:4px}}h2{{font-size:18px;margin:0 0 14px}}section{{background:#fff;padding:20px;margin:18px 0;border:1px solid #dce3ec;border-radius:6px}}.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.metric{{background:#eef6fb;padding:14px;border-radius:5px}}.metric b{{display:block;font-size:25px;color:#126b8d}}.metric span{{color:#526276}}.bar-row{{display:grid;grid-template-columns:190px 1fr 40px;gap:10px;align-items:center;margin:9px 0}}.bar{{height:14px;background:#edf1f6;border-radius:7px;overflow:hidden}}.bar i{{display:block;height:100%;background:#198b9b;border-radius:7px}}table{{width:100%;border-collapse:collapse}}td,th{{padding:8px;text-align:left;border-bottom:1px solid #dce3ec}}@media print{{body{{background:#fff;margin:16px}}section{{break-inside:avoid}}}}</style></head><body>
    <h1>System Management Report</h1><p>Generated: {escape(str(report.get('generated_at', '')))}</p>
    <section><h2>Management Summary</h2><div class=\"metrics\">{metric_cards}</div></section>
    {_report_bar_chart('Chat Language Usage', language.get('language_counts', {}))}
    {_report_bar_chart('Successful Responses by Language', language_success)}
    {_report_bar_chart('Language Switches', language.get('switches', {}))}
    {_report_bar_chart('System Performance: Average Response Time (ms) by Day', trend)}
    {_report_bar_chart('Appointment Types', appointments.get('by_type', {}))}
    {_report_bar_chart('Email Notification Outcomes', email_counts)}
    <section><h2>Language Switch Rates</h2><p>English to Swahili: {language.get('switch_rate_pct', {}).get('english_to_swahili', 0)}% | Swahili to English: {language.get('switch_rate_pct', {}).get('swahili_to_english', 0)}%</p></section>
    <section><h2>Visitor IP Addresses</h2><table><tr><th>IP address</th><th>First seen</th><th>Last seen</th><th>Hits</th></tr>{visitor_rows}</table></section>
    </body></html>"""


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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        "📊 Dashboard",
        "📅 Appointments",
        "⚙️ System",
        "👥 Users",
        "📝 Feedback",
        "💬 Chat Logs",
        "🩺 Chat Quality",
        "📧 Email Notifications",
        "🌐 Visitor IPs",
        "🗣️ Language Analytics",
        "📄 Full Report"
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
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Total Appointments", apt_data.get('total_appointments', 0))

            with col2:
                st.metric("Confirmed", apt_data.get('confirmed', 0))

            with col3:
                st.metric("Pending", apt_data.get('pending', 0))

            with col4:
                st.metric("Cancelled", apt_data.get('cancelled', 0))

            with col5:
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
                "Cancelled": apt_data.get('cancelled', 0),
                "Other": max(0, apt_data.get('total_appointments', 0) - apt_data.get('confirmed', 0) - apt_data.get('pending', 0) - apt_data.get('cancelled', 0)),
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
                            status = apt.get('status', 'N/A')
                            if status == 'confirmed':
                                status_color = "🟢"
                            elif status == 'cancelled':
                                status_color = "🔴"
                            else:
                                status_color = "🟡"
                            st.caption(f"{status_color} {status.upper()}")
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
        stats = call_backend_auth("/admin/feedback-stats", token=st.session_state.admin_token)

        if stats and stats.get("total_feedback"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total feedback submissions", stats.get("total_feedback", 0))
            with col2:
                avg_effort = stats.get("avg_natural_effort")
                st.metric("Avg. low-effort rating (1-5)", f"{avg_effort:.2f}" if avg_effort is not None else "N/A")

            st.divider()
            st.markdown("### 📊 Multiple-Choice Question Breakdown")
            for question in stats.get("questions", []):
                counts = question.get("counts") or {}
                if not counts:
                    continue
                st.markdown(f"**{question['label']}**")
                chart_df = pd.DataFrame(
                    {"Responses": list(counts.values())},
                    index=list(counts.keys()),
                )
                st.bar_chart(chart_df)

            effort_dist = stats.get("natural_effort_distribution") or {}
            if effort_dist:
                st.markdown("**Natural / low-effort rating (1 = hard, 5 = effortless)**")
                st.bar_chart(pd.DataFrame({"Responses": list(effort_dist.values())}, index=list(effort_dist.keys())))
        else:
            st.info("No feedback submitted yet.")

        st.divider()
        st.markdown("### 📋 Raw Feedback Records")
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

    with tab7:
        st.subheader("🩺 Chat Responsiveness & Hallucination Tracking")
        st.caption("Flags responses that were slow, empty, or fell back to an error message (possible hallucination/failure).")
        quality = call_backend_auth("/admin/chat-quality", token=st.session_state.admin_token)
        if quality:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total chats", quality.get("total_chats", 0))
            with col2:
                st.metric("Flagged", quality.get("flagged_count", 0), delta=f"{quality.get('flagged_rate_pct', 0)}%")
            with col3:
                avg_ms = quality.get("avg_response_time_ms")
                st.metric("Avg response time", f"{avg_ms:.0f} ms" if avg_ms is not None else "N/A")
            with col4:
                st.metric("Slow responses (>8s)", quality.get("slow_response_count", 0))

            st.divider()
            st.markdown("**Recent flagged interactions**")
            recent = quality.get("recent_flagged") or []
            if recent:
                st.dataframe(recent, use_container_width=True, hide_index=True)
            else:
                st.info("No flagged interactions recorded.")
        else:
            st.info("No chat quality data available yet.")

    with tab8:
        st.subheader("📧 Appointment Confirmation Emails")
        st.caption("Record of confirmation emails sent to patients after booking.")
        notifications = call_backend_auth("/admin/email-notifications", token=st.session_state.admin_token)
        if notifications:
            sent = len([n for n in notifications if n.get("status") == "sent"])
            failed = len([n for n in notifications if n.get("status") == "failed"])
            skipped = len([n for n in notifications if n.get("status") == "skipped"])
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sent", sent)
            with col2:
                st.metric("Failed", failed)
            with col3:
                st.metric("Skipped (SMTP not configured)", skipped)
            st.divider()
            st.dataframe(notifications, use_container_width=True, hide_index=True)
        else:
            st.info("No confirmation emails recorded yet.")

    with tab9:
        st.subheader("🌐 Unique Visitor IP Addresses")
        st.caption("Every distinct IP address that has used the chat, feedback, or booking flow, with first/last seen and visit count.")
        visitor_ips = call_backend_auth("/admin/visitor-ips", token=st.session_state.admin_token)
        if visitor_ips:
            st.metric("Unique IP addresses", len(visitor_ips))
            st.divider()
            st.dataframe(visitor_ips, use_container_width=True, hide_index=True)
        else:
            st.info("No visitor IP addresses recorded yet.")

    with tab10:
        st.subheader("🗣️ Chat Language and Success Analytics")
        language_stats = call_backend_auth("/admin/language-stats", token=st.session_state.admin_token)
        quality_stats = call_backend_auth("/admin/chat-quality", token=st.session_state.admin_token)
        if language_stats:
            counts = language_stats.get("language_counts", {})
            successful = language_stats.get("successful_responses", {})
            rates = language_stats.get("success_rate_pct", {})
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("English chats", counts.get("english", 0))
            with col2:
                st.metric("Swahili chats", counts.get("swahili", 0))
            with col3:
                st.metric("Successful English", successful.get("english", 0), delta=f"{rates.get('english', 0)}% success")
            with col4:
                st.metric("Successful Swahili", successful.get("swahili", 0), delta=f"{rates.get('swahili', 0)}% success")

            st.markdown("**Chats by language**")
            st.bar_chart(pd.DataFrame({"Chats": [counts.get("english", 0), counts.get("swahili", 0)]}, index=["English", "Swahili"]))
            st.markdown("**Successful responses by language**")
            st.bar_chart(pd.DataFrame({"Successful responses": [successful.get("english", 0), successful.get("swahili", 0)]}, index=["English", "Swahili"]))

            switches = language_stats.get("switches", {})
            switch_rates = language_stats.get("switch_rate_pct", {})
            col1, col2 = st.columns(2)
            with col1:
                st.metric("English to Swahili switches", switches.get("english_to_swahili", 0), delta=f"{switch_rates.get('english_to_swahili', 0)}% rate")
            with col2:
                st.metric("Swahili to English switches", switches.get("swahili_to_english", 0), delta=f"{switch_rates.get('swahili_to_english', 0)}% rate")

        if quality_stats and quality_stats.get("performance_trend"):
            st.divider()
            st.markdown("**System performance: average chat response time by day (ms)**")
            trend_df = pd.DataFrame(quality_stats["performance_trend"])
            st.line_chart(trend_df.set_index("date")[["avg_response_time_ms"]])
        elif language_stats:
            st.info("Response-time trend will appear after timed chat records are collected.")

    with tab11:
        st.subheader("📄 Full Management Report")
        st.caption("Generates a portable HTML report with dashboard totals, charts, performance, language, feedback, email, appointment, and visitor-IP data.")
        report = call_backend_auth("/admin/system-report", token=st.session_state.admin_token)
        if report:
            st.download_button(
                "Download Full Report (HTML)",
                data=build_system_report_html(report),
                file_name=f"system-management-report-{datetime.now().strftime('%Y-%m-%d')}.html",
                mime="text/html",
                use_container_width=True,
            )
            st.json({
                "generated_at": report.get("generated_at"),
                "system_status": report.get("system_status"),
                "appointments": report.get("appointments"),
            })


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
