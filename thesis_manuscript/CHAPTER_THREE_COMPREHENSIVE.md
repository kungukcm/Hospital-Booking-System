# CHAPTER 3. RESEARCH METHODOLOGY

## 3.1 Introduction

This chapter describes the philosophical foundations, research design, methodological framework, and evaluation strategy that guide the development and assessment of the AI-driven hospital appointment support artifact. The chapter explains why the design science research (DSR) paradigm was chosen for this study, how it was adapted for the specific context of healthcare conversational AI, what design processes were followed from problem identification through artifact evaluation, and how results are analyzed and interpreted.

Research methodology in information systems studies must address questions across multiple levels: the philosophical assumptions that guide what counts as knowledge and how it is generated, the strategy that structures how research questions are approached, the methods used to collect and analyze data, and the evaluation criteria that determine whether research objectives have been achieved. This chapter addresses all four levels in relation to the present study.

A critical observation that motivates the methodological approach is that the central research problem in this thesis is not an explanatory problem. Explaining why hospitals have scheduling challenges or why patients prefer certain appointment times requires behavioral or positivist research methods. The research problem is a design problem: how to create a system that solves specific healthcare administrative challenges in a specific socio-technical context. Design problems require design-oriented research methods that evaluate candidate solutions against requirements derived from the problem context.

## 3.2 Research Philosophy and Paradigm

### 3.2.1 Pragmatism as the Guiding Philosophical Orientation

The philosophical orientation of this thesis is pragmatism, combined with elements of critical realism about social institutions and technologies. Pragmatism, as articulated in the tradition of William James, John Dewey, and Charles Sanders Peirce, holds that knowledge should be evaluated by its consequences: by whether it enables effective action in the world. For pragmatist research, the question is not only "what is true?" but "what works?" and "for whom does it work?" These questions are fundamentally action-oriented and practically focused.

In the context of this thesis, pragmatism manifests in three specific ways. First, the research aim is explicitly practical: to design and evaluate a system that improves healthcare administrative outcomes, not merely to demonstrate that such a system is theoretically conceivable. Second, the evaluation criteria are outcome-oriented: the system is assessed not primarily by whether it uses the best available technology but by whether it reliably completes bookings, provides useful recommendations, and maintains language consistency. Third, the research is designed to produce knowledge that practitioners and policy-makers can use, not only knowledge that advances academic theory.

Critical realism contributes to the philosophical stance by acknowledging that hospitals, patients, and administrative systems have an independent existence beyond the researcher's perspective. The problems identified in the research problem statement, transactional unreliability, queue opacity, and multilingual inconsistency, are real problems experienced by real patients and staff, not constructs invented by the researcher. The artifact must work in this real world, not only in a theoretically constructed research world.

### 3.2.2 Positioning Relative to Other Research Paradigms

Positivist research assumes that social reality can be studied through observation and measurement in the same way as natural phenomena. It typically involves hypothesis testing through experimental or quasi-experimental designs with statistical analysis. While positivism is appropriate for many research questions in healthcare and information systems (for example, examining whether patients who use digital scheduling are more likely to attend appointments than those who schedule by phone), it is not well-suited to the design problem addressed here. The thesis does not test whether an existing phenomenon occurs; it creates a new phenomenon.

Interpretivism assumes that social reality is constructed through meaning and interpretation and is best understood through rich qualitative engagement with participants' perspectives. Interpretivist approaches would be appropriate for research examining how patients experience conversational AI scheduling systems or how administrative staff interpret AI system behavior. These are important research questions but they are not the primary questions addressed here.

Design science research occupies a distinctive methodological position by focusing on the creation of artifacts that solve real problems. Unlike positivism (which observes existing phenomena) or interpretivism (which interprets meaning in existing situations), DSR changes the world by creating new things. The rigor in DSR comes from the discipline of the design process (the artifact must address a clearly defined problem), the evaluation (the artifact must be assessed against explicit criteria in relevant scenarios), and the communication of generalized design knowledge (what was learned must be expressed in a form useful beyond this specific artifact).

## 3.3 Design Science Research Framework

### 3.3.1 Foundations of Design Science Research

Design science research in information systems was formally articulated as a legitimate and rigorous research paradigm by Hevner et al. (2004), who proposed seven guidelines for DSR: create a viable artifact, address a relevant problem, evaluate the artifact's utility, make contributions to knowledge, follow rigorous research methods, treat artifact design as a search process, and communicate research results to both academic and practice audiences. This framework established DSR as a complement to behavioral science research in IS, arguing that the field requires both kinds of knowledge: explanatory knowledge about how IT systems affect organizational behavior and constructive knowledge about how to design better IT systems.

Peffers et al. (2007) developed a DSR methodology process model that provides a structured approach to conducting DSR: identify and motivate the problem, define the objectives of a solution, design and develop the artifact, demonstrate the artifact in realistic scenarios, evaluate the artifact's performance against the defined objectives, and communicate the findings and contributions. This process model is widely used in IS research and provides the structural backbone of the present thesis.

The present thesis follows the Peffers et al. (2007) process model adapted for the healthcare AI context. The adaptation involves several modifications: the evaluation strategy incorporates health-specific reliability and safety metrics alongside standard task completion metrics, the scenario design reflects realistic healthcare administrative challenges rather than generic information systems scenarios, and the communication of findings includes explicit governance guidance relevant to healthcare deployment contexts.

### 3.3.2 Artifact Types in Design Science Research

DSR produces several types of artifacts: constructs (concepts and vocabulary for describing problems and solutions), models (abstractions that represent the problem or solution domain), methods (algorithms and guidelines for performing tasks), and instantiations (working systems or prototypes that demonstrate that the design works in practice). Each type of artifact contributes different kinds of knowledge.

The present thesis produces primarily an instantiation artifact, a working prototype of the AI appointment support system, supported by construct artifacts (the five-dimension analytical framework of accessibility, reliability, optimization, trust, and governance) and method artifacts (the hybrid conversational-deterministic architecture and the design iteration process). The instantiation provides the most direct evidence of what is possible in healthcare AI design; the constructs and methods provide the generalizable knowledge that extends beyond the specific prototype.

### 3.3.3 Adaptation of DSR for Healthcare Conversational AI

Standard DSR frameworks do not specifically address the challenges of healthcare AI design, which introduce additional requirements not present in generic information systems design. These healthcare-specific requirements include clinical boundary maintenance (the artifact must clearly identify and enforce the limit between administrative support and clinical advice), patient safety considerations (evaluation must address scenarios where system failure could affect patient care access), regulatory alignment (the artifact must be designed with awareness of applicable regulatory requirements), and language equity (in the Kenyan context, equitable service quality in both English and Swahili is an ethical requirement).

The adapted methodology incorporates these requirements into each phase of the DSR process. In problem identification, healthcare-specific failure modes (such as language drift at transaction completion) are explicitly included alongside generic chatbot limitations. In solution objective definition, patient safety and equity objectives are articulated alongside technical reliability and usability objectives. In evaluation, safety and governance metrics are evaluated alongside reliability and language consistency metrics. In communication, governance implications for healthcare deployment are explicitly addressed.

## 3.4 Research Design

### 3.4.1 Overall Research Design

The overall research design is an iterative artifact design and evaluation study following the DSR process model. The study does not follow a traditional research design with a single data collection phase followed by analysis; instead, it comprises multiple design-build-test cycles, each of which produces incremental improvements in artifact capability and generates learning that informs subsequent cycles.

This iterative design is appropriate for the research problem for several reasons. The challenges addressed, transactional reliability, multilingual consistency, and queue recommendation quality, interact with each other in ways that are difficult to predict before implementation. A single-cycle design would require complete specification of all requirements before building, but some requirements only become clear during implementation when specific interaction patterns reveal unexpected failure modes. Iterative design accommodates this inherent uncertainty while maintaining research rigor through explicit documentation of what each cycle attempted to address and what was learned.

The research design integrates multiple types of evidence: design decisions are guided by literature, implementation knowledge, and evaluation feedback; evaluation uses controlled scenarios that provide consistent evidence across conditions; and interpretation draws on literature to situate findings in the broader context of healthcare AI research. This triangulation of evidence types supports the credibility and trustworthiness of findings.

### 3.4.2 Design Iteration Cycles

The five major design iteration cycles each addressed a specific challenge domain within the overall research problem.

The first cycle established the baseline conversational booking capability: understanding user requests, collecting required information through multi-turn dialogue, and executing booking commands. The primary question addressed was whether LLM-based conversation was capable of understanding healthcare appointment booking requests expressed in natural language with realistic variation and colloquialism. The first cycle established that LLM understanding was sufficient for the domain but that tool invocation reliability required additional controls.

The second cycle addressed tool-call stability and schema compliance. Early implementation in the first cycle revealed systematic LLM tool-call failures: parameters omitted, formats incorrect, and schemas inconsistently satisfied. The second cycle simplified tool schemas to reduce the opportunity for format errors, added pre-invocation parameter validation that catches schema violations before they reach the backend, and implemented retry logic that guides the system to collect missing parameters rather than failing silently. The key question was: can parameter validation logic effectively prevent invalid tool calls without sacrificing conversational usability?

The third cycle addressed deterministic workflow control. User testing during the second cycle revealed that the system became confused when users provided information in non-standard order (providing date before service type, for example) or used implicit references to earlier conversation turns. The third cycle introduced a graph-based state machine that defines valid workflow states and permitted transitions, ensuring that the system maintains consistent knowledge of what information has been collected and what remains needed, regardless of conversational order. The key question was: does state machine orchestration eliminate sequence-dependent failures without creating workflow rigidity that frustrates users?

The fourth cycle addressed multilingual support and localization consistency. After the booking workflow was stable in English, Swahili support was added. Initial multilingual testing revealed the language drift problem: conversation conducted in Swahili produced English-language final confirmations. The fourth cycle implemented deterministic language detection, response language tracking through conversation state, and translation of transactional outputs through lookup tables and localized templates rather than LLM translation. The key question was: can deterministic localization mechanisms maintain language consistency end-to-end without requiring complete duplication of system logic?

The fifth cycle addressed integration, edge-case testing, and governance framing. The final cycle assembled all components into an integrated system, tested complex scenarios that combined multiple challenges (mixed language input with partial information and error recovery), and explicitly documented governance implications and required safeguards. The key question was: does the integrated system perform reliably across the full range of realistic scenarios, and what governance framework is needed for responsible deployment?

### 3.4.3 Validation Gates Between Cycles

Each cycle concluded with a validation phase that assessed whether the cycle's objectives had been met before proceeding to the next cycle. Validation checks included: no regressions in previously working functionality, new functionality working reliably in dedicated test scenarios, code quality standards maintained, and documentation adequate for future maintenance. Only when all validation checks passed did the next cycle begin. This disciplined gate approach prevented technical debt accumulation and ensured that the artifact was stable at each stage.

## 3.5 Case and Setting

### 3.5.1 Case Context: KUTRRH and Kenyan Referral Healthcare

The research case is the administrative scheduling challenge at Kenyatta University Teaching, Referral and Research Hospital (KUTRRH), used as an illustrative and representative context for Kenyan referral hospital scheduling needs. KUTRRH is a 500-bed tertiary teaching and referral facility that serves both specialist and general outpatient populations. The hospital's diverse departmental structure, high patient volume, and multilingual patient population make it a suitable and challenging case for demonstrating the artifact's capabilities.

The case selection followed theoretical sampling principles from qualitative research: the case was chosen because it represents the conditions under which the research questions are most sharply posed, not because it is statistically representative of all Kenyan hospitals. KUTRRH's complexity makes it a more challenging test environment than a smaller single-specialty clinic, and design knowledge generated in this more complex context is likely to be applicable to simpler contexts as well.

The evaluation is conducted as a controlled prototype evaluation rather than as a live deployment study. This choice reflects both ethical considerations (live patients should not be exposed to unvalidated system behavior) and methodological advantages (controlled scenarios allow systematic testing of specific conditions that may occur rarely in natural use). The implications of prototype-scale evaluation for generalizability are explicitly acknowledged in the limitations discussion.

### 3.5.2 Service Types and Scheduling Context

The artifact was designed and evaluated in relation to the healthcare services typically available at tertiary referral hospitals in Kenya. Service types in the system include general outpatient services, cardiology, orthopedics, oncology, nephrology, neurology, pediatrics, obstetrics and gynecology, ophthalmology, physiotherapy, and radiology, among others. This service taxonomy reflects realistic appointment booking scenarios where patients may express their service need in varied ways ("heart doctor," "Daktari wa moyo" in Swahili, "cardiologist," "cardiac consultation") and where the system must map varied expressions to valid service identifiers.

The scheduling context includes appointment slots distributed across a standard working week (Monday through Friday, 8:00 AM to 5:00 PM), with different services having different availability patterns (some services available all days, some only on specific days, some with variable specialist availability). Queue prediction is calibrated to general patterns observed in high-volume tertiary hospitals, with peak hours in mid-morning and early afternoon.

## 3.6 Artifact Description and Architecture

### 3.6.1 Overview of Artifact Components

The artifact consists of seven integrated subsystems, each responsible for a specific aspect of system function.

The frontend conversational interface provides the patient-facing interaction layer, implemented as a web-based chat interface that allows patients to type messages in natural language and receive conversational responses. The interface is built using Streamlit, chosen for its rapid development capabilities, built-in session state management, and ability to display both conversational content and structured information (such as appointment options) in a single view.

The orchestration graph handles workflow management, implementing the state machine that defines valid stages of the booking process and the transitions between them. This component is the central coordination layer that ensures the system never attempts to execute a booking without first passing through all required information-collection stages.

The LLM-powered language understanding component provides natural language understanding and response generation using Claude (Anthropic). This component interprets user intent, extracts information entities from natural language, detects language context, and generates conversational responses. The LLM interacts with the orchestration layer to receive current workflow context and with the tool layer to receive operation outcomes.

The deterministic parser and guardrail module provides rule-based validation of extracted information entities before they are used in tool invocations. This component validates that dates are correctly formatted and in the future, that service types correspond to valid system service identifiers, that phone numbers meet expected format requirements, and that all mandatory booking parameters are present and consistent before the booking tool is invoked.

The appointment operation tools provide the interface to backend appointment operations, including create booking, cancel appointment, retrieve next available, and check conflicts. Each tool has a strict schema defining required parameters, optional parameters, return types, and error conditions. Parameter schemas are intentionally simplified to reduce the opportunity for type errors.

The queue estimation and recommendation subsystem provides the prediction logic for estimating expected waiting times at different appointment slots. This subsystem uses a model combining service-type baseline wait times, time-of-day factors (reflecting typical patient volume patterns), day-of-week factors, and assumed staffing levels to produce relative congestion estimates. Rankings are expressed in qualitative terms (low, moderate, high congestion) with associated estimated wait time ranges.

The logging and audit subsystem provides comprehensive event logging, structured to support both development-phase debugging and production-phase governance auditing. Log records capture message events, intent detection outcomes, entity extraction results, tool invocations and their results, error conditions, and system state transitions, all with timestamps and session identifiers.

### 3.6.2 Technology Stack

The artifact is implemented in Python 3.10, using the following principal components: Streamlit for the web interface, the LangGraph framework for workflow graph management, the Anthropic Python SDK for LLM interaction, and a JSON-based data store for appointment record persistence (appropriate at prototype scale; production deployment would use a relational database). The artifact runs on standard consumer-grade hardware and has been tested on deployment platforms including Streamlit Cloud and standard Docker environments.

The choice of Python reflects the dominance of this language in AI and machine learning development, the availability of mature libraries for all required functions, and the accessibility of the language to developers at institutions considering adaptation or extension of the artifact. The specific LLM (Claude) was chosen for its capability in both English and Swahili, its support for explicit tool use, and its compliance with data processing requirements through Anthropic's API terms.

## 3.7 Data Sources and Management

### 3.7.1 Design and Implementation Data

The primary data in the study are the design documentation, implementation artifacts, and evaluation outcomes produced during the research process. Design documentation includes architectural diagrams, design rationale records, and the decisions made at each iteration cycle. Implementation artifacts include the source code, configuration files, and test scripts. Evaluation outcomes include the scenario execution records, outcome metrics, and error logs from the evaluation phase.

These data are not collected from external sources but produced by the researcher through the design and evaluation process. Their quality is ensured through systematic documentation practice: each design decision is documented with its rationale, each evaluation scenario is precisely defined before execution, and each outcome is recorded using consistent categorization.

### 3.7.2 Synthetic Test Data

Evaluation requires patient data and appointment scenarios. To avoid the ethical and practical complexities of using real patient data in a prototype evaluation, all test data is synthetic: patient names, identification numbers, contact details, and appointment histories are fabricated but realistic in structure and content. Test appointments reflect realistic patterns of service type distribution, time preference clustering, and seasonal variation, calibrated to public data on appointment patterns in East African referral hospitals.

The use of synthetic data is a deliberate methodological choice that enables rigorous edge-case testing without privacy risk. Real patient data could not easily be used to test error conditions (providing invalid patient ID, attempting to book non-existent services), which are among the most important test scenarios. Synthetic data allows systematic construction of test cases that exercise specific system behaviors.

### 3.7.3 Secondary Evidence

Secondary evidence from the literature review informs the design choices at each cycle and contextualizes evaluation findings. This evidence is documented in Chapter 2 and referenced in both design rationale documentation and evaluation interpretation. The relationship between literature evidence and design choices is explicitly documented to enable evaluation of whether the design is theoretically grounded and whether evaluation findings are consistent with or diverge from literature predictions.

No real patient clinical data is used at any point in the research. This is an explicit commitment both for ethical reasons and because clinical data is not required for the administrative functions being studied.

## 3.8 Evaluation Strategy

### 3.8.1 Evaluation Philosophy

The evaluation philosophy in this thesis is aligned with Hevner et al.'s (2004) DSR guideline that artifact utility must be rigorously evaluated using appropriate methods. In the context of a conversational AI system for healthcare administration, appropriate evaluation must assess: whether the system functions correctly across all defined use cases (functional evaluation), whether the system handles realistic edge cases without catastrophic failure (reliability evaluation), whether transactional outputs are consistent with requirements (output quality evaluation), and whether the system's design is governance-ready for institutional deployment (governance evaluation).

This comprehensive evaluation approach goes beyond user satisfaction surveys (which assess perceptions of the system) to examine actual system behavior in defined scenarios. This distinction is important: a system that users find conversationally pleasant but that frequently fails to complete bookings correctly is not a successful healthcare administrative system. The evaluation therefore prioritizes behavioral outcomes over perceived quality.

### 3.8.2 Evaluation Methods

The evaluation combines three primary methods: functional testing, scenario-based evaluation, and governance assessment.

Functional testing verifies that each defined system function (booking, cancellation, next-available lookup, queue recommendation) activates correctly and produces correct outputs in standard cases. Functional tests use predetermined inputs with known expected outputs, enabling binary pass-fail assessment of each function.

Scenario-based evaluation uses a library of 47 scenarios covering normal flows, edge cases, error conditions, mixed-language interactions, and complex combinations. Each scenario specifies the user input sequence, the expected system behavior at each turn, and the expected final state. Scenarios were designed to cover the following categories: standard single-language English booking flows, standard single-language Swahili booking flows, mixed-language flows, partial information provision flows, invalid input flows, error recovery flows, cancellation flows, next-available lookup flows, and queue recommendation flows.

Governance assessment evaluates the artifact's compliance with a defined set of governance requirements derived from the literature review and from Kenya's Data Protection Act requirements. Governance requirements assessed include audit log completeness, data minimization in captured fields, scope adherence (no clinical advice provided), escalation routing availability, and language consistency in confirmations.

### 3.8.3 Metrics and Criteria

For reliability evaluation, the primary metrics are booking completion rate (percentage of scenarios where a valid booking was successfully created when user provided the necessary information), invalid transaction prevention rate (percentage of potentially invalid bookings caught before execution), and error recovery rate (percentage of error scenarios where the system provided useful recovery guidance).

For multilingual consistency evaluation, the primary metric is language consistency rate (percentage of transactional outputs where the output language matched the user's demonstrated language preference). Secondary metrics include entity extraction accuracy in Swahili inputs and appropriateness of language detection in mixed-language scenarios.

For queue recommendation evaluation, metrics include recommendation activation rate (percentage of applicable scenarios where recommendations were presented), interpretability score (subjective assessment of whether recommendation language is understandable), and preference uptake (in scenarios where recommendations were presented, the percentage of times the recommended slot was selected).

For governance evaluation, metrics include audit log completeness (percentage of significant system events captured in logs), data minimization compliance (percentage of scenarios where only necessary data was collected), and escalation routing (presence of appropriate escalation pathways in edge-case scenarios).

## 3.9 Reliability, Validity, and Research Quality

### 3.9.1 Reliability of Findings

Research reliability in this context refers to consistency: would repeating the evaluation produce similar results? Several features of the research design support reliability. The use of deterministic system components (state machine, validation logic, localization lookup tables) ensures that the same inputs produce the same outputs on repeated runs. Test scenarios are precisely documented, enabling exact repetition. All evaluation was conducted on the same system implementation, preventing variation due to system changes.

The main threat to reliability in this study is the probabilistic nature of LLM outputs: the same input to the LLM may produce slightly different conversational responses on different runs. This variability is mitigated by the deterministic controls that gate transaction-critical operations: even if the LLM's conversational response varies, the guardrail logic ensuring completeness and validity is deterministic and produces consistent outcomes.

### 3.9.2 Internal Validity

Internal validity addresses whether the evaluation correctly attributes observed outcomes to the design choices rather than to extraneous factors. Internal validity is supported through iterative testing with explicit documentation of what changed between iterations, enabling attribution of outcome changes to specific design modifications. When a baseline pre-guardrail completion rate is compared with a post-guardrail rate, and the only change between conditions was the addition of guardrail logic, the difference in completion rate can be attributed to the guardrails with reasonable confidence.

The main threat to internal validity is the possibility that evaluation scenarios do not accurately represent realistic user behavior. This threat is partially mitigated by designing scenarios based on documented patterns of user behavior in appointment booking contexts from the literature and by including non-standard interaction sequences that challenge the system in ways that realistic users might.

### 3.9.3 External Validity and Transferability

External validity in DSR is less about statistical generalizability (the artifact was not evaluated on a random sample of hospitals) and more about design knowledge transferability: can the architecture, design principles, and evaluation approach be applied in other contexts? The present thesis addresses transferability through explicit documentation of design principles at a level of abstraction that goes beyond the specific implementation, enabling other institutions and researchers to apply the approach without replicating every implementation detail.

The main limitation on external validity is the prototype-scale evaluation without live user testing. The artifact's performance in controlled scenarios may not perfectly predict its performance with real patients in natural healthcare settings. This limitation is explicitly acknowledged and is proposed as the most important target for future research.

### 3.9.4 Research Ethics

The research does not involve human participants in ways that require ethics board review: no real patients or staff were asked to participate in evaluation, and no real patient data was used. The synthetic evaluation data presents no privacy risks. Institutional ethics considerations are addressed through the governance framework that would govern actual deployment, which the thesis documents but does not implement in a live setting.

The research does engage with the ethical dimensions of AI deployment in healthcare through the governance analysis in Chapter 4 and the policy recommendations in Chapter 7. These analyses treat ethical considerations not as abstract principles but as specific design requirements and governance mechanisms.

## 3.10 Limitations of the Methodology

Several methodological limitations merit explicit acknowledgment.

The prototype-scale evaluation means that performance under production load conditions, with thousands of concurrent sessions and integration with real hospital information systems, is not assessed. Load-dependent behavior may differ from the behavior observed in single-session controlled testing.

The researcher-conducted evaluation introduces the risk of confirmation bias: the researcher who designed the system also conducted the evaluation. This limitation was partially mitigated through the use of pre-defined scenarios and objective metrics that minimize interpretive discretion, but an independent evaluation would provide stronger evidence.

The evaluation by researchers rather than actual patients means that the user experience dimensions of the system's performance are assessed through the researcher's judgment rather than actual patient experience. User acceptance studies with real patients are identified as essential future work.

The Swahili localization evaluation was conducted with researcher-generated Swahili inputs and assessed by the researcher, who has competent but not native Swahili proficiency. Native Swahili speaker evaluation of the localization quality would provide stronger evidence of language consistency performance.

Queue prediction quality was assessed against simulated congestion patterns rather than real appointment data from a Kenyan hospital. The prediction model's accuracy in real-world conditions would require calibration against actual hospital data.

## 3.11 Chapter Summary

This chapter has described the philosophical foundations, design science research framework, research design, case setting, artifact architecture, evaluation strategy, and quality considerations that guide the study. The pragmatist, design-oriented approach is appropriate for the research problem because that problem is fundamentally a design problem: how to create a system that reliably solves specific healthcare administrative challenges in a specific socio-technical context.

The five design iteration cycles provided a structured approach to progressively addressing the challenges of conversational reliability, tool-call stability, workflow control, multilingual consistency, and governance integration. The evaluation strategy combines functional testing, scenario-based assessment, and governance evaluation to provide comprehensive evidence about artifact performance. Reliability, validity, and transferability of findings are addressed through systematic evaluation procedures, explicit documentation of design principles, and honest acknowledgment of limitations.

The following chapter presents the system design and implementation in detail, covering architectural decisions, component design, and the specific mechanisms through which the research objectives are realized in the working artifact.
