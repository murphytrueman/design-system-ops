---
description: Plan a token migration (format, tool, naming or tier) with codemods, deprecation and a comms plan
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(diff:*), Bash(grep:*), Bash(rg:*), Bash(npx style-dictionary:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(npx tsc:*), Bash(node:*), Bash(npx jscodeshift:*), Bash(npx jest:*), Bash(npx vitest:*)
---

Run the token-migration agent to plan a token migration. It produces a plan, codemods and a deprecation schedule; it doesn't apply them.

Load the agent from ${CLAUDE_PLUGIN_ROOT}/skills/token-migration-agent.md and follow its complete workflow.

The user should describe the migration context: $ARGUMENTS

Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — load each chained skill and the knowledge notes in its `references:` field only when its step starts, and pass short hand-off cards between steps.

The agent chains token-audit, codemod-generator, deprecation-process and change-communication into one migration plan: a transformation table, codemods, a three-stage rollout (ship new names with the old ones aliased and deprecated, consumers migrate, remove in the next major) and a communication package. It stops for your confirmation before the communication phase.
