from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from typing import List, Dict, Any, TypedDict, Tuple
import datetime
import re
import unicodedata
from config import AppConfig
from constants import GROQ_API_KEY
from logger import setup_logger
from enhanced_tools import (
    book_appointment,
    get_next_available_appointment,
    get_optimal_appointment_slots,
    suggest_alternative_slots,
    get_wait_time_prediction,
    get_busiest_times,
    get_least_busy_times,
    cancel_appointment,
    view_all_appointments
)
from hospital_tools import search_hospital_information

logger = setup_logger(__name__)

load_dotenv()

config = AppConfig()

llm = ChatGroq(model=config.LLM_MODEL, api_key=GROQ_API_KEY)
logger.info(f"LLM initialized with model: {llm}")

# Define tools list early for LLM binding
# NOTE: Hospital tool is NOT included in llm tool binding due to Groq compatibility issues
# Instead, we handle hospital queries through intent detection below
caller_tools = [
    book_appointment,
    get_next_available_appointment,
    get_optimal_appointment_slots,
    get_wait_time_prediction,
    get_busiest_times,
    get_least_busy_times,
    cancel_appointment
]

# Bind tools to LLM (excluding hospital tool)
llm_with_tools = llm.bind_tools(caller_tools)
logger.info(f"LLM bound with {len(caller_tools)} tools (hospital tool handled separately)")

class AgentState(TypedDict):
    messages: List[Any]
    current_time: str

def receive_message_from_caller(message: str, conversation: List[Any]) -> None:
    logger.info(f"Received message: {message}")
    conversation.append(HumanMessage(content=message))
    state: AgentState = {
        "messages": conversation,
        "current_time": config.get_current_time()
    }
    logger.debug(f"State before invoke: {state}")
    try:
        new_state = caller_app.invoke(state)
        logger.debug(f"New state after invoke: {new_state}")
        conversation.extend(new_state["messages"][len(conversation):])
    except Exception as e:
        logger.exception(f"Error in receive_message_from_caller: {str(e)}")
        raise

def should_continue_caller(state: AgentState) -> str:
    logger.debug(f"Entering should_continue_caller with state: {state}")
    messages = state["messages"]
    if not messages:
        logger.warning("No messages in state")
        return "end"
    last_message = messages[-1]
    logger.debug(f"Last message type: {type(last_message)}, content: {last_message.content if hasattr(last_message, 'content') else 'N/A'}")
    
    # Check if message has tool_calls (indicates tools should be invoked)
    if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        logger.info(f"Tool calls detected: {last_message.tool_calls}, continuing to action node")
        return "continue"
    # If message only has content (no tool calls), end the conversation
    elif isinstance(last_message, AIMessage) and last_message.content.strip() and not isinstance(last_message, ToolMessage):
        logger.info("AI message with content (no tool calls), ending conversation")
        return "end"
    # If last message is a ToolMessage, we need to go back to agent for synthesis
    elif hasattr(last_message, 'name') and last_message.name:  # ToolMessage has 'name' attribute
        logger.info("Tool message detected, returning to agent for synthesis")
        return "continue"
    else:
        logger.info("Other message type, continuing conversation")
        return "continue"

def is_greeting_or_social_message(message_content: str) -> bool:
    """Handle generic greetings or social chat without hitting the external LLM."""
    text = normalize_text(message_content)

    # Structured patient-detail submissions (name, ID, phone, email, comma-separated
    # fields, etc.) must never be misread as a greeting even if a name/word happens
    # to contain a short marker like "hi" (e.g. "Chirchir", "This", "White").
    looks_like_patient_details = (
        "@" in text
        or text.count(",") >= 2
        or bool(re.search(r"\d{6,}", text))
    )
    if looks_like_patient_details:
        return False

    greeting_markers = [
        'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
        'habari', 'mambo', 'jambo', 'salaam', 'hujambo',
        'how are you', 'howdy', 'greetings'
    ]
    return any(re.search(rf"\b{re.escape(marker)}\b", text) for marker in greeting_markers)


def is_hospital_query(message_content: str) -> bool:
    """Detect if a query is about hospital information (not appointments)"""
    hospital_keywords = [
        'hospital', 'service', 'department', 'contact', 'phone', 'address', 'location',
        'visiting hours', 'hours', 'insurance', 'payment', 'facility', 'staff', 'doctor',
        'nurse', 'clinic', 'kutrrh', 'kenyatta', 'teaching', 'referral', 'research',
        'what can i get', 'available treatment', 'medical', 'healthcare', 'specialist',
        'tariff', 'cost', 'charge', 'bill', 'price', 'fee', 'payment method', 'pay',
        'ceo', 'chief executive', 'director', 'management', 'leadership', 'executive',
        'who is', 'who runs', 'head of', 'administrator', 'matibabu', 'lipia', 'malipo',
        'kulipa', 'mpesa', 'paybill', 'kadi ya mkopo', 'gharama', 'gharamu', 'kadi',
        'deposit', 'insurance', 'hospitali', 'anwani', 'barua pepe', 'posta'
    ]
    
    message_lower = message_content.lower()
    
    # Check if message contains hospital keywords
    has_hospital_keyword = any(keyword in message_lower for keyword in hospital_keywords)
    
    # Check if it's NOT asking about appointment booking
    appointment_keywords = ['book', 'schedule', 'appointment', 'available slot', 'when', 'time']
    has_appointment_keyword = any(keyword in message_lower for keyword in appointment_keywords)
    
    # It's a hospital query if it has hospital keywords and is not purely about appointments
    is_hospital = has_hospital_keyword and not (has_appointment_keyword and 'appointment' in message_lower)
    
    logger.debug(f"Hospital query detection: has_hospital={has_hospital_keyword}, has_appointment={has_appointment_keyword}, result={is_hospital}")
    
    return is_hospital

def is_booking_flow_active(messages: List[Any]) -> bool:
    """Detect if the conversation is currently in appointment-booking flow.
    Only activate if the CURRENT user message or recent assistant context indicates booking."""
    
    # First check: does the LAST USER message contain booking intent?
    last_user_message = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            last_user_message = msg
            break
    
    if not last_user_message:
        return False
    
    text_lower = getattr(last_user_message, 'content', '').lower()
    
    # Strong booking indicators - if current message has these, we're in booking flow
    booking_intent_keywords = [
        'book appointment', 'book an appointment', 'booking an appointment',
        'book a', 'schedule appointment', 'make appointment',
        'panga miadi', 'kupanga miadi', 'naomba miadi', 'nataka miadi'
    ]
    
    if any(keyword in text_lower for keyword in booking_intent_keywords):
        return True
    
    # Check if we're already in the middle of collecting booking details
    # Look at recent assistant messages to see if we asked for details
    recent = messages[-10:] if len(messages) > 10 else messages
    collecting_details = False
    
    for msg in recent:
        if isinstance(msg, AIMessage):
            content_lower = getattr(msg, 'content', '').lower()
            if is_greeting_or_social_message(content_lower):
                continue
            # More flexible detection - check for booking-related keywords or structure
            if any(phrase in content_lower for phrase in [
                'patient details', 'full name', 'patient id', 'phone number', 'email',
                'appointment type', 'preferred date', 'choose one of these slots',
                'taarifa za mgonjwa', 'jina kamili', 'namba ya mgonjwa', 'namba ya simu',
                'ready to help', 'set up an appointment', 'appointment at kutrrh',
                'booking', 'book', 'miadi', 'panga', 'unakabilicha', 'huduma',
                'to continue', 'kuendelea'
            ]):
                collecting_details = True
                break
    
    # Only continue booking flow if we're actively collecting details AND user isn't asking a different question
    if collecting_details:
        # But if the current message is a hospital query, don't stay in booking flow
        if not is_hospital_query(text_lower):
            return True
    
    return False

def normalize_text(text: str) -> str:
    """Normalize text for reliable intent matching (handles accented characters)."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return ascii_text.lower().strip()

def detect_appointment_type(text: str) -> str:
    """Extract appointment/service type from user text."""
    normalized = normalize_text(text)

    # Ignore generic booking phrases that are not actual clinical services.
    generic_booking_phrases = [
        "naomba kupanga miadi", "panga miadi", "naomba miadi", "miadi",
        "book appointment", "book an appointment", "appointment",
        "schedule appointment", "need appointment", "nataka miadi"
    ]
    if any(phrase in normalized for phrase in generic_booking_phrases):
        # Continue below only if a known service keyword is also present.
        pass
    service_aliases = {
        "urology": "Urology",
        "urologia": "Urology",
        "cardiology": "Cardiology",
        "kadiolojia": "Cardiology",
        "dentistry": "Dentistry",
        "dentist": "Dentistry",
        "meno": "Dentistry",
        "general checkup": "General Check-up",
        "general check-up": "General Check-up",
        "checkup": "General Check-up",
        "check-up": "General Check-up",
        "uchunguzi wa kawaida": "General Check-up",
        "consultation": "Consultation",
        "ushauri": "Consultation",
        "follow up": "Follow-up",
        "follow-up": "Follow-up",
        "ufuatiliaji": "Follow-up",
        "specialist": "Specialist",
        "specialist appointment": "Specialist",
        "daktari bingwa": "Specialist",
        "orthopedic": "Orthopedic",
        "mifupa": "Orthopedic",
        "oncology": "Oncology",
        "ent": "ENT",
        "pediatrics": "Pediatrics",
        "watoto": "Pediatrics",
        "nephrology": "Nephrology",
    }

    for alias, canonical in service_aliases.items():
        if re.search(rf"\b{re.escape(alias)}\b", normalized):
            return canonical

    # If the message is only a generic booking phrase, do not treat it as a service.
    if any(phrase == normalized for phrase in generic_booking_phrases):
        return ""

    # If user enters a short service-only phrase, use it as provided.
    generic_tokens = {
        "naomba", "panga", "miadi", "book", "appointment", "schedule",
        "nataka", "need", "service", "huduma", "please"
    }
    tokens = [t for t in re.split(r"\s+", normalized) if t]
    if (
        len(tokens) <= 3
        and re.fullmatch(r"[a-z\s-]+", normalized)
        and any(t not in generic_tokens for t in tokens)
    ):
        return text.strip().title()

    return ""

def extract_recent_appointment_type(messages: List[Any]) -> str:
    """Find the most recent appointment type mentioned by the user."""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            appointment_type = detect_appointment_type(getattr(msg, "content", ""))
            if appointment_type:
                return appointment_type
    return ""

def extract_recent_preferred_date(messages: List[Any], current_time: str) -> str:
    """Find the most recent preferred date from user/tool messages."""
    for msg in reversed(messages):
        content = getattr(msg, "content", "")
        if not content:
            continue

        parsed = parse_preferred_date(content, current_time)
        if parsed:
            return parsed

        # Parse date shown in slot tool output: 📅 **YYYY-MM-DD**
        m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", content)
        if m:
            return m.group(1)

    return ""

def extract_patient_details(messages: List[Any]) -> Dict[str, str]:
    """Extract patient details collected in chat messages."""
    details = {
        "person_name": "",
        "patient_id": "",
        "phone_number": "",
        "email_address": "",
    }

    email_re = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    phone_re = re.compile(r"\b(?:\+?\d[\d\s-]{7,}\d)\b")
    id_re = re.compile(r"\b\d{6,}\b")

    for msg in messages:
        if not isinstance(msg, HumanMessage):
            continue
        text = (msg.content or "").strip()
        if not text:
            continue

        # Common single-line format: Name, ID, Phone, Email
        parts = [p.strip() for p in text.split(",")]
        if len(parts) >= 4 and not details["person_name"]:
            maybe_email = email_re.search(parts[3])
            maybe_id = id_re.search(parts[1])
            maybe_phone = phone_re.search(parts[2])
            if maybe_email and maybe_id and maybe_phone:
                details["person_name"] = parts[0]
                details["patient_id"] = maybe_id.group(0)
                details["phone_number"] = maybe_phone.group(0).replace(" ", "").replace("-", "")
                details["email_address"] = maybe_email.group(0)

        if not details["email_address"]:
            maybe_email = email_re.search(text)
            if maybe_email:
                details["email_address"] = maybe_email.group(0)

        if not details["phone_number"]:
            maybe_phone = phone_re.search(text)
            if maybe_phone:
                details["phone_number"] = maybe_phone.group(0).replace(" ", "").replace("-", "")

        if not details["patient_id"]:
            maybe_id = id_re.search(text)
            if maybe_id:
                details["patient_id"] = maybe_id.group(0)

    # If name not captured from CSV format, use a simple heuristic from first user message with letters.
    if not details["person_name"]:
        for msg in messages:
            if not isinstance(msg, HumanMessage):
                continue
            text = (msg.content or "").strip()
            if re.search(r"[A-Za-z]", text) and "," in text:
                candidate = text.split(",")[0].strip()
                if len(candidate.split()) >= 2:
                    details["person_name"] = candidate
                    break

    return details

def parse_selected_time(text: str) -> Tuple[int, int]:
    """Parse selected time and return (hour, minute) in 24h format."""
    value = (text or "").strip().lower()

    m = re.search(r"\b(\d{1,2}):(\d{2})\s*([ap]m)?\b", value)
    if m:
        hour = int(m.group(1))
        minute = int(m.group(2))
        suffix = m.group(3)
        if minute > 59:
            return (-1, -1)
        if suffix:
            if hour == 12:
                hour = 0
            if suffix == "pm":
                hour += 12
        if 0 <= hour <= 23:
            return (hour, minute)

    m2 = re.search(r"\b(\d{1,2})\s*([ap]m)\b", value)
    if m2:
        hour = int(m2.group(1))
        suffix = m2.group(2)
        if hour == 12:
            hour = 0
        if suffix == "pm":
            hour += 12
        if 0 <= hour <= 23:
            return (hour, 0)

    return (-1, -1)

def is_message_in_swahili(message_content: str) -> bool:
    """Check if a single message is in Swahili based on markers."""
    swahili_markers = [
        "habari", "naomba", "tafadhali", "miadi", "leo", "kesho", "asubuhi",
        "mchana", "jioni", "hospitali", "huduma", "nina", "nataka", "saa",
        "tarehe", "urologia", "kliniki", "asante", "nani", "nambari",
        "mambo", "jambo", "hujambo", "shikamoo", "salama", "salaam"
    ]
    
    text = normalize_text(message_content)
    swahili_count = sum(1 for marker in swahili_markers if marker in text)
    return swahili_count >= 1

def is_swahili_context(messages: List[Any], preserve_in_booking: bool = False) -> bool:
    """Detect whether the conversation is in Swahili.
    
    If preserve_in_booking is True and we're in a booking flow, maintain the language 
    from when booking started rather than re-detecting from current message.
    """
    swahili_markers = [
        "habari", "naomba", "tafadhali", "miadi", "leo", "kesho", "asubuhi",
        "mchana", "jioni", "hospitali", "huduma", "nina", "nataka", "saa",
        "tarehe", "urologia", "kliniki", "asante", "nani", "nambari",
        "mambo", "jambo", "hujambo", "shikamoo", "salama", "salaam"
    ]
    
    # Only check the LAST user message, not the entire conversation history
    last_user_message = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            last_user_message = msg
            break
    
    if not last_user_message:
        return False
    
    text = normalize_text(getattr(last_user_message, "content", ""))
    # Count how many Swahili markers appear in THIS message
    swahili_count = sum(1 for marker in swahili_markers if marker in text)
    
    # If current message has clear Swahili markers, use that
    if swahili_count >= 1:
        return True
    
    # If preserve_in_booking is True and current message doesn't have markers,
    # look back for booking-related assistant messages to detect the booking language
    if preserve_in_booking:
        # Look back through recent messages to find the booking language
        # Check last 10 messages for assistant prompts about booking details
        for msg in messages[-10:] if len(messages) > 10 else messages:
            if isinstance(msg, AIMessage):
                content = getattr(msg, "content", "")
                # Check if this is a booking-related prompt
                if any(phrase in content.lower() for phrase in [
                    'patient details', 'full name', 'patient id', 'phone number', 'email',
                    'appointment type', 'preferred date', 'choose one of these slots',
                    'taarifa za mgonjwa', 'jina kamili', 'namba ya mgonjwa', 'namba ya simu',
                    'tafadhali', 'miadi'
                ]):
                    # Found a booking-related message, check if it's in Swahili
                    if is_message_in_swahili(content):
                        return True
    
    return False

def localized_text(english: str, swahili: str, use_swahili: bool) -> str:
    return swahili if use_swahili else english

def localize_appointment_type_value_to_swahili(value: str) -> str:
    """Translate canonical appointment type value to Swahili."""
    if not value:
        return value

    mapping = {
        "Urology": "Urologia",
        "Cardiology": "Kadiolojia",
        "Dentistry": "Udaktari wa Meno",
        "General Check-up": "Uchunguzi wa Kawaida",
        "Consultation": "Ushauri",
        "Follow-up": "Ufuatiliaji",
        "Specialist": "Daktari Bingwa",
        "Orthopedic": "Mifupa",
        "Oncology": "Onkolojia",
        "ENT": "Sikio, Pua na Koo",
        "Pediatrics": "Watoto",
        "Nephrology": "Nefrologia",
    }

    for english, swahili in mapping.items():
        if value.strip().lower() == english.lower():
            return swahili

    return value

def translate_booking_confirmation_to_swahili(content: str) -> str:
    """Translate structured booking confirmation text to Swahili."""
    translated = content
    replacements = {
        "✅ **Appointment Booked!**": "✅ **Miadi Imewekwa!**",
        "**Patient:**": "**Mgonjwa:**",
        "**Patient ID:**": "**Namba ya Mgonjwa:**",
        "**Contact:**": "**Mawasiliano:**",
        "**Type:**": "**Aina ya Huduma:**",
        "**Date/Time:**": "**Tarehe/Muda:**",
        "**Appointment ID:**": "**Namba ya Miadi:**",
        "**Congestion Level:**": "**Kiwango cha Msongamano:**",
        "**Predicted Wait:**": "**Muda wa Kusubiri Uliokadiriwa:**",
        "**Confidence:**": "**Uhakika:**",
        " minutes": " dakika",
    }
    for old, new in replacements.items():
        translated = translated.replace(old, new)

    translated = re.sub(
        r"(?m)^(\*\*Aina ya Huduma:\*\*\s*)(.+)$",
        lambda m: f"{m.group(1)}{localize_appointment_type_value_to_swahili(m.group(2).strip())}",
        translated,
    )

    translated = translated.replace("⚠️ Note: Overlaps with ", "⚠️ Tahadhari: Inaingiliana na miadi ya ")
    translated = translated.replace("'s appointment", "")
    return translated

def translate_best_slots_to_swahili(content: str) -> str:
    """Translate best available slots output to Swahili."""
    translated = content
    replacements = {
        "🎯 **Best Available Slots for ": "🎯 **Muda Bora Unaopatikana kwa ",
        "congestion": "msongamano",
        "Low msongamano": "Msongamano mdogo",
        "Moderate msongamano": "Msongamano wa kati",
        "High msongamano": "Msongamano mkubwa",
        "⏱️ Est. wait:": "⏱️ Muda wa kusubiri unaokadiriwa:",
        "min (confidence:": "dakika (uhakika:",
        "📊 **Daily Analytics:**": "📊 **Takwimu za Siku:**",
        "• Available low-congestion slots:": "• Nafasi zenye msongamano mdogo zilizopo:",
        "• Available low-msongamano slots:": "• Nafasi zenye msongamano mdogo zilizopo:",
        "• Average wait time:": "• Wastani wa muda wa kusubiri:",
        "• Availability score:": "• Kiwango cha upatikanaji:",
        " min\n": " dakika\n",
    }
    for old, new in replacements.items():
        translated = translated.replace(old, new)

    translated = re.sub(
        r"\*\*Muda Bora Unaopatikana kwa\s+([^*]+)\*\*",
        lambda m: f"**Muda Bora Unaopatikana kwa {localize_appointment_type_value_to_swahili(m.group(1).strip())}**",
        translated,
    )
    return translated

def parse_preferred_date(text: str, current_time: str) -> str:
    """Parse preferred date from common user formats and return YYYY-MM-DD."""
    normalized = normalize_text(text)

    try:
        base_date = datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M").date()
    except Exception:
        base_date = datetime.date.today()

    if "today" in normalized:
        return base_date.isoformat()
    if "tomorrow" in normalized:
        return (base_date + datetime.timedelta(days=1)).isoformat()
    if "leo" in normalized:
        return base_date.isoformat()
    if "kesho" in normalized:
        return (base_date + datetime.timedelta(days=1)).isoformat()

    ymd = re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", normalized)
    if ymd:
        try:
            return datetime.date(int(ymd.group(1)), int(ymd.group(2)), int(ymd.group(3))).isoformat()
        except ValueError:
            return ""

    dmy_slash = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", normalized)
    if dmy_slash:
        try:
            return datetime.date(int(dmy_slash.group(3)), int(dmy_slash.group(2)), int(dmy_slash.group(1))).isoformat()
        except ValueError:
            return ""

    dmy_dash = re.search(r"\b(\d{1,2})-(\d{1,2})-(\d{4})\b", normalized)
    if dmy_dash:
        try:
            return datetime.date(int(dmy_dash.group(3)), int(dmy_dash.group(2)), int(dmy_dash.group(1))).isoformat()
        except ValueError:
            return ""

    return ""

def call_caller_model(state: AgentState) -> AgentState:
    logger.debug(f"Entering call_caller_model with state: {state}")
    messages = state["messages"]
    current_time = state["current_time"]
    
    # Check if the last human message is a hospital query
    # If so, handle it directly without going through LLM tool binding
    last_human_message = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            last_human_message = msg.content
            break
    
    booking_active = is_booking_flow_active(messages)
    # During booking, preserve the language from when booking started; otherwise detect fresh
    booking_start = bool(last_human_message and any(keyword in last_human_message.lower() for keyword in [
        "book appointment", "book an appointment", "booking an appointment",
        "book a", "schedule appointment", "make appointment",
        "panga miadi", "kupanga miadi", "naomba miadi", "nataka miadi"
    ]))
    sw_lang = is_swahili_context(
        messages,
        preserve_in_booking=booking_active and not booking_start,
    )
    
    # DEBUG: Log the detection results
    logger.info(f"DEBUG: last_human_message={last_human_message}, booking_active={booking_active}, sw_lang={sw_lang}")
    if last_human_message:
        is_hosp = is_hospital_query(last_human_message)
        logger.info(f"DEBUG: is_hospital_query={is_hosp}")

    # Hospital information questions must be answered before booking-flow logic,
    # otherwise payment-location-contact questions are misclassified as booking prompts.
    if last_human_message and is_hospital_query(last_human_message):
        logger.info(f"Hospital query detected (priority): {last_human_message}")
        try:
            hospital_result = search_hospital_information.invoke({"query": last_human_message})
            logger.info(f"Hospital tool returned: {hospital_result[:100] if len(str(hospital_result)) > 100 else hospital_result}")
            if "information not available" in str(hospital_result).lower():
                if "ceo" in last_human_message.lower() or "chief executive" in last_human_message.lower() or "management" in last_human_message.lower() or "leadership" in last_human_message.lower():
                    fallback_response = localized_text(
                        "I don't have specific information about KUTRRH's leadership in my current database. However, you can find detailed information about our management and executive team at www.kutrrh.go.ke/the-executive/ or call our main line at +254 20 8000000 for inquiries about hospital leadership.",
                        "Siyo na maelezo mahususi kuhusu viongozi wa KUTRRH katika angavu yangu. Lakini, unaweza kupata taarifa nzuri kuhusu timu yetu ya uongozi kwenye www.kutrrh.go.ke/the-executive/ au piga simu +254 20 8000000 kwa maswali kuhusu viongozi wa hospitali.",
                        sw_lang
                    )
                    return {
                        "messages": messages + [AIMessage(content=fallback_response)],
                        "current_time": current_time
                    }
            return {
                "messages": messages + [AIMessage(content=hospital_result)],
                "current_time": current_time
            }
        except Exception as e:
            logger.exception(f"Error calling hospital tool: {str(e)}")
            return {
                "messages": messages + [
                    AIMessage(content=localized_text(
                        "I encountered an error retrieving hospital information. Please try again or contact support.",
                        "Nimekumbana na hitilafu wakati wa kupata taarifa za hospitali. Tafadhali jaribu tena au wasiliana na usaidizi.",
                        sw_lang,
                    ))
                ],
                "current_time": current_time
            }

    # Greetings take priority over booking prompts, including mid-booking.
    if last_human_message and is_greeting_or_social_message(last_human_message):
        logger.info(f"Greeting/social message handled locally: {last_human_message}")
        greeting_sw_lang = is_message_in_swahili(last_human_message)
        return {
            "messages": messages + [
                AIMessage(content=localized_text(
                    "Hello! I can help with hospital information, locations, contact details, and appointment booking.",
                    "Habari! Naweza kukusaidia kuhusu taarifa za hospitali, maeneo, mawasiliano, na kupanga miadi.",
                    greeting_sw_lang,
                ))
            ],
            "current_time": current_time
        }

    # Deterministic handling for service/date-only replies in active booking flow.
    if booking_active and last_human_message:
        appointment_type = detect_appointment_type(last_human_message)
        preferred_date = parse_preferred_date(last_human_message, current_time)
        selected_hour, selected_minute = parse_selected_time(last_human_message)
        patient = extract_patient_details(messages)
        has_core_details = all([
            patient.get("person_name"),
            patient.get("patient_id"),
            patient.get("phone_number"),
            patient.get("email_address"),
        ])

        missing_details = []
        missing_labels = {
            "full name": localized_text("full name", "jina kamili", sw_lang),
            "patient ID": localized_text("patient ID", "namba ya mgonjwa", sw_lang),
            "phone number": localized_text("phone number", "namba ya simu", sw_lang),
            "email address": localized_text("email address", "barua pepe", sw_lang),
        }
        for key, label in [
            ("person_name", "full name"),
            ("patient_id", "patient ID"),
            ("phone_number", "phone number"),
            ("email_address", "email address"),
        ]:
            if not patient.get(key):
                missing_details.append(missing_labels[label])

        # Hard guard: in booking flow, collect mandatory patient details first.
        # This prevents invalid tool calls from partially specified booking data.
        if missing_details and selected_hour < 0:
            return {
                "messages": messages + [
                    AIMessage(content=localized_text(
                        f"To continue booking, please provide your {', '.join(missing_details)}.",
                        f"Ili kuendelea na uwekaji wa miadi, tafadhali toa {', '.join(missing_details)}.",
                        sw_lang,
                    ))
                ],
                "current_time": current_time
            }

        # Deterministic step: once patient details are fully provided, always continue
        # with type/date questions without waiting for LLM interpretation.
        if has_core_details and not appointment_type and not preferred_date and selected_hour < 0:
            return {
                "messages": messages + [
                    AIMessage(content=localized_text(
                        "Thank you. I have your patient details. What type of appointment do you need (for example: General Check-up, Urology, Cardiology)? You can also include your preferred date.",
                        "Asante. Nimepokea taarifa zako za mgonjwa. Unahitaji aina gani ya miadi (mfano: General Check-up, Urology, Cardiology)? Unaweza pia kutaja tarehe unayopendelea.",
                        sw_lang,
                    ))
                ],
                "current_time": current_time
            }

        if appointment_type and not preferred_date:
            return {
                "messages": messages + [
                    AIMessage(content=localized_text(
                        f"Great, I can help with a {appointment_type} appointment. What is your preferred date? You can use formats like YYYY-MM-DD or DD/MM/YYYY.",
                        f"Vizuri, naweza kusaidia miadi ya {appointment_type}. Tarehe unayopendelea ni ipi? Unaweza kutumia muundo wa YYYY-MM-DD au DD/MM/YYYY.",
                        sw_lang,
                    ))
                ],
                "current_time": current_time
            }

        if preferred_date:
            resolved_type = appointment_type or extract_recent_appointment_type(messages)
            if not resolved_type:
                return {
                    "messages": messages + [
                        AIMessage(content=localized_text(
                            "Thanks. Please tell me the type of appointment you need first (for example: Urology, Cardiology, or General Check-up).",
                            "Asante. Tafadhali niambie kwanza aina ya miadi unayohitaji (mfano: Urology, Cardiology, au General Check-up).",
                            sw_lang,
                        ))
                    ],
                    "current_time": current_time
                }

            try:
                slots_result = get_optimal_appointment_slots.invoke({
                    "appointment_type": resolved_type,
                    "preferred_date": preferred_date,
                })
                if sw_lang:
                    slots_result = translate_best_slots_to_swahili(str(slots_result))
                follow_up = localized_text(
                    "\n\nPlease choose one of the available times above, and I will book it for you.",
                    "\n\nTafadhali chagua muda mmoja kati ya hiyo hapo juu, nami nitakuwekea miadi.",
                    sw_lang,
                )
                return {
                    "messages": messages + [AIMessage(content=f"{slots_result}{follow_up}")],
                    "current_time": current_time
                }
            except Exception as e:
                logger.exception(f"Error retrieving slots from deterministic booking handler: {str(e)}")

        # Deterministic booking when user selects a preferred time (e.g. 09:30, 9:30am).
        if selected_hour >= 0:
            resolved_type = appointment_type or extract_recent_appointment_type(messages)
            resolved_date = extract_recent_preferred_date(messages, current_time)
            patient = extract_patient_details(messages)

            if not resolved_type:
                return {
                    "messages": messages + [
                        AIMessage(content=localized_text(
                            "Please confirm the appointment type first (for example: Urology, Cardiology, or General Check-up).",
                            "Tafadhali thibitisha kwanza aina ya miadi (mfano: Urology, Cardiology, au General Check-up).",
                            sw_lang,
                        ))
                    ],
                    "current_time": current_time
                }

            if not resolved_date:
                return {
                    "messages": messages + [
                        AIMessage(content=localized_text(
                            "Please provide your preferred appointment date first (for example: 2026-07-01).",
                            "Tafadhali toa kwanza tarehe unayopendelea kwa miadi (mfano: 2026-07-01).",
                            sw_lang,
                        ))
                    ],
                    "current_time": current_time
                }

            if missing_details:
                return {
                    "messages": messages + [
                        AIMessage(content=localized_text(
                            f"Before I book the selected time, please provide your {', '.join(missing_details)}.",
                            f"Kabla sijaweka muda uliochagua, tafadhali toa {', '.join(missing_details)}.",
                            sw_lang,
                        ))
                    ],
                    "current_time": current_time
                }

            try:
                date_obj = datetime.datetime.strptime(resolved_date, "%Y-%m-%d")
                booking_result = book_appointment.invoke({
                    "person_name": patient["person_name"],
                    "patient_id": patient["patient_id"],
                    "phone_number": patient["phone_number"],
                    "email_address": patient["email_address"],
                    "appointment_type": resolved_type,
                    "appointment_year": date_obj.year,
                    "appointment_month": date_obj.month,
                    "appointment_day": date_obj.day,
                    "appointment_hour": selected_hour,
                    "appointment_minute": selected_minute,
                })
                final_booking_msg = str(booking_result)
                if sw_lang:
                    final_booking_msg = translate_booking_confirmation_to_swahili(final_booking_msg)
                return {
                    "messages": messages + [AIMessage(content=final_booking_msg)],
                    "current_time": current_time
                }
            except Exception as e:
                logger.exception(f"Error booking from deterministic time handler: {str(e)}")
                return {
                    "messages": messages + [
                        AIMessage(content=localized_text(
                            "I couldn't complete booking with that time. Please try another slot from the list (for example 09:00 or 09:30).",
                            "Sikuweza kukamilisha uwekaji wa miadi kwa muda huo. Tafadhali jaribu muda mwingine kutoka kwenye orodha (mfano 09:00 au 09:30).",
                            sw_lang,
                        ))
                    ],
                    "current_time": current_time
                }

    try:
        system_message = config.CALLER_PA_PROMPT.format(current_time=current_time)
        logger.debug(f"Formatted system message: {system_message}")

        formatted_messages = [
            SystemMessage(content=system_message)
        ]

        # Check if we have tool messages (results from tool execution)
        # If so, this is a synthesis step - don't bind tools to prevent new tool calls
        has_tool_messages = any(isinstance(m, ToolMessage) for m in messages)

        # For booking confirmations in Swahili, bypass synthesis and return
        # deterministic translated confirmation details.
        if has_tool_messages and sw_lang:
            last_tool_message = None
            for m in reversed(messages):
                if isinstance(m, ToolMessage):
                    last_tool_message = m
                    break
            if last_tool_message and getattr(last_tool_message, "name", "") == "book_appointment":
                translated = translate_booking_confirmation_to_swahili(last_tool_message.content)
                return {
                    "messages": messages + [AIMessage(content=translated)],
                    "current_time": current_time
                }
            if last_tool_message and getattr(last_tool_message, "name", "") == "get_optimal_appointment_slots":
                translated = translate_best_slots_to_swahili(last_tool_message.content)
                translated += "\n\nTafadhali chagua muda mmoja kati ya hiyo hapo juu, nami nitakuwekea miadi."
                return {
                    "messages": messages + [AIMessage(content=translated)],
                    "current_time": current_time
                }
        
        # Include all messages for context
        for m in messages:
            if isinstance(m, HumanMessage):
                formatted_messages.append(m)
            elif isinstance(m, AIMessage):
                # For synthesis step, include only content messages (not tool calls)
                # For initial request step, include everything
                if has_tool_messages:
                    if not (hasattr(m, 'tool_calls') and m.tool_calls):
                        formatted_messages.append(m)
                else:
                    formatted_messages.append(m)
            elif isinstance(m, ToolMessage):
                # Include tool messages as simple text
                formatted_messages.append(
                    HumanMessage(content=f"Tool results for {m.name}:\n{m.content}")
                )

        logger.debug(f"Formatted messages count: {len(formatted_messages)}")

        # For synthesis (when we have tool results), use LLM without tools
        # For initial request, use LLM with tools
        max_retries = 2
        last_error = None
        for attempt in range(max_retries):
            try:
                if has_tool_messages:
                    logger.debug("Synthesis step - using LLM without tools")
                    llm_response = llm.invoke(formatted_messages)
                else:
                    logger.debug(f"Initial request step - using LLM with tools (attempt {attempt+1})")
                    llm_response = llm_with_tools.invoke(formatted_messages)
                break  # success
            except Exception as retry_e:
                last_error = retry_e
                err_str = str(retry_e)
                if "400" in err_str and "tool" in err_str.lower() and attempt < max_retries - 1:
                    logger.warning(f"Groq tool call error on attempt {attempt+1}, retrying: {err_str[:200]}")
                    continue
                raise  # re-raise on final attempt or non-retryable errors

        logger.info(f"LLM response: {llm_response}")

        new_state = {"messages": messages + [llm_response], "current_time": current_time}
        logger.debug(f"New state after LLM response: {new_state}")
        return new_state

    except Exception as e:
        logger.exception(f"Error in call_caller_model: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        # Give a more useful message on known API/tool errors
        err_str = str(e)
        if "400" in err_str and "tool" in err_str.lower():
            user_msg = "I had trouble processing that request. Could you please rephrase your message and try again?"
        elif "429" in err_str or "rate limit" in err_str.lower():
            sw_lang = is_swahili_context(messages)
            user_msg = localized_text(
                "I'm currently rate-limited by the AI provider. Please wait about 2-3 minutes and try again.",
                "Kwa sasa nimefikia kikomo cha matumizi ya huduma ya AI. Tafadhali subiri dakika 2-3 kisha ujaribu tena.",
                sw_lang,
            )
        else:
            user_msg = "I'm sorry, I encountered an error. Could you please try again?"
        return {
            "messages": messages + [AIMessage(content=user_msg)],
            "current_time": current_time
        }

def preprocess_llm_output(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.content:
        content = last_message.content
        if "<tool_call>" in content:
            tool_call = content.split("<tool_call>")[1].split("</tool_call>")[0].strip()
            try:
                result = eval(tool_call)
                content = result
            except Exception as e:
                content = f"Error processing request: {str(e)}"
        state["messages"][-1] = AIMessage(content=content)
    return state

tool_node = ToolNode(caller_tools)
logger.info(f"Tools initialized: {len(caller_tools)} ML-enhanced tools")

# Graph
caller_workflow = StateGraph(AgentState)

# Add Nodes
caller_workflow.add_node("agent", call_caller_model)
caller_workflow.add_node("action", tool_node)

# Add Edges - from agent, decide if we have tool calls or end
caller_workflow.add_conditional_edges(
    "agent",
    should_continue_caller,
    {
        "continue": "action",  # Continue to action node if tool calls present
        "end": END,            # End if no tool calls
    },
)
# After tools are executed, go back to agent
caller_workflow.add_edge("action", "agent")

# Set Entry Point and build the graph
caller_workflow.set_entry_point("agent")

caller_app = caller_workflow.compile()
logger.info("Caller workflow compiled successfully")