# CHAPTER 5 SUPPLEMENT D. EXTENDED CASE TRANSCRIPTS AND ANALYTICAL VIGNETTES

## 1. Introduction

This supplement adds narrative-style case vignettes that illustrate the assistant’s behavior under different interaction conditions. The aim is to make system performance easier to understand in thesis form.

## 2. Vignette 1: Standard English Booking Flow

A patient opens the assistant and asks to book an appointment. The assistant asks for patient details, service type, date, and time in sequence. The patient provides the necessary information step by step. The assistant returns a structured booking confirmation with appointment ID, wait estimate, and congestion level.

Analytical point:

This vignette demonstrates the baseline intended workflow. Its significance lies in showing that the system can support a complete transactional path without external intervention.

## 3. Vignette 2: Swahili Booking Flow

A patient begins in Swahili and continues in Swahili through the booking process. After the final time selection, the system returns a fully localized confirmation, including appointment type value translation.

Analytical point:

This vignette demonstrates the localization principle in action. It shows that language consistency must extend all the way to the confirmation block to preserve user confidence.

## 4. Vignette 3: Service-Only Interaction

The user says only the desired service, such as a specialty or general checkup. The system identifies the service and asks for the preferred date. This prevents the assistant from prematurely guessing the full booking details.

Analytical point:

The system’s ability to continue the booking process without losing context improves user experience and reduces repetition.

## 5. Vignette 4: Date-Only Interaction

The user gives only a preferred date after the service has already been established. The assistant returns ranked slots with congestion labels. This supports informed slot choice instead of forcing the user to wait for the system to infer what to do next.

Analytical point:

This vignette illustrates how deterministic branch logic improves progression in partially specified conversations.

## 6. Vignette 5: Time-Only Completion

After earlier context exists, the user simply sends a time such as 09:30. The system uses the stored service and date context, then books the appointment directly. The user is not required to restate prior information.

Analytical point:

This is an important usability feature because natural conversation rarely follows rigid form-style structure.

## 7. Vignette 6: Missing Details at Booking Stage

A user attempts to finalize a booking without providing all mandatory personal details. The assistant blocks completion and requests only the missing items.

Analytical point:

This behavior demonstrates transaction safety. It avoids incomplete bookings and guides the user toward correction rather than silent failure.

## 8. Vignette 7: Congested Slot Alternative Suggestion

A user expresses preference for a time that the system detects as congested. The assistant does not simply accept the selection without comment; instead, it offers a better set of alternatives with lower predicted waiting time.

Analytical point:

This vignette shows the value of queue-aware intelligence. The assistant becomes a decision-support tool, not just a booking relay.

## 9. Vignette 8: Tool Error Recovery

A tool call fails because of model-side formatting or upstream limitations. Rather than letting the session collapse, the assistant gives a user-facing recovery message and suggests rephrasing or waiting briefly.

Analytical point:

This case is important because good systems are defined not only by success cases but also by how they recover from failure.

## 10. Vignette 9: Conflict Warning

The booking tool detects an overlap with an existing appointment. The assistant still returns the confirmation but includes a warning about the overlap. This ensures the user is not left unaware of possible schedule conflicts.

Analytical point:

Conflict warnings enhance transparency and can support better scheduling decisions.

## 11. Vignette 10: Mixed-Language Conversation

The user alternates between English and Swahili within the same conversation. The assistant maintains a coherent flow and uses the dominant language context to guide outputs.

Analytical point:

This vignette supports the claim that multilingual systems must be robust to real-world code-switching rather than assuming one-language purity.

## 12. Interpretive Summary

These vignettes collectively show that the assistant is more than a basic chatbot. It is a workflow-sensitive, context-aware, multilingual service interface with deterministic safety mechanisms.

## 13. Implication for Thesis Evaluation

The use of vignettes in the thesis helps bridge the gap between technical outputs and human-readable evidence. They are especially useful for advisors and examiners who want to see how the artifact behaves in realistic service situations.

## 14. Conclusion

The case vignettes provide a richer picture of assistant behavior across common and edge-case interactions. They reinforce the thesis claim that reliability, language consistency, and queue awareness are all necessary components of a usable hospital appointment assistant.
