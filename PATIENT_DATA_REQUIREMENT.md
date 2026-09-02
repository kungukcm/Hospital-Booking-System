# Patient Data Collection Requirements

## Overview
The Hospital Booking System now requires patients to provide comprehensive contact information through **both the manual form and the AI chat assistant**. This ensures complete patient data capture regardless of booking method.

## Required Patient Information
All four fields must be provided before any appointment can be confirmed:

1. **Full Name** - Patient's complete name
2. **Patient ID Number** - Hospital patient identification number
3. **Phone Number** - Valid contact phone number
4. **Email Address** - Valid email address (must contain @)

## Implementation Details

### Manual Form (app.py)
- **Location:** "Patient Information" section at the top of the form
- **Fields:** Four required input fields with asterisks (*) indicating requirement
- **Validation:**
  - All fields must be non-empty
  - Email must contain "@" symbol
  - Error messages displayed for missing/invalid fields
- **Data Stored:** Patient details saved to appointment record in appointments_db
- **Confirmation Display:** All patient information shown in 2-column layout after booking

### Chat Assistant (agent.py + enhanced_tools.py)
- **System Prompt Location:** `settings.yaml` under `prompts.caller_pa`
- **Agent Behavior:** 
  - First asks patient for name, patient ID, phone, and email
  - Validates each field before proceeding
  - Confirms all details match required format
  - Only calls book_appointment tool after all 4 fields collected
- **Tool Enhancement:**
  - `book_appointment()` function updated with 4 new required parameters:
    - `patient_id: str` (position 2)
    - `phone_number: str` (position 3)
    - `email_address: str` (position 4)
  - Function validates patient data before booking
  - Returns error if any required field is missing/invalid

## Database Schema Update
The appointments database now stores:
```json
{
  "id": "APT_0001",
  "name": "John Doe",
  "patient_id": "KU-12345",
  "phone": "+254712345678",
  "email": "john@example.com",
  "type": "General Checkup",
  "datetime": "2026-01-15T10:30:00",
  "predicted_wait_minutes": 18.5,
  "confidence": 0.92,
  "congestion_level": "Low",
  "duration_minutes": 30,
  "status": "confirmed",
  "created_at": "2026-01-10T14:22:30"
}
```

## Validation Rules

| Field | Type | Rules | Error Message |
|-------|------|-------|----------------|
| Name | String | Non-empty | "❌ Patient name is required." |
| Patient ID | String | Non-empty | "❌ Patient ID is required." |
| Phone | String | Non-empty | "❌ Phone number is required." |
| Email | String | Non-empty, contains @ | "❌ Valid email address is required." |

## Files Modified

### 1. app.py (Streamlit UI)
- **Changes:** Added 4 patient information input fields in "Patient Information" section
- **Validation:** Form submission checks all 4 fields before creating appointment
- **Display:** Appointment confirmation shows all patient details

### 2. enhanced_tools.py (LangChain Tools)
- **Changes:** Updated `book_appointment()` function signature to include:
  - `patient_id: str`
  - `phone_number: str`
  - `email_address: str`
- **Validation:** Added input validation at tool level
- **Response:** Confirmation includes patient ID and contact information

### 3. settings.yaml (System Prompt)
- **Changes:** Updated `prompts.caller_pa` with:
  - PATIENT INFORMATION REQUIREMENT section
  - Clear instructions to collect all 4 fields
  - Validation requirements
  - Updated tool signature documentation
- **Impact:** Agent now knows to request patient data before booking

### 4. appointments_db.py (Database)
- **No changes required:** Database accepts any additional fields in appointment record
- **Compatibility:** New fields (patient_id, phone, email) automatically stored

## User Experience

### Form-Based Booking
1. User opens form and sees "Patient Information" section
2. Required fields marked with red asterisks (*)
3. Fields: Name, Patient ID, Phone, Email with placeholders
4. Form validates all fields before submission
5. Confirmation displays all patient information in structured 2-column layout
6. Appointment ID generated and displayed

### Chat-Based Booking
1. User says "I want to book an appointment"
2. Agent responds: "I'd be happy to help! First, I need some information..."
3. Agent asks for each field with friendly context:
   - "What is your full name?"
   - "What is your patient ID number?"
   - "What is your contact phone number?"
   - "What is your email address?"
4. Agent validates each response
5. Agent confirms details before booking
6. Agent calls `book_appointment()` with all 4 data fields
7. Confirmation includes appointment ID and patient details

## Testing Checklist

- [x] Manual form collects all 4 patient fields
- [x] Form validation requires all fields
- [x] Email validation checks for @ symbol
- [x] Appointment record includes patient_id, phone, email
- [x] Confirmation displays all patient information
- [x] book_appointment tool accepts 4 new parameters
- [x] System prompt instructs agent to collect patient data
- [x] Database stores all fields correctly
- [ ] Chat-based booking prompts for all 4 fields
- [ ] Chat validation matches form validation
- [ ] End-to-end chat booking captures complete data

## Benefits

1. **Complete Patient Records** - All necessary contact information captured
2. **Better Communication** - Hospital has phone and email for patient notification
3. **Consistency** - Same data collected regardless of booking method
4. **Data Integrity** - Form and chat validation ensures quality data
5. **Hospital Compliance** - Meets patient data requirements for scheduling systems
6. **KUTRRH Branding** - System represents hospital as KUTRRH (Kenyatta University Teaching, Referral and Research Hospital)
