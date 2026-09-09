import json
import os

from appointments_db import add_appointment, cancel_appointment, get_appointments


def reset_db():
    os.makedirs('data', exist_ok=True)
    with open('data/appointments.json', 'w') as f:
        json.dump({'appointments': []}, f)


def test_cancel_appointment_by_patient_id_requires_confirmation():
    reset_db()
    add_appointment({
        'name': 'Jane Doe',
        'patient_id': 'P-1001',
        'phone': '0712345678',
        'email': 'jane@example.com',
        'type': 'urology',
        'datetime': '2026-09-10T09:00:00',
        'duration_minutes': 30,
        'status': 'confirmed',
    })

    blocked = cancel_appointment('P-1001', reason='Patient request', confirm_cancel=False)
    assert blocked is False
    assert len(get_appointments(filter_by_status='cancelled')) == 0

    cancelled = cancel_appointment('P-1001', reason='Patient request', confirm_cancel=True)
    assert cancelled is True
    appointments = get_appointments(filter_by_status='cancelled')
    assert len(appointments) == 1
    assert appointments[0]['patient_id'] == 'P-1001'
    reset_db()
