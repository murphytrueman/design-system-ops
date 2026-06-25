---
description: Generate a CI/CD pipeline for design system quality checks
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the cicd-integration skill to generate a CI/CD pipeline configuration.

Load the cicd-integration skill from ${CLAUDE_PLUGIN_ROOT}/skills/cicd-integration/SKILL.md and follow its complete workflow.

If the user provided a file or directory path as an argument, use that as the system root: $ARGUMENTS

Before starting, read the knowledge notes declared in the skill's frontmatter `references:` field, located in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/.

Produce the full pipeline package including: workflow YAML, helper scripts, quality gates configuration, PIPELINE.md documentation, and phased roadmap.
