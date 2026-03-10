---
description: Generate a migration codemod with tests and rollback plan
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(node:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the codemod-generator skill to produce a migration codemod.

Load the codemod-generator skill from ${CLAUDE_PLUGIN_ROOT}/skills/codemod-generator/SKILL.md and follow its complete workflow.

The user should provide the migration context as an argument: $ARGUMENTS

Before starting, read the reference material specified in the skill's frontmatter from ${CLAUDE_PLUGIN_ROOT}/skills/codemod-generator/references/.

Produce the full codemod package including: jscodeshift transform, test cases, migration runner script, MIGRATION.md, and ROLLBACK.md.
