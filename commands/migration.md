---
description: Plan a token migration (format, tool, naming or tier) with codemods and a comms plan
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(diff:*), Bash(grep:*), Bash(rg:*), Bash(npx style-dictionary:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(npx tsc:*)
---

Run the migration agent to plan a token migration. It produces a plan and codemods; it doesn't apply them.

Load the migration agent from ${CLAUDE_PLUGIN_ROOT}/skills/migration-agent.md and follow its complete workflow.

The user should describe the migration context: $ARGUMENTS

Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — load each chained skill and the knowledge notes in its `references:` field only when its step starts, and pass short hand-off cards between steps.

The agent chains token-audit, naming-audit, codemod-generator, deprecation-process, and change-communication into a migration plan with a transformation table, codemods, a staged rollout with rollback checkpoints, and a communication package. It stops for your confirmation before the communication phase.
