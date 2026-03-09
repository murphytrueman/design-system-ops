---
description: Pre-release validation pipeline for a component
allowed-tools: Read, Write, Grep, Glob, Bash(find:*), Bash(wc:*)
---

Run the component-to-release pipeline to validate a component is ready to ship.

This command chains multiple skills into a single pre-release workflow. Load the agent instructions from ${CLAUDE_PLUGIN_ROOT}/skills/component-to-release-agent.md and follow the complete pipeline.

Before starting, read the reference material for each chained skill from their respective ${CLAUDE_PLUGIN_ROOT}/skills/*/references/ directories.

Begin with Phase 0 (Component type decision) — classify whether this is a new component, enhancement, breaking change, or bug fix, then adjust the pipeline depth accordingly.

The pipeline runs in order:
1. Design-to-code check (visual alignment, interactive states, responsive behaviour)
2. Accessibility audit (keyboard, screen reader, contrast, focus, ARIA)
3. Token compliance (hardcoded values, wrong-tier references, DTCG alignment)
4. AI component description (six-section format + JSON metadata)
5. Usage guidelines (anti-patterns, edge cases, content guidelines)
6. Change communication (release notes, migration guide if breaking)

Produce a release package with all documentation, a sign-off checklist, and gate decisions (critical findings block release).

The component to validate: $ARGUMENTS
