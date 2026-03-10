---
description: Audit your design token architecture
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the token-audit skill against the user's design system tokens.

Load the token-audit skill from ${CLAUDE_PLUGIN_ROOT}/skills/token-audit/SKILL.md and follow its complete workflow.

If the user provided a file or directory path as an argument, use that as the token source: $ARGUMENTS

If no argument was provided, begin with Step 0 (Token discovery) — search the codebase for CSS custom properties, SCSS variables, JSON/YAML token files, Style Dictionary configs, TypeScript token objects, Tailwind configs, and Tokens Studio exports.

Before starting the audit, read the reference material specified in the skill's frontmatter from ${CLAUDE_PLUGIN_ROOT}/skills/token-audit/references/.

Produce the full audit report including: three-tier assessment, naming violations, value-level violations, severity-rated findings, dependency map, and prioritised remediation list.
