"""
Enhanced Appointment Booking Tools with TCN Scheduling + Intelligent Recommendations
Integrates prescriptive scheduling, persistence, and batch processing
"""

from langchain_core.tools import tool
import datetime
import streamlit as st
from logger import setup_logger
from config import AppConfig
from appointments_db import add_appointment, cancel_appointment as db_cancel, get_appointments, check_conflict, get_appointment_stats, get_next_appointment as get_next_apt_db
from appointment_recommender import get_recommender, CongestionCategory
from email_service import send_appointment_confirmation_email

logger = setup_logger(__name__)
config = AppConfig()


@tool
def book_appointment(person_name: str, patient_id: str, phone_number: str, email_address: str, 
                     appointment_type: str, appointment_year: int, appointment_month: int,
                     appointment_day: int, appointment_hour: int, appointment_minute: int):
    """
    Book an appointment with AI-predicted waiting time.
    Requires patient information: name, ID, phone, and email.
    Checks for conflicts and stores in persistent database.
    Returns confirmation with predicted wait time and congestion level.
    """
    logger.debug(f"Attempting to book appointment for {person_name}")
    
    # Validate patient information
    if not person_name or not person_name.strip():
        return "❌ Error: Patient name is required."
    if not patient_id or not patient_id.strip():
        return "❌ Error: Patient ID is required."
    if not phone_number or not phone_number.strip():
        return "❌ Error: Phone number is required."
    if not email_address or '@' not in email_address:
        return "❌ Error: Valid email address is required."
    
    try:
        appointment_time = datetime.datetime(
            appointment_year, appointment_month, appointment_day, 
            appointment_hour, appointment_minute
        )
        
        # Get recommender for prediction
        recommender = get_recommender()
        wait_time, confidence = recommender.predictor.predict_waiting_time(
            appointment_type, appointment_time
        )
        
        # Categorize congestion
        congestion = CongestionCategory.categorize(wait_time)
        
        # Check for conflicts
        conflict = check_conflict(appointment_time.isoformat(), duration_minutes=30)
        conflict_warning = ""
        if conflict:
            conflict_warning = f" ⚠️ Note: Overlaps with {conflict['name']}'s appointment"
        
        # Create appointment record with patient details
        appointment_record = {
            "name": person_name.strip(),
            "patient_id": patient_id.strip(),
            "phone": phone_number.strip(),
            "email": email_address.strip(),
            "type": appointment_type,
            "datetime": appointment_time.isoformat(),
            "predicted_wait_minutes": round(wait_time, 1),
            "confidence": round(confidence, 2),
            "congestion_level": congestion['level'],
            "duration_minutes": 30,
            "status": "confirmed"
        }
        
        # Save to database
        saved_apt = add_appointment(appointment_record)

        # Send confirmation email (best-effort; booking already succeeded regardless of outcome)
        email_sent = send_appointment_confirmation_email(
            recipient_email=email_address.strip(),
            patient_name=person_name.strip(),
            appointment_id=saved_apt['id'],
            appointment_type=appointment_type,
            appointment_time_display=appointment_time.strftime('%B %d, %Y at %I:%M %p'),
        )
        email_status_line = (
            "📧 **Confirmation email sent**" if email_sent
            else "⚠️ Confirmation email could not be sent; please note your Appointment ID."
        )

        # Format response
        response = (
            f"✅ **Appointment Booked!**\n\n"
            f"**Patient:** {person_name}\n"
            f"**Patient ID:** {patient_id}\n"
            f"**Contact:** {phone_number} | {email_address}\n"
            f"**Type:** {appointment_type}\n"
            f"**Date/Time:** {appointment_time.strftime('%B %d, %Y at %I:%M %p')}\n"
            f"**Appointment ID:** {saved_apt['id']}\n\n"
            f"{congestion['emoji']} **Congestion Level:** {congestion['level']}\n"
            f"⏱️ **Predicted Wait:** {wait_time:.0f} minutes\n"
            f"📊 **Confidence:** {confidence*100:.0f}%\n"
            f"{email_status_line}\n"
            f"{conflict_warning}"
        )
        
        logger.info(f"✅ Booked: {saved_apt['id']} for {person_name} (ID: {patient_id})")
        return response
        
    except ValueError as e:
        return f"❌ Error: {str(e)}"
    except Exception as e:
        logger.error(f"Error booking appointment: {e}")
        return f"❌ Error booking appointment: {str(e)}"


@tool
def get_optimal_appointment_slots(appointment_type: str, preferred_date: str):
    """
    Get optimal appointment slots with lowest predicted waiting times.
    Uses batch TCN predictions to identify least busy periods.
    Returns color-coded recommendations (Green=Low, Yellow=Moderate, Red=High congestion).
    """
    num_recommendations = 5
    logger.debug(f"Getting optimal slots for {appointment_type} on {preferred_date}")
    
    try:
        
        # Parse date
        date_obj = datetime.datetime.strptime(preferred_date, '%Y-%m-%d')
        
        # Get recommender
        recommender = get_recommender()
        
        # Get optimal slots
        slots, analytics = recommender.recommend_optimal_slots(
            appointment_type, date_obj, num_recommendations
        )
        
        # Build response
        response = f"🎯 **Best Available Slots for {appointment_type}**\n"
        response += f"📅 **{preferred_date}**\n\n"
        
        for i, slot in enumerate(slots, 1):
            response += (
                f"{i}. {slot['congestion_emoji']} **{slot['time']}**\n"
                f"   {slot['congestion_color']} {slot['congestion_level']} congestion\n"
                f"   ⏱️ Est. wait: {slot['predicted_wait_minutes']:.0f} min "
                f"(confidence: {slot['confidence']*100:.0f}%)\n\n"
            )
        
        # Add analytics
        response += f"📊 **Daily Analytics:**\n"
        response += f"• Available low-congestion slots: {analytics['low_congestion_slots']}/{analytics['total_slots']}\n"
        response += f"• Average wait time: {analytics['avg_wait_time']} min\n"
        response += f"• Availability score: {analytics['availability_score']}%\n"
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting optimal slots: {e}")
        return f"❌ Error: {str(e)}"


@tool
def suggest_alternative_slots(appointment_type: str, preferred_date: str, preferred_time: str, num_alternatives: int = 3):
    """
    If user's preferred slot is congested, suggest better alternatives.
    Analyzes congestion level and recommends less busy times with lower predicted waits.
    """
    logger.debug(f"Suggesting alternatives for {appointment_type} at {preferred_time}")
    
    try:
        # Parse datetime
        preferred_datetime = datetime.datetime.strptime(
            f"{preferred_date} {preferred_time}", '%Y-%m-%d %H:%M'
        )
        
        # Get recommender
        recommender = get_recommender()
        
        # Suggest alternatives
        result = recommender.suggest_alternatives(
            appointment_type, preferred_datetime, num_alternatives
        )
        
        # Build response
        response = f"🔍 **Appointment Availability Analysis**\n\n"
        response += f"**Your Preferred Time:** {result['preferred']['time']}\n"
        response += (
            f"{result['preferred']['congestion_emoji']} "
            f"Congestion: {result['preferred']['congestion_level']}\n"
            f"⏱️ Predicted wait: {result['preferred']['predicted_wait_minutes']:.0f} min\n\n"
        )
        
        if result['recommendation'] == 'ACCEPT':
            response += "✅ **Great choice!** This time has low congestion.\n"
        
        elif result['recommendation'] == 'SUGGEST_ALTERNATIVE':
            response += f"⚠️ **We have better options:**\n\n"
            for i, alt in enumerate(result['alternatives'], 1):
                response += (
                    f"{i}. {alt['congestion_emoji']} **{alt['time']}** - "
                    f"{alt['congestion_color']} {alt['congestion_level']}\n"
                    f"   ⏱️ Wait: {alt['predicted_wait_minutes']:.0f} min "
                    f"(save {result['preferred']['predicted_wait_minutes'] - alt['predicted_wait_minutes']:.0f} min)\n\n"
                )
            response += f"💡 {result['message']}\n"
        
        else:
            response += f"ℹ️ {result['message']}\n"
        
        return response
        
    except Exception as e:
        logger.error(f"Error suggesting alternatives: {e}")
        return f"❌ Error: {str(e)}"


@tool
def get_wait_time_prediction(appointment_type: str, appointment_date: str, appointment_time: str):
    """
    Get waiting time prediction for a specific appointment slot.
    Includes confidence score and congestion categorization.
    """
    logger.debug(f"Predicting wait for {appointment_type} at {appointment_time}")
    
    try:
        appointment_datetime = datetime.datetime.strptime(
            f"{appointment_date} {appointment_time}", '%Y-%m-%d %H:%M'
        )
        
        recommender = get_recommender()
        wait_time, confidence = recommender.predictor.predict_waiting_time(
            appointment_type, appointment_datetime
        )
        
        congestion = CongestionCategory.categorize(wait_time)
        
        response = (
            f"⏱️ **Wait Time Prediction**\n\n"
            f"**Appointment:** {appointment_type} at {appointment_time}\n"
            f"**Predicted Wait:** {wait_time:.0f} minutes\n"
            f"{congestion['emoji']} **Congestion:** {congestion['level']}\n"
            f"📊 **Confidence:** {confidence*100:.0f}%\n"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error predicting wait time: {e}")
        return f"❌ Error: {str(e)}"


@tool
def get_least_busy_times(appointment_type: str, preferred_date: str):
    """
    Get the least busy appointment times for a given day.
    Returns slots with lowest predicted waiting times.
    """
    logger.debug(f"Getting least busy times for {appointment_type}")
    
    try:
        date_obj = datetime.datetime.strptime(preferred_date, '%Y-%m-%d')
        recommender = get_recommender()
        
        slots = recommender.get_least_busy_slots(appointment_type, date_obj, num_slots=5)
        
        response = f"🟢 **Least Busy Times for {appointment_type}**\n"
        response += f"📅 **{preferred_date}**\n\n"
        
        for i, slot in enumerate(slots, 1):
            response += (
                f"{i}. {slot['congestion_emoji']} **{slot['time']}** - "
                f"⏱️ {slot['predicted_wait_minutes']:.0f} min wait\n"
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting least busy times: {e}")
        return f"❌ Error: {str(e)}"


@tool
def get_busiest_times(appointment_type: str, preferred_date: str):
    """
    Get the busiest appointment times for a given day (times to avoid).
    Returns slots with highest predicted waiting times.
    """
    logger.debug(f"Getting busiest times for {appointment_type}")
    
    try:
        date_obj = datetime.datetime.strptime(preferred_date, '%Y-%m-%d')
        recommender = get_recommender()
        
        slots = recommender.get_busiest_slots(appointment_type, date_obj, num_slots=5)
        
        response = f"🔴 **Busiest Times to Avoid**\n"
        response += f"📅 **{preferred_date}**\n\n"
        
        for i, slot in enumerate(slots, 1):
            response += (
                f"{i}. {slot['congestion_emoji']} **{slot['time']}** - "
                f"⏱️ {slot['predicted_wait_minutes']:.0f} min wait (avoid!)\n"
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting busiest times: {e}")
        return f"❌ Error: {str(e)}"


@tool
def cancel_appointment(appointment_id: str, person_name: str):
    """
    Cancel an appointment by providing either the appointment ID or the patient name.
    Pass the appointment_id if known, otherwise pass the person_name.
    Pass an empty string for the parameter you do not have.
    """  
    reason = "Patient request"
    logger.debug(f"Attempting to cancel appointment: {appointment_id or person_name}")
    
    try:
        # Find appointment to cancel
        apt_to_cancel = None
        
        if appointment_id:
            appointments = get_appointments()
            apt_to_cancel = next((a for a in appointments if a['id'] == appointment_id), None)
        
        elif person_name:
            appointments = get_appointments(filter_by_status='confirmed')
            matching = [a for a in appointments if a['name'].lower() == person_name.lower()]
            if matching:
                apt_to_cancel = matching[0]
        
        if not apt_to_cancel:
            return f"❌ Appointment not found"
        
        # Cancel it
        success = db_cancel(apt_to_cancel['id'], reason)
        
        if success:
            response = (
                f"✅ **Appointment Cancelled**\n\n"
                f"**Patient:** {apt_to_cancel['name']}\n"
                f"**ID:** {apt_to_cancel['id']}\n"
                f"**Type:** {apt_to_cancel['type']}\n"
                f"**Original Time:** {apt_to_cancel.get('datetime', 'N/A')}\n"
                f"**Reason:** {reason}"
            )
            logger.info(f"✅ Cancelled: {apt_to_cancel['id']}")
            return response
        
        return "❌ Failed to cancel appointment"
        
    except Exception as e:
        logger.error(f"Error cancelling appointment: {e}")
        return f"❌ Error: {str(e)}"


@tool
def get_next_available_appointment():
    """
    Get the next scheduled appointment in the system.
    Shows details with predicted waiting time.
    """
    logger.debug("Getting next available appointment")
    
    try:
        apt = get_next_apt_db()
        
        if not apt:
            return "📅 No upcoming appointments scheduled."
        
        response = (
            f"📅 **Next Appointment**\n\n"
            f"**Patient:** {apt['name']}\n"
            f"**Type:** {apt['type']}\n"
            f"**ID:** {apt['id']}\n"
            f"**Scheduled:** {apt['datetime']}\n"
            f"⏱️ **Predicted Wait:** {apt.get('predicted_wait_minutes', 'N/A')} min\n"
            f"**Status:** {apt['status']}"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting next appointment: {e}")
        return f"❌ Error: {str(e)}"


@tool
def view_all_appointments():
    """
    View all confirmed appointments with details.
    Displays statistics including total appointments, types, and average wait.
    """
    logger.debug("Viewing all appointments")
    
    try:
        appointments = get_appointments(filter_by_status='confirmed')
        stats = get_appointment_stats()
        
        if not appointments:
            return "📅 No appointments scheduled."
        
        response = f"📊 **Appointment Summary**\n\n"
        response += f"**Total Appointments:** {stats['total']}\n"
        response += f"**Upcoming:** {stats['upcoming_count']}\n"
        response += f"**Average Wait Time:** {stats['average_wait_time']} min\n\n"
        
        response += "**Appointments by Type:**\n"
        for apt_type, count in stats['by_type'].items():
            response += f"• {apt_type}: {count}\n"
        
        response += f"\n**All Appointments:**\n"
        for apt in appointments[:10]:  # Show first 10
            response += (
                f"• {apt['name']} - {apt['type']} "
                f"({apt['datetime']}) - Wait: {apt.get('predicted_wait_minutes', 'N/A')} min\n"
            )
        
        if len(appointments) > 10:
            response += f"... and {len(appointments) - 10} more\n"
        
        return response
        
    except Exception as e:
        logger.error(f"Error viewing appointments: {e}")
        return f"❌ Error: {str(e)}"
