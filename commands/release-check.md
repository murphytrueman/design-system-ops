---
description: Pre-release gates (design-to-code, accessibility, token compliance) and docs for one component, producing a release package for sign-off
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(git log:*), Bash(git blame:*), Bash(rg:*)
---

Run the component-to-release pipeline to validate a component is ready to ship.

This command chains multiple skills into a single pre-release workflow. Load the agent instructions from ${CLAUDE_PLUGIN_ROOT}/skills/component-to-release-agent.md and follow the complete pipeline.

Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — load each chained skill and the knowledge notes in its `references:` field only when its step starts, and pass short hand-off cards between steps. Skip any step whose tools aren't permitted (for example, Figma) and record the skip in the package's Scope block.

Begin with Phase 0 (Component type decision) — classify the change as New component, Enhancement, Breaking change, or Bug fix, then adjust the pipeline depth accordingly.

The pipeline runs in order:
1. Design-to-code check (visual alignment, interactive states, responsive behaviour)
2. Accessibility audit (keyboard, screen reader, contrast, focus, ARIA)
3. Token compliance (hardcoded values, wrong-tier references, DTCG alignment)
   - Breaking changes only: blast radius (version-bump-advisor plus a search of consuming repositories)
4. AI component description (six-section prose; the skill's write-back to Figma is skipped and goes on the sign-off checklist)
5. Usage guidelines (anti-patterns, edge cases, content guidelines)
6. Change communication (release notes, migration guide if breaking)

Produce a release package with all documentation, a sign-off checklist, and gate decisions (critical findings block release). Nothing is published or written to Figma.

The component to validate: $ARGUMENTS
