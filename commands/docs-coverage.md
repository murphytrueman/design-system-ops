---
description: Audit whether your documentation surface keeps pace with your components
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(git log:*), Bash(git ls-files:*)
---

Run the docs-coverage skill against the user's design system.

Load the docs-coverage skill from ${CLAUDE_PLUGIN_ROOT}/skills/docs-coverage/SKILL.md and follow its complete workflow.

If the user provided a path as an argument, treat it as the components directory or the Storybook build to audit: $ARGUMENTS

If no argument was provided, begin with Step 0 (build the component inventory) — locate the components directory, then look for a Storybook build (`storybook-static/index.json`) and any configured documentation platform.

Before starting, read the knowledge notes declared in the skill's frontmatter `references:` field, located in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/.

Produce the full report including: coverage by rung (exists / described / guided / undocumented), severity-rated findings with a join-confidence tier on each, git-based staleness risks with both change dates shown, orphaned documentation, and a prioritised action list. Never present a low-confidence name match as a fact, and never block the audit on a missing integration.
