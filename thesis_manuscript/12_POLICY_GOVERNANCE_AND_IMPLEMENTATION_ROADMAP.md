# CHAPTER 6 SUPPLEMENT. POLICY, GOVERNANCE, AND IMPLEMENTATION ROADMAP

## A. Purpose

This supplement translates research findings into a practical governance and implementation framework for Kenyan hospitals considering AI-assisted appointment systems.

## B. Governance Domains

### B.1 Institutional Accountability

Hospitals should define ownership of AI assistant outcomes across:

1. operations management;
2. IT and cybersecurity;
3. quality assurance;
4. legal/compliance office;
5. patient experience office.

### B.2 Data Governance

Minimum controls should include:

1. data minimization by default;
2. purpose-limited use of identifiers;
3. role-based access to records and logs;
4. retention and deletion policy alignment;
5. encryption of sensitive data in transit and at rest.

### B.3 Clinical Boundary Governance

The assistant must remain non-diagnostic unless formally approved and validated for clinical support. Messaging should always communicate role boundaries clearly.

## C. Risk Taxonomy

1. Transaction risk: incomplete or incorrect booking records.
2. Communication risk: misleading language or inconsistent confirmation.
3. Privacy risk: unauthorized access to patient-identifying fields.
4. Equity risk: reduced usability for specific language groups.
5. Operational risk: downtime or upstream model interruption.

## D. Control Matrix

### D.1 Preventive Controls

1. deterministic mandatory-field validation;
2. strict input parsing rules for date/time;
3. controlled tool schema definitions;
4. language-context enforcement rules.

### D.2 Detective Controls

1. structured log monitoring;
2. failed booking audit dashboard;
3. periodic localization quality review;
4. anomaly detection on repeated retries.

### D.3 Corrective Controls

1. fallback prompts and guided correction;
2. rapid human handoff options;
3. incident triage and root-cause review;
4. patch cycle for recurring failure patterns.

## E. Ethical Implementation Principles

1. Respect for autonomy: users should understand what the assistant does and does not do.
2. Beneficence: prioritize utility in reducing service friction and improving access.
3. Non-maleficence: block unsafe or ambiguous transaction progression.
4. Justice: support multilingual and inclusive access pathways.
5. Accountability: preserve auditable records and transparent governance ownership.

## F. Deployment Maturity Model

### Stage 1: Prototype Validation

Characteristics:

1. controlled environment testing;
2. synthetic or non-sensitive data pathways;
3. technical behavior stabilization.

### Stage 2: Limited Pilot

Characteristics:

1. one department deployment;
2. monitored service hours;
3. human fallback mandatory;
4. weekly incident review.

### Stage 3: Managed Scale

Characteristics:

1. multiple departments;
2. performance dashboards;
3. formal governance committee oversight;
4. quarterly policy compliance audits.

### Stage 4: Institutional Service Integration

Characteristics:

1. integrated appointment operations;
2. standard operating procedures and KPIs;
3. periodic independent evaluation.

## G. KPI Framework for Governance and Service Quality

1. booking completion rate;
2. invalid execution prevention rate;
3. average response-to-confirmation time;
4. language-consistent confirmation rate;
5. escalation response time;
6. incident closure time;
7. patient satisfaction index for administrative interaction.

## H. Stakeholder Implementation Roles

1. Hospital leadership: strategic approval and accountability.
2. ICT teams: platform operation and security controls.
3. Front-desk management: workflow integration and escalation handling.
4. Clinical governance teams: boundary oversight and safety assurance.
5. Data protection officers: compliance monitoring.

## I. Legal and Policy Alignment Checklist

1. informed-use disclosure published and visible;
2. data policy documentation approved;
3. incident management workflow documented;
4. human escalation service-level agreements defined;
5. audit log retention policy enforced;
6. multilingual accessibility standard monitored.

## J. 12-Month Implementation Roadmap

### Quarter 1

1. governance charter finalization;
2. policy checklist completion;
3. baseline operational metrics capture.

### Quarter 2

1. pilot launch in one service line;
2. weekly reliability and localization monitoring;
3. rapid correction cycles.

### Quarter 3

1. pilot expansion to additional units;
2. dashboard-driven performance management;
3. external advisory review.

### Quarter 4

1. institutional adoption decision;
2. documented lessons and policy updates;
3. scale strategy and budget planning.

## K. Summary

Responsible implementation of AI appointment assistants requires as much governance design as technical design. This roadmap provides a practical path from prototype to policy-aligned institutional service.
