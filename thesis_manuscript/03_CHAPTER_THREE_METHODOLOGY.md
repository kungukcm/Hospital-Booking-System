# CHAPTER 3. RESEARCH METHODOLOGY

## 3.1 Introduction

This chapter describes the research methodology used to design, develop, and evaluate the AI-driven hospital assistant artifact. The study adopts a design science approach, which is well suited for solving practical problems through purposeful artifact creation and iterative evaluation. Rather than asking only whether something exists in nature or society, design science asks how to create something that does not yet exist but should, in order to solve a real-world problem. This approach is particularly appropriate for healthcare technology research where practical implementation and real-world utility are paramount concerns.

The methodology in this thesis integrates design science scholarship with health informatics evaluation practices and software engineering discipline. The result is a rigorous but pragmatic approach that produces both a working artifact and documented learning about the design process itself.

## 3.2 Research Philosophy and Paradigm

The philosophical orientation of this thesis is pragmatism, combined with elements of critical realism about technology and social systems. Pragmatism emphasizes that research should solve real problems and produce knowledge that is useful in practice. Rather than asking only abstract theoretical questions, pragmatist research asks: "Does this work? For whom? Under what conditions? And how can we improve it?"

Critical realism acknowledges that systems like hospitals are complex social entities with independent existence, not just constructions of researchers' minds. However, technologies like chatbots are socially constructed artifacts created for purposes defined by humans. The design science approach respects both realities by focusing on artifacts that work within real institutional contexts while acknowledging that their success depends on human choices, adoption, and integration.

The philosophical stance adopted in this thesis is that:

1. Practical problems in healthcare warrant rigorous scholarship, not just engineering
2. Artifacts can be studied scientifically, documenting both what works and why it works
3. Multiple types of knowledge—theoretical, practical, procedural—are valuable
4. Real-world constraints should inform research design, not be eliminated from it
5. Both internal validity (does it work in controlled conditions) and external validity (could it work elsewhere) matter, though in different ways

## 3.3 Design Science Research Framework

The study follows an established six-step design science research process adapted from Peffers et al. (2007) and aligned with recent design science practice in information systems:

**Step 1: Problem Identification and Motivation.** The thesis begins with documented problems in hospital scheduling: transactional failures when users provide partial input, opacity around queue congestion, and inconsistent language support. These problems were identified through literature review, discussion of practical healthcare IT challenges, and articulation of gaps between what healthcare systems need and what existing chatbots provide.

**Step 2: Definition of Solution Objectives.** From the identified problems, specific objectives were defined: develop an architecture that combines LLM flexibility with deterministic transaction control, implement reliable booking completion under realistic conversational conditions, design queue-aware recommendations that are interpretable to users, maintain language consistency through transaction completion, and establish governance-ready design practices suitable for institutional deployment.

**Step 3: Design and Development of Artifact.** The artifact was developed iteratively across five major design cycles, each introducing new capabilities or refinements. The artifact consists of interconnected subsystems: conversational interface, semantic understanding, workflow orchestration, transaction execution, queue analysis, and governance controls. Each component was designed with explicit consideration of how it interfaces with other components and how failures in one component affect the whole system.

**Step 4: Demonstration in Realistic Scenarios.** Rather than testing in artificial laboratory conditions, the demonstration involved realistic usage scenarios that reflected actual patient booking challenges: users providing partial information, using colloquial language for services, selecting dates without times, and switching between languages mid-session. These scenarios were developed based on literature and practical experience, then systematically executed to show what the system can and cannot do.

**Step 5: Evaluation Against Pre-defined Criteria.** Evaluation examined whether the artifact met its specified objectives. Did it reliably complete bookings? Did recommendations improve slot selection? Did it maintain language consistency? Did it provide adequate governance controls? Evaluation combined quantitative metrics (completion rates, error rates) with qualitative assessment of user experience and institutional readiness.

**Step 6: Communication of Findings and Implications.** This thesis communicates not only the artifact and its performance but also the design knowledge generated through the process. What design patterns emerged? What trade-offs were made? What governance implications arose? What would future systems need to do differently?

## 3.4 Research Design and Approach

The overall research design is iterative and artifact-centered. The system was not designed once and then tested; instead, it evolved through multiple design cycles, with each cycle building on lessons from the previous iteration.

### 3.4.1 Design Iteration Cycles

The five major iteration cycles addressed different design challenges:

**Iteration 1: Baseline Conversational Booking.** The first cycle implemented basic conversational booking: understanding user requests in natural language, capturing required details, and executing booking commands. This cycle established whether conversational understanding was viable in the domain and what basic interface patterns were needed.

**Iteration 2: Tool-Call Stability and Schema Simplification.** Once basic conversation worked, the challenge became reliable tool invocation. Early attempts suffered from malformed parameters, missing required fields, and schema violations. This cycle simplified tool schemas, added parameter validation, and implemented pre-execution checks to prevent invalid tool calls from reaching the backend system.

**Iteration 3: Deterministic Booking-State Controls.** The third cycle addressed flow stability. When users provided input in unexpected orders (date before service, time without date), the system became confused about what to ask next. This cycle introduced a deterministic state machine that defined valid transitions and mandatory information prerequisites, regardless of conversational order.

**Iteration 4: Multilingual Support and Localization Consistency.** The fourth cycle implemented language support. Initial multilingual attempts maintained language in conversational exchanges but reverted to English in final confirmations. This cycle enforced language context detection, localized booking confirmation labels, and translated appointment-type values to ensure language consistency end-to-end.

**Iteration 5: End-to-End Validation and Governance Framing.** The final cycle integrated all components, tested complex scenarios combining multiple challenges (mixed language, partial input, error recovery), and explicitly documented governance implications and safeguards.

### 3.4.2 Validation Gates Between Iterations

Each iteration included internal validation before proceeding. Acceptance criteria included: no regressions in previous functionality, new features working reliably in test scenarios, code quality standards met, and documentation adequate for maintenance.

## 3.5 Case and Setting

The research case reflects referral-hospital scheduling needs in Kenya, with practical alignment to Kenyatta University Teaching, Referral and Research Hospital (KUTRRH) service realities. KUTRRH is a 500+ bed tertiary teaching and referral facility serving Central Kenya and beyond, with diverse departments, high outpatient demand, and the communication challenges characteristic of high-volume referral centers.

The artifact is evaluated as a prototype in controlled conditions, not under live institutional deployment. Controlled conditions allowed rigorous testing of edge cases and error recovery without risk of affecting real patient care. However, scenarios were designed to be realistic—using actual appointment type names, realistic patient detail patterns, and operational assumptions grounded in hospital workflow.

## 3.6 Artifact Description and Scope

The artifact consists of seven integrated subsystems:

**Frontend Conversational Interface.** A web-based chat interface (built with Streamlit) where patients type requests in natural language. The interface is simple and accessible, with no menus or forms to navigate.

**Orchestration Graph for Workflow Management.** A state machine that defines valid transitions through the booking process: initial request interpretation → service clarification → date selection → time selection → confirmation. This graph ensures the system does not attempt to book without required information, regardless of conversational order.

**LLM-Powered Language Understanding.** An LLM (Claude 3.5) that interprets user requests, detects intent, extracts key entities (service, date, time), and generates conversational responses. The LLM handles linguistic flexibility that deterministic parsers cannot.

**Deterministic Parser and Guardrail Module.** Rule-based parsing for service names, dates, and times, with validation logic that prevents the system from accepting ambiguous or incomplete input as confirmed information.

**Appointment Operation Tools.** Interfaces to backend appointment operations: create booking, cancel appointment, retrieve next available, check conflicts. These tools have strict schemas and return structured outcomes that the system can validate.

**Queue Estimation and Recommendation Subsystem.** Prediction logic that estimates waiting time for different slots, ranks options, and recommends less-congested times to users with transparency about uncertainty.

**Logging, Exception Handling, and Audit Utilities.** Comprehensive logging of all interactions, system decisions, and errors; exception handling that recovers gracefully from partial failures; and audit trails for governance compliance.

## 3.7 Data Sources and Management

The methodology uses three distinct data categories:

**Design and Implementation Data.** Source code, design documents, architecture diagrams, and implementation logs from project development. This data is not sensitive and documents the creation process.

**Evaluation Data.** Test scenario execution results, including conversation transcripts, system outputs, error logs, and outcome metrics. This data reflects system behavior under defined conditions but does not involve real patient information.

**Secondary Evidence.** Literature references, prior research findings, and external standards that contextualize the artifact within known research. This evidence grounds design choices in established scholarship.

Importantly, the methodology explicitly does NOT use real patient clinical data. All evaluation uses synthetic test records with realistic structure but fictional content. This protects actual patient privacy and allows rigorous testing of edge cases without ethical concerns.

## 3.8 Research Procedures

### 3.8.1 Requirements Elicitation

Requirements were derived from three sources: (a) documented problems in hospital scheduling from literature, (b) practical booking flow failures observed when LLMs attempt transactional work, and (c) multilingual user needs articulated in the Kenya context. Rather than using formal requirements engineering processes, this thesis engaged directly with the problems, iteratively refining what needed to be solved.

Key derived requirements included: mandatory data validation before transaction execution, deterministic error recovery, language context preservation, queue visibility, and governance auditability. These requirements drove architectural choices throughout design.

### 3.8.2 System Construction Process

Modules were implemented incrementally with clear separation of concerns: conversational generation logic was strictly separated from transactional execution logic. This separation meant that conversational mistakes did not automatically result in transactional errors. A generated response that misunderstood a user could still be caught by validation logic before harming data.

Implementation followed test-driven development practices: test cases were written first, defining what correct behavior looked like, then implementation code was written to pass tests. This approach reduced bugs and provided continuous validation.

### 3.8.3 Validation and Iterative Testing

Each major feature was validated through deterministic test prompts and scenario walkthroughs. Test scenarios included:

- **Generic intent testing:** Users saying "I need an appointment" without specifying service; the system should ask clarifying questions
- **Partial information testing:** Date-only replies ("next Tuesday") or time-only replies ("2 PM"); the system should prompt for missing information
- **Missing required data testing:** Attempting to book without name, patient ID, or other mandatory fields; the system should catch this and request data
- **Tool invocation failures:** Backend systems unavailable or returning errors; the system should handle gracefully with user-friendly messages
- **Language consistency testing:** Same scenario in English, same scenario in Swahili, mixed-language scenario; all should maintain language context appropriately
- **Edge case testing:** Conflicting times, non-existent services, boundary dates; all should be handled explicitly

These tests were not one-time validations but were repeated across iterations to ensure no regressions.

## 3.9 Evaluation Strategy

Evaluation was both formative and summative:

### 3.9.1 Formative Evaluation

Conducted during development iterations to identify instability and guide refinement. Formative evaluation asked: "Is this working as intended? What problems are emerging?" When issues were found, they immediately informed the next iteration.

### 3.9.2 Summative Evaluation

Conducted after major stabilizations using integrated scenarios combining multiple challenges. Summative evaluation asked: "Does the final artifact meet its objectives? How reliable is it? How usable?"

## 3.10 Evaluation Metrics and Criteria

The evaluation examined artifact performance across multiple dimensions:

**Reliability Metrics:**
- Booking completion rate: percentage of scenarios resulting in confirmed appointments
- Invalid transaction prevention: percentage of potentially erroneous requests caught before execution
- Error recovery rate: percentage of error scenarios where the system provided appropriate guidance

**Consistency Metrics:**
- Language consistency in transactional outputs: percentage of confirmations matching user language context
- Deterministic behavior: consistency of responses to identical inputs across multiple runs

**Usability Metrics:**
- Message clarity: subjective assessment of whether users understand system prompts
- Confirmation unambiguity: whether final confirmation blocks clearly state what was booked
- Recovery path availability: whether users can recover from errors without starting over

**Governance Metrics:**
- Audit trail completeness: whether all significant actions are logged
- Escalation routing: whether edge cases are properly routed to human staff
- Data minimization compliance: whether only necessary data is captured

## 3.11 Reliability, Validity, and Limitations

### 3.11.1 Reliability

Reliability is the consistency of results: would repeated testing produce similar outcomes? Reliability in this study is enhanced through deterministic checks (the same input should produce the same output), repeatable test scripts (scenarios are precisely defined), and explicit handling of known failure modes (errors are trapped and communicated rather than silently ignored).

### 3.11.2 Construct Validity

Construct validity examines whether what is being measured actually reflects what we claim to be measuring. Construct validity is supported by mapping design objectives directly to observable system behaviors: if the objective is "reliable booking completion," the measure is whether bookings succeed under realistic conditions; if the objective is "language consistency," the measure is whether outputs match user language context.

### 3.11.3 Internal Validity

Internal validity addresses whether observed effects are due to the intervention or to other factors. This thesis strengthens internal validity through: baseline testing before improvements, isolation of single changes per iteration, and documentation of confounding factors. However, limitations exist because the artifact is evaluated in controlled conditions, not live hospital settings.

### 3.11.4 External Validity

External validity addresses whether findings generalize beyond this specific case. This thesis acknowledges external validity limitations: the prototype operates at small scale, uses simulated queue data, and is evaluated by researchers rather than actual users. However, external validity is improved through modular architecture (components can be used elsewhere), policy-agnostic design (principles apply beyond Kenya), and transparent documentation of context-specific and general-purpose elements.

### 3.11.5 Study Limitations

Key limitations include: prototype-scale evaluation, no live user testing, simulated appointment data, limited testing with actual Swahili speakers, and researcher-conducted evaluation. These limitations do not invalidate findings but contextualize them as evidence of feasibility and design patterns rather than proof of real-world effectiveness.

## 3.12 Ethical and Governance Procedures

The system is intentionally and explicitly constrained to administrative functions only. This constraint protects both users and the institution by preventing drift into clinical advice. Ethical safeguards include:

- **Role transparency:** The system clearly states it is not a clinical tool and cannot provide medical advice
- **Data minimization:** Only appointment-related data (name, ID, contact, service, date, time) is collected
- **Access controls:** Audit logs are restricted to authorized personnel
- **Escalation pathways:** Complex or sensitive issues are routed to qualified human staff
- **Language respect:** Supporting Swahili and English equally, not treating one as a secondary option
- **Recourse mechanisms:** Users can request corrections or deletions of their interaction data

These safeguards are not compliance add-ons but are built into system design.

## 3.13 Chapter Summary

This chapter has presented a design science methodology appropriate for healthcare technology research. The approach combines iterative development, realistic scenario testing, and systematic evaluation to produce both a working artifact and documented design knowledge. The next chapter describes the system architecture and implementation details of the artifact itself.
2. minimal data requirements;
3. non-diagnostic boundaries;
4. recommendation of human escalation where needed.

## 3.13 Methodological Justification

Design science is appropriate because the contribution is not purely explanatory. The study contributes a tangible artifact, validated behavior patterns, and a practical framework for responsible deployment.

## 3.14 Chapter Summary

This chapter has described how the research was executed, how the artifact was evaluated, and how methodological quality was addressed. The next chapter details architecture and implementation choices.
