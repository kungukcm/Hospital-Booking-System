# CHAPTER 6. DISCUSSION

## 6.1 Introduction

This chapter interprets the evaluation findings reported in Chapter 5 in relation to the five research questions, the literature reviewed in Chapter 2, the specific context of Kenyan healthcare administration, and the broader implications for design and deployment of conversational AI in healthcare settings. The discussion moves progressively from specific findings to general principles, situating the evidence from this thesis within the wider conversation about healthcare AI design, multilingual digital health equity, and AI governance.

A central thread running through this discussion is the productive tension between conversational flexibility and operational reliability. The evaluation findings confirm that this tension is real: purely generative approaches do not reliably complete healthcare administrative transactions, while purely deterministic approaches lack the linguistic flexibility needed to serve diverse users. The hybrid architecture demonstrated in this thesis resolves the tension by applying each approach where it is most suitable: LLM capability for the interpretive and generative dimensions of interaction, deterministic logic for the transactional and localization dimensions. Understanding why this combination works and where its limits lie is the primary intellectual contribution of this discussion.

## 6.2 Interpreting Research Question 1: Architecture for Reliable Healthcare AI

Research Question 1 asked what modular architecture best combines conversational flexibility with reliable hospital transaction execution and what design principles should govern boundaries between components.

The evaluation provides clear evidence that the five-layer architecture with explicit separation of concerns at each boundary is effective. The most important boundary is between the intelligence layer (LLM) and the tool layer (transaction execution), mediated by the orchestration layer's validation logic. This boundary prevents conversational errors from becoming transactional errors, and preventing them is more efficient than detecting and correcting them after they occur.

The literature review established that hybrid architectures combining LLM flexibility with deterministic control are emerging as a consensus recommendation in reliability-critical AI applications (Caldarini et al., 2022). The present findings confirm this recommendation in a specific healthcare administrative context and provide design detail about how the boundary between layers should be implemented. Key boundary design principles that emerged from the evaluation are: the LLM suggests, deterministic logic validates; conversational errors produce clarifying questions, not transaction failures; and language understanding is separated from language output in critical messages.

The comparison between pre-guardrail and post-guardrail performance (85% vs. 100% completion rate) is particularly instructive. The improvement is not marginal; it represents elimination of a systematic failure class. In practical terms, an 85% completion rate means that one in six booking attempts fails, while a 100% rate means all booking attempts succeed when the user provides required information. The difference in patient experience between these scenarios is significant: in the 85% case, one in six users who attempts to book an appointment online will either not succeed or will not know whether they succeeded. In the 100% case, all users who provide the required information receive a confirmed booking.

This finding aligns with the literature on service quality in healthcare. Kim et al. (2023) found that administrative chatbot effectiveness was primarily determined by task completion reliability rather than conversational quality: users tolerate less-than-perfectly-natural conversation much more readily than they tolerate incomplete or uncertain task outcomes. The present findings confirm that in the specific context of appointment booking, reliability must be engineered into the architecture, not expected as a natural property of LLM-based conversation.

The modular architecture also has implications for institutional adoption and sustainability. Healthcare institutions are cautious technology adopters with good reason: failed technology deployments affect patient care. A modular architecture enables incremental adoption, where each layer can be tested and validated independently before integration. It also enables component upgrading: when a better LLM becomes available, it can be integrated into the intelligence layer without requiring changes to the orchestration, tool, or data layers. This flexibility supports long-term sustainability in a technology environment where AI capabilities are advancing rapidly.

## 6.3 Interpreting Research Question 2: Deterministic Guardrails and Booking Reliability

Research Question 2 asked how deterministic guardrail mechanisms affect booking completion quality, error recovery behavior, and user experience.

The evaluation findings provide strong evidence on all three dimensions. On completion quality, the improvement from 85% to 100% demonstrates that guardrails directly improve the reliability of the core function. This improvement came without degradation in the scenarios that were already working, confirming the design principle that guardrails should enhance reliability without reducing flexibility.

On error recovery, the five error recovery scenarios all produced appropriate system behavior with clear recovery paths available in each case. This finding is particularly important because it addresses a concern sometimes raised about deterministic controls: that they might produce rigid, unhelpful behavior when errors occur. The evaluation shows that deterministic controls can enforce required conditions while still generating helpful, context-appropriate error recovery guidance through the LLM layer.

On user experience, the evaluation did not measure user satisfaction directly (because the evaluation used researcher-conducted rather than user-conducted tests), but the qualitative assessment of system responses suggests that the deterministic controls are not visible to users as rigidity. The system's behavior throughout error scenarios was consistently helpful, specific, and recovery-oriented, consistent with the trust-building interaction patterns emphasized in the literature (Ensuring Consumer Satisfaction with Chatbots, 2022).

The design implication from Research Question 2 is that deterministic controls and LLM flexibility are complementary rather than competing. The LLM provides conversational naturalness and linguistic intelligence; the deterministic controls provide operational reliability. A system designer need not choose between them. The architectural challenge is placing each correctly: LLM judgment for interpretation and generation, deterministic logic for validation and execution.

A theoretical contribution emerges here that challenges a common framing in the chatbot literature. Earlier literature tended to position rule-based and generative systems as two ends of a spectrum where one must choose. Understanding How Chatbots Work: An Exploratory Study (2021) noted this binary framing as limiting research progress. The present thesis contributes empirical evidence that the binary is false: in the specific context of healthcare transactional chatbots, the most effective design uses both rule-based controls and generative language models, each for the functions it performs most reliably.

## 6.4 Interpreting Research Question 3: Queue-Aware Recommendations

Research Question 3 asked how predicted congestion indicators and interpretable queue recommendations can be integrated into conversational booking workflows to improve patient slot selection.

The evaluation found that the integration of queue recommendations into conversational booking is feasible and produces recommendation outputs that users can understand and act upon. The key design choices that supported this outcome were: presenting recommendations in plain language rather than technical metrics, including brief explanatory context that allows users to evaluate the recommendation, being transparent about prediction uncertainty, and integrating recommendations naturally into the booking conversation without requiring users to navigate a separate information-seeking process.

The 86% uptake rate for recommended slots in the scripted scenarios suggests potential for meaningful demand redistribution in real deployment. The literature review established that when patients have visibility into congestion, demand naturally distributes more evenly (Technical Metrics Used to Evaluate Healthcare Chatbots, n.d.; Factors Influencing Patient Engagement, n.d.). The present findings are consistent with this expectation, though the scripted nature of the evaluation limits the confidence with which this finding can be generalized to real patient behavior.

The uncertainty communication approach, using qualitative language ("typically shorter waiting times") rather than precise predictions, proved effective in the evaluation context. This aligns with the recommendation science literature's finding that interpretable rankings outperform precise predictions in decision support applications because users can reason about rankings and apply their own contextual knowledge, while precise predictions that do not materialize damage trust (Ensuring Consumer Satisfaction with Chatbots, 2022).

The integration of queue recommendations into conversational booking represents an advance over the standard appointment booking interface in two ways. First, it provides information that no current standard interface provides: expected congestion at the time of booking. Second, it provides this information in a contextually appropriate format, as part of a natural conversation rather than as a separate information-seeking task. These advances position the conversational interface as not merely a digital replacement for phone booking but as a qualitatively superior service channel.

An important limitation of the queue recommendation system is that the prediction model is calibrated to general hospital patterns rather than local data from a specific institution. In production deployment, the model would require calibration from actual appointment volume data to achieve the accuracy needed for predictions to be trusted consistently. The design of the calibration process, and the governance of model updates over time, are important implementation considerations that are beyond the scope of this prototype evaluation but should be central to production deployment planning.

## 6.5 Interpreting Research Question 4: Multilingual Localization Consistency

Research Question 4 asked how consistent language localization in transactional messages can be achieved throughout the full booking workflow without complete duplication of system logic.

The evaluation provides the clearest and most unambiguous findings in the study on this research question. The improvement from 57% to 100% consistency in transaction-critical outputs using deterministic localization, against the 100% consistency in English outputs throughout, demonstrates conclusively that LLM-based language consistency is insufficient for transaction-critical messages in multilingual contexts and that deterministic localization addresses this gap completely.

The theoretical significance of this finding extends beyond the specific Kenyan English-Swahili context. The language drift problem is a structural property of language models trained on multilingual data: the model's output language is influenced by the language of the immediate context, the language of the specific content being expressed (technical terms tend toward the language of technical literature), and the distribution of training data (which typically overrepresents English). When any of these influences pulls the output toward a non-user-preferred language at a critical output point, language drift occurs.

The deterministic localization solution addresses this by removing language-consistency decisions from the probabilistic model for transaction-critical messages. The solution is not "better prompting" or "a more advanced language model" but architectural separation: transaction-critical messages are templates populated with data, not natural language generated by a model. This solution is simple, effective, and robust to model changes. When the LLM is upgraded, the localization templates remain effective. When a new language is added, it requires adding a new set of templates, not retraining the model.

This finding has implications for other multilingual chatbot deployments beyond healthcare. Any domain where transaction-critical messages must be delivered consistently in the user's preferred language would benefit from this architectural approach. Banking (transaction confirmations), government services (application status notifications), and logistics (delivery confirmations) all have the same requirement and could benefit from the same solution.

The literature reviewed in Chapter 2 identified multilingual transactional consistency as an underexplored area (Chatbots as a New User Interface for Providing Health Information, 2018; LLM-Based Chatbots in Language Learning, 2024). This thesis contributes both the identification of the problem and a practical solution, filling a genuine gap in the design knowledge for multilingual conversational AI.

## 6.6 Interpreting Research Question 5: Governance and Policy Alignment

Research Question 5 asked what ethical safeguards, accountability mechanisms, audit capabilities, and governance controls are necessary for responsible deployment in Kenyan hospital contexts.

The governance evaluation found that the artifact's built-in controls address the primary governance requirements identified in the literature review and in Kenya's Data Protection Act. Audit log completeness at 100%, data minimization compliance, scope adherence, and escalation routing together constitute a governance-ready foundation for institutional deployment.

The deeper insight from the governance evaluation is that governance controls are most effective when they are built into the system architecture rather than applied as external oversight mechanisms. When audit logging is a structural feature of the data layer, it cannot be disabled or circumvented by component changes elsewhere. When scope adherence is part of the LLM system prompt and validated by intent classification, it is consistently enforced across all interactions. When data minimization is a property of the data schema (the schema has no fields for clinical data), it is structurally enforced rather than dependent on user compliance.

This "governance by design" approach, documented in the literature on privacy by design (EREBOTS, 2021) and in bioethics-informed AI design frameworks, represents an important shift from the traditional model of governance as external oversight. External governance mechanisms, audit committees, regulatory inspections, incident reporting requirements, remain important and are not replaced by built-in governance controls. But built-in controls establish a baseline of responsible behavior that external oversight can then verify and improve.

The Kenyan context introduces specific governance considerations not fully addressed in literature generated in high-income country settings. The Data Protection Act (2019) requirements for explicit consent, purpose limitation, and data security are addressed in the artifact's design through: the scope disclaimer provided at session start (establishing scope and implicitly gathering informed consent for the described use), the data minimization design (purpose limitation in practice), and the session-state-clearing mechanism (data security through minimizing data persistence).

The governance framework documented in this thesis also addresses institutional accountability questions that are often left unaddressed in research prototypes: who is responsible if the chatbot produces an incorrect booking? What escalation processes must exist? What training do staff require? What audit review processes are needed? These questions are addressed in the governance framework section of this thesis, providing hospitals with a practical starting point for developing AI governance policies specific to their institutional context.

## 6.7 Broader Implications for Healthcare AI Design

### 6.7.1 The Case for Hybrid Architecture as a Standard Approach

The collective evidence from this thesis makes a strong case that hybrid conversational-deterministic architecture should become the standard approach for healthcare administrative AI, replacing both purely rule-based and purely generative alternatives. The specific evidence base includes: better reliability outcomes than purely generative approaches, better linguistic flexibility than purely rule-based approaches, and compatibility with the trust-building, error-recovery, and governance requirements that healthcare deployment demands.

The design principle that enables this combination is boundary clarity: the boundary between LLM and deterministic components must be precisely defined and consistently enforced. When the boundary is clear, each component can be designed and optimized for its function without interfering with the other. When the boundary is blurry or inconsistent, the benefits of the hybrid approach are undermined.

### 6.7.2 Implications for Digital Health Equity

The findings on multilingual localization have direct implications for digital health equity. The Kenyan context makes the equity implications visible: if transaction-critical messages are delivered in English to Swahili-speaking patients, those patients receive a lower quality of service than English-speaking patients, even if the booking function completes correctly. The information that matters most (what was booked, when, where, and what to do) is delivered in a language the patient may not confidently read.

The deterministic localization approach demonstrated in this thesis is a concrete technical mechanism for achieving language equity in conversational health services. Institutions implementing this approach can provide genuinely equivalent service quality to speakers of all supported languages, not merely cosmetic multilingual support. This distinction matters for health equity: cosmetic multilingual support can actually be worse than no multilingual support, because it creates the expectation of equitable service while failing to deliver it.

### 6.7.3 Implications for AI Governance in Low-Resource Settings

The governance framework documented in this thesis was developed for the Kenyan context but draws on principles with wider applicability. The finding that governance by design is more effective than governance by oversight alone applies in any institutional context. The specific governance mechanisms documented (audit logging, data minimization, scope enforcement, escalation routing) address requirements that exist in most jurisdictions where healthcare AI might be deployed.

For low-resource settings specifically, the governance framework addresses an important practical concern: governance in these settings must be achievable without large compliance staff or sophisticated monitoring infrastructure. The governance controls implemented in this artifact are automated and do not require manual compliance processes for routine operation. They do require institutional policies for when human review is triggered and what action is taken, but the collection of evidence for review is automated.

### 6.7.4 Design Science as an Appropriate Methodology

The design science approach adopted in this thesis proved well-suited to the research problem. The iterative design process allowed progressive resolution of challenges that interacted in ways not fully predictable before implementation. The five design cycles addressed increasingly sophisticated challenges, with each cycle building on the stable foundation provided by the previous cycle. This progressive complexity management is a structural feature of iterative design science that is particularly valuable for complex socio-technical problems.

The dual contribution of DSR, producing both an evaluable artifact and generalizable design knowledge, is appropriate for a field (healthcare conversational AI) where both kinds of contribution are needed. The artifact demonstrates feasibility and provides a replicable implementation model. The design knowledge, embodied in the architecture, the design principles, the evaluation framework, and the governance controls, can be applied beyond the specific artifact to inform similar implementations.

## 6.8 Study Limitations and Their Implications

The study has several limitations that contextualize the strength of evidence for the findings.

The most significant limitation is that evaluation was conducted with scripted scenarios and synthetic data rather than real patients and natural interaction. This means that user behavior patterns unique to natural healthcare contexts, including anxiety, technical difficulties, and unexpected questions, were not tested. The controlled evaluation is best understood as evidence of the system's technical capability rather than evidence of its real-world effectiveness with actual patients. Pilot deployment with real patients is the essential next step for establishing real-world effectiveness.

The researcher-conducted evaluation introduces the risk of inadvertent bias, as noted in the methodology chapter. Independent evaluation by researchers not involved in system development would provide stronger evidence, and evaluations with actual hospital staff and patients would be most persuasive to institutional decision-makers.

The Swahili evaluation was conducted by a non-native Swahili speaker who can assess functional accuracy but may not assess naturalness of expression with the sensitivity of a native speaker. Native speaker evaluation of the Swahili localization is needed, particularly for the template-generated transaction-critical messages, which must be not only accurate but natural and reassuring to Swahili-speaking patients.

The queue prediction model is calibrated to general hospital patterns rather than data from a specific Kenyan hospital. While the model is structurally sound and produces internally consistent predictions, its accuracy for a specific hospital context would require validation against actual appointment volume data from that hospital. This calibration is achievable but requires institutional data access beyond what is available for the prototype evaluation.

## 6.9 Chapter Summary

This discussion chapter has interpreted the evaluation findings across all five research questions, situating them within the existing literature and drawing out implications for theory, practice, and policy. The central finding, that hybrid conversational-deterministic architecture effectively addresses the tension between conversational flexibility and operational reliability in healthcare administrative AI - is supported by quantitative evidence from the reliability and localization comparisons and by qualitative assessment of the governance evaluation.

The discussion contributes to theory by providing a concrete, evaluated example of hybrid architecture in a healthcare context, advancing the understanding of how rule-based and generative components can be combined productively. It contributes to practice by providing design principles and governance guidance that healthcare institutions can apply to their own implementations. It contributes to policy by demonstrating technical approaches to achieving language equity and governance by design that can inform digital health policy at the national level.

The limitations of the study identify a clear research agenda: pilot deployment with real patients to validate real-world effectiveness, native-speaker Swahili evaluation of localization quality, calibration of the queue prediction model with real hospital data, and independent evaluation by researchers not involved in system development. These steps are addressed in the recommendations and future work sections of the concluding chapter.
