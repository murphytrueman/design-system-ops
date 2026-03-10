---
description: Comprehensive design system health sweep
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the full system diagnostic — a comprehensive health sweep that chains five audit skills into a unified diagnostic report.

Load the agent instructions from ${CLAUDE_PLUGIN_ROOT}/skills/full-system-diagnostic-agent.md and follow the complete workflow.

Before starting, read the reference material for each chained skill from their respective ${CLAUDE_PLUGIN_ROOT}/skills/*/references/ directories.

The diagnostic runs in this order:
1. Token audit — token architecture, naming, structural debt
2. Component audit — inventory, usage, duplication, coverage gaps
3. Naming audit — convention consistency, ambiguity, intent clarity
4. Drift detection — where teams diverge and why
5. System health — scored assessment across 7 dimensions

After running all five, use the synthesis decision tree (Phase 3) to identify cross-skill patterns: concentrated debt, documentation gaps, governance gaps, structural gaps, AI-readiness gaps, platform maturity gaps, or dependency cascades.

Produce a unified diagnostic report with: executive summary, per-skill findings table, cross-skill patterns, and a ranked action list ordered by impact.

If the user provides context about their system: $ARGUMENTS
