---
description: Write a six-section AI-optimised prose description of one component for Figma MCP and LLMs
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
---

Run the ai-component-description skill to write a six-section, AI-optimised prose description for a design system component.

Load the ai-component-description skill from ${CLAUDE_PLUGIN_ROOT}/skills/ai-component-description/SKILL.md and follow its complete workflow.

Before starting, read the knowledge notes declared in the skill's frontmatter `references:` field, located in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/.

Produce a six-section description:
1. Purpose — what the component does and when to use it
2. Props — every prop with type, default, and guidance
3. Anti-patterns — what NOT to do (use the inference guide for new components)
4. Composition rules — how it works with other components
5. Accessibility — keyboard, screen reader, ARIA, focus
6. Usage examples — concrete code showing correct usage

This command produces prose only. For JSON metadata, use the metadata-schema-generator skill.

Run the self-test: could an AI agent select this component correctly, configure it, and avoid misuse based solely on this description?

The component to describe: $ARGUMENTS
