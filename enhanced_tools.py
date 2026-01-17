"""
Enhanced Appointment Booking Tools with TCN Scheduling
Integrates prescriptive scheduling for optimal appointment times
"""

from langchain_core.tools import tool
import datetime
import streamlit as st
from logger import setup_logger
from config import AppConfig
from scheduling_model import SchedulingPredictor, get_predictor

logger = setup_logger(__name__)
config = AppConfig()

# Initialize predictor
predictor = None


def init_predictor(model_path=None):
    """Initialize the scheduling predictor"""
    global predictor
    if predictor is None:
        # Use real model if available
        model_path = model_path or "models/tcn_scheduling_model.h5"
        predictor = SchedulingPredictor(model_path=model_path, framework="tensorflow")
        logger.info(f"Scheduling predictor initialized with model: {model_path}")
    return predictor


@tool
def book_appointment(person_name: str, appointment_type: str, appointment_year: int, appointment_month: int,
                     appointment_day: int, appointment_hour: int, appointment_minute: int):
    """
    Book an appointment with the given details.
    Uses ML model to provide waiting time predictions.
    """
    logger.debug(f"Attempting to book appointment for {person_name}")
    time = datetime.datetime(appointment_year, appointment_month, appointment_day, appointment_hour, appointment_minute)
    
    # Initialize predictor if needed
    init_predictor()
    
    # Predict waiting time for this slot
    wait_time, confidence = predictor.predict_waiting_time(appointment_type, time)
    
    new_appointment = {
        "name": person_name,
        "type": appointment_type,
        "time": time,
        "predicted_wait_minutes": round(wait_time, 1),
        "wait_confidence": round(confidence, 2)
    }

    if 'appointments' not in st.session_state:
        logger.warning("appointments not in session state, initializing")
        st.session_state.appointments = []

    st.session_state.appointments.append(new_appointment)

    logger.info(f"Booked appointment: {new_appointment}")
    logger.debug(f"Current appointments: {st.session_state.appointments}")

    return (f"✅ Appointment booked for {person_name} ({appointment_type}) on "
            f"{time.strftime('%B %d, %Y at %I:%M %p')}. "
            f"Predicted waiting time: {wait_time:.0f} minutes "
            f"(confidence: {confidence*100:.0f}%). "
            f"Is there anything else you need?")


@tool
def get_next_available_appointment():
    """
    Get the next available appointment slot with minimal predicted waiting time.
    Uses ML model to recommend slots that minimize patient wait duration.
    """
    logger.debug("Checking for next available optimal appointment")
    if 'appointments' not in st.session_state or not st.session_state.appointments:
        logger.info("No appointments found")
        return "All time slots are currently available. When would you like to schedule your appointment?"

    current_time = datetime.datetime.now()
    
    # Initialize predictor
    init_predictor()
    
    # Find next available slot
    next_slot = current_time + datetime.timedelta(minutes=(30 - current_time.minute % 30))
    
    # Check for conflicts
    while any(appointment["time"] == next_slot for appointment in st.session_state.appointments):
        next_slot += datetime.timedelta(minutes=30)
    
    # Get predicted waiting time
    appointment_type = st.session_state.appointments[-1]["type"] if st.session_state.appointments else "checkup"
    wait_time, confidence = predictor.predict_waiting_time(appointment_type, next_slot)

    logger.info(f"Next available slot: {next_slot} with {wait_time:.0f} min predicted wait")
    
    return (f"The next available slot is {next_slot.strftime('%B %d, %Y at %I:%M %p')}. "
            f"Predicted waiting time: {wait_time:.0f} minutes. "
            f"Would you like to book this time or see other options?")


@tool
def get_optimal_appointment_slots(appointment_type: str, preferred_date: str, num_recommendations: int = 5):
    """
    Get recommended appointment slots for a given date that minimize predicted waiting time.
    Uses ML predictions to identify optimal booking times.
    
    Args:
        appointment_type: Type of appointment (e.g., 'consultation', 'checkup')
        preferred_date: Date in format YYYY-MM-DD
        num_recommendations: Number of recommended slots to return
    """
    logger.debug(f"Getting optimal slots for {appointment_type} on {preferred_date}")
    
    try:
        # Parse date
        date_obj = datetime.datetime.strptime(preferred_date, "%Y-%m-%d").date()
        
        # Initialize predictor
        init_predictor()
        
        # Get optimal slots
        optimal_slots = predictor.recommend_optimal_slots(
            appointment_type, 
            date_obj, 
            num_recommendations=num_recommendations
        )
        
        if not optimal_slots:
            return f"No available slots found for {preferred_date}. Please try another date."
        
        # Format response
        response = f"🎯 Optimal appointment times for {appointment_type.title()} on {preferred_date}:\n\n"
        for slot in optimal_slots:
            response += (f"{slot['rank']}. {slot['time']} - "
                        f"Predicted wait: {slot['predicted_wait_minutes']:.0f} min "
                        f"(confidence: {slot['confidence']*100:.0f}%)\n")
        
        response += "\nThese times are ranked by lowest predicted waiting time. "
        response += "Which time would you prefer?"
        
        logger.info(f"Recommended {len(optimal_slots)} optimal slots")
        return response
        
    except ValueError:
        logger.error(f"Invalid date format: {preferred_date}")
        return (f"Please provide the date in YYYY-MM-DD format. "
                f"For example, 2026-01-20 for January 20, 2026.")


@tool
def cancel_appointment(year: int, month: int, day: int, hour: int, minute: int):
    """
    Cancel an appointment at the specified time.
    """
    logger.debug(f"Attempting to cancel appointment at {year}-{month}-{day} {hour}:{minute}")
    
    cancel_time = datetime.datetime(year, month, day, hour, minute)
    
    if 'appointments' not in st.session_state:
        return "No appointments to cancel."

    initial_count = len(st.session_state.appointments)
    st.session_state.appointments = [
        app for app in st.session_state.appointments 
        if app["time"] != cancel_time
    ]

    if len(st.session_state.appointments) < initial_count:
        logger.info(f"Cancelled appointment at {cancel_time}")
        return f"Appointment on {cancel_time.strftime('%B %d, %Y at %I:%M %p')} has been cancelled."
    else:
        logger.warning(f"No appointment found at {cancel_time}")
        return f"No appointment found at {cancel_time.strftime('%B %d, %Y at %I:%M %p')}."


@tool
def get_wait_time_prediction(appointment_type: str, appointment_year: int, appointment_month: int,
                            appointment_day: int, appointment_hour: int, appointment_minute: int):
    """
    Get predicted waiting time for a specific appointment without booking.
    Helps patients understand expected wait times for different time slots.
    """
    logger.debug(f"Getting wait time prediction for {appointment_type}")
    
    appointment_time = datetime.datetime(
        appointment_year, appointment_month, appointment_day, 
        appointment_hour, appointment_minute
    )
    
    # Initialize predictor
    init_predictor()
    
    wait_time, confidence = predictor.predict_waiting_time(appointment_type, appointment_time)
    
    return (f"For a {appointment_type} appointment on "
            f"{appointment_time.strftime('%B %d, %Y at %I:%M %p')}, "
            f"the predicted waiting time is {wait_time:.0f} minutes "
            f"(confidence: {confidence*100:.0f}%). "
            f"Would you like to book at this time or see other options?")


@tool
def get_busiest_times(appointment_type: str, date_str: str):
    """
    Get the busiest appointment times for a given date.
    Helps patients understand when to avoid for shorter waits.
    
    Args:
        appointment_type: Type of appointment
        date_str: Date in format YYYY-MM-DD
    """
    logger.debug(f"Getting busiest times for {appointment_type} on {date_str}")
    
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Initialize predictor
        init_predictor()
        
        busiest = predictor.get_busiest_times(appointment_type, date_obj)
        
        response = f"⏰ Busiest times for {appointment_type.title()} on {date_str}:\n\n"
        for time_str in busiest:
            response += f"• {time_str}\n"
        
        response += "\nConsider booking earlier or later in the day for shorter waits."
        return response
        
    except ValueError:
        return "Please provide the date in YYYY-MM-DD format (e.g., 2026-01-20)."


@tool
def get_least_busy_times(appointment_type: str, date_str: str):
    """
    Get the least busy appointment times for a given date.
    These times typically have minimal predicted waiting periods.
    
    Args:
        appointment_type: Type of appointment
        date_str: Date in format YYYY-MM-DD
    """
    logger.debug(f"Getting least busy times for {appointment_type} on {date_str}")
    
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Initialize predictor
        init_predictor()
        
        least_busy = predictor.get_least_busy_times(appointment_type, date_obj)
        
        response = f"✨ Best times for {appointment_type.title()} on {date_str}:\n\n"
        for recommendation in least_busy:
            response += f"• {recommendation}\n"
        
        response += "\nThese times are predicted to have minimal waiting periods."
        return response
        
    except ValueError:
        return "Please provide the date in YYYY-MM-DD format (e.g., 2026-01-20)."
