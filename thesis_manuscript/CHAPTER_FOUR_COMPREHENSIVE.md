# CHAPTER 4. SYSTEM DESIGN AND IMPLEMENTATION

## 4.1 Introduction

This chapter details the architecture and implementation of the AI-driven hospital patient support assistant, presenting the design decisions that address the research objectives defined in Chapter 1 and grounded in the literature reviewed in Chapter 2. The chapter moves from high-level architectural principles through individual component design to specific implementation choices that realize the system's key capabilities: reliable booking completion, queue-aware recommendation, and multilingual localization consistency.

The design documentation in this chapter serves two purposes. At the immediate level, it documents the artifact created in this thesis, enabling replication, adaptation, and critique. At the broader level, it communicates design knowledge, the principles and patterns that proved effective in addressing the specific challenges of healthcare conversational AI, that can be applied beyond this specific system. Design science research generates value through both kinds of documentation.

The chapter is organized to follow the layered architecture of the system, beginning with the principles that guided all design decisions, proceeding through the five architectural layers from interface to data, and then examining the specific sub-systems that implement the system's distinctive capabilities: the booking state machine, the multilingual localization engine, and the queue prediction and recommendation subsystem.

## 4.2 Design Philosophy and Foundational Principles

Five foundational design principles informed all architectural and implementation decisions. These principles represent the translation of research insights from the literature review into concrete design commitments.

### 4.2.1 Separation of Language Understanding from Transaction Execution

The first principle is that conversational understanding and transaction execution must be architecturally separated, both in code organization and in execution flow. This principle responds directly to the reliability challenge documented in the literature: LLMs are optimized for language production, not for structured schema compliance, and their tool invocations cannot be fully trusted without validation.

In the implemented system, the LLM performs language understanding: interpreting user messages, extracting intent, identifying information entities, generating conversational responses, and adapting language style to context. The LLM does not execute transactions. Instead, its outputs are received by the orchestration layer, validated by the guardrail module, and only then passed to the tool execution layer. If validation fails, the orchestration layer generates a clarifying prompt, and the LLM generates the conversational response to that prompt, but the transaction does not proceed.

This separation creates an architectural boundary where errors in language understanding cannot automatically propagate to errors in system state. The LLM can misunderstand a user input, but the guardrail will catch any resulting parameter problems before a transaction is attempted. The user receives a clarifying question rather than a failed booking, and the conversation continues rather than ending in error.

### 4.2.2 Deterministic Control for High-Risk Workflow Transitions

The second principle is that workflow transitions with consequences for patient records must be controlled by deterministic logic, not probabilistic model judgment. The system cannot decide whether to attempt a booking based on whether the LLM "seems confident." Instead, the booking transition requires that all mandatory parameters have been explicitly collected and validated, that the requested service exists, that the date is in the future, that the time slot is available, and that no conflicts exist. These conditions are checked deterministically before the booking tool is invoked.

This principle means that some conversational flexibility is constrained: a user cannot instruct the system to proceed without all required information. However, the constraint is entirely transparent to users: when mandatory information is missing, the system explains what is needed and asks the user to provide it. The constraint is experienced as helpful guidance rather than arbitrary refusal.

### 4.2.3 Minimal but Sufficient Data Capture

The third principle is data minimization: the system captures only what is necessary for appointment operations and nothing more. Required data elements are patient name, patient identification number, phone number, email address, service type, appointment date, and appointment time. The system does not collect medical history, diagnosis information, insurance details, or any information beyond what is needed to create an appointment record and contact the patient.

This principle serves two functions. First, it reduces privacy risk: less data means a smaller harm surface if data is compromised. Second, it reinforces the system's identity as an administrative tool: by not asking for clinical information, the system makes clear through its behavior that it is not performing a clinical function.

### 4.2.4 Explainable Recommendation Outputs

The fourth principle is that queue recommendations must be explainable: they must include not just rankings but the reasoning behind them. A recommendation that says "Book at 11 AM" without explanation is unlikely to influence patient behavior or be trusted. A recommendation that says "This slot is recommended because it typically has shorter waiting times, usually around 15 to 20 minutes compared to over 40 minutes at peak hours" enables patients to evaluate the recommendation against their own priorities and make an informed choice.

Explainability in queue recommendations is implemented through structured output templates that include the predicted congestion level (low, moderate, high), an estimated wait time range, and a brief explanation of why this slot is predicted to be less busy. The explanation is kept brief and non-technical to ensure it is accessible to patients without healthcare operations knowledge.

### 4.2.5 Policy-Aware Logging and Error Handling

The fifth principle is that logging and error handling are governance functions as well as operational functions. Every significant event is logged in a structured format that supports both debugging and auditing: message receipt, intent classification, entity extraction, tool invocation, tool outcome, error occurrence, and state transition. Logs include timestamps, session identifiers, event types, and relevant data, enabling reconstruction of complete interaction histories.

Error handling is user-facing and recovery-oriented. When the system cannot complete a task, it explains why in user-appropriate language and suggests what the user should do next. Generic error messages are avoided; specific, actionable guidance is provided. This approach maintains user engagement and minimizes the likelihood of users abandoning the booking process due to confusion about what went wrong.

## 4.3 System Architecture

### 4.3.1 Layered Architecture Design

The system employs a five-layer architecture that supports independent development, testing, and modification of each layer without requiring coordinated changes across the entire system.

Layer 1, the Interface Layer, is the patient-facing component that receives user input and displays system responses. It is responsible for rendering the conversation, managing session state, and displaying structured outputs (appointment options, confirmations) in an appropriate visual format.

Layer 2, the Orchestration Layer, is the coordination component that manages workflow state, determines what action to take based on current state and user input, and coordinates between the intelligence and tool layers. This layer implements the state machine and validation logic.

Layer 3, the Intelligence Layer, is the AI component responsible for language understanding and response generation. It receives structured context from the orchestration layer (current workflow state, collected information, detected language) and returns structured intent classifications, extracted entities, and conversational response text.

Layer 4, the Tool and Operations Layer, provides interfaces to backend appointment operations. Tools receive validated parameters from the orchestration layer and return structured results. This layer is the only layer that modifies persistent system state (appointment records).

Layer 5, the Data and Logging Layer, provides persistent storage for appointment records and structured logging for all system events. This layer serves both operational functions (storing appointments) and governance functions (maintaining audit trails).

### 4.3.2 Interface Layer Implementation

The patient-facing interface is implemented as a web-based chat application using the Streamlit framework. The design follows a familiar messaging application pattern: user messages appear on the right side of the conversation view, system responses on the left, and the input field is at the bottom. This convention is recognizable to mobile-phone users familiar with SMS and messaging apps, reducing the learning curve for first-time users.

The interface maintains and displays the full conversation history within a session, allowing users to scroll back and review what was discussed and what was agreed. This is particularly important for confirmation: users can verify their booking details against the conversation history if they are uncertain about what was booked.

Session state management in Streamlit handles the persistence of conversation history, detected language, partially collected booking information, and user preferences within a session. Session state is cleared at the end of a session (or when the browser tab is closed), ensuring that patient data from one session does not persist into subsequent sessions.

The interface includes a visible scope disclaimer that is displayed at the start of each session: the system explains that it can help with appointment booking, cancellation, and information about available times, and that it does not provide medical advice. This proactive scope communication reduces the likelihood of users asking for clinical guidance and sets accurate expectations about what the system can do.

### 4.3.3 Orchestration Layer Implementation

The orchestration layer is built on the LangGraph framework, which provides a graph-based workflow management system. The booking workflow is represented as a directed graph where nodes represent workflow states and edges represent conditional transitions between states.

The booking workflow graph includes the following principal states: initial (waiting for user intent), intent-detected (user has expressed booking intention), collecting-patient-details (gathering name, ID, phone, email), service-confirmed (service type has been identified and validated), date-selected (appointment date has been provided and parsed), time-selected (appointment time has been provided), pre-booking-validation (all required parameters are present and valid), booking-executing (tool invocation is in progress), booking-confirmed (booking was successfully created), and booking-failed (booking encountered an error requiring recovery).

State transitions are conditional: moving from collecting-patient-details to service-confirmed requires that all four patient detail fields are present and validated. Moving from pre-booking-validation to booking-executing requires that all booking parameters are present, valid, and non-conflicting. If a condition for transition is not met, the workflow remains in the current state and the system generates an appropriate clarifying prompt.

The workflow also includes alternative paths for cancellation and information retrieval, which have their own state sequences with appropriate validation requirements. The graph structure makes these alternative paths explicit and ensures that validation requirements are enforced on all paths, not just the primary booking flow.

### 4.3.4 Intelligence Layer Implementation

The intelligence layer uses Claude (Anthropic) accessed through the Anthropic Python SDK. The integration follows a structured prompting approach where each LLM call receives a carefully designed system prompt, the current conversation history, and structured context about the current workflow state.

The system prompt establishes the assistant's identity, scope, and operating principles. Key elements of the system prompt include: a description of the assistant as a hospital appointment scheduling assistant, explicit statements that the assistant does not provide medical advice, instructions to respond in the same language the user is using, guidelines for handling ambiguous requests (ask for clarification rather than guessing), and instructions for how to collect each required booking field if it has not yet been provided.

The system prompt is updated dynamically based on the current workflow state: when the system is in the service-confirmed state, the prompt includes additional instruction to focus on date collection; when the system is in the date-selected state, the prompt focuses on time collection. This dynamic prompting reduces the LLM's cognitive load at each step and increases the relevance of its responses to the current stage of the interaction.

Tool definitions are provided to the LLM using Anthropic's tool use format, which specifies each tool's name, description, and parameter schema. The LLM may suggest tool invocations, but as noted above, these suggestions are validated by the orchestration layer before execution.

### 4.3.5 Tool and Operations Layer Implementation

The tool layer implements seven operations, each defined as a Python function with a strict parameter schema and structured return type.

The create-appointment tool accepts patient name, patient ID, phone, email, service type, date, and time as required parameters, with an optional notes field. It validates that the service type is recognized, that the date and time combination is available, and that no duplicate booking exists for the patient, date, and time. On success, it creates an appointment record and returns a structured confirmation including appointment ID, confirmed date and time, service name, location, and patient instructions. On failure, it returns a structured error response indicating what went wrong.

The cancel-appointment tool accepts an appointment ID and patient ID as required parameters, validates that the appointment exists and belongs to the specified patient, updates the appointment status to cancelled, and returns a cancellation confirmation. It does not accept cancellations without appointment ID verification to prevent accidental or unauthorized cancellations.

The get-next-available tool accepts a service type as a required parameter and returns the next available appointment slot for that service, including date, time, and a brief description of what to expect. It queries the appointment database for available slots and returns the earliest unbooked slot.

The recommend-best-slot tool accepts a service type and an optional date range as parameters and returns a ranked list of appointment options with congestion estimates, estimated wait times, and recommendation explanations. The congestion estimates are generated by the queue prediction subsystem described below.

The check-availability tool accepts a service type, date, and time and returns a boolean indicating whether that specific slot is available, along with the predicted congestion level for that slot. This tool supports the scenario where a user has a strong preference for a specific time and wants to know whether that time is available and how busy it will be.

The get-appointment-details tool accepts an appointment ID and patient ID and returns the full details of an existing appointment. This tool supports the cancellation workflow (where the user needs to confirm details before cancelling) and the information-retrieval workflow (where the user wants to know the details of a scheduled appointment).

The list-services tool accepts no required parameters and returns the list of available services with brief descriptions. This tool supports the initial phase of booking conversations where users may not know the name of the service they need.

### 4.3.6 Data and Logging Layer Implementation

Appointment records are stored in a JSON-based data store for the prototype implementation. Each record includes a unique appointment ID, patient details (name, ID, phone, email), service type, date and time, appointment status (scheduled, cancelled, completed), creation timestamp, and modification timestamps. The JSON format is adequate for prototype evaluation purposes; a production system would use a relational database (such as PostgreSQL) with proper indexing, backup, and transaction management.

The logging subsystem writes structured log records for all significant system events. Log records follow a consistent schema: timestamp, session ID, event type, event data, and outcome. The event type vocabulary includes message-received, intent-classified, entity-extracted, state-transition, tool-invoked, tool-completed, tool-failed, error-occurred, and session-ended. This structured vocabulary enables automated analysis of log data and ensures consistency across the audit trail.

Logs are written to a rotating log file system in the prototype; a production deployment would write to a centralized logging system with access controls, retention policies, and search capabilities appropriate for healthcare audit requirements.

## 4.4 Booking Workflow Design in Detail

### 4.4.1 Information Collection Sequence

The booking workflow collects information in a tolerant order: the system accepts information in whatever order the user provides it and tracks what has been collected. However, the state machine enforces that execution does not proceed until all required information has been received, regardless of the order in which it arrived.

The required information falls into two categories. Patient identification information, comprising name, patient ID, phone, and email, is collected first when not already known. This ordering ensures that if the booking fails for any reason, the patient's contact details are available to notify them. Appointment specification information, comprising service type, date, and time, is collected second, as the patient may need guidance in specifying these correctly.

The state machine tolerates users providing information across multiple turns. A user who says "I want a cardiology appointment next Tuesday at 2 PM" has provided three pieces of appointment information in a single message. The entity extraction component identifies all three and updates the workflow state accordingly. The system then asks only for the remaining missing information rather than asking for information that has already been provided.

### 4.4.2 Service Type Resolution

Service type resolution is a specific challenge in the healthcare booking context. Patients may refer to services using clinical terminology (cardiologist, nephrologist), common descriptive terms (heart doctor, kidney specialist), Swahili equivalents (daktari wa moyo, daktari wa figo), or informal descriptions (the clinic for blood problems, the department that handles breathing issues). The system must map all of these expressions to the valid service identifiers in the system.

The service type resolution uses a two-stage approach. First, the LLM attempts to match the user's expression to one of the defined service types using its language understanding capabilities. Second, if the LLM's suggestion is uncertain or maps to an ambiguous service, the system presents the user with a confirmation question: "Did you mean cardiology? Or were you looking for a different service?" This two-stage approach uses the LLM's broad language knowledge for initial matching while requiring explicit user confirmation before proceeding, ensuring that the service type in the final booking is accurate.

A service type lookup table maintains the authorized mapping between natural language service expressions and service system identifiers, including both English and Swahili common names for each service. This lookup table is a deterministic component that ensures consistent mapping regardless of how the LLM interprets a specific expression.

### 4.4.3 Date and Time Parsing

Date and time parsing in natural language is a specific technical challenge due to the variety of expressions users employ. Absolute dates ("January 15," "15th of next month," "2026-01-15"), relative dates ("next Tuesday," "in three weeks," "tomorrow"), time of day expressions ("morning," "afternoon," "10 AM," "2 PM," "lunchtime"), and Swahili date expressions all require parsing to extract structured date-time values.

The date-time parsing uses a combination of LLM interpretation for natural language expressions and deterministic validation of the resulting values. The LLM interprets relative expressions relative to the current date, converts natural language time expressions to specific hours (translating "morning" to 9:00 AM to 11:30 AM range, for example), and handles both English and Swahili date expressions. The resulting date-time values are validated deterministically: dates must be in the future, times must be within clinic hours (8:00 AM to 5:00 PM), and the combination must not fall on a day when the requested service is unavailable.

If parsing produces an ambiguous or out-of-range value, the system asks the user for clarification rather than making an assumption. "Did you mean next Tuesday, January 14th, or Tuesday in two weeks, January 21st?" This explicit disambiguation prevents booking errors caused by misinterpreted relative date references.

## 4.5 Multilingual Localization Engine

### 4.5.1 Language Detection and Context Tracking

Language detection operates at the conversation level rather than the message level. The system detects the user's preferred language at the start of each session based on the first substantive message and updates the language context if the user switches languages persistently. A single message in a different language (such as an English medical term in an otherwise Swahili conversation) does not trigger a language context switch; sustained use of a different language across two or more turns does.

Language detection uses a combination of LLM-based language identification and a list of common Swahili function words and common English function words that can be identified by simple string matching. This hybrid approach handles code-switched messages correctly: a message containing both English medical terms and Swahili conversational words is identified as Swahili-context (because the Swahili conversational structure dominates) rather than as English.

The detected language context is stored in session state and passed to every subsequent system component as a parameter, ensuring that all components have access to the same language context. This single-source-of-truth approach prevents inconsistencies that could arise if different components performed independent language detection.

### 4.5.2 Deterministic Localization of Transaction-Critical Outputs

Transaction-critical outputs, specifically appointment confirmations, error messages, and queue recommendation summaries, are generated through deterministic localization templates rather than through LLM generation. This is the key architectural decision that addresses the language drift problem.

For each transaction-critical message type, two templates exist: one in English and one in Swahili. The template selection is determined by the session language context stored in the session state. When a booking confirmation must be generated, the confirmation template in the appropriate language is populated with the booking details (service name localized, date and time formatted appropriately for the language, location description, patient instructions) and returned as the confirmation message. The LLM is not involved in generating the confirmation text; it is assembled deterministically.

Service type labels are maintained in a bilingual lookup table that maps each service identifier to both its English name and its Swahili name. When service names appear in confirmations or recommendations, the appropriate language version is retrieved from this table based on the session language context.

Appointment type labels (for example, labels distinguishing first appointments from follow-up appointments) are similarly maintained in a bilingual table. Error messages for all defined error conditions are pre-written in both languages and selected based on language context.

### 4.5.3 Conversational Language Consistency

Beyond transaction-critical outputs, the system maintains language consistency in conversational responses through LLM prompting. The system prompt includes explicit instruction to respond in the user's language, and the detected language context is included in each LLM call. This approach is sufficient for conversational exchanges, where some variation is acceptable, but is not relied upon for transaction-critical outputs where exact consistency is required.

In practice, LLM language consistency in conversational exchanges is high when the language context is clearly established and the conversation is conducted consistently in one language. The LLM will follow the language context instruction for the vast majority of conversational turns. The deterministic localization for transaction-critical outputs adds a safety layer that guarantees consistency in the messages where correctness is most important.

## 4.6 Queue Prediction and Recommendation Subsystem

### 4.6.1 Congestion Prediction Model

The queue prediction model is implemented as a deterministic scoring function that estimates expected congestion for appointment slots based on three factors: service-type baseline congestion, time-of-day factor, and day-of-week factor.

Service-type baseline congestion reflects the general pattern that some services consistently have higher demand than others. General outpatient appointments, which see the broadest patient population, have higher baseline congestion than specialized services with smaller but more focused patient populations. These baseline values are set through expert estimation informed by publicly available patterns of appointment volume in East African tertiary hospitals and can be calibrated from actual hospital data in production deployment.

Time-of-day factors reflect the consistent pattern across most healthcare settings that early morning slots (8:00 AM to 10:00 AM) and mid-morning slots (10:00 AM to 12:00 PM) are the most congested, while early afternoon slots (1:00 PM to 3:00 PM) tend to be less congested, and late afternoon slots (3:00 PM to 5:00 PM) have variable congestion depending on service type. These factors are expressed as multipliers applied to the baseline congestion score.

Day-of-week factors reflect patterns where Mondays typically see higher demand as patients who delayed appointments over the weekend seek care, while mid-week days (Tuesday through Thursday) have more even distribution, and Fridays sometimes see lower demand for non-urgent services as patients prefer earlier-week appointments. Again, these factors are approximate and would be calibrated from actual hospital data in production.

The combined score is normalized to a scale of zero to one, where zero represents the lowest predicted congestion and one represents the highest. This normalized score is then mapped to a qualitative category (low, moderate, high) and to an estimated wait time range derived from the baseline wait time for the service type adjusted by the congestion score.

### 4.6.2 Recommendation Generation

The recommendation generation process takes a service type and optional date constraints as input, computes congestion scores for available slots in the specified period, ranks slots by ascending congestion (lowest congestion first), and returns the top five recommendations with their congestion scores, estimated wait times, and explanation text.

Each recommendation includes four elements: the slot date and time (in user-appropriate format for the detected language), the congestion level label (Low, Moderate, or High in English; Chini, Wastani, or Juu in Swahili), an estimated wait time range (expressed as "usually around X to Y minutes"), and a brief explanation (for example, "This slot is recommended because Wednesday afternoons typically have shorter waiting times at this clinic").

Recommendations are presented in the conversational interface as a structured list with the top recommendation highlighted. The user can select any of the presented options or ask for different options if none are suitable. This presentation supports informed choice without being directive: the recommendation is a suggestion with a rationale, not a constraint.

### 4.6.3 Handling Prediction Uncertainty

An important design commitment in the recommendation subsystem is honest communication about prediction uncertainty. The predictions are estimates based on historical patterns, not guarantees. Actual waiting times on any given day depend on factors that the system cannot predict: unexpected patient volume variations, staff absences, equipment issues, and other operational factors.

This uncertainty is communicated to users through disclaimer language in the recommendation presentation: "These estimates are based on typical patterns. Actual waiting times may vary based on clinic conditions on the day of your appointment." This disclaimer maintains transparency without undermining the utility of the recommendation: even uncertain predictions can guide better decisions if they are accurate on average, and honest uncertainty communication maintains user trust when actual waits differ from estimates.

## 4.7 Governance Controls Implementation

### 4.7.1 Scope Enforcement

Scope enforcement is implemented through a combination of system prompt instructions and intent classification logic. The system prompt explicitly prohibits the assistant from providing medical advice, clinical recommendations, or any health information beyond the administrative scope of appointment booking. The intent classifier, implemented in the LLM through few-shot examples in the system prompt, identifies when users are requesting clinical rather than administrative support.

When a clinical request is detected, the system responds with a scope redirect: acknowledging that it cannot help with clinical questions, explaining that it is an appointment scheduling assistant, and offering to help the user book an appointment with the appropriate specialist who can address their clinical question. This response pattern maintains helpful engagement with the user without overstepping the administrative scope.

### 4.7.2 Escalation Pathways

The system implements explicit escalation pathways for situations that exceed its capabilities or that involve potential safety concerns. Escalation is triggered by several conditions: repeated failed booking attempts (three consecutive failures in the same session), explicit user requests for human assistance ("Can I speak to someone?"), detection of emergency language ("I am very sick" or "This is urgent"), and technical errors that prevent normal operation.

Upon escalation trigger, the system provides the user with the hospital's phone number, walk-in hours, and a brief explanation of why the system is suggesting human assistance. The escalation message is generated in the user's language using a deterministic template. Escalation events are logged with the trigger condition and conversation context, enabling staff to review escalations and follow up with patients if necessary.

### 4.7.3 Audit Logging and Data Governance

The audit logging system captures all significant system events with sufficient detail to reconstruct the full history of any session upon review. Log records include session start and end, all user messages and system responses, intent classification results, entity extraction outcomes, tool invocations and results, state transitions, and error conditions. Each log record includes a timestamp, session ID, and event type, enabling chronological reconstruction and filtering by event type.

Data governance controls include automatic session data clearing at session end (patient details entered during booking are not persisted in the conversational interface beyond the session), separation of audit logs from patient-identifiable data where possible, and access control for audit log review (in the production governance framework, audit log access would be restricted to authorized administrative and IT staff).

## 4.8 Chapter Summary

This chapter has detailed the design and implementation of the AI-driven hospital appointment support artifact across five architectural layers. The design is guided by five foundational principles: separation of language understanding from transaction execution, deterministic control for high-risk transitions, minimal data capture, explainable recommendations, and policy-aware logging. The layered architecture separates concerns between interface, orchestration, intelligence, tools, and data, enabling independent development and testing of each layer.

The booking workflow design implements tolerant information collection that accepts user input in any order while enforcing completeness before execution. The multilingual localization engine combines LLM-based language understanding for conversational exchanges with deterministic template-based generation for transaction-critical outputs, addressing the language drift problem through architectural design rather than model instruction. The queue prediction and recommendation subsystem provides interpretable, honest congestion estimates that support informed patient choice without creating unrealistic expectations. The governance controls implement scope enforcement, escalation pathways, and comprehensive audit logging appropriate for healthcare deployment.

The following chapter presents evaluation results from systematic testing of this artifact across functional, reliability, multilingual consistency, and governance dimensions.
