"""Persistent feedback and chat audit storage."""

import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "system_management.sqlite3")

# Responses slower than this are flagged as "unresponsive" for quality tracking.
SLOW_RESPONSE_THRESHOLD_MS = 8000

# Phrases in assistant output that indicate an error/fallback or likely hallucination.
ERROR_RESPONSE_MARKERS = [
    "encountered an error",
    "i'm sorry, i encountered",
    "nimekumbana na hitilafu",
    "❌ error",
]


def _connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_store() -> None:
    with _connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                rating INTEGER,
                message TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL,
                user_message TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS email_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_id TEXT,
                recipient_email TEXT NOT NULL,
                subject TEXT NOT NULL,
                status TEXT NOT NULL,
                error_message TEXT,
                created_at TEXT NOT NULL
            );
            """
        )
        # Migrate older chat_logs tables (created before quality tracking existed).
        existing_columns = {row["name"] for row in connection.execute("PRAGMA table_info(chat_logs)")}
        for column, ddl in (
            ("response_time_ms", "ALTER TABLE chat_logs ADD COLUMN response_time_ms REAL"),
            ("flagged", "ALTER TABLE chat_logs ADD COLUMN flagged INTEGER NOT NULL DEFAULT 0"),
            ("flag_reason", "ALTER TABLE chat_logs ADD COLUMN flag_reason TEXT"),
        ):
            if column not in existing_columns:
                connection.execute(ddl)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def add_feedback(email: str, message: str, ip_address: str, rating: Optional[int] = None) -> Dict[str, Any]:
    initialize_store()
    with _connection() as connection:
        cursor = connection.execute(
            "INSERT INTO feedback (email, rating, message, ip_address, created_at) VALUES (?, ?, ?, ?, ?)",
            (email.strip(), rating, message.strip(), ip_address, _now()),
        )
        return {"id": cursor.lastrowid, "message": "Feedback submitted successfully"}


def classify_chat_quality(assistant_response: str, response_time_ms: Optional[float]) -> Optional[str]:
    """Return a flag reason if the response looks unresponsive/erroneous, else None."""
    reasons = []
    text = (assistant_response or "").strip().lower()

    if not text:
        reasons.append("empty_response")
    elif any(marker in text for marker in ERROR_RESPONSE_MARKERS):
        reasons.append("error_or_fallback_response")

    if response_time_ms is not None and response_time_ms >= SLOW_RESPONSE_THRESHOLD_MS:
        reasons.append("slow_response")

    return ",".join(reasons) if reasons else None


def log_chat(
    ip_address: str,
    user_message: str,
    assistant_response: str,
    response_time_ms: Optional[float] = None,
    flag_reason: Optional[str] = None,
) -> None:
    initialize_store()
    if flag_reason is None:
        flag_reason = classify_chat_quality(assistant_response, response_time_ms)
    flagged = 1 if flag_reason else 0
    with _connection() as connection:
        connection.execute(
            """INSERT INTO chat_logs
               (ip_address, user_message, assistant_response, created_at, response_time_ms, flagged, flag_reason)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (ip_address, user_message, assistant_response, _now(), response_time_ms, flagged, flag_reason),
        )


def add_email_notification(
    recipient_email: str,
    subject: str,
    status: str,
    appointment_id: Optional[str] = None,
    error_message: Optional[str] = None,
) -> Dict[str, Any]:
    initialize_store()
    with _connection() as connection:
        cursor = connection.execute(
            """INSERT INTO email_notifications
               (appointment_id, recipient_email, subject, status, error_message, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (appointment_id, recipient_email, subject, status, error_message, _now()),
        )
        return {"id": cursor.lastrowid}


def list_email_notifications(limit: int = 200) -> List[Dict[str, Any]]:
    initialize_store()
    with _connection() as connection:
        rows = connection.execute(
            """SELECT id, appointment_id, recipient_email, subject, status, error_message, created_at
               FROM email_notifications ORDER BY id DESC LIMIT ?""",
            (max(1, min(limit, 1000)),),
        ).fetchall()
        return [dict(row) for row in rows]


def get_chat_quality_stats() -> Dict[str, Any]:
    """Aggregate metrics for the admin dashboard: responsiveness and flagged/hallucination rate."""
    initialize_store()
    with _connection() as connection:
        total = connection.execute("SELECT COUNT(*) AS c FROM chat_logs").fetchone()["c"]
        flagged = connection.execute("SELECT COUNT(*) AS c FROM chat_logs WHERE flagged = 1").fetchone()["c"]
        avg_ms_row = connection.execute(
            "SELECT AVG(response_time_ms) AS avg_ms FROM chat_logs WHERE response_time_ms IS NOT NULL"
        ).fetchone()
        slow = connection.execute(
            "SELECT COUNT(*) AS c FROM chat_logs WHERE response_time_ms >= ?",
            (SLOW_RESPONSE_THRESHOLD_MS,),
        ).fetchone()["c"]
        recent_flagged = connection.execute(
            """SELECT id, ip_address, user_message, assistant_response, created_at, response_time_ms, flag_reason
               FROM chat_logs WHERE flagged = 1 ORDER BY id DESC LIMIT 20"""
        ).fetchall()

        return {
            "total_chats": total,
            "flagged_count": flagged,
            "flagged_rate_pct": round((flagged / total) * 100, 1) if total else 0.0,
            "avg_response_time_ms": round(avg_ms_row["avg_ms"], 0) if avg_ms_row["avg_ms"] is not None else None,
            "slow_response_count": slow,
            "recent_flagged": [dict(row) for row in recent_flagged],
        }


def list_feedback(limit: int = 200) -> List[Dict[str, Any]]:
    initialize_store()
    with _connection() as connection:
        rows = connection.execute(
            "SELECT id, email, rating, message, ip_address, created_at FROM feedback ORDER BY id DESC LIMIT ?",
            (max(1, min(limit, 1000)),),
        ).fetchall()
        return [dict(row) for row in rows]


def list_chat_logs(limit: int = 500, ip_address: Optional[str] = None) -> List[Dict[str, Any]]:
    initialize_store()
    with _connection() as connection:
        if ip_address:
            rows = connection.execute(
                """SELECT id, ip_address, user_message, assistant_response, created_at,
                          response_time_ms, flagged, flag_reason
                   FROM chat_logs WHERE ip_address = ? ORDER BY id DESC LIMIT ?""",
                (ip_address, max(1, min(limit, 2000))),
            ).fetchall()
        else:
            rows = connection.execute(
                """SELECT id, ip_address, user_message, assistant_response, created_at,
                          response_time_ms, flagged, flag_reason
                   FROM chat_logs ORDER BY id DESC LIMIT ?""",
                (max(1, min(limit, 2000)),),
            ).fetchall()
        return [dict(row) for row in rows]
