"""Persistent feedback and chat audit storage."""

import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "system_management.sqlite3")


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
            """
        )


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


def log_chat(ip_address: str, user_message: str, assistant_response: str) -> None:
    initialize_store()
    with _connection() as connection:
        connection.execute(
            "INSERT INTO chat_logs (ip_address, user_message, assistant_response, created_at) VALUES (?, ?, ?, ?)",
            (ip_address, user_message, assistant_response, _now()),
        )


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
                "SELECT id, ip_address, user_message, assistant_response, created_at FROM chat_logs WHERE ip_address = ? ORDER BY id DESC LIMIT ?",
                (ip_address, max(1, min(limit, 2000))),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT id, ip_address, user_message, assistant_response, created_at FROM chat_logs ORDER BY id DESC LIMIT ?",
                (max(1, min(limit, 2000)),),
            ).fetchall()
        return [dict(row) for row in rows]
