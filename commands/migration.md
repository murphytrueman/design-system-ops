---
description: Plan and execute a design system migration
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(diff:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the migration agent to plan and execute a design system migration.

Load the migration agent from ${CLAUDE_PLUGIN_ROOT}/skills/migration-agent.md and follow its complete workflow.

The user should describe the migration context: $ARGUMENTS

The agent chains multiple skills (token-audit, codemod-generator, deprecation-process, change-communication) into a coordinated migration plan with impact analysis, codemods, communication packages, and rollback strategy.
