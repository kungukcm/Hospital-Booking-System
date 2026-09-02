"""
Authentication utilities for admin dashboard access
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict
import secrets
import json
import hashlib
from pathlib import Path

ADMIN_USERS_FILE = "data/admin_users.json"
ADMIN_TOKENS_FILE = "data/admin_tokens.json"

# Default admin credentials (CHANGE THESE IN PRODUCTION)
DEFAULT_ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
DEFAULT_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
VALID_ROLES = {"admin", "systems_manager", "scheduler", "support", "analyst", "viewer"}


def ensure_admin_data_exists():
    """Create admin data files if they don't exist"""
    Path("data").mkdir(exist_ok=True)
    
    # Create admin users file with default admin
    if not os.path.exists(ADMIN_USERS_FILE):
        admin_data = {
            "users": [
                {
                    "username": DEFAULT_ADMIN_USERNAME,
                    "password_hash": hash_password(DEFAULT_ADMIN_PASSWORD),
                    "role": "admin",
                    "created_at": datetime.now().isoformat()
                }
            ]
        }
        with open(ADMIN_USERS_FILE, 'w') as f:
            json.dump(admin_data, f, indent=2)
    
    # Create tokens file
    if not os.path.exists(ADMIN_TOKENS_FILE):
        with open(ADMIN_TOKENS_FILE, 'w') as f:
            json.dump({"tokens": []}, f, indent=2)


def hash_password(password: str) -> str:
    """Create a stable password hash for persistence across process restarts."""
    return hashlib.sha256((password + "salt").encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == password_hash


def get_admin_users() -> Dict:
    """Load admin users from file"""
    ensure_admin_data_exists()
    with open(ADMIN_USERS_FILE, 'r') as f:
        return json.load(f)


def authenticate_admin(username: str, password: str) -> Optional[str]:
    """
    Authenticate admin user and return token
    
    Args:
        username: Admin username
        password: Admin password
    
    Returns:
        Auth token if credentials are valid, None otherwise
    """
    users_data = get_admin_users()
    
    for user in users_data.get("users", []):
        if user["username"] == username and verify_password(password, user["password_hash"]):
            # Generate token
            token = secrets.token_urlsafe(32)
            
            # Save token
            save_admin_token(token, username)
            
            return token
    
    return None


def save_admin_token(token: str, username: str):
    """Save authentication token"""
    ensure_admin_data_exists()
    with open(ADMIN_TOKENS_FILE, 'r') as f:
        data = json.load(f)
    
    data["tokens"].append({
        "token": token,
        "username": username,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=7)).isoformat()
    })
    
    with open(ADMIN_TOKENS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def verify_admin_token(token: str) -> Optional[str]:
    """
    Verify admin token and return username if valid
    
    Args:
        token: Admin auth token
    
    Returns:
        Username if token is valid, None otherwise
    """
    ensure_admin_data_exists()
    with open(ADMIN_TOKENS_FILE, 'r') as f:
        data = json.load(f)
    
    for token_data in data.get("tokens", []):
        if token_data["token"] == token:
            # Check if token is expired
            expires_at = datetime.fromisoformat(token_data["expires_at"])
            if datetime.now() < expires_at:
                return token_data["username"]
            break
    
    return None


def create_admin_user(username: str, password: str, role: str = "viewer") -> bool:
    """Create a dashboard user with a defined access level."""
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role. Choose one of: {', '.join(sorted(VALID_ROLES))}")
    users_data = get_admin_users()
    
    # Check if user already exists
    for user in users_data.get("users", []):
        if user["username"] == username:
            return False
    
    # Add new user
    users_data["users"].append({
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "created_at": datetime.now().isoformat()
    })
    
    with open(ADMIN_USERS_FILE, 'w') as f:
        json.dump(users_data, f, indent=2)
    
    return True
