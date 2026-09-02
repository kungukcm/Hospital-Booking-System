# CHAPTER 4 SUPPLEMENT D. IMPLEMENTATION TROUBLESHOOTING AND VALIDATION JOURNAL

## 1. Introduction

This supplement documents implementation issues encountered during development and the logic used to resolve them. It serves as a technical validation journal and makes the implementation process more transparent for thesis readers and reviewers.

## 2. Why Troubleshooting Matters in a Thesis Artifact

For an applied thesis, it is not enough to show the final system. The path from initial instability to a working artifact reveals the design principles that matter most. Troubleshooting exposes the assumptions that failed when tested against real usage patterns, boundaries that were too loose and allowed invalid transitions, inputs the system misread due to unexpected user phrasing, and how reliability improved over multiple iterations. This is valuable because the final architecture is only understandable when viewed alongside the problems that shaped it.

## 3. Input Interpretation Issues

### 3.1 Generic Booking Phrases Misread as Service Names

Early versions of the assistant sometimes interpreted generic booking requests such as "I need an appointment" as though they were specific service types. This created invalid flow transitions because the system could not confidently infer the next step. To resolve this, the system was updated to introduce a rejection rule for generic booking phrases so they would not be misclassified. Explicit service aliases for known departments were added to improve recognition. The flow was preserved as a query for missing information rather than a failed booking, allowing users to clarify what they wanted.

### 3.2 Service Abbreviation Ambiguity

Some users supplied short forms or colloquial terms for service types. The system needed to map these to canonical services without overfitting to unrelated phrases. The solution created a service alias table that mapped common variations to official department names, normalized text for consistent matching across spellings and formatting, and returned canonical service names where confidence was high.

### 3.3 Date and Time Parsing Variability

Users do not always provide dates and times in the expected format. The assistant therefore needed to support both structured and natural expressions.

Resolution:

1. accepted multiple date formats;
2. recognized common relative date words;
3. parsed 24-hour and am/pm time expressions;expressions like "2024-06-15" and natural language like "next Tuesday." The solution accepted multiple date formats, recognized common relative date words like "today," "tomorrow," and "next week," parsed both 24-hour time notation and am/pm expressions, and retained previous context when only time was supplied so the user would not need to repeat the dateoking data. If the assistant tried to continue without name, patient ID, phone, or email, the booking tool would reject the request.

Resolution:

1. implemented a hard gate before booking execution;
2. returned only the missing details to the user;
3. avoided sending incomplete data into the tool layer.
 To resolve this, the system implemented a hard gate before booking execution that would not allow the booking tool to be called with incomplete data. Instead of attempting the booking, the system returned only the missing details to the user. This avoided sending incomplete data into the tool layer where it would fail with unclear error messages
1. made flow progression deterministic for service-only, date-only, and time-only inputs;
2. stored context from earlier turns;
3. continued the booking sequence without requiring the user to restate everything. The solution made flow progression deterministic for service-only responses, date-only responses, and time-only responses. The system stored context from earlier turns so information from previous exchanges would not be lost. This allowed the booking sequence to continu when schemas are too permissive or too complex. Optional fields and nested ambiguity increase the chance of malformed invocations.

Resolution:

1. simplified tool signatures;
2. limited optional parameters where possible;
3. added validation before tool execution; The solution simplified tool signatures to only essential parameters, limited optional parameters where possible to reduce ambiguity, added validation before tool execution to catch schema violations early, andsolution:

1. separated tool execution from synthesis;
2. translated or reformatted tool outputs where necessary;
3. bypassed synthesis in certain deterministic cases to preserve control.

## 6. Multilingual Troubleshooting

### 6.1 Language Drift

Initially, outputs could drift back to English at the confirmation stage even when the user was clearly interacting in Swahili.
 The solution separated tool execution from synthesis so they could be controlled independently, translated or reformatted tool outputs where necessary to match user expectations, and bypassed synthesis in certain deterministic cases to preserve control over critical messages

### 6.2 Mixed-Language Contexts

Some sessions contained both English and Swahili, which complicated simple language detection.

Resolution: To resolve this, the system expanded language-context detection beyond simple text checking, included assistant history in the context window so prior language choices would be remembered, applied deterministic translation to booking and slot messages rather than relying on open-ended generation, and localized appointment-type values so that system output would always match the user's language
### 7.1 Rate Limits

When upstream service limits occurred, the assistant needed to remain responsive instead of failing silently.
 The solution used recent conversational signals instead of checking only the single most recent message, favored the dominant local context in booking flows so the language used at the start would be maintained through the booking process, and
### 7.2 Conflict Warnings

The booking system also had to report overlapping appointment warnings rather than suppress them.

Resolution:

1. retained conflict detection results in the final response;
2. warned the user while still completing the booking;
3. preserved user awareness of schedule overlap risk.

## 8. Validation Logic

Validation was performed at several levels:

1. parser validation for service, date, and time;
2. workflow validation for state transitions;
3. tool validation for required booking fields;
4. localization validation for final outputs;
5. end-to-end validation through realistic scenarios.

This layered validation approach was essential because failure could occur at more than one point in the pipeline.

## 9. What the Troubleshooting Taught the Design

The debugging process led to several design lessons:

1. language models are excellent interpreters but unreliable executors without constraints;
2. booking systems must be stateful and not purely conversational;
3. multilingual support must include the final confirmation layer;
4. deterministic recovery is more valuable than elegant failure;
5. fewer degrees of freedom can produce a more dependable user experience.

## 10. Documentation Value

This troubleshooting journal has thesis value because it makes the artifact evolution visible. It shows that reliability was not assumed but designed, tested, and improved through iterative corrections.

## 11. Conclusion

The final assistant behavior is best understood as the result of successive validation cycles rather than a single design decision. The system became more reliable because the implementation acknowledged and corrected its failure modes.
