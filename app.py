import streamlit as st
from agent import receive_message_from_caller, CONVERSATION
from langchain_core.messages import HumanMessage
from config import AppConfig
from logger import setup_logger
from appointments_db import add_appointment, get_appointments
from appointment_recommender import get_recommender
import datetime
import numpy as np
import os

# Set random seeds for deterministic ML predictions
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(42)
try:
    import tensorflow as tf
    tf.random.set_seed(42)
except ImportError:
    pass

logger = setup_logger(__name__)


def initialize_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    if 'show_confirmation' not in st.session_state:
        st.session_state.show_confirmation = False


def main():
    config = AppConfig()
    initialize_session_state()

    st.set_page_config(layout="wide", page_title="KUTRRH - Hospital Appointment System")
    
    # Hospital header with logo and branding
    header_col1, header_col2, header_col3 = st.columns([0.5, 2, 0.5])
    
    with header_col1:
        st.write("")  # Spacing
    
    with header_col2:
        st.markdown("""
        <div style="text-align: center;">
            <h2 style="color: #1f4788; margin: 0; font-weight: bold;">
                🏥 KUTRRH HOSPITAL
            </h2>
            <p style="color: #666; margin: 5px 0; font-size: 14px;">
                Kenyatta University Teaching, Referral and Research Hospital
            </p>
            <h3 style="color: #2196F3; margin: 10px 0;">
                AI-Powered Appointment Management System
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col3:
        st.write("")  # Spacing
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("💬 Chat with AI Assistant")
        
        # Display conversation
        for message in CONVERSATION:
            if isinstance(message, HumanMessage):
                st.chat_message("user").write(message.content)
            else:
                st.chat_message("assistant").write(message.content)

        # User input
        user_input = st.chat_input("Ask about appointments, book a slot, or get recommendations...")
        if user_input:
            logger.debug(f"Received user input: {user_input}")
            receive_message_from_caller(user_input)
            st.rerun()

    with col2:
        st.subheader("📊 Appointment Dashboard")
        
        # Get current appointments
        appointments = get_appointments(filter_by_status='confirmed')
        
        if appointments:
            st.success(f"**{len(appointments)} Active Appointments**")
            
            # Display appointments in a table
            for apt in appointments[:5]:
                with st.container(border=True):
                    # Header with ID and patient name
                    st.markdown(f"**{apt['name']}** - `{apt['id']}`")
                    
                    # Service type and date/time
                    info_col1, info_col2 = st.columns(2)
                    with info_col1:
                        st.caption(f"🏥 Service: {apt['type']}")
                    with info_col2:
                        st.caption(f"📅 {apt.get('datetime', 'N/A')}")
                    
                    # Wait time and congestion
                    if apt.get('predicted_wait_minutes'):
                        wait = apt['predicted_wait_minutes']
                        if wait <= 15:
                            congestion = "🟢 Low"
                        elif wait <= 30:
                            congestion = "🟡 Moderate"
                        else:
                            congestion = "🔴 High"
                        st.caption(f"⏱️ Est. wait: {wait:.0f} min ({congestion})")
        else:
            st.info("No appointments scheduled yet")
        
        # Manual appointment form with recommendations
        st.divider()
        st.subheader("➕ Quick Add Appointment")
        
        # Patient Information Section
        st.markdown("**📋 Patient Information:**")
        form_info_col1, form_info_col2 = st.columns(2)
        with form_info_col1:
            person_name = st.text_input("Patient Name *", placeholder="Full name", key="form_name")
            patient_id_input = st.text_input("Patient ID Number *", placeholder="12345678", key="form_patient_id")
            # Filter to only numerical values
            patient_id = ''.join(filter(str.isdigit, patient_id_input))
        
        with form_info_col2:
            phone_number = st.text_input("Phone Number *", placeholder="+254 XXX XXX XXX", key="form_phone")
            email_address = st.text_input("Email Address *", placeholder="patient@example.com", key="form_email")
        
        # Appointment Details Section
        st.markdown("**📅 Appointment Details:**")
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            appointment_type = st.selectbox("Service Type *", ["consultation", "checkup", "follow-up"], key="form_type")
        
        with col_form2:
            appointment_date = st.date_input("Date *", key="form_date")
        
        # Show recommendations when type and date are selected
        if appointment_date and appointment_type:
            st.markdown("**📅 Recommended Time Slots:**")
            try:
                recommender = get_recommender()
                date_obj = datetime.datetime.combine(appointment_date, datetime.time(0, 0))
                slots, analytics = recommender.recommend_optimal_slots(
                    appointment_type, date_obj, num_recommendations=5
                )
                
                # Display recommended slots with color coding
                slot_col1, slot_col2 = st.columns([2, 2])
                
                with slot_col1:
                    st.caption("**Available Slots:**")
                    
                    # Create slot options for selectbox
                    slot_options = []
                    slot_map = {}
                    for i, slot in enumerate(slots):
                        # Color code the display
                        if slot['congestion_level'] == 'Low':
                            display_text = f"🟢 {slot['time']} (Low wait: {slot['predicted_wait_minutes']:.0f} min)"
                        elif slot['congestion_level'] == 'Moderate':
                            display_text = f"🟡 {slot['time']} (Moderate: {slot['predicted_wait_minutes']:.0f} min)"
                        else:
                            display_text = f"🔴 {slot['time']} (High wait: {slot['predicted_wait_minutes']:.0f} min)"
                        
                        slot_options.append(display_text)
                        slot_map[display_text] = slot['time']
                    
                    # Use selectbox for better responsiveness
                    selected_option = st.selectbox("Select a time slot:", slot_options, key="slot_selection")
                    
                    # Store selected slot in session immediately
                    if selected_option in slot_map:
                        st.session_state.selected_slot = slot_map[selected_option]
                        st.session_state.show_confirmation = True
                
                with slot_col2:
                    st.caption("**Daily Analytics:**")
                    st.metric("Low-Congestion Slots", f"{analytics['low_congestion_slots']}/{analytics['total_slots']}")
                    st.metric("Avg Wait Time", f"{analytics['avg_wait_time']} min")
                    st.metric("Availability Score", f"{analytics['availability_score']}%")
                
                st.divider()
                
            except Exception as e:
                st.warning(f"Could not load recommendations: {str(e)}")
        
        # Show confirmation dialog if a slot was selected
        if st.session_state.get('show_confirmation') and 'selected_slot' in st.session_state:
            st.divider()
            st.markdown("### 📝 Confirm Your Appointment")
            
            # Modal-style dialog - Read-only confirmation
            with st.container(border=True):
                col_dialog1, col_dialog2 = st.columns(2)
                
                with col_dialog1:
                    st.markdown("**📋 Patient Information:**")
                    st.text(f"👤 **Name:** {person_name}")
                    st.text(f"🆔 **Patient ID:** {patient_id}")
                    st.text(f"📱 **Phone:** {phone_number}")
                    st.text(f"📧 **Email:** {email_address}")
                
                with col_dialog2:
                    st.markdown("**📅 Appointment Details:**")
                    st.text(f"🏥 **Service Type:** {appointment_type}")
                    st.text(f"📅 **Date:** {appointment_date.strftime('%B %d, %Y')}")
                    st.text(f"⏰ **Time:** {st.session_state.selected_slot}")
                
                st.divider()
                
                # Dialog buttons
                button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
                
                with button_col1:
                    if st.button("✅ Confirm Appointment", use_container_width=True, key="dialog_confirm"):
                        # Validate that all required fields were filled in the form above
                        if not person_name.strip():
                            st.error("❌ Patient Name is required")
                        elif not patient_id:
                            st.error("❌ Patient ID Number is required (numbers only)")
                        elif not phone_number.strip():
                            st.error("❌ Phone Number is required")
                        elif not email_address.strip():
                            st.error("❌ Email Address is required")
                        elif '@' not in email_address:
                            st.error("❌ Please enter a valid email address")
                        else:
                            try:
                                dialog_time = datetime.datetime.strptime(st.session_state.selected_slot, "%H:%M").time()
                                appointment_record = {
                                    "name": person_name.strip(),
                                    "patient_id": patient_id.strip(),
                                    "phone": phone_number.strip(),
                                    "email": email_address.strip(),
                                    "type": appointment_type,
                                    "datetime": f"{appointment_date}T{dialog_time.isoformat()}",
                                    "status": "confirmed"
                                }
                                result = add_appointment(appointment_record)
                                
                                # Display confirmation with ID
                                st.success(f"✅ Appointment Created Successfully!")
                                
                                with st.container(border=True):
                                    conf_col1, conf_col2 = st.columns(2)
                                    
                                    with conf_col1:
                                        st.markdown(f"**🏥 Appointment ID:** `{result['id']}`")
                                        st.markdown(f"**👤 Patient ID:** `{patient_id}`")
                                        st.markdown(f"**Patient Name:** {person_name}")
                                        st.markdown(f"**Phone:** {phone_number}")
                                    
                                    with conf_col2:
                                        st.markdown(f"**📅 Date:** {appointment_date.strftime('%B %d, %Y')}")
                                        st.markdown(f"**⏰ Time:** {dialog_time.strftime('%I:%M %p')}")
                                        
                                        if result.get('predicted_wait_minutes'):
                                            wait = result['predicted_wait_minutes']
                                            if wait <= 15:
                                                congestion = "🟢 Low"
                                            elif wait <= 30:
                                                congestion = "🟡 Moderate"
                                            else:
                                                congestion = "🔴 High"
                                            st.markdown(f"**⏳ Estimated Wait:** {congestion} ({wait:.0f} min)")
                                
                                st.divider()
                                st.markdown("**✓ Please arrive 15 minutes early for check-in**")
                                
                                # Clear the selected slot
                                if 'selected_slot' in st.session_state:
                                    del st.session_state.selected_slot
                                st.session_state.show_confirmation = False
                                
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                                logger.error(f"Error creating appointment: {e}")
                
                with button_col2:
                    if st.button("❌ Cancel", use_container_width=True, key="dialog_cancel"):
                        st.session_state.show_confirmation = False
                        if 'selected_slot' in st.session_state:
                            del st.session_state.selected_slot
                        st.rerun()
                
                with button_col3:
                    st.write("")  # Spacing


if __name__ == "__main__":
    main()
