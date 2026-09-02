# COVER PAGE

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Kung'u Kelvin Mathigi

Thesis for Master's Degree
2026

Department of Techno Convergence based on ICT Policy
Graduate School of Global Development and Entrepreneurship
Handong Global University

---

# TITLE PAGE (PAGE 1)

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Kung'u Kelvin Mathigi

Thesis for Master's Degree
2026

Department of Techno Convergence based on ICT Policy
Graduate School of Global Development and Entrepreneurship
Handong Global University

---

# TITLE PAGE (PAGE 2)

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Design Science Research for Practical Health-Service Transformation in Kenya

---

# SUBMISSION SENTENCE PAGE

A Design Science Approach to AI-Driven Patient Support and Queue Optimization in Kenyan Hospitals: A Case Study of Kenyatta University Teaching, Referral and Research Hospital

Academic Advisor: Professor [Advisor Name]

By

Kung'u Kelvin Mathigi

Department of Techno Convergence based on ICT Policy
Handong Global University

A thesis submitted to faculty of Handong Global University in partial fulfillment of the requirements for the degree of Master of Science in the Department of Techno Convergence based on ICT Policy.

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

Healthcare appointment management in many low- and middle-income countries remains constrained by communication bottlenecks, fragmented administrative systems, and uneven digital access. At referral hospitals in Kenya, these constraints frequently manifest as prolonged waiting times, high front-desk pressure, poor visibility into queue conditions, and incomplete patient interaction records. This thesis presents a design science study that develops and evaluates a multilingual AI-driven patient support assistant for appointment booking and congestion-aware slot recommendation.

The developed artifact combines a large language model for conversational understanding with deterministic workflow controls for transaction-critical booking states. Unlike purely generative chatbot systems, the artifact enforces rule-based gating for mandatory patient details, appointment type confirmation, date parsing, and time selection before final booking execution. The architecture integrates prediction-informed queue indicators to recommend lower-congestion appointment windows and improve patient decision quality.

A specific contribution is robust multilingual operation in English and Swahili, with deterministic localization of high-risk outputs such as best-available-slot summaries and booking confirmations. This addresses known failure patterns where language consistency can degrade near transaction completion.

Evaluation is conducted through functional, scenario-based, and reliability testing. Findings demonstrate practical gains in booking flow stability, reduction of malformed transaction attempts, stronger error recovery behavior, and improved end-state clarity for users. The thesis further develops policy and governance guidance for responsible deployment, emphasizing transparency, data minimization, role boundaries, human escalation, and auditability.

The study contributes a transferable architecture and implementation approach for trustworthy, policy-aware healthcare service automation in Kenyan and comparable contexts.

Keywords: design science research, healthcare chatbot, multilingual AI, appointment scheduling, queue optimization, Swahili localization, ICT policy.

---

# ACKNOWLEDGEMENTS

I thank God for grace, strength, and guidance throughout my graduate studies and research journey. I sincerely appreciate my academic advisor for supervision, constructive feedback, and consistent encouragement. I also thank the faculty members of the Graduate School of Global Development and Entrepreneurship for creating an intellectually rigorous environment that strengthened this work.

I am grateful to healthcare professionals and stakeholders whose practical perspectives informed the case context and implementation priorities of this study. My appreciation also extends to colleagues and peers who provided technical discussions and moral support during system development and evaluation.

Finally, I thank my family for their unwavering prayers, patience, and support.

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
Figure 3. Booking state transitions with deterministic guardrails
Figure 4. Tool-call orchestration and synthesis loop
Figure 5. Multilingual localization enforcement pipeline
Figure 6. Congestion-aware slot ranking process
Figure 7. Proposed hospital deployment topology

---

# LIST OF TABLES

Table 1. Research objectives and measurable indicators
Table 2. Literature synthesis themes and gaps
Table 3. Artifact modules and implementation functions
Table 4. Test scenarios and expected outcomes
Table 5. Risk categories and mitigation controls
Table 6. Governance and policy compliance checklist
