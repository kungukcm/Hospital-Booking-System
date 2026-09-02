# CHAPTER 3 SUPPLEMENT C. FIELD PILOT DESIGN AND OPERATIONAL METHODS

## 1. Introduction

This supplement defines how the prototype can transition into a controlled field pilot while preserving methodological rigor and participant safety. It expands the evaluation framework beyond local technical tests to institution-oriented operational research.

## 2. Pilot Objectives

The pilot is designed to answer four applied questions. First, does the assistant improve booking completion under real workflow conditions, or does the operational complexity of a live environment introduce new failure modes? Second, does queue-aware recommendation influence selected slot distribution, or do users ignore the recommendations? Third, does multilingual transactional consistency hold under live usage variation, or do edge cases cause language drift at critical moments? Fourth, can governance controls be operationalized without excessive overhead, or do they create administrative burden that offsets the benefits? These questions are practical rather than theoretical and require real-world observation to answer.

## 3. Pilot Design Type

A quasi-experimental phased rollout is recommended, with baseline and intervention periods. During the baseline period, measurement of existing appointment flow indicators occurs without assistant intervention for a fixed duration to establish the control state. The intervention period involves deploying the assistant in a limited department or service line while capturing the same indicators to compare. The comparative analysis then reviews baseline and intervention trends while accounting for confounders like seasonality, staffing changes, and service-volume shifts.

## 4. Pilot Site and Service-Line Selection Criteria

Recommended criteria:

1. high enough booking volume for measurable outcomes;
2. manageable complexity for first deployment wave;
3. availability of staff for escalation and monitoring;
4. readiness for bilingual communication support.

Suitable candidates may include outpatient specialty clinics with recurring appointment demand.

## 5. Participant and Interaction Inclusion Rules

The scope of included interactions encompasses routine appointment booking requests where patients seek to make a new appointment, cancellation and rescheduling inquiries where changes to existing bookings are requested, and slot recommendation and selection interactions where the system is helping with choice. Excluded interactions involve emergency requests that demand immediate clinical action rather than administrative scheduling, direct clinical diagnosis requests where patients ask for medical opinions, and highly sensitive issues requiring immediate clinician engagement such as critical symptoms or psychological crises
5. event logs are captured for evaluation.

## 7. Escalation Model

### 7.1 Escalation Triggers

1. repeated missing-field loops;
2. unresolved parsing ambiguity after configured attempts;
3. user explicitly requests human support;
4. system-detected tool failures beyond recovery threshold.

### 7.2 Escalation Targets

The workflow follows a clear sequence. The user initiates a request through the chat interface using natural language. The assistant processes the request with deterministic controls to ensure only valid operations proceed. If the booking succeeds, a transaction confirmation is issued in the user's selected language. If an exception occurs that the system cannot resolve, the escalation pathway routes the request to human staff who take over. Throughout the process, event logs are captured for later evaluation and analysis
Escalation is triggered by several conditions. Repeated missing-field loops where the user does not provide required information after multiple attempts indicate the system is not communicating clearly and should escalate. Unresolved parsing ambiguity after the configured number of clarification attempts suggests the natural language input is too complex for the system's current capability. User explicitly requested human support, as stated through words like "speak to someone," should be honored immediately. System-detected tool failures beyond the recovery threshold, where the backend is not responding or is returning errors, mean the assistant cannot complete the booking. Escalation routes to the front-desk operator for administrative correction when the issue is a data problem, to the call center queue for follow-up support when the issue requires a conversation, or to thely capture operationally required details. Separate analytical datasets from direct identifiers where possible.

## 9. Data Governance and Ethics in Pilot

1. publish clear participant disclosure;
2. define data retention window and deletion process;
3. enforce role-based access to logs;
4. prohibit unauthorized secondary use of interaction data;
5. include opt-out route where feasible.

## 10. Monitoring Cadence

### 10.1 Daily Monitoring

1. incident count review;
Event-level data capture includes session identifiers so that interactions can be grouped and traced, timestamps per transition to measure system response time and user response time, detected language context to verify that localization is working correctly, invoked operation type to distinguish between different booking actions, and completion or escalation status to measure success rate. To ensure data minimization, only operationally required details are captured. Analytical datasets are separated from direct identifiers where possible, reducing the risk that raw data links appointments to specific patient names
1. policy compliance status;
2. risk register updates;
3. deployment continuation decision.
Governance and ethics protections include publishing clear participant disclosure explaining how data is used and what rights participants have. The data retention window and deletion process must be defined upfront so that data is not stored indefinitely. Role-based access controls enforce that only authorized personnel can view interaction logs. Unauthorized secondary use of interaction data is prohibited, meaning that data collected for booking operations cannot be repurposed for marketing or other uses without consent. An opt-out route is included where feasible, allowing patients to request that their interactions not be analyzed or logged
1. booking completion rate;
2. average turns to completion;
3. invalid execution prevention rate;
4. language-consistent confirmation rate.

Secondary KPIs:

1. escalation frequency;
2. median time to resolution;
3. low-congestion slot uptake share;
4. user-reported clarity score.

## 12. Quality Assurance Protocol

### 12.1 Pre-Go-Live QA

1. run deterministic scenario suite;
2. verify escalation routing;
3. verify localization regressions;
4. validate tool schema compatibility.

### 12.2 In-Pilot QA

1. weekly regression on critical flows;
2. targeted checks on newly observed failure patterns;
3. patch verification before deployment updates.

## 13. Incident Classification Schema

Class A: critical transactional failures.
Class B: recoverable operational disruptions.
Class C: minor wording/localization defects.
Class D: non-impact technical warnings.

This schema improves triage prioritization and reporting consistency.

## 14. Analytical Methods for Pilot Data

1. pre/post proportion comparisons for completion outcomes;
2. trend analysis for escalation rates;
3. subgroup analysis by language context;
4. slot-selection distribution analysis by congestion category.

## 15. Human Factors Evaluation

Introduce a short post-interaction rating prompt for:

1. clarity of instructions;
2. confidence in booking completion;
3. ease of understanding recommended slots.

Ratings provide complementary evidence to purely system-level metrics.

## 16. Pilot Exit Criteria

Pilot should proceed to scale only if thresholds are met, such as:

1. sustained completion improvement;
2. localization consistency above target;
3. acceptable incident rate and resolution performance;
4. governance checklist compliance.

## 17. Documentation Requirements

Pilot documentation should include:

1. weekly operations report;
2. incident register;
3. change-log of fixes applied;
4. governance compliance memo;
5. final pilot evaluation report.

## 18. Risk Mitigation During Pilot

1. maintain manual fallback booking pathway;
2. limit initial service scope;
3. stagger deployment hours if needed;
4. freeze major feature additions during high-demand weeks.

## 19. Methodological Integrity Considerations

To preserve study credibility:

1. predefine key metrics and thresholds;
2. avoid selective reporting of positive cases;
3. document all major incidents and fixes;
4. report limitations transparently.

## 20. Conclusion

This field-pilot design provides a practical bridge between prototype validation and evidence-based institutional decision making. It enables controlled learning while safeguarding service continuity and policy compliance.
