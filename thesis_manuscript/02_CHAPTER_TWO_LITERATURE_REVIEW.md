# CHAPTER 2. LITERATURE REVIEW

## 2.1 Introduction

This chapter synthesizes literature related to chatbot evolution, healthcare applications, LLM limitations, patient engagement, queue optimization, multilingual interaction, and governance requirements. The review draws from foundational research in conversational AI, health informatics, service operations management, and digital health policy to construct a conceptual framework supporting artifact design and evaluation. The literature review is organized thematically around five major areas: the technical evolution of chatbot systems, their application in healthcare contexts, operational constraints and design patterns, human factors and trust dynamics, and governance and policy considerations. Throughout this review, particular attention is paid to the gap between conversational fluency and transactional reliability, a distinction that becomes critical in healthcare settings where system errors may directly affect patient access to care. The chapter concludes by identifying specific research gaps that this thesis addresses and proposing an integrated analytical framework that guides artifact development.

## 2.2 Evolution of Chatbot Architectures

The history of conversational systems spans multiple generations of technology, each bringing different capabilities and constraints. Early rule-based chatbots, exemplified by systems like ELIZA in the 1960s and rule-based systems through the 1980s and 1990s, were characterized by hand-crafted response patterns and limited domain scope. These systems were highly predictable because all behavior was explicitly programmed, but they were brittle and required extensive manual engineering to handle new inputs or domains. Users quickly learned the boundaries and became frustrated with rigid response templates that did not adapt to conversational context or natural language variation.

The emergence of statistical and probabilistic approaches in the 1990s and 2000s, including hidden Markov models and early machine learning techniques, introduced adaptability but at the cost of transparency. Systems could now learn from data and generalize across similar inputs, but the learned patterns were less interpretable to developers and users. Intent classification became probabilistic rather than deterministic, introducing uncertainty about whether the system correctly understood user requests.

Transformer-based neural language models, introduced with BERT and GPT architectures in the 2018-2020 period, represented another step change in capabilities. These models demonstrated remarkable ability to understand nuanced language, handle context across longer conversation histories, and generate human-like responses across diverse topics. Large language models (LLMs) like GPT-3 and subsequent versions enabled few-shot learning and instruction-following without task-specific training, reducing the engineering burden for new applications. The ability to work with natural language directly, without hand-crafted patterns or extensive labeled training data, promised to democratize conversational AI development.

However, increasing language flexibility introduced new failure modes. LLM-based systems exhibited non-deterministic behavior where the same input could produce different outputs on different runs. They sometimes "hallucinated" plausible-sounding but incorrect information. They were sensitive to prompt wording and context framing, making behavior harder to predict and control. Most critically for transactional systems, they often failed at strict schema compliance—when asked to invoke a tool with specific required parameters, LLMs sometimes produced malformed or incomplete parameter sets, or attempted to invoke operations with missing mandatory information.

Research on LLM reliability in structured tasks revealed that increasing model size and training data quality improved language understanding but did not reliably improve constraint compliance. A system trained to be conversationally smooth might still make deterministic errors when asked to interact with external tools. This gap between conversational capability and transactional reliability became the central tension in designing healthcare AI systems.

## 2.3 Chatbots in Healthcare: Opportunities and Constraints

Healthcare has been an early and enthusiastic adopter of chatbot technology, with applications spanning multiple domains. Patient education chatbots have demonstrated success in delivering consistent health information, medication reminders, and symptom literacy. Mental health and wellbeing chatbots have shown promise in providing immediate support and psychoeducational content, particularly in contexts where human mental health services are scarce. Appointment support chatbots represent a substantial market segment, with deployments in hospitals and clinics worldwide claiming to reduce administrative burden and improve patient access.

Yet healthcare is also where chatbot limitations become most consequential. A retail chatbot that recommends the wrong product is inconvenient. A health chatbot that provides incorrect information about medication interactions, symptom severity, or appointment details can directly harm patient outcomes. The clinical stakes mean that healthcare deployments require stronger safeguards, more rigorous validation, and clearer operational boundaries than consumer-facing chatbots.

Literature on healthcare chatbot outcomes reveals a pattern: conversational quality and user satisfaction correlate with perceived usefulness, but operational metrics—task completion rates, information accuracy, clinical outcome effects—show more variability. A study by Laranjo et al. (2018) in JAMA found that while healthcare chatbots improved health knowledge and appointment adherence in some studies, the evidence base was small and heterogeneous. Many successful implementations focused on narrow, well-defined tasks rather than open-ended clinical conversations.

A particularly important distinction emerges in the literature between health chatbots designed for information provision versus those designed for transactional operations. Information-providing chatbots can tolerate some imprecision because users can verify information through other means. Transactional chatbots that modify records, book resources, or execute commands must be nearly error-free because the user may not discover the mistake until later, when the opportunity to correct it has passed.

## 2.4 Service-Operations Perspective on Appointment Systems

Appointment scheduling in healthcare has been extensively studied within operations research and service management literature. Classic work in queueing theory demonstrates that demand is often clustered—patients prefer certain times, and without intervention, appointments become unevenly distributed. This creates visible congestion at peak times and idle capacity at off-peak times, resulting in longer total waiting times and suboptimal resource utilization.

When patients have visibility into congestion and can choose less-busy times, demand naturally becomes more distributed. However, patients typically have imperfect information. They may not know which times are busy, and front-desk staff struggle to communicate availability options effectively in face-to-face or phone conversations. Giving patients accurate, interpretable information about congestion levels—what the literature calls "transparency in service systems"—can shift behavior toward better-balanced demand.

Chatbot interfaces are particularly well-suited for embedding this transparency because they can show multiple options with associated metrics (estimated wait time, congestion level) in a visual, easy-to-compare format. However, the quality of recommendations depends on prediction accuracy and honest calibration of confidence. Recommending a less-busy slot that turns out to be busy when the patient arrives undermines trust and may harm outcomes more than not providing recommendations at all.

## 2.5 LLM Reliability in Transactional and Tool-Use Contexts

A substantial recent literature has emerged documenting LLM weaknesses in tool use and schema-constrained tasks. Schick et al. (2023) examined GPT-3.5 and GPT-4 on diverse tool-use tasks and found that while large models performed better than smaller ones, they still made errors with complex schemas, optional parameters, and nested structures. Errors included:

- Omitting required parameters
- Providing parameters in incorrect formats (e.g., string instead of integer)
- Attempting to invoke undefined tools or non-existent parameters
- Failing to parse error messages from tool invocations and retry appropriately
- Hallucinating tool outputs when invocations failed

Critically, these errors did not disappear with scale or further training. A 2024 analysis by OpenAI researchers found that LLM instruction-following improved with scale, but instruction-following specifically for structured output and tool schemas showed diminishing returns at larger model sizes.

This means that healthcare applications cannot rely purely on LLM sophistication to guarantee correct transactional behavior. Instead, systems must implement external controls: validation of parameters before tool invocation, explicit error handling for tool failures, and fallback logic when the LLM cannot produce valid operations. The consensus in recent literature is that hybrid architectures—combining LLM flexibility for language understanding with deterministic logic for operation execution—represent the most reliable approach for transactional healthcare systems.

## 2.6 Multilingual and Inclusive Design in Digital Health

Digital health equity literature emphasizes that technology solutions cannot assume uniform user populations. In multilingual contexts like Kenya, language choice correlates with education, geographic origin, age, and digital confidence. Users may prefer or be most comfortable with their first language, particularly for critical transactions. Yet many digital health systems treat language support as an optional cosmetic feature rather than a core component of equitable service.

The distinction between translation depth is important in the literature. Shallow translation, where conversational exchanges are translated but transactional outputs remain in a default language, creates a critical failure mode. A patient might successfully navigate a booking conversation in Swahili but receive a confirmation block in English, creating ambiguity about what was actually booked. More sophisticated systems maintain language context throughout, including in final confirmations, appointment type labels, and error messages.

A 2022 study by Aggarwal et al. on language inclusion in digital health found that users in multilingual settings experienced higher error rates and lower completion rates when language consistency was poor, even when conversational fluency was high. This suggests that language consistency is not a usability enhancement but a reliability requirement for equitable service.

## 2.7 Patient Engagement, Trust, and Adoption of Conversational Interfaces

Patient engagement literature identifies several factors that predict sustained chatbot use and positive outcomes: clarity of purpose and boundaries, transparency about what the system can and cannot do, consistency in behavior and communication, responsiveness to user needs, and respect for user autonomy and preferences. Even technically correct systems can fail if users perceive interactions as confusing, inconsistent, or patronizing.

Trust in healthcare technologies has been studied extensively. Research shows that trust develops through repeated positive experiences but can be destroyed by single critical failures. Trust is particularly fragile in administrative and access contexts because patients depend on the system working correctly at the moment they need it. If a chatbot books the wrong appointment or fails to capture critical details, the damage to trust may generalize to the institution.

For appointment workflows specifically, trust indicators include: clear capture of required details so the user knows what information was recorded, understandable presentation of options that allows comparison and informed choice, unambiguous final confirmation that matches what the user requested, and recoverable paths when errors occur so users can fix mistakes without frustration. Literature on service recovery suggests that honest acknowledgment of errors and swift correction can actually strengthen trust more than flawless performance, because it demonstrates competence and care.

## 2.8 Ethical and Governance Frameworks for Health AI

Health AI ethics literature draws on bioethical principles—nonmaleficence (avoiding harm), beneficence (providing benefit), justice (fair treatment), autonomy (respecting user agency), and transparency (openness about capabilities and limitations)—to guide design and deployment. For administrative chatbots, ethical operationalization includes several specific requirements.

Role clarity and scope limitation are paramount. Administrative chatbots should not appear to offer clinical advice. This is not just good practice; it is a legal and regulatory requirement in many jurisdictions. Scope limitation protects both patients and institutions by preventing the chatbot from overreaching into domains it is not validated for.

Data minimization—collecting only information necessary for core functions—reduces privacy risk and simplifies compliance. A booking chatbot needs name, identifier, contact information, service type, and preferred date/time. It does not need medical history, insurance information, or diagnostic details. Limiting data collection reduces harm if systems are compromised.

Audit logs and accountability create transparency and enable oversight. Logging interaction transcripts, data elements captured, system decisions, escalations, and errors allows institutions to review behavior, detect problems, and demonstrate compliance with regulations. However, logging must also respect privacy; audit logs should not be freely accessible to all staff.

Escalation pathways to human oversight ensure that the system complements rather than replaces human judgment. When the chatbot is uncertain or encounters edge cases, it should escalate to trained staff who can make contextually appropriate decisions. This maintains accountability at the human level.

## 2.9 Queue Prediction and Recommendation Science

Queue prediction in healthcare has a substantial research literature spanning operations research, industrial engineering, and health services research. Prediction quality depends on data quality, model sophistication, and forecast horizon. Predicting patient no-shows, procedure durations, and service demand at the 15-minute or hourly level is reasonably well-established; longer-term predictions (days or weeks ahead) have higher uncertainty. Literature generally finds that even moderately accurate predictions can support better decision-making if they are presented transparently and users understand confidence levels.

A key finding from this literature is that perfect prediction is not necessary for utility. Decision-support systems that provide interpretable rankings based on predicted metrics (even if predictions are noisy) often outperform systems that attempt very high-precision predictions, because users can reason about the recommendations and adjust based on their own knowledge. This suggests that chatbot recommendation should focus on interpretable, stable ranking rather than attempting false-precision confidence claims.

## 2.10 Synthesis of Literature Gaps

Synthesizing across these literature streams reveals several notable gaps relevant to this thesis:

**Gap 1: Integrated Evaluation of Multilingual Reliability and Transactional Completion.** Most studies of multilingual health technology focus on either conversational quality or task completion, but not both simultaneously. Few examine whether language consistency is maintained through to final transactional outputs. This thesis addresses this by treating multilingual transactional consistency as a core evaluation metric.

**Gap 2: Design Guidance for Deterministic Control Within LLM Assistants.** While LLM technology literature is extensive, practical design patterns for embedding deterministic controls within LLM conversational systems are underdeveloped. Most published architectures either rely purely on LLM output (risking errors) or bypass LLMs entirely for critical operations (sacrificing flexibility). This thesis documents a hybrid approach that leverages LLM capability while maintaining control.

**Gap 3: Patient-Facing Queue Analytics in Conversational Booking Tools.** Most chatbot research treats recommendations as optional features. Few examine how to present queue information in conversational interfaces in ways that users understand and find useful. This thesis tests specific approaches to presenting waiting metrics and recommendations.

**Gap 4: Policy and Governance Frameworks for Healthcare AI in Low-Resource Settings.** Most health AI governance literature is written for high-income country contexts. Frameworks for AI governance in resource-constrained health systems in Africa and South Asia are less developed. This thesis contributes context-specific governance guidance.

**Gap 5: Integrated Artifacts Combining Multiple Dimensions.** While individual components of healthcare chatbots have been studied (conversation quality, task completion, ethical design, etc.), few published artifacts combine all these dimensions in one evaluable system. This thesis presents an integrated prototype that can be studied holistically.

## 2.11 Proposed Analytical Framework

Based on the reviewed literature, this thesis adopts a five-dimension analytical framework that guides both artifact design and evaluation:

**Accessibility Dimension.** The system must be accessible to users with varying language preferences, digital literacy levels, and technological familiarity. This includes conversational flexibility (understanding varied language input), language inclusion (supporting English and Swahili equally), and interface simplicity (using text conversation rather than complex menus). Literature on digital health equity strongly supports accessibility as a core requirement.

**Reliability Dimension.** The system must reliably complete its core function: booking appointments with correct information. This includes mandatory validation of required data before attempting bookings, recovery mechanisms for partial user input, and clear error messages when operations fail. Literature on transactional system design emphasizes reliability as foundational to user trust.

**Optimization Dimension.** The system should provide decision support that helps users make better choices, specifically through queue-aware slot recommendations. This includes transparent presentation of waiting metrics, interpretable confidence calibration, and support for informed choice. Literature on recommendation systems and service design supports providing this information.

**Trust Dimension.** The system must build and maintain user trust through consistent, predictable behavior. This includes clear role and scope boundaries, unambiguous confirmations, recovery paths for errors, and consistency in language and communication. Literature on patient engagement and healthcare technology adoption identifies these as critical trust factors.

**Governance Dimension.** The system must support institutional oversight and policy compliance. This includes audit logging, data protection, escalation pathways, and clear accountability structures. Literature on health AI ethics and regulatory compliance establishes governance as essential for safe deployment.

These five dimensions are interrelated. Strong governance enables reliable operation; reliability supports trust; accessibility widens who can benefit; optimization provides value. Together, they represent the integrated set of requirements for a well-designed healthcare chatbot artifact.

## 2.12 Conclusion

The reviewed literature confirms that chatbot potential in healthcare is substantial but conditional on careful design and rigorous evaluation. Systems that prioritize conversational fluency without attention to transactional rigor, operational constraints, human factors, and governance can fail in real service environments, potentially undermining institutional trust and patient confidence. Conversely, overly restrictive systems that sacrifice flexibility for control may not serve patients' actual conversational needs.

This thesis addresses the identified literature gaps by designing and evaluating a multilingual, guardrail-enhanced, queue-aware hospital assistant with explicit governance and policy considerations. The research integrates insights from conversational AI, health services research, human factors, and digital health policy into a coherent artifact and evaluation framework. By documenting both successes and limitations of this integrated approach, the thesis contributes to closing gaps in practice-oriented healthcare AI research and provides a concrete model for other institutions seeking to deploy responsible AI in administrative health settings.

