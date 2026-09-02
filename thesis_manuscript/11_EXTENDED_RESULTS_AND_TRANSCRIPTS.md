# CHAPTER 5 SUPPLEMENT. EXTENDED RESULTS, OBSERVATIONS, AND TRANSCRIPT-STYLE CASES

## A. Purpose

This supplement expands the results chapter with structured observations from key scenario families. It emphasizes behavior-level evidence relevant to reliability, localization, and queue-informed support.

## B. Aggregate Findings Overview

Across evaluated scenarios, three broad outcomes were observed:

1. Deterministic flow controls improved transaction completion reliability.
2. Queue-aware recommendations improved decision transparency at slot-selection stages.
3. Deterministic localization eliminated language drift in critical transaction outputs.

## C. Scenario Case Narratives

### Case R1: Standard Booking Completion

User trajectory:

1. user initiates booking intent;
2. system requests mandatory details;
3. user provides details and service type;
4. system requests date;
5. user selects date and time;
6. system confirms appointment.

Observed quality:

1. clear progression prompts;
2. no skipped mandatory field;
3. complete confirmation record.

### Case R2: Date-Only Input After Service

User trajectory:

1. service type provided;
2. user provides only date;
3. system returns ranked slot options with congestion indicators.

Observed quality:

1. context recovery successful;
2. recommendation block interpretable;
3. user prompt to choose a time is explicit.

### Case R3: Time-Only Completion

User trajectory:

1. user had previously provided service and date;
2. user submits only time token;
3. system recovers context and executes booking.

Observed quality:

1. robust partial-input handling;
2. reduced need for repetitive user restatement.

### Case R4: Missing Patient Details

User trajectory:

1. user attempts to advance booking without full details;
2. system blocks transaction and requests missing fields.

Observed quality:

1. safe prevention of incomplete booking;
2. precise missing-field feedback.

### Case R5: Swahili End-to-End Booking

User trajectory:

1. user interacts in Swahili;
2. system guides flow in Swahili;
3. final booking confirmation returned fully localized.

Observed quality:

1. transactional consistency maintained;
2. localized labels and appointment-type values present.

### Case R6: Swahili Best-Slots Message

User trajectory:

1. user requests booking flow in Swahili;
2. date provided;
3. system returns best available slots in Swahili.

Observed quality:

1. slot heading localized;
2. congestion labels localized;
3. appointment type value localized;
4. analytics labels localized.

## D. Error Recovery Observations

### D.1 Tool Schema Instability Cases

Observed condition:

Some model-tool interactions produced malformed argument structures.

Recovery behavior:

1. retry path initiated for known failure pattern;
2. user-facing fallback messaging if retry fails.

### D.2 Rate Limit Cases

Observed condition:

Upstream model rate limits caused temporary interruption.

Recovery behavior:

1. explicit user message advising retry interval;
2. no silent failure.

### D.3 Ambiguous Service Input Cases

Observed condition:

Generic booking phrases were occasionally interpreted as service names.

Recovery behavior:

1. service parser refined with alias mapping and generic phrase rejection;
2. booking flow prompt requests valid service type.

## E. Comparative Behavior Delta

### E.1 Before Deterministic Controls

1. intermittent stalls in booking progression;
2. invalid tool calls under partial input;
3. occasional ambiguous user guidance.

### E.2 After Deterministic Controls

1. stable sequence transitions;
2. higher completion confidence;
3. clearer correction prompts;
4. improved transaction safety.

## F. Localization Delta

### F.1 Before Localization Enforcement

1. mixed-language final confirmations;
2. English reversion in recommendation blocks;
3. untranslated appointment-type values.

### F.2 After Localization Enforcement

1. consistent Swahili transactional blocks;
2. localized slot recommendation labels;
3. localized appointment-type values in both booking and slots outputs.

## G. Operational Implications

1. Front-desk burden may reduce for routine scheduling interactions.
2. Patient self-service quality may improve through interpretable slot options.
3. Communication quality may improve for Swahili-preferred users.
4. Deterministic controls can reduce avoidable corrective loops.

## H. Residual Gaps and Known Constraints

1. Prediction confidence requires local data calibration in live deployment.
2. Human escalation protocol must be institutionally defined before production rollout.
3. Formal user-acceptance testing remains a next-step requirement.

## I. Reporting Template for Pilot Deployment

For future live pilots, collect monthly indicators:

1. booking completion rate;
2. average interaction turns per completed booking;
3. escalation rate to human staff;
4. language preference distribution;
5. queue-shift effect by selected slot category;
6. incident categories and recovery success.

## J. Summary

The extended results support the thesis claim that hybrid design materially improves practical reliability and multilingual transaction consistency in AI-assisted hospital scheduling workflows.
