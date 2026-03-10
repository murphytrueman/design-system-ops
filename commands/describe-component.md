---
description: Generate an AI-optimised component description
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the ai-component-description skill to generate a structured, machine-readable description for a design system component.

Load the ai-component-description skill from ${CLAUDE_PLUGIN_ROOT}/skills/ai-component-description/SKILL.md and follow its complete workflow.

Before starting, read the reference material specified in the skill's frontmatter from ${CLAUDE_PLUGIN_ROOT}/skills/ai-component-description/references/.

Produce a six-section description:
1. Purpose — what the component does and when to use it
2. Props — every prop with type, default, and guidance
3. Anti-patterns — what NOT to do (use the inference guide for new components)
4. Composition rules — how it works with other components
5. Accessibility — keyboard, screen reader, ARIA, focus
6. Usage examples — concrete code showing correct usage

Also generate the structured JSON metadata for machine-readable manifests.

Run the self-test: could an AI agent select this component correctly, configure it, and avoid misuse based solely on this description?

The component to describe: $ARGUMENTS
