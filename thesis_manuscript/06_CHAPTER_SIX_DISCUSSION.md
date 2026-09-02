# CHAPTER 6. DISCUSSION

## 6.1 Introduction

This chapter interprets the results in relation to research questions, literature themes, deployment implications for Kenyan healthcare settings, and broader contributions to digital health scholarship. The discussion moves from specific findings to higher-level implications about how conversational AI should be designed and deployed when reliability and inclusion matter.

## 6.2 Interpreting the Core Finding: Reliability Through Hybrid Architecture

The central finding from evaluation is that conversational AI capability alone is insufficient for high-stakes administrative workflows. Purely generative models can fail at transactional tasks through tool-call errors, parameter omission, and silent failures. Instead, reliable hospital scheduling support emerges from a hybrid model where conversational flexibility and deterministic controls balance each other: natural language understanding remains with the LLM, but transaction-critical decisions (data validation, state transitions, parameter checking) are governed by deterministic rules.

This finding directly addresses a gap in literature where much LLM research emphasizes improving conversational quality (BLEU scores, coherence metrics, task completion through LLM-generated reasoning) but less attention is paid to what happens after the conversation when the system must execute real-world operations with consequences. Healthcare requires that the conversation is natural but also that the operation succeeds correctly. The hybrid approach makes this trade-off explicit: allow flexibility in dialogue, enforce rigidity in transactions.

The alignment with literature on AI in critical systems is clear. Autonomous systems for high-stakes decisions (medical diagnosis, drug dosing, autonomous vehicles) typically separate the perception/reasoning layer from the action execution layer, enforcing validation between layers. This thesis applies the same principle to conversational AI, demonstrating that the same separation improves healthcare administrative chatbots.

## 6.3 Implications for Research Question 1: Architectural Design

**Research Question 1 Asked:** What modular architecture best combines artificial intelligence conversation flexibility with reliable hospital transaction execution?

**Findings:** The layered architecture (interface → orchestration → intelligence → tools → data/logging) successfully separated concerns and enabled targeted reliability improvements. Key architectural features that proved effective:

**Separation of Language from Transaction.** The LLM never directly executes transactions. Instead, it interprets user language and suggests actions; deterministic logic validates these suggestions before execution. This separation meant that conversational errors (misunderstanding, uncertainty) did not translate into transactional errors. When the LLM was unsure what the user meant, it could ask clarifying questions, and the user could correct. Only when the system was certain did it proceed with action.

**State Machine Orchestration.** The graph-based workflow ensured the system never attempted an operation out of sequence. The system could not try to book without collecting patient details first, no matter what the user said. This prevented a class of errors: "I thought I said my name, why is the system asking again?" The state machine provided a shared understanding between system and user about what step was currently active.

**Tool Abstraction and Schema Enforcement.** Tools had explicit schemas (required parameters, return types). The system validated parameters before tool invocation. This prevented malformed requests from reaching the backend system. In effect, the tool layer provided a contract: if the system calls a tool, the tool receives valid parameters.

**Modularity and Maintainability.** The separation into distinct layers meant that improvements in one layer did not require changes elsewhere. For example, the language model could be upgraded (new version, different vendor) without changing orchestration or tool logic. This modularity is important for sustainability: as technology evolves, components can be updated incrementally.

**Architectural Contribution:** This thesis demonstrates that layered architecture with explicit separation of concerns is viable and beneficial for healthcare chatbots. The approach is not novel in software engineering (layered architecture is standard), but its application to healthcare conversational AI and the specific attention to transaction reliability fills a gap. Future healthcare AI work can build on this architecture pattern.

## 6.4 Implications for Research Question 2: Deterministic Guardrails and Reliability

**Research Question 2 Asked:** How do deterministic guardrail mechanisms affect completion quality and error recovery in booking workflows?

**Findings:** Deterministic guardrails materially improved booking reliability across multiple dimensions:

**Incomplete Booking Prevention.** Mandatory detail enforcement ensured that no booking executed without patient name, ID, phone, and email. In pre-guardrail testing, the system occasionally attempted bookings with incomplete data; post-guardrail, zero incomplete bookings occurred. This shift from 85% to 100% completion rate is not merely a metric improvement—it represents elimination of a class of failure mode.

**Sequence Consistency.** The state machine enforced that the system moved through booking stages in logical order: request understanding → detail collection → service confirmation → date selection → time selection → confirmation. Users could provide information out of order, but the system would not proceed to the next stage until previous stages were satisfied. This structure prevented confusions like "the system is asking for date but I haven't confirmed the service yet."

**Invalid Tool Call Prevention.** Pre-guardrail, the system occasionally generated malformed tool calls (missing required parameters, invalid service type, invalid date). Post-guardrail, validation logic caught 100% of these before execution. The backend system never received an invalid request. This reliability is critical for institutional trust: hospitals need to know that tool failures are impossible, not merely rare.

**User-Directed Error Recovery.** When errors occurred (e.g., service not recognized, date in past), the system did not fail silently. Instead, it explicitly reported the problem and guided recovery: "I don't recognize that service. Did you mean one of these?" This transparency is important for user confidence. Even if the error occurs, the user knows what happened and how to proceed.

**Theoretical Implication:** The study supports the thesis that deterministic control is compatible with conversational usability. Early chatbot research sometimes positioned deterministic systems (rule-based, tree-based) and conversational systems (generative, flexible) as opposites: either you had structure but no flexibility, or flexibility but no structure. This thesis demonstrates that they can coexist: a conversational interface with underlying deterministic controls. The determinism is not visible to users (they still experience natural conversation); it governs the parts where reliability matters.

## 6.5 Implications for Research Question 3: Queue-Aware Recommendations

**Research Question 3 Asked:** How can predicted congestion indicators and interpretable recommendations improve patient slot selection and demand distribution?

**Findings:** Queue recommendations successfully guided users toward lower-congestion slots and demonstrated interpretability:

**Demand-Shifting Potential.** In test scenarios, when recommendations explicitly labeled low-congestion slots as preferred, users shifted their choices accordingly (80% selection rate for recommended slots in test scenarios). This behavior suggests that queue visibility can influence patient decisions. In a real deployment with many patients, such shifting could naturally distribute demand toward less-busy times, reducing peak-hour congestion.

**Interpretability as Key.** Queue recommendation value depends entirely on whether users understand it. The study found that abstract metrics ("Capacity: 67%") are not helpful, but relative rankings with explicit explanation ("This slot is recommended because it typically has shorter waits") are interpretable. Users could make rational decisions with this information. The inclusion of estimated waiting time (e.g., "est. 15 min") made the recommendation concrete.

**Uncertainty Transparency.** The system acknowledged that queue predictions are uncertain ("Estimated times based on typical patterns; actual waits may vary"). This honesty about limitations maintains user trust. If the system predicted "10 minute wait" with false confidence, and the actual wait was 45 minutes, user trust would erode. By instead saying "typically low wait," the system maintains credibility even when actual conditions differ.

**Operational Intelligence Integration.** Queue recommendations represent a shift from "fulfill patient request" (book the first available slot) to "optimize patient experience" (book the slot that minimizes burden). This shift requires integration of operational data (congestion, staffing) into decision support. The study demonstrates that this integration is feasible and valuable in conversational interfaces.

**Limitation and Future Work:** The queue prediction model used in this prototype is simplified (linear assumptions about service type, time of day, staffing). Production-grade deployment would require local hospital data to calibrate predictions. A hospital with different staffing patterns, different specialty demand, and different peak hours would need its own predictive model. The framework for integrating queue predictions is demonstrated; the prediction accuracy is context-dependent.

## 6.6 Implications for Research Question 4: Multilingual Localization Consistency

**Research Question 4 Asked:** What implementation approach ensures consistent language localization in transactional messages?

**Findings:** Deterministic localization of transactional blocks successfully eliminated language drift and maintained user language context through to final confirmations.

**The Language Drift Problem.** The starting problem was clear from literature and practice: multilingual systems would maintain language through conversational exchanges but revert to default (English) in critical transactional outputs. A patient having a successful Swahili conversation would receive an English booking confirmation, undermining the entire benefit of multilingual support. This problem arose because LLMs, even when instructed to maintain language, sometimes reverted to their dominant training language (English) especially in structured output.

**Deterministic Solution.** Rather than relying on the LLM to maintain language in transactional outputs, the system used deterministic translation: lookup tables mapping service types to Swahili/English, template strings with language placeholders, and explicit conditional logic checking user language before outputting confirmations. This approach was less flexible (no novel phrasings in transactional outputs) but guaranteed correctness. Users received confirmations that were reliable and consistent.

**Impact on Trust and Accessibility.** For Swahili-speaking users, having the final confirmation in their language signals that the system is designed for them, not merely localized as an afterthought. The booking confirmation is the most critical message—the user needs to understand exactly what was booked. Having this in their preferred language is not a cosmetic feature but a reliability feature.

**Policy Implication for Language Equity.** The study demonstrates that true multilingual support requires investment in transactional localization, not just conversational multilanguage capability. For healthcare systems aiming to serve diverse language communities, this means supporting language all the way through to the patient's most critical interaction with the system.

## 6.7 Policy, Governance, and Institutional Deployment Discussion

### 6.7.1 Accountability and Responsibility

Healthcare institutions deploying AI systems must maintain clear lines of accountability. The system should never execute consequential actions (booking, cancellation) without logged evidence of why it took that action. This thesis documents extensive logging: who sent which message, what entities were extracted, what operations were performed, what outcomes resulted. Logs enable post-hoc review if disputes arise ("Did I really book that appointment?").

Institutional policy should establish: (1) who is responsible for system correctness (vendor, institution, or both), (2) what support pathways exist if things go wrong, (3) how disputes about bookings or errors are resolved, and (4) who has access to audit logs and under what conditions. The system architecture supports these accountabilities through structured logging, but policy defines how logs are used.

### 6.7.2 Data Protection and Minimization

The system captures only operationally necessary data: patient name, ID, contact information, appointment details. It does not capture diagnosis, symptoms, medical history, or other clinical details. This minimization reduces both compliance burden (less sensitive data to protect) and risk (smaller data volume exposes fewer people if security is breached).

Institutional policy should specify: (1) who can access appointment data (receptionists, clinicians, administrators?), (2) how long data is retained (forever, or deleted after appointment completion?), (3) what security controls protect data (encryption, access logs), and (4) what happens if data is lost or breached. The system's role is to not collect unnecessary data; policy defines how to protect what is collected.

### 6.7.3 Equity and Inclusion in Design

Digital health initiatives can increase or decrease equity depending on design. A system available only in English reduces access for non-English speakers. A system with unreliable booking increases frustration for marginalized users who already face barriers. This thesis treated language inclusion and reliability as equity concerns, not luxury features.

For Kenyan hospitals aiming to serve inclusive populations, this means: (1) supporting multiple languages actively, not as an afterthought, (2) testing with actual speakers of each language to ensure quality is truly equivalent, (3) monitoring uptake across language groups (if Swahili speakers use the system at much lower rates, something is wrong), and (4) iterating based on user feedback from underrepresented groups.

### 6.7.4 Human Oversight and Escalation Pathways

AI systems should support human judgment, not replace it. The system is designed to escalate to human staff whenever: (1) user requests something the system cannot handle (complex rescheduling, special accommodations), (2) the system is uncertain (ambiguous requests), or (3) the user expresses distress or frustration. Clear escalation pathways maintain the human-in-the-loop principle essential for healthcare.

Institutional policy should define: (1) what criteria trigger escalation, (2) who receives escalations (which staff roles), (3) what response time is expected, and (4) how escalations feed back into system improvement (were there patterns in escalations that suggest the system needs redesign?).

## 6.8 Limitations of the Study and Implications for Generalization

Several important limitations affect how broadly findings can be generalized:

### 6.8.1 Controlled Testing vs. Real Deployment

Evaluation occurred with scripted test scenarios on a research workstation, not in a real hospital with real patients. Real-world behavior might differ due to: (1) unexpected user interactions the tests did not foresee, (2) load effects (how does the system behave when handling dozens of concurrent users?), (3) integration challenges (connecting to the actual hospital appointment system, not a simulation), and (4) organizational factors (staff resistance, workflow integration issues).

**Implication:** Results demonstrate feasibility and design patterns but do not prove real-world success. Institutional pilot deployment is the next essential step.

### 6.8.2 Simulated Data and Queue Models

Queue predictions were based on simplified assumptions and test data, not actual hospital queue behavior. A real hospital's congestion patterns depend on staffing levels, specialty demand, seasonal variation, and many other factors that the simplified model does not capture.

**Implication:** The framework for integrating queue predictions is demonstrated; prediction accuracy must be calibrated for each specific hospital.

### 6.8.3 Language Testing Limitations

While the system supports Swahili, most testing was conducted by researchers with varying Swahili fluency. A Swahili native speaker might identify language infelicities, unnatural phrasings, or cultural misunderstandings that research testers missed.

**Implication:** Pilot deployment should include formal testing with native speakers of each supported language and iterative refinement based on their feedback.

### 6.8.4 Limited User Studies

No formal user acceptance studies were conducted. User satisfaction, trust development, adoption rates, and long-term usage patterns are not measured. The 80% recommendation uptake rate observed in test scenarios might not predict real user behavior.

**Implication:** Pilot deployment should include user surveys, usage analytics, and qualitative interviews to understand actual user experience and satisfaction.

### 6.8.5 Prototype Scale and Performance

Performance was not evaluated under load (many concurrent users, high message volume). Latency, error rates, and reliability under stress are unknown.

**Implication:** Pre-production deployment should include load testing and performance optimization.

## 6.9 Theoretical Contributions and Future Scholarship Directions

This thesis contributes to scholarship in several directions:

**Design Science in Healthcare IT:** Demonstrates a concrete artifact-centered methodology for designing trustworthy healthcare administrative systems. Future work can build on this framework, extending it to other administrative tasks (staff scheduling, bed management) or other clinical domains.

**AI Governance in Low-Resource Contexts:** Demonstrates that governance-ready design (logging, escalation, data minimization) is compatible with and improves healthcare chatbot deployment in resource-constrained settings. Future work can operationalize governance frameworks for specific country contexts.

**Multilingual AI for Inclusive Health:** Challenges the assumption that English-language AI is sufficient for global health; demonstrates that true multilingual support requires investment in localization at all levels of system interaction. Future work can build on this framework to address multilingual design in other health applications.

## 6.10 Practical and Policy Recommendations

### 6.10.1 For Healthcare Institutions

1. **Architecture First.** When evaluating chatbot vendors or building systems, prioritize architectural separation of language interpretation and transaction execution. Ask vendors: "What prevents transactional errors from occurring?"

2. **Language Equity.** Treat multilingual support as a core requirement, not an optional feature. Evaluate language quality through user testing with native speakers, not just vendor demonstrations.

3. **Transparent Logging.** Require comprehensive logging and audit trails. Be able to answer questions like "What did the system tell this patient?" and "Why did this booking get canceled?"

4. **Pilot Carefully.** Deploy first at limited scale with strong human oversight. Monitor uptake, error rates, user feedback, and clinical impact before scaling.

### 6.10.2 For Policy Makers

1. **Set Governance Standards.** Establish national or institutional standards for healthcare AI including data minimization, accountability, escalation pathways, and language equity.

2. **Support Localization.** Fund multilingual AI development for healthcare; do not assume English-language systems are sufficient for diverse populations.

3. **Mandate Transparency.** Require that healthcare AI systems maintain audit trails, document decisions, and provide clear explanations to users.

4. **Invest in Capacity.** Ensure institutions have capacity (staff training, infrastructure, governance expertise) to deploy and monitor AI systems responsibly.

## 6.11 Chapter Summary

The discussion has interpreted results across research questions, explored implications for architecture, reliability, queue optimization, and multilingual inclusion, and situated the work within healthcare governance and policy contexts. Key findings support the value of hybrid conversational-deterministic design for healthcare administrative chatbots. The next and final chapter concludes the thesis with synthesis of contributions, remaining research gaps, and recommendations for future work.
