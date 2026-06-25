---
description: Generate a visual dashboard from audit findings
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the visual-report skill to generate visual output from audit data.

Load the visual-report skill from ${CLAUDE_PLUGIN_ROOT}/skills/visual-report/SKILL.md and follow its complete workflow.

The user may provide audit data inline or reference previous skill outputs: $ARGUMENTS

Before starting, read the knowledge notes declared in the skill's frontmatter `references:` field, located in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/.

Produce the visual output: an interactive HTML dashboard with Chart.js charts, metric cards, and text summaries for accessibility.
