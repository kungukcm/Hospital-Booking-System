# CHAPTER 4. SYSTEM DESIGN AND IMPLEMENTATION

## 4.1 Introduction

This chapter details the architecture and implementation of the AI-driven hospital patient support assistant. The design objective was to preserve conversational usability—allowing users to interact naturally in their preferred language—while guaranteeing reliable transaction completion in appointment workflows. The chapter covers architectural decisions, component design, workflow implementation, and privacy-aligned practices.

## 4.2 Design Philosophy and Core Principles

The implementation is guided by five foundational principles that informed all technical and architectural decisions:

**Principle 1: Separation of Language Understanding from Transaction Execution.** Conversational understanding and transaction execution must be logically separated in the codebase and in execution flow. An LLM can handle language understanding: interpreting varied expressions of the same intent, maintaining conversational context, and generating natural responses. However, LLMs should not directly execute transactions. Instead, their output should be validated, parsed by deterministic logic, and checked against operational constraints before any transaction occurs. This separation creates a boundary where errors in language understanding do not automatically become errors in data or system state.

**Principle 2: Deterministic Control for High-Risk Workflow Transitions.** Any workflow transition that has consequences for patient records or system state must be deterministic, not probabilistic. The system cannot attempt a booking "if the LLM seems confident." Instead, it must verify that all mandatory data is present, that the requested service is valid, that the date and time are feasible, and that no conflicts exist. These checks must be explicit, testable, and logged. This principle means that some conversational flexibility is sacrificed—the user cannot say "just book something" without specifying details—but this trade-off protects data integrity.

**Principle 3: Minimal but Sufficient Data Capture.** The system captures only data necessary for appointment operations and institutional communication: patient name for identification, patient ID for medical record linkage, phone number and email for appointment reminders and confirmation. It does not capture diagnosis history, treatment details, or other clinical information. This data minimization reduces privacy risk, simplifies compliance, and reduces the scope for misuse if data is compromised. It also reinforces that the system is administrative, not clinical.

**Principle 4: Explainable Recommendation Outputs for User Decision Support.** Queue-aware recommendations are valuable only if users understand them and can act on them rationally. This means recommendations must include not just a list of slots but explanation: why this slot is recommended (lower waiting time), what the estimated waiting time is, and how confident the system is in that estimate. Opaque recommendations or recommendations without reasoning undermine user trust.

**Principle 5: Policy-Aware Logging and Error Handling.** Every significant event in the system is logged: messages received, language context detected, parsed entities, tool invocations, outcomes, and errors. Logs are structured to support both debugging during development and auditing during deployment. Error handling is user-facing and recovery-oriented: when the system cannot complete a task, it explains why and suggests next steps, rather than returning generic failures.

## 4.3 System Architecture Overview

### 4.3.1 Layered Architecture Rationale

The system employs a five-layer architecture that supports independent development, testing, and improvement of each layer:

**Layer 1: Interface Layer** - How users interact with the system  
**Layer 2: Orchestration Layer** - How the system sequences operations  
**Layer 3: Intelligence Layer** - How the system understands language and generates responses  
**Layer 4: Tool/Operations Layer** - How the system affects external systems  
**Layer 5: Data and Logging Layer** - How the system persists information and creates audit trails  

This layering avoids tight coupling where a change in one layer requires changes throughout the system. The interface can be redesigned without touching orchestration logic. The intelligence layer can be swapped to a different LLM without affecting tool execution.

### 4.3.2 Interface Layer Design

**User-Facing Conversational Interface.** The interface is implemented using Streamlit, a Python framework for rapid development of data applications with web interfaces. Streamlit was chosen for several reasons: it supports real-time session state management (important for maintaining conversation context), it provides simple widget libraries for displaying information, it is easy for developers to prototype and modify, and it can be deployed rapidly in research or institutional settings.

The interface displays the conversation history showing both user messages and system responses, creating a clear visual narrative of the interaction. This approach is more familiar to modern users accustomed to messaging applications than traditional form-based interfaces. Users can see what they said, what the system understood, what questions the system asked, and what confirmations were provided.

**Session State Management.** Session state preserves conversation history, detected language context, partially-entered information (service type, date, time), and user preferences across messages within a single session. This state allows the system to maintain context when a user provides information incrementally.

### 4.3.3 Orchestration Layer Design

**Graph-Based Workflow State Machine.** Orchestration logic uses a graph-based workflow model where nodes represent states (e.g., "awaiting_service_specification," "awaiting_date_selection") and edges represent transitions. The transitions are conditional based on what information the system has, what the user provided, and what the next step requires.

The state machine approach makes workflow logic explicit and testable. Each state specifies: what prompts should be shown, what information is required to leave the state, what conditions trigger transitions to which next states. This makes it easy to validate that the workflow is correct and to identify gaps or loops.

**Deterministic Routing Logic.** At each transition point, routing logic checks preconditions: Do we have all mandatory information? Is the selected service valid? Is the date in the future? Only when preconditions are satisfied do transitions proceed. If preconditions are not met, the system returns to the current state with a clarifying prompt.

### 4.3.4 Intelligence Layer Design

**LLM-Powered Understanding and Generation.** The system uses Claude 3.5 (Anthropic) for language understanding and response generation. The model is prompted to: interpret user intent from natural language, detect whether required information is present, identify potential entities (service type, date, time), and generate conversational responses.

Prompting is careful about boundaries. The system prompt explicitly instructs the model to:
- Not provide clinical advice
- Not claim to have information it does not have
- Ask clarifying questions when user input is ambiguous
- Respect language context (respond in the language the user is using)
- Admit uncertainty ("I'm not sure what service you mean by 'heart check'—could you say more?")

**Tool Binding and Controlled Invocation.** The LLM has access to tool definitions and can suggest tool invocations. However, tool invocation is gated: the system validates that all required parameters are present and valid before actually executing the tool. If the LLM generates a malformed tool invocation, it is caught and reported rather than passed to the backend.

### 4.3.5 Tool/Operations Layer Design

**Tool Abstraction.** Tools abstract hospital operations: "create appointment," "recommend best slot," "estimate wait time," "retrieve next available," "cancel appointment," "check conflicts." Tools have explicit schemas defining required and optional parameters and expected return types.

**Appointment Booking Tool.** The core tool creates appointment records with mandatory fields (patient name, ID, phone, email, service type, date, time) and optional fields (notes, follow-up scheduling). The tool validates that the requested service exists and that the time slot is available. It returns a structured confirmation containing appointment ID, confirmed date/time, service name, location/clinician, and instructions for the patient.

**Queue Prediction and Recommendation Tool.** This tool predicts waiting time for different slots using a simple model: high-volume services have longer waits, peak hours have longer waits, more staff allocated reduce waits. Predictions are probabilistic but are presented deterministically (e.g., "low" vs "high" congestion rather than exact minutes). The tool ranks slots and returns the top 3-5 recommendations with explanations.

**Cancellation Tool.** This tool cancels existing appointments and optionally creates a new booking with different parameters. It verifies the appointment exists before canceling and returns confirmation that the old appointment is removed.

### 4.3.6 Data and Logging Layer Design

**Persistent Appointment Storage.** Appointment records are persisted in a JSON-based data store. This is appropriate for a prototype; production systems would use a relational database. The JSON structure includes appointment ID, patient details, service information, date/time, status (booked, canceled), and creation/modification timestamps.

**Structured Event Logging.** All significant events are logged in a structured format: timestamp, event type (message_received, intent_detected, tool_invoked, tool_completed, error_occurred), relevant data, and outcome. This structured format allows downstream analysis and auditing.

## 4.4 Booking Workflow Design in Detail

### 4.4.1 Workflow Stages and Transitions

The booking flow progresses through seven stages, each with defined prerequisites and transitions:

**Stage 1: Booking Intent Detection.** The system detects that the user wants to book an appointment. The user might say "I need an appointment," "Can I book a clinic visit?" or simply "Cardiology." The system confirms intent and moves to Stage 2. If the user also provided the service type (e.g., "I want to book Cardiology"), Stage 1 is essentially completed and Stage 2 can proceed immediately.

**Stage 2: Patient Detail Collection.** The system requests or confirms patient name, ID, phone number, and email. The user might provide all of this at once ("My name is James Karanja, ID is K123456, phone is 0712345678, email is james@example.com") or in pieces across multiple messages. The system parses and collects information incrementally. Stage 2 is complete when all four fields are present and validated.

**Stage 3: Appointment Type Confirmation.** If the user did not specify a service in Stage 1, the system asks. If they did, the system confirms understanding ("So you want to book Cardiology?") and requests confirmation. This stage resolves potential ambiguity (e.g., distinguishing between "Cardiac Surgery" and "Cardiology," or clarifying colloquial terms like "heart doctor" to the official service name). Stage 3 is complete when a valid service type is confirmed.

**Stage 4: Preferred Date Parsing and Validation.** The system asks for the preferred date. Users might provide dates in multiple formats: "next Tuesday," "July 15," "2024-07-15," "in two weeks." The date parsing logic normalizes these to a canonical date format. Validation checks that the date is in the future, within a reasonable booking window (e.g., not more than 3 months ahead), and that the requested service has availability on that date. Stage 4 is complete when a valid future date is selected.

**Stage 5: Slot Recommendation and Presentation.** The system queries available slots for the service on the selected date. It predicts congestion for different slots and presents the top 3-5 options ranked by lower predicted waiting burden. Each option shows: time, congestion level (green for low, yellow for moderate, red for high), and estimated waiting time. This stage gives users information to make informed selections.

**Stage 6: Time Selection.** The user selects a specific time from the presented options, or the system interprets their time preference ("I prefer morning" or "around 2 PM"). The system confirms the selected time is still available. Stage 6 is complete when the user selects a specific slot.

**Stage 7: Transaction Confirmation and Booking Execution.** The system presents a final confirmation showing exactly what will be booked: patient name, service, date, time, and expected location/clinician. The user confirms, and the booking tool is executed. Upon successful booking, the system provides a booking confirmation including appointment ID and instructions to bring their card/identification.

### 4.4.2 Mandatory Detail Enforcement

Before the booking tool is invoked, the system enforces that all mandatory details are present and valid:

**Patient Name.** Required to identify the patient in the medical record system. Must be non-empty and match institutional naming conventions (alphabetic characters with possible spaces).

**Patient ID.** Required to link the appointment to the correct medical record. Format validation ensures the ID matches institutional format (typically alphanumeric or numeric).

**Phone Number.** Required for appointment reminders and follow-up communication. Format validation checks that the number is a valid Kenyan format or similar.

**Email Address.** Required for electronic confirmation. Format validation uses standard email regex patterns. If a user does not provide an email, the system offers to use phone-only communication.

The system will not proceed past Stage 6 without all mandatory details. If details are missing, it loops back to request them, showing which specific fields are required.

### 4.4.3 Input Parsing and Entity Recognition

**Service Type Parsing.** A mapping table translates colloquial or abbreviated service names to canonical service types. For example, "heart doctor" maps to "Cardiology," "cancer clinic" maps to "Oncology," "blood pressure" maps to "Internal Medicine." Users can also provide exact service names. If the user's input does not clearly match any service, the system lists available options and asks the user to choose.

**Date Parsing.** The date parser handles multiple formats: "next Tuesday," "July 15," "2024-07-15," "in three days," "tomorrow." The parser uses a library for natural language date parsing and then validates the resulting date is in the future and within the booking window.

**Time Parsing.** The time parser handles "9 AM," "09:00," "2 PM," "14:00," "morning" (interpreted as 9 AM), "afternoon" (interpreted as 2 PM). Users can also respond to slot recommendations by selecting an option number ("Option 2, the 10:30 slot").

### 4.4.4 Context Recovery from Partial Input

When users provide partial information—for example, only time—the system must recover context from earlier in the conversation. Context recovery logic maintains a session-level variable tracking: current service type (if selected), current date (if selected), patient details (if provided). When a user later says "I prefer 2 PM," the system recovers that this applies to the already-selected service and date, rather than asking for those again.

## 4.5 Queue-Aware Recommendation Design

### 4.5.1 Recommendation Philosophy

Queue-aware recommendations are not predictions of the future but decision support based on typical patterns. The system does not claim to know exactly how long a user will wait (too many unknowns affect actual wait time). Instead, it provides relative guidance: this slot is typically less busy than another, so it might be a better choice if wait time matters to you.

### 4.5.2 Congestion Categories and Presentation

Slots are categorized into three congestion bands based on predicted waiting time:

**Low Congestion (Green).** Expected waiting time <20 minutes. This might be early morning or late afternoon on slower days. Users typically see several low-congestion options; these are highlighted as "best" choices.

**Moderate Congestion (Yellow).** Expected waiting time 20-45 minutes. This is typical for mid-day or mid-week appointments. Users can choose these if specific times matter to them, with the understanding they should prepare for a wait.

**High Congestion (Red).** Expected waiting time >45 minutes. This might be peak hours (morning rush) or specialty clinics with very high demand. Users are presented with high-congestion options for completeness but with clear indication that these slots are busy.

The presentation shows the recommendation, the congestion band, and a brief explanation: "10:00 - Low (est. 15 min wait) - Recommended" vs "11:00 - High (est. 50 min wait)."

### 4.5.3 Confidence and Uncertainty Handling

The system is transparent about limitations. Queue predictions are based on historical patterns and assumptions about staffing and demand. Reality could differ due to emergencies, staff changes, or unexpected high demand. The system includes a disclaimer: "Estimated waiting times are based on typical patterns and may vary. Actual wait time could be longer if there are urgent cases or staff changes."

### 4.5.4 User Presentation

Recommendations are presented in a user-friendly table format:

| Time | Congestion | Est. Wait | Status |
|------|-----------|-----------|--------|
| 09:00 | 🟢 Low | 15 min | ← Recommended |
| 10:30 | 🟢 Low | 18 min | ← Recommended |
| 14:00 | 🟢 Low | 12 min | ← Recommended |
| 11:00 | 🟡 Moderate | 35 min | |
| 12:00 | 🔴 High | 55 min | |

Below the table: "We recommend the green options if your schedule allows. They typically have shorter waits. You can choose any option—which time works for you?"

This format makes it easy for users to see options and understand reasoning.

## 4.6 Multilingual Implementation

### 4.6.1 Language Context Detection

Language context is detected using a multi-signal approach:

**Primary Signal: Recent User Messages.** The most recent user message(s) are checked for language indicators. If recent messages are in Swahili, the context is Swahili. If recent messages are in English, the context is English.

**Secondary Signal: Explicit Language Selection.** Users can explicitly state language preference ("reply in Swahili" or "please use English"). This overrides automatic detection.

**Fallback Signal: Session History.** If the current message is ambiguous (e.g., purely numeric date), the system looks back at earlier messages in the session to infer language context. If the user has been using Swahili throughout, the assumption is Swahili unless they switch.

**Default**: In ambiguous cases where no clear language signal exists, the system defaults to English but offers to switch: "I'm responding in English, but I can use Swahili if you prefer."

### 4.6.2 Language-Mirroring in Conversational Response

The LLM is prompted to mirror the user's language in conversational exchanges. If the user says something in Swahili, the response should be in Swahili. If the user switches to English, the response should switch to English. This mirroring is maintained across the conversation unless the user explicitly requests a different language.

### 4.6.3 Deterministic Transactional Localization

While conversational fluency can use LLM-generated language, critical transactional messages must be deterministically localized to prevent language drift. Four types of messages are deterministically localized:

**Booking Confirmation Block.** When a booking is confirmed, the confirmation shows exactly what was booked in the user's language:

*English:* "✓ Appointment Booked! Your appointment is confirmed: Cardiology, July 15, 2024, 10:00 AM. Appointment ID: APT-2024-07-15-001."

*Swahili:* "✓ Miadi Imehifadhiwa! Miadi yako imehakikishwa: Cardiology, Julai 15, 2024, saa 10:00 asubuhi. Kitambulisho cha Miadi: APT-2024-07-15-001."

**Best-Slot Recommendation Block.** When presenting slot options, the columns and content are localized:

*English header:* "Here are your best available times:" with columns "Time | Congestion | Wait"

*Swahili header:* "Hichi ndicho wakati wako wa haraka zaidi:" with columns "Wakati | Kasi | Kusubiri"

**Service-Type Values.** Appointment types are presented in the user's language. A service might be stored internally as "Cardiology" but presented as "Cardiology" in English and "Magonjwa ya Moyo" in Swahili.

**Follow-up Prompts.** When the system needs additional information, prompts are localized:

*English:* "To complete your booking, I need your patient ID."

*Swahili:* "Ili kukamilisha miadi yako, ninahitaji namba yako ya mgonjwa."

This deterministic localization is implemented using lookup tables and string templates rather than relying on LLM translation, ensuring consistency.

### 4.6.4 Error Messages and Clarifications

Even error messages maintain language context:

*English error:* "I'm not sure what service you mean by 'heart check.' Did you mean: Cardiology, Cardiac Surgery, or Internal Medicine?"

*Swahili error:* "Sijui huduma gani unayomaanisha na 'heckup ya moyo.' Je, unakusudiwa: Cardiology, Operesheni ya Moyo, au Tiba ya Ndani?"

## 4.7 Error Handling and Recovery Strategies

### 4.7.1 Graceful Degradation

When the system cannot complete an operation perfectly, it degrades gracefully rather than failing:

- If the LLM is unable to parse a date, the system asks for clarification rather than guessing.
- If a backend tool times out, the system informs the user and suggests retry or escalation.
- If language context is ambiguous, the system asks the user to clarify rather than guessing wrong.

### 4.7.2 Retry Logic

For transient failures (e.g., temporary API unavailability), the system automatically retries up to 3 times with exponential backoff before reporting failure to the user.

### 4.7.3 Explicit Fallback Prompts

When deterministic checks fail (e.g., missing mandatory data), the system returns to specific prompts:

- Missing service type: "What service or clinic do you need an appointment with?"
- Missing date: "What date works for you?"
- Missing patient ID: "To complete the booking, I need your patient ID."

These are explicit, unambiguous prompts that guide the user toward providing the needed information.

### 4.7.4 Escalation to Human Review

When the system cannot confidently handle a request (e.g., "I need to reschedule but I'm not sure what I'm currently booked for"), it escalates to human staff with a clear summary: "This patient needs help rescheduling an existing appointment. I couldn't look up their current booking. Please assist."

## 4.8 Security and Privacy-Oriented Design Choices

### 4.8.1 Data Minimization

The system captures only operationally necessary data: patient name, ID, contact information, and appointment preferences. It does not capture:
- Diagnosis or symptoms
- Medical history
- Treatment details
- Insurance information
- Emergency contact information

This minimization reduces privacy risk and simplifies compliance.

### 4.8.2 Role and Scope Clarity

The system never provides medical advice. Responses explicitly avoid clinical guidance:
- ✓ "I can help you book an appointment with a cardiologist."
- ✗ "You should see a cardiologist because you might have high blood pressure."

This role clarity protects users from mistaking the system for clinical guidance.

### 4.8.3 Audit Logging

All significant events are logged with timestamps and context: messages received, entities parsed, tool invocations, outcomes, errors. Logs support debugging during development and auditing during deployment.

### 4.8.4 Access Control Assumptions

In a deployed system, access to logs and appointment records would be role-restricted (only authorized administrative staff), and changes would be logged. The prototype demonstrates logging infrastructure but relies on deployment configuration for access control.

## 4.9 Chapter Summary

This chapter has detailed the architecture and implementation of the system, from high-level design principles through specific technical implementation patterns. The next chapter presents evaluation results, demonstrating how well this design achieves its objectives of reliable booking, language consistency, and queue-aware recommendation in realistic usage scenarios.
3. logging architecture designed for controlled access;
4. recommendation to move secrets to environment variables.

## 4.9 Deployment and Operationalization

Deployment artifacts include Docker files, cloud deployment documentation, runtime specification, and quick-start guides. This supports transition from prototype testing to pilot deployment after institutional compliance checks.

## 4.10 Chapter Summary

This chapter has presented implementation architecture and core design logic, emphasizing deterministic reliability and multilingual transactional consistency. The next chapter evaluates system outcomes and performance implications.
