# CHAPTER 7 SUPPLEMENT. LIMITATIONS, RISK REGISTER, AND FUTURE RESEARCH

## 1. Introduction

This supplement provides a more explicit account of limitations, residual risks, and future research directions. It strengthens the thesis by showing where the current work ends and where further inquiry is needed.

## 2. Limitations of the Current Study

### 2.1 Prototype Context Limitation

The implementation has been validated primarily as a prototype and controlled conversational system. It has not yet been evaluated at full institutional scale with live operational traffic across multiple departments.

### 2.2 Single-Case Orientation

The case context is aligned to a Kenyan referral-hospital environment, but the evaluation does not yet include multiple hospitals or comparative facilities.

### 2.3 Data Availability Limitation

Queue prediction and congestion analysis are constrained by the data available to the prototype. A live deployment would require richer historical and operational data for calibration.

### 2.4 User Diversity Limitation

The study has not yet conducted full-scale usability evaluation across all demographic groups, language preferences, age categories, or digital literacy levels.

### 2.5 Organizational Dependence Limitation

Effectiveness depends on staff adoption, workflow integration, and governance compliance. These are not purely technical variables.

## 3. Risk Register

### 3.1 Technical Risks

#### Risk T1: Tool-call failure under model instability
Impact: booking interruptions or misleading state transitions.
Mitigation: deterministic routing, schema simplification, and fallback prompts.

#### Risk T2: Language drift in high-stakes outputs
Impact: unclear confirmations and user confusion.
Mitigation: deterministic localization layer and regression checks.

#### Risk T3: Queue recommendation miscalibration
Impact: poor slot guidance if prediction data is not representative.
Mitigation: local calibration and periodic recalibration.

### 3.2 Operational Risks

#### Risk O1: Front-desk process resistance
Impact: reduced adoption or workarounds that bypass the system.
Mitigation: early staff engagement and workflow co-design.

#### Risk O2: Escalation overload
Impact: human staff may receive too many unresolved cases.
Mitigation: clearer prompts, improved parsing, and limited rollout scope.

#### Risk O3: Overreliance on the assistant
Impact: users may assume it performs functions beyond its scope.
Mitigation: explicit boundary communication and disclaimers.

### 3.3 Governance Risks

#### Risk G1: Inadequate data governance
Impact: privacy and compliance concerns.
Mitigation: access controls, retention policy, and audit logs.

#### Risk G2: Scope creep into clinical support
Impact: safety and regulatory issues.
Mitigation: role boundaries and governance approval for any expansion.

#### Risk G3: Unclear accountability
Impact: unresolved responsibility for failures.
Mitigation: formal ownership structure and incident review procedure.

## 4. Limitations as Research Opportunities

Each limitation can also be treated as a future research opportunity. The prototype limitation points toward the need for field pilot research that tests in real-world conditions. The single-case orientation suggests multi-site comparative studies would strengthen understanding of transferability. The data availability limitation indicates the value of predictive model calibration research using richer operational datasets. The user diversity limitation reveals the importance of detailed usability and accessibility study. The organizational dependence limitation points toward implementation science research examining how adoption actually occurs.

## 5. Future Research Directions

### 5.1 Multi-Site Field Evaluation

A next-step study should test the assistant in multiple hospital settings to determine transferability across institutional workflows.

### 5.2 Longitudinal Impact Study

A longitudinal design could assess whether the assistant changes appointment completion, no-show rates, and queue distribution over time.

### 5.3 Human Factors and Trust Study

Future work should measure trust, comprehension, and satisfaction using user surveys, interviews, and observational methods.

### 5.4 Fairness and Inclusion Study

Research should examine whether performance differs by language preference, digital literacy, age, or service type.

### 5.5 Interoperability Study

Future versions could explore integration with appointment databases, electronic health records, SMS notifications, and institutional dashboards.

### 5.6 Governance and Policy Study

A policy-focused study could develop sector-specific standards for administrative AI in healthcare, especially around multilingual communication and accountability.

## 6. Recommended Research Questions for Future Work

1. How does a multilingual appointment assistant affect appointment completion in live hospital settings?
2. Does queue-aware recommendation improve low-congestion slot uptake?
3. What factors shape patient trust in administrative AI assistants?
4. Which governance models best support safe scaling across hospitals?
5. How do language and digital literacy affect assistant effectiveness?

## 7. Suggested Future Methods

1. quasi-experimental deployment study;
2. mixed-method usability evaluation;
3. conversation-log analysis;
4. policy implementation study;
5. multi-stakeholder design workshops.

## 8. Residual Uncertainty Statement

Despite the positive technical results, several uncertainties remain:

1. live workload variability may change system behavior;
2. institutional policy differences may affect adoption;
3. localized language expectations may evolve over time;
4. model-service dependencies may shift with upstream vendor changes.

## 9. Final Implication

The present thesis establishes a robust foundation, but responsible progression requires continued empirical validation. The most valuable next step is a controlled field pilot with strong governance support.
