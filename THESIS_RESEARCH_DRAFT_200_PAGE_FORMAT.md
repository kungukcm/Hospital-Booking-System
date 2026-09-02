# COVER PAGE

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Kung'u Kelvin Mathigi

Thesis for Master's Degree
2026

Department of Techno Convergence based on ICT Policy
Graduate School of Global Development and Entrepreneurship
Handong Global University

---

# TITLE PAGE (PAGE 1)

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Kung'u Kelvin Mathigi

Thesis for Master's Degree
2026

Department of Techno Convergence based on ICT Policy
Graduate School of Global Development and Entrepreneurship
Handong Global University

---

# TITLE PAGE (PAGE 2)

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

(Localized/Institutional Subtitle Placeholder)

Applied Research in Health Informatics, AI Governance, and Service Delivery Optimization

---

# SUBMISSION SENTENCE PAGE

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Academic Advisor: Professor [Advisor Name]

By

Kung'u Kelvin Mathigi

Department of Techno Convergence based on ICT Policy
Handong Global University

A thesis submitted to faculty of Handong Global University in partial fulfillment of the requirements for the degree of Master of Science in the Department of Techno Convergence based on ICT Policy.

November 2026

Approved by

Professor [Advisor Name]
Thesis Advisor

---

# APPROVAL PAGE

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Kung'u Kelvin Mathigi

Accepted in partial fulfillment of the requirements for the degree of Master of Science.

November 2026

Academic Advisor: Prof. [Advisor Name]
Member: Prof. [Committee Member 1]
Member: Prof. [Committee Member 2]

---

# ABSTRACT

## English Abstract

Healthcare systems in low- and middle-income countries continue to face persistent service bottlenecks caused by high patient volumes, limited specialist availability, fragmented communication channels, and manual appointment workflows. In Kenya, tertiary and referral facilities such as Kenyatta University Teaching, Referral and Research Hospital (KUTRRH) must manage both ordinary outpatient demand and complex specialist care while maintaining equitable access and clinical safety. This research presents a design science approach to developing and evaluating an AI-driven hospital assistant that supports patient-facing appointment interactions, multilingual communication, and queue-aware scheduling recommendations.

The artifact developed in this thesis is a conversational AI assistant implemented as a modular system with a Streamlit user interface, orchestration logic using LangGraph, language processing through a large language model (LLM), deterministic guardrails for critical booking states, and a tool layer for appointment operations. The assistant supports intent understanding for booking, cancellation, next-available appointment retrieval, and congestion-aware slot recommendations. It also integrates a predictive waiting-time mechanism for identifying low-, medium-, and high-congestion windows, enabling patients to make informed appointment-time decisions.

A key contribution of this research is the practical integration of multilingual support, specifically English and Swahili, at both policy and implementation levels. Rather than relying only on prompt instructions, the system enforces deterministic localization for high-risk transactional outputs such as booking confirmations and best-available-slot summaries. This hybrid pattern addresses known instability in pure generative tool-calling systems and increases reliability in user-critical interactions.

Evaluation was conducted through functional test suites, scenario-based walkthroughs, and implementation verification across booking flow states, including edge cases such as incomplete patient data, malformed service requests, date-only/time-only input, and tool-call failure recovery. Results indicate that deterministic transition rules materially improve system robustness by reducing invalid tool invocations, preventing stalled conversation states, and improving successful completion of end-to-end booking flows. Localization outcomes confirm that full Swahili transactional messaging can be enforced consistently when language context is detected.

This thesis contributes to design science in digital health by providing: (1) a reusable architecture for AI-enabled hospital booking assistants in resource-constrained settings, (2) a practical reliability framework for combining LLM flexibility with deterministic control logic, and (3) policy-relevant guidance for trustworthy deployment, including transparency, data governance, linguistic inclusion, and human oversight. The findings support a phased implementation strategy for Kenyan hospitals that balances innovation with safety, accountability, and patient-centered service quality.

Keywords: healthcare chatbot, queue optimization, design science research, multilingual AI, hospital scheduling, Swahili localization, ICT policy, Kenya.

---

# ACKNOWLEDGEMENTS

I thank God for strength and guidance throughout this research journey. I extend sincere appreciation to my academic advisor, committee members, and faculty at Handong Global University for their mentorship and critical feedback. I am grateful to colleagues and peers whose technical and policy discussions sharpened this work. Special appreciation is extended to healthcare practitioners and stakeholders in Kenya whose practical realities inspired this study. Finally, I thank my family for their unwavering support.

---

# TABLE OF CONTENTS

Abstract
Acknowledgements
List of Figures
List of Tables

Chapter 1. Introduction
Chapter 2. Literature Review
Chapter 3. Research Methodology
Chapter 4. System Design and Implementation
Chapter 5. Results and Evaluation
Chapter 6. Discussion
Chapter 7. Conclusion and Recommendations
References
Appendices

---

# LIST OF FIGURES

Figure 1. Design science research cycle used in this thesis
Figure 2. High-level architecture of the AI hospital assistant
Figure 3. Booking flow state transitions with deterministic gates
Figure 4. Tool invocation and synthesis loop in LangGraph
Figure 5. Localization pipeline for English-Swahili outputs
Figure 6. Congestion-aware scheduling decision process
Figure 7. Deployment topology options

---

# LIST OF TABLES

Table 1. Research objectives and corresponding evaluation metrics
Table 2. Functional modules and implementation artifacts
Table 3. Test scenarios and expected outcomes
Table 4. Reliability risks and mitigation controls
Table 5. Ethical, legal, and policy compliance matrix
Table 6. Comparative strengths and limitations of chatbot approaches

---

# CHAPTER 1. INTRODUCTION

## 1.1 Background and Context

The digital transformation of healthcare has accelerated globally, but practical implementation in many public and referral systems remains uneven. In Kenya, healthcare facilities serve diverse patient populations with varying digital literacy levels, language preferences, and access constraints. Administrative congestion in appointment scheduling contributes to longer waiting times, poor patient communication, and inefficient use of specialist time. While chatbot systems have matured in customer service and education contexts, safe and reliable adaptation for healthcare operations requires stronger controls than generic conversational systems.

This thesis addresses a practical challenge: how to design and evaluate a trustworthy AI assistant that can facilitate appointment booking and queue-informed guidance while respecting local policy, ethical constraints, and multilingual realities. The study focuses on a project artifact developed as a hospital booking assistant with AI support for natural-language interaction and predictive scheduling recommendations.

## 1.2 Problem Statement

Conventional hospital appointment workflows often involve fragmented communication channels (phone, in-person desk queues, ad hoc digital forms), leading to delays, data inconsistency, and avoidable congestion. Existing AI chat interfaces can interpret user intent, but in healthcare scheduling they may produce unstable behavior during tool calls, especially where strict data requirements exist (patient ID, contact details, appointment type, date, time). These failures can cause invalid requests, incomplete transactions, and user frustration.

The core research problem is therefore:

How can a hospital-facing AI assistant be designed to deliver reliable, multilingual, and congestion-aware appointment support in a Kenyan referral-hospital context while preserving safety, accountability, and usability?

## 1.3 Research Aim

To design, implement, and evaluate an AI-driven patient support and scheduling artifact that improves booking reliability and queue-awareness through a hybrid architecture combining LLM reasoning with deterministic booking controls.

## 1.4 Research Objectives

1. To develop a modular AI assistant architecture for hospital appointment support.
2. To implement deterministic guardrails for critical booking states to reduce invalid transactions.
3. To integrate congestion-aware scheduling recommendations into appointment selection.
4. To support bilingual conversational interaction (English and Swahili), including localized transactional outputs.
5. To evaluate functional reliability, user-flow completeness, and policy implications for deployment in Kenya.

## 1.5 Research Questions

1. What architecture best balances conversational flexibility and transactional reliability for hospital booking?
2. How does deterministic flow control affect booking completion and error reduction?
3. How can queue-prediction insights be operationalized for patient-facing slot recommendations?
4. What implementation approach ensures consistent multilingual outputs in high-stakes booking messages?
5. What governance, ethics, and ICT policy considerations are required for production deployment?

## 1.6 Scope of the Study

This study focuses on non-diagnostic patient support for appointment operations. It excludes clinical diagnosis, medical triage decisions, and direct treatment recommendations. The implemented system supports: booking, cancellation, next-appointment retrieval, and best-available-slot recommendation with congestion estimates. The case context is aligned with KUTRRH operational realities; however, direct institutional production deployment is outside this thesis scope.

## 1.7 Significance of the Study

The significance is threefold:

1. Practical significance: demonstrates an implementable model for reducing booking friction and congestion blind spots.
2. Methodological significance: contributes a design pattern for combining LLMs with deterministic constraints in healthcare workflows.
3. Policy significance: provides guidance for multilingual inclusion, data governance, and accountable AI deployment in Kenyan health systems.

## 1.8 Definition of Key Terms

AI Assistant: A software agent using natural language processing and workflow logic to support user tasks.

Deterministic Guardrail: Explicit rule-based logic that constrains transition or action in a workflow regardless of model output.

Queue Optimization: Process of reducing waiting-time burden through scheduling decisions informed by predicted congestion.

Transactional Localization: Consistent translation of operationally important outputs (booking confirmations, slot options) into user language context.

## 1.9 Organization of the Thesis

Chapter 1 introduces the study context and problem. Chapter 2 synthesizes relevant literature. Chapter 3 explains the research design and methods. Chapter 4 presents artifact architecture and implementation details. Chapter 5 reports evaluation outcomes. Chapter 6 discusses implications for theory, practice, and policy. Chapter 7 concludes with recommendations and future work.

---

# CHAPTER 2. LITERATURE REVIEW

## 2.1 Introduction

This chapter reviews prior work on healthcare chatbots, AI-enabled service automation, queue-aware systems, multilingual interaction, and ethical governance. The review draws from the references provided in the project repository and identifies a research gap addressed by this thesis.

## 2.2 Evolution of Chatbots in Service Delivery

Chatbots have evolved from rule-based scripted interfaces to data-driven and transformer-based conversational systems. Studies on customer service chatbots indicate gains in responsiveness, 24/7 availability, and cost reduction, but also recurring issues around trust, escalation handling, and domain specificity [R7, R11, R24, R27]. Public-sector communication literature suggests chatbot adoption can improve citizen access where processes are repetitive and informationally structured, provided accountability and transparency safeguards are present [R5].

In health contexts, the stakes are higher. The literature on biomedical and telemedicine chatbots emphasizes that user experience and workflow integration matter as much as linguistic fluency [R16, R23]. Systems that fail gracefully and route exceptions effectively perform better than those optimized only for open-ended conversation quality.

## 2.3 Healthcare Chatbots: Capabilities and Boundaries

Health chatbot studies identify common use cases: symptom guidance, mental-health support, appointment assistance, patient education, and medication reminders [R3, R14, R15, R17, R22]. Mental-health chatbot literature reports potential for engagement and accessibility, but warns that emotional safety, escalation paths, and context-sensitive language are critical [R3, R14, R17].

For appointment workflows, practical utility depends on data precision and transaction completion. A chatbot that engages users conversationally but fails at final booking can degrade trust faster than no chatbot at all. Thus, research increasingly emphasizes measurable process outcomes: completion rates, error rates, turnaround time, and user confidence [R21].

## 2.4 LLM-Based Chatbots and Reliability Concerns

LLM-based systems expand language flexibility and reduce intent-classification rigidity. However, literature and technical analyses repeatedly note limitations in factual consistency, tool-call robustness, and deterministic compliance [R13, R26]. In structured workflow domains, hallucinations and malformed action calls may cause operational failures. Reliability-oriented architecture patterns recommend combining model reasoning with explicit constraints, validation layers, and fallback logic.

This thesis adopts that principle by implementing deterministic gates in booking flow states. The design recognizes that LLMs excel at natural interaction but should not unilaterally control transactional side effects.

## 2.5 Patient Engagement and Trust Factors

Patient engagement studies show that clarity, empathy, responsiveness, and perceived control shape sustained use of digital health services [R15, R11]. Confusing instructions, language mismatch, and inconsistent confirmations reduce confidence. In multilingual settings, transactional language consistency is especially important because misinterpretation can alter appointment outcomes.

The present artifact addresses this through explicit bilingual policy and deterministic localization for final outputs. This extends beyond interface translation and targets operational correctness in user-visible confirmations.

## 2.6 Queue Optimization and Scheduling Intelligence

Queue management in healthcare has long relied on administrative heuristics and static schedules. AI-enhanced approaches can leverage historical patterns to predict congestion and recommend lower-wait slots. Research on technical metrics for healthcare chatbots highlights the need to evaluate not only language quality but process efficiency and service impact [R21].

By presenting best available slots with congestion levels and predicted wait times, the developed artifact introduces decision support directly at the booking moment. This bridges conversational UX and operational optimization.

## 2.7 Ethical and Policy Considerations

Ethics literature in health AI underscores privacy, fairness, transparency, explainability, and non-maleficence [R9, R12]. Privacy-compliant agent frameworks stress secure data handling, role boundaries, and explicit consent mechanisms [R12]. Governance-oriented works caution against deploying persuasive AI without clear accountability and escalation protocols [R5, R9].

In Kenya, digital health policy priorities include equitable access, inclusion of local languages, data protection compliance, and interoperability readiness. A deployment-ready chatbot strategy should therefore include policy controls for logging, retention, auditability, and safe human handoff.

## 2.8 Research Gap

The reviewed literature reveals gaps at the intersection of:

1. multilingual transactional reliability;
2. deterministic workflow controls in LLM chatbots;
3. patient-facing queue prediction integration;
4. policy-grounded deployment frameworks for low-resource hospital settings.

Most studies discuss these dimensions separately. This thesis contributes an integrated artifact and evaluation strategy that operationalizes all four dimensions in one design science cycle.

## 2.9 Conceptual Framework

The conceptual model used in this thesis links six constructs:

1. Conversational Accessibility (natural language and multilingual support)
2. Transactional Reliability (guardrails and validation)
3. Scheduling Intelligence (queue prediction and slot ranking)
4. User Trust (clear confirmations and recoverable flows)
5. Operational Efficiency (reduced friction and better slot distribution)
6. Governance Readiness (ethics, policy, logging, escalation)

Hypothesized relationship: improved transactional reliability and localization quality mediate the effect of conversational AI on user trust and completion outcomes.

---

# CHAPTER 3. RESEARCH METHODOLOGY

## 3.1 Research Paradigm

This study follows the Design Science Research (DSR) paradigm, suitable for problems that require creating and evaluating purposeful artifacts in context. DSR aligns with this thesis because the objective is not only to describe current scheduling challenges but to build and assess a working AI solution.

## 3.2 Design Science Process

The study follows an iterative process:

1. Problem identification and motivation
2. Objective definition
3. Design and development of artifact
4. Demonstration in realistic scenarios
5. Evaluation against functional and quality criteria
6. Communication of results and implications

## 3.3 Case Context

The case context is Kenyan hospital service environments with emphasis on referral-level complexity. KUTRRH is used as the motivating institution due to its specialist service profile and public-facing demand pressures. The artifact is developed as a prototype-ready system that reflects operational realities but does not claim formal institutional rollout within this thesis timeline.

## 3.4 Data and Inputs

Data inputs include:

1. System design requirements inferred from appointment operations and patient communication needs.
2. Project implementation artifacts (codebase modules, logs, test reports).
3. Literature-based design constraints and quality indicators from provided references.

The queue model in the prototype uses predictive outputs to estimate congestion categories and waiting-time ranges for slot recommendations.

## 3.5 Artifact Components

The artifact includes:

1. Streamlit interface for patient conversation
2. LangGraph orchestrator for message-state transitions
3. LLM integration for intent understanding and responses
4. Tool layer for booking operations
5. Deterministic parsers for service/date/time extraction
6. Localization and translation layer for transactional outputs
7. Logging and error handling subsystem

## 3.6 Evaluation Design

Evaluation applies mixed technical validation methods:

1. Functional test cases for all core booking operations
2. Scenario walkthroughs for edge-case handling
3. Reliability checks for malformed inputs and tool-call errors
4. Localization verification for English/Swahili outputs
5. Deployment readiness checklist review

### 3.6.1 Key Evaluation Metrics

1. Booking completion success (state progression to confirmed booking)
2. Invalid transaction prevention (guardrail effectiveness)
3. Flow recovery quality (error messaging and fallback behavior)
4. Localization consistency in high-stakes outputs
5. Operational intelligibility (clarity of slots and congestion messaging)

## 3.7 Validity and Trustworthiness

Construct validity is strengthened by mapping each objective to a measurable artifact behavior. Internal validity is supported by deterministic guardrails that isolate causal effects in workflow reliability. External validity is limited by single-case context and prototype scope, but transferability is improved through modular architecture and policy-focused documentation.

## 3.8 Ethical Considerations

The artifact is a non-diagnostic administrative assistant and intentionally avoids clinical decision-making. Recommended deployment controls include:

1. explicit disclosure that assistant is not a clinician;
2. data minimization for booking fields;
3. secure storage and access policies;
4. escalation to human staff where ambiguity persists;
5. clear opt-out and correction pathways.

---

# CHAPTER 4. SYSTEM DESIGN AND IMPLEMENTATION

## 4.1 Architectural Overview

The system architecture is layered:

1. Presentation Layer: Streamlit chat interface.
2. Orchestration Layer: State graph managing turn flow.
3. Intelligence Layer: LLM for language interpretation.
4. Tool Layer: Deterministic operations for booking logic.
5. Data Layer: Appointment persistence and analytics records.

The architecture enforces separation of concerns: language flexibility is kept distinct from transactional execution.

## 4.2 Core Implementation Modules

### 4.2.1 app.py

Provides the web interface, session-state conversation persistence, and invocation hooks to the agent workflow.

### 4.2.2 agent.py

Implements:

1. state transitions;
2. booking-flow detection;
3. deterministic parsing and guardrails;
4. tool-call orchestration;
5. localized response synthesis.

### 4.2.3 enhanced_tools.py

Provides operational tools:

1. book_appointment
2. get_optimal_appointment_slots
3. suggest_alternative_slots
4. get_wait_time_prediction
5. get_least_busy_times
6. get_busiest_times
7. cancel_appointment

### 4.2.4 appointments_db.py

Handles persistent storage and conflict checks for appointment records.

### 4.2.5 scheduling_model.py and appointment_recommender.py

Support predictive and prescriptive logic for congestion-aware recommendations.

## 4.3 Booking Flow and Deterministic Guardrails

A central challenge in LLM-driven transactional systems is unstable transition handling when user responses are short or ambiguous. The implementation addresses this with deterministic checks:

1. Validate mandatory patient details before final booking.
2. Detect service-only input and prompt for date.
3. Detect date-only input and return best slots.
4. Detect time-only input and complete booking with stored context.
5. Reject generic booking phrases as appointment types.

This logic reduces malformed tool calls and prevents stalled interactions.

## 4.4 Localization Strategy

Localization uses a dual mechanism:

1. Prompt-level instruction to mirror user language.
2. Code-level deterministic translation for critical outputs.

This second mechanism ensures Swahili consistency in:

1. final booking confirmation block;
2. best available slot recommendations;
3. appointment-type value translation;
4. follow-up action prompts.

This design addresses a common multilingual failure mode where language drifts at final transactional steps.

## 4.5 Error Handling and Resilience

The system includes robust fallback behavior:

1. retries for specific tool-call schema failures;
2. user-friendly responses for rate-limit events;
3. deterministic alternatives when model uncertainty is high;
4. structured logging for diagnosis.

## 4.6 Deployment Readiness

Deployment artifacts include Docker configuration, cloud deployment guides, runtime configuration, and security checklists. The prototype is suitable for staged pilot deployment after institutional compliance review.

---

# CHAPTER 5. RESULTS AND EVALUATION

## 5.1 Introduction

This chapter presents technical and process-oriented findings from artifact testing, emphasizing reliability, localization consistency, and queue-aware support outcomes.

## 5.2 Functional Testing Outcomes

Project test artifacts indicate broad operational coverage across booking, cancellation, conflict detection, wait prediction, and slot recommendations. End-to-end flow tests show that users can complete appointment operations through natural-language interaction with system-generated confirmations.

### 5.2.1 Booking and Confirmation

Observed outcomes demonstrate:

1. successful booking record creation with identifiers;
2. predicted waiting-time and congestion annotation;
3. conflict warning when overlap exists;
4. status persistence across sessions.

### 5.2.2 Slot Recommendation Quality

The best-available-slots function returns ranked options by predicted waiting burden and daily analytics indicators. This supports patient decision-making and can distribute demand away from peak windows.

### 5.2.3 Cancellation and Retrieval

Cancellation by appointment ID or patient name is supported, with state updates and traceable confirmation details.

## 5.3 Reliability Improvements from Deterministic Logic

A major finding is the reliability gain from deterministic flow controls layered over LLM outputs. Before guardrails, short replies and tool-schema mismatches could cause invalid requests or silent stalls. After introducing explicit parsing and sequence gates:

1. booking progression became predictable;
2. invalid call attempts decreased in practical scenarios;
3. user guidance became clearer at each stage.

## 5.4 Multilingual Evaluation

The system supports English and Swahili conversations. Validation confirms that final transactional messages can be consistently enforced in Swahili when context indicates Swahili interaction. Importantly, this includes:

1. booking confirmation headings and labels;
2. best available slots heading and analytics labels;
3. localized appointment-type values (example: Dentistry -> Udaktari wa Meno).

## 5.5 User-Flow Robustness Scenarios

### Scenario A: Service-only Response

Input: service name only
Outcome: system prompts for preferred date and continues flow.

### Scenario B: Date-only Response

Input: preferred date only
Outcome: system infers recent service and presents optimized slots.

### Scenario C: Time-only Response

Input: selected time only
Outcome: system uses stored context and books appointment.

### Scenario D: Missing Patient Details

Input: booking progression without required identifiers
Outcome: system blocks booking and requests mandatory details.

These scenarios illustrate controlled state transitions that improve transactional safety.

## 5.6 Discussion of Operational Value

The artifact demonstrates potential value for hospital operations:

1. Reduced front-desk communication burden for routine appointment requests.
2. Improved patient visibility into waiting-time implications.
3. Better consistency in confirmation and follow-up messages.
4. Inclusion benefits through Swahili support.

## 5.7 Limitations of Evaluation

1. Evaluation reflects prototype and controlled scenarios rather than full clinical production load.
2. Queue predictions are model-dependent and require local calibration with institutional historical data.
3. Formal user acceptance studies with patients and staff are recommended in future phases.

---

# CHAPTER 6. DISCUSSION

## 6.1 Theoretical Contributions

This thesis contributes to digital health design science by showing that LLM-enabled assistants in healthcare should be architected as hybrid systems rather than pure conversational agents. Deterministic constraints are not merely implementation details; they are core design mechanisms for trust in high-consequence administrative workflows.

## 6.2 Practical Contributions

Practical contributions include:

1. a reusable booking assistant architecture;
2. a deterministic flow-control pattern for reliable transactions;
3. multilingual transactional localization strategy;
4. queue-aware slot recommendation integration.

These patterns can be adapted to outpatient clinics, specialist departments, and telehealth scheduling desks.

## 6.3 ICT Policy and Governance Implications for Kenya

AI-enabled hospital assistants should align with policy principles:

1. Human-centered service access
2. Data protection and purpose limitation
3. Transparency and explainability in user communication
4. Non-discrimination and language inclusion
5. Accountability through logging and audit trails

A policy-aligned deployment roadmap should include governance committees, risk classification, incident reporting workflows, and periodic model-behavior audits.

## 6.4 Ethical Reflection

Ethically, the artifact remains administrative and avoids diagnosis. This boundary is intentional and should be preserved in production governance. Patients must always know when they are interacting with AI, what data is being stored, and how to reach human staff.

## 6.5 Design Principles Derived from the Study

1. Keep language generation and transactional execution separate.
2. Make critical transitions deterministic.
3. Treat multilingual support as operational reliability, not UI cosmetics.
4. Build for graceful failure and human handoff.
5. Evaluate success by completion, clarity, and safety, not only fluency.

## 6.6 Future Research Directions

1. Multi-hospital pilot studies with comparative outcomes.
2. Real-world impact analysis on waiting-time distribution.
3. Formal usability and trust studies across language groups.
4. Integration with national digital health interoperability frameworks.
5. Advanced fairness audits across demographics and service lines.

---

# CHAPTER 7. CONCLUSION AND RECOMMENDATIONS

## 7.1 Conclusion

This thesis addressed a pressing healthcare operations challenge: reliable, patient-centered appointment support in environments with high demand and constrained administrative capacity. Using a design science approach, the study developed and evaluated a hybrid AI artifact that combines LLM conversational capability with deterministic booking controls and queue-aware scheduling assistance.

The results show that reliability in healthcare administrative AI is improved when high-risk workflow steps are explicitly constrained and validated. The artifact demonstrates practical feasibility for multilingual, congestion-informed appointment support and provides a replicable blueprint for institutions aiming to modernize patient access pathways.

## 7.2 Recommendations for Hospital Practice

1. Deploy in phased pilots (single department first) with continuous monitoring.
2. Maintain explicit non-clinical boundaries and human escalation options.
3. Require deterministic validation for all transaction-critical fields.
4. Monitor language consistency and user comprehension in multilingual deployments.
5. Establish governance for logs, privacy, and incident response before scaling.

## 7.3 Recommendations for Policy and Regulators

1. Develop sector-specific guidelines for conversational AI in healthcare administration.
2. Encourage multilingual service standards for digital public-health interfaces.
3. Require auditability and error reporting for AI-assisted booking systems.
4. Support interoperability and secure data-sharing standards.

## 7.4 Final Statement

AI can improve healthcare access workflows when designed with humility, control, and public-interest governance. In this thesis, the combination of conversational intelligence, deterministic safeguards, and policy-aware design demonstrates a viable path toward trustworthy AI-enabled appointment support in Kenya.

---

# REFERENCES (FROM PROVIDED FOLDER)

[R1] A Framework for Chatbots in Medical Practice. Source file: A_Framework_for_Chatbots_in_Medical_Pre.pdf.

[R2] A Literature Survey of Recent Advances in Chatbots. Source file: A_Literature_Survey_of_Recent_Advances_i.pdf.

[R3] AI Powered Chatbots for Mental Health Support. Source file: AI_powered_Chatbots_for_Mental_Health_Su.pdf.

[R4] Bibliometric Analysis of Chatbots in Healthcare. Source file: Bibliometric_Analysis_of_Chatbots_in_Hea.pdf.

[R5] Chatbots and Government Communications. Source file: Chatbots_and_Government_Communications_i.pdf.

[R6] Chatbots as a New User Interface for Process Automation. Source file: Chatbots_as_a_new_user_interface_for_pro.pdf.

[R7] Chatbots for Brand Representation in Communication. Source file: Chatbots_for_Brand_Representation_in_Com.pdf.

[R8] Chatbots in Airport Customer Service Experience. Source file: Chatbots_in_Airport_Customer_Service_Exp.pdf.

[R9] Ethical Considerations in Using Artificial Intelligence. Source file: Ethical_considerations_in_using_artifici.pdf.

[R10] Developing Chatbots in the Field of Health. Source file: Developing_chatbots_in_the_field_of_heal.pdf.

[R11] Ensuring Consumer Satisfaction with Chatbots. Source file: Ensuring_Consumer_Satisfaction_with_Chat.pdf.

[R12] EREBOTS Privacy-Compliant Agent-Based Platform. Source file: EREBOTS_Privacy_Compliant_Agent_Based_Pl.pdf.

[R13] Understanding the Limitations of AI Chatbots. Source file: Understanding_the_Limitations_of_AI_Chat.pdf.

[R14] Exploring the Potential of Chatbots in Mental Health (Version 1). Source file: Exploring_the_Potential_of_Chatbots_in_M.pdf.

[R15] Factors Influencing Patient Engagement in Digital Health Chatbot Use. Source file: Factors_influencing_patient_engagement_i.pdf.

[R16] Natural Language Chatbots in Biomedical Contexts. Source file: Natural_Language_Chatbots_in_Biomedical.pdf.

[R17] Proposed Use of Chatbots in Mental Health. Source file: Proposed_Use_of_Chatbots_in_Mental_Healt.pdf.

[R18] Revolutionizing e-Health: Transformative Roles of Chatbots. Source file: Revolutionizing_e_health_the_transformat.pdf.

[R19] Technical Metrics Used to Evaluate Health Chatbots. Source file: Technical_Metrics_Used_to_Evaluate_Healt.pdf.

[R20] The Evolving Role of Virtual Health Assistants. Source file: The_Evolving_Role_of_Virtual_Health_Assi.docx.

[R21] The Health Chatbots in Telemedicine Integration. Source file: The_Health_ChatBots_in_Telemedicine_Inte.pdf.

[R22] Empathic Response Generation in Chatbots. Source file: Empathic_Response_Generation_in_Chatbots.pdf.

[R23] Understanding How Chatbots Work: An Exploratory Perspective. Source file: Understanding_How_Chatbots_Work_An_Explo.pdf.

[R24] The Role of Chatbots in Enhancing Customer Service. Source file: The_Role_of_Chatbots_in_Enhancing_Custom.pdf.

[R25] Use of Chatbots for Customer Service in [Industry Context]. Source file: Use_of_chatbots_for_customer_service_in.pdf.

[R26] LLM-Based Chatbots in Language Learning. Source file: LLM_Based_Chatbots_in_Language_Learning.pdf.

[R27] Exploring the Potential of Chatbots in Mental Health (Version 2). Source file: Exploring_the_Potential_of_Chatbots_in_M (1).pdf.

---

# APPENDIX A. SYSTEM ARCHITECTURE NARRATIVE

The implemented system follows a graph-based orchestration model where each user turn enters an agent node, transitions to tools when actionable calls are present, and returns to synthesis for user-ready messaging. Deterministic branches intercept critical booking states to prevent malformed requests and force prerequisite collection of patient details.

---

# APPENDIX B. BOOKING FLOW LOGIC (SUMMARY)

1. User intent enters booking mode.
2. Mandatory details are validated.
3. Appointment type is confirmed.
4. Preferred date is parsed.
5. Best slots are presented with congestion indicators.
6. User-selected time triggers booking tool.
7. Confirmation is localized and returned.

---

# APPENDIX C. MULTILINGUAL LOCALIZATION LOGIC (SUMMARY)

1. Detect language context from recent conversation turns.
2. Apply localized prompts for guidance messages.
3. Force deterministic translation of high-risk transactional outputs.
4. Translate appointment-type values for full output consistency.
5. Preserve audit logs in original and translated forms where needed.

---

# APPENDIX D. RECOMMENDED 200-PAGE EXPANSION PLAN

To reach a full institutional 200-page submission, expand this manuscript with:

1. Full chapter-by-chapter empirical evidence tables.
2. Detailed source-by-source literature synthesis matrix.
3. Full methodology instruments and coding protocol.
4. Extended scenario transcripts and error taxonomies.
5. Policy crosswalk against Kenyan and institutional frameworks.
6. Additional appendices: deployment guides, test scripts, and trace logs.

Suggested chapter page targets:

1. Front matter: 12 pages
2. Chapter 1: 20 pages
3. Chapter 2: 55 pages
4. Chapter 3: 28 pages
5. Chapter 4: 30 pages
6. Chapter 5: 28 pages
7. Chapter 6: 15 pages
8. Chapter 7: 8 pages
9. References and appendices: 24 pages

Total: 220 pages (editable downward to 200 pages based on final formatting and committee guidance).
