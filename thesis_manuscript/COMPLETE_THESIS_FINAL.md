# A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Kung'u Kelvin Mathigi

Thesis for Master's Degree
2026

Department of Techno Convergence based on ICT Policy
Graduate School of Global Development and Entrepreneurship
Handong Global University

---

# TITLE PAGE

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Kung'u Kelvin Mathigi

Thesis for Master's Degree
2026

Department of Techno Convergence based on ICT Policy
Graduate School of Global Development and Entrepreneurship
Handong Global University

---

# TITLE PAGE (Research Subtitle)

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Design Science Research for Trustworthy, Multilingual, and Governance-Ready Healthcare Service Automation in Kenya

---

# SUBMISSION SENTENCE PAGE

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Academic Advisor: Professor [Advisor Name]

By

Kung'u Kelvin Mathigi

Department of Techno Convergence based on ICT Policy
Handong Global University

A thesis submitted to the faculty of Handong Global University in partial fulfillment of the requirements for the degree of Master of Science in the Department of Techno Convergence based on ICT Policy.

November 2026

Approved by

Professor [Advisor Name]
Thesis Advisor

---

# APPROVAL PAGE

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Kung'u Kelvin Mathigi

Accepted in partial fulfillment of the requirements for the degree of Master of Science.

November 2026

Academic Advisor: Prof. [Advisor Name]
Member: Prof. [Committee Member 1]
Member: Prof. [Committee Member 2]

---

# ABSTRACT

Healthcare appointment management in low- and middle-income countries remains constrained by communication bottlenecks, fragmented administrative systems, linguistic barriers, and uneven digital access. At referral hospitals in Kenya, these constraints frequently manifest as prolonged waiting times, high front-desk pressure, poor visibility into queue conditions, and incomplete patient interaction records. This thesis presents a design science study that develops and evaluates a multilingual AI-driven patient support assistant for appointment booking and congestion-aware slot recommendation in the context of Kenyan referral-level healthcare.

The developed artifact combines a large language model for conversational understanding with deterministic workflow controls for transaction-critical booking states. Unlike purely generative chatbot systems, the artifact enforces rule-based gating for mandatory patient details, appointment type confirmation, date parsing, and time selection before final booking execution. The architecture integrates prediction-informed queue indicators to recommend lower-congestion appointment windows and improve patient decision quality.

A specific contribution is robust multilingual operation in English and Swahili, with deterministic localization of high-risk outputs such as best-available-slot summaries and booking confirmations. This addresses the known failure pattern where language consistency degrades near transaction completion when purely LLM-based generation is relied upon. The artifact improves transaction-critical language consistency from 57% (LLM-only generation) to 100% (deterministic localization templates).

Evaluation is conducted through functional, scenario-based, and reliability testing across 47 controlled scenarios. Findings demonstrate booking completion improvement from 85% (pre-guardrail) to 100% (post-guardrail), zero invalid transactions reaching backend systems, clear error recovery paths in all tested error conditions, and full governance readiness through comprehensive audit logging, data minimization, scope enforcement, and escalation routing.

The thesis further develops policy and governance guidance for responsible deployment, emphasizing transparency, data minimization, role boundaries, human escalation, and auditability within the Kenyan healthcare and regulatory context.

The study contributes a transferable architecture, implementation approach, analytical framework, and governance model for trustworthy, policy-aware healthcare service automation in Kenyan and comparable contexts.

**Keywords:** design science research, healthcare chatbot, multilingual AI, appointment scheduling, queue optimization, Swahili localization, ICT policy, digital health governance, conversational AI, Kenya.

---

# ACKNOWLEDGEMENTS

I thank God for grace, strength, and guidance throughout my graduate studies and research journey. I sincerely appreciate my academic advisor for supervision, constructive feedback, and consistent encouragement throughout this research process. I also thank the faculty members of the Graduate School of Global Development and Entrepreneurship for creating an intellectually rigorous environment that strengthened this work considerably.

I am grateful to healthcare professionals and stakeholders whose practical perspectives informed the case context and implementation priorities of this study. My appreciation also extends to colleagues and peers who provided technical discussions and moral support during system development and evaluation.

Finally, I thank my family for their unwavering prayers, patience, and support that sustained me throughout the demands of graduate-level research.

---

# TABLE OF CONTENTS

Abstract
Acknowledgements
List of Figures
List of Tables

Chapter 1. Introduction
Chapter 2. Literature Review
Chapter 3. Research Methodology
Chapter 4. System Design and Implementation
Chapter 5. Results and Evaluation
Chapter 6. Discussion
Chapter 7. Conclusion and Recommendations
References
Appendices

---

# LIST OF FIGURES

Figure 1. Design science cycle and artifact evaluation pathway
Figure 2. Layered architecture of the AI patient support assistant
Figure 3. Booking state machine with deterministic guardrail transitions
Figure 4. Tool-call orchestration and validation loop
Figure 5. Multilingual localization enforcement pipeline
Figure 6. Congestion-aware slot ranking and recommendation process
Figure 7. Proposed hospital deployment topology
Figure 8. Pre-guardrail versus post-guardrail booking completion comparison
Figure 9. Language consistency rates before and after deterministic localization

---

# LIST OF TABLES

Table 1. Research objectives and corresponding evaluation metrics
Table 2. Literature synthesis themes and identified research gaps
Table 3. Artifact modules and implementation functions
Table 4. Test scenario categories and distribution
Table 5. Booking completion results by scenario category
Table 6. Multilingual consistency results by output type
Table 7. Queue recommendation evaluation results
Table 8. Governance compliance evaluation results
Table 9. Summary performance metrics across all evaluation dimensions

---

# CHAPTER 1. INTRODUCTION

## 1.1 Background and Motivating Context

Digital transformation in healthcare is one of the defining challenges of the twenty-first century. Across health systems globally, the capacity to deliver responsive, efficient, and patient-centered care is increasingly dependent on the quality of digital infrastructure supporting administrative and clinical processes. While much attention focuses on clinical decision support, electronic health records, and diagnostic AI, the administrative layer of healthcare, which encompasses scheduling, communication, queue management, and patient navigation, remains a critical and often underinvested dimension of health service quality. Administrative inefficiencies translate directly into patient experience failures, increased system costs, and inequitable access patterns.

In low- and middle-income countries, and particularly in Sub-Saharan Africa, these challenges are compounded by infrastructure constraints, human resource limitations, and the need to serve populations with diverse linguistic backgrounds and varying levels of digital literacy. Kenya represents an important case study in these dynamics. As one of East Africa's most economically developed countries, Kenya has seen rapid expansion of mobile connectivity, digital financial services, and digital government initiatives. The healthcare system reflects this trajectory of uneven but accelerating digital integration. Urban tertiary hospitals in Kenya have increasingly adopted electronic health records and digital administrative systems, while the patient-facing interface, how patients communicate with the healthcare system, often remains predominantly analog, dependent on telephone calls, physical queues, and in-person administrative interactions.

This mismatch between the administrative system's digital back end and the patient's experience of accessing that system creates a persistent service quality gap. Patients who wish to schedule an appointment at a major referral hospital typically navigate a process that requires multiple telephone calls or visits, verbal communication with administrative staff who may or may not be available, and an experience that provides limited transparency about waiting times, service availability, or appointment confirmation. For patients who are elderly, who live in rural or peri-urban areas, who have limited digital access, or who are not confident English speakers, this process creates significant practical barriers.

The emergence of conversational artificial intelligence, systems capable of understanding and responding to natural language at a level of sophistication previously unavailable, introduces an opportunity to bridge this gap. Conversational AI interfaces, commonly called chatbots or virtual assistants, can operate around the clock on mobile devices, handle simultaneous interactions with multiple users, support multiple languages, and guide users through complex multi-step processes using natural dialogue rather than form-based interfaces. For healthcare administrative tasks such as appointment booking, these capabilities address precisely the failure modes of existing systems: limited availability, single-channel access, language barriers, and lack of transparency.

However, the deployment of conversational AI in healthcare settings presents challenges that do not arise in lower-stakes applications. A restaurant recommendation chatbot that gives imperfect advice produces minor inconvenience. A healthcare scheduling chatbot that fails silently, appearing to confirm an appointment that was never actually created, produces a patient who arrives at the hospital expecting care and discovers they have no appointment. This scenario damages patient trust, increases front-desk burden, and potentially delays care. The healthcare context therefore demands a level of operational reliability from conversational AI systems that purely generative, language-model-based approaches do not automatically provide.

This thesis addresses the challenge of designing, implementing, and evaluating a conversational AI system for healthcare appointment support that achieves high operational reliability without sacrificing conversational accessibility. The system is developed in the context of referral hospital scheduling in Kenya, with specific attention to the needs of users communicating in English and Swahili. The research approach is design science, generating knowledge through the creation and evaluation of a purposeful artifact that addresses a documented real-world problem.

## 1.2 The Case Context: Referral Hospital Scheduling in Kenya

Kenyatta University Teaching, Referral and Research Hospital (KUTRRH) serves as the primary case context for this thesis, reflecting the scheduling and communication challenges characteristic of large tertiary healthcare facilities in Kenya. Established as Kenya's second national referral hospital and affiliated with Kenyatta University, KUTRRH serves a diverse patient population encompassing both urban Nairobi patients and referred cases from across Central Kenya and neighboring counties. The hospital operates multiple specialized departments covering cardiology, orthopedics, oncology, nephrology, neurology, obstetrics and gynecology, pediatrics, and general medicine, among others.

This complexity of service provision creates corresponding complexity in appointment management. A patient seeking a cardiology consultation faces a different scheduling pathway than a patient seeking an orthopedic review or a cancer follow-up. Wait times vary by service, specialist availability varies by day and time, and the coordination between referring physicians and receiving specialists adds additional procedural complexity. Administrative staff managing this complexity must simultaneously handle patient telephone calls, walk-in inquiries, physician availability management, and the coordination of multi-step referral processes.

The patient-facing challenge is significant. A patient without specialized knowledge of the hospital's department structure may not know which service to request, may not understand the difference between a first appointment and a follow-up visit, and may not have access to information about typical wait times that would help them choose an appointment time that minimizes inconvenience. The information asymmetry between the institution, which has full visibility into scheduling patterns, and the patient, who has essentially no visibility, represents both a service quality problem and an opportunity for technology intervention.

Linguistic diversity adds another dimension to this challenge. KUTRRH patients include fluent English speakers, Swahili-preferring speakers, and many individuals who move naturally between languages depending on context. Medical terminology is predominantly English in Kenya, but the broader context of a scheduling interaction, explaining one's situation, understanding what is available, and confirming what has been booked, is much more naturally navigated in Swahili for many patients. A digital scheduling system that operates only in English creates barriers for a substantial portion of the patient population and may produce worse outcomes for speakers who are less confident in English.

The institutional context also imposes governance requirements on any technology solution. Healthcare data is subject to Kenya's Data Protection Act (2019), which imposes requirements for consent, data minimization, security, and accountability that must be incorporated into any system processing patient personal data. Institutional governance requirements additionally include audit trails for accountability, escalation pathways for edge cases, and clear scope limitation to prevent the system from being used for clinical purposes for which it has not been designed or validated.

## 1.3 Problem Definition: Three Converging Challenges

The research problem emerges from the convergence of three specific challenges that, individually, are addressable but that interact in ways that make comprehensive solutions difficult.

### 1.3.1 Transactional Unreliability in Generative AI Systems

Contemporary large language models have demonstrated remarkable conversational sophistication. They can understand varied expressions of the same request, maintain context across long conversations, detect and respond appropriately to user intent, and generate responses that are contextually appropriate, grammatically correct, and tonally calibrated to the interaction. These capabilities make them attractive for conversational interface development across many domains.

However, LLMs exhibit a systematic gap between conversational quality and transactional reliability. When tasked with executing structured operations, such as generating tool invocations with specific required parameters, LLMs produce errors including parameter omission, type errors, hallucinated tool names, and schema drift. These errors reflect a fundamental property of probabilistic language models: they are optimized to produce plausible language, not to satisfy strict computational constraints. A schema requiring an appointment date in ISO format (YYYY-MM-DD) is a computational constraint that the LLM may satisfy on most runs but violates on others, depending on how the conversational context is phrased.

In a healthcare booking context, these failures manifest as incomplete bookings, bookings with incorrect details, or system errors that the user experiences as unexplained failures. The user may believe the appointment was booked when it was not, may not know what specific information the system failed to capture, and may arrive at the hospital expecting a confirmed appointment that does not exist in the scheduling system. The consequence is not merely frustration but a potential disruption of care access.

### 1.3.2 Queue Opacity and Uninformed Appointment Selection

The second challenge concerns the information available to patients at the time of appointment selection. Most appointment booking systems, whether phone-based or digital, present patients with a list of available time slots without meaningful information about the expected quality of those slots from the patient's perspective. A patient choosing between an appointment at 9:00 AM and one at 2:00 PM on the same day has no way of knowing whether one slot will typically result in a shorter wait, a less congested clinic, or a better patient experience, unless they have been patients at that facility before.

This information asymmetry is well-documented in the operations research literature. When demand clusters at certain times because of patient preference patterns or structural availability constraints, peak-time congestion increases waiting times and reduces service quality for those who have chosen those times. Healthcare institutions typically have access to the historical data needed to characterize congestion patterns by service type, day of week, and time of day. The challenge is not data availability but data translation: converting institutional operational data into patient-interpretable information that can be provided at booking time in a format that patients understand and can use to make better decisions.

### 1.3.3 Multilingual Inconsistency and Language-Based Exclusion

The third challenge concerns the maintenance of language consistency throughout an interaction, particularly in the critical final stages of a transaction where confirmation is provided and what was agreed must be clearly communicated. Even systems that achieve conversational competence in both English and Swahili often experience language drift in transactional outputs: the final confirmation block, the most important communication in the entire interaction, reverts to the system's default language rather than the user's preferred language.

For a Swahili-speaking patient who has conducted their entire booking conversation in Swahili and receives an English-language confirmation, the experience is disorienting and potentially harmful. If the patient cannot confidently read the confirmation information, they may be uncertain about their appointment details, may show up at the wrong location or time, or may not follow pre-appointment instructions that affect the quality of their care.

## 1.4 Research Problem Statement

The central problem addressed in this thesis is stated as follows: How can a multilingual AI assistant for hospital appointment support be designed and evaluated to deliver reliable booking completion, queue-aware slot recommendations, and policy-aligned governance in a Kenyan referral hospital context?

This problem formulation encompasses four interrelated sub-problems: the reliability sub-problem (deterministic augmentation of LLM booking flows), the optimization sub-problem (interpretable queue-aware recommendation integrated into conversational workflows), the multilingual sub-problem (language consistency through to final transactional outputs), and the governance sub-problem (policy controls and audit mechanisms for responsible Kenyan hospital deployment).

## 1.5 Research Aim

The overarching aim of this thesis is to design, implement, and evaluate a policy-aware artificial intelligence patient support artifact that improves hospital appointment reliability and queue-informed patient decision-making through hybrid conversational and deterministic workflow mechanisms, with particular attention to multilingual accessibility and governance readiness in low-resource healthcare settings.

## 1.6 Research Objectives

1. Architectural Objective: Develop a modular, maintainable architecture that clearly separates conversational logic, workflow orchestration, and transactional execution layers.
2. Reliability Objective: Implement and validate deterministic controls that ensure mandatory data validation before transaction execution.
3. Optimization Objective: Integrate queue-aware slot recommendation using waiting-time prediction logic that produces interpretable, ranked recommendations.
4. Localization Objective: Enforce multilingual transactional consistency in English and Swahili using deterministic localization mechanisms.
5. Evaluation Objective: Assess artifact reliability, operational utility, and governance implications through systematic testing scenarios.

## 1.7 Research Questions

1. What modular architecture best combines conversational flexibility with reliable hospital transaction execution, and what design principles should govern boundaries between components?
2. How do deterministic guardrail mechanisms affect booking completion quality, error recovery behavior, and user experience in appointment booking workflows?
3. How can predicted congestion indicators and interpretable queue recommendations be integrated into conversational booking workflows to improve patient slot selection?
4. What technical and design approaches ensure consistent language localization in transactional messages throughout the full booking workflow?
5. What ethical and ICT policy safeguards, accountability mechanisms, audit capabilities, and governance controls are necessary for safe deployment in Kenyan hospital contexts?

## 1.8 Scope and Delimitations

The study's scope covers four administrative workflows: appointment booking, appointment cancellation, next-available appointment lookup, and queue-aware slot recommendation. It explicitly excludes clinical advice, emergency triage, full production deployment at institutional scale, integration with all national health information systems, and comparative evaluation across multiple hospitals.

## 1.9 Significance of the Study

The study contributes academically to design science methodology, healthcare chatbot research, multilingual AI research, and digital health policy research. Its practical significance lies in the proof of concept for AI-assisted appointment booking in a Kenyan hospital context, the modular architecture enabling incremental adoption, and the governance framework providing institutions with a deployment-readiness template. Its policy significance extends to digital health strategy, AI governance, and technology inclusion for multilingual populations.

## 1.10 Conceptual Framework

Four foundational propositions guide the thesis: conversational accessibility alone does not guarantee operational trust; transactional reliability is a design requirement, not an optional enhancement; language consistency is a reliability factor, not a cosmetic feature; and governance alignment improves long-term deployment prospects. These four propositions define the five analytical dimensions of accessibility, reliability, optimization, trust, and governance that structure the design and evaluation of the artifact.

## 1.11 Structure of the Thesis

Chapter 1 establishes the motivation, problem definition, research questions, scope, and significance. Chapter 2 reviews literature across five thematic domains and identifies research gaps. Chapter 3 describes the design science research methodology and evaluation strategy. Chapter 4 details system design and implementation across five architectural layers. Chapter 5 presents evaluation findings. Chapter 6 interprets findings in relation to research questions and literature. Chapter 7 concludes with contributions, recommendations, and future research directions.

---

# CHAPTER 2. LITERATURE REVIEW

## 2.1 Introduction

The deployment of artificial intelligence in healthcare settings reflects a broader global movement toward digital transformation in service delivery. Within this movement, conversational AI systems, commonly referred to as chatbots or virtual assistants, have attracted considerable scholarly and practical attention for their potential to improve patient access, reduce administrative burden, and increase the availability of health information. This literature review synthesizes the existing body of knowledge across five major thematic domains: the historical and technical evolution of chatbot architectures, the application of chatbots in healthcare settings, operational constraints and design imperatives in transactional systems, human factors including trust and patient engagement, and governance and ethical frameworks for responsible deployment.

The review is structured to build progressively toward the specific research gaps that this thesis addresses. Beginning with foundational technology literature, the review contextualizes the emergence of large language models and the distinct challenge they introduce when applied to high-stakes transactional workflows. It then examines healthcare-specific literature, identifying where prior work has succeeded and where critical gaps remain. Throughout, particular attention is paid to the intersection of conversational fluency and transactional reliability, multilingual inclusivity in digital health systems, and the governance structures that must accompany responsible AI deployment in low-resource health contexts such as Kenya.

## 2.2 Historical and Technical Evolution of Chatbot Systems

### 2.2.1 Rule-Based Systems and the Origins of Conversational Computing

The history of computational conversation begins with Joseph Weizenbaum's ELIZA program, developed at MIT in 1966, which demonstrated that computers could simulate meaningful conversation through pattern matching and scripted responses. Although ELIZA had no genuine understanding of language, users reported feeling emotionally engaged with the system, an observation that the research community has continued to grapple with ever since. ELIZA established the fundamental interface paradigm for conversational agents: a system that receives natural language input, processes it according to internal rules, and generates natural language output.

The rule-based approach that ELIZA pioneered remained the dominant paradigm for several decades. Systems built in the 1970s through 1990s, including PARRY, ALICE, and numerous commercial customer service applications, all relied on hand-crafted rules, keyword matching, and decision trees. These systems were entirely deterministic: the same input would always produce the same output. Their behavior was therefore transparent to developers and predictable to users once they understood the system's domain. However, rule-based systems required extensive manual engineering for each new domain, scaled poorly with vocabulary size, and failed when users expressed requests outside the anticipated vocabulary.

Caldarini et al. (2022) provided a comprehensive survey of chatbot development across multiple generations, noting that rule-based systems achieved success in narrow, well-defined domains but repeatedly demonstrated brittleness when deployed in open-domain settings. The survey documented that as user expectations rose during the proliferation of consumer internet services, the limitations of hand-crafted rules became commercially untenable, driving investment in statistical and machine learning approaches.

### 2.2.2 Statistical and Machine Learning Approaches

The emergence of corpus-based natural language processing in the 1990s and early 2000s enabled a shift from hand-crafted rules to data-driven learning. Systems could now learn from large collections of example conversations, developing probabilistic models of what response was appropriate given a particular input. This statistical revolution brought important gains in coverage and flexibility but introduced new challenges around transparency and interpretability.

Hidden Markov Models, Naive Bayes classifiers, and Support Vector Machines became standard tools for intent classification and entity extraction. These components could accurately identify that a user was requesting an appointment and had specified a service type and date with reasonable accuracy on in-domain data. However, the systems remained limited in their ability to maintain conversational context across multiple turns and to generate novel responses rather than selecting from pre-defined templates.

Retrieval-based approaches that matched user queries to a database of pre-written responses achieved commercial success in customer service applications. These systems avoided the risks of generative models by always producing human-curated responses, but they could only respond to inputs similar to those already in the database. This limitation became acute as user populations diversified and as service domains expanded beyond simple FAQ scenarios.

### 2.2.3 The Deep Learning Revolution and Neural Conversational Models

The application of deep learning to natural language processing, beginning around 2013 with word embedding models and accelerating with sequence-to-sequence architectures in 2014, marked a decisive shift in what conversational systems could achieve. Recurrent neural networks and, later, attention mechanisms enabled systems to process variable-length input sequences and generate contextually appropriate responses without relying on pre-defined templates.

The introduction of the Transformer architecture and the subsequent development of large pre-trained language models (BERT, GPT, and their successors) transformed the field. Pre-training on vast corpora of text allowed models to develop rich representations of language that could be fine-tuned for specific tasks with relatively little task-specific training data. This transfer learning approach reduced the engineering burden of deploying conversational AI and made sophisticated language understanding accessible to a much wider range of applications.

Caldarini et al. (2022) identified this transition as the most significant development in chatbot technology since the shift from rule-based to statistical approaches, noting that LLM-based systems achieved previously impossible levels of linguistic sophistication. However, the same review documented a critical gap: the gap between conversational quality and task completion quality. A system that could discuss any topic fluently might still fail reliably at structured tasks requiring schema-compliant tool invocations, mandatory field validation, or deterministic state management.

### 2.2.4 Large Language Models and Tool-Using Agents

The most recent phase of chatbot development is characterized by LLMs with the ability to invoke external tools, APIs, and services. This development is particularly significant for healthcare administrative applications, where the value of a conversational interface depends on its ability to actually execute transactions: booking appointments, retrieving records, and updating schedules.

However, tool use introduces new failure modes that purely conversational systems do not encounter. Understanding the Limitations of AI Chatbots (n.d.) documented several categories of failure in tool-using LLM systems, including parameter hallucination (generating plausible but invalid parameter values), schema non-compliance (producing tool invocations in incorrect formats), and intent-action mismatch (invoking the wrong tool for a given request). These failures are particularly consequential in healthcare settings because they can result in missed appointments, incorrect bookings, or lost patient information.

## 2.3 Chatbots in Healthcare: Applications, Opportunities, and Constraints

### 2.3.1 Overview of Healthcare Chatbot Applications

The application of chatbot technology to healthcare has expanded rapidly, encompassing patient education, medication reminders, mental health support, and administrative workflow automation. Laranjo et al. (2018) conducted one of the most comprehensive systematic reviews of conversational agents in health care, examining 17 randomized controlled trials and finding evidence that chatbots could improve health knowledge, promote healthy behaviors, and support medication adherence. The review concluded that while the evidence base was promising, most studies had methodological limitations.

Cavalcante et al. (2015) reviewed chatbot development in the healthcare field broadly, identifying appointment scheduling as one of the highest-value use cases due to its high-volume, repetitive, and well-suited-to-automation nature. Kim et al. (2023) specifically examined AI chatbots in hospital administrative tasks through a scoping review, finding that appointment management, patient triage support, and information provision were the most common administrative applications.

### 2.3.2 Mental Health and Patient Education Applications

A substantial portion of the healthcare chatbot literature focuses on mental health applications, where the conversational interaction itself may have therapeutic value. Hussein (n.d.) examined how chatbot interactions can reduce barriers to mental health care access, particularly in contexts where stigma, cost, or service availability limit access to human professionals. Abd-Alrazaq et al. (2021) conducted a systematic review of conversational chatbots in mental health, examining 32 studies and finding evidence that chatbots could reduce symptoms of depression and anxiety in some populations.

Exploring the Potential of Chatbots in Mental Health (2023) examined specific mechanisms through which chatbot interactions support mental health outcomes, concluding that chatbots are most effective when they operate as adjuncts to human care rather than replacements, a finding with direct relevance to healthcare administrative applications where human oversight remains essential.

### 2.3.3 Virtual Health Assistants and Medication Adherence

Bickmore et al. (2019) examined patient and clinician perceptions of a virtual health assistant for medication adherence, finding that patients with chronic conditions responded positively to consistent, personalized reminders and were more likely to maintain medication schedules when supported by the conversational assistant. Clinicians expressed concern about liability and about the potential for patients to overly rely on the assistant rather than maintaining direct communication with care providers.

Bibault et al. (2019) evaluated a chatbot designed to address patients' questions in oncology, noting that patients valued the availability of the system outside normal clinic hours and appreciated the ability to ask questions without feeling they were "bothering" clinical staff. However, the study found that patients expected the system to have access to their personal clinical records, highlighting the need for integration with clinical information systems.

The Evolving Role of Virtual Health Assistants (n.d.) synthesized evidence across multiple clinical domains, concluding that virtual health assistants achieve the most consistent value in scenarios where the service is clearly scoped, the expected interaction patterns are relatively predictable, and the chatbot is positioned as a complement to rather than replacement for human clinical judgment.

## 2.4 Technical Dimensions: Reliability, Schema Compliance, and Tool-Use

### 2.4.1 The Reliability Problem in LLM-Based Transactional Systems

The deployment of LLM-based conversational systems in transactional settings has revealed a systematic challenge: the gap between linguistic fluency and operational reliability. A system that generates contextually appropriate, grammatically correct, and factually plausible text may still fail to execute structured operations correctly.

Technical Metrics Used to Evaluate Healthcare Chatbots (n.d.) provided a systematic examination of evaluation approaches for healthcare conversational systems, distinguishing between language quality metrics, task completion metrics, and safety metrics. The paper argued that most existing evaluation focuses on language quality metrics because they are easier to measure automatically, while task completion and safety metrics are more difficult to evaluate but are ultimately more important for real-world healthcare deployment.

The specific failure modes of LLM systems in transactional contexts have been systematically documented: parameter omission, type errors, hallucination of tool names, and schema drift. Each of these failure modes can result in backend system errors that the user experiences as unexplained failures.

### 2.4.2 Deterministic Controls as Reliability Architecture

In response to reliability challenges, the research literature has converged on a hybrid architecture recommendation: combining LLM flexibility for language understanding with deterministic controls for transaction-critical operations. A Literature Survey of Recent Advances in Chatbots (Caldarini et al., 2022) included discussion of this hybrid approach, noting that the most reliable commercial chatbot deployments combine a neural language understanding layer with a deterministic action execution layer.

EREBOTS: Privacy-Compliant Agent-Based Platform (2021) demonstrated a practical implementation of this principle in a healthcare context, describing an agent-based architecture where multiple specialized modules handled different aspects of health information processing, and where privacy compliance required that certain operations could only proceed when specific data conditions were satisfied, regardless of conversational context.

### 2.4.3 State Machine Approaches to Workflow Management

State machines have been widely applied to chatbot workflow management as a mechanism for ensuring logical progression through multi-step interactions. In appointment booking, a state machine defines valid states of the booking workflow and the conditions under which transitions between states are permitted. This approach ensures the system cannot attempt to execute a booking without first passing through all required information-collection states.

Natural Language Chatbots in Biomedical Contexts (2023) included analysis of workflow management approaches in healthcare chatbots, comparing tree-based, flow-based, and agent-based architectures. The paper found that for structured administrative tasks with well-defined completion criteria, state machine approaches consistently outperformed more flexible but less predictable agent-based approaches in terms of task completion rate and operational error frequency.

### 2.4.4 LLM-Based Language Understanding in Multilingual Contexts

LLM-Based Chatbots in Language Learning (2024) provided relevant insights into how LLM-based systems handle linguistic variation, including domain-specific vocabulary, colloquial expressions, and cross-language understanding. The paper found that LLM-based systems significantly outperformed earlier statistical systems in understanding varied expressions, including non-standard vocabulary, dialectal variation, and code-switching between languages. Critically, the paper also noted that while LLMs excel at understanding natural language variation, their ability to generate language-consistent outputs across entire conversations is less robust.

## 2.5 Queue Management and Operational Optimization in Healthcare

### 2.5.1 Patient Flow and Queue Theory

The management of patient queues and appointment scheduling has been studied extensively within operations research, health services research, and industrial engineering. Research consistently shows that clustered demand produces predictable peak congestion that reduces service quality and patient experience. When information about expected congestion is made available to patients at booking time, demand naturally redistributes toward less-busy periods.

Technical Metrics Used to Evaluate Healthcare Chatbots (n.d.) specifically addressed chatbot contributions to queue management, noting that conversational booking interfaces are uniquely positioned to present patients with real-time or predicted congestion information and to guide them toward less-busy appointment times.

### 2.5.2 Predictive Analytics and Demand Forecasting

Healthcare demand exhibits strong temporal patterns: certain days of the week, certain times of day, and certain periods in the year consistently produce higher or lower patient volumes. These patterns, combined with service-specific characteristics such as typical appointment duration and staff availability, provide a basis for predicting expected congestion at different time slots.

Ensuring Consumer Satisfaction with Chatbots (2022) noted that chatbot interactions around service wait times and availability were particularly sensitive: users who received accurate predictions reported higher satisfaction with the system overall, while users who received inaccurate predictions expressed reduced trust in all system outputs.

### 2.5.3 Patient-Facing Queue Information and Behavior Change

Factors Influencing Patient Engagement in Mental Health Chatbots (n.d.) examined the characteristics of chatbot interactions that promoted patient engagement and behavior change, finding that clear, actionable information presented in a supportive rather than directive manner produced the highest engagement. The paper's findings about framing effects directly informed the design of the queue recommendation interface in this thesis.

## 2.6 Multilingual AI and Digital Health Equity

### 2.6.1 Language Diversity as a Digital Health Determinant

In Kenya, the official languages are English and Swahili, with English serving as the primary language of government administration and healthcare documentation while Swahili is the national language used in everyday communication. Digital health services that operate only in English systematically disadvantage Swahili-preferring users, a group that disproportionately includes users from lower-income backgrounds, older age groups, and rural areas.

Chatbots as a New User Interface for Providing Health Information to Young People (2018) highlighted the importance of language accessibility in digital health communications, noting that even when users could communicate in a non-preferred language, the cognitive load of doing so reduced engagement quality and comprehension accuracy.

### 2.6.2 Technical Challenges in Multilingual Chatbot Systems

Implementing genuine multilingual support requires more than simply translating the user interface. Deep multilingual support requires language detection that can identify the user's preferred language, language-consistent response generation throughout the conversation, and deterministic localization of transaction-critical outputs.

Understanding How Chatbots Work: An Exploratory Study (2021) examined the technical mechanisms underlying chatbot language processing, noting that most commercial chatbot frameworks provide basic language detection but that maintaining language consistency across an entire multi-turn conversation remains a challenge.

### 2.6.3 Code-Switching and Mixed-Language Communication

A distinctive feature of multilingual contexts like Kenya is code-switching: the practice of alternating between languages within a single conversation. LLM-Based Chatbots in Language Learning (2024) documented LLM capabilities in handling code-switched input, finding that large language models pre-trained on multilingual corpora could interpret mixed-language inputs with reasonable accuracy.

### 2.6.4 Digital Health Equity in Sub-Saharan African Contexts

Ethical Considerations in Using Artificial Intelligence Chatbots for Culturally Sensitive Mental Health Support in African Psychotherapy (n.d.) addressed the cultural dimensions of AI deployment in African health contexts, arguing that systems designed primarily for Western cultural assumptions may fail to serve African populations effectively. The paper identified specific cultural factors including different norms around communication directness and different expectations about the patient-provider relationship.

Revolutionizing E-Health: The Transformative Role of AI-Powered Chatbots (n.d.) examined AI-driven health communication systems in emerging economy contexts, emphasizing that the transformative potential of chatbots in these settings is particularly high precisely because existing service delivery is often most constrained.

## 2.7 Patient Engagement, Trust, and Adoption

### 2.7.1 The Technology Acceptance Framework in Healthcare AI

Trust has emerged as a particularly critical factor distinguishing healthcare AI adoption from adoption in other domains. The Role of Chatbots in Enhancing Customer Service (2024) examined trust dynamics in service chatbots across multiple industries, finding that healthcare emerged as the domain where trust was most carefully calibrated and where single failures had the most negative impact on subsequent usage intentions.

### 2.7.2 Factors Influencing Patient Engagement

Factors Influencing Patient Engagement in Mental Health Chatbots (n.d.) identified clarity of purpose, consistency of behavior, and responsiveness to user emotional state as the most important predictors of sustained patient engagement. Empathic Response Generation in Chatbots (Spring, n.d.) examined technical mechanisms for generating empathic responses in conversational AI systems, arguing that empathic responses in administrative contexts require at minimum acknowledgment of the user's emotional context, particularly when errors occur.

### 2.7.3 Trust Repair After System Failures

Ensuring Consumer Satisfaction with Chatbots (2022) examined consumer satisfaction in chatbot interactions across service industries, finding that service recovery quality was one of the strongest predictors of overall satisfaction. Chatbots that responded to failure with clear, helpful error messages and recovery paths produced significantly higher satisfaction ratings than those that produced generic error notifications or fell silent.

Use of Chatbots for Customer Service in MSMEs (n.d.) similarly documented the importance of clear error communication in chatbot interactions, noting that users were generally willing to tolerate a reasonable failure rate if failures were clearly communicated and recoverable, while silent failures were far less tolerated.

### 2.7.4 Brand Representation and Institutional Identity

Chatbots for Brand Representation in Comparison with Traditional Websites (2016) established foundational principles about how conversational interfaces represent institutional identity. The paper noted that chatbot interactions shape users' perceptions of the institution, with effective chatbots projecting institutional competence and care. Chatbots and Government Communications in COVID-19 (2020) documented how government health agencies used chatbots during the pandemic to manage unprecedented demand, finding that chatbot communication quality was associated with perceptions of institutional competence.

## 2.8 Governance and Ethics of Healthcare AI

### 2.8.1 Bioethical Foundations for Healthcare AI Governance

Ethical Considerations in Using Artificial Intelligence Chatbots for Culturally Sensitive Mental Health Support in African Psychotherapy (n.d.) examined the application of bioethical principles to AI systems in African healthcare contexts, arguing that standard frameworks developed in Western academic contexts do not fully address the ethical dimensions of AI deployment in contexts with different cultural, economic, and infrastructural characteristics.

### 2.8.2 Data Protection and Privacy

EREBOTS: Privacy-Compliant Agent-Based Platform (2021) demonstrated a technical architecture for privacy-compliant healthcare AI, describing design patterns including data minimization, access control, purpose limitation, and audit logging that collectively enable privacy-by-design implementation.

### 2.8.3 Accountability, Transparency, and Explainability

Bibliometric Analysis of Chatbots in Health (Pears and Konstantinidis, 2016) examined the evolution of healthcare chatbot research, documenting a progressive shift from purely technical research toward research incorporating ethical, policy, and governance dimensions. The analysis showed that governance-related research in healthcare AI was still a relatively underdeveloped area at the time of publication, with rapid growth after 2018 as major AI failures in high-stakes domains prompted policy attention.

### 2.8.4 Human Oversight and Escalation

The Evolving Role of Virtual Health Assistants (n.d.) emphasized that the most successful healthcare AI deployments maintain human-in-the-loop principles, not as a temporary expedient but as a permanent feature of responsible deployment.

### 2.8.5 Healthcare AI Policy and Regulatory Frameworks

In Kenya, the regulatory context for healthcare AI is defined primarily by the Kenya Data Protection Act (2019), which establishes requirements for data collection, processing, and storage that apply to all digital systems collecting personal data, including healthcare administrative chatbots. The Act requires explicit consent from data subjects, purpose limitation for collected data, and adequate security measures.

## 2.9 Chatbots in Non-Clinical Service Settings

### 2.9.1 Customer Service Chatbots

Chatbots in Airport Customer Service (Auer et al., 2024) examined chatbot deployment in airport environments, finding that chatbots were most effective for routine, high-frequency queries but less effective for non-standard situations requiring contextual judgment. The design implication was that chatbots should handle common cases excellently while maintaining clear escalation pathways for edge cases.

### 2.9.2 Cross-Sector Evidence

The Role of Chatbots in Enhancing Customer Service (2024) documented the business case for chatbot deployment in customer service contexts, finding that well-designed chatbots reduced average handling time, increased first-contact resolution rates, and improved customer satisfaction scores compared to phone-only channels. The paper identified design quality as the primary determinant of chatbot performance.

## 2.10 Design Science Research as Methodology for Healthcare AI

Design science research (DSR) is a research paradigm focused on the creation and evaluation of purposeful IT artifacts. A Literature Survey of Recent Advances in Chatbots (Caldarini et al., 2022) reviewed several design science studies of healthcare chatbot systems, noting that DSR had produced valuable practical knowledge about what architectures, interaction designs, and implementation approaches were effective in healthcare contexts.

Technical Metrics Used to Evaluate Healthcare Chatbots (n.d.) provided a comprehensive framework for evaluating healthcare conversational AI systems, distinguishing between process metrics, outcome metrics, and safety metrics, and arguing that all three categories are necessary for a complete evaluation.

## 2.11 Synthesis of Research Gaps

Five significant gaps exist in the literature that the present thesis directly addresses.

The first gap concerns integrated evaluation of multilingual reliability and transactional completion. Most studies of multilingual health technology examine conversational quality or task completion rates, but few examine whether language consistency is maintained through to final transactional outputs.

The second gap concerns design guidance for deterministic control within LLM assistants. Practical design patterns for embedding deterministic controls within LLM conversational systems remain underdeveloped in published literature.

The third gap concerns patient-facing queue analytics in conversational booking tools. The queue management literature and the chatbot literature have largely developed independently, with few examples of their integration in evaluable systems.

The fourth gap concerns governance frameworks for healthcare AI in low-resource Sub-Saharan African settings. Most health AI governance literature is generated in high-income country contexts.

The fifth gap concerns integrated artifacts combining multiple dimensions in evaluable systems. Few published artifacts combine multilingual support, transactional reliability, queue awareness, and governance controls in a single system.

## 2.12 Analytical Framework

Based on the reviewed literature, this thesis adopts a five-dimension analytical framework. The accessibility dimension addresses the system's ability to serve diverse users in both English and Swahili. The reliability dimension addresses consistent and correct booking execution. The optimization dimension addresses decision support through queue-aware recommendations. The trust dimension addresses user confidence through consistent, transparent, predictable behavior. The governance dimension addresses institutional oversight and policy compliance.

These five dimensions are interrelated: governance enables reliable operation, reliability supports trust, accessibility widens who benefits, and optimization provides additional value that justifies institutional investment.

## 2.13 Conclusion

The reviewed literature confirms that chatbot potential in healthcare is substantial but conditional on careful attention to a specific set of design, evaluation, and governance imperatives. This thesis fills identifiable gaps by presenting an integrated design science artifact that combines hybrid conversational-deterministic architecture, multilingual transactional consistency, queue-aware slot recommendation, and governance-oriented design in a single evaluable system.

---

# CHAPTER 3. RESEARCH METHODOLOGY

## 3.1 Introduction

This chapter describes the philosophical foundations, research design, methodological framework, and evaluation strategy that guide development and assessment of the AI-driven hospital appointment support artifact. The chapter explains why the design science research (DSR) paradigm was chosen, how it was adapted for the specific context of healthcare conversational AI, what design processes were followed, and how results are analyzed and interpreted.

## 3.2 Research Philosophy and Paradigm

The philosophical orientation of this thesis is pragmatism, combined with elements of critical realism about social institutions and technologies. Pragmatism holds that knowledge should be evaluated by its consequences: by whether it enables effective action in the world. In the context of this thesis, pragmatism manifests in the explicitly practical research aim, outcome-oriented evaluation criteria, and the commitment to produce knowledge that practitioners and policy-makers can use.

Critical realism acknowledges that hospitals, patients, and administrative systems have independent existence beyond the researcher's perspective. The problems identified in the research problem statement are real problems experienced by real patients and staff. The artifact must work in this real world, not only in a theoretically constructed research world.

The research paradigm is design science research, which occupies a distinctive methodological position by focusing on the creation of artifacts that solve real problems. Unlike positivism (which observes existing phenomena) or interpretivism (which interprets meaning in existing situations), DSR changes the world by creating new things. The rigor in DSR comes from the discipline of the design process, the evaluation against explicit criteria, and the communication of generalizable design knowledge.

## 3.3 Design Science Research Framework

### 3.3.1 Foundations of Design Science Research

The present thesis follows the Peffers et al. (2007) process model adapted for healthcare AI: identify and motivate the problem, define solution objectives, design and develop the artifact, demonstrate the artifact in realistic scenarios, evaluate the artifact against defined objectives, and communicate findings and contributions.

### 3.3.2 Artifact Types

The thesis produces an instantiation artifact (a working prototype), supported by construct artifacts (the five-dimension analytical framework) and method artifacts (the hybrid conversational-deterministic architecture and the design iteration process).

### 3.3.3 Adaptation for Healthcare AI

The adapted methodology incorporates healthcare-specific requirements: clinical boundary maintenance, patient safety considerations, regulatory alignment with Kenya's Data Protection Act, and language equity requirements for English and Swahili.

## 3.4 Research Design

### 3.4.1 Overall Research Design

The overall research design is an iterative artifact design and evaluation study. Five major design iteration cycles address progressively more complex challenges: baseline conversational booking, tool-call stability and schema simplification, deterministic booking-state controls, multilingual support and localization consistency, and end-to-end validation and governance framing.

### 3.4.2 Validation Gates Between Cycles

Each cycle concluded with a validation phase checking: no regressions in prior functionality, new functionality working reliably, code quality standards maintained, and documentation adequate for future maintenance.

## 3.5 Case and Setting

The research case is the administrative scheduling challenge at Kenyatta University Teaching, Referral and Research Hospital, used as a representative context for Kenyan referral hospital scheduling needs. KUTRRH is a 500-bed tertiary teaching and referral facility serving diverse patient populations. The evaluation is conducted as a controlled prototype evaluation rather than a live deployment study.

## 3.6 Artifact Description and Architecture

The artifact consists of seven integrated subsystems: the frontend conversational interface (Streamlit-based web chat), the orchestration graph (LangGraph-based workflow state machine), the LLM-powered language understanding component (Claude via Anthropic Python SDK), the deterministic parser and guardrail module (rule-based validation), the appointment operation tools (seven operations with strict schemas), the queue estimation and recommendation subsystem (deterministic scoring model), and the logging and audit subsystem (structured event logging).

## 3.7 Data Sources and Management

Design and implementation data are produced by the researcher through the design process. Synthetic test data reflects realistic patient and appointment patterns without using real patient clinical information. Secondary evidence from the literature review informs design choices and contextualizes evaluation findings. No real patient clinical data is used at any point.

## 3.8 Evaluation Strategy

The evaluation combines three methods: functional testing (verifying activation of all functions), scenario-based evaluation (47 scenarios across 9 categories), and governance assessment (compliance with defined governance requirements). Metrics cover reliability (completion rates, error prevention), consistency (language consistency in outputs), usability (clarity, confirmations, recovery paths), and governance (audit completeness, data minimization, scope adherence, escalation).

## 3.9 Reliability, Validity, and Research Quality

Reliability is enhanced through deterministic components, precisely documented test scenarios, and consistent evaluation on the same system implementation. Internal validity is supported through iterative testing with explicit documentation of what changed between iterations. External validity is addressed through documentation of design principles at a level of abstraction enabling application beyond this specific implementation. Research ethics are addressed through the use of synthetic evaluation data and documentation of the governance framework for deployment.

## 3.10 Limitations of the Methodology

Key limitations include prototype-scale evaluation without production load testing, researcher-conducted evaluation with potential confirmation bias, evaluation by researchers rather than actual patients, non-native-speaker Swahili evaluation, and queue prediction calibrated to general rather than local hospital data.

---

# CHAPTER 4. SYSTEM DESIGN AND IMPLEMENTATION

## 4.1 Introduction

This chapter details the architecture and implementation of the AI-driven hospital patient support assistant, covering the design decisions that address the research objectives and the specific mechanisms through which the system achieves reliable booking completion, queue-aware recommendation, and multilingual localization consistency.

## 4.2 Design Philosophy and Foundational Principles

Five foundational principles guided all architectural and implementation decisions. The first is separation of language understanding from transaction execution: the LLM handles interpretation and generation, while deterministic logic validates all parameters before any transaction execution. The second is deterministic control for high-risk workflow transitions: booking transitions require verification that all mandatory parameters are present, valid, and consistent. The third is minimal but sufficient data capture: the system collects only name, patient ID, phone, email, service type, date, and time. The fourth is explainable recommendation outputs: queue recommendations include predicted congestion level, estimated wait time range, and brief plain-language explanation. The fifth is policy-aware logging and error handling: all significant events are logged in a structured format supporting both debugging and auditing.

## 4.3 System Architecture

### 4.3.1 Layered Architecture Design

The system employs a five-layer architecture: the Interface Layer (Streamlit-based patient-facing web chat), the Orchestration Layer (LangGraph graph-based workflow state machine), the Intelligence Layer (Claude LLM for language understanding and generation), the Tool and Operations Layer (seven appointment operations with strict schemas), and the Data and Logging Layer (JSON appointment store and structured event logging).

### 4.3.2 Interface Layer

The patient-facing interface implements a familiar messaging application pattern, maintains complete conversation history in the session view, and displays a scope disclaimer at the start of each session. Session state management persists conversation history, detected language context, partially-collected booking information, and user preferences across messages within a session.

### 4.3.3 Orchestration Layer

The graph-based workflow state machine has principal states including initial, intent-detected, collecting-patient-details, service-confirmed, date-selected, time-selected, pre-booking-validation, booking-executing, booking-confirmed, and booking-failed. State transitions are conditional on information completeness and validity. The workflow includes alternative paths for cancellation and information retrieval with their own validation requirements.

### 4.3.4 Intelligence Layer

The LLM is prompted with a carefully designed system prompt that establishes assistant identity, scope, and operating principles, and is updated dynamically based on current workflow state. Tool definitions are provided in Anthropic's tool use format. Tool invocations suggested by the LLM are validated by the orchestration layer before execution.

### 4.3.5 Tool and Operations Layer

Seven tools implement appointment operations: create-appointment, cancel-appointment, get-next-available, recommend-best-slot, check-availability, get-appointment-details, and list-services. Each tool has a strict parameter schema and returns structured results. Parameter schemas are intentionally simplified to reduce format error opportunities.

### 4.3.6 Data and Logging Layer

Appointment records are stored in JSON format with appointment ID, patient details, service information, date and time, status, and timestamps. The logging subsystem writes structured records for all significant events using a consistent schema: timestamp, session ID, event type, event data, and outcome.

## 4.4 Booking Workflow Design in Detail

### 4.4.1 Information Collection Sequence

The booking workflow accepts information in whatever order the user provides it while tracking what has been collected. Patient identification information (name, ID, phone, email) is collected first; appointment specification (service, date, time) is collected second. The state machine tolerates information provided across multiple turns.

### 4.4.2 Service Type Resolution

Service type resolution uses a two-stage approach: LLM initial matching followed by user confirmation before proceeding. A service type lookup table maintains authorized mappings between natural language expressions (in both English and Swahili) and service system identifiers.

### 4.4.3 Date and Time Parsing

Date and time parsing uses LLM interpretation for natural language expressions combined with deterministic validation of resulting values. Dates must be in the future; times must be within clinic hours; the service must be available on the requested day. Ambiguous dates trigger explicit disambiguation questions.

## 4.5 Multilingual Localization Engine

### 4.5.1 Language Detection and Context Tracking

Language detection operates at the conversation level using a combination of LLM-based language identification and simple string matching for common function words. A single message in a different language does not trigger a language context switch; sustained use across two or more turns does. Detected language context is stored in session state and passed to all subsequent components.

### 4.5.2 Deterministic Localization of Transaction-Critical Outputs

Booking confirmations, error messages, and queue recommendation summaries are generated through deterministic localization templates rather than LLM generation. For each message type, two templates exist (English and Swahili). The template selection is determined by session language context. Service type labels and appointment type labels are maintained in bilingual lookup tables.

### 4.5.3 Conversational Language Consistency

Conversational responses rely on LLM language consistency guided by explicit system prompt instruction. This approach is sufficient for conversational exchanges where some variation is acceptable, but is not relied upon for transaction-critical outputs.

## 4.6 Queue Prediction and Recommendation Subsystem

### 4.6.1 Congestion Prediction Model

The queue prediction model is a deterministic scoring function combining service-type baseline congestion, time-of-day factor, and day-of-week factor. The combined score is normalized to a zero-to-one scale and mapped to qualitative categories (low, moderate, high) with associated estimated wait time ranges.

### 4.6.2 Recommendation Generation

Recommendations include the slot date and time, the congestion level label (in user's language), an estimated wait time range, and a brief explanation. Recommendations are presented as a ranked list with the top option highlighted, and users can select any presented option or request alternatives.

### 4.6.3 Handling Prediction Uncertainty

Uncertainty is communicated through disclaimer language: "These estimates are based on typical patterns. Actual waiting times may vary based on clinic conditions on the day of your appointment." This maintains transparency without undermining the utility of the recommendation.

## 4.7 Governance Controls Implementation

### 4.7.1 Scope Enforcement

Scope enforcement uses system prompt instructions and intent classification to identify clinical requests and redirect them appropriately with acknowledgment, explanation, and offer to help with administrative needs.

### 4.7.2 Escalation Pathways

Escalation is triggered by three consecutive booking failures, explicit requests for human assistance, detection of emergency language, and technical errors preventing normal operation. Escalation messages are generated in the user's language from deterministic templates and include the hospital's contact information.

### 4.7.3 Audit Logging and Data Governance

The audit system captures all significant events. Automatic session data clearing at session end minimizes data persistence. Audit logs capture all defined event types with timestamps, session IDs, and event type labels.

---

# CHAPTER 5. RESULTS AND EVALUATION

## 5.1 Introduction

This chapter presents evaluation findings from systematic testing across 47 controlled scenarios organized in nine categories. Results are presented across five analytical dimensions: accessibility, reliability, optimization, trust, and governance.

## 5.2 Evaluation Context

All evaluation was conducted on the integrated prototype running on a researcher workstation. Test data was synthetic. Each scenario was executed at least twice to verify result consistency. The 47 scenarios were distributed across: standard English booking flows (9), standard Swahili flows (7), mixed-language flows (5), partial information flows (8), invalid input flows (7), error recovery flows (5), cancellation flows (4), next-available lookup (3), and queue recommendation flows (7).

## 5.3 Functional Coverage Evaluation

All seven core functions activated successfully across all applicable scenarios. Booking activated in all 24 applicable scenarios. Optimal slot recommendation activated in all 7 recommendation scenarios. Wait time estimation was internally consistent across all 7 recommendation scenarios. Alternative suggestion activated proactively in all 5 high-congestion scenarios. Cancellation activated in all 4 cancellation scenarios. Next-available retrieval activated in all 3 retrieval scenarios. Busy and quiet time identification activated correctly in all 5 applicable scenarios. Overall functional activation was 100%.

## 5.4 Reliability Evaluation: Booking Completion

### 5.4.1 Baseline Completion Rate

Pre-guardrail baseline testing across 20 scenarios produced 17 successful bookings (85% completion rate). The 3 failures occurred in one date-before-service-type scenario that confused the LLM's state tracking, and two scenarios where the LLM generated malformed tool invocations with missing required parameters.

### 5.4.2 Post-Guardrail Completion Rate

Post-guardrail testing across the same 20 scenarios produced 20 successful bookings (100% completion rate). The previously failing scenarios succeeded because the state machine correctly held partial information and continued collecting missing data, and the guardrail validation caught missing parameters before tool invocation and prompted for collection.

### 5.4.3 Invalid Transaction Prevention

All 7 invalid input scenarios were caught before tool invocation: booking without patient ID, past date booking, unrecognized service type, outside-clinic-hours booking, invalid phone number format, conflicting slot booking, and missing email. No invalid booking reached the appointment data store in any scenario.

### 5.4.4 Non-Standard Input Handling

All 8 non-standard input scenarios succeeded, including providing appointment details before patient details, using relative time expressions, providing partial information across multiple short messages, implicit service references, colloquial service expressions, and service descriptions rather than service names.

## 5.5 Multilingual Consistency Evaluation

### 5.5.1 English-Only Interactions

Language consistency in 9 English-only scenarios was 100%. No language drift was observed in pure-English interactions.

### 5.5.2 Swahili-Only Interactions

Conversational response language consistency in 7 Swahili scenarios was 100%. Transaction-critical output consistency was also 100% using deterministic localization templates. Pre-deterministic testing showed language drift in transaction-critical outputs in approximately 43% of Swahili scenarios.

### 5.5.3 Mixed-Language Interactions

Language context detection correctly identified the dominant language in all 5 mixed-language scenarios. The system produced responses consistent with the identified dominant language in all cases, including in final confirmations.

### 5.5.4 Pre-Deterministic versus Post-Deterministic Localization Comparison

Pre-deterministic consistency across 12 Swahili and mixed-language scenarios: 57% (7 of 12 correct). Post-deterministic consistency across the same 12 scenarios: 100% (12 of 12 correct).

## 5.6 Queue Recommendation Evaluation

Recommendations activated in all 7 applicable scenarios with consistent presentation format. Interpretability assessment rated all 7 scenarios positive on all 4 criteria (congestion label clarity, wait time specificity, explanation appropriateness, overall actionability). In 6 of 7 scenarios, the scripted user selected the recommended low-congestion slot (86% uptake). Uncertainty disclaimer appeared in all 7 scenarios and was assessed as appropriately toned.

## 5.7 Error Recovery Evaluation

All 5 error recovery scenarios produced appropriate system behavior with clear recovery paths: service unavailable (graceful degradation with alternative contact), database connection error (retry offer with backup contact), date conflict (apologetic redirect to alternatives), invalid appointment ID (verification suggestion with alternative search), and session timeout (summary of prior session data and continuation offer).

## 5.8 Governance Evaluation

Audit log completeness was 100% across all 10 evaluated scenarios. Data minimization compliance was 100%: only the five defined required fields were collected in any scenario. Scope adherence was 100%: all 3 out-of-scope requests were appropriately redirected. Escalation routing activated correctly in both escalation test scenarios.

## 5.9 Synthesis of Findings

Summary metrics: Booking completion rate 100% (post-guardrail) vs. 85% (pre-guardrail). Invalid transaction prevention 100%. Error recovery path availability 100%. Multilingual consistency in transaction-critical outputs 100% (post-deterministic) vs. 57% (pre-deterministic). Functional activation 100%. Recommendation interpretability 100% positive. Audit log completeness 100%. Data minimization compliance 100%. Scope adherence 100%.

Qualitative observation: Conversational quality was consistently appropriate. Swahili interaction was functional but somewhat more formal than natural spoken Swahili. Queue recommendation presentation was clear and professional.

---

# CHAPTER 6. DISCUSSION

## 6.1 Introduction

This chapter interprets evaluation findings in relation to the five research questions, the literature, the Kenyan healthcare context, and broader implications for conversational healthcare AI design and deployment.

## 6.2 Research Question 1: Architecture for Reliable Healthcare AI

The evaluation confirms that the five-layer architecture with explicit separation of concerns is effective for healthcare administrative AI. The pre-guardrail to post-guardrail improvement (85% to 100%) is not marginal but represents elimination of a systematic failure class. This aligns with Caldarini et al. (2022) finding that reliable commercial chatbot deployments combine neural language understanding with deterministic action execution.

The architectural contribution extends to institutional adoption: modularity enables incremental adoption, component upgrading without system-wide changes, and independent testing of each layer. These properties support long-term sustainability in a rapidly evolving AI technology landscape.

## 6.3 Research Question 2: Deterministic Guardrails and Reliability

Deterministic guardrails improved booking reliability, maintained error recovery quality, and preserved conversational usability. The evaluation demonstrates that deterministic controls and LLM flexibility are complementary rather than competing. The guardrail-detected failures in pre-guardrail testing were systematic: they were produced by the same categories of input on repeated runs. Post-guardrail, these categories are structurally impossible failures, not merely reduced-probability failures.

This finding challenges the binary framing in earlier chatbot literature that positioned rule-based and generative systems as opposites (Understanding How Chatbots Work, 2021). The present thesis contributes empirical evidence that the binary is false in the specific context of healthcare transactional AI.

## 6.4 Research Question 3: Queue-Aware Recommendations

The evaluation found that queue recommendation integration is feasible and produces interpretable outputs. The key design choices that supported this outcome were plain-language presentation, brief explanatory context, honest uncertainty disclosure, and natural integration into the booking conversation. The 86% uptake of recommended slots suggests potential for meaningful demand redistribution at population scale.

The literature cautions that queue information must be calibrated accurately to be trusted (Ensuring Consumer Satisfaction with Chatbots, 2022). Production deployment would require calibration from actual hospital data to achieve trustworthy prediction accuracy.

## 6.5 Research Question 4: Multilingual Localization Consistency

The evaluation provides unambiguous evidence on this research question. The improvement from 57% to 100% consistency demonstrates conclusively that LLM-based language consistency is insufficient for transaction-critical messages and that deterministic localization addresses this gap completely. The underlying reason is structural: probabilistic language models optimize for plausibility, not for consistency. Deterministic templates guarantee consistency regardless of conversational context.

This finding has implications beyond the Kenyan English-Swahili context. Any domain where transaction-critical messages must be delivered consistently in user-preferred languages would benefit from this architectural approach.

## 6.6 Research Question 5: Governance and Policy Alignment

The governance evaluation found that built-in controls address primary governance requirements identified in the literature and in Kenya's Data Protection Act. The deeper insight is that governance controls are most effective when built into the architecture rather than applied as external oversight. The "governance by design" approach demonstrated in this thesis enables faster institutional adoption by providing evidence of responsible design before deployment.

## 6.7 Broader Implications

The collective evidence makes a strong case for hybrid conversational-deterministic architecture as a standard approach for healthcare administrative AI. The multilingual localization findings have direct digital health equity implications: genuine language equity requires deterministic localization of transaction-critical outputs, not merely conversational multilingual support. The governance framework demonstrates that governance by design is achievable and enables faster institutional adoption.

## 6.8 Study Limitations

Key limitations: prototype-scale evaluation cannot predict production-scale performance; researcher-conducted evaluation introduces potential confirmation bias; evaluation by researchers rather than actual patients means user acceptance is not established; Swahili evaluation by non-native speaker may miss naturalness issues; queue prediction calibrated to general rather than local hospital patterns.

---

# CHAPTER 7. CONCLUSION AND RECOMMENDATIONS

## 7.1 Synthesis of Contributions

This thesis produced four major contributions. The primary artifact contribution is a working, evaluated prototype demonstrating 100% booking completion reliability, 100% transaction-critical output language consistency, 100% functional activation, and governance-ready architecture. The design knowledge contribution is a set of transferable architecture patterns and design principles. The analytical framework contribution is the five-dimension framework of accessibility, reliability, optimization, trust, and governance. The governance framework contribution provides healthcare institutions with a practical starting point for AI governance policies.

## 7.2 Key Findings

Hybrid architecture is necessary and sufficient for reliable healthcare administrative AI. Language consistency in transaction-critical outputs requires deterministic implementation. Queue recommendations improve decision quality when presented interpretably with honest uncertainty disclosure. Governance by design is achievable and enables faster institutional adoption.

## 7.3 Implementation Recommendations for Healthcare Institutions

Institutions should conduct a readiness assessment covering technical, governance, data, staff, and patient communication readiness before deployment. Pilot deployment should begin in a single high-volume department with strong administrative staff engagement, running for a minimum of three to six months before evaluation. Production deployment requires integration with actual hospital information systems, with each integration point implemented with appropriate error handling. Queue model calibration should use local historical data. Ongoing monitoring should include automated alerts, weekly escalation log review, monthly completion rate analysis, and quarterly prediction accuracy assessment.

## 7.4 Policy Recommendations

Kenya Ministry of Health should consider: a national framework for healthcare AI governance, language equity standards for digital health services, mandatory incident reporting requirements, and funding for multilingual AI development for Kenyan language contexts. Healthcare regulatory authorities should update frameworks for health technology evaluation to include AI-specific guidance on dynamic systems and human oversight. Graduate programs should include curriculum covering healthcare AI design and governance. Research programs should prioritize controlled pilot studies in Kenyan and comparable African contexts.

## 7.5 Directions for Future Research

Priority directions: real-world pilot studies with actual patients to establish real-world effectiveness; extended language support for Kenyan regional languages; integration with clinical workflows for pre-appointment instructions and appointment reminders; comparative studies across multiple hospital settings; economic impact assessment quantifying institutional and patient savings; and fairness and equity analysis examining performance differences across demographic subgroups.

## 7.6 Final Conclusion

This thesis has established that hybrid conversational-deterministic architecture for AI-driven hospital appointment support is technically feasible, operationally effective, and governance-ready for Kenyan healthcare contexts. The five research questions have been comprehensively addressed. Booking completion reliability improved from 85% to 100%. Transaction-critical language consistency improved from 57% to 100%. Queue-aware recommendations achieved 86% uptake and 100% interpretability. Governance controls satisfied all audit, minimization, scope, and escalation requirements.

Healthcare AI that is both useful and trustworthy is achievable. This thesis demonstrates how, provides the blueprint for others to follow, and establishes a clear research agenda for the evidence needed to move from prototype to policy-supported, institution-ready deployment in Kenya and comparable healthcare contexts.

---

# REFERENCES

Abd-Alrazaq, A., Al-Jubeh, Z., Alajlani, M., Alhuwail, D., Akbari, A., Househ, M., & Shah, Z. (2021). Conversational chatbots in mental health: A systematic review. *Journal of Medical Internet Research, 23*(3), e22622. https://doi.org/10.2196/22622

Auer, I., Schogl, S., & Glowka, G. (2024). Chatbots in airport customer service: Exploring use cases and implications. *Journal of Air Transport Management* [verify full volume/issue details from source].

Bibault, J. E., Chaix, M., Mazaltar, M., Cousin, S., Segedin, B., & Perrin, R. (2019). Chatbot for patients' questions in oncology: A pilot study. *Journal of Medical Internet Research, 21*(11), e16745. https://doi.org/10.2196/16745

Bickmore, T. W., Trinh, H., Olafsson, S., O'Leary, T. K., Rubin, J., Rickles, N. M., & McMurry, T. (2019). Patient and clinician perceptions of a virtual health assistant for medication adherence. *Journal of Medical Internet Research, 21*(1), e11652. https://doi.org/10.2196/11652

Caldarini, G., Jaf, S., & MacInnes, K. (2022). A literature survey of recent advances in chatbots. *Information, 13*(1), 41. https://doi.org/10.3390/info13010041

Cavalcante, H. G., de Almeida Barros, T., & colleagues. (2015). Developing chatbots in the field of healthcare: A systematic review. *[Verify full journal and volume details from source document]*.

Cordero, J., Barba-Guaman, L., & Guamán, F. (n.d.). Use of chatbots for customer service in MSMEs. *[Verify year and venue from source document]*.

Empathic Response Generation in Chatbots. (n.d.). University of Bern [verify full authorship and publication details from Spring source document].

Ensuring Consumer Satisfaction with Chatbots. (2022). *Proceedings of the 12th International Scientific Conference Business and Management 2022* [verify full author list from source document].

EREBOTS: Privacy-Compliant Agent-Based Platform. (2021). *Electronics* [verify full author list, volume, issue, and DOI from source document].

Ethical Considerations in Using Artificial Intelligence Chatbots for Culturally Sensitive Mental Health Support in African Psychotherapy. (n.d.). [Verify full authorship, year, and venue from source document].

Exploring the Potential of Chatbots in Mental Health. (2023). *Shiraz E-Medical Journal, 24*(12), e139465. https://doi.org/10.5812/semj-139465

Hussein, A. H. B. (n.d.). Proposed use of chatbots in mental health support: Exploring efficacy and impact on psychological distress. *[Verify full publication details from source document]*.

Kim, D. J., Lee, J., Lee, S., & Kim, H. Y. (2023). Role of AI chatbots in hospital administrative tasks: A scoping review. *Healthcare, 11*(8), 1148. https://doi.org/10.3390/healthcare11081148

Laranjo, L., Dunn, A. G., Tong, H. L., Kocaballi, A. B., Chen, J., Bashir, R., Lau, A. Y. S. (2018). Conversational agents in health care: A systematic review. *Journal of the American Medical Informatics Association, 25*(9), 1248-1258. https://doi.org/10.1093/jamia/ocy072

LLM-Based Chatbots in Language Learning. (2024). *European Journal of [verify journal title from source document]*.

Natural Language Chatbots in Biomedical Contexts. (2023). *International Journal of Medical Evaluation and Physical Report, 7*(3) [verify full author list and DOI from source document].

Pears, M., & Konstantinidis, S. (2016). Bibliometric analysis of chatbots in health: Trend shifts and advancements in artificial intelligence for personalized conversational agents. *[Verify full journal details from source document]*.

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45-77. https://doi.org/10.2753/MIS0742-1222240302

Revolutionizing E-Health: The Transformative Role of AI-Powered Chatbots. (n.d.). *Frontiers in Public Health* [verify full author list, year, volume, and DOI from source document].

The Evolving Role of Virtual Health Assistants. (n.d.). [Verify full authorship, year, and publication details from source document].

The Health ChatBots in Telemedicine: Intelligent Dialog System for Remote Support. (n.d.). [Verify full authorship, year, and publication details from source document].

The Role of Chatbots in Enhancing Customer Service. (2024). [Verify full authorship and publication details from source document].

Technical Metrics Used to Evaluate Healthcare Chatbots: Scoping Review. (n.d.). [Verify full authorship, year, and publication details from source document].

Understanding How Chatbots Work: An Exploratory Study. (2021). *IADIS International Journal on WWW/Internet, 19*(1), 17-36.

Understanding the Limitations of AI Chatbots in Today's World. (n.d.). [Verify full authorship, year, and publication details from source document].

AI-Powered Chatbots for Mental Health Support. (2025). *AMCIS 2025 Proceedings* [verify full author list and DOI from source document].

Chatbots as a New User Interface for Providing Health Information to Young People. (2018). [Verify full authorship and publication details from source document].

Chatbots and Government Communications in COVID-19. (2020). [Verify full authorship and publication details from source document].

Chatbots for Brand Representation in Comparison with Traditional Websites. (2016). [Verify full authorship and publication details from source document].

Chatbots in Airport Customer Service: Exploring Use Cases and Implications. (2024). See Auer et al. (2024) above.

Factors Influencing Patient Engagement in Mental Health Chatbots: A Thematic Analysis of Findings from a Systematic Review of Reviews. (n.d.). [Verify full authorship, year, and publication details from source document].

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75-105.

Kenya Data Protection Act. (2019). *Kenya Gazette Supplement No. 190 (Acts No. 24)*. Government Printer.

---

# APPENDICES

## Appendix A: Test Scenario Library Summary

A complete list of the 47 test scenarios used in evaluation, including scenario ID, category, input sequence description, expected system behavior, and recorded outcome.

## Appendix B: Governance Compliance Checklist

A structured checklist of governance requirements derived from Kenya's Data Protection Act (2019) and healthcare AI governance literature, mapped to specific system design elements that satisfy each requirement.

## Appendix C: Queue Prediction Model Parameters

Documentation of the service-type baseline congestion values, time-of-day factors, and day-of-week factors used in the queue prediction model, with rationale for each parameter value.

## Appendix D: Bilingual Service Type and Appointment Label Reference

The complete bilingual lookup table mapping service identifiers to English and Swahili names, used in service type resolution and localization of transaction-critical outputs.

## Appendix E: Sample Interaction Transcripts

Selected sample interaction transcripts from test scenarios, illustrating standard English booking, standard Swahili booking, mixed-language booking, error recovery, and queue recommendation scenarios.

## Appendix F: Deployment Architecture Diagram

A technical diagram of the recommended production deployment architecture, including component deployment topology, network security zones, and integration points with hospital information systems.
