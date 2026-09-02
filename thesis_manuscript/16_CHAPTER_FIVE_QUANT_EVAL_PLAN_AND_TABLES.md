# CHAPTER 5 SUPPLEMENT B. QUANTITATIVE EVALUATION PLAN, TABLE SHELLS, AND ANALYTICAL EXTENSION

## A. Purpose

This supplement provides a quantitative evaluation blueprint for moving from controlled technical validation to institution-level pilot evidence.

## B. Evaluation Logic Model

Inputs:

1. conversational assistant artifact;
2. deterministic booking controls;
3. queue recommendation engine;
4. multilingual localization module.

Activities:

1. user interactions for appointment tasks;
2. booking flow transitions;
3. recommendation display and selection;
4. confirmation generation and storage.

Outputs:

1. completed bookings;
2. prevented invalid transactions;
3. localized transaction blocks;
4. recommendation usage records.

Outcomes:

1. improved scheduling reliability;
2. improved communication clarity;
3. improved queue-informed slot choice behavior.

## C. Core Metrics and Definitions

### C.1 Transaction Metrics

1. Booking Completion Rate
Formula: completed bookings / initiated booking sessions.

2. Guardrail Intervention Rate
Formula: sessions requiring missing-field correction / initiated booking sessions.

3. Invalid Booking Attempt Prevention Rate
Formula: blocked incomplete booking attempts / incomplete booking attempts.

### C.2 Recommendation Metrics

1. Recommendation View Rate
Formula: sessions where slot recommendation is shown / sessions with valid date input.

2. Low-Congestion Selection Share
Formula: bookings choosing low-congestion slots / bookings from recommendation sessions.

3. Recommendation Acceptance Latency
Formula: median time from recommendation display to time selection.

### C.3 Localization Metrics

1. Transaction Language Match Rate
Formula: confirmations in preferred language / total confirmations.

2. Localization Completeness Score
Rubric-based score on labels, values, and follow-up prompts.

## D. Data Collection Plan

### D.1 Event Schema

Recommended logged events:

1. booking_session_started
2. patient_details_collected
3. appointment_type_set
4. preferred_date_set
5. slots_presented
6. selected_time_received
7. booking_completed
8. booking_blocked_missing_fields
9. localization_applied
10. escalation_triggered

### D.2 Data Quality Rules

1. unique session identifiers required.
2. timestamp ordering checks required.
3. no missing event type values.
4. language field must be populated for transaction events.

## E. Statistical Analysis Plan

### E.1 Descriptive Statistics

1. means, medians, and percentiles for interaction turns and latency;
2. distribution of slot-category selections;
3. language preference distribution and localization outcomes.

### E.2 Comparative Analysis

1. pre/post guardrail comparison using proportion tests;
2. comparison of completion outcomes by language context;
3. analysis of recommendation uptake by service type.

### E.3 Regression Extensions

Possible models:

1. logistic regression for completion probability;
2. ordinal regression for clarity rating outcomes;
3. survival analysis for time-to-completion.

## F. Table Shells for Thesis Presentation

### Table F1. Session-Level Completion Summary

Columns:

1. period
2. initiated sessions
3. completed bookings
4. completion rate
5. confidence interval

### Table F2. Guardrail Effects

Columns:

1. scenario type
2. missing-field prompts triggered
3. corrected successfully
4. unresolved
5. correction success rate

### Table F3. Recommendation Behavior

Columns:

1. service type
2. slots shown
3. low-congestion selected
4. moderate selected
5. high selected
6. low-congestion share

### Table F4. Localization Quality

Columns:

1. language context
2. transaction blocks generated
3. fully localized
4. partially localized
5. localization match rate

### Table F5. Incident Summary

Columns:

1. incident class
2. frequency
3. median resolution time
4. recurrence rate after patch

## G. Figure Suggestions

1. Funnel chart for booking completion stages.
2. Heatmap of selected slots by predicted congestion.
3. Trend chart of localization match rate over time.
4. Control chart for malformed-tool-call incidents.

## H. Pilot Study Design Option

### H.1 Quasi-Experimental Setup

1. baseline period: manual/legacy process measurement;
2. intervention period: assistant-enabled workflow;
3. matched service-line comparison where possible.

### H.2 Sample and Duration

Suggested minimum:

1. 8-12 weeks pilot period;
2. at least 400 booking sessions;
3. stratification by language and service type.

### H.3 Outcome Interpretation Thresholds

Example thresholds:

1. completion rate improvement >= 10 percentage points;
2. localization match >= 95 percent;
3. invalid execution prevention >= 90 percent.

## I. Threats in Quantitative Interpretation

1. novelty effects in early pilot periods;
2. operational confounders such as staffing fluctuations;
3. upstream model-service variance;
4. non-random language preference distributions.

Mitigation strategies:

1. time-window normalization;
2. stratified reporting;
3. sensitivity analyses;
4. transparent caveat reporting.

## J. Ethical Analytics Guidance

1. avoid logging unnecessary free-text personal content when aggregate events suffice;
2. pseudonymize identifiers before analysis;
3. enforce role-based data access;
4. report only aggregate metrics in public outputs.

## K. Implementation Script Recommendations

1. nightly metric aggregation job;
2. weekly quality dashboard update;
3. incident triage report generation;
4. monthly governance review packet.

## L. Summary

This quantitative extension plan enables rigorous impact assessment beyond prototype validation and provides a direct bridge to evidence-based deployment decisions in hospital settings.
