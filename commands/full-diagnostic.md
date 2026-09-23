---
description: Full health sweep chaining token, naming, component, drift, docs-coverage and system-health audits into one report with cross-skill patterns
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(git log:*), Bash(git ls-files:*), Bash(npx style-dictionary:*), Bash(npm view:*)
---

Run the full system diagnostic — a comprehensive health sweep that chains six audit skills (plus conditional theme and Figma audits) into a unified diagnostic report.

Load the agent instructions from ${CLAUDE_PLUGIN_ROOT}/skills/full-system-diagnostic-agent.md and follow the complete workflow.

Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — load each chained skill and the knowledge notes in its `references:` field only when its step starts, build one inventory up front, and pass short hand-off cards between steps. Skip any step whose tools aren't permitted (for example, Figma) and record the skip in the report's Scope block.

The diagnostic runs in this order:
1. Token audit — token architecture, naming, structural debt
2. Naming audit — convention consistency, ambiguity, intent clarity
3. Component audit — inventory, usage, duplication, coverage gaps
4. Drift detection — where teams diverge and why
5. Docs coverage — documentation that has fallen behind the components (coverage gaps, staleness)
6. System health — status assessment across 7 dimensions, run last so it synthesises everything upstream

Conditional steps run before system-health when they apply: theme audit (if the system supports theming) and Figma variable audit (if Figma is configured and its tools are permitted).

After running the chain, use the synthesis decision tree (Phase 3) to identify cross-skill patterns: concentrated debt, documentation gaps, governance gaps, structural gaps, AI-readiness gaps, platform maturity gaps, or dependency cascades.

Produce a unified diagnostic report that opens with a headline sentence, then: executive summary, per-skill findings table, cross-skill patterns, a ranked action list ordered by impact, one combined Scope block, and a one-line provenance footer.

If the user provides context about their system: $ARGUMENTS
