---
name: context-engine-builder
description: "Generate context-engine blueprint YAML in .ai/context-engine/ (UX, UI, content, a11y, ethical, technical, business) that agents load. Triggers: build a context engine, seven blueprints. Component inventory/dependency graph: codebase-index. Health assessment: system-health."
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
  - ../../knowledge-notes/agent-orchestration-guide.md
  - ../../knowledge-notes/mcp-setup-guide.md
  - ../../knowledge-notes/context-engine-blueprints.md
  - ../../knowledge-notes/output-discipline.md
---

# Context engine builder

A skill for generating a context engine — a structured, multi-layered knowledge base that gives AI agents the complete picture of a design system. The engine encodes seven dimensions of system knowledge (UX, UI, content, accessibility, ethical, technical, and business intelligence) as machine-readable blueprints that agents load, reason over, and apply without requiring implicit knowledge or human interpretation.

## Before you begin: verify references

Before doing anything else, confirm that every file listed in this skill's frontmatter `references:` field exists at its relative path from this SKILL.md. If any are missing, stop — the install is incomplete. This usually means a third-party installer (for example `npx skills install`) flattened the skill into a standalone folder and dropped the repo-root `knowledge-notes/` directory this skill depends on. Tell the user to reinstall using a supported method from `1-INSTALL.md` (git clone, or the `.plugin` bundle in Cowork) and to run `verify-install.sh` from the install root to confirm the fix. Only proceed without the references if the user explicitly says to — and if they do, state clearly in your output that it was produced in degraded mode without the pack's reference material.

## Context

A design system encodes decisions about UX patterns, visual language, content voice, accessibility, ethical guardrails, technical constraints and business rules. Those decisions live in Figma, code, wikis, Slack threads and people's heads, and most of them are invisible to AI agents. An agent that only sees props and token values produces output that is technically valid but contextually wrong: the right components in a login form that ignores the system's authentication pattern.

A context engine front-loads that knowledge as structured files, one per blueprint, that agents, MCP servers and developer tooling load at the start of a task. The seven blueprints match the seven kinds of missing context that cause the most common classes of AI-generated error.

## Boundaries

This skill builds context infrastructure. It does not assess system health (`system-health`), build the component inventory and dependency graph (`codebase-index`), or generate per-component JSON metadata (`metadata-schema-generator`). If the system has no documented components, tokens, or patterns yet, the engine has nothing to encode; help the team establish foundations first. The engine is modular: partial generation is a feature, not a gap.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `system.framework` — pre-selects framework for technical blueprint generation
- `system.component_paths` — directs blueprint scanning to correct directories
- `system.tokens` — identifies token files for UI blueprint extraction
- `integrations.*` — blueprint data sources (see below)
- `context_engine.blueprints` — which blueprints to generate (default: Technical and UI; ask before generating the rest)
- `context_engine.output_format` — `yaml` (default, `.yml` files) or `json` (same structure, `.json` files)

## Auto-pull integrations

**Figma MCP** (`integrations.figma.enabled: true`):
- Read the published library from `integrations.figma.file_key`
- Extract component descriptions, variant structures, and layer hierarchies for the UX and UI blueprints
- Pull design token definitions (colour, spacing, typography) for the UI blueprint
- Extract accessibility annotations if present for the accessibility blueprint

**Storybook** (`integrations.storybook.enabled: true`):
- Fetch the story index and component metadata
- Extract documented states, interactions, and composition patterns for the UX blueprint
- Pull accessibility addon results for the accessibility blueprint

**GitHub** (`integrations.github.enabled: true`):
- Scan component source files for prop types, default values, and TypeScript interfaces for the technical blueprint
- Pull PR templates and contribution guidelines for governance context
- Check for existing documentation files that inform blueprint content

**Existing `.ai/` infrastructure:** if `.ai/index/` (from `codebase-index`) or `.ai/metadata/` (from `metadata-schema-generator`) exists, load it and link to it from the blueprints rather than regenerating the same data.

---

## Provenance rule

Every rule in every blueprint carries a `source:`: a file path, a URL, or `user`. A rule you can't trace gets `status: proposed`, or is left out. If a whole blueprint would be mostly proposed (common for content, ethical and business intelligence, which are policy rather than code), don't pad it with generic good practice: skip it and list it under "Not inspected" in the Scope block, or generate it only with the user's sign-off that it is a proposal. Agents treat these files as the system's actual policy. See "Every figure and fact needs a source" in the output-discipline knowledge note.

---

## Step 1: Assess current context coverage

Before building blueprints, understand what context already exists. Scan for:

- **Existing documentation**: Component docs, pattern libraries, design principles pages, content guidelines, accessibility policies
- **Structured metadata**: `.ai/index/`, `.ai/metadata/`, token files, manifest files
- **Implicit context**: README files, contribution guides, code comments, Storybook stories that encode knowledge informally

Produce a brief context coverage assessment:

| Blueprint | Existing sources found | Coverage | Primary gaps |
|---|---|---|---|
| UX | [list] | [none/partial/good] | [what's missing] |
| UI | [list] | [none/partial/good] | [what's missing] |
| Content | [list] | [none/partial/good] | [what's missing] |
| Accessibility | [list] | [none/partial/good] | [what's missing] |
| Ethical | [list] | [none/partial/good] | [what's missing] |
| Technical | [list] | [none/partial/good] | [what's missing] |
| Business intelligence | [list] | [none/partial/good] | [what's missing] |

Ask for or confirm (skip questions already answered by config or auto-pull):
- Which blueprints to generate. Default to Technical and UI, which can be built from code; ask before the other five, and show which have source material in the table above
- Are there existing documents that should be treated as source material for specific blueprints?
- Are there team members who hold institutional knowledge for specific dimensions that should be captured?

---

The structures for Steps 2–8 are in the context-engine-blueprints knowledge note; each step below names the template and what to take from where.

## Step 2: Generate the UX blueprint

Behavioural rules: for each documented pattern, its trigger, states and transitions, completion criteria, errors and edge cases; plus selection rules ("if the user needs [intent], use [pattern] because [reason]") and multi-step flows (authentication, data entry, navigation, feedback). Take patterns from pattern docs, Storybook and code; if `component-decision-tree` output exists in `.ai/decision-trees/`, link to it for selection rules.

Follow the **UX blueprint template** in the context-engine-blueprints knowledge note.

---

## Step 3: Generate the UI blueprint

The visual system as a specification: the token hierarchy with semantic intent (primitive → semantic → component), layout (grid, breakpoints, spacing rules, container widths), and visual rules (elevation, radius, colour and typography application). Take values from the token files; take usage rules from token descriptions or docs.

Follow the **UI blueprint template** in the context-engine-blueprints knowledge note.

---

## Step 4: Generate the content blueprint

Voice attributes, vocabulary (preferred and prohibited terms), tone per context, content patterns (button labels, error messages, empty states, placeholders, confirmations) and a terminology glossary. Every rule comes from the team's content guidelines or style guide, or from the user, and carries its `source:`. Don't fill this blueprint with generic UX writing advice: if there is no content guidance to encode, skip it and say so.

Follow the **Content blueprint template** in the context-engine-blueprints knowledge note.

---

## Step 5: Generate the accessibility blueprint

Per-component contracts (role, required ARIA, keyboard, focus management, announcements, touch target) and system rules (focus visible, skip links, heading hierarchy, contrast, motion, dark mode), plus testing protocols (automated rules, manual checks, AT support matrix). Take contracts from component source or `.ai/metadata/` accessibility blocks; mark anything unconfirmed `status: proposed`. The baseline is WCAG 2.2 AA. Some legal baselines (e.g. EN 301 549) still reference WCAG 2.1 AA; use that if it's the team's obligation.

Follow the **Accessibility blueprint template** in the context-engine-blueprints knowledge note.

---

## Step 6: Generate the ethical blueprint

Concrete guardrails the system enforces: dark pattern prohibitions (manipulative urgency, forced continuity, confirmshaming, hidden costs, misdirection), inclusive design rules (name and identity inputs, language, representation), data and privacy patterns (consent, PII display, notification frequency, user control) and bias signals. The categories are illustrative; the rules must be the team's own, each with a `source:` (policy doc, docs page, or `user`). A generic list of good intentions presented as the system's policy is worse than no blueprint.

Follow the **Ethical blueprint template** in the context-engine-blueprints knowledge note.

---

## Step 7: Generate the technical blueprint

Component API contracts, composition rules, performance constraints (bundle budgets, SSR, lazy loading) and integration patterns (imports, theme overrides, semver contract). When `.ai/metadata/` or `.ai/index/` exists, reference those files for props, composition and the dependency graph instead of copying them in; this blueprint then adds only what they don't hold (performance, integration, versioning). Otherwise extract from source, and suggest `metadata-schema-generator` and `codebase-index` for the fuller versions.

Follow the **Technical blueprint template** in the context-engine-blueprints knowledge note.

---

## Step 8: Generate the business intelligence blueprint

Component-to-outcome mapping, metric associations (primary, secondary, anti-metrics), experimentation rules and analytics hooks. Only the user or the team's docs and analytics code can supply these, so every entry needs a `source:`; never infer a component's business function or metrics from its name. If `.ai/metadata/` files carry `business_context`, link to them rather than duplicating. With no sourced input, skip this blueprint and list it under Scope.

Follow the **Business intelligence blueprint template** in the context-engine-blueprints knowledge note.

---

## Step 9: Assemble and output the context engine

### File structure

Generate the context engine as a set of files in `.ai/context-engine/` (only the blueprints actually generated):

```
.ai/
  context-engine/
    ux-blueprint.yml
    ui-blueprint.yml
    content-blueprint.yml
    accessibility-blueprint.yml
    ethical-blueprint.yml
    technical-blueprint.yml
    business-intelligence-blueprint.yml
    engine-manifest.yml
    usage-guide.md
```

### Engine manifest

The manifest ties the blueprints together and provides metadata for tooling. Follow the **Engine manifest template** in the context-engine-blueprints knowledge note. It lists each blueprint with its file path and a coverage fact count ("12 of 40 components have a11y contracts"), plus the blueprints skipped and why. No total across blueprints: the counts measure different things.

### Usage guide

Generate a `usage-guide.md` that teaches AI agents how to consume the engine. Follow the **Usage guide template** in the context-engine-blueprints knowledge note. The guide covers engine loading, task-based blueprint selection, query patterns for each blueprint dimension, and that `status: proposed` rules are suggestions, not system policy.

---

## Step 10: Summarise in chat

End with a short chat summary:
- **Headline:** which blueprints were generated and which were skipped
- **Files written:** paths under `.ai/context-engine/`, and any `.ai/index/` or `.ai/metadata/` files linked rather than regenerated
- **Proposed:** a count of `status: proposed` rules per blueprint, with the ones the team should confirm first
- **Scope:** the block from the output-discipline knowledge note, with skipped blueprints under "Not inspected"

---

## Recommend to the user

- Commit the context engine files alongside the codebase
- Re-generate blueprints after significant system changes (new patterns, token restructuring, accessibility policy updates)
- Start with the blueprints that address the team's most common AI-generated errors
- Reference the usage guide in any AI agent system prompt that interacts with the design system
- Treat the context engine as living documentation — update it as the system evolves

---

## Quality checks

- Every blueprint addresses its specific dimension — no overlap or duplication between blueprints
- YAML output is valid and parseable by standard YAML parsers
- Component contracts in the accessibility and technical blueprints reference the same component names used in the codebase
- Content blueprint voice and tone rules are specific to this system, not generic writing advice
- Ethical blueprint prohibitions cite specific patterns, not abstract principles
- Business intelligence blueprint connects to measurable outcomes, not aspirational goals
- The usage guide provides task-specific blueprint loading recommendations, not a generic "load everything" instruction
- Coverage counts in the manifest are counted from the generated files — not estimated, not aspirational
- Every rule has a `source:` or `status: proposed`; no blueprint is padded with generic advice
