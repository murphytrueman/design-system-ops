---
description: Benchmark your design system across 12 scored dimensions
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the system-benchmark skill against the user's design system.

Load the system-benchmark skill from ${CLAUDE_PLUGIN_ROOT}/skills/system-benchmark/SKILL.md and follow its complete workflow.

If the user provided a file or directory path as an argument, use that as the system root: $ARGUMENTS

If no argument was provided, search the codebase for package.json, component directories, token files, and documentation to identify the system boundaries.

Before starting the benchmark, read the reference material specified in the skill's frontmatter from ${CLAUDE_PLUGIN_ROOT}/skills/system-benchmark/references/.

Produce the full benchmark report including: 12-dimension scores across 4 pillars, percentile positioning, pillar analysis, and improvement recommendations.
