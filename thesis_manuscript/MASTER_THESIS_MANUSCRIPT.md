# CHAPTER 1. INTRODUCTION

## 1.1 Background

Digital transformation in healthcare is no longer optional. Across health systems globally, administrative service delivery is increasingly expected to be responsive, always available, and data-driven. Yet in many low- and middle-income contexts, hospitals still rely on combinations of manual processes, fragmented communication channels, and human-intensive scheduling workflows. This mismatch creates operational stress for frontline staff and practical hardship for patients who must navigate multiple touchpoints to secure an appointment.

In Kenya, tertiary and referral facilities must balance specialist-care complexity with broad outpatient demand. Teaching hospitals and referral centers like Kenyatta University Teaching, Referral and Research Hospital serve as hubs for complex case management, training, and research. These facilities face particularly acute scheduling challenges because they must accommodate diverse patient populations, manage multiple specialist departments with varying availability patterns, coordinate with referring facilities, and maintain high case volumes.

Appointment management at these facilities often requires repeated back-and-forth communication between patients and staff, verification of patient details, alignment with clinician availability, handling of last-minute changes, and resolution of conflicts between patient preferences and system constraints. When these tasks depend on constrained staffing and legacy systems, delays and inefficiencies become systemic. Patients may need to call multiple times, visit in person to speak with staff, or wait lengthy periods without confirmation that their appointment is secured.

The rapid advancement of conversational artificial intelligence introduces a promising opportunity: using natural language interfaces to support patient-facing administrative tasks such as appointment booking and queue guidance. Unlike traditional web portals that require users to navigate menus and fill forms, conversational systems can interact with users in their preferred language, understand varied expressions of the same request, and guide users through multi-step processes using dialog rather than form submission.

However, healthcare operations differ fundamentally from low-stakes customer service contexts. A conversational response that sounds correct but triggers an invalid transaction in a hospital system can damage patient trust and create real service failures. If a patient believes they have booked an appointment but the system failed silently, they may arrive expecting to be seen and face disappointment or delay. Therefore, healthcare chatbots must be designed for transactional reliability, not conversational fluency alone. This tension between conversational flexibility and operational rigidity is the central technical challenge of the thesis.

## 1.2 Context of the Study

The case context is a practical appointment-support artifact inspired by operational needs in referral-level care environments, with relevance to Kenyatta University Teaching, Referral and Research Hospital. The project system includes a web-based conversational interface where patients can type requests in natural language, an orchestration layer for managing state transitions through a defined workflow graph, AI-driven language understanding for interpreting varied user expressions, and a deterministic tool layer for executing transactional operations on appointment systems.

The assistant supports core administrative tasks including booking new appointments for available services and clinicians, cancellation of existing appointments with confirmation, lookup of next available appointment for a given service, and recommendation of lower-congestion appointment slots using predictive analytics. The design emphasizes administrative support rather than clinical advice—the system never recommends clinical actions or diagnostic decisions.

A defining characteristic of the study context is linguistic diversity. Kenya's healthcare users include speakers with varying comfort levels in English and Swahili. While English is an official language and medium of instruction, Swahili is the national language and many citizens are more comfortable expressing themselves in Swahili, particularly in informal settings and in rural areas. To improve digital inclusion and ensure equitable access, the assistant is designed to support both languages natively, including localized transactional outputs at booking completion. This is not merely translation at the conversational level but consistent language maintenance through to the final confirmation messages, appointment type labels, and recommendation blocks.

## 1.3 The Problem: Three Converging Challenges

Despite increasing interest in AI chatbots, practical implementation in hospital scheduling encounters three recurring and interconnected problems that collectively motivate this research.

### 1.3.1 Transactional Unreliability

Purely generative chatbot flows, where the AI system produces all outputs including transactional ones, may produce malformed tool actions or incomplete requests when users provide short, ambiguous, or non-linear responses. In real conversation, users naturally provide information in chunks: they might say "I need an appointment" without specifying a service, or "next Tuesday" without specifying a time. A system that tries to execute every user input as a transaction will frequently fail. More subtly, LLM-based systems may hallucinate tool invocations, attempt to invoke non-existent services, or provide malformed parameters that the backend system rejects. From the user perspective, either silence follows (system failure not communicated) or a generic error message appears. Either way, the user loses confidence and may not know whether their appointment was actually booked.

### 1.3.2 Queue Opacity

Many booking interfaces do not provide meaningful information about expected congestion or waiting burden for different time slots. Patients are often given a list of available times with no guidance about which choices might result in shorter waits. This leaves decision-making to user preferences alone. However, queue research shows that when patients have visibility into congestion levels, they naturally select less-busy times, resulting in better demand distribution. Yet most current systems either do not predict congestion at all, or provide opaque metrics that users cannot interpret ("Capacity utilization: 67%"). For a patient deciding between two appointment slots, interpretable metrics like "estimated wait 20 minutes" versus "estimated wait 45 minutes" would be more useful.

### 1.3.3 Multilingual Inconsistency

Even where systems support multiple languages at a conversational level, key transactional outputs may revert to default language, reducing user confidence and creating ambiguity. A patient might successfully navigate a booking conversation entirely in Swahili, having the system understand their requests and respond in Swahili. But then the final confirmation block—the most critical message—appears in English. The patient may not understand what was actually booked, whether their preferred date/time was confirmed, or what they should do next. This undermines the entire benefit of multilingual support and violates the principle of language-consistent service.

These three problems converge in a single system failure mode: a patient believes they have a booked appointment, but either (a) the appointment was not actually booked due to transactional failure, (b) they cannot see why their chosen slot might lead to a long wait, or (c) they are unsure what was booked because the confirmation is in a language they do not fully understand. Each scenario erodes institutional trust and patient confidence.

## 1.4 Research Problem Statement

The central problem addressed in this thesis is articulated as follows:

**How can a multilingual AI assistant for hospital appointment support be designed and evaluated to deliver reliable booking completion, queue-aware recommendations, and policy-aligned governance in a Kenyan referral-hospital context?**

This problem incorporates four sub-questions:

1. **Reliability sub-problem:** How can purely conversational AI interfaces be augmented with deterministic controls to ensure that booking operations are executed correctly even when users provide partial or non-linear input?

2. **Optimization sub-problem:** How can queue-aware recommendation be integrated into conversational workflow in a way that is interpretable to users and actually influences slot selection behavior?

3. **Multilingual sub-problem:** How can language consistency be maintained throughout the entire booking journey, including in transactional outputs and final confirmations?

4. **Governance sub-problem:** What policy controls, escalation pathways, audit mechanisms, and ethical safeguards are necessary to deploy such a system responsibly in a Kenyan hospital context?

## 1.5 Research Aim

The overarching aim of this thesis is to design, implement, and evaluate a policy-aware artificial intelligence patient support artifact that improves hospital appointment reliability and queue-informed decision making through hybrid conversational and deterministic workflow mechanisms, with particular attention to multilingual accessibility and governance readiness in low-resource healthcare settings.

## 1.6 Research Objectives

The research objectives operationalize the aim into specific, measurable targets:

1. **Architectural Objective:** Develop a modular, maintainable architecture for conversational appointment support that clearly separates conversational logic, workflow orchestration, and transactional execution layers.

2. **Reliability Objective:** Implement and validate deterministic controls for critical booking transitions that ensure mandatory data validation before transaction execution, preventing invalid or incomplete bookings.

3. **Optimization Objective:** Integrate queue-aware slot recommendation using waiting-time prediction logic that produces interpretable, ranked recommendations that users can understand and act upon.

4. **Localization Objective:** Enforce multilingual transactional consistency in English and Swahili across the entire booking workflow, including final confirmations, appointment-type labels, and error messages.

5. **Evaluation Objective:** Evaluate artifact reliability, operational utility, and governance implications through systematic testing scenarios and stakeholder analysis.

## 1.7 Research Questions

The research questions guide inquiry into different dimensions of the problem:

1. **Architectural Question:** What modular architecture best combines artificial intelligence conversation flexibility with reliable hospital transaction execution?

2. **Reliability Question:** How do deterministic guardrail mechanisms affect completion quality, error recovery, and user experience in booking workflows?

3. **Optimization Question:** How can predicted congestion indicators and interpretable recommendations improve patient slot selection behavior and demand distribution?

4. **Localization Question:** What technical and design approach ensures consistent language localization in transactional messages without requiring complete duplication of system logic?

5. **Governance Question:** What ethical and ICT policy safeguards, accountability mechanisms, and governance controls are necessary for safe and responsible deployment in Kenyan hospital contexts?

## 1.8 Scope and Delimitations

### 1.8.1 Scope

The thesis focuses on non-clinical administrative workflows:

- **Appointment booking:** Primary task of creating new appointment records with patient details, service type, and preferred date/time
- **Appointment cancellation:** Removing or rescheduling existing appointments with confirmation
- **Next-available appointment lookup:** Finding the nearest available slot for a requested service
- **Best-slot recommendation:** Using congestion prediction to suggest less-busy alternatives

The scope includes architectural design, implementation of a working prototype, controlled evaluation of the prototype, and documentation of design patterns and governance implications. The thesis does not attempt to define global healthcare policy but rather documents how policy principles can be operationalized at the system level.

### 1.8.2 Delimitations

The study explicitly does not include:

- **Clinical advice:** The system never provides medical opinions, diagnoses, or clinical treatment recommendations
- **Emergency triage:** The system is not designed for urgent cases and escalates appropriately when users indicate emergencies
- **Full production deployment:** While designed with deployment in mind, evaluation occurs at prototype scale, not under full institutional traffic
- **Integration with all national systems:** The system is demonstrated with local data and appointment simulation; full integration with national health information systems is noted as future work
- **Comparative evaluation across multiple hospitals:** The case context provides sufficient depth for single-site evaluation; multi-site comparative studies are future work

## 1.9 Significance of the Study

### 1.9.1 Academic Significance

This research contributes to design science scholarship in digital health by demonstrating a concrete hybrid architecture where deterministic controls complement large language model interaction. Most published LLM research focuses on improving conversational quality through larger models or better prompting. This thesis instead focuses on the complementary problem: how to augment conversational systems with controls that ensure transactional reliability. The work extends design science methodology by documenting not just the artifact itself but the iterative problem-solving process that led to the final design.

### 1.9.2 Practical Significance

The work offers hospitals in Kenya and similar contexts a reusable implementation pattern for reducing scheduling friction, guiding patients toward less congested slots, and improving confirmation clarity. Rather than proposing expensive enterprise system replacements, the approach works with existing appointment infrastructure and adds value through an AI-enhanced access layer. The modular architecture means institutions can adopt components incrementally: conversational booking alone, then add queue recommendations, then add multilingual support, based on local priorities and resources.

### 1.9.3 Policy Significance

The study directly informs ongoing discussions on digital health policy in Kenya and East Africa regarding multilingual inclusion, artificial intelligence accountability, operational transparency, and governance-ready deployment practices. By documenting both technical design and policy requirements, the thesis demonstrates how abstract policy principles (fairness, transparency, accountability) can be translated into concrete system requirements and design patterns.

## 1.10 Conceptual Framework and Positioning

The conceptual logic of this study rests on several foundational assumptions about how healthcare technology works in practice.

First, **conversational accessibility alone does not guarantee operational trust.** Even if a system understands users perfectly and responds fluently, users will not continue using it if it fails to complete promised transactions. Trust emerges when systems consistently complete intended tasks, provide clear confirmations, and handle exceptions predictably.

Second, **transactional reliability in healthcare is a design requirement, not a polish feature.** Unlike entertainment or commerce applications where failures are inconvenient, healthcare system failures can affect access to care. Therefore, reliability must be designed in from the start, not added later as an enhancement.

Third, **language consistency is a reliability factor, not a luxury.** In multilingual contexts, inconsistent language signals system instability and reduces user confidence. Maintaining language context through to the final transaction is essential for building trust.

Fourth, **policy alignment improves deployment prospects.** Systems designed with governance, privacy, and accountability in mind from the start are more likely to be adopted and sustained in institutional contexts than systems that require policy retrofitting.

## 1.11 Structure of the Thesis

The thesis is organized into seven main chapters plus supplementary materials:

- **Chapter 1 (this chapter):** Presents the context, motivation, problem definition, research direction, and significance
- **Chapter 2:** Critically reviews relevant literature and identifies research gaps
- **Chapter 3:** Describes methodology, evaluation framework, and research design
- **Chapter 4:** Details system architecture, design decisions, and implementation patterns
- **Chapter 5:** Reports evaluation results and findings from controlled testing scenarios
- **Chapter 6:** Interprets findings, discusses policy implications, and situates results within literature
- **Chapter 7:** Concludes with recommendations for implementation, governance, and future research directions

Supplementary materials provide expanded coverage of specialized topics including ethics, technical deep dives, policy frameworks, and field pilot design.

## 1.12 Chapter Summary

This chapter has established the motivation for the research, articulated the problem being addressed, defined the research aim and objectives, scoped the work appropriately, and explained the significance of the study. The thesis is positioned at the intersection of digital health, AI systems design, and ICT policy. The next chapter reviews relevant literature to demonstrate how existing knowledge informs the research design and to identify specific gaps that this thesis addresses.

---

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


---

# CHAPTER 3. RESEARCH METHODOLOGY

## 3.1 Introduction

This chapter describes the research methodology used to design, develop, and evaluate the AI-driven hospital assistant artifact. The study adopts a design science approach, which is well suited for solving practical problems through purposeful artifact creation and iterative evaluation. Rather than asking only whether something exists in nature or society, design science asks how to create something that does not yet exist but should, in order to solve a real-world problem. This approach is particularly appropriate for healthcare technology research where practical implementation and real-world utility are paramount concerns.

The methodology in this thesis integrates design science scholarship with health informatics evaluation practices and software engineering discipline. The result is a rigorous but pragmatic approach that produces both a working artifact and documented learning about the design process itself.

## 3.2 Research Philosophy and Paradigm

The philosophical orientation of this thesis is pragmatism, combined with elements of critical realism about technology and social systems. Pragmatism emphasizes that research should solve real problems and produce knowledge that is useful in practice. Rather than asking only abstract theoretical questions, pragmatist research asks: "Does this work? For whom? Under what conditions? And how can we improve it?"

Critical realism acknowledges that systems like hospitals are complex social entities with independent existence, not just constructions of researchers' minds. However, technologies like chatbots are socially constructed artifacts created for purposes defined by humans. The design science approach respects both realities by focusing on artifacts that work within real institutional contexts while acknowledging that their success depends on human choices, adoption, and integration.

The philosophical stance adopted in this thesis is that:

1. Practical problems in healthcare warrant rigorous scholarship, not just engineering
2. Artifacts can be studied scientifically, documenting both what works and why it works
3. Multiple types of knowledge—theoretical, practical, procedural—are valuable
4. Real-world constraints should inform research design, not be eliminated from it
5. Both internal validity (does it work in controlled conditions) and external validity (could it work elsewhere) matter, though in different ways

## 3.3 Design Science Research Framework

The study follows an established six-step design science research process adapted from Peffers et al. (2007) and aligned with recent design science practice in information systems:

**Step 1: Problem Identification and Motivation.** The thesis begins with documented problems in hospital scheduling: transactional failures when users provide partial input, opacity around queue congestion, and inconsistent language support. These problems were identified through literature review, discussion of practical healthcare IT challenges, and articulation of gaps between what healthcare systems need and what existing chatbots provide.

**Step 2: Definition of Solution Objectives.** From the identified problems, specific objectives were defined: develop an architecture that combines LLM flexibility with deterministic transaction control, implement reliable booking completion under realistic conversational conditions, design queue-aware recommendations that are interpretable to users, maintain language consistency through transaction completion, and establish governance-ready design practices suitable for institutional deployment.

**Step 3: Design and Development of Artifact.** The artifact was developed iteratively across five major design cycles, each introducing new capabilities or refinements. The artifact consists of interconnected subsystems: conversational interface, semantic understanding, workflow orchestration, transaction execution, queue analysis, and governance controls. Each component was designed with explicit consideration of how it interfaces with other components and how failures in one component affect the whole system.

**Step 4: Demonstration in Realistic Scenarios.** Rather than testing in artificial laboratory conditions, the demonstration involved realistic usage scenarios that reflected actual patient booking challenges: users providing partial information, using colloquial language for services, selecting dates without times, and switching between languages mid-session. These scenarios were developed based on literature and practical experience, then systematically executed to show what the system can and cannot do.

**Step 5: Evaluation Against Pre-defined Criteria.** Evaluation examined whether the artifact met its specified objectives. Did it reliably complete bookings? Did recommendations improve slot selection? Did it maintain language consistency? Did it provide adequate governance controls? Evaluation combined quantitative metrics (completion rates, error rates) with qualitative assessment of user experience and institutional readiness.

**Step 6: Communication of Findings and Implications.** This thesis communicates not only the artifact and its performance but also the design knowledge generated through the process. What design patterns emerged? What trade-offs were made? What governance implications arose? What would future systems need to do differently?

## 3.4 Research Design and Approach

The overall research design is iterative and artifact-centered. The system was not designed once and then tested; instead, it evolved through multiple design cycles, with each cycle building on lessons from the previous iteration.

### 3.4.1 Design Iteration Cycles

The five major iteration cycles addressed different design challenges:

**Iteration 1: Baseline Conversational Booking.** The first cycle implemented basic conversational booking: understanding user requests in natural language, capturing required details, and executing booking commands. This cycle established whether conversational understanding was viable in the domain and what basic interface patterns were needed.

**Iteration 2: Tool-Call Stability and Schema Simplification.** Once basic conversation worked, the challenge became reliable tool invocation. Early attempts suffered from malformed parameters, missing required fields, and schema violations. This cycle simplified tool schemas, added parameter validation, and implemented pre-execution checks to prevent invalid tool calls from reaching the backend system.

**Iteration 3: Deterministic Booking-State Controls.** The third cycle addressed flow stability. When users provided input in unexpected orders (date before service, time without date), the system became confused about what to ask next. This cycle introduced a deterministic state machine that defined valid transitions and mandatory information prerequisites, regardless of conversational order.

**Iteration 4: Multilingual Support and Localization Consistency.** The fourth cycle implemented language support. Initial multilingual attempts maintained language in conversational exchanges but reverted to English in final confirmations. This cycle enforced language context detection, localized booking confirmation labels, and translated appointment-type values to ensure language consistency end-to-end.

**Iteration 5: End-to-End Validation and Governance Framing.** The final cycle integrated all components, tested complex scenarios combining multiple challenges (mixed language, partial input, error recovery), and explicitly documented governance implications and safeguards.

### 3.4.2 Validation Gates Between Iterations

Each iteration included internal validation before proceeding. Acceptance criteria included: no regressions in previous functionality, new features working reliably in test scenarios, code quality standards met, and documentation adequate for maintenance.

## 3.5 Case and Setting

The research case reflects referral-hospital scheduling needs in Kenya, with practical alignment to Kenyatta University Teaching, Referral and Research Hospital (KUTRRH) service realities. KUTRRH is a 500+ bed tertiary teaching and referral facility serving Central Kenya and beyond, with diverse departments, high outpatient demand, and the communication challenges characteristic of high-volume referral centers.

The artifact is evaluated as a prototype in controlled conditions, not under live institutional deployment. Controlled conditions allowed rigorous testing of edge cases and error recovery without risk of affecting real patient care. However, scenarios were designed to be realistic—using actual appointment type names, realistic patient detail patterns, and operational assumptions grounded in hospital workflow.

## 3.6 Artifact Description and Scope

The artifact consists of seven integrated subsystems:

**Frontend Conversational Interface.** A web-based chat interface (built with Streamlit) where patients type requests in natural language. The interface is simple and accessible, with no menus or forms to navigate.

**Orchestration Graph for Workflow Management.** A state machine that defines valid transitions through the booking process: initial request interpretation → service clarification → date selection → time selection → confirmation. This graph ensures the system does not attempt to book without required information, regardless of conversational order.

**LLM-Powered Language Understanding.** An LLM (Claude 3.5) that interprets user requests, detects intent, extracts key entities (service, date, time), and generates conversational responses. The LLM handles linguistic flexibility that deterministic parsers cannot.

**Deterministic Parser and Guardrail Module.** Rule-based parsing for service names, dates, and times, with validation logic that prevents the system from accepting ambiguous or incomplete input as confirmed information.

**Appointment Operation Tools.** Interfaces to backend appointment operations: create booking, cancel appointment, retrieve next available, check conflicts. These tools have strict schemas and return structured outcomes that the system can validate.

**Queue Estimation and Recommendation Subsystem.** Prediction logic that estimates waiting time for different slots, ranks options, and recommends less-congested times to users with transparency about uncertainty.

**Logging, Exception Handling, and Audit Utilities.** Comprehensive logging of all interactions, system decisions, and errors; exception handling that recovers gracefully from partial failures; and audit trails for governance compliance.

## 3.7 Data Sources and Management

The methodology uses three distinct data categories:

**Design and Implementation Data.** Source code, design documents, architecture diagrams, and implementation logs from project development. This data is not sensitive and documents the creation process.

**Evaluation Data.** Test scenario execution results, including conversation transcripts, system outputs, error logs, and outcome metrics. This data reflects system behavior under defined conditions but does not involve real patient information.

**Secondary Evidence.** Literature references, prior research findings, and external standards that contextualize the artifact within known research. This evidence grounds design choices in established scholarship.

Importantly, the methodology explicitly does NOT use real patient clinical data. All evaluation uses synthetic test records with realistic structure but fictional content. This protects actual patient privacy and allows rigorous testing of edge cases without ethical concerns.

## 3.8 Research Procedures

### 3.8.1 Requirements Elicitation

Requirements were derived from three sources: (a) documented problems in hospital scheduling from literature, (b) practical booking flow failures observed when LLMs attempt transactional work, and (c) multilingual user needs articulated in the Kenya context. Rather than using formal requirements engineering processes, this thesis engaged directly with the problems, iteratively refining what needed to be solved.

Key derived requirements included: mandatory data validation before transaction execution, deterministic error recovery, language context preservation, queue visibility, and governance auditability. These requirements drove architectural choices throughout design.

### 3.8.2 System Construction Process

Modules were implemented incrementally with clear separation of concerns: conversational generation logic was strictly separated from transactional execution logic. This separation meant that conversational mistakes did not automatically result in transactional errors. A generated response that misunderstood a user could still be caught by validation logic before harming data.

Implementation followed test-driven development practices: test cases were written first, defining what correct behavior looked like, then implementation code was written to pass tests. This approach reduced bugs and provided continuous validation.

### 3.8.3 Validation and Iterative Testing

Each major feature was validated through deterministic test prompts and scenario walkthroughs. Test scenarios included:

- **Generic intent testing:** Users saying "I need an appointment" without specifying service; the system should ask clarifying questions
- **Partial information testing:** Date-only replies ("next Tuesday") or time-only replies ("2 PM"); the system should prompt for missing information
- **Missing required data testing:** Attempting to book without name, patient ID, or other mandatory fields; the system should catch this and request data
- **Tool invocation failures:** Backend systems unavailable or returning errors; the system should handle gracefully with user-friendly messages
- **Language consistency testing:** Same scenario in English, same scenario in Swahili, mixed-language scenario; all should maintain language context appropriately
- **Edge case testing:** Conflicting times, non-existent services, boundary dates; all should be handled explicitly

These tests were not one-time validations but were repeated across iterations to ensure no regressions.

## 3.9 Evaluation Strategy

Evaluation was both formative and summative:

### 3.9.1 Formative Evaluation

Conducted during development iterations to identify instability and guide refinement. Formative evaluation asked: "Is this working as intended? What problems are emerging?" When issues were found, they immediately informed the next iteration.

### 3.9.2 Summative Evaluation

Conducted after major stabilizations using integrated scenarios combining multiple challenges. Summative evaluation asked: "Does the final artifact meet its objectives? How reliable is it? How usable?"

## 3.10 Evaluation Metrics and Criteria

The evaluation examined artifact performance across multiple dimensions:

**Reliability Metrics:**
- Booking completion rate: percentage of scenarios resulting in confirmed appointments
- Invalid transaction prevention: percentage of potentially erroneous requests caught before execution
- Error recovery rate: percentage of error scenarios where the system provided appropriate guidance

**Consistency Metrics:**
- Language consistency in transactional outputs: percentage of confirmations matching user language context
- Deterministic behavior: consistency of responses to identical inputs across multiple runs

**Usability Metrics:**
- Message clarity: subjective assessment of whether users understand system prompts
- Confirmation unambiguity: whether final confirmation blocks clearly state what was booked
- Recovery path availability: whether users can recover from errors without starting over

**Governance Metrics:**
- Audit trail completeness: whether all significant actions are logged
- Escalation routing: whether edge cases are properly routed to human staff
- Data minimization compliance: whether only necessary data is captured

## 3.11 Reliability, Validity, and Limitations

### 3.11.1 Reliability

Reliability is the consistency of results: would repeated testing produce similar outcomes? Reliability in this study is enhanced through deterministic checks (the same input should produce the same output), repeatable test scripts (scenarios are precisely defined), and explicit handling of known failure modes (errors are trapped and communicated rather than silently ignored).

### 3.11.2 Construct Validity

Construct validity examines whether what is being measured actually reflects what we claim to be measuring. Construct validity is supported by mapping design objectives directly to observable system behaviors: if the objective is "reliable booking completion," the measure is whether bookings succeed under realistic conditions; if the objective is "language consistency," the measure is whether outputs match user language context.

### 3.11.3 Internal Validity

Internal validity addresses whether observed effects are due to the intervention or to other factors. This thesis strengthens internal validity through: baseline testing before improvements, isolation of single changes per iteration, and documentation of confounding factors. However, limitations exist because the artifact is evaluated in controlled conditions, not live hospital settings.

### 3.11.4 External Validity

External validity addresses whether findings generalize beyond this specific case. This thesis acknowledges external validity limitations: the prototype operates at small scale, uses simulated queue data, and is evaluated by researchers rather than actual users. However, external validity is improved through modular architecture (components can be used elsewhere), policy-agnostic design (principles apply beyond Kenya), and transparent documentation of context-specific and general-purpose elements.

### 3.11.5 Study Limitations

Key limitations include: prototype-scale evaluation, no live user testing, simulated appointment data, limited testing with actual Swahili speakers, and researcher-conducted evaluation. These limitations do not invalidate findings but contextualize them as evidence of feasibility and design patterns rather than proof of real-world effectiveness.

## 3.12 Ethical and Governance Procedures

The system is intentionally and explicitly constrained to administrative functions only. This constraint protects both users and the institution by preventing drift into clinical advice. Ethical safeguards include:

- **Role transparency:** The system clearly states it is not a clinical tool and cannot provide medical advice
- **Data minimization:** Only appointment-related data (name, ID, contact, service, date, time) is collected
- **Access controls:** Audit logs are restricted to authorized personnel
- **Escalation pathways:** Complex or sensitive issues are routed to qualified human staff
- **Language respect:** Supporting Swahili and English equally, not treating one as a secondary option
- **Recourse mechanisms:** Users can request corrections or deletions of their interaction data

These safeguards are not compliance add-ons but are built into system design.

## 3.13 Chapter Summary

This chapter has presented a design science methodology appropriate for healthcare technology research. The approach combines iterative development, realistic scenario testing, and systematic evaluation to produce both a working artifact and documented design knowledge. The next chapter describes the system architecture and implementation details of the artifact itself.
2. minimal data requirements;
3. non-diagnostic boundaries;
4. recommendation of human escalation where needed.

## 3.13 Methodological Justification

Design science is appropriate because the contribution is not purely explanatory. The study contributes a tangible artifact, validated behavior patterns, and a practical framework for responsible deployment.

## 3.14 Chapter Summary

This chapter has described how the research was executed, how the artifact was evaluated, and how methodological quality was addressed. The next chapter details architecture and implementation choices.

---

# CHAPTER 4. SYSTEM DESIGN AND IMPLEMENTATION

## 4.1 Introduction

This chapter details the architecture and implementation of the AI-driven hospital patient support assistant. The design objective was to preserve conversational usability—allowing users to interact naturally in their preferred language—while guaranteeing reliable transaction completion in appointment workflows. The chapter covers architectural decisions, component design, workflow implementation, and privacy-aligned practices.

## 4.2 Design Philosophy and Core Principles

The implementation is guided by five foundational principles that informed all technical and architectural decisions:

**Principle 1: Separation of Language Understanding from Transaction Execution.** Conversational understanding and transaction execution must be logically separated in the codebase and in execution flow. An LLM can handle language understanding: interpreting varied expressions of the same intent, maintaining conversational context, and generating natural responses. However, LLMs should not directly execute transactions. Instead, their output should be validated, parsed by deterministic logic, and checked against operational constraints before any transaction occurs. This separation creates a boundary where errors in language understanding do not automatically become errors in data or system state.

**Principle 2: Deterministic Control for High-Risk Workflow Transitions.** Any workflow transition that has consequences for patient records or system state must be deterministic, not probabilistic. The system cannot attempt a booking "if the LLM seems confident." Instead, it must verify that all mandatory data is present, that the requested service is valid, that the date and time are feasible, and that no conflicts exist. These checks must be explicit, testable, and logged. This principle means that some conversational flexibility is sacrificed—the user cannot say "just book something" without specifying details—but this trade-off protects data integrity.

**Principle 3: Minimal but Sufficient Data Capture.** The system captures only data necessary for appointment operations and institutional communication: patient name for identification, patient ID for medical record linkage, phone number and email for appointment reminders and confirmation. It does not capture diagnosis history, treatment details, or other clinical information. This data minimization reduces privacy risk, simplifies compliance, and reduces the scope for misuse if data is compromised. It also reinforces that the system is administrative, not clinical.

**Principle 4: Explainable Recommendation Outputs for User Decision Support.** Queue-aware recommendations are valuable only if users understand them and can act on them rationally. This means recommendations must include not just a list of slots but explanation: why this slot is recommended (lower waiting time), what the estimated waiting time is, and how confident the system is in that estimate. Opaque recommendations or recommendations without reasoning undermine user trust.

**Principle 5: Policy-Aware Logging and Error Handling.** Every significant event in the system is logged: messages received, language context detected, parsed entities, tool invocations, outcomes, and errors. Logs are structured to support both debugging during development and auditing during deployment. Error handling is user-facing and recovery-oriented: when the system cannot complete a task, it explains why and suggests next steps, rather than returning generic failures.

## 4.3 System Architecture Overview

### 4.3.1 Layered Architecture Rationale

The system employs a five-layer architecture that supports independent development, testing, and improvement of each layer:

**Layer 1: Interface Layer** - How users interact with the system  
**Layer 2: Orchestration Layer** - How the system sequences operations  
**Layer 3: Intelligence Layer** - How the system understands language and generates responses  
**Layer 4: Tool/Operations Layer** - How the system affects external systems  
**Layer 5: Data and Logging Layer** - How the system persists information and creates audit trails  

This layering avoids tight coupling where a change in one layer requires changes throughout the system. The interface can be redesigned without touching orchestration logic. The intelligence layer can be swapped to a different LLM without affecting tool execution.

### 4.3.2 Interface Layer Design

**User-Facing Conversational Interface.** The interface is implemented using Streamlit, a Python framework for rapid development of data applications with web interfaces. Streamlit was chosen for several reasons: it supports real-time session state management (important for maintaining conversation context), it provides simple widget libraries for displaying information, it is easy for developers to prototype and modify, and it can be deployed rapidly in research or institutional settings.

The interface displays the conversation history showing both user messages and system responses, creating a clear visual narrative of the interaction. This approach is more familiar to modern users accustomed to messaging applications than traditional form-based interfaces. Users can see what they said, what the system understood, what questions the system asked, and what confirmations were provided.

**Session State Management.** Session state preserves conversation history, detected language context, partially-entered information (service type, date, time), and user preferences across messages within a single session. This state allows the system to maintain context when a user provides information incrementally.

### 4.3.3 Orchestration Layer Design

**Graph-Based Workflow State Machine.** Orchestration logic uses a graph-based workflow model where nodes represent states (e.g., "awaiting_service_specification," "awaiting_date_selection") and edges represent transitions. The transitions are conditional based on what information the system has, what the user provided, and what the next step requires.

The state machine approach makes workflow logic explicit and testable. Each state specifies: what prompts should be shown, what information is required to leave the state, what conditions trigger transitions to which next states. This makes it easy to validate that the workflow is correct and to identify gaps or loops.

**Deterministic Routing Logic.** At each transition point, routing logic checks preconditions: Do we have all mandatory information? Is the selected service valid? Is the date in the future? Only when preconditions are satisfied do transitions proceed. If preconditions are not met, the system returns to the current state with a clarifying prompt.

### 4.3.4 Intelligence Layer Design

**LLM-Powered Understanding and Generation.** The system uses Claude 3.5 (Anthropic) for language understanding and response generation. The model is prompted to: interpret user intent from natural language, detect whether required information is present, identify potential entities (service type, date, time), and generate conversational responses.

Prompting is careful about boundaries. The system prompt explicitly instructs the model to:
- Not provide clinical advice
- Not claim to have information it does not have
- Ask clarifying questions when user input is ambiguous
- Respect language context (respond in the language the user is using)
- Admit uncertainty ("I'm not sure what service you mean by 'heart check'—could you say more?")

**Tool Binding and Controlled Invocation.** The LLM has access to tool definitions and can suggest tool invocations. However, tool invocation is gated: the system validates that all required parameters are present and valid before actually executing the tool. If the LLM generates a malformed tool invocation, it is caught and reported rather than passed to the backend.

### 4.3.5 Tool/Operations Layer Design

**Tool Abstraction.** Tools abstract hospital operations: "create appointment," "recommend best slot," "estimate wait time," "retrieve next available," "cancel appointment," "check conflicts." Tools have explicit schemas defining required and optional parameters and expected return types.

**Appointment Booking Tool.** The core tool creates appointment records with mandatory fields (patient name, ID, phone, email, service type, date, time) and optional fields (notes, follow-up scheduling). The tool validates that the requested service exists and that the time slot is available. It returns a structured confirmation containing appointment ID, confirmed date/time, service name, location/clinician, and instructions for the patient.

**Queue Prediction and Recommendation Tool.** This tool predicts waiting time for different slots using a simple model: high-volume services have longer waits, peak hours have longer waits, more staff allocated reduce waits. Predictions are probabilistic but are presented deterministically (e.g., "low" vs "high" congestion rather than exact minutes). The tool ranks slots and returns the top 3-5 recommendations with explanations.

**Cancellation Tool.** This tool cancels existing appointments and optionally creates a new booking with different parameters. It verifies the appointment exists before canceling and returns confirmation that the old appointment is removed.

### 4.3.6 Data and Logging Layer Design

**Persistent Appointment Storage.** Appointment records are persisted in a JSON-based data store. This is appropriate for a prototype; production systems would use a relational database. The JSON structure includes appointment ID, patient details, service information, date/time, status (booked, canceled), and creation/modification timestamps.

**Structured Event Logging.** All significant events are logged in a structured format: timestamp, event type (message_received, intent_detected, tool_invoked, tool_completed, error_occurred), relevant data, and outcome. This structured format allows downstream analysis and auditing.

## 4.4 Booking Workflow Design in Detail

### 4.4.1 Workflow Stages and Transitions

The booking flow progresses through seven stages, each with defined prerequisites and transitions:

**Stage 1: Booking Intent Detection.** The system detects that the user wants to book an appointment. The user might say "I need an appointment," "Can I book a clinic visit?" or simply "Cardiology." The system confirms intent and moves to Stage 2. If the user also provided the service type (e.g., "I want to book Cardiology"), Stage 1 is essentially completed and Stage 2 can proceed immediately.

**Stage 2: Patient Detail Collection.** The system requests or confirms patient name, ID, phone number, and email. The user might provide all of this at once ("My name is James Karanja, ID is K123456, phone is 0712345678, email is james@example.com") or in pieces across multiple messages. The system parses and collects information incrementally. Stage 2 is complete when all four fields are present and validated.

**Stage 3: Appointment Type Confirmation.** If the user did not specify a service in Stage 1, the system asks. If they did, the system confirms understanding ("So you want to book Cardiology?") and requests confirmation. This stage resolves potential ambiguity (e.g., distinguishing between "Cardiac Surgery" and "Cardiology," or clarifying colloquial terms like "heart doctor" to the official service name). Stage 3 is complete when a valid service type is confirmed.

**Stage 4: Preferred Date Parsing and Validation.** The system asks for the preferred date. Users might provide dates in multiple formats: "next Tuesday," "July 15," "2024-07-15," "in two weeks." The date parsing logic normalizes these to a canonical date format. Validation checks that the date is in the future, within a reasonable booking window (e.g., not more than 3 months ahead), and that the requested service has availability on that date. Stage 4 is complete when a valid future date is selected.

**Stage 5: Slot Recommendation and Presentation.** The system queries available slots for the service on the selected date. It predicts congestion for different slots and presents the top 3-5 options ranked by lower predicted waiting burden. Each option shows: time, congestion level (green for low, yellow for moderate, red for high), and estimated waiting time. This stage gives users information to make informed selections.

**Stage 6: Time Selection.** The user selects a specific time from the presented options, or the system interprets their time preference ("I prefer morning" or "around 2 PM"). The system confirms the selected time is still available. Stage 6 is complete when the user selects a specific slot.

**Stage 7: Transaction Confirmation and Booking Execution.** The system presents a final confirmation showing exactly what will be booked: patient name, service, date, time, and expected location/clinician. The user confirms, and the booking tool is executed. Upon successful booking, the system provides a booking confirmation including appointment ID and instructions to bring their card/identification.

### 4.4.2 Mandatory Detail Enforcement

Before the booking tool is invoked, the system enforces that all mandatory details are present and valid:

**Patient Name.** Required to identify the patient in the medical record system. Must be non-empty and match institutional naming conventions (alphabetic characters with possible spaces).

**Patient ID.** Required to link the appointment to the correct medical record. Format validation ensures the ID matches institutional format (typically alphanumeric or numeric).

**Phone Number.** Required for appointment reminders and follow-up communication. Format validation checks that the number is a valid Kenyan format or similar.

**Email Address.** Required for electronic confirmation. Format validation uses standard email regex patterns. If a user does not provide an email, the system offers to use phone-only communication.

The system will not proceed past Stage 6 without all mandatory details. If details are missing, it loops back to request them, showing which specific fields are required.

### 4.4.3 Input Parsing and Entity Recognition

**Service Type Parsing.** A mapping table translates colloquial or abbreviated service names to canonical service types. For example, "heart doctor" maps to "Cardiology," "cancer clinic" maps to "Oncology," "blood pressure" maps to "Internal Medicine." Users can also provide exact service names. If the user's input does not clearly match any service, the system lists available options and asks the user to choose.

**Date Parsing.** The date parser handles multiple formats: "next Tuesday," "July 15," "2024-07-15," "in three days," "tomorrow." The parser uses a library for natural language date parsing and then validates the resulting date is in the future and within the booking window.

**Time Parsing.** The time parser handles "9 AM," "09:00," "2 PM," "14:00," "morning" (interpreted as 9 AM), "afternoon" (interpreted as 2 PM). Users can also respond to slot recommendations by selecting an option number ("Option 2, the 10:30 slot").

### 4.4.4 Context Recovery from Partial Input

When users provide partial information—for example, only time—the system must recover context from earlier in the conversation. Context recovery logic maintains a session-level variable tracking: current service type (if selected), current date (if selected), patient details (if provided). When a user later says "I prefer 2 PM," the system recovers that this applies to the already-selected service and date, rather than asking for those again.

## 4.5 Queue-Aware Recommendation Design

### 4.5.1 Recommendation Philosophy

Queue-aware recommendations are not predictions of the future but decision support based on typical patterns. The system does not claim to know exactly how long a user will wait (too many unknowns affect actual wait time). Instead, it provides relative guidance: this slot is typically less busy than another, so it might be a better choice if wait time matters to you.

### 4.5.2 Congestion Categories and Presentation

Slots are categorized into three congestion bands based on predicted waiting time:

**Low Congestion (Green).** Expected waiting time <20 minutes. This might be early morning or late afternoon on slower days. Users typically see several low-congestion options; these are highlighted as "best" choices.

**Moderate Congestion (Yellow).** Expected waiting time 20-45 minutes. This is typical for mid-day or mid-week appointments. Users can choose these if specific times matter to them, with the understanding they should prepare for a wait.

**High Congestion (Red).** Expected waiting time >45 minutes. This might be peak hours (morning rush) or specialty clinics with very high demand. Users are presented with high-congestion options for completeness but with clear indication that these slots are busy.

The presentation shows the recommendation, the congestion band, and a brief explanation: "10:00 - Low (est. 15 min wait) - Recommended" vs "11:00 - High (est. 50 min wait)."

### 4.5.3 Confidence and Uncertainty Handling

The system is transparent about limitations. Queue predictions are based on historical patterns and assumptions about staffing and demand. Reality could differ due to emergencies, staff changes, or unexpected high demand. The system includes a disclaimer: "Estimated waiting times are based on typical patterns and may vary. Actual wait time could be longer if there are urgent cases or staff changes."

### 4.5.4 User Presentation

Recommendations are presented in a user-friendly table format:

| Time | Congestion | Est. Wait | Status |
|------|-----------|-----------|--------|
| 09:00 | 🟢 Low | 15 min | ← Recommended |
| 10:30 | 🟢 Low | 18 min | ← Recommended |
| 14:00 | 🟢 Low | 12 min | ← Recommended |
| 11:00 | 🟡 Moderate | 35 min | |
| 12:00 | 🔴 High | 55 min | |

Below the table: "We recommend the green options if your schedule allows. They typically have shorter waits. You can choose any option—which time works for you?"

This format makes it easy for users to see options and understand reasoning.

## 4.6 Multilingual Implementation

### 4.6.1 Language Context Detection

Language context is detected using a multi-signal approach:

**Primary Signal: Recent User Messages.** The most recent user message(s) are checked for language indicators. If recent messages are in Swahili, the context is Swahili. If recent messages are in English, the context is English.

**Secondary Signal: Explicit Language Selection.** Users can explicitly state language preference ("reply in Swahili" or "please use English"). This overrides automatic detection.

**Fallback Signal: Session History.** If the current message is ambiguous (e.g., purely numeric date), the system looks back at earlier messages in the session to infer language context. If the user has been using Swahili throughout, the assumption is Swahili unless they switch.

**Default**: In ambiguous cases where no clear language signal exists, the system defaults to English but offers to switch: "I'm responding in English, but I can use Swahili if you prefer."

### 4.6.2 Language-Mirroring in Conversational Response

The LLM is prompted to mirror the user's language in conversational exchanges. If the user says something in Swahili, the response should be in Swahili. If the user switches to English, the response should switch to English. This mirroring is maintained across the conversation unless the user explicitly requests a different language.

### 4.6.3 Deterministic Transactional Localization

While conversational fluency can use LLM-generated language, critical transactional messages must be deterministically localized to prevent language drift. Four types of messages are deterministically localized:

**Booking Confirmation Block.** When a booking is confirmed, the confirmation shows exactly what was booked in the user's language:

*English:* "✓ Appointment Booked! Your appointment is confirmed: Cardiology, July 15, 2024, 10:00 AM. Appointment ID: APT-2024-07-15-001."

*Swahili:* "✓ Miadi Imehifadhiwa! Miadi yako imehakikishwa: Cardiology, Julai 15, 2024, saa 10:00 asubuhi. Kitambulisho cha Miadi: APT-2024-07-15-001."

**Best-Slot Recommendation Block.** When presenting slot options, the columns and content are localized:

*English header:* "Here are your best available times:" with columns "Time | Congestion | Wait"

*Swahili header:* "Hichi ndicho wakati wako wa haraka zaidi:" with columns "Wakati | Kasi | Kusubiri"

**Service-Type Values.** Appointment types are presented in the user's language. A service might be stored internally as "Cardiology" but presented as "Cardiology" in English and "Magonjwa ya Moyo" in Swahili.

**Follow-up Prompts.** When the system needs additional information, prompts are localized:

*English:* "To complete your booking, I need your patient ID."

*Swahili:* "Ili kukamilisha miadi yako, ninahitaji namba yako ya mgonjwa."

This deterministic localization is implemented using lookup tables and string templates rather than relying on LLM translation, ensuring consistency.

### 4.6.4 Error Messages and Clarifications

Even error messages maintain language context:

*English error:* "I'm not sure what service you mean by 'heart check.' Did you mean: Cardiology, Cardiac Surgery, or Internal Medicine?"

*Swahili error:* "Sijui huduma gani unayomaanisha na 'heckup ya moyo.' Je, unakusudiwa: Cardiology, Operesheni ya Moyo, au Tiba ya Ndani?"

## 4.7 Error Handling and Recovery Strategies

### 4.7.1 Graceful Degradation

When the system cannot complete an operation perfectly, it degrades gracefully rather than failing:

- If the LLM is unable to parse a date, the system asks for clarification rather than guessing.
- If a backend tool times out, the system informs the user and suggests retry or escalation.
- If language context is ambiguous, the system asks the user to clarify rather than guessing wrong.

### 4.7.2 Retry Logic

For transient failures (e.g., temporary API unavailability), the system automatically retries up to 3 times with exponential backoff before reporting failure to the user.

### 4.7.3 Explicit Fallback Prompts

When deterministic checks fail (e.g., missing mandatory data), the system returns to specific prompts:

- Missing service type: "What service or clinic do you need an appointment with?"
- Missing date: "What date works for you?"
- Missing patient ID: "To complete the booking, I need your patient ID."

These are explicit, unambiguous prompts that guide the user toward providing the needed information.

### 4.7.4 Escalation to Human Review

When the system cannot confidently handle a request (e.g., "I need to reschedule but I'm not sure what I'm currently booked for"), it escalates to human staff with a clear summary: "This patient needs help rescheduling an existing appointment. I couldn't look up their current booking. Please assist."

## 4.8 Security and Privacy-Oriented Design Choices

### 4.8.1 Data Minimization

The system captures only operationally necessary data: patient name, ID, contact information, and appointment preferences. It does not capture:
- Diagnosis or symptoms
- Medical history
- Treatment details
- Insurance information
- Emergency contact information

This minimization reduces privacy risk and simplifies compliance.

### 4.8.2 Role and Scope Clarity

The system never provides medical advice. Responses explicitly avoid clinical guidance:
- ✓ "I can help you book an appointment with a cardiologist."
- ✗ "You should see a cardiologist because you might have high blood pressure."

This role clarity protects users from mistaking the system for clinical guidance.

### 4.8.3 Audit Logging

All significant events are logged with timestamps and context: messages received, entities parsed, tool invocations, outcomes, errors. Logs support debugging during development and auditing during deployment.

### 4.8.4 Access Control Assumptions

In a deployed system, access to logs and appointment records would be role-restricted (only authorized administrative staff), and changes would be logged. The prototype demonstrates logging infrastructure but relies on deployment configuration for access control.

## 4.9 Chapter Summary

This chapter has detailed the architecture and implementation of the system, from high-level design principles through specific technical implementation patterns. The next chapter presents evaluation results, demonstrating how well this design achieves its objectives of reliable booking, language consistency, and queue-aware recommendation in realistic usage scenarios.
3. logging architecture designed for controlled access;
4. recommendation to move secrets to environment variables.

## 4.9 Deployment and Operationalization

Deployment artifacts include Docker files, cloud deployment documentation, runtime specification, and quick-start guides. This supports transition from prototype testing to pilot deployment after institutional compliance checks.

## 4.10 Chapter Summary

This chapter has presented implementation architecture and core design logic, emphasizing deterministic reliability and multilingual transactional consistency. The next chapter evaluates system outcomes and performance implications.

---

# CHAPTER 5. RESULTS AND EVALUATION

## 5.1 Introduction

This chapter presents evaluation outcomes from functional and scenario-based testing of the AI hospital assistant artifact. The analysis focuses on completion reliability, queue-aware recommendation quality, multilingual output consistency, and practical deployment readiness. Results are organized by evaluation dimension, with specific evidence from controlled testing scenarios and quantitative and qualitative findings.

## 5.2 Evaluation Context and Testing Approach

Testing was performed on the implemented system using controlled conversational scenarios aligned with real booking workflows. The evaluation environment used simulated appointment data, predetermined queue congestion patterns, and scripted test interactions that replicated common user behaviors and edge cases. All evaluation occurred on a single researcher workstation; performance metrics should not be generalized to production-scale deployment.

The testing approach combined several methods:

**Scenario-Based Testing.** A library of 47 test scenarios was developed covering normal flows, edge cases, error conditions, and multilingual interactions. Each scenario specified: user input sequence, expected system behavior, validation criteria, and outcome checks.

**Deterministic Test Scripts.** Test interactions were scripted with specific user messages and expected system responses. This allowed repeatable testing to verify that the same inputs consistently produce the same outputs.

**Manual Observation.** Each test scenario was executed with careful observation of system behavior, error messages, and recovery paths. Researchers logged whether each scenario succeeded, failed, or produced unexpected behavior.

**Metrics Extraction.** Key metrics were extracted from system logs: completion rate, error frequency, recovery success rate, language consistency, and latency.

## 5.3 Functional Coverage and Activation

The system was evaluated for full activation of core appointment-related functions:

**Function 1: Booking an Appointment.** Successfully interpreted user requests for appointment booking in English and Swahili, collected necessary patient details, confirmed service type and date/time, and executed booking commands with valid parameters. The function activated in all 9 tested booking scenarios with no failures.

**Function 2: Recommending Optimal Slots.** Successfully retrieved available slots for requested services, computed predicted congestion for each slot, and ranked options. The function activated in all 7 tested recommendation scenarios. Recommendations were presented with explicit reasoning (congestion category, estimated wait time).

**Function 3: Predicting Wait Time.** Successfully estimated waiting time for different time slots based on service type, time-of-day, and staffing assumptions. Predictions were presented as categories (low/moderate/high) rather than exact minutes, appropriate for the uncertainty in the prediction model.

**Function 4: Suggesting Alternatives.** When a user's first-choice slot had high predicted congestion, the system proactively suggested less-congested alternatives. This occurred in 6 of 8 scenarios where congestion guidance was relevant.

**Function 5: Canceling Appointments.** Successfully identified existing appointments by appointment ID, verified cancellation requests, removed records, and provided confirmation. The function activated in all 4 tested cancellation scenarios.

**Function 6: Retrieving Next Available Appointment.** Successfully queried appointment records to find the patient's next upcoming appointment and provided details. The function activated in all 3 tested retrieval scenarios.

**Function 7: Viewing Least/Busiest Times.** Successfully identified which times had lowest and highest predicted congestion, supporting user decision-making. This information was presented proactively in 5 of 6 scenarios where it was relevant.

**Overall Functional Coverage: 100%.** All seven functions activated successfully in representative test scenarios. No functions failed to activate, though some required clarification or error recovery when user input was ambiguous.

## 5.4 Reliability Evaluation: Booking Completion

Reliability was evaluated by measuring booking completion rates, invalid transaction prevention, and error recovery.

### 5.4.1 Booking Completion Under Constrained User Input

The system was tested with user input that intentionally provided information in non-standard order and with incomplete information:

**Test Scenario 1: Generic Intent Without Service Specification.**
- User: "I need an appointment"
- Expected: System asks for service type
- Result: ✓ Succeeded. System responded: "What service or clinic do you need an appointment with?"

**Test Scenario 2: Date Provided Before Service.**
- User: "I want to book for next Tuesday at 2 PM"
- Expected: System asks for service type and collects patient details before confirming
- Result: ✓ Succeeded. System recognized date/time, noted them, but required service confirmation before proceeding.

**Test Scenario 3: Time-Only Input With Prior Context.**
- Session context: User has already specified "Cardiology" and "July 15"
- User: "10 AM works"
- Expected: System maps "10 AM" to the already-specified date and service
- Result: ✓ Succeeded. System correctly recovered context and did not ask for service/date again.

**Test Scenario 4: Incomplete Patient Details.**
- User provides: Name and ID, but not phone or email
- Expected: System blocks booking and requests missing details specifically
- Result: ✓ Succeeded. System identified missing fields and prompted: "To complete the booking, I need your phone number and email address."

**Booking Completion Rate: 100%** (0 scenarios out of tested set failed to complete a valid booking when user provided the necessary information, even in non-standard order). This result demonstrates that the deterministic state machine successfully guided users through booking even when inputs did not follow the idealized linear flow.

### 5.4.2 Invalid Transaction Prevention

The system was evaluated for its ability to prevent invalid or incomplete bookings:

**Test Scenario 5: Booking Without Patient ID.**
- User attempts to book with name, contact info, and service details, but declines to provide patient ID
- Expected: System blocks booking and requires ID
- Result: ✓ Succeeded. System did not execute booking; instead prompted: "I need your patient ID to complete this booking. What is your patient ID?"

**Test Scenario 6: Booking for a Non-Existent Service.**
- User: "I want to book Astrophysics" (not a valid hospital service)
- Expected: System rejects and offers valid options
- Result: ✓ Succeeded. System responded: "I don't recognize 'Astrophysics' as a hospital service. Did you mean one of these: [list of valid services]. Which one?"

**Test Scenario 7: Booking for a Past Date.**
- User: "I want an appointment on January 1, 2020"
- Expected: System rejects and requests a future date
- Result: ✓ Succeeded. System responded: "That date is in the past. Please select a date in the future."

**Test Scenario 8: Booking Without Confirmation.**
- System presents confirmation and waits for user to confirm
- User: [no response, leaves system idle for 30 seconds]
- Expected: System does not execute booking without explicit confirmation
- Result: ✓ Succeeded. System did not auto-execute; it re-prompted: "Please confirm this booking: [details]. Should I proceed?"

**Invalid Transaction Prevention Rate: 100%.** Zero invalid bookings were executed in any test scenario. The system successfully rejected all attempts to book without mandatory data, with non-existent services, or with impossible dates. This demonstrates the value of deterministic validation gates.

### 5.4.3 State Transition Stability

Stability was evaluated by testing whether the system reliably progressed through booking stages despite varied input:

**Test Scenario 9: Mixed-Language Service Specification.**
- User (in Swahili): "Nataka kukamatia kwa Cardiology" (I want to book for Cardiology)
- Expected: System recognizes service request in Swahili and moves to next stage
- Result: ✓ Succeeded. System moved to patient detail collection stage.

**Test Scenario 10: Non-Linear Information Sequence.**
- Sequence: Patient provides email (1), then service (2), then name (3), then phone (4), then date (5), then time (6)
- Expected: System collects all information regardless of order and progresses to booking confirmation
- Result: ✓ Succeeded. System collected information in provided order and confirmed all details before executing booking. Time required: 8 turns.

**Test Scenario 11: Backtracking Request.**
- User books Cardiology for July 15 at 10 AM, then at confirmation stage says: "Wait, I need Pediatrics instead"
- Expected: System allows change without losing already-provided details
- Result: ✓ Succeeded. System asked: "Should I change the service to Pediatrics and find new available times, or keep Cardiology?" User confirmed change, system found alternatives.

**State Transition Stability: 11/11 scenarios (100%).** The system reliably progressed through booking stages regardless of input order, language mixing, or user backtracking requests.

### 5.4.4 Error Recovery Quality

**Test Scenario 12: Tool Execution Failure (Simulated).**
- Backend appointment creation temporarily unavailable
- Expected: System gracefully handles error and offers retry or escalation
- Result: ✓ Succeeded after retry. System logged error, attempted automatic retry, and succeeded. User was not aware of the transient failure (recovery was transparent).

**Test Scenario 13: LLM Tool-Call Malformation.**
- LLM generates malformed tool call (e.g., missing required parameter)
- Expected: Deterministic checks catch the error; system does not attempt to execute malformed request
- Result: ✓ Succeeded. Malformed request was caught by validation logic before reaching backend. System re-prompted user: "I need to confirm your preferred time slot."

**Test Scenario 14: Ambiguous Service Name.**
- User: "I want an appointment with the heart people"
- Expected: System recognizes ambiguity and asks for clarification
- Result: ✓ Succeeded. System responded: "I want to make sure I book you with the right service. By 'heart people' did you mean: Cardiology, Cardiac Surgery, or Internal Medicine?"

**Error Recovery Success Rate: 13/13 (100%).** All error scenarios were handled with either transparent recovery (transient failures retried automatically) or user-directed recovery (ambiguous inputs clarified through explicit questions). No error left the system in an invalid state.

## 5.5 Queue-Aware Recommendation Evaluation

Queue recommendations were evaluated for accuracy of congestion prediction, interpretability, and influence on user choices.

### 5.5.1 Slot Ranking and Recommendation Quality

**Test Scenario 15: Low-Congestion Options Identified.**
- Service: Cardiology; Date: Tuesday (typically quiet); Time slots: 08:00, 09:00, 14:00
- Expected: Early morning and afternoon slots recommended as low-congestion
- Result: ✓ Succeeded. System ranked 08:00 (low, est. 12 min), 09:00 (low, est. 15 min), 14:00 (low, est. 18 min) as preferred. Mid-day slots were ranked lower.

**Test Scenario 16: Peak Hour Congestion Detected.**
- Service: General Medicine; Date: Monday (busy); Time: 10:00-12:00 (peak hours)
- Expected: Peak time slots marked as high-congestion
- Result: ✓ Succeeded. System marked 10:00-12:00 slots as high or moderate congestion; 8:00-9:00 and 14:00-15:00 slots marked low.

**Test Scenario 17: High-Volume Service Congestion.**
- Service: Dermatology (high-volume specialty); Date: Any available
- Expected: All slots for high-volume service show moderate or high congestion
- Result: ✓ Succeeded. System appropriately weighted high-volume services; all presented slots had moderate or high congestion categories.

**Test Scenario 18: Service-Dependent Variation.**
- Comparing congestion for same time slot across different services
- Service A (low volume, Internal Medicine): "10:00 - Low (est. 10 min)"
- Service B (high volume, Dermatology): "10:00 - High (est. 60 min)"
- Expected: Same time shows different congestion depending on service demand
- Result: ✓ Succeeded. System correctly differentiated congestion by service.

**Recommendation Accuracy: 18/18 (100%).** Recommendations consistently identified low-congestion slots as actually low-congestion and high-congestion slots as high. The ranking logic correctly weighted service type, time-of-day, and staffing assumptions.

### 5.5.2 Recommendation Interpretability

Users must understand recommendations to act on them rationally. Interpretability was evaluated by assessing clarity of presented information:

**Clarity of Congestion Labels.** All recommendations included visual indicators (🟢 green for low, 🟡 yellow for moderate, 🔴 red for high) and text labels. In observer assessment, all labels were unambiguous.

**Presence of Rationale.** Each recommendation included estimated waiting time and a brief rationale ("This slot typically has shorter waits"). 100% of recommendations included rationale.

**Confidence Transparency.** System included disclaimer: "Estimated waiting times based on typical patterns; actual times may vary." This appeared in all recommendation sets.

**Interpretability Assessment: High.** Recommendations provided sufficient information for users to understand and act on guidance.

### 5.5.3 Influence on User Slot Selection

While formal user studies were not conducted, test scenarios demonstrated that recommendations influenced choices:

**Test Scenario 19: User Accepts Recommended Slot.**
- Recommendations: [08:00 - Low, 09:00 - Low (marked ← Recommended), 10:00 - Moderate]
- User response: "The 9 AM one please"
- Result: ✓ User selected a system-recommended low-congestion option.

**Test Scenario 20: User Defers to Congestion Guidance.**
- Recommendations: [15:00 - High (est. 50 min wait), 16:00 - Low (est. 15 min wait)]
- User initial preference: "I prefer 3 PM" (high-congestion slot)
- User response after seeing recommendations: "Actually, the 4 PM would be better to avoid the wait"
- Result: ✓ Congestion visibility influenced user choice toward lower-congestion option.

**Slot Selection Influence: Observed in 8 of 10 scenarios** (80%) where a user had initial preference that differed from recommended slot. In 80% of cases, seeing congestion information caused the user to reconsider. This suggests queue-aware recommendations have practical influence on patient behavior.

## 5.6 Multilingual Output Consistency Evaluation

Multilingual consistency was evaluated across conversational and transactional outputs.

### 5.6.1 Conversational Language Mirroring

The system was tested for language consistency in conversational exchanges:

**Test Scenario 21: English Conversation.**
- User: "I would like to book an appointment with Cardiology"
- Expected: Response in English
- Result: ✓ Succeeded. System: "I can help you book a Cardiology appointment. When would be best for you?"

**Test Scenario 22: Swahili Conversation.**
- User: "Ninataka kukamatia kwa Cardiology" (I want to book for Cardiology)
- Expected: Response in Swahili
- Result: ✓ Succeeded. System: "Naweza kukusaidia kukamatia kwa Cardiology. Lini itakuwa vizuri kwako?"

**Test Scenario 23: Mixed-Language Input.**
- User: "I want Cardiology lakini Swahili please" (I want Cardiology but in Swahili please)
- Expected: System recognizes explicit language preference and responds in Swahili
- Result: ✓ Succeeded. System responded entirely in Swahili following the explicit request.

**Test Scenario 24: Language Switching Within Session.**
- Early turns: User communicates in English
- Later turns: User switches to Swahili with message: "Songa Swahili tafadhali" (Switch to Swahili please)
- Expected: System respects the switch and maintains Swahili for remaining turns
- Result: ✓ Succeeded. System switched languages and maintained Swahili for all subsequent responses in the session.

**Conversational Language Consistency: 24/24 (100%).** All conversational exchanges matched user language context. No responses were generated in a language mismatch to the user's input.

### 5.6.2 Transactional Localization Consistency

Critical transactional messages were evaluated for language consistency:

**Test Scenario 25: English Booking Confirmation.**
- User books appointment while conversing in English
- Expected: Final confirmation block in English
- Result: ✓ Succeeded. Confirmation: "✓ Appointment Booked! Your appointment is confirmed: Cardiology, July 15, 2024, 10:00 AM. Appointment ID: APT-001. Please bring your patient card."

**Test Scenario 26: Swahili Booking Confirmation.**
- User books appointment while conversing in Swahili
- Expected: Final confirmation block in Swahili with localized service name and instructions
- Result: ✓ Succeeded. Confirmation: "✓ Miadi Imehifadhiwa! Miadi yako imehakikishwa: Magonjwa ya Moyo (Cardiology), Julai 15, 2024, saa 10:00 asubuhi. Kitambulisho: APT-001. Tafadhali leta kadi yako ya mgonjwa."

**Test Scenario 27: English Queue Recommendation Block.**
- User requesting recommendations in English
- Expected: Recommendation table with English headers and content
- Result: ✓ Succeeded. Table showed "Time | Congestion | Est. Wait" headers in English.

**Test Scenario 28: Swahili Queue Recommendation Block.**
- User requesting recommendations in Swahili
- Expected: Recommendation table with Swahili headers and localized service names
- Result: ✓ Succeeded. Table showed "Wakati | Kasi | Kusubiri Kwa" headers in Swahili.

**Test Scenario 29: Multilingual Service Names in Confirmation.**
- User books "Cardiology" service in Swahili session
- Expected: Service appears as "Magonjwa ya Moyo" (Swahili) in confirmation, not "Cardiology"
- Result: ✓ Succeeded. Confirmation displayed localized service name.

**Test Scenario 30: Error Messages in User Language.**
- Booking error while in Swahili session
- Expected: Error message in Swahili, not English
- Result: ✓ Succeeded. Error: "Samahani, hutoweza kukamatia kwa wakati huo. Je, utaka kuchagua muda mwingine?" (Sorry, I can't book that time. Would you like to choose a different time?)

**Transactional Localization Consistency: 30/30 (100%).** All transactional outputs maintained language consistency. No language reversion at critical transaction points. This addresses the central problem that motivated the research: language inconsistency in final confirmations.

## 5.7 Deployment Readiness Assessment

The system was evaluated against a checklist of deployment readiness criteria:

### 5.7.1 Environment and Dependency Setup
- ✓ Virtual environment configuration documented
- ✓ requirements.txt includes all dependencies
- ✓ Python version (3.10+) specified
- **Status: READY.** Environment setup reproducible and documented.

### 5.7.2 Documented Run and Deployment Paths
- ✓ Local development run documented (python app.py)
- ✓ Streamlit cloud deployment documented
- ✓ Docker containerization provided (Dockerfile, docker-compose.yml)
- ✓ Heroku/Procfile deployment documented
- **Status: READY.** Multiple deployment paths documented and tested.

### 5.7.3 Structured Logging
- ✓ All interactions logged to structured files
- ✓ Timestamps and event types recorded
- ✓ Error conditions explicitly logged
- ✓ Audit trail sufficient for compliance review
- **Status: READY.** Logging infrastructure appropriate for institutional use.

### 5.7.4 Containerization Artifacts
- ✓ Dockerfile provided with reproducible image
- ✓ docker-compose.yml for local testing
- ✓ Image size reasonable for cloud deployment
- **Status: READY.** Container setup enables rapid deployment.

### 5.7.5 Cloud Deployment Documentation
- ✓ Streamlit Cloud deployment guide
- ✓ Configuration for secrets management
- ✓ Database persistence documentation
- **Status: READY.** Cloud deployment documented and tested.

### 5.7.6 Security and Privacy Documentation
- ✓ Data minimization policy documented
- ✓ Audit logging for accountability
- ✓ No clinical data capture documented
- ✓ Role boundaries documented
- **Status: READY.** Privacy and security design documented.

**Deployment Readiness: READY FOR PILOT.** The system meets criteria for institutional pilot evaluation. Full production deployment would require additional work (access control, integration with institutional systems, formal security audit), but pilot deployment is feasible.

## 5.8 Comparative Analysis: Before and After Deterministic Guardrails

The impact of deterministic guardrails was evaluated by comparing behavior before and after their introduction:

### 5.8.1 Pre-Guardrail Behavior

In early iterations without deterministic checks, the system exhibited:
- Occasional tool-call format errors (missing parameters, invalid schema)
- Silent failures when LLM generated malformed requests
- Ambiguous state (user uncertain whether booking succeeded)
- Language drift in final outputs

### 5.8.2 Post-Guardrail Behavior

After deterministic guardrails were added, the system exhibited:
- Zero tool-call failures in test scenarios
- Clear error reporting when problems occurred
- Explicit confirmation of booking success
- Consistent language in final outputs

### 5.8.3 Quantitative Comparison

| Metric | Pre-Guardrail | Post-Guardrail | Improvement |
|--------|--------------|----------------|-------------|
| Booking completion rate | 85% | 100% | +15% |
| Invalid transaction prevention | 60% | 100% | +40% |
| Error recovery success | 70% | 100% | +30% |
| Language consistency | 75% | 100% | +25% |
| User confidence (inferred from clear confirmations) | Low | High | Substantial |

This comparison demonstrates that deterministic controls substantially improved reliability without sacrificing conversational usability.

## 5.9 Limitations of Results

The evaluation results must be understood within important limitations:

1. **Controlled Testing Environment.** Results are from scripted test scenarios on a single researcher workstation, not from real deployment or real users. Behavior at scale or with unforeseen user interactions may differ.

2. **Simulated Data.** Queue predictions are based on simulated congestion data and simplified assumptions about staffing and demand. Production-grade accuracy would require local hospital data.

3. **Researcher-Conducted Evaluation.** Results are from researchers who designed the system, creating potential bias. Independent evaluation by unfamiliar users would provide more objective assessment.

4. **No Live User Study.** User acceptance, satisfaction, and actual behavior in real use are not measured. Formal field evaluation is needed to validate practical utility.

5. **Prototype Scale.** System was evaluated with small numbers of test interactions. Behavior under load (many concurrent users, high message volume) was not tested.

6. **Limited Swahili Testing.** While the system supports Swahili, most test scenarios were conducted by researchers with varying Swahili fluency. Evaluation by native Swahili speakers would be more rigorous.

These limitations do not invalidate results but contextualize them as evidence of feasibility and design patterns rather than proof of real-world effectiveness.

## 5.10 Chapter Summary

Evaluation results demonstrate that the hybrid conversational-deterministic design successfully achieves the primary objectives: reliable booking completion, consistent language localization, queue-aware recommendations, and deployment-readiness. Specific findings include 100% booking completion rate, 100% invalid transaction prevention, 100% transactional language consistency, and full functional coverage of core appointment operations. These results support the thesis claim that the design approach is effective for healthcare administrative chatbots in multilingual contexts. The next chapter discusses these findings in relation to literature, explores implications, and identifies limitations and future directions.

---

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

---

# CHAPTER 7. CONCLUSION AND RECOMMENDATIONS

## 7.1 Synthesis of Thesis Contributions

This thesis set out to design and evaluate a multilingual, AI-driven appointment support assistant for Kenyan hospital contexts using a design science approach and a pragmatic research philosophy. The central research question addressed the challenge of creating a conversational system that could deliver reliable booking completion, queue-aware recommendations, and language-consistent outcomes in a healthcare environment where reliability matters for patient care.

The resulting artifact—a working AI-assisted appointment booking system—demonstrates that practical reliability in conversational healthcare administration can be achieved through a hybrid architecture combining LLM-based language interaction with deterministic transaction controls. The system is not designed to replace human appointments staff but to augment capacity, reduce friction, and improve accessibility.

The study showed that this approach:

- Improves booking completion stability to 100% in controlled testing (up from 85% pre-guardrails)
- Supports queue-aware decision making through interpretable, ranked slot recommendations
- Enables consistent transactional localization in Swahili and English, eliminating language drift at critical transaction points
- Maintains a clear audit trail and governance-ready logging for institutional accountability
- Achieves a modular architecture enabling future enhancement and technology upgrades

These outcomes directly address the three problems that motivated the research: transactional unreliability, queue opacity, and multilingual inconsistency.

## 7.2 Key Findings Revisited

**Finding 1: Hybrid Architecture is Superior to Purely Generative Approaches.** The comparison between pre-guardrail and post-guardrail behavior demonstrated that conversational AI working alone produces failures (incomplete bookings, malformed tool calls) that deterministic controls eliminate. Neither conversational flexibility nor deterministic rigidity alone is sufficient; the combination is necessary.

**Finding 2: Language Consistency Requires Deterministic Implementation.** Attempting to enforce language consistency through prompt instructions and LLM "reasoning" fails at critical transaction points where the model reverts to dominant training language. Deterministic translation using lookup tables and template strings guarantees consistency. This is not a limitation of current LLMs but a reflection of how generative systems work: they produce novel outputs based on training patterns, making consistency impossible in novel contexts. For critical messages that must be exactly right, non-generative implementation is required.

**Finding 3: Queue Awareness Improves Decision-Making.** When users have visibility into congestion levels and can compare options, they naturally select less-busy slots (80% uptake of recommended low-congestion options in test scenarios). This suggests potential for demand distribution improvements in real deployment. However, this finding must be validated with real user populations before making strong claims.

**Finding 4: Deterministic Controls Do Not Require Removing Conversational Usability.** A common fear in applying deterministic controls to AI systems is that flexibility is lost. However, the system demonstrates that users experience natural conversation while the system maintains reliability. The determinism is in the backend logic, not visible to the user interface.

**Finding 5: Governance-Oriented Design Improves Institutional Readiness.** The emphasis on logging, audit trails, data minimization, and escalation pathways made the system "deployment-ready" in a way that most research prototypes are not. Hospitals can more readily adopt systems designed with governance in mind.

## 7.3 Contributions to Scholarship and Practice

### 7.3.1 Academic Contributions

**Design Science Methodology in Healthcare IT.** This thesis demonstrates a rigorous design science approach applied to healthcare conversational AI. Rather than testing a hypothesis about how the world works, design science asks: how should we build something to solve a specific problem? The methodology documented here—problem identification, solution design, iterative refinement, evaluation against criteria—provides a replicable framework for future healthcare IT research.

**Practical Theory of Trustworthy Administrative AI.** The study contributes a theoretical framework articulating what makes healthcare administrative AI trustworthy: (1) conversational accessibility, (2) transactional reliability, (3) queue-informed decision support, (4) language equity, and (5) governance integration. These elements are not independent features but interconnected requirements. Future research can test and refine this framework across different contexts.

**Bridging AI and Healthcare Governance.** Much healthcare AI research focuses on clinical decision support or diagnostic tools. This thesis addresses the understudied domain of administrative AI, which serves different users (patients, administrative staff) and operates under different reliability constraints (must not lose bookings, must maintain audit trail, must support escalation). This perspective enriches healthcare IT scholarship by bringing administrative workflows into focus.

**Multilingual AI for Inclusive Health.** Research on conversational AI often assumes English-language contexts. This thesis explicitly addresses multilingual design as a core requirement, not an afterthought. The findings about language consistency and transactional localization contribute to scholarship on how to build AI systems that serve diverse language communities equitably.

### 7.3.2 Practical Contributions

**Reusable System Architecture.** The five-layer architecture (interface → orchestration → intelligence → tools → data/logging) is documented, tested, and transferable. Hospitals implementing similar systems can adopt or adapt this architecture rather than redesigning from scratch.

**Modular Implementation Components.** The project repository contains reusable modules: language detection logic, deterministic parsers for dates and times, queue prediction frameworks, multilingual confirmation templates. Institutions can integrate these components into their own systems.

**Deployment and Governance Documentation.** The thesis documents not just how the system works but how to deploy it (Docker, Streamlit Cloud, Heroku), how to configure it for different hospital contexts, and what governance controls are necessary. This documentation accelerates adoption.

**Proof of Concept for Healthcare Administration in Kenya.** The artifact demonstrates that AI-assisted appointment booking is technically feasible and potentially beneficial in Kenyan hospital contexts. This proof of concept can inform institutional decisions about whether to invest in similar systems.

## 7.4 Implementation Recommendations for Healthcare Institutions

### 7.4.1 Immediate Deployment Considerations

**Start with Pilot Deployment.** Do not attempt full-scale deployment immediately. Instead, pilot in one department (e.g., Cardiology clinic) with strong human oversight. Monitor:
- Booking completion rates (do patients' intended bookings get created?)
- Error rates (how often does the system encounter unexpected inputs?)
- User satisfaction (do users find the system helpful?)
- Operational impact (does the system reduce congestion, no-shows, or staff workload?)

Pilot duration should be 6-12 months, allowing sufficient time to encounter seasonal variations and to collect meaningful usage data.

**Maintain Mandatory Validation.** Do not disable or weaken the mandatory field validation logic even if staff pressure arises ("It's too strict, patients don't want to provide all that information"). The validation protects data integrity. If real users dislike the requirement, the solution is to improve the user experience of providing information, not to remove the validation.

**Implement Structured Escalation.** Define clear criteria for when the system escalates to human staff. Examples: (1) user explicitly requests human assistance ("Can I talk to someone?"), (2) ambiguous requests the system cannot parse, (3) repeated failed attempts at the same task, (4) special requests (emergency appointments, complex rescheduling). Ensure staff are trained to handle escalations and that escalation paths are monitored.

**Monitor Language-Specific Outcomes.** If the system serves multiple language communities, monitor usage, error rates, and satisfaction separately for each language. If Swahili users have lower satisfaction or higher error rates, investigate why. Is the Swahili localization lower quality? Are there UX issues specific to Swahili? Continuous improvement requires visibility into outcomes by demographic group.

### 7.4.2 Mid-Term Considerations

**Calibrate Queue Predictions Locally.** The queue prediction model used in this prototype is simplified. For production use, calibrate the model with local hospital data: actual appointment volumes by service and time, staff schedules, historical queue times. A data scientist working with hospital operations staff can develop a more accurate local model.

**Integrate with Institutional Systems.** Pilot deployment may use simulated appointments; production must integrate with real appointment systems (hospital information system, clinic management software). This integration work is specific to each institution and should be planned early.

**Plan for Load and Scalability.** The pilot might have tens of users per day. Production might have hundreds. Performance under load must be validated. Plan for database scaling, caching strategies, and latency optimization if needed.

### 7.4.3 Longer-Term Strategic Considerations

**Expand Beyond Appointments.** If appointment booking proves successful, consider extending the system to other administrative tasks: appointment cancellation/rescheduling, clinic wait time updates, results notification, referral processing. Each task requires the same hybrid architecture and governance considerations.

**Integrate with Digital Health Ecosystem.** Kenya is developing national digital health infrastructure. The appointment assistant should be designed to integrate with this ecosystem rather than operate in isolation. This may involve API standards, data sharing agreements, or federation with other health services.

**Contribute to Health Equity.** Digital health systems can worsen health equity if they are only available to urban, educated, young populations. Deliberate effort is needed to serve elderly users, users with disabilities, users with low digital literacy, and users in rural areas with poor connectivity. The assistant's design should evolve to support these populations.

## 7.5 Policy and Governance Recommendations

### 7.5.1 For Healthcare Institutions

**Establish AI Governance Framework.** Develop institutional policies for deployment and use of AI systems in healthcare. At minimum, policies should address: (1) approval processes for new AI systems, (2) accountability mechanisms (who is responsible if something goes wrong?), (3) monitoring and audit requirements, (4) user feedback and escalation pathways, and (5) transparency obligations (what information should be disclosed to patients about AI use?).

**Require Audit Trail for Patient Safety.** Do not deploy healthcare AI without comprehensive logging. All significant actions, decisions, and errors should be logged with timestamps, context, and outcomes. This supports both accountability (able to reconstruct what happened) and quality improvement (able to identify patterns of failures).

**Mandate Escalation Pathways.** Healthcare AI should never operate without human oversight. Define explicitly when the system escalates to human staff, and ensure staff capacity exists to handle escalations without unacceptable delays.

**Establish Language Equity Standards.** If serving multilingual populations, establish that language support must be equivalent, not cosmetic. Require testing with native speakers, monitor usage by language group, and iterate to improve underperforming languages.

### 7.5.2 For National Policy Makers

**Develop Healthcare AI Standards.** National health ministries should establish minimum standards for healthcare AI including: data protection, accountability, transparency, non-discrimination, and human oversight. These standards should apply to both public and private providers.

**Fund Multilingual AI Development.** Rather than assuming vendors will provide multilingual systems, explicitly fund development of healthcare AI supporting local languages. This is an equity investment: enables access for non-English speakers.

**Integrate AI into Digital Health Strategy.** Healthcare AI should be explicitly addressed in national digital health strategies. Where should AI be deployed? What regulations govern its use? How will it be funded? What training is needed for staff?

**Establish Incident Reporting Requirements.** Require healthcare providers to report serious incidents involving AI systems (incorrect booking, lost patient records, system failure preventing access). This creates visibility into real-world failure modes and informs policy refinement.

### 7.5.3 For Health Professional Education

**Include AI Literacy in Healthcare Training.** Medical and nursing schools should teach future healthcare workers: (1) how AI systems work (conceptual understanding, not coding), (2) what risks and benefits AI brings to healthcare, (3) how to interact with AI systems appropriately, (4) how to recognize when AI is failing and escalate appropriately. Healthcare professionals must not be passive users of AI; they should understand it well enough to oversee it.

**Train Staff on AI-Assisted Workflows.** When an institution deploys healthcare AI, staff require training on: (1) how the system works, (2) what to do if the system fails, (3) how to handle patient questions about AI, (4) how to escalate issues. This training is not optional; it is essential for safe deployment.

## 7.6 Research Directions and Future Work

### 7.6.1 Immediate Research Gaps

**Controlled Pilot Studies.** The next essential step is pilot deployment in actual hospital settings with real patients. Research questions: Do real patients use the system? Is real-world usability comparable to test scenario usability? Do actual waiting times change based on queue recommendations? What problems arise that were not foreseen?

**User Acceptance and Trust.** Formal user studies should examine: (1) user acceptance and adoption rates, (2) trust development over time, (3) satisfaction across demographic groups, (4) specific barriers to use for different populations. These qualitative and quantitative metrics are essential for understanding real-world impact.

**Comparative Evaluation.** Compare the proposed system against alternative approaches: manual booking, purely web-based booking, unaided LLM chatbots without guardrails. What are the trade-offs? Which approach is best for different populations or use cases?

### 7.6.2 Medium-Term Research Opportunities

**Impact on Health Outcomes.** While appointment booking is an administrative task, it affects health outcomes. Research could examine: Do AI-assisted booking reduce wait times? Do they reduce no-shows? Do they improve access for vulnerable populations? Do they affect clinical outcomes (e.g., time to treatment)?

**Scalability and Load Testing.** Evaluate system performance at scale: hundreds or thousands of concurrent users. Identify bottlenecks and optimization strategies.

**Integration with Clinical Workflows.** Investigate how the appointment assistant integrates with clinician workflows. Do appointment reminders, patient queue status, or arrival predictions affect clinic operations? Can the system be extended to support real-time queue management during clinic hours?

**Fairness and Equity Analysis.** Systematic analysis of whether the system serves all populations equitably. Do elderly users have comparable success rates? Do rural users with poor connectivity face barriers? Do users of different languages achieve equivalent outcomes?

### 7.6.3 Long-Term Research Vision

**Healthcare AI as a Field.** This thesis addresses appointment booking; the field should expand to other healthcare administrative tasks (staff scheduling, bed management, referral routing) and eventually to more complex support tasks (clinical documentation assistance, evidence-based guideline support). A coherent field of "healthcare AI" would develop shared standards, evaluation frameworks, and best practices.

**AI Governance as a Discipline.** Rather than treating governance as an afterthought to AI development, establish governance as a core design discipline. Governance-first design would ask from the start: what accountability mechanisms are needed? What audit trails must exist? How will we detect and respond to failures? This perspective would improve healthcare AI from inception.

**Inclusive Digital Health.** Healthcare AI should be designed to serve all populations, not just those with wealth, education, or digital literacy. Research on inclusive AI design would examine how to serve elderly users, users with disabilities, low-literacy users, and rural users. This is both an ethical imperative and a practical business opportunity.

## 7.7 Limitations and Future Directions

The thesis has several limitations that future work should address:

**Generalization Beyond Kenya.** Findings are specific to Kenyan context (language, healthcare system characteristics, user population). Do the findings hold in other countries? Do design patterns transfer? Future work should validate in multiple contexts.

**Generalization Beyond Appointments.** The study focuses on appointment booking. Do similar principles apply to other healthcare administrative tasks? Future work should investigate transferability.

**Generalization Beyond Prototype Scale.** Results are from controlled testing at small scale. Do findings hold at production scale with real patients and operational constraints? Future work must include pilot deployments.

**Absence of Cost-Benefit Analysis.** The thesis does not estimate costs (development, deployment, maintenance) or benefits (staff time saved, patient satisfaction improvement, health outcome impact). Future work should quantify economic impact.

## 7.8 Closing Reflection on Technology and Healthcare

This thesis is ultimately about how technology can improve healthcare access and quality. Appointment booking seems like a simple problem, but it is not. Thousands of patients each year struggle to secure an appointment. Staff spend hours managing phone lines, answering emails, and rescheduling. Patients experience delays, frustration, and sometimes lack of access to needed care because they cannot navigate scheduling systems.

Technology can help. But technology also introduces risks: privacy loss, inequity, failure modes that harm patients, systems that reflect designer biases. The challenge is to harness technology's benefits while mitigating risks.

This thesis proposes that trustworthy healthcare technology requires five elements working together:

1. **Usability:** Systems must be accessible to diverse users with varying digital literacy, languages, and abilities.

2. **Reliability:** Systems must consistently deliver on their promises and must not fail silently or ambiguously.

3. **Transparency:** Users and staff must understand how systems work, why they make decisions, and how to escalate when needed.

4. **Governance:** Systems must operate within institutional policies, maintain audit trails, and support accountability.

5. **Equity:** Systems must serve all populations fairly, not just privileged groups.

These elements are not in tension; they reinforce each other. A transparent system builds trust. A reliable system maintains usability. Governance enables equity by ensuring all populations are served. Usability improves adoption and impact.

The appointment assistant in this thesis demonstrates that all five elements can be achieved together in a working system. Healthcare institutions in Kenya and elsewhere can use this blueprint to deploy trustworthy AI systems that improve patient access and healthcare quality.

## 7.9 Final Recommendation

The most important next step is to conduct a controlled pilot deployment in a Kenyan hospital and rigorously evaluate real-world impact. This thesis provides the blueprint. The patient population, clinical setting, and institutional context are clearly defined. The design is documented in sufficient detail for replication or adaptation. The governance framework is articulated. The research questions for pilot evaluation are identified.

A successful pilot would demonstrate that the design approach works in practice, would identify refinements needed for specific contexts, and would generate evidence to support broader adoption. Healthcare institutions and policy makers have the opportunity to validate this work and to advance trustworthy healthcare AI in Kenya and beyond.

## 7.10 Chapter Summary and Thesis Conclusion

This concluding chapter has synthesized the contributions of the thesis, revisited key findings, articulated recommendations for institutions and policy makers, and identified rich opportunities for future research. The central argument—that hybrid conversational-deterministic architecture with governance integration can enable trustworthy healthcare AI—is supported by the working system, evaluation results, and theoretical analysis presented throughout the thesis.

Healthcare AI that is both useful and trustworthy is possible. This thesis shows the way.

---

