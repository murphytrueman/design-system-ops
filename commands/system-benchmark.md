---
description: Compare your design system against named public systems across 12 dimensions in 4 pillars
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the system-benchmark skill against the user's design system.

Load the system-benchmark skill from ${CLAUDE_PLUGIN_ROOT}/skills/system-benchmark/SKILL.md and follow its complete workflow.

If the user provided a file or directory path as an argument, use that as the system root: $ARGUMENTS

If no argument was provided, search the codebase for package.json, component directories, token files, and documentation to identify the system boundaries.

Before starting the benchmark, read the knowledge notes declared in the skill's frontmatter `references:` field, located in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/.

Produce the full benchmark report including: a status for each of the 12 dimensions across 4 pillars, a comparison matrix against named public systems, pillar summaries, and improvement recommendations.
