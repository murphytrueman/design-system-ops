---
description: Comprehensive design system health sweep
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the full system diagnostic — a comprehensive health sweep that chains six audit skills (plus conditional theme and Figma audits) into a unified diagnostic report.

Load the agent instructions from ${CLAUDE_PLUGIN_ROOT}/skills/full-system-diagnostic-agent.md and follow the complete workflow.

Before starting, read the reference material for each chained skill from the `references:` field of each skill's frontmatter, located in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/.

The diagnostic runs in this order:
1. Token audit — token architecture, naming, structural debt
2. Naming audit — convention consistency, ambiguity, intent clarity
3. Component audit — inventory, usage, duplication, coverage gaps
4. Drift detection — where teams diverge and why
5. Docs coverage — documentation that has fallen behind the components (coverage gaps, staleness)
6. System health — scored assessment across 7 dimensions, run last so it synthesises everything upstream

Conditional steps run before system-health when they apply: theme audit (if the system supports theming) and Figma variable audit (if Figma is configured).

After running the chain, use the synthesis decision tree (Phase 3) to identify cross-skill patterns: concentrated debt, documentation gaps, governance gaps, structural gaps, AI-readiness gaps, platform maturity gaps, or dependency cascades.

Produce a unified diagnostic report with: executive summary, per-skill findings table, cross-skill patterns, and a ranked action list ordered by impact.

If the user provides context about their system: $ARGUMENTS
