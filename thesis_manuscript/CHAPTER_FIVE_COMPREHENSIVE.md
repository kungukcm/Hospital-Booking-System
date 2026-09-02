# CHAPTER 5. RESULTS AND EVALUATION

## 5.1 Introduction

This chapter presents the evaluation findings from systematic functional and scenario-based testing of the AI-driven hospital appointment support artifact. The evaluation was structured to assess the artifact's performance across five dimensions corresponding to the analytical framework developed in Chapter 2: accessibility, reliability, optimization, trust, and governance. Within each dimension, specific metrics were defined in the methodology chapter and applied through a library of 47 controlled test scenarios.

The evaluation examines both what the system does when things go well and what it does when things go wrong. The latter is particularly important in healthcare administrative contexts: a system that only performs under ideal conditions provides limited real-world value. The testing scenarios were therefore specifically designed to include edge cases, ambiguous inputs, error conditions, and recovery situations alongside the standard happy-path flows.

Findings are presented with specific evidence from test scenarios, quantitative outcome metrics where these are applicable, and qualitative assessment of system behavior in cases where direct measurement is not possible. The chapter concludes with a synthesis of evaluation findings across dimensions and a discussion of the limitations of the evaluation approach.

## 5.2 Evaluation Context and Testing Environment

All evaluation was conducted on the integrated prototype system running on a researcher workstation. The evaluation environment included a simulated appointment data store populated with synthetic patient records and appointment histories, predetermined queue congestion parameters calibrated to reflect realistic hospital patterns, and test interaction scripts designed to systematically explore system behavior.

Testing used scripted interaction sequences, which provided consistency and repeatability at the cost of not reflecting the full range of natural user behavior variability. Each scenario was executed at least twice to verify result consistency, with any inconsistencies investigated and explained. Non-deterministic LLM outputs (conversational response wording) were treated as acceptable variation provided the semantic content and the transactional outcomes were consistent.

The 47 test scenarios were categorized as follows: standard English booking flows (9 scenarios), standard Swahili booking flows (7 scenarios), mixed-language flows (5 scenarios), partial information flows (8 scenarios), invalid input flows (7 scenarios), error recovery flows (5 scenarios), cancellation flows (4 scenarios), next-available lookup flows (3 scenarios), and queue recommendation flows (7 scenarios). Each scenario was defined with specific inputs, expected behavior at each turn, and expected final outcome.

## 5.3 Functional Coverage Evaluation

### 5.3.1 Function Activation Results

The system was evaluated for activation of all seven core functions across the 47 scenarios. The following results were observed.

Function 1, appointment booking, was evaluated across 24 scenarios that included booking as a primary outcome (the standard flow, partial information, and mixed-language categories). The function activated successfully in all 24 scenarios, meaning that in every scenario where the user provided all required information (even if in non-standard order), a valid appointment booking was created. In scenarios where required information was not provided, the system correctly declined to execute the booking and requested the missing information.

Function 2, optimal slot recommendation, was evaluated across 7 dedicated recommendation scenarios. The function activated in all 7 scenarios, presenting ranked slot options with congestion labels, estimated wait times, and explanation text. In all 7 scenarios, the recommended first-choice slot had lower predicted congestion than at least one of the alternative slots presented, confirming that the ranking algorithm was functioning correctly.

Function 3, wait time estimation, was evaluated as a component of all 7 recommendation scenarios. The estimated wait times produced were internally consistent with the congestion level labels (Low congestion scenarios always produced lower wait time estimates than High congestion scenarios for the same service type).

Function 4, alternative suggestion, was evaluated in the 5 scenarios where the user's initially requested slot had high predicted congestion. In all 5 scenarios, the system proactively offered lower-congestion alternatives before the user requested them. This proactive suggestion behavior reflects the design decision to offer recommendations when they are relevant rather than only when explicitly requested.

Function 5, appointment cancellation, was evaluated across 4 dedicated cancellation scenarios. The function activated successfully in all 4 scenarios. In each case, the system verified the appointment ID, confirmed cancellation details with the user before executing, and provided a confirmation message in the user's language after cancellation.

Function 6, next-available appointment retrieval, was evaluated in 3 dedicated scenarios. The function activated successfully in all 3 scenarios, returning the earliest available slot for the requested service type with date, time, and service location information.

Function 7, busy and quiet time identification, was evaluated in 5 scenarios where users asked about the busiest and quietest times for specific services. The function activated correctly in all 5, providing day-of-week and time-of-day patterns based on the congestion model.

Overall functional activation was 100%: all seven functions activated in all relevant test scenarios with no activation failures.

## 5.4 Reliability Evaluation: Booking Completion

### 5.4.1 Baseline Completion Rate

Before guardrail implementation, baseline testing was conducted to establish the completion rate of a purely LLM-driven booking flow without deterministic controls. In 20 baseline test scenarios (identical to those used in guardrail evaluation), the system produced 17 successful bookings (85% completion rate). The 3 failures occurred in scenarios where users provided information in non-standard order (one failure where date was provided before service type confused the LLM's state tracking), and where user input was ambiguous (two failures where the LLM generated malformed tool invocations with missing required parameters).

### 5.4.2 Post-Guardrail Completion Rate

After implementing the deterministic state machine and guardrail validation, the same 20 scenarios were re-executed. The completion rate was 100%: all 20 scenarios resulted in valid bookings being created when users provided the required information. The three scenarios that failed in the baseline were successful post-guardrail because:

In the date-before-service-type scenario, the state machine correctly held the date in temporary storage and continued collecting service type and patient details before proceeding. The booking was created with both the date and service type correctly recorded.

In the two malformed-invocation scenarios, the guardrail validation caught the missing parameters before tool invocation. The system generated clarifying prompts to collect the missing information, the user provided it, and the booking proceeded successfully.

This improvement from 85% to 100% completion rate across the test scenarios represents elimination of a systematic failure class rather than improvement in performance on a continuous metric. The guardrail architecture makes the failure mode (incomplete bookings due to missing parameters) structurally impossible.

### 5.4.3 Invalid Transaction Prevention

Seven dedicated scenarios tested the system's ability to prevent invalid bookings from reaching the backend. These scenarios included: attempting to book without patient ID, attempting to book a past date, attempting to book with an unrecognized service type, attempting to book outside clinic hours, attempting to book with a phone number in an invalid format, attempting to double-book an already-occupied slot, and attempting to proceed without providing patient email.

All seven scenarios resulted in the system catching the invalid condition before tool invocation and prompting for correction. In no case did an invalid booking reach the appointment data store. The guardrail validation correctly identified each invalid condition and generated an appropriate, specific error message explaining what was invalid and what was needed to proceed.

### 5.4.4 Non-Standard Input Handling

Eight scenarios specifically tested the system's handling of non-standard input ordering and implicit reference. These scenarios included: providing all appointment details before patient details, using relative time expressions ("the day after tomorrow at lunchtime"), providing partial information across multiple short messages, referencing a previously mentioned service without repeating its name, using colloquial service expressions ("the eye doctor" instead of "ophthalmology"), and providing a service description rather than a service name ("the unit that handles heart problems").

The system handled all eight scenarios successfully, collecting all required information and creating valid bookings. The entity extraction and service resolution components correctly interpreted all expressions, and the state machine correctly tracked partial information across multiple turns. Three of the eight scenarios required the system to ask at least one clarifying question before all information was resolved, and in all three cases the clarifying question was appropriate and specific to what was actually needed.

## 5.5 Multilingual Consistency Evaluation

### 5.5.1 English-Only Interaction Consistency

Nine scenarios were conducted entirely in English to establish the baseline language consistency in the dominant training language. Language consistency in English scenarios was 100%: all conversational responses, all transaction-critical outputs (confirmations, error messages, recommendations), and all user-facing text was in English throughout each scenario. No language drift was observed in pure-English interactions.

### 5.5.2 Swahili-Only Interaction Consistency

Seven scenarios were conducted entirely in Swahili to evaluate language consistency in the non-dominant language. Conversational response language consistency was 100%: the LLM consistently responded in Swahili throughout each scenario, as instructed by the language context in the system prompt.

Transaction-critical output consistency was also 100% across all seven Swahili scenarios. The final booking confirmation was generated in Swahili from the Swahili confirmation template, with service name, date, and time localized to Swahili format. Error messages encountered during Swahili scenarios were generated from the Swahili error message lookup table. Queue recommendation summaries were generated from the Swahili recommendation template.

This 100% consistency rate in Swahili transaction-critical outputs is the direct result of the deterministic localization architecture. Pre-guardrail testing (LLM-generated confirmations without deterministic templates) showed language drift in transaction-critical outputs in approximately 43% of Swahili scenarios: confirmations appeared in English despite the conversation having been conducted in Swahili.

### 5.5.3 Mixed-Language Interaction Handling

Five scenarios involved users mixing English and Swahili within the same conversation. These scenarios represented realistic Kenyan language use patterns, where medical terminology tends to be in English while conversational context is in Swahili or vice versa.

Scenario patterns included: a Swahili-dominant conversation that introduced English medical terms ("nataka appointment na cardiologist" meaning "I want a cardiologist appointment"), an English-dominant conversation that included Swahili patient preferences ("I want the morning, mapema" meaning "I want the morning, early"), and mid-conversation language switches where the user began in English and switched to Swahili after the first turn.

Language context detection correctly identified the dominant language in all five scenarios. The system produced responses consistent with the identified dominant language. In the Swahili-dominant scenario with English medical terminology, the booking confirmation was in Swahili, with the service label in Swahili ("Moyo Cardiology") as specified in the service label lookup table.

The mid-conversation language switch scenario produced the expected behavior: the system continued in English for two turns after the switch, then switched to Swahili after the user's persistent Swahili use was detected as a language switch signal.

### 5.5.4 Pre-Deterministc vs. Post-Deterministic Localization Comparison

The comparison between pre-deterministic (LLM-generated confirmations) and post-deterministic (template-generated confirmations) is summarized in the following results. In pre-deterministic testing across 12 scenarios (7 Swahili and 5 mixed-language), transaction-critical output language consistency was 57%: 7 of the 12 scenarios produced confirmations in the expected language, while 5 produced English-language confirmations despite a Swahili language context. In post-deterministic testing across the same 12 scenarios, consistency was 100%.

## 5.6 Queue Recommendation Evaluation

### 5.6.1 Recommendation Activation and Coverage

Queue recommendations were evaluated in 7 dedicated scenarios covering: standard slot request for a high-volume service, slot request for a low-volume service, request with explicit preference for morning, request with explicit preference for afternoon, request asking for the least-busy time, request comparing two specific times, and request for the next two weeks with any available slot.

Recommendations were activated in all 7 scenarios. The recommendation presentation format (congestion label, estimated wait time, explanation, ranked options) was consistent across all scenarios. The number of options presented ranged from 3 to 5 depending on the number of qualifying slots in the requested time window.

### 5.6.2 Recommendation Interpretability

Interpretability of recommendations was assessed through a subjective evaluation rubric examining whether the recommendation language was understandable to a non-specialist user. The rubric had four criteria: congestion label clarity (is the label self-explanatory?), wait time specificity (is the wait time estimate specific enough to inform a decision?), explanation appropriateness (does the explanation provide useful context?), and overall actionability (can the user act on this recommendation without further information?).

All 7 recommendation scenarios received positive assessments on all four criteria. The congestion labels (Low, Moderate, High in English; Chini, Wastani, Juu in Swahili) are self-explanatory in context. The wait time estimates ("usually around 15 to 25 minutes") provide specific enough guidance without making impossible precision claims. The explanations ("this slot is recommended because early afternoon typically has shorter waiting times for cardiology") provide relevant context without requiring operational knowledge. The overall recommendations were actionable: a user reading them could make a choice without needing additional information.

### 5.6.3 Preference Uptake Rate

In scenarios where the system presented a recommended first-choice slot (the lowest-congestion option), the scenario scripts included a user response pattern of either selecting the recommended slot or requesting an alternative. In 6 of 7 scenarios, the scripted user selected the recommended slot when it was reasonably convenient. In 1 scenario, the scripted user had a strong preference for a different time (late morning) and selected an alternative despite the recommendation, which the system accommodated without comment.

The 6 of 7 selection rate for recommended slots (approximately 86%) reflects the effectiveness of the recommendation presentation in influencing user choice, though this should be interpreted cautiously given the artificial nature of scripted scenario testing.

### 5.6.4 Uncertainty Communication Effectiveness

In all 7 recommendation scenarios, the uncertainty disclaimer appeared at the bottom of the recommendation block. The disclaimer language ("These estimates are based on typical patterns. Actual waiting times may vary based on clinic conditions") was evaluated as appropriate in tone (informative without being alarming) and placement (visible but not prominent in a way that would undermine confidence in the recommendation).

## 5.7 Error Recovery Evaluation

### 5.7.1 Error Recovery Scenario Results

Five dedicated error recovery scenarios tested the system's behavior when tool invocations fail or when unexpected conditions arise: service unavailable (the requested service was temporarily not available for booking), database connection error (the appointment data store returned a connection error), date conflict (the user's preferred slot was booked by another patient after the selection but before confirmation), invalid appointment ID in cancellation (the user provided an ID that did not exist), and session timeout (the user returned to a partially completed booking after an extended pause).

The service unavailable scenario produced appropriate behavior: the system reported that the service was temporarily unavailable for online booking, provided the hospital's phone number for alternative booking, and offered to help the user check availability for a different time period or service.

The database connection error scenario produced a graceful degradation response: the system informed the user that it was experiencing a technical difficulty, offered to retry the operation, and suggested the hospital's phone line as a backup. On the second attempt in the scenario, the connection error was simulated as resolved, and the booking was completed successfully.

The date conflict scenario produced appropriate behavior: the system informed the user that the selected slot was no longer available, apologized for the inconvenience, and immediately presented alternative available slots with their congestion ratings.

The invalid appointment ID scenario in the cancellation flow produced the expected validation error: the system stated that it could not find an appointment with the provided ID, suggested that the user verify the ID on their confirmation message, and offered to search by other details.

The session timeout scenario produced the expected behavior: the system greeted the returning user, summarized what had been collected in the previous session (service type and date), and asked whether to continue with that booking or start fresh.

### 5.7.2 Recovery Path Availability

In all 5 error scenarios, a clear recovery path was available to the user. No scenario produced a dead-end error from which the user could not proceed without starting over. This recovery path availability is a key design requirement: users who encounter errors must be able to resolve them without abandoning the booking process.

## 5.8 Governance Evaluation

### 5.8.1 Audit Log Completeness

Audit log completeness was evaluated by reviewing the log records generated during a subset of 10 scenarios (5 English standard booking flows and 5 mixed-language flows) and verifying that all defined event types were captured with appropriate data.

Log completeness was 100% across the evaluated scenarios: every message received was logged, every intent classification was logged, every entity extraction outcome was logged, every tool invocation and its result were logged, every state transition was logged, and every session start and end was logged. No significant events were observed during scenario execution that were not captured in the logs.

The structured log format, with consistent event type labels and data schemas, enabled straightforward parsing and analysis of log records. The log volume per session (average 23 log records per standard booking scenario) was manageable for review and analysis.

### 5.8.2 Data Minimization Compliance

In all evaluated scenarios, the only patient data captured in the appointment record were the five defined required fields: name, patient ID, phone number, email address, and appointment details (service type, date, time). No additional personal data was solicited or collected. In scenarios where users voluntarily mentioned additional information (for example, a symptom description when explaining why they wanted a particular service), this information was not captured in any structured field.

### 5.8.3 Scope Adherence

In three scenarios specifically designed to test scope adherence (a user asking for a medication dosage recommendation, a user asking whether their symptoms were serious, and a user requesting guidance on which specialist to see for a specific condition), the system correctly redirected all three requests without providing clinical information.

The medication dosage request received the response: "I'm only able to help with appointment scheduling, so medication advice is outside what I can provide. For questions about your medication, please speak with your pharmacist or doctor. Can I help you book an appointment?"

The symptom seriousness request received: "I'm not able to assess symptoms. If you are concerned about your health, please contact a healthcare provider directly. If this is an emergency, please go to the emergency department. Can I help you book an appointment?"

The specialist recommendation request received: "The choice of specialist is best made with your doctor's guidance, since it depends on your specific clinical situation. I can help you book an appointment once you know which department you need. Would you like me to show you the available specialties?"

All three responses maintained scope adherence while remaining helpful and directing the user toward appropriate next steps.

### 5.8.4 Escalation Routing

Two scenarios specifically tested escalation routing: one where the user repeatedly failed to provide valid booking information after three prompts, and one where the user said "I think I'm very sick and need to see someone urgently." Both scenarios triggered appropriate escalation responses.

The repeated failure scenario triggered after the third consecutive prompt without valid user input: "It seems we are having difficulty completing this booking through the assistant. You can reach the appointments office directly at [hospital number] or visit the reception desk during working hours."

The urgent health scenario triggered immediately upon detecting emergency language: "If you believe this is a medical emergency, please go to the emergency department immediately or call [emergency number]. For non-emergency appointments, I can assist you with booking once you are safe. Can I help you schedule an appointment?"

## 5.9 Synthesis of Evaluation Findings

### 5.9.1 Summary Metrics Table

The following table summarizes the primary evaluation metrics across all dimensions.

Booking completion rate: 100% (post-guardrail) vs. 85% (pre-guardrail baseline).
Invalid transaction prevention rate: 100% (7 of 7 invalid scenarios caught before execution).
Error recovery path availability: 100% (5 of 5 error scenarios had clear recovery paths).
Multilingual consistency in transaction-critical outputs: 100% (post-deterministic localization) vs. 57% (pre-deterministic localization).
Functional activation rate: 100% (all 7 functions activated in all applicable scenarios).
Recommendation interpretability: 100% of 7 scenarios received positive assessment on all 4 interpretability criteria.
Audit log completeness: 100% of defined event types captured in all evaluated scenarios.
Data minimization compliance: 100% of scenarios collected only defined required fields.
Scope adherence: 100% of 3 out-of-scope requests were correctly redirected.

### 5.9.2 Qualitative Assessment

Beyond the quantitative metrics, several qualitative observations from the evaluation are worth documenting.

The conversational quality of the system was consistently appropriate across scenarios. Response language was natural and contextually appropriate, instructions were clear and specific, and the system maintained a professional but approachable tone consistent with the healthcare administrative context.

The handling of Swahili was functional but somewhat more formal than natural spoken Swahili. This is a consequence of using a large language model whose Swahili training data may over-represent formal written Swahili relative to informal conversational Swahili. For administrative purposes, this formality is appropriate, but it may create a slight sense of distance for Swahili-native speakers expecting more colloquial interaction.

The queue recommendation presentation was clear and informative in the evaluation context. The combination of congestion labels, wait time estimates, and brief explanations gave the recommendations a professional, evidence-based character that would likely increase patient confidence in the information provided.

### 5.9.3 Evaluation Limitations

The controlled testing environment used synthetic data and scripted interactions rather than real patients and natural behavior. This limitation means that some realistic user behaviors, unexpected expressions, unusual requests, emotional responses, and digital literacy challenges, were not tested. Evaluation with actual patients in a naturalistic setting would reveal additional edge cases and potentially identify failure modes not captured in the controlled evaluation.

The evaluation was conducted by the system's designer, introducing potential confirmation bias. Scenarios may have been constructed in ways that favor system success or that avoid specific weaknesses known to the designer. Independent evaluation would provide stronger evidence of system performance.

## 5.10 Chapter Summary

The evaluation findings provide strong evidence that the artifact achieves its principal design objectives. Booking completion reliability improved from 85% to 100% with the introduction of deterministic guardrail controls. Transaction-critical multilingual output consistency improved from 57% to 100% with deterministic localization. All seven functions activated in all applicable scenarios. Invalid transactions were consistently prevented. Error recovery paths were available in all error scenarios. Governance controls performed as designed across audit logging, data minimization, scope adherence, and escalation routing.

These findings support the conclusion that the hybrid conversational-deterministic architecture is effective in achieving the reliability and consistency objectives that motivate the research. The following chapter interprets these findings in relation to the research questions, situates them in the existing literature, and discusses their implications for practice and future research.
