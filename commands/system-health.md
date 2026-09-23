---
description: Quick single-pass status check across 7 dimensions, with maturity stage (no sub-audits run)
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the system-health skill for a quick single-pass status check of the user's design system across 7 dimensions. It doesn't run the sub-audits; for that, use /full-diagnostic.

Load the system-health skill from ${CLAUDE_PLUGIN_ROOT}/skills/system-health/SKILL.md and follow its complete workflow.

Before starting, read the knowledge notes declared in the skill's frontmatter `references:` field, located in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/.

Assess all 7 dimensions (Tokens, Components, Documentation, Adoption, Governance, AI readiness, Platform maturity) with expectations calibrated to the library type, then infer the maturity stage from the evidence (Step 1b) rather than asking the user for it.

Produce the full health report including: dimension status (Strong / Functional / Weak / Absent) for each of the 7 dimensions, maturity stage, findings per dimension, and a prioritised action list.

If the user provides context about their system as an argument, use it: $ARGUMENTS
