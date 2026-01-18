"""
Appointments Database Manager
Handles persistent storage, retrieval, and management of appointments
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

APPOINTMENTS_DB = "data/appointments.json"


def ensure_db_exists():
    """Create database file if it doesn't exist"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(APPOINTMENTS_DB):
        with open(APPOINTMENTS_DB, 'w') as f:
            json.dump({"appointments": []}, f, indent=2)
        logger.info("Created new appointments database")


def add_appointment(appointment: Dict) -> Dict:
    """
    Add appointment to database with validation
    
    Args:
        appointment: Dict with keys: name, type, datetime, duration_minutes, 
                     predicted_wait, confidence, status, notes
    
    Returns:
        Appointment with added id and created_at timestamp
    """
    ensure_db_exists()
    
    # Validate required fields
    required_fields = ['name', 'type', 'datetime']
    for field in required_fields:
        if field not in appointment:
            raise ValueError(f"Missing required field: {field}")
    
    # Load existing appointments
    with open(APPOINTMENTS_DB, 'r') as f:
        data = json.load(f)
    
    # Add metadata
    appointment['id'] = f"APT_{len(data['appointments']) + 1:04d}"
    appointment['created_at'] = datetime.now().isoformat()
    appointment['status'] = appointment.get('status', 'confirmed')
    appointment['duration_minutes'] = appointment.get('duration_minutes', 30)
    
    # Check for conflicts
    conflict = check_conflict(appointment['datetime'], appointment.get('duration_minutes', 30))
    if conflict:
        appointment['conflict_warning'] = f"Overlaps with {conflict['name']}"
    
    # Save
    data['appointments'].append(appointment)
    with open(APPOINTMENTS_DB, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Added appointment: {appointment['id']} for {appointment['name']}")
    return appointment


def get_appointments(
    filter_by_date: Optional[str] = None,
    filter_by_type: Optional[str] = None,
    filter_by_status: Optional[str] = None
) -> List[Dict]:
    """
    Get appointments with optional filtering
    
    Args:
        filter_by_date: Filter by date string (YYYY-MM-DD)
        filter_by_type: Filter by appointment type
        filter_by_status: Filter by status (confirmed, cancelled, pending)
    
    Returns:
        List of appointments matching filters
    """
    ensure_db_exists()
    
    with open(APPOINTMENTS_DB, 'r') as f:
        data = json.load(f)
    
    appointments = data['appointments']
    
    # Apply filters
    if filter_by_status:
        appointments = [a for a in appointments if a.get('status') == filter_by_status]
    
    if filter_by_type:
        appointments = [a for a in appointments if a.get('type', '').lower() == filter_by_type.lower()]
    
    if filter_by_date:
        appointments = [a for a in appointments if a.get('datetime', '').startswith(filter_by_date)]
    
    return sorted(appointments, key=lambda x: x.get('datetime', ''))


def cancel_appointment(appointment_id: str, reason: str = "") -> bool:
    """Cancel an appointment"""
    ensure_db_exists()
    
    with open(APPOINTMENTS_DB, 'r') as f:
        data = json.load(f)
    
    for apt in data['appointments']:
        if apt['id'] == appointment_id:
            apt['status'] = 'cancelled'
            apt['cancelled_at'] = datetime.now().isoformat()
            apt['cancellation_reason'] = reason
            
            with open(APPOINTMENTS_DB, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Cancelled appointment: {appointment_id}")
            return True
    
    logger.warning(f"Appointment not found: {appointment_id}")
    return False


def reschedule_appointment(appointment_id: str, new_datetime: str, reason: str = "") -> Optional[Dict]:
    """Reschedule an appointment to a new time"""
    ensure_db_exists()
    
    with open(APPOINTMENTS_DB, 'r') as f:
        data = json.load(f)
    
    for apt in data['appointments']:
        if apt['id'] == appointment_id and apt.get('status') != 'cancelled':
            # Check for conflicts
            conflict = check_conflict(new_datetime, apt.get('duration_minutes', 30))
            if conflict:
                raise ValueError(f"Conflict with existing appointment: {conflict['id']}")
            
            apt['previous_datetime'] = apt['datetime']
            apt['datetime'] = new_datetime
            apt['rescheduled_at'] = datetime.now().isoformat()
            apt['reschedule_reason'] = reason
            
            with open(APPOINTMENTS_DB, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Rescheduled appointment: {appointment_id} to {new_datetime}")
            return apt
    
    logger.warning(f"Appointment not found: {appointment_id}")
    return None


def check_conflict(datetime_str: str, duration_minutes: int = 30) -> Optional[Dict]:
    """Check if appointment time conflicts with existing appointments"""
    ensure_db_exists()
    
    with open(APPOINTMENTS_DB, 'r') as f:
        data = json.load(f)
    
    try:
        new_time = datetime.fromisoformat(datetime_str)
    except:
        return None
    
    for apt in data['appointments']:
        if apt.get('status') == 'cancelled':
            continue
        
        try:
            existing_time = datetime.fromisoformat(apt['datetime'])
            existing_duration = apt.get('duration_minutes', 30)
            
            # Check if times overlap
            new_end = new_time.timestamp() + (duration_minutes * 60)
            existing_end = existing_time.timestamp() + (existing_duration * 60)
            
            if (new_time.timestamp() < existing_end and new_end > existing_time.timestamp()):
                return apt
        except:
            continue
    
    return None


def get_appointment_stats() -> Dict:
    """Get appointment statistics"""
    ensure_db_exists()
    
    appointments = get_appointments(filter_by_status='confirmed')
    
    stats = {
        'total': len(appointments),
        'by_type': {},
        'average_wait_time': 0,
        'upcoming_count': 0
    }
    
    total_wait = 0
    count = 0
    now = datetime.now()
    
    for apt in appointments:
        # Count by type
        apt_type = apt.get('type', 'Unknown')
        stats['by_type'][apt_type] = stats['by_type'].get(apt_type, 0) + 1
        
        # Average wait time
        if 'predicted_wait' in apt:
            total_wait += apt['predicted_wait']
            count += 1
        
        # Upcoming appointments
        try:
            apt_datetime = datetime.fromisoformat(apt['datetime'])
            if apt_datetime > now:
                stats['upcoming_count'] += 1
        except:
            pass
    
    if count > 0:
        stats['average_wait_time'] = round(total_wait / count, 1)
    
    return stats


def get_next_appointment() -> Optional[Dict]:
    """Get the next scheduled appointment"""
    appointments = get_appointments(filter_by_status='confirmed')
    now = datetime.now()
    
    future_apts = []
    for apt in appointments:
        try:
            apt_datetime = datetime.fromisoformat(apt['datetime'])
            if apt_datetime > now:
                future_apts.append(apt)
        except:
            continue
    
    if future_apts:
        return sorted(future_apts, key=lambda x: x['datetime'])[0]
    
    return None


def delete_all_appointments():
    """Clear all appointments (for testing)"""
    ensure_db_exists()
    with open(APPOINTMENTS_DB, 'w') as f:
        json.dump({"appointments": []}, f, indent=2)
    logger.info("Deleted all appointments")
