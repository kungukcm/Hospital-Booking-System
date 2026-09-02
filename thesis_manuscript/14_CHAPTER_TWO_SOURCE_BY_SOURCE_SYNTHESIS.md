# CHAPTER 2 SUPPLEMENT B. SOURCE-BY-SOURCE SYNTHESIS

## Purpose

This chapter supplement provides a compact critical synthesis of each reference in the provided folder and maps each source to the design and evaluation decisions used in this thesis.

## S1. A Framework for Chatbots in Medical Practice

This source contributes foundational framing for chatbot role boundaries in medical environments. It distinguishes informational and administrative chatbot functions from clinical decision authority. That distinction informs this thesis design choice to constrain the assistant to appointment operations and avoid diagnostic outputs. The source also highlights structured user-flow design and controlled dialogue transitions as safety enablers. In the present study, these ideas are reflected in deterministic state gates that enforce required booking details before transaction execution. The source is particularly relevant to governance posture, emphasizing that implementation quality depends on both technical rigor and process accountability.

## S2. A Literature Survey of Recent Advances in Chatbots

This survey provides broad historical context from rule-driven to neural and transformer-based chatbot paradigms. It supports the argument that language flexibility has increased significantly while controllability has become a greater challenge. For this thesis, the source supports adoption of a hybrid architecture where generative language capabilities are retained but bounded by deterministic transaction controls. It also motivates a comparative view of chatbot quality metrics, extending beyond user satisfaction to include completion reliability, recovery behavior, and action precision.

## S3. AI-Powered Chatbots for Mental Health Support

Although domain-specific to mental health support, this source provides valuable insights on accessibility and always-on support structures. It highlights benefits in reducing access friction and stigma barriers, which parallels appointment-access challenges in general hospital workflows. At the same time, it reinforces role-boundary concerns and the need for escalation pathways when cases exceed safe automation scope. This thesis adapts these lessons by requiring non-clinical framing and explicit handoff readiness as part of deployment governance recommendations.

## S4. Bibliometric Analysis of Chatbots in Health

The bibliometric perspective shows rapid growth and topic diversification in health chatbot scholarship, especially around personalization and AI-enabled conversational agents. For this thesis, the source provides macro-level justification that healthcare chatbot deployment is not experimental fringe but an accelerating area of practice and research. It also indicates that reliability and evaluation practices remain uneven, reinforcing the contribution of this work in offering implementation-level reliability patterns.

## S5. Chatbots and Government Communications

This source contributes a public-sector communication lens where trust, clarity, and consistency are central. While not hospital-specific, it is relevant for understanding institutional communication obligations in high-stakes contexts. The thesis uses this lens to frame multilingual confirmation consistency as a public-value feature, not merely interface preference. It also supports governance arguments around transparency, accountability, and explainability in service messages.

## S6. Chatbots as a New User Interface for Health Information

This source highlights chatbot utility as a user-friendly access channel for health-related information, especially where users may prefer conversational over form-based interaction. The thesis builds on this by implementing a conversational interface for appointment operations. However, this study extends beyond informational use into transactional workflow completion, adding deterministic safeguards absent in many informational chatbot models.

## S7. Chatbots for Brand Representation

This source emphasizes consistency of communication and user-perceived trust from interaction quality. Though commercial in orientation, it informs the thesis claim that inconsistency at critical interaction points can quickly erode confidence. Applied to healthcare booking, this translates into the need for coherent, complete, and language-aligned final confirmations.

## S8. Chatbots in Airport Customer Service

Airport service environments share high-volume, time-sensitive characteristics with hospital administrative workflows. This source provides transferable insights on use-case segmentation, expectation management, and escalation needs. The thesis uses these parallels to justify queue-aware recommendation and explicit fallback messaging.

## S9. Developing Chatbots in Healthcare: Systematic Review

This review strongly supports healthcare-specific implementation caution, noting recurring concerns around validity, integration, and user trust. The thesis draws on this evidence to justify controlled scope (administrative tasks only), deterministic flow control, and careful messaging around limitations.

## S10. Empathic Response Generation in Chatbots

This source contributes to understanding conversational quality dimensions that influence engagement and comfort. While empathy is less central in purely administrative scheduling than in counseling contexts, tone still matters for user confidence and compliance with required steps. The thesis incorporates this insight through polite, corrective, and language-sensitive prompts.

## S11. Ensuring Consumer Satisfaction with Chatbots

Satisfaction literature links trust with utility, clarity, and successful completion. This directly supports the thesis focus on completion reliability and interpretable outputs. In healthcare scheduling, completion outcomes are likely stronger predictors of satisfaction than stylistic fluency alone.

## S12. EREBOTS Privacy-Compliant Agent Platform

This source provides architecture-level privacy and compliance guidance for agent-based systems. It informs thesis recommendations on access control, data minimization, and auditability as prerequisites for production deployment.

## S13. Ethical Considerations in AI Chatbots for Culturally Sensitive Mental Health

This ethics-oriented source highlights cultural context and the risks of one-size-fits-all AI messaging. For this thesis, it strengthens the rationale for language inclusion and culturally appropriate communication strategies in Kenyan hospital settings.

## S14 and S15. Exploring the Potential of Chatbots in Mental Health (Duplicate Files)

These sources contribute evidence on practical chatbot support potential and limitations in sensitive domains. Their duplication in the folder is treated as one conceptual reference for synthesis. The study uses these insights to reinforce strict boundary setting and escalation preparedness.

## S16. Factors Influencing Patient Engagement in Mental Health Chatbots

This source is useful for identifying engagement factors transferable to hospital scheduling: clarity, responsiveness, personalization, and trust. The thesis applies these by ensuring context-aware prompts and explicit confirmation messaging.

## S17. LLM-Based Chatbots in Language Learning

Although education-focused, this source provides relevant observations on LLM adaptability and interaction quality in multilingual contexts. It supports the thesis decision to pair LLM flexibility with deterministic controls in action-critical outputs.

## S18. Natural Language Chatbots in Biomedical Contexts

This source supports the viability of NLP-driven interfaces in biomedical-adjacent tasks and provides domain relevance for language-based support systems. The thesis extends this into robust appointment transaction flows.

## S19. Proposed Use of Chatbots in Mental Health Support

The source contributes conceptual framing for efficacy and potential impact analysis. The thesis adapts this structure to administrative outcomes: completion quality, reliability, and communication clarity.

## S20. Revolutionizing e-Health with AI-Powered Chatbots

This source offers broad transformation narratives and practical opportunities in e-health. It helps frame this thesis within system-level modernization goals while highlighting that transformational claims must be tempered by governance and safety controls.

## S21. Technical Metrics Used to Evaluate Health Care Chatbots

This source is central to this thesis evaluation design. It supports use of measurable operational metrics and discourages overreliance on subjective conversation quality alone. The thesis reflects this through completion, recovery, and localization consistency criteria.

## S22. The Evolving Role of Virtual Health Assistants

This source provides a comprehensive overview of applications, benefits, and governance concerns. It is particularly useful for linking administrative task automation with operational efficiency and privacy considerations. The thesis leverages these themes in implementation and deployment-roadmap chapters.

## S23. Health Chatbots in Telemedicine Integration

This source contributes integration perspectives relevant to remote support and digital care continuity. The thesis uses this evidence to discuss scalability and future interoperability pathways.

## S24. The Role of Chatbots in Enhancing Customer Service

Customer service literature contributes practical understanding of expectation management, response-time value, and perceived convenience. The thesis adapts these into healthcare-specific quality criteria while acknowledging stronger risk constraints in clinical-adjacent settings.

## S25. Understanding How Chatbots Work: Exploratory Study

This source offers foundational conceptual clarity on chatbot mechanics and interaction flow structures. It supports the thesis architecture discussion, particularly around intent interpretation and structured dialogue progression.

## S26. Understanding the Limitations of AI Chatbots

This source reinforces caution regarding overconfidence in conversational AI. The thesis directly operationalizes this insight by introducing deterministic checks, fallback prompts, and explicit scope boundaries.

## S27. Use of Chatbots for Customer Service in MSMEs

This source adds practical adoption lessons for resource-constrained environments. Although not healthcare-specific, it supports the feasibility of phased rollout and low-cost automation benefits, both relevant for Kenyan institutional planning.

## Cross-Source Integration Summary

Across all sources, five converging principles emerge:

1. utility must be paired with control;
2. high-stakes domains require stronger safeguards;
3. trust depends on completion quality and clarity;
4. inclusion requires operational language consistency;
5. governance readiness is essential for sustainable deployment.

These principles directly inform the artifact and recommendations in this thesis.
