# CHAPTER 2 SUPPLEMENT. DETAILED LITERATURE SYNTHESIS

## A. Purpose of This Supplement

This supplement deepens Chapter 2 by providing a structured synthesis across all references supplied in the project repository. It organizes evidence around conceptual themes directly relevant to the artifact designed in this thesis: conversational reliability, queue-aware operations, multilingual inclusivity, patient trust, and governance.

## B. Thematic Synthesis Matrix

### Theme 1: Chatbot Evolution and Capability Trajectory

The reviewed works collectively show three major phases of chatbot development.

1. Rule-based systems emphasized deterministic responses and predictable outcomes but were narrow in coverage.
2. Data-driven conversational systems expanded adaptability but required training resources and domain engineering.
3. LLM-era systems introduced broad linguistic flexibility and lower intent-engineering overhead, while creating new reliability concerns in action-constrained workflows.

Across non-health sectors, this trajectory is associated with improved responsiveness and reduced service response time. However, the same literature highlights a persistent mismatch between conversational quality and transaction completion quality. The practical implication for healthcare is that model capability cannot substitute for process control.

### Theme 2: Healthcare Chatbots as Administrative Infrastructure

Many references describe healthcare chatbot opportunities through patient communication and education lenses. Fewer works provide concrete operational architecture for appointment workflows under administrative constraints. The references nevertheless converge on two important insights:

1. Administrative use cases are suitable early deployment targets because they are high-volume and repetitive.
2. Healthcare chatbots require tighter quality boundaries than generic customer-service bots due to direct implications for service access.

The artifact in this thesis aligns with this evidence by focusing on non-clinical appointment operations and explicitly separating administrative support from clinical decision making.

### Theme 3: Reliability Under LLM-Based Interaction

The references discussing contemporary AI limitations reinforce a core design concern: generative systems can produce coherent text while still violating operational constraints. In transactional domains this appears as malformed calls, skipped prerequisites, or inconsistent action sequencing.

This literature finding justifies the deterministic guardrail strategy used in the artifact. Rather than viewing guardrails as fallback patches, this thesis treats them as foundational reliability architecture.

### Theme 4: Engagement, Trust, and User Confidence

Studies focused on user satisfaction and engagement indicate that trust in chatbots is strongly linked to perceived clarity and successful completion. Users are more tolerant of constrained interaction if outcomes are accurate and transparent.

In hospital booking workflows, trust is especially sensitive to final-step messaging. A user who receives unclear or language-inconsistent confirmation may question whether a booking was actually recorded. This insight informed deterministic localization at transaction completion points.

### Theme 5: Queue Visibility and Operational Choice Support

References addressing technical evaluation and service impact suggest that chatbot quality should include process performance indicators. Queue-aware recommendations can reduce informational asymmetry by helping users choose lower-burden slots when possible.

This thesis operationalizes that principle by presenting ranked slot options with congestion levels, estimated waits, and confidence. The intention is not to claim perfect prediction but to improve decision quality under uncertainty.

### Theme 6: Ethics, Privacy, and Governance

The ethics-oriented references emphasize that healthcare AI must remain accountable, transparent, and bounded. Relevant governance dimensions include:

1. explicit role communication;
2. purpose-limited data collection;
3. privacy and access controls;
4. fair service availability;
5. human oversight for exceptions.

The privacy-compliant platform literature provides practical direction for auditability and control design. This thesis extends those principles to a Kenyan administrative deployment context.

## C. Comparative Conceptual Positioning

This section positions the thesis artifact relative to dominant chatbot design approaches.

### C.1 Purely Generative Conversational Design

Strengths:

1. natural language breadth;
2. high flexibility with varied user phrasing;
3. lower up-front intent rule authoring.

Limitations in healthcare booking:

1. weak guarantee of required field completeness;
2. potential schema mismatch in tool actions;
3. inconsistent multilingual transaction outputs.

### C.2 Rule-Heavy Deterministic Design

Strengths:

1. predictable action behavior;
2. strong control of transaction state;
3. easier formal verification.

Limitations:

1. rigid language handling;
2. lower tolerance for varied user phrasing;
3. higher friction in open-ended conversation.

### C.3 Hybrid Conversational-Deterministic Design (This Thesis)

Strengths:

1. natural language interaction with controlled transaction execution;
2. improved completion reliability;
3. explicit multilingual transaction consistency;
4. interpretable queue recommendation outputs.

Trade-offs:

1. greater implementation complexity;
2. need for careful boundary maintenance between model and rules;
3. ongoing calibration for recommendation quality.

## D. Literature-Derived Design Requirements

The synthesis yields concrete design requirements adopted in the artifact.

1. The assistant must collect and validate mandatory booking identifiers before transaction execution.
2. The assistant must recover gracefully from short or partial user replies.
3. The system must present queue-aware options in interpretable terms.
4. The system must ensure language consistency in final transactional messages.
5. The deployment model must include governance controls for privacy and accountability.

## E. Research Gap Revisited

Based on the synthesis, the research gap can be restated as follows:

There is limited practical evidence on healthcare administrative assistants that simultaneously combine deterministic transaction reliability, multilingual transactional consistency, and patient-facing queue optimization in a policy-aware design for Kenyan contexts.

The artifact and evaluation in this thesis directly target that combined gap.

## F. Implications for Evaluation Criteria

The literature synthesis informs the final evaluation criteria used in this study.

1. Reliability criterion: Can the system complete booking workflows without invalid transaction attempts?
2. Clarity criterion: Are slot options and final confirmations understandable and actionable?
3. Inclusion criterion: Are Swahili and English transactional outputs consistent with user language context?
4. Governance criterion: Does the implementation support traceability, bounded scope, and operational accountability?

## G. Extended Critical Reflections

### G.1 On Generalizability

Much chatbot literature is domain-generic. Healthcare administration imposes stronger constraints. Therefore, direct transfer of findings from customer service should be cautious and control-enhanced.

### G.2 On Evaluation Bias

Studies frequently overemphasize conversational satisfaction while underreporting transaction failure rates. This thesis addresses that imbalance by prioritizing completion behavior and state correctness.

### G.3 On Language Equity

Multilingual support is often framed as interface localization. The reviewed evidence suggests a stronger requirement: end-to-end operational language equity, including confirmations and action-critical labels.

### G.4 On Policy Readiness

Technical feasibility does not imply governance readiness. Responsible deployment requires organizational processes, incident pathways, and explicit accountability structures.

## H. Synthesis Summary

The literature strongly supports the thesis position that healthcare chatbot success should be measured by trustworthy operational outcomes. The hybrid architecture developed in this study is consistent with evidence on reliability needs, inclusion priorities, and governance obligations.
