# CHAPTER 3 SUPPLEMENT. EXTENDED METHODOLOGY, INSTRUMENTS, AND ANALYTICAL PROTOCOLS

## A. Purpose

This supplement expands the methodology chapter into operational detail suitable for full-length thesis submission. It documents the artifact evaluation protocol, scenario design logic, reliability scoring framework, and quality-assurance process for reproducibility.

## B. Design Science Traceability Table

This section maps each design-science stage to concrete outputs.

1. Problem identification
Output: documented booking-flow failure patterns and multilingual inconsistency risks.
2. Objective definition
Output: reliability, localization, and queue-visibility requirements.
3. Design and development
Output: modular architecture and deterministic booking controls.
4. Demonstration
Output: scenario-based walkthroughs and simulated user interactions.
5. Evaluation
Output: functional test suite results and edge-case behavior checks.
6. Communication
Output: thesis chapters, implementation reports, deployment guidance.

## C. Artifact Evaluation Protocol

### C.1 Evaluation Questions

1. Can users complete booking flows using natural language with partial and shorthand responses?
2. Does the system prevent incomplete or invalid booking execution?
3. Are queue-aware slot recommendations clear and actionable?
4. Is transactional language consistently localized in Swahili contexts?
5. Does the system recover predictably from model/tool failures?

### C.2 Evaluation Phases

Phase 1. Baseline behavior observation.
Phase 2. Deterministic guardrail integration.
Phase 3. Localization enforcement enhancement.
Phase 4. Regression and end-to-end reliability validation.

## D. Scenario Engineering Framework

Scenarios were designed to emulate realistic booking pathways and common user variability.

### D.1 Scenario Families

1. Complete-input scenarios
2. Partial-input scenarios
3. Ambiguous-input scenarios
4. Missing-data scenarios
5. Localization scenarios
6. Failure and recovery scenarios

### D.2 Representative Scenario Definitions

Scenario S1: Full booking in a single turn.
Expected behavior: extract details, validate, and complete booking.

Scenario S2: Patient details first, service later.
Expected behavior: collect and proceed without reset.

Scenario S3: Date-only reply after service selection.
Expected behavior: return optimized slots and prompt time selection.

Scenario S4: Time-only reply after date and service.
Expected behavior: complete booking with recovered context.

Scenario S5: Swahili flow to booking completion.
Expected behavior: full transactional localization.

Scenario S6: Malformed tool-call event.
Expected behavior: retry/fallback and informative user messaging.

## E. Measurement Definitions

### E.1 Reliability Metrics

1. Completion success ratio
Definition: number of successfully completed bookings divided by total booking attempts.

2. Invalid execution prevention ratio
Definition: number of blocked incomplete transaction attempts divided by total incomplete attempts.

3. Recovery success ratio
Definition: number of sessions restored after error divided by total sessions with error conditions.

### E.2 Communication Quality Metrics

1. Instruction clarity score
2. Confirmation clarity score
3. Recommendation interpretability score

These can be assessed by expert raters using a 5-point rubric.

### E.3 Localization Consistency Metrics

1. Transaction output language match rate
2. Label localization completeness rate
3. Appointment-type value localization rate

## F. Rubrics

### F.1 Completion Quality Rubric

5 = all required details captured and valid booking completed with clear confirmation.
4 = booking completed with minor phrasing issue but no ambiguity.
3 = booking completed but requires user correction step.
2 = booking not completed due to avoidable system behavior.
1 = invalid or misleading booking outcome.

### F.2 Localization Quality Rubric

5 = fully localized transactional blocks and values.
4 = minor untranslated non-critical token.
3 = mixed-language transaction block with understandable meaning.
2 = key transactional fields untranslated.
1 = language mismatch causes ambiguity.

## G. Internal Validity Controls

1. Fixed scenario scripts for repeated evaluations.
2. Deterministic parser checks to isolate causal effects.
3. Consistent environment setup across test runs.
4. Versioned code changes tied to observed behavior deltas.

## H. Construct and Content Validity

Construct validity is supported by direct objective-to-metric mapping.

Objective: improve reliability.
Metric: completion success and invalid execution prevention.

Objective: improve multilingual consistency.
Metric: localization completeness and match rates.

Objective: improve queue-informed decision support.
Metric: recommendation clarity and slot interpretability.

## I. Threats to Validity

1. Scenario realism may not capture all real-world user diversity.
2. Predictive queue logic may perform differently under live hospital demand.
3. Controlled testing cannot fully represent production infrastructure volatility.
4. Absence of large patient-user studies limits perception-level inference.

Mitigation strategies include phased pilots, continuous logging review, and mixed-method follow-up studies.

## J. Reproducibility Package

Recommended reproducibility artifacts:

1. Scenario scripts and expected outcomes matrix.
2. Environment and dependency manifest.
3. Log snapshots tied to evaluation rounds.
4. Change log linking fixes to observed failures.
5. Localization test cases with bilingual expected outputs.

## K. Statistical Extension Plan for Future Work

For larger-scale pilots, apply:

1. pre/post deployment comparison on waiting-time distribution;
2. interrupted time-series analysis for service throughput;
3. stratified analysis by language preference and service type;
4. user trust modeling with ordinal regression.

## L. Methodological Summary

This supplement operationalizes the study's methodology as an auditable, repeatable evaluation approach. It supports transition from prototype validation to field-grade assessment while retaining design-science rigor.
