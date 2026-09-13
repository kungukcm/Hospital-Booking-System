"""
Admin Dashboard for Hospital Appointment System
Protected admin interface for management and analytics with privacy/PII masking,
rich multi-colored visualizations, comprehensive chat quality tracking, and full reporting.
"""

import streamlit as st
import requests
import logging
import os
import re
import pandas as pd
import altair as alt
from html import escape
from datetime import datetime
from urllib.parse import quote
from typing import Any, Dict, List, Optional
from appointments_db import normalize_appointment_type

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
    page_title="KUTRRH Admin Management Dashboard",
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Privacy & PII Masking Utilities
# ============================================================================

def mask_name(name: Optional[str], enabled: bool = True) -> str:
    """Mask full name while preserving first letters, e.g. 'John Doe' -> 'J*** D**'."""
    if not enabled:
        return str(name or "N/A")
    if not name or not isinstance(name, str) or not name.strip():
        return "N/A"
    parts = name.strip().split()
    masked_parts = []
    for part in parts:
        if len(part) <= 1:
            masked_parts.append(part + "***")
        elif len(part) == 2:
            masked_parts.append(part[0] + "*")
        else:
            masked_parts.append(part[0] + "*" * (len(part) - 1))
    return " ".join(masked_parts)


def mask_phone(phone: Optional[str], enabled: bool = True) -> str:
    """Mask phone number, keeping country/network prefix and ending digits."""
    if not enabled:
        return str(phone or "N/A")
    if not phone or not isinstance(phone, str) or not phone.strip():
        return "N/A"
    s = phone.strip()
    if len(s) <= 4:
        return "****"
    prefix_len = 4 if s.startswith("+") else 3
    suffix_len = 2
    if len(s) <= prefix_len + suffix_len:
        return s[:2] + "*" * (len(s) - 3) + s[-1:]
    return s[:prefix_len] + "*" * (len(s) - prefix_len - suffix_len) + s[-suffix_len:]


def mask_email(email: Optional[str], enabled: bool = True) -> str:
    """Mask email address, e.g. 'jane.doe@example.com' -> 'j******e@example.com'."""
    if not enabled:
        return str(email or "N/A")
    if not email or not isinstance(email, str) or "@" not in email:
        return "***@***" if email else "N/A"
    name_part, domain_part = email.strip().split("@", 1)
    if len(name_part) <= 2:
        masked_name = name_part[:1] + "***"
    else:
        masked_name = name_part[0] + "*" * max(2, len(name_part) - 2) + name_part[-1]
    return f"{masked_name}@{domain_part}"


def mask_ip(ip: Optional[str], enabled: bool = True) -> str:
    """Mask IPv4 / IPv6 address, e.g. '192.168.1.105' -> '192.168.***.***'."""
    if not enabled:
        return str(ip or "N/A")
    if not ip or not isinstance(ip, str) or not ip.strip():
        return "N/A"
    ip_str = ip.strip()
    if ":" in ip_str:
        parts = ip_str.split(":")
        return ":".join(parts[:2] + ["****", "****"])
    parts = ip_str.split(".")
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.***.***"
    return re.sub(r"\d+$", "***", ip_str)


def mask_patient_id(pid: Optional[str], enabled: bool = True) -> str:
    """Mask patient ID, e.g. 'P-1001' -> 'P-**01'."""
    if not enabled:
        return str(pid or "N/A")
    if not pid or not isinstance(pid, str) or not pid.strip():
        return "N/A"
    s = pid.strip()
    if len(s) <= 3:
        return s[:1] + "**"
    return s[:2] + "*" * max(1, len(s) - 4) + s[-2:]


def anonymize_text(text: Optional[str], enabled: bool = True) -> str:
    """Scrub potential emails, phones, and IPs from arbitrary log text when masking is active."""
    if not enabled or not text or not isinstance(text, str):
        return str(text or "")
    text = re.sub(r'([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', r'\1***@\2', text)
    text = re.sub(r'(\+?254|0)?(7\d{2}|\d{3})(\d{3})(\d{3})', r'\1\2****\4', text)
    text = re.sub(r'(\b\d{1,3}\.\d{1,3}\.)\d{1,3}\.\d{1,3}\b', r'\1***.***', text)
    return text


# ============================================================================
# Altair Visualizations Helper (Multi-colored, Legends, Data Labels)
# ============================================================================

PALETTES = {
    "vibrant": [
        "#1976D2", "#2E7D32", "#F57C00", "#7B1FA2", "#0097A7", "#D32F2F",
        "#C2185B", "#388E3C", "#5D4037", "#0288D1", "#6A1B9A", "#00838F",
        "#EF6C00", "#AD1457", "#4527A0", "#00695C", "#9E9D24", "#4E342E",
        "#1565C0", "#558B2F", "#C62828", "#283593", "#00897B", "#F9A825",
    ],
    "status": ["#2E7D32", "#F57C00", "#D32F2F", "#757575"],
    "quality": ["#2E7D32", "#D32F2F", "#F57C00", "#7B1FA2", "#0097A7"],
}

def render_colored_bar_chart(
    df: pd.DataFrame,
    category_col: str,
    value_col: str,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    legend_title: Optional[str] = None,
    color_scheme: str = "tableau10",
    height: int = 320,
    horizontal: bool = False
):
    """Render a multi-colored bar chart with explicit data labels and legend."""
    if df.empty:
        st.info(f"No data available for {title}")
        return

    legend_title = legend_title or category_col
    categories = [str(value) for value in df[category_col].tolist()]
    if len(categories) <= len(PALETTES["vibrant"]):
        color_scale = alt.Scale(
            domain=categories,
            range=PALETTES["vibrant"][:len(categories)],
        )
    else:
        color_scale = alt.Scale(domain=categories, scheme=color_scheme)
    if horizontal:
        bars = alt.Chart(df).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
            y=alt.Y(f"{category_col}:N", sort='-x', title=y_label or category_col, axis=alt.Axis(labelLimit=0, labelOverlap=False)),
            x=alt.X(f"{value_col}:Q", title=x_label or value_col),
            color=alt.Color(f"{category_col}:N", scale=color_scale, legend=alt.Legend(title=legend_title, orient="right")),
            tooltip=[f"{category_col}:N", f"{value_col}:Q"]
        )
        text = alt.Chart(df).mark_text(dx=12, fontSize=11, fontWeight="bold", color="#152238").encode(
            y=alt.Y(f"{category_col}:N", sort='-x'),
            x=alt.X(f"{value_col}:Q"),
            text=alt.Text(f"{value_col}:Q")
        )
    else:
        bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X(f"{category_col}:N", sort='-y', title=x_label or category_col, axis=alt.Axis(labelAngle=-25, labelLimit=0, labelOverlap=False)),
            y=alt.Y(f"{value_col}:Q", title=y_label or value_col),
            color=alt.Color(f"{category_col}:N", scale=color_scale, legend=alt.Legend(title=legend_title, orient="right")),
            tooltip=[f"{category_col}:N", f"{value_col}:Q"]
        )
        text = alt.Chart(df).mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#152238").encode(
            x=alt.X(f"{category_col}:N", sort='-y'),
            y=alt.Y(f"{value_col}:Q"),
            text=alt.Text(f"{value_col}:Q")
        )

    chart = (bars + text).properties(
        title=alt.TitleParams(text=title, fontSize=14, fontWeight="bold", color="#152238"),
        height=max(height, len(categories) * 34 if horizontal else height)
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


def render_donut_chart(
    df: pd.DataFrame,
    category_col: str,
    value_col: str,
    title: str,
    legend_title: Optional[str] = None,
    color_scale: Optional[alt.Scale] = None,
    color_scheme: str = "tableau10",
    height: int = 300
):
    """Render a multi-colored donut chart with legend and interactive hover details."""
    if df.empty or df[value_col].sum() == 0:
        st.info(f"No data available for {title}")
        return

    legend_title = legend_title or category_col
    color_enc = alt.Color(
        f"{category_col}:N",
        scale=color_scale or alt.Scale(scheme=color_scheme),
        legend=alt.Legend(title=legend_title, orient="right")
    )

    donut = alt.Chart(df).mark_arc(innerRadius=60, outerRadius=110).encode(
        theta=alt.Theta(f"{value_col}:Q"),
        color=color_enc,
        tooltip=[f"{category_col}:N", f"{value_col}:Q"]
    ).properties(
        title=alt.TitleParams(text=title, fontSize=14, fontWeight="bold", color="#152238"),
        height=height
    ).configure_view(strokeWidth=0)

    st.altair_chart(donut, use_container_width=True)


def render_line_trend_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    x_title: str = "Date",
    y_title: str = "Average Latency (ms)",
    line_color: str = "#1976D2",
    height: int = 320
):
    """Render a smooth line chart with points, data labels, and tooltips."""
    if df.empty:
        st.info(f"No data available for {title}")
        return

    line = alt.Chart(df).mark_line(point=True, color=line_color, strokeWidth=3).encode(
        x=alt.X(f"{x_col}:N", title=x_title, axis=alt.Axis(labelAngle=-30)),
        y=alt.Y(f"{y_col}:Q", title=y_title),
        tooltip=[f"{x_col}:N", f"{y_col}:Q"]
    )

    points = alt.Chart(df).mark_point(size=60, color=line_color, fill="#ffffff").encode(
        x=alt.X(f"{x_col}:N"),
        y=alt.Y(f"{y_col}:Q")
    )

    text = alt.Chart(df).mark_text(dy=-10, fontSize=10, fontWeight="bold", color="#152238").encode(
        x=alt.X(f"{x_col}:N"),
        y=alt.Y(f"{y_col}:Q"),
        text=alt.Text(f"{y_col}:Q")
    )

    chart = (line + points + text).properties(
        title=alt.TitleParams(text=title, fontSize=14, fontWeight="bold", color="#152238"),
        height=height
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True)


# ============================================================================
# Authentication Management
# ============================================================================

def call_backend_auth(endpoint: str, method: str = "GET", data: dict = None, token: str = None) -> Any:
    """Call backend API with optional authentication"""
    url = f"{BACKEND_URL}{endpoint}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Backend API error ({endpoint}): {str(e)}")
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
# Full System Report HTML Builder (Multi-Colored Visuals, PII Masking, Complete Data)
# ============================================================================

def _build_html_bar_chart(title: str, data: Dict[str, Any], colors: List[str] = None) -> str:
    """Generate clean self-contained multi-colored CSS/SVG bar chart for standalone HTML reports."""
    if not data or not any(data.values()):
        return f"<div class=\"card\"><h3>{escape(title)}</h3><p class=\"muted\">No data recorded.</p></div>"
    
    colors = colors or PALETTES["vibrant"]
    max_val = max(data.values()) or 1
    total = sum(data.values()) or 1

    bars_html = ""
    for idx, (label, val) in enumerate(data.items()):
        color = colors[idx % len(colors)]
        pct = (val / total) * 100
        bar_pct = (val / max_val) * 100
        bars_html += f"""
        <div class="chart-row">
            <span class="chart-label" title="{escape(str(label))}">{escape(str(label))}</span>
            <div class="chart-bar-wrap">
                <div class="chart-bar" style="width: {bar_pct:.1f}%; background-color: {color};"></div>
            </div>
            <span class="chart-val"><b>{val}</b> <small>({pct:.1f}%)</small></span>
        </div>
        """

    legend_items = "".join(
        f'<div class="legend-item"><span class="legend-dot" style="background:{colors[i % len(colors)]}"></span>{escape(str(lbl))}</div>'
        for i, lbl in enumerate(data.keys())
    )

    return f"""
    <div class="card">
        <h3>{escape(title)}</h3>
        <div class="chart-container">{bars_html}</div>
        <div class="legend-box">{legend_items}</div>
    </div>
    """


def _build_html_pie_chart(title: str, data: Dict[str, Any], colors: List[str] = None) -> str:
    """Generate a self-contained pie chart with percentages, labels, and a legend."""
    values = {str(label): float(value or 0) for label, value in data.items()}
    values = {label: value for label, value in values.items() if value > 0}
    if not values:
        return f'<div class="card"><h3>{escape(title)}</h3><p class="muted">No data recorded.</p></div>'

    colors = colors or PALETTES["vibrant"]
    total = sum(values.values())
    start = 0.0
    stops = []
    legend_items = []
    for index, (label, value) in enumerate(values.items()):
        end = start + (value / total) * 360
        color = colors[index % len(colors)]
        stops.append(f"{color} {start:.2f}deg {end:.2f}deg")
        percentage = (value / total) * 100
        legend_items.append(
            f'<div class="legend-item"><span class="legend-dot" style="background:{color}"></span>'
            f'{escape(label)}: <b>{value:g}</b> ({percentage:.1f}%)</div>'
        )
        start = end

    return f"""
    <div class="card pie-card">
        <h3>{escape(title)}</h3>
        <div class="pie-layout">
            <div class="pie-chart" style="background: conic-gradient({', '.join(stops)});" role="img" aria-label="{escape(title)}"></div>
            <div class="legend-box pie-legend">{''.join(legend_items)}</div>
        </div>
    </div>
    """


def _build_html_line_chart(title: str, data: Dict[str, Any], line_color: str = "#1976D2") -> str:
    """Generate a self-contained SVG line chart with point values and date labels."""
    points_data = [(str(label), float(value or 0)) for label, value in data.items()]
    if not points_data:
        return f'<div class="card"><h3>{escape(title)}</h3><p class="muted">No data recorded.</p></div>'

    width, height = 760, 300
    left, right, top, bottom = 58, 20, 28, 62
    plot_width = width - left - right
    plot_height = height - top - bottom
    maximum = max(value for _, value in points_data) or 1
    step = plot_width / max(1, len(points_data) - 1)

    coordinates = []
    for index, (label, value) in enumerate(points_data):
        x = left + index * step
        y = top + plot_height - (value / maximum) * plot_height
        coordinates.append((x, y, label, value))

    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in coordinates)
    grid_lines = "".join(
        f'<line x1="{left}" y1="{y}" x2="{width - right}" y2="{y}" stroke="#DCE3EC" stroke-width="1"/>'
        f'<text x="{left - 8}" y="{y + 4}" text-anchor="end" class="axis-label">{maximum * ratio:.0f}</text>'
        for ratio in (0, 0.25, 0.5, 0.75, 1)
        for y in (top + plot_height - ratio * plot_height,)
    )
    markers = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#fff" stroke="{line_color}" stroke-width="3"/>'
        f'<text x="{x:.1f}" y="{y - 10:.1f}" text-anchor="middle" class="point-label">{value:.0f}</text>'
        f'<text x="{x:.1f}" y="{height - 25}" text-anchor="middle" class="axis-label">{escape(label[-10:])}</text>'
        for x, y, label, value in coordinates
    )

    return f"""
    <div class="card line-card">
        <h3>{escape(title)}</h3>
        <svg class="line-chart" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
            {grid_lines}
            <polyline points="{polyline}" fill="none" stroke="{line_color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
            {markers}
            <text x="{left}" y="16" class="axis-title">Value</text>
            <text x="{width / 2}" y="{height - 2}" text-anchor="middle" class="axis-title">Date</text>
        </svg>
        <div class="legend-box"><div class="legend-item"><span class="legend-dot" style="background:{line_color}"></span>{escape(title)}</div></div>
    </div>
    """


def _safe_number(value: Any, default: float = 0.0) -> float:
    """Convert nullable API values to numbers for report formatting."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_system_report_html(report: dict, mask_pii: bool = True) -> str:
    """Create a complete, high-quality, multi-colored management HTML report."""
    quality = report.get("chat_quality", {})
    language = report.get("language", {})
    appointments_meta = report.get("appointments", {})
    all_appointments = appointments_meta.get("all_appointments", [])
    feedback_records = report.get("feedback_records", [])
    visitor_ips = report.get("visitor_ips", [])
    emails = report.get("email_notifications", [])
    system_status = report.get("system_status", {})
    feedback_stats = report.get("feedback", {})

    total_chats = quality.get("total_chats", 0)
    successful_chats = quality.get("successful_count", max(0, total_chats - quality.get("flagged_count", 0)))
    error_fallbacks = quality.get("error_fallback_count", 0)
    error_fallback_pct = quality.get("error_fallback_rate_pct", round((error_fallbacks / total_chats * 100), 1) if total_chats else 0.0)
    slow_chats = quality.get("slow_response_count", 0)
    slow_chats_pct = quality.get("slow_response_rate_pct", round((slow_chats / total_chats * 100), 1) if total_chats else 0.0)
    avg_latency = _safe_number(quality.get("avg_response_time_ms"))

    email_counts = {
        "Delivered / Sent": sum(item.get("status") == "sent" for item in emails),
        "Failed Delivery": sum(item.get("status") == "failed" for item in emails),
        "Skipped (No SMTP)": sum(item.get("status") == "skipped" for item in emails),
    }

    # Group appointments by normalized canonical specialty
    normalized_by_type = {}
    if all_appointments:
        for apt in all_appointments:
            canon = normalize_appointment_type(apt.get('type', 'Unknown')) or "General Check-up"
            normalized_by_type[canon] = normalized_by_type.get(canon, 0) + 1
    else:
        for k, v in appointments_meta.get('by_type', {}).items():
            canon = normalize_appointment_type(k) or "General Check-up"
            normalized_by_type[canon] = normalized_by_type.get(canon, 0) + v

    # Appointment status counts
    apt_status_counts = {
        "Confirmed Bookings": sum(item.get("status") == "confirmed" for item in all_appointments),
        "Pending Bookings": sum(item.get("status") == "pending" for item in all_appointments),
        "Cancelled Bookings": sum(item.get("status") == "cancelled" for item in all_appointments),
    }

    quality_chart_data = {
        "Successful Responses": successful_chats,
        "Error / Fallback Responses": error_fallbacks,
        "Slow Responses (>8s)": slow_chats,
        "Empty Responses": quality.get("empty_response_count", 0),
    }

    language_counts = language.get("language_counts", {})
    language_success = language.get("successful_responses", {})
    language_success_rates = language.get("success_rate_pct", {})
    language_switches = language.get("switches", {})
    language_switch_rates = language.get("switch_rate_pct", {})
    language_success_chart = {
        "English successful": language_success.get("english", 0),
        "Swahili successful": language_success.get("swahili", 0),
    }
    language_switch_chart = {
        "English to Swahili": language_switches.get("english_to_swahili", 0),
        "Swahili to English": language_switches.get("swahili_to_english", 0),
    }
    performance_trend = quality.get("performance_trend", [])
    performance_chart = {
        str(item.get("date", "Unknown")): item.get("avg_response_time_ms", 0) or 0
        for item in performance_trend
    }
    performance_error_chart = {
        str(item.get("date", "Unknown")): item.get("error_fallbacks", 0) or 0
        for item in performance_trend
    }
    outcome_pie_chart = _build_html_pie_chart(
        "Chat Response Outcome & Fallback Breakdown",
        quality_chart_data,
        ["#2E7D32", "#D32F2F", "#F57C00", "#757575"],
    )
    performance_line_chart = _build_html_line_chart(
        "System Performance: Average Response Time by Day (ms)",
        performance_chart,
        "#1976D2",
    )
    latency_values = [item.get("avg_response_time_ms") for item in performance_trend if item.get("avg_response_time_ms") is not None]
    performance_summary = (
        f"<p><b>Average response time:</b> {avg_latency:.0f} ms "
        f"| <b>Fastest daily average:</b> {min(latency_values):.0f} ms "
        f"| <b>Slowest daily average:</b> {max(latency_values):.0f} ms "
        f"| <b>Days measured:</b> {len(latency_values)}</p>"
        if latency_values
        else "<p><b>Performance records:</b> No timed response records available.</p>"
    )
    language_summary = f"""
    <div class="card">
        <h2>🗣️ Language Analytics</h2>
        <p><b>Total language-classified chats:</b> {language.get('total_chats', total_chats)} "
        f"| <b>English:</b> {language_counts.get('english', 0)} ({language_success_rates.get('english', 0)}% success) "
        f"| <b>Swahili:</b> {language_counts.get('swahili', 0)} ({language_success_rates.get('swahili', 0)}% success)</p>
        <p><b>English to Swahili switches:</b> {language_switches.get('english_to_swahili', 0)} ({language_switch_rates.get('english_to_swahili', 0)}%) "
        f"| <b>Swahili to English switches:</b> {language_switches.get('swahili_to_english', 0)} ({language_switch_rates.get('swahili_to_english', 0)}%)</p>
        <div class="grid-2">
            {_build_html_bar_chart('Chats by Language', language_counts, ['#1976D2', '#7B1FA2'])}
            {_build_html_bar_chart('Successful Responses by Language', language_success_chart, ['#2E7D32', '#0097A7'])}
            {_build_html_bar_chart('Language Switches', language_switch_chart, ['#F57C00', '#C2185B'])}
        </div>
    </div>
    """
    performance_analytics = f"""
    <div class="card">
        <h2>⚙️ System Performance Analytics</h2>
        {performance_summary}
        <p class="muted">Daily averages and fallback counts are based on timed chat records stored by the system.</p>
        {performance_line_chart}
        <div class="grid-2">
            {_build_html_bar_chart('Average Response Time by Day (ms)', performance_chart, ['#1976D2', '#0097A7', '#7B1FA2'])}
            {_build_html_bar_chart('Error / Fallback Responses by Day', performance_error_chart, ['#D32F2F', '#F57C00', '#C2185B'])}
        </div>
    </div>
    """

    feedback_charts = ""
    for question in feedback_stats.get("questions", []):
        counts = question.get("counts") or {}
        if counts:
            feedback_charts += _build_html_bar_chart(
                question.get("label", question.get("column", "Feedback question")),
                counts,
                PALETTES["vibrant"],
            )
    effort_distribution = feedback_stats.get("natural_effort_distribution") or {}
    if effort_distribution:
        feedback_charts += _build_html_bar_chart(
            "Natural / Low-Effort Rating Distribution (1 = Difficult, 5 = Effortless)",
            {f"Score {key}": value for key, value in effort_distribution.items()},
            PALETTES["quality"],
        )
    rating_values = []
    for record in feedback_records:
        try:
            rating_values.append(int(record.get("rating")))
        except (TypeError, ValueError):
            continue
    rating_distribution = {
        f"Rating {rating}": rating_values.count(rating)
        for rating in range(1, 6)
        if rating_values.count(rating)
    }
    if rating_distribution:
        feedback_charts += _build_html_bar_chart(
            "Overall Feedback Rating Distribution (1-5)",
            rating_distribution,
            PALETTES["quality"],
        )
    average_effort = feedback_stats.get("avg_natural_effort")
    average_rating = sum(rating_values) / len(rating_values) if rating_values else None
    feedback_summary = (
        f"<p><b>Total submissions:</b> {feedback_stats.get('total_feedback', len(feedback_records))} "
        f"| <b>Average rating:</b> {average_rating:.2f} / 5 "
        f"| <b>Average effort rating:</b> {average_effort:.2f} / 5</p>"
        if average_effort is not None
        else f"<p><b>Total submissions:</b> {feedback_stats.get('total_feedback', len(feedback_records))}"
        f" | <b>Average rating:</b> {average_rating:.2f} / 5</p>" if average_rating is not None
        else f"<p><b>Total submissions:</b> {feedback_stats.get('total_feedback', len(feedback_records))}</p>"
    )
    feedback_analytics = f"""
    <div class="card">
        <h2>📊 Feedback Statistics & Visual Analysis</h2>
        {feedback_summary}
        <p class="muted">Each bar includes its response count and percentage of responses for that question. Colors identify answer categories in the legend.</p>
        <div class="grid-2">{feedback_charts or '<p class="muted">No structured feedback statistics recorded.</p>'}</div>
    </div>
    """

    apt_rows = ""
    if all_appointments:
        for apt in all_appointments:
            status = apt.get("status", "unknown").lower()
            status_badge = f"<span class=\"badge badge-{status}\">{escape(status.upper())}</span>"
            c_name = escape(mask_name(apt.get("name"), mask_pii))
            c_pid = escape(mask_patient_id(apt.get("patient_id"), mask_pii))
            c_phone = escape(mask_phone(apt.get("phone"), mask_pii))
            c_email = escape(mask_email(apt.get("email"), mask_pii))
            reason = escape(str(apt.get("cancellation_reason") or apt.get("notes") or "-"))
            apt_rows += f"""
            <tr>
                <td><b>{escape(str(apt.get('id', 'N/A')))}</b></td>
                <td>{c_name}<br><small class="muted">ID: {c_pid}</small></td>
                <td><b>{escape(str(apt.get('type', 'General')))}</b></td>
                <td>{escape(str(apt.get('datetime', 'N/A')))}</td>
                <td>{status_badge}</td>
                <td>{c_phone}<br><small class="muted">{c_email}</small></td>
                <td>{_safe_number(apt.get('predicted_wait_minutes')):.0f} min</td>
                <td>{reason}</td>
            </tr>
            """
    else:
        apt_rows = "<tr><td colspan=\"8\" class=\"text-center\">No appointments recorded.</td></tr>"

    visitor_rows = ""
    if visitor_ips:
        for item in visitor_ips:
            ip_val = escape(mask_ip(item.get("ip_address"), mask_pii))
            visitor_rows += f"""
            <tr>
                <td><code>{ip_val}</code></td>
                <td>{escape(str(item.get('first_seen', '')))}</td>
                <td>{escape(str(item.get('last_seen', '')))}</td>
                <td><b>{item.get('hit_count', 1)}</b></td>
            </tr>
            """
    else:
        visitor_rows = "<tr><td colspan=\"4\" class=\"text-center\">No visitor IPs recorded.</td></tr>"

    feedback_rows = ""
    if feedback_records:
        for fb in feedback_records:
            fb_email = escape(mask_email(fb.get("email"), mask_pii))
            fb_ip = escape(mask_ip(fb.get("ip_address"), mask_pii))
            fb_msg = escape(anonymize_text(fb.get("message") or fb.get("additional_feedback") or "-", mask_pii))
            rating = fb.get("rating", "N/A")
            feedback_rows += f"""
            <tr>
                <td><b>#{fb.get('id', '-')}</b></td>
                <td>{fb_email}<br><small class="muted">{fb_ip}</small></td>
                <td><span class="badge badge-primary">{rating} / 5</span></td>
                <td>{escape(str(fb.get('booking_success') or '-'))}</td>
                <td>{escape(str(fb.get('information_accuracy') or '-'))}</td>
                <td>{escape(str(fb.get('natural_effort') or '-'))}</td>
                <td>{fb_msg}</td>
                <td><small>{escape(str(fb.get('created_at', ''))[:19])}</small></td>
            </tr>
            """
    else:
        feedback_rows = "<tr><td colspan=\"8\" class=\"text-center\">No feedback submitted yet.</td></tr>"

    email_rows = ""
    if emails:
        for em in emails:
            status = em.get("status", "unknown").lower()
            status_badge = f"<span class=\"badge badge-{status}\">{escape(status.upper())}</span>"
            em_recip = escape(mask_email(em.get("recipient_email"), mask_pii))
            email_rows += f"""
            <tr>
                <td><b>#{em.get('id', '-')}</b></td>
                <td>{escape(str(em.get('appointment_id', '-')))}</td>
                <td>{em_recip}</td>
                <td>{escape(str(em.get('subject', '-')))}</td>
                <td>{status_badge}</td>
                <td><small>{escape(str(em.get('created_at', ''))[:19])}</small></td>
            </tr>
            """
    else:
        email_rows = "<tr><td colspan=\"6\" class=\"text-center\">No email notifications logged.</td></tr>"

    mask_notice = (
        "<div class=\"privacy-banner privacy-active\">🛡️ <b>PII Anonymization Enabled:</b> All patient names, phone numbers, email addresses, and IP addresses have been masked in accordance with healthcare data protection guidelines.</div>"
        if mask_pii else
        "<div class=\"privacy-banner privacy-inactive\">⚠️ <b>PII Anonymization Disabled:</b> Unmasked personal patient details are displayed in this report. Handle with strict confidentiality.</div>"
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KUTRRH System Management Report</title>
<style>
    :root {{
        --primary: #1976D2;
        --success: #2E7D32;
        --warning: #F57C00;
        --danger: #D32F2F;
        --purple: #7B1FA2;
        --teal: #0097A7;
        --bg: #F4F7FB;
        --card-bg: #FFFFFF;
        --text: #152238;
        --muted: #607289;
        --border: #DCE3EC;
    }}
    * {{ box-sizing: border-box; }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: var(--text);
        background-color: var(--bg);
        margin: 0;
        padding: 30px;
        line-height: 1.5;
    }}
    .header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid var(--border);
        padding-bottom: 16px;
        margin-bottom: 24px;
    }}
    .header h1 {{ margin: 0 0 6px 0; font-size: 26px; color: var(--primary); }}
    .header p {{ margin: 0; color: var(--muted); font-size: 14px; }}
    .privacy-banner {{
        padding: 12px 18px;
        border-radius: 8px;
        margin-bottom: 24px;
        font-size: 14px;
    }}
    .privacy-active {{ background-color: #E8F5E9; color: #1B5E20; border: 1px solid #A5D6A7; }}
    .privacy-inactive {{ background-color: #FFF3E0; color: #E65100; border: 1px solid #FFCC80; }}
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }}
    .kpi-card {{
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }}
    .kpi-card .val {{ font-size: 28px; font-weight: bold; color: var(--primary); margin-bottom: 4px; }}
    .kpi-card .lbl {{ font-size: 13px; color: var(--muted); text-transform: uppercase; font-weight: 600; }}
    .kpi-card.kpi-danger .val {{ color: var(--danger); }}
    .kpi-card.kpi-success .val {{ color: var(--success); }}
    .kpi-card.kpi-warning .val {{ color: var(--warning); }}
    .grid-2 {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 24px;
    }}
    @media (max-width: 900px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
    .card {{
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }}
    .card h2, .card h3 {{
        margin-top: 0;
        margin-bottom: 16px;
        font-size: 18px;
        color: var(--text);
        border-bottom: 1px solid var(--border);
        padding-bottom: 10px;
    }}
    .chart-container {{ margin: 16px 0; }}
    .chart-row {{
        display: grid;
        grid-template-columns: 220px 1fr 120px;
        gap: 12px;
        align-items: center;
        margin-bottom: 10px;
    }}
    .chart-label {{ font-size: 13px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .chart-bar-wrap {{ background: #EDF2F7; height: 18px; border-radius: 9px; overflow: hidden; }}
    .chart-bar {{ height: 100%; border-radius: 9px; transition: width 0.3s; }}
    .chart-val {{ font-size: 13px; text-align: right; }}
    .legend-box {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 14px;
        padding-top: 10px;
        border-top: 1px dashed var(--border);
    }}
    .legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--muted); }}
    .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
    .pie-layout {{ display: flex; align-items: center; justify-content: center; gap: 28px; flex-wrap: wrap; }}
    .pie-chart {{ width: 220px; height: 220px; border-radius: 50%; border: 8px solid #fff; box-shadow: 0 1px 5px rgba(0,0,0,.12); }}
    .pie-legend {{ display: grid; gap: 8px; border-top: 0; margin-top: 0; padding-top: 0; }}
    .line-chart {{ width: 100%; height: auto; min-height: 250px; overflow: visible; }}
    .axis-label {{ fill: #607289; font-size: 11px; }}
    .axis-title {{ fill: #526276; font-size: 12px; font-weight: 600; }}
    .point-label {{ fill: #152238; font-size: 11px; font-weight: 700; }}
    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        margin-top: 10px;
    }}
    th, td {{
        padding: 10px 12px;
        text-align: left;
        border-bottom: 1px solid var(--border);
    }}
    th {{ background: #F8FAFC; color: var(--muted); font-weight: 600; }}
    tr:hover {{ background-color: #F8FAFC; }}
    .badge {{
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
    }}
    .badge-confirmed, .badge-sent {{ background: #E8F5E9; color: #2E7D32; }}
    .badge-pending, .badge-skipped {{ background: #FFF3E0; color: #E65100; }}
    .badge-cancelled, .badge-failed {{ background: #FFEBEE; color: #C62828; }}
    .badge-primary {{ background: #E3F2FD; color: #1565C0; }}
    .muted {{ color: var(--muted); }}
    .text-center {{ text-align: center; }}
    code {{ background: #ECEFF1; padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
    @media print {{
        body {{ background: #fff; padding: 0; }}
        .card {{ break-inside: avoid; box-shadow: none; }}
    }}
</style>
</head>
<body>

<div class="header">
    <div>
        <h1>🏥 Kenyatta University Teaching, Referral & Research Hospital (KUTRRH)</h1>
        <p>AI Appointment & Patient Support System — Management & Analytics Report</p>
    </div>
    <div style="text-align: right;">
        <p><b>Generated:</b> {escape(str(report.get('generated_at', datetime.now().isoformat())))}</p>
        <p><small class="muted">Status: {escape(str(system_status.get('api_status', 'Operational')).upper())}</small></p>
    </div>
</div>

{mask_notice}

<!-- EXECUTIVE KPI SUMMARY -->
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="val">{total_chats}</div>
        <div class="lbl">Total Chat Sessions</div>
    </div>
    <div class="kpi-card kpi-success">
        <div class="val">{successful_chats}</div>
        <div class="lbl">Successful Chats</div>
    </div>
    <div class="kpi-card kpi-danger">
        <div class="val">{error_fallbacks} <small style="font-size:16px;">({error_fallback_pct}%)</small></div>
        <div class="lbl">Error Fallback Chats</div>
    </div>
    <div class="kpi-card kpi-warning">
        <div class="val">{slow_chats} <small style="font-size:16px;">({slow_chats_pct}%)</small></div>
        <div class="lbl">Slow Responses (>8s)</div>
    </div>
    <div class="kpi-card">
        <div class="val">{avg_latency:.0f} ms</div>
        <div class="lbl">Avg Response Time</div>
    </div>
    <div class="kpi-card">
        <div class="val">{len(all_appointments)}</div>
        <div class="lbl">Total Appointments</div>
    </div>
    <div class="kpi-card kpi-success">
        <div class="val">{apt_status_counts['Confirmed Bookings']}</div>
        <div class="lbl">Confirmed Bookings</div>
    </div>
    <div class="kpi-card kpi-danger">
        <div class="val">{apt_status_counts['Cancelled Bookings']}</div>
        <div class="lbl">Cancelled Bookings</div>
    </div>
    <div class="kpi-card">
        <div class="val">{len(visitor_ips)}</div>
        <div class="lbl">Unique Visitor IPs</div>
    </div>
    <div class="kpi-card">
        <div class="val">{len(feedback_records)}</div>
        <div class="lbl">Feedback Submissions</div>
    </div>
</div>

<!-- SECTION 1: CHAT QUALITY & RESOLUTION VISUALIZATIONS -->
<div class="grid-2">
    {outcome_pie_chart}
    {_build_html_bar_chart('Response Latency Distribution', quality.get('latency_distribution', {}), ['#2E7D32', '#1976D2', '#F57C00', '#D32F2F'])}
</div>

<!-- SECTION 2: APPOINTMENTS & SERVICES VISUALIZATIONS -->
<div class="grid-2">
    {_build_html_bar_chart('Appointments by Service Specialty', normalized_by_type, PALETTES['vibrant'])}
    {_build_html_bar_chart('Appointment Status Distribution', apt_status_counts, ['#2E7D32', '#F57C00', '#D32F2F'])}
</div>

<!-- SECTION 3: LANGUAGE USAGE & EMAIL NOTIFICATIONS -->
<div class="grid-2">
    {_build_html_bar_chart('Language Distribution', language_counts, ['#1976D2', '#7B1FA2'])}
    {_build_html_bar_chart('Email Confirmation Delivery Status', email_counts, ['#2E7D32', '#D32F2F', '#757575'])}
</div>

<!-- SECTION 4: LANGUAGE ANALYTICS -->
{language_summary}

<!-- SECTION 5: SYSTEM PERFORMANCE ANALYTICS -->
{performance_analytics}

<!-- SECTION 6: FEEDBACK STATISTICS & VISUAL ANALYSIS -->
{feedback_analytics}

<!-- SECTION 7: COMPLETE APPOINTMENTS TABLE (ALL BOOKED, PENDING, CANCELLED) -->
<div class="card">
    <h2>📅 Complete Appointments Record (Booked, Pending & Cancelled)</h2>
    <p class="muted">All appointment bookings stored in the hospital scheduling database with current status and patient references.</p>
    <div style="overflow-x: auto;">
        <table>
            <thead>
                <tr>
                    <th>Booking ID</th>
                    <th>Patient</th>
                    <th>Specialty</th>
                    <th>Date & Time</th>
                    <th>Status</th>
                    <th>Contact Info</th>
                    <th>Est. Wait</th>
                    <th>Notes / Reason</th>
                </tr>
            </thead>
            <tbody>
                {apt_rows}
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 8: VISITOR IP AUDIT LOG -->
<div class="card">
    <h2>🌐 Unique Visitor IP Audit Trail</h2>
    <p class="muted">Audited client IP addresses tracking platform interaction frequency and engagement timestamps.</p>
    <div style="overflow-x: auto;">
        <table>
            <thead>
                <tr>
                    <th>Client IP Address</th>
                    <th>First Seen</th>
                    <th>Last Seen</th>
                    <th>Hit Count</th>
                </tr>
            </thead>
            <tbody>
                {visitor_rows}
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 9: USER FEEDBACK & EVALUATION RECORDS -->
<div class="card">
    <h2>📝 User Evaluation & Feedback Records</h2>
    <p class="muted">Structured patient feedback responses evaluating usability, accuracy, queue utility, and satisfaction.</p>
    <div style="overflow-x: auto;">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Submitted By</th>
                    <th>Rating</th>
                    <th>Booking Success</th>
                    <th>Info Accurate</th>
                    <th>Effort (1-5)</th>
                    <th>User Comment / Feedback</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
                {feedback_rows}
            </tbody>
        </table>
    </div>
</div>

<!-- SECTION 10: EMAIL NOTIFICATION AUDIT -->
<div class="card">
    <h2>📧 Patient Email Confirmation Delivery Logs</h2>
    <div style="overflow-x: auto;">
        <table>
            <thead>
                <tr>
                    <th>Log ID</th>
                    <th>Appointment ID</th>
                    <th>Recipient Email</th>
                    <th>Subject</th>
                    <th>Delivery Status</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {email_rows}
            </tbody>
        </table>
    </div>
</div>

<div style="text-align: center; margin-top: 40px; color: var(--muted); font-size: 12px; border-top: 1px solid var(--border); padding-top: 20px;">
    KUTRRH AI Assistant Management System &bull; Confidential Administrative & Research Artifact &bull; Generated on {escape(str(report.get('generated_at', '')))}
</div>

</body>
</html>"""


def build_system_report_pdf(report: dict, mask_pii: bool = True) -> bytes:
    """Convert the complete HTML report to a downloadable PDF."""
    try:
        from xhtml2pdf import pisa
    except ImportError as exc:
        raise RuntimeError(
            "PDF export is unavailable because xhtml2pdf is not installed. "
            "Install the dependencies from requirements.txt."
        ) from exc

    from io import BytesIO
    output = BytesIO()
    result = pisa.CreatePDF(
        src=build_system_report_html(report, mask_pii=mask_pii),
        dest=output,
        encoding="utf-8",
    )
    pdf_bytes = output.getvalue()
    if result.err and not pdf_bytes.startswith(b"%PDF-"):
        raise RuntimeError(f"PDF export failed with {result.err} conversion error(s).")
    if result.err:
        logger.warning("PDF export completed with %s non-fatal layout warning(s)", result.err)
    return pdf_bytes


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
            <h2 style="color: #1976D2; margin-bottom: 4px;">KUTRRH Admin Dashboard</h2>
            <p style="color: #607289; font-size: 14px;">Secure Administrative & Analytics Portal</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("🔐 Sign In")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your administrator username")
            password = st.text_input("Password", placeholder="Enter your password", type="password")
            
            submitted = st.form_submit_button("🔓 Sign In to Dashboard", use_container_width=True, type="primary")
            
            if submitted:
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                elif login_admin(username, password):
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please verify username and password.")
        
        st.markdown("---")
        st.info("ℹ️ Authorized hospital management and systems audit use only.")


# ============================================================================
# Main Admin Dashboard View
# ============================================================================

def show_admin_dashboard():
    """Display full admin dashboard with enhanced visualizations, quality stats, and privacy controls."""
    
    # ------------------------------------------------------------------------
    # Sidebar Controls & Privacy Masking Toggle
    # ------------------------------------------------------------------------
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.admin_username}")
        st.caption("🛡️ Authenticated Management Session")
        st.divider()
        
        st.markdown("### 🔒 Privacy & Compliance")
        mask_pii = st.toggle(
            "Mask / Anonymize Personal Data (PII)",
            value=True,
            help="Mask patient names, phone numbers, email addresses, and IP addresses across all dashboard views, charts, and downloadable reports for HIPAA/DPA compliance."
        )
        if mask_pii:
            st.success("🛡️ **PII Masking Active**\nPersonal details (names, phones, emails, IPs) are protected.")
        else:
            st.warning("⚠️ **PII Masking Inactive**\nFull unmasked personal information is visible.")
            
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout_admin()
            st.rerun()
    
    # ------------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------------
    header_col1, header_col2, header_col3 = st.columns([1, 3, 1])
    with header_col2:
        if os.path.exists(LOGO_PATH):
            logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
            with logo_col2:
                st.image(LOGO_PATH, width=220)
        st.markdown("""
        <div style="text-align: center;">
            <h2 style="color: #1976D2; margin-bottom: 2px;">KUTRRH AI Assistant Management Dashboard</h2>
            <p style="color: #607289; margin-top: 0;">Prescriptive Scheduling, Multi-Modal Quality & System Governance</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ------------------------------------------------------------------------
    # Dashboard Tabs
    # ------------------------------------------------------------------------
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
    # Tab 1: 📊 Dashboard Overview
    # ====================================================================
    with tab1:
        st.subheader("📊 Executive System Overview")
        
        status_data = call_backend_auth("/admin/system-status", token=st.session_state.admin_token)
        apt_data = call_backend_auth("/admin/appointments", token=st.session_state.admin_token) or {}
        quality_data = call_backend_auth("/admin/chat-quality", token=st.session_state.admin_token) or {}
        feedback_data = call_backend_auth("/admin/feedback", token=st.session_state.admin_token) or []
        chat_data = call_backend_auth("/admin/chat-logs", token=st.session_state.admin_token) or []
        
        raw_by_type = apt_data.get('by_type', {})
        by_type = {}
        for k, v in raw_by_type.items():
            canon = normalize_appointment_type(k) or "General Check-up"
            by_type[canon] = by_type.get(canon, 0) + v

        # Top KPI Metrics Cards
        kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
        with kpi_col1:
            st.metric("Total Appointments", apt_data.get('total_appointments', 0))
        with kpi_col2:
            st.metric("Confirmed Bookings", apt_data.get('confirmed', 0), delta="🟢 Active")
        with kpi_col3:
            st.metric("Pending Bookings", apt_data.get('pending', 0), delta="🟡 Unconfirmed")
        with kpi_col4:
            st.metric("Cancelled Bookings", apt_data.get('cancelled', 0), delta="🔴 Cancelled")
        with kpi_col5:
            st.metric("Clinical Specialties", len(by_type))

        st.divider()
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Total Chat Sessions", quality_data.get("total_chats", len(chat_data)))
        with m_col2:
            err_cnt = quality_data.get("error_fallback_count", 0)
            err_pct = quality_data.get("error_fallback_rate_pct", 0.0)
            st.metric("Error / Fallback Chats", err_cnt, delta=f"{err_pct}% error rate", delta_color="inverse")
        with m_col3:
            st.metric("Patient Feedback Submissions", len(feedback_data))
        with m_col4:
            unique_ips = len({row.get('ip_address') for row in chat_data if row.get('ip_address')})
            st.metric("Unique Visitor IPs", unique_ips)

        st.divider()

        # Multi-colored Visualizations
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("#### 🏥 Appointments by Service Specialty")
            by_type = apt_data.get('by_type', {})
            if by_type:
                df_type = pd.DataFrame([{"Specialty": k, "Appointments": v} for k, v in by_type.items()])
                render_colored_bar_chart(
                    df_type,
                    category_col="Specialty",
                    value_col="Appointments",
                    title="Distribution of Appointments by Medical Department",
                    x_label="Department / Specialty",
                    y_label="Total Appointments",
                    legend_title="Specialty",
                    color_scheme="tableau10",
                    height=320,
                    horizontal=True
                )
            else:
                st.info("No appointments recorded yet.")

        with chart_col2:
            st.markdown("#### 🔄 Appointment Booking Status Distribution")
            df_status = pd.DataFrame([
                {"Status": "Confirmed", "Count": apt_data.get("confirmed", 0)},
                {"Status": "Pending", "Count": apt_data.get("pending", 0)},
                {"Status": "Cancelled", "Count": apt_data.get("cancelled", 0)},
            ])
            status_scale = alt.Scale(
                domain=["Confirmed", "Pending", "Cancelled"],
                range=["#2E7D32", "#F57C00", "#D32F2F"]
            )
            render_donut_chart(
                df_status,
                category_col="Status",
                value_col="Count",
                title="Confirmed vs Pending vs Cancelled Appointments",
                legend_title="Status",
                color_scale=status_scale,
                height=320
            )

    # ====================================================================
    # Tab 2: 📅 Appointments Management
    # ====================================================================
    with tab2:
        st.subheader("📅 Appointments Management & Records")
        apt_data = call_backend_auth("/admin/appointments", token=st.session_state.admin_token)
        
        if apt_data:
            appointments = apt_data.get('appointments', [])
            
            # Filter bar
            filter_col1, filter_col2 = st.columns([1, 2])
            with filter_col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Confirmed", "Pending", "Cancelled"])
            with filter_col2:
                search_query = st.text_input("Search by Specialty or Booking ID", placeholder="e.g. Optical, Nephrology, APT_0001")
            
            filtered = appointments
            if status_filter != "All":
                filtered = [a for a in filtered if a.get('status', '').lower() == status_filter.lower()]
            if search_query.strip():
                q = search_query.strip().lower()
                filtered = [
                    a for a in filtered
                    if q in str(a.get('id', '')).lower() or q in str(a.get('type', '')).lower() or q in str(a.get('name', '')).lower()
                ]

            st.caption(f"Showing **{len(filtered)}** appointment records (PII Masking: {'Active 🛡️' if mask_pii else 'Off ⚠️'})")

            # Table view
            if filtered:
                display_rows = []
                for apt in filtered:
                    display_rows.append({
                        "Booking ID": apt.get("id", "N/A"),
                        "Status": apt.get("status", "N/A").upper(),
                        "Specialty": apt.get("type", "N/A"),
                        "Date & Time": apt.get("datetime", "N/A"),
                        "Patient Name": mask_name(apt.get("name"), mask_pii),
                        "Patient ID": mask_patient_id(apt.get("patient_id"), mask_pii),
                        "Phone": mask_phone(apt.get("phone"), mask_pii),
                        "Email": mask_email(apt.get("email"), mask_pii),
                        "Est. Wait": f"{apt.get('predicted_wait_minutes', 0):.0f} min",
                        "Created At": str(apt.get("created_at", ""))[:19]
                    })
                st.dataframe(pd.DataFrame(display_rows), use_container_width=True, hide_index=True)
            else:
                st.info("No matching appointments found.")
        else:
            st.info("No appointments found.")

    # ====================================================================
    # Tab 3: ⚙️ System Management
    # ====================================================================
    with tab3:
        st.subheader("⚙️ System Health & Knowledge Base")
        status_data = call_backend_auth("/admin/system-status", token=st.session_state.admin_token)
        
        if status_data:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### System Components")
                st.json(status_data)
            with col2:
                st.markdown("#### Knowledge Base Status")
                kb_init = status_data.get('knowledge_base', {}).get('initialized')
                if kb_init:
                    st.success("✅ Knowledge Base: Initialized & Vector Store Ready")
                else:
                    st.error("❌ Knowledge Base: Not Initialized")
                st.info(f"Vector Store Directory: `{status_data.get('knowledge_base', {}).get('path', 'hospital_vector_store')}`")
        
        st.divider()
        st.subheader("🔄 Rebuild Hospital Knowledge Base")
        st.warning("⚠️ This will re-index all source hospital documents, service charters, and FAQs into FAISS vector embeddings.")
        
        if st.button("🔨 Rebuild Knowledge Base Index", use_container_width=True, type="primary"):
            with st.spinner("Re-indexing hospital knowledge documents..."):
                result = call_backend_auth("/admin/rebuild-kb", method="POST", token=st.session_state.admin_token)
                if result and result.get('success'):
                    st.success("✅ Knowledge base rebuilt successfully!")
                    st.json(result)
                elif result:
                    st.warning(f"⚠️ {result.get('message', 'Rebuild completed with warnings')}")
                    st.json(result)
                else:
                    st.error("❌ Rebuild failed. Please verify backend logs.")

    # ====================================================================
    # Tab 4: 👥 User Access Management
    # ====================================================================
    with tab4:
        st.subheader("👥 System User Access & Roles")
        
        with st.form("create_admin_form"):
            st.markdown("#### Add New Management User")
            new_username = st.text_input("Username", placeholder="e.g. jdoe_admin")
            new_password = st.text_input("Password", placeholder="Minimum 6 characters", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            new_role = st.selectbox(
                "Access Role",
                ["viewer", "support", "scheduler", "analyst", "systems_manager", "admin"],
                format_func=lambda r: r.replace("_", " ").title()
            )
            submitted = st.form_submit_button("➕ Create User Account", use_container_width=True)
            if submitted:
                if not new_username or not new_password:
                    st.error("❌ Username and password are required")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    res = call_backend_auth(
                        f"/admin/create-user?username={quote(new_username)}&password={quote(new_password)}&role={quote(new_role)}",
                        method="POST",
                        token=st.session_state.admin_token
                    )
                    if res and res.get('success'):
                        st.success(f"✅ {res.get('message', 'User created')}")
                    else:
                        st.error("❌ Failed to create user")

        st.divider()
        st.markdown("#### Existing System Users")
        users = call_backend_auth("/admin/users", token=st.session_state.admin_token)
        if users:
            st.dataframe(pd.DataFrame(users), use_container_width=True, hide_index=True)

    # ====================================================================
    # Tab 5: 📝 Feedback & Evaluation
    # ====================================================================
    with tab5:
        st.subheader("📝 Patient Usability & System Evaluation Feedback")
        stats = call_backend_auth("/admin/feedback-stats", token=st.session_state.admin_token)
        raw_feedback = call_backend_auth("/admin/feedback", token=st.session_state.admin_token) or []

        if stats and stats.get("total_feedback"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Submissions", stats.get("total_feedback", 0))
            with col2:
                avg_effort = stats.get("avg_natural_effort")
                st.metric("Avg Effort Rating (1-5)", f"{avg_effort:.2f} / 5" if avg_effort is not None else "N/A")
            with col3:
                st.metric("Unique Responding IPs", len({f.get('ip_address') for f in raw_feedback if f.get('ip_address')}))

            st.divider()
            st.markdown("### 📊 Question-by-Question Evaluation Breakdown")

            for question in stats.get("questions", []):
                counts = question.get("counts") or {}
                if not counts:
                    continue
                q_df = pd.DataFrame([{"Option": k, "Responses": v} for k, v in counts.items()])
                render_colored_bar_chart(
                    q_df,
                    category_col="Option",
                    value_col="Responses",
                    title=f"Question: {question['label']}",
                    x_label="Number of Responses",
                    y_label="Answer Option",
                    legend_title="Answer",
                    color_scheme="set2",
                    height=200,
                    horizontal=True
                )

            effort_dist = stats.get("natural_effort_distribution") or {}
            if effort_dist:
                st.markdown("### 🌟 Natural / Low-Effort Rating Distribution (1 = Difficult, 5 = Effortless)")
                effort_df = pd.DataFrame([{"Rating": f"Score {k}", "Count": v} for k, v in effort_dist.items()])
                render_colored_bar_chart(
                    effort_df,
                    category_col="Rating",
                    value_col="Count",
                    title="User-Reported Effort Level",
                    x_label="Score Level",
                    y_label="Respondent Count",
                    legend_title="Score",
                    color_scheme="tableau10",
                    height=260
                )
        else:
            st.info("No feedback submissions recorded yet.")

        st.divider()
        st.markdown("### 📋 Anonymized Feedback Submissions")
        if raw_feedback:
            clean_fb = []
            for fb in raw_feedback:
                clean_fb.append({
                    "ID": fb.get("id"),
                    "Email": mask_email(fb.get("email"), mask_pii),
                    "Rating": f"{fb.get('rating', 'N/A')}/5",
                    "Booking Completed": fb.get("booking_success", "-"),
                    "Info Accurate": fb.get("information_accuracy", "-"),
                    "KB Honesty": fb.get("knowledge_base_honesty", "-"),
                    "Queue Utility": fb.get("queue_recommendations", "-"),
                    "Language Consistency": fb.get("language_consistency", "-"),
                    "Natural Effort": fb.get("natural_effort", "-"),
                    "Message / Comments": anonymize_text(fb.get("message") or fb.get("additional_feedback") or "", mask_pii),
                    "IP Address": mask_ip(fb.get("ip_address"), mask_pii),
                    "Timestamp": str(fb.get("created_at", ""))[:19]
                })
            st.dataframe(pd.DataFrame(clean_fb), use_container_width=True, hide_index=True)

    # ====================================================================
    # Tab 6: 💬 Chat Audit Log
    # ====================================================================
    with tab6:
        st.subheader("💬 Chat Interaction Audit Logs")
        st.caption("Detailed record of user queries and assistant responses with originating client IP tracking.")
        
        ip_filter = st.text_input("Filter by Client IP Address", key="chat_log_ip_input")
        endpoint = "/admin/chat-logs"
        if ip_filter.strip():
            endpoint += f"?ip_address={quote(ip_filter.strip())}"
        logs = call_backend_auth(endpoint, token=st.session_state.admin_token) or []

        if logs:
            st.caption(f"Showing **{len(logs)}** log entries (PII Masking: {'Active 🛡️' if mask_pii else 'Off ⚠️'})")
            clean_logs = []
            for item in logs:
                clean_logs.append({
                    "Log ID": item.get("id"),
                    "Client IP": mask_ip(item.get("ip_address"), mask_pii),
                    "User Message": anonymize_text(item.get("user_message"), mask_pii),
                    "Assistant Response": anonymize_text(item.get("assistant_response"), mask_pii),
                    "Latency (ms)": f"{item.get('response_time_ms', 0):.0f}" if item.get('response_time_ms') is not None else "N/A",
                    "Flagged": "🚩 Yes" if item.get("flagged") else "✅ Normal",
                    "Flag Reason": item.get("flag_reason") or "-",
                    "Language": (item.get("language") or "English").title(),
                    "Timestamp": str(item.get("created_at", ""))[:19]
                })
            st.dataframe(pd.DataFrame(clean_logs), use_container_width=True, hide_index=True)
        else:
            st.info("No chat logs found.")

    # ====================================================================
    # Tab 7: 🩺 Chat Quality & Error Fallback Analytics (ENHANCED)
    # ====================================================================
    with tab7:
        st.subheader("🩺 Chat Quality, Responsiveness & Error Fallback Monitoring")
        st.caption("Tracks fallback error triggers, slow responses (>8s), empty outputs, and conversational quality metrics.")
        
        quality = call_backend_auth("/admin/chat-quality", token=st.session_state.admin_token)
        
        if quality:
            total_chats = quality.get("total_chats", 0)
            successful_chats = quality.get("successful_count", max(0, total_chats - quality.get("flagged_count", 0)))
            successful_pct = quality.get("successful_rate_pct", round((successful_chats / total_chats * 100), 1) if total_chats else 0.0)
            
            error_fallbacks = quality.get("error_fallback_count", 0)
            error_fallback_pct = quality.get("error_fallback_rate_pct", 0.0)
            
            slow_count = quality.get("slow_response_count", 0)
            slow_pct = quality.get("slow_response_rate_pct", 0.0)
            
            empty_count = quality.get("empty_response_count", 0)
            empty_pct = quality.get("empty_response_rate_pct", 0.0)
            
            avg_ms = quality.get("avg_response_time_ms")

            # KPI Summary Cards (Prominently displaying Error Fallbacks!)
            q_col1, q_col2, q_col3, q_col4, q_col5, q_col6 = st.columns(6)
            with q_col1:
                st.metric("Total Chats", total_chats)
            with q_col2:
                st.metric("Successful Chats", successful_chats, delta=f"{successful_pct}% success")
            with q_col3:
                st.metric("Error Fallbacks", error_fallbacks, delta=f"{error_fallback_pct}% error rate", delta_color="inverse")
            with q_col4:
                st.metric("Slow (>8s)", slow_count, delta=f"{slow_pct}% slow rate", delta_color="inverse")
            with q_col5:
                st.metric("Empty Responses", empty_count, delta=f"{empty_pct}% empty rate", delta_color="inverse")
            with q_col6:
                st.metric("Avg Latency", f"{avg_ms:.0f} ms" if avg_ms is not None else "N/A")

            st.divider()

            # Multi-colored Visualizations on Chat Quality
            qc_col1, qc_col2 = st.columns(2)
            with qc_col1:
                st.markdown("#### 🎯 Chat Response Outcome & Fallback Breakdown")
                df_quality = pd.DataFrame([
                    {"Outcome": "Successful Responses", "Count": successful_chats},
                    {"Outcome": "Error / Fallback Responses", "Count": error_fallbacks},
                    {"Outcome": "Slow Responses (>8s)", "Count": slow_count},
                    {"Outcome": "Empty Responses", "Count": empty_count},
                ])
                outcome_scale = alt.Scale(
                    domain=["Successful Responses", "Error / Fallback Responses", "Slow Responses (>8s)", "Empty Responses"],
                    range=["#2E7D32", "#D32F2F", "#F57C00", "#757575"]
                )
                render_donut_chart(
                    df_quality,
                    category_col="Outcome",
                    value_col="Count",
                    title="Resolution & Error Fallback Distribution",
                    legend_title="Outcome Type",
                    color_scale=outcome_scale,
                    height=320
                )

            with qc_col2:
                st.markdown("#### ⏱️ Response Latency Distribution")
                latency_dist = quality.get("latency_distribution", {})
                if latency_dist:
                    df_lat = pd.DataFrame([{"Speed Bucket": k, "Chat Count": v} for k, v in latency_dist.items()])
                    render_colored_bar_chart(
                        df_lat,
                        category_col="Speed Bucket",
                        value_col="Chat Count",
                        title="Chat Response Time Distribution",
                        x_label="Response Time Bucket",
                        y_label="Number of Chats",
                        legend_title="Latency Range",
                        color_scheme="tableau10",
                        height=320
                    )
                else:
                    st.info("No latency bucket data recorded.")

            st.divider()

            # Performance Trend Chart
            trend = quality.get("performance_trend", [])
            if trend:
                st.markdown("#### 📈 Response Time Trend by Date (ms)")
                df_trend = pd.DataFrame(trend)
                if "avg_response_time_ms" in df_trend.columns and "date" in df_trend.columns:
                    render_line_trend_chart(
                        df_trend,
                        x_col="date",
                        y_col="avg_response_time_ms",
                        title="Average Chat Latency Over Time (ms)",
                        x_title="Date (YYYY-MM-DD)",
                        y_title="Average Response Time (ms)",
                        line_color="#1976D2",
                        height=300
                    )

            st.divider()
            st.markdown("#### 🚩 Flagged & Fallback Chat Audit Records")
            recent = quality.get("recent_flagged") or []
            if recent:
                clean_recent = []
                for r in recent:
                    clean_recent.append({
                        "ID": r.get("id"),
                        "Client IP": mask_ip(r.get("ip_address"), mask_pii),
                        "User Query": anonymize_text(r.get("user_message"), mask_pii),
                        "Assistant Output": anonymize_text(r.get("assistant_response"), mask_pii),
                        "Flag Reason": r.get("flag_reason") or "Flagged",
                        "Latency (ms)": f"{r.get('response_time_ms', 0):.0f}" if r.get('response_time_ms') is not None else "N/A",
                        "Date": str(r.get("created_at", ""))[:19]
                    })
                st.dataframe(pd.DataFrame(clean_recent), use_container_width=True, hide_index=True)
            else:
                st.success("🎉 No flagged error or fallback interactions recorded.")
        else:
            st.info("No chat quality metrics available.")

    # ====================================================================
    # Tab 8: 📧 Email Notifications
    # ====================================================================
    with tab8:
        st.subheader("📧 Patient Appointment Confirmation Emails")
        notifications = call_backend_auth("/admin/email-notifications", token=st.session_state.admin_token) or []
        
        if notifications:
            sent = len([n for n in notifications if n.get("status") == "sent"])
            failed = len([n for n in notifications if n.get("status") == "failed"])
            skipped = len([n for n in notifications if n.get("status") == "skipped"])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Delivered Emails", sent, delta="🟢 Sent")
            with col2:
                st.metric("Failed Deliveries", failed, delta="🔴 Failed", delta_color="inverse")
            with col3:
                st.metric("Skipped (No SMTP)", skipped, delta="🟡 Skipped")

            st.divider()
            df_email = pd.DataFrame([
                {"Delivery Status": "Delivered", "Count": sent},
                {"Delivery Status": "Failed", "Count": failed},
                {"Delivery Status": "Skipped", "Count": skipped},
            ])
            render_donut_chart(
                df_email,
                category_col="Delivery Status",
                value_col="Count",
                title="Email Delivery Outcomes",
                legend_title="Status",
                color_scale=alt.Scale(domain=["Delivered", "Failed", "Skipped"], range=["#2E7D32", "#D32F2F", "#757575"]),
                height=280
            )

            st.divider()
            st.markdown("#### Email Audit Logs")
            clean_emails = []
            for item in notifications:
                clean_emails.append({
                    "Log ID": item.get("id"),
                    "Appointment ID": item.get("appointment_id", "N/A"),
                    "Recipient Email": mask_email(item.get("recipient_email"), mask_pii),
                    "Subject": item.get("subject", "N/A"),
                    "Status": item.get("status", "N/A").upper(),
                    "Error Details": item.get("error_message") or "-",
                    "Timestamp": str(item.get("created_at", ""))[:19]
                })
            st.dataframe(pd.DataFrame(clean_emails), use_container_width=True, hide_index=True)
        else:
            st.info("No email notifications logged yet.")

    # ====================================================================
    # Tab 9: 🌐 Visitor IPs
    # ====================================================================
    with tab9:
        st.subheader("🌐 Unique Visitor IP Address Audit")
        visitor_ips = call_backend_auth("/admin/visitor-ips", token=st.session_state.admin_token) or []
        
        if visitor_ips:
            st.metric("Total Unique IP Addresses", len(visitor_ips))
            st.divider()

            # Top IPs chart
            df_ips = pd.DataFrame(visitor_ips[:10])
            if not df_ips.empty and "hit_count" in df_ips.columns:
                df_ips["Masked_IP"] = df_ips["ip_address"].apply(lambda x: mask_ip(x, mask_pii))
                render_colored_bar_chart(
                    df_ips,
                    category_col="Masked_IP",
                    value_col="hit_count",
                    title="Top 10 Most Active Client IP Addresses",
                    x_label="Client IP Address",
                    y_label="Visit / Interaction Count",
                    legend_title="Client IP",
                    color_scheme="category20",
                    height=300
                )

            st.divider()
            st.markdown("#### Full IP Audit Register")
            clean_ips = []
            for item in visitor_ips:
                clean_ips.append({
                    "IP Address": mask_ip(item.get("ip_address"), mask_pii),
                    "First Seen": str(item.get("first_seen", ""))[:19],
                    "Last Seen": str(item.get("last_seen", ""))[:19],
                    "Hit Count": item.get("hit_count", 1)
                })
            st.dataframe(pd.DataFrame(clean_ips), use_container_width=True, hide_index=True)
        else:
            st.info("No visitor IP addresses recorded yet.")

    # ====================================================================
    # Tab 10: 🗣️ Language Analytics
    # ====================================================================
    with tab10:
        st.subheader("🗣️ Multi-Lingual Analytics (English vs Swahili)")
        lang_stats = call_backend_auth("/admin/language-stats", token=st.session_state.admin_token)
        
        if lang_stats:
            counts = lang_stats.get("language_counts", {})
            successful = lang_stats.get("successful_responses", {})
            rates = lang_stats.get("success_rate_pct", {})
            switches = lang_stats.get("switches", {})
            switch_rates = lang_stats.get("switch_rate_pct", {})

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("English Chats", counts.get("english", 0))
            with col2:
                st.metric("Swahili Chats", counts.get("swahili", 0))
            with col3:
                st.metric("English Success", f"{rates.get('english', 0)}%", delta=f"{successful.get('english', 0)} chats")
            with col4:
                st.metric("Swahili Success", f"{rates.get('swahili', 0)}%", delta=f"{successful.get('swahili', 0)} chats")

            st.divider()
            l_col1, l_col2 = st.columns(2)
            with l_col1:
                df_lang = pd.DataFrame([
                    {"Language": "English", "Chats": counts.get("english", 0)},
                    {"Language": "Swahili", "Chats": counts.get("swahili", 0)},
                ])
                render_colored_bar_chart(
                    df_lang,
                    category_col="Language",
                    value_col="Chats",
                    title="Chat Sessions by User Language",
                    x_label="Language",
                    y_label="Total Chat Count",
                    legend_title="Language",
                    color_scheme="tableau10",
                    height=300
                )

            with l_col2:
                df_succ = pd.DataFrame([
                    {"Language": "English", "Successful Chats": successful.get("english", 0)},
                    {"Language": "Swahili", "Successful Chats": successful.get("swahili", 0)},
                ])
                render_colored_bar_chart(
                    df_succ,
                    category_col="Language",
                    value_col="Successful Chats",
                    title="Successful Responses by Language",
                    x_label="Language",
                    y_label="Successful Responses",
                    legend_title="Language",
                    color_scheme="set2",
                    height=300
                )

            st.divider()
            st.markdown("#### 🔄 Cross-Language Switching Rates")
            sw_col1, sw_col2 = st.columns(2)
            with sw_col1:
                st.metric("English ➔ Swahili Switches", switches.get("english_to_swahili", 0), delta=f"{switch_rates.get('english_to_swahili', 0)}% rate")
            with sw_col2:
                st.metric("Swahili ➔ English Switches", switches.get("swahili_to_english", 0), delta=f"{switch_rates.get('swahili_to_english', 0)}% rate")
        else:
            st.info("No language analytics data available yet.")

    # ====================================================================
    # Tab 11: 📄 Full Management Report
    # ====================================================================
    with tab11:
        st.subheader("📄 Full Comprehensive Management & Research Report")
        st.caption("Includes all booked & cancelled appointments, masked visitor IPs, evaluation feedback, email notifications, and quality metrics.")

        report = call_backend_auth("/admin/system-report", token=st.session_state.admin_token)
        
        if report:
            html_content = build_system_report_html(report, mask_pii=mask_pii)
            report_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            download_col1, download_col2 = st.columns(2)
            with download_col1:
                st.download_button(
                    label="📥 Download Full Report (HTML)",
                    data=html_content,
                    file_name=f"KUTRRH_System_Management_Report_{report_timestamp}.html",
                    mime="text/html",
                    use_container_width=True,
                    type="primary"
                )
            with download_col2:
                try:
                    pdf_content = build_system_report_pdf(report, mask_pii=mask_pii)
                    st.download_button(
                        label="📄 Download Full Report (PDF)",
                        data=pdf_content,
                        file_name=f"KUTRRH_System_Management_Report_{report_timestamp}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as pdf_error:
                    logger.exception("PDF report generation failed")
                    st.error(str(pdf_error))
            
            st.divider()
            st.markdown("### 📋 Executive Summary Preview")
            
            quality = report.get("chat_quality", {})
            appointments_meta = report.get("appointments", {})
            all_appointments = appointments_meta.get("all_appointments", [])
            visitor_ips = report.get("visitor_ips", [])
            feedback_records = report.get("feedback_records", [])

            s_col1, s_col2, s_col3, s_col4 = st.columns(4)
            with s_col1:
                st.metric("Total Chats", quality.get("total_chats", 0))
            with s_col2:
                err_cnt = quality.get("error_fallback_count", 0)
                err_pct = quality.get("error_fallback_rate_pct", 0.0)
                st.metric("Error Fallbacks", f"{err_cnt} ({err_pct}%)")
            with s_col3:
                st.metric("All Appointments", len(all_appointments))
            with s_col4:
                st.metric("Visitor IPs", len(visitor_ips))

            st.divider()
            st.markdown("#### 📅 All Appointments Included in Report (Booked, Pending, Cancelled)")
            if all_appointments:
                rep_apt_df = pd.DataFrame([
                    {
                        "Booking ID": a.get("id"),
                        "Status": a.get("status", "N/A").upper(),
                        "Specialty": a.get("type"),
                        "Date & Time": a.get("datetime"),
                        "Patient Name": mask_name(a.get("name"), mask_pii),
                        "Patient ID": mask_patient_id(a.get("patient_id"), mask_pii),
                        "Phone": mask_phone(a.get("phone"), mask_pii),
                        "Email": mask_email(a.get("email"), mask_pii),
                        "Est. Wait (min)": a.get("predicted_wait_minutes"),
                        "Cancellation Reason": a.get("cancellation_reason") or "-"
                    }
                    for a in all_appointments
                ])
                st.dataframe(rep_apt_df, use_container_width=True, hide_index=True)

            st.divider()
            st.markdown("#### 🌐 Masked Visitor IPs Included in Report")
            if visitor_ips:
                rep_ip_df = pd.DataFrame([
                    {
                        "Client IP": mask_ip(v.get("ip_address"), mask_pii),
                        "First Seen": str(v.get("first_seen", ""))[:19],
                        "Last Seen": str(v.get("last_seen", ""))[:19],
                        "Visit Count": v.get("hit_count", 1)
                    }
                    for v in visitor_ips
                ])
                st.dataframe(rep_ip_df, use_container_width=True, hide_index=True)

            st.divider()
            st.markdown("#### 📝 Masked Feedback Records Included in Report")
            if feedback_records:
                rep_fb_df = pd.DataFrame([
                    {
                        "ID": f.get("id"),
                        "Email": mask_email(f.get("email"), mask_pii),
                        "Rating": f.get("rating"),
                        "Booking Success": f.get("booking_success"),
                        "Accuracy": f.get("information_accuracy"),
                        "Effort Rating": f.get("natural_effort"),
                        "Comments": anonymize_text(f.get("message") or f.get("additional_feedback") or "", mask_pii),
                        "IP Address": mask_ip(f.get("ip_address"), mask_pii)
                    }
                    for f in feedback_records
                ])
                st.dataframe(rep_fb_df, use_container_width=True, hide_index=True)
        else:
            st.info("Unable to retrieve report data from backend API.")


# ============================================================================
# Main Application Entry Point
# ============================================================================

def main():
    initialize_session_state()
    
    # Check backend connectivity
    try:
        requests.get(f"{BACKEND_URL}/health", timeout=2).json()
    except Exception:
        st.error(f"❌ Cannot connect to backend API at `{BACKEND_URL}`. Ensure backend server is running on port 8000.")
        st.stop()
    
    # Display login or dashboard
    if not st.session_state.admin_token:
        show_login_page()
    else:
        show_admin_dashboard()


if __name__ == "__main__":
    main()
