---
description: Quarterly governance review package
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the governance review — a quarterly assessment that produces an internal review, adoption analysis, drift summary, and stakeholder-ready brief.

Load the agent instructions from ${CLAUDE_PLUGIN_ROOT}/skills/governance-review-agent.md and follow the complete workflow.

Before starting, read the reference material for the adoption-report and drift-detection skills from their respective ${CLAUDE_PLUGIN_ROOT}/skills/*/references/ directories.

Begin with Step 1b (Adoption measurement calibration) to establish maturity-appropriate adoption expectations.

The review produces:
1. Internal assessment — adoption summary, drift summary, cross-skill interpretation, primary blocker, what is working, recommendations
2. At-risk team detail — teams showing declining engagement
3. Stakeholder brief — business-language summary for leadership
4. Suggested follow-up — which other skills to run next

For recurring reviews, compare against the previous period and flag persistent blockers.

If the user provides context about their review period or teams: $ARGUMENTS
