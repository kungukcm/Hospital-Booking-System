# CHAPTER 7 SUPPLEMENT B. IMPLEMENTATION-READY RECOMMENDATIONS

## 1. Introduction

This supplement turns the conclusion chapter into practical recommendations that a hospital, project team, or policy unit could use as a starting point for deployment planning.

## 2. Recommendation 1: Start with One Administrative Use Case

Do not launch the assistant with too many tasks at once. Start with appointment booking and slot guidance for one department. This reduces complexity and makes validation easier.

## 3. Recommendation 2: Keep Human Escalation Visible

The assistant should never be the only path available. Users must be able to reach a human staff member when the assistant cannot safely complete the task.

## 4. Recommendation 3: Preserve the Deterministic Core

The rules that validate patient details, service type, date, and time should remain stable even as other features expand. This deterministic core is what protects reliability.

## 5. Recommendation 4: Treat Swahili Support as a Core Feature

Swahili should not be added as a decorative extra. It should be a standard service channel, with full transactional consistency in confirmation blocks and slot recommendations.

## 6. Recommendation 5: Measure Outcomes from Day One

Collect operational metrics from the start of deployment. These should include the booking completion rate to measure whether the assistant is achieving its primary goal, time to confirmation to understand user experience and system responsiveness, escalation frequency to see how often human staff must take over, localization match rate to verify that language consistency is being maintained, and conflict warning rate to track how often potential issues are detected. Without measurement, improvement cannot be demonstrated and early problems may go unnoticed.

## 7. Recommendation 6: Review Failures Systematically

Every failed or partially failed interaction should be logged, categorized, and reviewed. Common failures should inform immediate patches or prompt revisions.

## 8. Recommendation 7: Train Staff Before Expansion

Front-desk staff, supervisors, and support teams should understand what the assistant does and what it does not do so they know when to trust it and when not to. They should know how to take over from the assistant when escalation is needed, how to report issues when something appears broken, and how to interpret logs or reports when questions arise about specific interactions. Training should happen before the assistant is released to real patient use.

## 9. Recommendation 8: Update References and Policies Together

If the institution updates the assistant, it should also update the supporting policy documents and training materials. Technical change without governance change will create inconsistency.

## 10. Recommendation 9: Use Pilot Feedback to Refine Language

User feedback should be used to improve prompt wording, clarification steps, and translated terminology. This is especially important for local language nuances.

## 11. Recommendation 10: Expand Only After Thresholds Are Met

Do not scale until core thresholds are achieved consistently. Expansion before stabilization is a common cause of breakdown in digital service projects.

## 12. Conclusion

These recommendations are intentionally practical. They are designed to help a real implementation team move from thesis artifact to controlled institutional pilot without losing the reliability and governance discipline that the thesis establishes.
