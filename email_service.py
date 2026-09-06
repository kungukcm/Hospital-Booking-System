"""Appointment confirmation email dispatch via SMTP.

Configured through environment variables so no code changes are needed per
deployment:
    SMTP_HOST, SMTP_PORT (default 587), SMTP_USERNAME, SMTP_PASSWORD,
    SMTP_FROM_EMAIL (default SMTP_USERNAME), SMTP_USE_TLS (default "true")

If SMTP_HOST/SMTP_USERNAME/SMTP_PASSWORD are not set, sending is skipped
gracefully (booking still succeeds) and the attempt is recorded as "skipped".
"""

import os
import smtplib
from email.message import EmailMessage
from typing import Optional

from logger import setup_logger
from feedback_store import add_email_notification

logger = setup_logger(__name__)


def _smtp_configured() -> bool:
    return bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_USERNAME") and os.getenv("SMTP_PASSWORD"))


def send_appointment_confirmation_email(
    recipient_email: str,
    patient_name: str,
    appointment_id: str,
    appointment_type: str,
    appointment_time_display: str,
) -> bool:
    """Send a confirmation email and record the outcome. Returns True if sent."""
    subject = f"KUTRRH Appointment Confirmation - {appointment_id}"

    if not _smtp_configured():
        logger.warning("SMTP not configured; skipping confirmation email for %s", recipient_email)
        add_email_notification(
            recipient_email=recipient_email,
            subject=subject,
            status="skipped",
            appointment_id=appointment_id,
            error_message="SMTP not configured (SMTP_HOST/SMTP_USERNAME/SMTP_PASSWORD missing)",
        )
        return False

    body = (
        f"Dear {patient_name},\n\n"
        f"Your appointment at KUTRRH has been confirmed.\n\n"
        f"Appointment ID: {appointment_id}\n"
        f"Type: {appointment_type}\n"
        f"Date/Time: {appointment_time_display}\n\n"
        f"Please arrive 15 minutes early with your patient ID.\n\n"
        f"For emergencies, call +254 20 8 000 000.\n\n"
        f"KUTRRH Hospital Appointment System"
    )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = os.getenv("SMTP_FROM_EMAIL", os.getenv("SMTP_USERNAME", ""))
    message["To"] = recipient_email
    message.set_content(body)

    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() != "false"

    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            if use_tls:
                server.starttls()
            server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            server.send_message(message)

        logger.info("Sent appointment confirmation email to %s for %s", recipient_email, appointment_id)
        add_email_notification(
            recipient_email=recipient_email,
            subject=subject,
            status="sent",
            appointment_id=appointment_id,
        )
        return True
    except Exception as e:
        logger.error("Failed to send confirmation email to %s: %s", recipient_email, e)
        add_email_notification(
            recipient_email=recipient_email,
            subject=subject,
            status="failed",
            appointment_id=appointment_id,
            error_message=str(e),
        )
        return False
