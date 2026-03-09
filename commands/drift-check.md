---
description: Detect where teams are diverging from the system
allowed-tools: Read, Grep, Glob, Bash(find:*), Bash(diff:*)
---

Run the drift-detection skill to identify where consuming teams are diverging from the design system.

Load the drift-detection skill from ${CLAUDE_PLUGIN_ROOT}/skills/drift-detection/SKILL.md and follow its complete workflow.

Before starting, read the reference material specified in the skill's frontmatter from ${CLAUDE_PLUGIN_ROOT}/skills/drift-detection/references/.

Classify every drift instance into one of five categories: A (intentional divergence), B (version lag), C (accidental drift), D (misunderstanding), E (system gap). Apply severity weighting based on component criticality (Step 4a).

For each classification, provide the recommendation path routing to the appropriate next skill: A→decision-record, B→deprecation-process, C→design-to-code-check, D→change-communication, E→contribution-workflow.

If the user provides specific files or teams to check as an argument, focus on those: $ARGUMENTS
