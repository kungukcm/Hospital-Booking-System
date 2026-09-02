# CHAPTER 2 SUPPLEMENT D. TRUST, GOVERNANCE, AND ADOPTION LITERATURE

## 1. Introduction

This supplement focuses on the literature relating to trust, governance, adoption readiness, and institutional acceptance of chatbot and AI systems. It complements the technical review by centering the human and organizational factors that shape real-world deployment.

## 2. Trust as a System Property

Trust in AI systems is often discussed as a user attitude, but it is also a system property. A system earns trust through repeated performance that is accurate, predictable, transparent in its reasoning, recoverable when errors occur, and aligned with user expectations. The literature on customer service chatbots and virtual assistants suggests that users are more likely to trust systems that consistently complete tasks and communicate clearly about what they can and cannot do.

## 3. Trust and Completion Reliability

One of the strongest predictors of trust is whether the system actually completes the user’s intended task. In appointment scheduling, this means the booking exists, the confirmation is clear, and the user understands what was booked. If the system only gives fluent text but fails the booking, trust decreases.

The thesis adopts this insight by treating completion reliability as a primary trust metric rather than a secondary implementation detail.

## 4. Governance as Design, Not Just Oversight

The literature on ethics and privacy makes clear that governance should not only exist outside the system. It should also be reflected in the system's design. This includes field-level data minimization where unnecessary personal information is not collected, restricted task scope that prevents the system from making clinical or administrative decisions beyond its domain, traceable event logging so that all significant actions can be audited and reviewed, language-consistent confirmations that ensure users receive transaction details in their chosen language, and escalation pathways to humans where the system is uncertain. The thesis therefore frames governance as a built-in design property rather than an afterthought.

## 5. Institutional Acceptance and Staff Trust

Adoption literature often emphasizes end-user acceptance, but institutional uptake depends on staff trust as well. Front-desk teams, supervisors, and IT teams must believe the assistant reduces workload rather than creates additional ambiguity. Key staff-facing trust factors include believing the system does not produce random or unsafe outputs, following predictable booking logic that staff understand, allowing exceptions to be escalated easily to human review, providing logs that are available for staff review when questions arise, and maintaining clear boundaries by not overreaching into clinical advice.

## 6. Transparency and Explainability

The literature consistently suggests that users trust systems more when outputs are explainable. In this thesis, transparency is implemented by showing:

1. the predicted congestion level;
2. the estimated wait time;
3. the confidence attached to the recommendation;
4. the exact appointment details in final confirmation.

This approach is especially important in scheduling, where decisions are often made under uncertainty.
 the predicted congestion level so users know how busy the chosen slot is, the estimated wait time so they understand the service duration, the confidence attached to the recommendation so they know whether the system is certain or making a guess, and the exact appointment details in final confirmation so there is no ambiguity about what was booked. ## 8. The Role of Human Oversight

A recurring theme in the literature is that high-stakes AI should not function without human oversight. Human oversight is important because it can catch edge cases, handle exceptional workflows, and maintain accountability when the system is uncertain.

In the present thesis, human oversight is designed into escalation pathways rather than added after failure.

## 9. Acceptance Barriers

The literature identifies several barriers to chatbot adoption in sensitive domains:

1. fear of inaccuracy;
2. privacy concerns;
3. poor prior digital experiences;
4. language mismatch;
5. unclear responsibility when things go wrong.
. Institutions and users may fear inaccuracy, particularly when the stakes are high such as in healthcare. Privacy concerns arise around data collection and storage. Poor prior digital experiences with other systems can create skepticism. Language mismatch makes users feel excluded or misunderstood. Finally, unclear responsibility when things go wrong creates ambiguity about who to blame and what recourse exists. The thesis addresses these barriers through deterministic flow control that prevents drift, privacy-aware design recommendations that minimize data collection, and visible language consistency that assures users they are understood
## 11. Human-Centered Communication

Even in administrative workflows, tone matters. The literature on empathic response generation suggests that respectful, supportive, and clear communication can improve user experience. In this thesis, this insight is reflected in polite correction prompts, localized guidance, and supportive follow-up instructions.

## 12. Language and Trust Interdependence

Language consistency is not merely an accessibility issue. It shapes trust because users interpret language drift as system instability. If the assistant starts in Swahili but ends in English at a crucial moment, users may infer that the system is unreliable or inattentive.

The thesis therefore localizes not just conversational turns but transaction-critical outputs.

## 13. Error Recovery as Trust Repair

When errors occur, the system’s response can either destroy trust or repair it. The literature suggests that honest, useful, and immediate error messages can preserve trust better than silence or generic failure notices.

Accordingly, the thesis uses recovery messages that explain what went wrong and what the user should do next.

## 14. Adoption-Readiness Model

Based on the literature, institutional adoption readiness can be summarized as a five-factor model:

1. usability;
2. reliability;
3. privacy;
4. explainability;
5. governance.

The present artifact is designed to perform well on all five factors, though real-world deployment would still require local validation.

## 15. Summary of the Trust Literature

The trust literature confirms that successful AI assistants in healthcare-adjacent settings must do more than respond naturally. They must also behave predictably, respect user language, protect information, and support human oversight. These are not optional extras; they are core requirements for adoption.
. First is usability: the system must be easy for patients and staff to use without extensive training. Second is reliability: the system must complete its core tasks consistently without frequent failures. Third is privacy: the system must protect sensitive information according to legal and ethical standards. Fourth is explainability: the system must help users understand why it made particular recommendations or decisions. Fifth is governance: the system must fit into the institution's oversight structures and accountability mechanisms. 