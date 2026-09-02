"""
KUTRRH Hospital - Redesigned Public Frontend
Modern multi-page interface with separate chat and booking forms
KUTRRH branding and professional UI/UX design
"""

import streamlit as st
import requests
import datetime
import os
from typing import List, Dict
import logging

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

# KUTRRH Branding & Colors
KUTRRH_COLORS = {
    "primary": "#1f4788",      # Deep blue
    "secondary": "#2196F3",    # Light blue
    "accent": "#00897B",       # Teal
    "success": "#4CAF50",      # Green
    "warning": "#FF9800",      # Orange
    "danger": "#F44336",       # Red
    "light": "#ECEFF1",        # Light gray
    "dark": "#263238",         # Dark blue-gray
}

# Page configuration with custom theme
st.set_page_config(
    layout="wide",
    page_title="KUTRRH Hospital - Appointments",
    page_icon="🏥",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": "KUTRRH Hospital AI-Powered Appointment System v2.0"
    }
)

# ============================================================================
# CUSTOM CSS STYLING FOR KUTRRH BRANDING
# ============================================================================

st.markdown(f"""
<style>
    /* Root variables */
    :root {{
        --primary: {KUTRRH_COLORS['primary']};
        --secondary: {KUTRRH_COLORS['secondary']};
        --accent: {KUTRRH_COLORS['accent']};
        --success: {KUTRRH_COLORS['success']};
    }}
    
    /* Main container styling */
    .main {{
        padding-top: 1rem;
    }}
    
    /* Header styling */
    .header-container {{
        background: linear-gradient(135deg, {KUTRRH_COLORS['primary']} 0%, {KUTRRH_COLORS['secondary']} 100%);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(31, 71, 136, 0.2);
    }}
    
    .header-container h1 {{
        color: white;
        margin: 0 0 0.5rem 0;
        font-size: 2.8rem;
        font-weight: bold;
        letter-spacing: -0.5px;
    }}
    
    .header-container .subtitle {{
        color: rgba(255, 255, 255, 0.95);
        margin: 0.3rem 0;
        font-size: 1.05rem;
        font-weight: 500;
    }}
    
    .header-container .tagline {{
        color: rgba(255, 255, 255, 0.85);
        margin-top: 0.8rem;
        font-size: 0.95rem;
        font-style: italic;
    }}
    
    /* Navigation buttons */
    .nav-button {{
        transition: all 0.3s ease;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.05rem;
    }}
    
    /* Card styling */
    .info-card {{
        background: white;
        border-left: 5px solid {KUTRRH_COLORS['secondary']};
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }}
    
    .success-card {{
        background: rgba(76, 175, 80, 0.05);
        border-left: 5px solid {KUTRRH_COLORS['success']};
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, {KUTRRH_COLORS['secondary']} 0%, {KUTRRH_COLORS['accent']} 100%);
        color: white;
        border: none;
        font-weight: 600;
        padding: 0.7rem 2rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-size: 1rem;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(33, 150, 243, 0.4);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Primary button variant */
    [data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, {KUTRRH_COLORS['success']} 0%, {KUTRRH_COLORS['accent']} 100%) !important;
    }}
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {{
        border: 2px solid {KUTRRH_COLORS['light']} !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.8rem !important;
        font-size: 0.95rem;
        transition: border-color 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {{
        border: 2px solid {KUTRRH_COLORS['secondary']} !important;
        box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
    }}
    
    /* Chat container */
    .stContainer {{
        background: white;
        border-radius: 12px;
        border: 1px solid {KUTRRH_COLORS['light']};
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    
    /* Chat messages - Streamlit native components styling */
    [data-testid="stChatMessage"] {{
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }}
    
    /* Metric cards */
    .metric {{
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.05) 0%, rgba(0, 137, 123, 0.05) 100%);
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid {KUTRRH_COLORS['light']};
        margin: 0.8rem 0;
    }}
    
    /* Form sections */
    .form-section {{
        background: {KUTRRH_COLORS['light']};
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
    }}
    
    /* Divider */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, {KUTRRH_COLORS['secondary']}, transparent);
        margin: 2rem 0;
    }}
    
    /* Section headers */
    h2, h3 {{
        color: {KUTRRH_COLORS['primary']};
        margin-top: 1.5rem;
    }}
    
    /* Links */
    a {{
        color: {KUTRRH_COLORS['secondary']};
        text-decoration: none;
    }}
    
    a:hover {{
        text-decoration: underline;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        color: #999;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding: 1.5rem 0;
        border-top: 1px solid {KUTRRH_COLORS['light']};
    }}
    
    /* Slot buttons - Custom styling */
    .slot-button {{
        background: white;
        border: 2px solid {KUTRRH_COLORS['light']};
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .slot-button:hover {{
        border-color: {KUTRRH_COLORS['secondary']};
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.2);
    }}
    
    .slot-button-selected {{
        background: linear-gradient(135deg, {KUTRRH_COLORS['secondary']} 0%, {KUTRRH_COLORS['accent']} 100%);
        color: white;
        border-color: {KUTRRH_COLORS['accent']};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Helper Functions
# ============================================================================

def call_backend(endpoint: str, method: str = "GET", data: dict = None) -> dict:
    """Call backend API"""
    url = f"{BACKEND_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Backend API error: {str(e)}")
        st.error(f"⚠️ Service unavailable. Please try again later.")
        return None


def initialize_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "chat"
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'show_confirmation' not in st.session_state:
        st.session_state.show_confirmation = False
    if 'selected_slot' not in st.session_state:
        st.session_state.selected_slot = None


def kutrrh_header():
    """Display KUTRRH branded header with logo"""
    col1, col2, col3 = st.columns([1, 1.5, 1.5])
    
    with col1:
        try:
            logo_path = os.path.join(os.path.dirname(__file__), ".streamlit", "kutrrh_logo.png")
            st.image(
                logo_path,
                width=250
            )
        except Exception as e:
            logger.warning(f"Could not load logo: {str(e)}")
    
    with col2:
        st.markdown(f"""
        <div class="header-container" style="text-align: center;">
            <h1 style="margin: 0.5rem 0; font-size: 0.9rem;"><strong>Welcome to KUTRRH AI-Powered Appointment Manager</strong></h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.empty()


def show_page_navigation():
    """Show navigation between pages"""
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button(
            "💬 Chat Assistant",
            use_container_width=True,
            key="nav_chat",
            type="primary" if st.session_state.current_page == "chat" else "secondary"
        ):
            st.session_state.current_page = "chat"
            st.rerun()
    
    with col2:
        if st.button(
            "📅 Book Appointment",
            use_container_width=True,
            key="nav_book",
            type="primary" if st.session_state.current_page == "book" else "secondary"
        ):
            st.session_state.current_page = "book"
            st.rerun()
    
    with col3:
        if st.button(
            "📝 Feedback",
            use_container_width=True,
            key="nav_feedback",
            type="primary" if st.session_state.current_page == "feedback" else "secondary"
        ):
            st.session_state.current_page = "feedback"
            st.rerun()
    
    st.divider()


# ============================================================================
# PAGE 1: Chat with AI Assistant
# ============================================================================

def page_chat():
    """Chat interface page with proper message alignment"""
    st.subheader("💬 Chat with Our AI Assistant", divider="blue")
    
    st.markdown("💬 Get instant answers about hospital services, departments, and more!")
    
    # Create a container for the chat with custom styling
    st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            padding: 1rem;
        }
        
        .chat-message {
            display: flex;
            margin-bottom: 1rem;
            gap: 0.5rem;
        }
        
        .chat-message.user {
            justify-content: flex-start;
        }
        
        .chat-message.assistant {
            justify-content: flex-end;
        }
        
        .chat-bubble {
            max-width: 70%;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            word-wrap: break-word;
        }
        
        .chat-bubble.user {
            background: linear-gradient(135deg, #2196F3 0%, #00897B 100%);
            color: white;
            border-radius: 12px 2px 12px 12px;
        }
        
        .chat-bubble.assistant {
            background: white;
            color: #1f4788;
            border: 2px solid #ECEFF1;
            border-radius: 2px 12px 12px 12px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display chat container
    if st.session_state.conversation:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.conversation:
            role = message.get('role', 'assistant')
            content = message.get('content', '')
            
            if role == 'user':
                st.markdown(f"""
                <div class="chat-message user">
                    <div class="chat-bubble user">
                        <p style="margin: 0; line-height: 1.5;">{content}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant">
                    <div class="chat-bubble assistant">
                        <p style="margin: 0; line-height: 1.5;">{content}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Welcome message for first-time users
        st.info("""
        👋 **Welcome to KUTRRH AI Assistant!**
        
        You can ask me about:
        - 🏥 Hospital services and departments
        - 👨‍⚕️ Medical staff and specialists
        - 🕐 Visiting hours and contact information
        - 💳 Payment methods and insurance
        - 📍 Directions and facilities
        
        **For appointment booking**, use the "📅 Book Appointment" page.
        """)
    
    st.divider()
    
    # Chat input
    user_input = st.chat_input(
        placeholder="💬 Ask your question...",
        key="chat_input"
    )
    
    if user_input:
        logger.info(f"User input: {user_input}")
        
        # Add user message to conversation
        st.session_state.conversation.append({
            'role': 'user',
            'content': user_input
        })
        
        # Get response from backend
        with st.spinner("🤔 AI Assistant is thinking..."):
            response_data = call_backend(
                "/chat",
                method="POST",
                data={
                    "message": user_input,
                    "conversation_history": st.session_state.conversation[:-1]
                }
            )
        
        if response_data:
            # Update conversation with backend response
            st.session_state.conversation = response_data['conversation_history']
            st.rerun()


def page_feedback():
    """Collect user feedback with a mandatory email address."""
    st.subheader("📝 Application Feedback", divider="orange")
    st.markdown("Help us improve the KUTRRH assistant by sharing your experience.")

    with st.form("feedback_form", clear_on_submit=True):
        email = st.text_input("Email address *", placeholder="you@example.com")
        functions_used = st.multiselect(
            "Which functions did you use? *",
            ["Appointment booking", "Hospital information / customer support", "Both"],
        )
        booking_success = st.radio(
            "If you booked an appointment, did it complete successfully on your first attempt, and did the confirmation reflect your details and language?",
            ["Not applicable", "Yes", "Partly", "No"],
        )
        information_accuracy = st.radio(
            "If you asked a hospital information question, was the answer accurate and clearly based on an official hospital source?",
            ["Not applicable", "Yes", "Partly", "No"],
        )
        knowledge_base_honesty = st.radio(
            "When the knowledge base had no answer, did the system say so honestly rather than make something up?",
            ["Not applicable", "Yes", "Partly", "No"],
        )
        queue_recommendations = st.radio(
            "Were queue/slot congestion recommendations useful and trustworthy?",
            ["Not applicable", "Yes, I chose a lower-wait slot", "Useful, but I chose another time", "No"],
        )
        language_consistency = st.radio(
            "Did the system recognize and consistently use your preferred language, including booking confirmation?",
            ["Yes", "Partly", "No"],
        )
        misread_request = st.radio(
            "Did the system misread what you wanted, such as asking booking questions when you wanted information?",
            ["No", "Once", "More than once"],
        )
        personal_details_concern = st.radio(
            "Did you have concerns about why the system requested personal details?",
            ["No", "Some concerns", "Yes"],
        )
        natural_effort = st.select_slider(
            "Compared with calling or visiting the hospital, how natural and low-effort was the conversation?",
            options=[1, 2, 3, 4, 5], value=3,
        )
        confidence_change = st.text_area(
            "What one change would most increase your confidence in relying on this system for a real hospital visit? *",
            placeholder="Share the most important improvement.",
        )
        additional_feedback = st.text_area(
            "Additional comments",
            placeholder="Anything else you would like us to know?",
        )
        submitted = st.form_submit_button("📨 Submit feedback", type="primary", use_container_width=True)

        if submitted:
            if not email.strip() or "@" not in email:
                st.error("Please enter a valid email address.")
            elif not functions_used:
                st.error("Please select the function(s) you used.")
            elif not confidence_change.strip():
                st.error("Please answer the confidence-improvement question.")
            else:
                message = "\n".join([
                    f"Functions used: {', '.join(functions_used)}",
                    f"Booking completion and confirmation: {booking_success}",
                    f"Information accuracy and official sourcing: {information_accuracy}",
                    f"Knowledge-base honesty: {knowledge_base_honesty}",
                    f"Queue/slot recommendations: {queue_recommendations}",
                    f"Language consistency: {language_consistency}",
                    f"Request interpretation errors: {misread_request}",
                    f"Personal-details concerns: {personal_details_concern}",
                    f"Natural/low-effort rating: {natural_effort}/5",
                    f"Confidence improvement: {confidence_change.strip()}",
                    f"Additional comments: {additional_feedback.strip()}",
                ])
                result = call_backend(
                    "/feedback",
                    method="POST",
                    data={"email": email, "rating": natural_effort, "message": message},
                )
                if result:
                    st.success("Thank you. Your feedback was submitted successfully.")


# ============================================================================
# PAGE 2: Book Appointment
# ============================================================================

def page_book_appointment():
    """Appointment booking page"""
    st.subheader("📅 Book Your Appointment", divider="green")
    
    st.markdown("""
    Schedule your visit at KUTRRH easily. Our system will recommend 
    the best available time slots based on congestion and your preferences.
    """)
    
    # ========================================================================
    # STEP 1: Patient Information
    # ========================================================================
    
    st.markdown("### 📋 Step 1: Your Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        person_name = st.text_input(
            "Full Name *",
            placeholder="Enter your full name",
            key="book_name",
            help="Your complete name as it appears in your identification"
        )
        
        patient_id_input = st.text_input(
            "Patient ID / National ID *",
            placeholder="e.g., 12345678",
            key="book_patient_id",
            help="Your national ID or patient identification number"
        )
        patient_id = ''.join(filter(str.isdigit, patient_id_input))
    
    with col2:
        phone_number = st.text_input(
            "Phone Number *",
            placeholder="+254 XXX XXX XXX",
            key="book_phone",
            help="We'll use this to confirm your appointment"
        )
        
        email_address = st.text_input(
            "Email Address *",
            placeholder="your.email@example.com",
            key="book_email",
            help="Appointment confirmation will be sent to your email"
        )
    
    st.divider()
    
    # ========================================================================
    # STEP 2: Appointment Details
    # ========================================================================
    
    st.markdown("### 🏥 Step 2: Appointment Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        appointment_type = st.selectbox(
            "Service Type *",
            ["consultation", "checkup", "follow-up"],
            key="book_type",
            help="Select the type of medical service you need",
            format_func=lambda x: {
                "consultation": "💊 Consultation",
                "checkup": "🔍 General Checkup",
                "follow-up": "📌 Follow-up Appointment"
            }.get(x, x)
        )
    
    with col2:
        appointment_date = st.date_input(
            "Preferred Date *",
            min_value=datetime.date.today(),
            key="book_date",
            help="Select a date from today onwards"
        )
    
    st.divider()
    
    # ========================================================================
    # STEP 3: Time Slot Selection
    # ========================================================================
    
    recommended_slots = []
    analytics = {}
    
    if appointment_date and appointment_type:
        st.markdown("### ⏰ Step 3: Select Time Slot")
        
        slot_response = call_backend(
            f"/recommendations/slots?appointment_type={appointment_type}&date={appointment_date.isoformat()}&num_recommendations=5"
        )
        
        if slot_response:
            recommended_slots = slot_response.get('slots', [])
            analytics = slot_response.get('analytics', {})
            
            if recommended_slots:
                # Display analytics in metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "🟢 Low-Wait Slots",
                        f"{analytics.get('low_congestion_slots', 0)}/{analytics.get('total_slots', 0)}"
                    )
                
                with col2:
                    st.metric(
                        "⏱️ Average Wait Time",
                        f"{analytics.get('avg_wait_time', 0)} min"
                    )
                
                with col3:
                    st.metric(
                        "📊 Availability Score",
                        f"{analytics.get('availability_score', 0)}%"
                    )
                
                st.divider()
                
                st.markdown("**Select your preferred time slot:**")
                
                # Display slots as buttons in columns
                slot_columns = st.columns(min(5, len(recommended_slots)))
                
                for idx, slot in enumerate(recommended_slots):
                    with slot_columns[idx]:
                        congestion = slot['congestion_level']
                        wait_time = int(slot['predicted_wait_minutes'])
                        
                        # Emoji based on congestion
                        emoji = "🟢" if congestion == "Low" else "🟡" if congestion == "Moderate" else "🔴"
                        
                        # Color-coded button
                        button_label = f"{emoji}\n{slot['time']}\n{wait_time}m wait"
                        
                        if st.button(
                            button_label,
                            use_container_width=True,
                            key=f"slot_{idx}",
                            type="primary" if st.session_state.selected_slot == slot['time'] else "secondary"
                        ):
                            st.session_state.selected_slot = slot['time']
                            st.session_state.show_confirmation = True
                            st.rerun()
                
                st.divider()
            else:
                st.warning("⚠️ No available slots for this date. Please select a different date.")
    
    # ========================================================================
    # Confirmation Section
    # ========================================================================
    
    if st.session_state.get('show_confirmation') and st.session_state.selected_slot:
        st.markdown("### ✅ Confirm Your Appointment")
        
        confirmation_box = st.container(border=True)
        
        with confirmation_box:
            col1, col2 = st.columns(2)
            
            # Patient info column
            with col1:
                st.markdown("**📋 Your Information:**")
                info_text = f"""
                👤 **Name:** {person_name or 'Not entered'}
                
                🆔 **Patient ID:** {patient_id or 'Not entered'}
                
                📱 **Phone:** {phone_number or 'Not entered'}
                
                📧 **Email:** {email_address or 'Not entered'}
                """
                st.write(info_text)
            
            # Appointment info column
            with col2:
                st.markdown("**🏥 Appointment Details:**")
                apt_text = f"""
                💊 **Service:** {appointment_type.title()}
                
                📅 **Date:** {appointment_date.strftime('%B %d, %Y')}
                
                ⏰ **Time:** {st.session_state.selected_slot}
                
                📍 **Location:** Main Hospital
                """
                st.write(apt_text)
            
            st.divider()
            
            # Confirmation buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button(
                    "✅ Confirm",
                    use_container_width=True,
                    key="confirm_btn",
                    type="primary"
                ):
                    # Validate inputs
                    errors = []
                    
                    if not person_name.strip():
                        errors.append("❌ Please enter your full name")
                    if not patient_id:
                        errors.append("❌ Please enter a valid patient ID number")
                    if not phone_number.strip():
                        errors.append("❌ Please enter your phone number")
                    if not email_address.strip() or '@' not in email_address:
                        errors.append("❌ Please enter a valid email address")
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        try:
                            dialog_time = datetime.datetime.strptime(
                                st.session_state.selected_slot, "%H:%M"
                            ).time()
                            
                            # Create appointment via backend
                            apt_data = {
                                "name": person_name.strip(),
                                "patient_id": patient_id.strip(),
                                "phone": phone_number.strip(),
                                "email": email_address.strip(),
                                "type": appointment_type,
                                "datetime": f"{appointment_date}T{dialog_time.isoformat()}",
                                "status": "confirmed"
                            }
                            
                            with st.spinner("📝 Creating your appointment..."):
                                result = call_backend("/appointments", method="POST", data=apt_data)
                            
                            if result:
                                st.success("🎉 Appointment Confirmed Successfully!")
                                
                                # Show confirmation details
                                success_box = st.container(border=True)
                                
                                with success_box:
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        st.markdown("**Confirmation Details:**")
                                        conf_text = f"""
                                        **Appointment ID:**
                                        `{result.get('id', 'N/A')}`
                                        
                                        **Patient ID:** {patient_id}
                                        
                                        **Name:** {person_name}
                                        """
                                        st.write(conf_text)
                                    
                                    with col2:
                                        st.markdown("**Appointment Info:**")
                                        apt_conf_text = f"""
                                        **Date:** {appointment_date.strftime('%B %d, %Y')}
                                        
                                        **Time:** {dialog_time.strftime('%I:%M %p')}
                                        
                                        **Service:** {appointment_type.title()}
                                        """
                                        st.write(apt_conf_text)
                                        
                                        if result.get('predicted_wait_minutes'):
                                            wait = result['predicted_wait_minutes']
                                            congestion = "🟢 Low" if wait <= 15 else "🟡 Moderate" if wait <= 30 else "🔴 High"
                                            st.markdown(f"**Est. Wait:** {congestion} ({wait:.0f} min)")
                                
                                st.divider()
                                
                                st.info(
                                    "✓ Please arrive 15 minutes early for check-in\n\n"
                                    "✓ A confirmation SMS and email have been sent to you\n\n"
                                    "✓ Keep your Appointment ID for your records"
                                )
                                
                                # Clear state and reset form
                                st.session_state.show_confirmation = False
                                st.session_state.selected_slot = None
                                st.session_state.conversation = []
                                
                                # Show success and offer next steps
                                st.markdown("""
                                ### What's Next?
                                - Check your email and SMS for confirmation details
                                - Add the appointment to your calendar
                                - Contact us if you need to reschedule
                                """)
                        
                        except Exception as e:
                            st.error(f"❌ Error creating appointment: {str(e)}")
                            logger.error(f"Error creating appointment: {str(e)}")
            
            with col2:
                if st.button(
                    "❌ Cancel",
                    use_container_width=True,
                    key="cancel_btn"
                ):
                    st.session_state.show_confirmation = False
                    st.session_state.selected_slot = None
                    st.rerun()
            
            with col3:
                st.empty()


# ============================================================================
# Main Application
# ============================================================================

def main():
    initialize_session_state()
    
    # Display KUTRRH header
    kutrrh_header()
    
    # Check backend connectivity with better error handling
    try:
        health_check = call_backend("/health")
        if not health_check:
            st.warning("⚠️ Backend service is loading. Please refresh the page.")
    except Exception as e:
        st.warning(f"⚠️ Connecting to backend... Please try again if issues persist.")
        logger.warning(f"Backend connection issue: {str(e)}")
    
    # Show page navigation
    show_page_navigation()
    
    # Render selected page
    if st.session_state.current_page == "chat":
        page_chat()
    elif st.session_state.current_page == "book":
        page_book_appointment()
    else:
        page_feedback()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🏥 KUTRRH | AI-Powered Appointment Management System</p>
        <p>For emergencies, call: <strong>+254 20 8 000 000</strong> | Support: help@kutrrh.go.ke</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">© 2026 Kenyatta University Teaching, Referral and Research Hospital</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
