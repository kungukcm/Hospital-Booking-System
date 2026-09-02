# CHAPTER 3 SUPPLEMENT D. ETHICS, RESEARCH INTEGRITY, AND RESPONSIBLE ARTIFACT DESIGN

## 1. Introduction

This supplement expands the methodological chapter by detailing the ethical and integrity considerations that shaped the research process and artifact design. Although the thesis focuses on a technical assistant, ethical responsibility is central because the system interacts with patient-related information.

## 2. Boundary of the Artifact

The assistant is designed for administrative support only. This boundary is ethically important because it prevents the system from drifting into diagnostic, therapeutic, or triage functions without validation.

The boundary also simplifies user expectations and helps maintain accountability.

## 3. Data Minimization Principle

The artifact captures only the data necessary for booking and scheduling tasks. This includes the patient's name, patient ID, phone number, email address, appointment type being requested, and the desired date and time. This minimal set supports privacy by design and reduces unnecessary exposure of sensitive information that could be misused if compromised.

## 4. Consent and Transparency

Any future deployment should make clear what data is collected and why, how the collected data will be used, how long it is retained before deletion, and what human fallback exists if the system fails. Even in prototype work, these principles are important because they establish the ethical tone for later deployment and help users make informed decisions about engaging with the system.

## 5. Non-Maleficence in Design

The system is built to avoid harm through multiple mechanisms. First, it blocks incomplete bookings rather than allowing users to complete a booking without critical information. Second, it prevents unsupported clinical outputs that could mislead users about medical guidance. Third, it warns users when conflicts exist between requested slots and their other information. Fourth, it offers corrective prompts instead of silently failing and leaving users unaware of problems. Fifth, it maintains scope boundaries to avoid drift into areas it is not qualified for. These design choices express non-maleficence as a practical principle in system architecture.

## 6. Justice and Language Inclusion

Justice in digital health includes fair access across language groups. If one language group receives clearer or more complete output than another, the system is uneven in service quality.

The thesis therefore treats Swahili localization as a justice issue, not only a usability feature.

## 7. Accountability in Development

The research process should be traceable. That means:

1. changes are logged;
2. behavior differences are tied to code revisions;
3. validation steps are documented;
4. known limitations are not hidden.

This strengthens the integrity of the scholarship and the prototype.
 and documented. This means that changes to the codebase are logged, behavior differences are tied to specific code revisions for investigation, validation steps are documented so the work is reproducible, and known limitations are not hidden or downplayed. This strengthens the integrity of the scholarship and the prototype by making clear what was done and what was learned
4. sensitivity to prompt framing;
5. variation across contexts.
. These include non-deterministic behavior where the same input produces different outputs, hallucination risk where models generate plausible-sounding but false information, tool schema mismatch where model outputs do not align with what the calling system expects, sensitivity to prompt framing where slight wording changes produce different results, and variation across contexts where a model performs better in some domains than others. Rather than assuming model correctness, the thesis surrounds the model with controls that compensate for these limitations and prevent them from reaching user
Queue recommendations can influence patient behavior. If not designed carefully, they could unintentionally push users toward unsuitable times. Therefore, recommendation messages must be framed as guidance, not instructions, and should include clarity around uncertainty.

## 11. Human Oversight as Ethical Safeguard

Human oversight is a key safeguard because it provides:

1. exception handling;
2. contextual judgment;
3. accountability;
4. empathy where needed;
5. correction of system errors.

The assistant should therefore complement human servic exception handling when edge cases arise that the system cannot process, contextual judgment that understands the person and situation, accountability through a human responsible for decisions, empathy where needed to address emotional or sensitive requests, and correction of system errors before they harm users. 1. Is the system’s scope clear?
2. Are data capture practices minimal and justified?
3. Are language groups treated equitably?
4. Can users reach a human when needed?
5. Are failures visible and recoverable?
6. Are limitations explicitly stated?

## 14. Future Ethical Considerations

If the assistant is deployed later, additional ethical considerations will include:

1. formal consent language;
2. security review;
3. audit rights;
4. complaint handling;
5. periodic fairness review.

## 15. Conclusion

Ethics is not external to the technical design of this thesis. It is embedded in how the system defines its scope, handles data, communicates uncertainty, and preserves human responsibility.
