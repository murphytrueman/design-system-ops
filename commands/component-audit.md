---
description: Audit your component library inventory
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the component-audit skill against the user's design system component library.

Load the component-audit skill from ${CLAUDE_PLUGIN_ROOT}/skills/component-audit/SKILL.md and follow its complete workflow.

If the user provided a file or directory path as an argument, use that as the component source: $ARGUMENTS

Before starting the audit, read the reference material specified in the skill's frontmatter from ${CLAUDE_PLUGIN_ROOT}/skills/component-audit/references/.

Begin with Step 1b (Define usage signals) to establish which metrics the user wants to track. Then produce the full inventory including: component catalogue, usage signal assessment, complexity distribution, duplication analysis with dependency graphs, coverage gap analysis, AI-readiness scoring, and maturity level assessment.
