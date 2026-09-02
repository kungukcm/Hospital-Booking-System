# REFERENCES

Note: The following entries are organized from the provided reference files. Replace each with full APA 7 bibliographic details (authors, year, title, source, DOI/URL where available) from the original documents before final submission.

1. A Framework for Chatbots in Medical Practice. File: A_Framework_for_Chatbots_in_Medical_Pre.pdf
2. A Literature Survey of Recent Advances in Chatbots. File: A_Literature_Survey_of_Recent_Advances_i.pdf
3. AI-Powered Chatbots for Mental Health Support. File: AI_powered_Chatbots_for_Mental_Health_Su.pdf
4. Bibliometric Analysis of Chatbots in Healthcare. File: Bibliometric_Analysis_of_Chatbots_in_Hea.pdf
5. Chatbots and Government Communications. File: Chatbots_and_Government_Communications_i.pdf
6. Chatbots as a New User Interface for Process Automation. File: Chatbots_as_a_new_user_interface_for_pro.pdf
7. Chatbots for Brand Representation in Communication. File: Chatbots_for_Brand_Representation_in_Com.pdf
8. Chatbots in Airport Customer Service Experience. File: Chatbots_in_Airport_Customer_Service_Exp.pdf
9. Developing Chatbots in the Field of Health. File: Developing_chatbots_in_the_field_of_heal.pdf
10. Empathic Response Generation in Chatbots. File: Empathic_Response_Generation_in_Chatbots.pdf
11. Ensuring Consumer Satisfaction with Chatbots. File: Ensuring_Consumer_Satisfaction_with_Chat.pdf
12. EREBOTS Privacy-Compliant Agent-Based Platform. File: EREBOTS_Privacy_Compliant_Agent_Based_Pl.pdf
13. Ethical Considerations in Using Artificial Intelligence. File: Ethical_considerations_in_using_artifici.pdf
14. Exploring the Potential of Chatbots in Mental Health. File: Exploring_the_Potential_of_Chatbots_in_M.pdf
15. Exploring the Potential of Chatbots in Mental Health (alternate copy). File: Exploring_the_Potential_of_Chatbots_in_M (1).pdf
16. Factors Influencing Patient Engagement in Chatbot Use. File: Factors_influencing_patient_engagement_i.pdf
17. LLM-Based Chatbots in Language Learning. File: LLM_Based_Chatbots_in_Language_Learning.pdf
18. Natural Language Chatbots in Biomedical Contexts. File: Natural_Language_Chatbots_in_Biomedical.pdf
19. Proposed Use of Chatbots in Mental Health. File: Proposed_Use_of_Chatbots_in_Mental_Healt.pdf
20. Revolutionizing e-Health Through Chatbots. File: Revolutionizing_e_health_the_transformat.pdf
21. Technical Metrics Used to Evaluate Health Chatbots. File: Technical_Metrics_Used_to_Evaluate_Healt.pdf
22. The Evolving Role of Virtual Health Assistants. File: The_Evolving_Role_of_Virtual_Health_Assi.docx
23. The Health Chatbots in Telemedicine Integration. File: The_Health_ChatBots_in_Telemedicine_Inte.pdf
24. The Role of Chatbots in Enhancing Customer Service. File: The_Role_of_Chatbots_in_Enhancing_Custom.pdf
25. Understanding How Chatbots Work: An Exploratory Study. File: Understanding_How_Chatbots_Work_An_Explo.pdf
26. Understanding the Limitations of AI Chatbots. File: Understanding_the_Limitations_of_AI_Chat.pdf
27. Use of Chatbots for Customer Service. File: Use_of_chatbots_for_customer_service_in.pdf

---

# APPENDIX A. EXTENDED DESIGN SPECIFICATION

The assistant is designed as a stateful conversational system where each user message updates a shared state. The state includes message history and current time context. Decision logic routes execution between conversation synthesis and operational tools.

Deterministic checks are implemented before tool execution to enforce mandatory-field completeness and flow order. These checks reduce the risk of malformed booking transactions and improve user guidance.

---

# APPENDIX B. TEST SCENARIO MATRIX

1. Service-only input after patient details
Expected: prompt for date
2. Date-only input after service
Expected: return ranked slots
3. Time-only input after date and service
Expected: complete booking
4. Missing patient details at booking stage
Expected: block and request missing fields
5. Swahili booking flow completion
Expected: fully localized confirmation block
6. Swahili best slots retrieval
Expected: localized slot heading, labels, and appointment type value

---

# APPENDIX C. GOVERNANCE CHECKLIST

1. Disclosure statement that assistant is non-clinical
2. Data minimization by default
3. Access controls for logs and identifiers
4. Rate-limit and failure handling policy
5. Human escalation pathways
6. Periodic quality and fairness audits

---

# APPENDIX D. PROPOSED PAGE-BY-PAGE EXPANSION BLUEPRINT

To build a complete 200-page final thesis, expand each chapter with the following:

1. Chapter 1 (20 pages): context statistics, expanded policy background, detailed objectives map.
2. Chapter 2 (55 pages): per-reference critical summaries, theme matrix, comparative theory analysis.
3. Chapter 3 (28 pages): instrument details, evaluation rubric definitions, validity threats and controls.
4. Chapter 4 (30 pages): module-by-module code narrative, sequence diagrams, configuration details.
5. Chapter 5 (28 pages): full scenario transcripts, quantitative summary tables, error taxonomy.
6. Chapter 6 (15 pages): policy argumentation, comparative interpretation with literature.
7. Chapter 7 (8 pages): implementation roadmap and strategic recommendations.
8. References + Appendices (16 pages): finalized APA references, supporting logs, templates.

Total target: 200 pages.
