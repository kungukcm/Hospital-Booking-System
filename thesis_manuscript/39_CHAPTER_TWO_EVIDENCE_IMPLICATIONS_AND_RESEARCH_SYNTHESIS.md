# CHAPTER 2 SUPPLEMENT F. EVIDENCE IMPLICATIONS AND RESEARCH SYNTHESIS

## 1. Introduction

This supplement consolidates the evidence reviewed across the literature into a tighter set of research implications. The goal is to connect what the sources say with what this thesis actually builds and evaluates.

## 2. Core Evidence Pattern

Across the provided sources, a consistent pattern appears:

1. chatbots can improve access and convenience;
2. the benefit weakens when the system cannot reliably complete tasks;
3. trust depends on clear and predictable outputs;
4. governance and privacy concerns remain central in health settings;
5. multilingual inclusion strengthens access and perceived legitimacy.

This pattern strongly supports the architectural choices used in the thesis.

## 3. What the Literature Implies for Hospital Scheduling

The literature implies that hospital scheduling assistants should do more than answer questions. They should:

1. interpret user intent from natural language;
2. maintain state across turns;
3. guide users through incomplete information;
4. present interpretable appointment options;
5. return clear and localized confirmations;
6. avoid overclaiming clinical capability.

These requirements map directly onto the prototype design.

## 4. Evidence on Reliability

Reliability is the central differentiator between a useful chatbot and a frustrating one. The literature repeatedly points to the same lesson: users are willing to accept a machine interface if it can complete the intended job.

In administrative healthcare tasks, this means the system must be able to:

1. collect mandatory information;
2. preserve context;
3. handle short replies;
4. recover from partial or missing information;
5. provide final confirmation without ambiguity.

## 5. Evidence on Queue Awareness

The literature on service efficiency and technical evaluation suggests that response quality alone is not enough. In many environments, timing matters. A chatbot that can suggest less congested slots contributes to more efficient service use.

This thesis therefore treats queue-aware recommendation as a meaningful extension of chatbot utility.

## 6. Evidence on Language Inclusion

Language inclusion is treated in the literature as a broad accessibility issue, but the thesis argues for a more operational interpretation. It is not sufficient for a system to be generally bilingual if the final transaction still defaults to one language.

The evidence implies that:

1. the final confirmation must be readable in the user’s language context;
2. appointment-type values should also be localized;
3. follow-up prompts should remain consistent with the same language choice.

## 7. Evidence on Governance

The literature consistently warns that AI in healthcare must be controlled, auditable, and limited in scope. This supports the thesis decision to avoid diagnostic behavior and to build explicit escalation pathways.

The implication is clear: governance is not a final chapter add-on. It is part of the system’s basic acceptance conditions.

## 8. Research Synthesis Statement

From the literature, the thesis derives the following synthesis statement:

A hospital appointment assistant will be most effective when it combines natural language flexibility, deterministic workflow control, queue-aware recommendation, multilingual transactional consistency, and governance readiness.

## 9. Contribution of the Thesis

This thesis contributes an implementation pattern that demonstrates how the synthesis statement can be operationalized in practice. It fills the gap between conceptual discussion and working artifact behavior.

## 10. Conclusion

The evidence base does not merely support the thesis; it directs it. The artifact is a response to the recurring findings across the literature, especially around reliability, trust, inclusion, and governance.
