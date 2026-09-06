"""
FastAPI Backend for Hospital Appointment System
Handles chat, appointments, and admin operations
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import os
import shutil

# Import core business logic
from agent import receive_message_from_caller
from langchain_core.messages import HumanMessage, AIMessage
from config import AppConfig
from appointments_db import add_appointment, get_appointments, get_appointment
from appointment_recommender import get_recommender
from email_service import send_appointment_confirmation_email
from hospital_setup import setup_hospital_knowledge_base
from auth import authenticate_admin, verify_admin_token, create_admin_user, get_admin_users, VALID_ROLES
from logger import setup_logger
from feedback_store import (
    add_feedback,
    initialize_store,
    list_chat_logs,
    list_feedback,
    log_chat,
    get_chat_quality_stats,
    get_feedback_stats,
    list_email_notifications,
)
import time

logger = setup_logger(__name__)
config = AppConfig()

app = FastAPI(title="KUTRRH Hospital Appointment System API", version="1.0.0")
initialize_store()

# Enable CORS for frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Request/Response Models
# ============================================================================

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    response: str
    conversation_history: List[ChatMessage]


class FeedbackRequest(BaseModel):
    email: str
    message: str
    rating: Optional[int] = None
    functions_used: Optional[str] = None
    booking_success: Optional[str] = None
    information_accuracy: Optional[str] = None
    knowledge_base_honesty: Optional[str] = None
    queue_recommendations: Optional[str] = None
    language_consistency: Optional[str] = None
    misread_request: Optional[str] = None
    personal_details_concern: Optional[str] = None
    natural_effort: Optional[int] = None
    confidence_change: Optional[str] = None
    additional_feedback: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    message: str


class AppointmentRequest(BaseModel):
    name: str
    patient_id: str
    phone: str
    email: str
    type: str  # consultation, checkup, follow-up
    datetime: str
    status: str = "confirmed"


class AppointmentResponse(BaseModel):
    id: str
    name: str
    patient_id: str
    type: str
    datetime: str
    predicted_wait_minutes: Optional[float] = None
    status: str


class RecommendedSlot(BaseModel):
    time: str
    congestion_level: str
    predicted_wait_minutes: float


class SlotsRecommendationResponse(BaseModel):
    date: str
    appointment_type: str
    slots: List[RecommendedSlot]
    analytics: Dict[str, Any]


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    token: str
    message: str


class AdminResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Hospital Appointment System API"
    }


# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(request: AdminLoginRequest):
    """Authenticate admin user and return token"""
    token = authenticate_admin(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    logger.info(f"Admin login successful for user: {request.username}")
    return AdminLoginResponse(
        token=token,
        message=f"Welcome {request.username}!"
    )


def verify_admin_auth(authorization: Optional[str] = Header(None)) -> str:
    """Verify admin authentication token from header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token from "Bearer <token>" format
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    username = verify_admin_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return username


# ============================================================================
# Chat Endpoints (Public)
# ============================================================================

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request):
    """
    Chat with AI assistant
    
    Args:
        message: User message
        conversation_history: Optional previous conversation for context
    
    Returns:
        AI response and full conversation history
    """
    start_time = time.monotonic()
    try:
        # Convert conversation history to langchain messages
        conversation = []
        if request.conversation_history:
            for msg in request.conversation_history:
                if msg.role == "user":
                    conversation.append(HumanMessage(content=msg.content))
                else:
                    conversation.append(AIMessage(content=msg.content))
        
        # Process message through agent
        receive_message_from_caller(request.message, conversation)
        
        # Convert back to response format
        chat_history = []
        for msg in conversation:
            if isinstance(msg, HumanMessage):
                chat_history.append(ChatMessage(role="user", content=msg.content))
            else:
                chat_history.append(ChatMessage(role="assistant", content=msg.content))
        
        # Get last assistant message as response
        response_text = ""
        for msg in reversed(conversation):
            if isinstance(msg, AIMessage):
                response_text = msg.content
                break

        response_time_ms = (time.monotonic() - start_time) * 1000
        client_ip = http_request.client.host if http_request.client else "unknown"
        log_chat(client_ip, request.message, response_text, response_time_ms=response_time_ms)
        
        logger.info(f"Chat processed successfully. Conversation length: {len(conversation)}")
        return ChatResponse(
            response=response_text,
            conversation_history=chat_history
        )
    
    except Exception as e:
        response_time_ms = (time.monotonic() - start_time) * 1000
        client_ip = http_request.client.host if http_request.client else "unknown"
        log_chat(client_ip, request.message, "", response_time_ms=response_time_ms, flag_reason="exception")
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")


@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest, http_request: Request):
    """Store public application feedback; email and message are mandatory."""
    email = request.email.strip()
    message = request.message.strip()
    if not email or "@" not in email:
        raise HTTPException(status_code=422, detail="A valid email address is required")
    if not message:
        raise HTTPException(status_code=422, detail="Feedback message is required")
    if request.rating is not None and not 1 <= request.rating <= 5:
        raise HTTPException(status_code=422, detail="Rating must be between 1 and 5")

    client_ip = http_request.client.host if http_request.client else "unknown"
    structured = {
        "functions_used": request.functions_used,
        "booking_success": request.booking_success,
        "information_accuracy": request.information_accuracy,
        "knowledge_base_honesty": request.knowledge_base_honesty,
        "queue_recommendations": request.queue_recommendations,
        "language_consistency": request.language_consistency,
        "misread_request": request.misread_request,
        "personal_details_concern": request.personal_details_concern,
        "natural_effort": request.natural_effort,
        "confidence_change": request.confidence_change,
        "additional_feedback": request.additional_feedback,
    }
    return add_feedback(email, message, client_ip, request.rating, structured=structured)


# ============================================================================
# Appointment Endpoints (Public)
# ============================================================================

@app.get("/appointments", response_model=List[AppointmentResponse])
async def list_appointments(status: Optional[str] = "confirmed", limit: int = 10):
    """Get list of appointments"""
    try:
        appointments = get_appointments(filter_by_status=status, limit=limit)
        return [AppointmentResponse(**apt) for apt in appointments]
    except Exception as e:
        logger.error(f"Error listing appointments: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def get_single_appointment(appointment_id: str):
    """Get specific appointment details"""
    try:
        apt = get_appointment(appointment_id)
        if not apt:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return AppointmentResponse(**apt)
    except Exception as e:
        logger.error(f"Error getting appointment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/appointments", response_model=AppointmentResponse)
async def create_appointment(request: AppointmentRequest):
    """Create new appointment"""
    try:
        appointment_data = request.model_dump()
        result = add_appointment(appointment_data)

        try:
            appointment_dt = datetime.fromisoformat(result["datetime"])
            time_display = appointment_dt.strftime("%B %d, %Y at %I:%M %p")
        except ValueError:
            time_display = result["datetime"]

        send_appointment_confirmation_email(
            recipient_email=result["email"],
            patient_name=result["name"],
            appointment_id=result["id"],
            appointment_type=result["type"],
            appointment_time_display=time_display,
        )

        logger.info(f"Appointment created: {result['id']}")
        return AppointmentResponse(**result)
    except Exception as e:
        logger.error(f"Error creating appointment: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/recommendations/slots")
async def get_recommended_slots(
    appointment_type: str,
    date: str,
    num_recommendations: int = 5
) -> SlotsRecommendationResponse:
    """
    Get recommended appointment time slots for a given date and type
    
    Args:
        appointment_type: Type of appointment (consultation, checkup, follow-up)
        date: Date in YYYY-MM-DD format
        num_recommendations: Number of slots to recommend
    
    Returns:
        List of recommended time slots with analytics
    """
    try:
        import datetime as dt
        date_obj = dt.datetime.strptime(date, "%Y-%m-%d")
        
        recommender = get_recommender()
        slots, analytics = recommender.recommend_optimal_slots(
            appointment_type, date_obj, num_recommendations=num_recommendations
        )
        
        return SlotsRecommendationResponse(
            date=date,
            appointment_type=appointment_type,
            slots=[RecommendedSlot(**slot) for slot in slots],
            analytics=analytics
        )
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Admin Endpoints (Protected)
# ============================================================================

@app.post("/admin/rebuild-kb", response_model=AdminResponse)
async def rebuild_knowledge_base(admin_user: str = Depends(verify_admin_auth)):
    """
    Rebuild hospital knowledge base from PDFs and website
    Only accessible to authenticated admins
    """
    try:
        logger.info(f"Admin {admin_user} triggered KB rebuild")
        
        # Remove existing vector store
        if os.path.exists("hospital_vector_store"):
            shutil.rmtree("hospital_vector_store")
        
        # Rebuild from scratch
        result = setup_hospital_knowledge_base()
        
        if result:
            logger.info("Knowledge base rebuilt successfully")
            return AdminResponse(
                success=True,
                message="Hospital knowledge base rebuilt successfully",
                data={"rebuild_time": datetime.now().isoformat()}
            )
        else:
            logger.warning("Knowledge base rebuild completed with warnings")
            return AdminResponse(
                success=True,
                message="Knowledge base rebuild completed with warnings. Some sources may be missing.",
                data={"rebuild_time": datetime.now().isoformat()}
            )
    except Exception as e:
        logger.error(f"Knowledge base rebuild failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Rebuild failed: {str(e)}")


@app.get("/admin/appointments", response_model=Dict[str, Any])
async def admin_get_all_appointments(admin_user: str = Depends(verify_admin_auth)):
    """
    Get analytics and summary of all appointments
    Only accessible to authenticated admins
    """
    try:
        logger.info(f"Admin {admin_user} accessed appointments analytics")
        
        appointments = get_appointments(limit=None)
        
        # Calculate analytics
        total = len(appointments)
        confirmed = len([a for a in appointments if a.get('status') == 'confirmed'])
        pending = len([a for a in appointments if a.get('status') == 'pending'])
        
        by_type = {}
        for apt in appointments:
            apt_type = apt.get('type', 'unknown')
            by_type[apt_type] = by_type.get(apt_type, 0) + 1
        
        return {
            "total_appointments": total,
            "confirmed": confirmed,
            "pending": pending,
            "by_type": by_type,
            "appointments": appointments[:100],  # Return last 100 for performance
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting admin appointments: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/admin/system-status", response_model=Dict[str, Any])
async def admin_system_status(admin_user: str = Depends(verify_admin_auth)):
    """
    Get system status and health information
    Only accessible to authenticated admins
    """
    try:
        logger.info(f"Admin {admin_user} checked system status")
        
        # Check if knowledge base exists
        kb_exists = os.path.exists("hospital_vector_store")
        
        # Check database
        db_exists = os.path.exists("data/appointments.json")
        
        return {
            "status": "operational",
            "knowledge_base": {
                "initialized": kb_exists,
                "path": "hospital_vector_store"
            },
            "database": {
                "initialized": db_exists,
                "path": "data/appointments.json"
            },
            "api": {
                "version": "1.0.0",
                "status": "running"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/admin/feedback", response_model=List[Dict[str, Any]])
async def admin_get_feedback(admin_user: str = Depends(verify_admin_auth)):
    """Return submitted feedback for authenticated systems managers."""
    return list_feedback()


@app.get("/admin/feedback-stats", response_model=Dict[str, Any])
async def admin_get_feedback_stats(admin_user: str = Depends(verify_admin_auth)):
    """Return per-question multiple-choice counts (Yes/Partly/No, etc.) for dashboard charts."""
    return get_feedback_stats()


@app.get("/admin/chat-logs", response_model=List[Dict[str, Any]])
async def admin_get_chat_logs(
    ip_address: Optional[str] = None,
    admin_user: str = Depends(verify_admin_auth),
):
    """Return the chat audit log, optionally filtered by client IP."""
    return list_chat_logs(ip_address=ip_address)


@app.get("/admin/chat-quality", response_model=Dict[str, Any])
async def admin_get_chat_quality(admin_user: str = Depends(verify_admin_auth)):
    """Return chat responsiveness/hallucination metrics for the admin dashboard."""
    return get_chat_quality_stats()


@app.get("/admin/email-notifications", response_model=List[Dict[str, Any]])
async def admin_get_email_notifications(admin_user: str = Depends(verify_admin_auth)):
    """Return the log of appointment confirmation emails sent to patients."""
    return list_email_notifications()


@app.post("/admin/create-user", response_model=AdminResponse)
async def admin_create_user(
    username: str,
    password: str,
    role: str = "viewer",
    admin_user: str = Depends(verify_admin_auth)
):
    """
    Create new admin user
    Only accessible to authenticated admins
    """
    try:
        if create_admin_user(username, password, role):
            logger.info(f"Admin {admin_user} created new admin user: {username}")
            return AdminResponse(
                success=True,
                message=f"Admin user '{username}' created successfully"
            )
        else:
            raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/admin/users", response_model=List[Dict[str, Any]])
async def admin_get_users(admin_user: str = Depends(verify_admin_auth)):
    """Return dashboard users and access levels without exposing password hashes."""
    return [
        {key: user.get(key) for key in ("username", "role", "created_at")}
        for user in get_admin_users().get("users", [])
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
