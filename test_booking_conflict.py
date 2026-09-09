import json
import os
from appointments_db import add_appointment


def reset_db():
    os.makedirs('data', exist_ok=True)
    with open('data/appointments.json', 'w') as f:
        json.dump({'appointments': []}, f)


reset_db()
first = {
    'name': 'Alice',
    'patient_id': 'P001',
    'phone': '0712345678',
    'email': 'alice@example.com',
    'type': 'urology',
    'datetime': '2026-09-10T09:00:00',
    'duration_minutes': 30,
    'status': 'confirmed',
}
second = {
    'name': 'Bob',
    'patient_id': 'P002',
    'phone': '0723456789',
    'email': 'bob@example.com',
    'type': 'urology',
    'datetime': '2026-09-10T09:00:00',
    'duration_minutes': 30,
    'status': 'confirmed',
}

add_appointment(first)
try:
    add_appointment(second)
    raise AssertionError('Second booking for the same urology slot should have been rejected')
except ValueError as exc:
    print(f'PASS: {exc}')
finally:
    reset_db()
