---
description: Periodic governance package linking adoption to drift causes, with a leadership brief ready for review
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(npm view:*)
---

Run the governance review — a periodic (usually quarterly) assessment that produces an internal review, adoption analysis, drift summary, and stakeholder-ready brief.

Load the agent instructions from ${CLAUDE_PLUGIN_ROOT}/skills/governance-review-agent.md and follow the complete workflow.

Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — load each chained skill — ${CLAUDE_PLUGIN_ROOT}/skills/adoption-report/SKILL.md, ${CLAUDE_PLUGIN_ROOT}/skills/drift-detection/SKILL.md, and ${CLAUDE_PLUGIN_ROOT}/skills/stakeholder-brief/SKILL.md — and the knowledge notes in its `references:` field only when its step starts.

The review produces:
1. Internal assessment — adoption summary, drift summary, cross-skill interpretation, primary blocker, what is working, recommendations
2. At-risk team detail — teams showing declining engagement
3. Stakeholder brief — business-language summary for leadership
4. Suggested follow-up — which other skills to run next

For recurring reviews, compare against the previous period and flag persistent blockers.

If the user provides context about their review period or teams: $ARGUMENTS
