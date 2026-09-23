---
name: ai-component-description
description: "Write a six-section prose description (purpose, props, anti-patterns, composition, accessibility, examples) for a Figma component's description field so LLMs read it via MCP. Triggers: describe this component for AI, Figma MCP description. JSON metadata files: use metadata-schema-generator."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*)
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
  - ../../knowledge-notes/mcp-setup-guide.md
  - ../../knowledge-notes/output-discipline.md
---

# AI component description

A skill for generating structured component descriptions optimised for consumption by LLMs via Figma's MCP server. Output is a six-section description that gives an AI agent the information it needs to understand, compose, and generate from a component accurately — without relying on implicit knowledge, visual inference, or team context.

## Before you begin: verify references

Before doing anything else, confirm that every file listed in this skill's frontmatter `references:` field exists at its relative path from this SKILL.md. If any are missing, stop — the install is incomplete. This usually means a third-party installer (for example `npx skills install`) flattened the skill into a standalone folder and dropped the repo-root `knowledge-notes/` directory this skill depends on. Tell the user to reinstall using a supported method from `1-INSTALL.md` (git clone, or the `.plugin` bundle in Cowork) and to run `verify-install.sh` from the install root to confirm the fix. Only proceed without the references if the user explicitly says to — and if they do, state clearly in your output that it was produced in degraded mode without the pack's reference material.

## Context

Most component descriptions are written for human designers discovering the component for the first time: "use this to show important information", "works great in cards". An LLM reading a description needs to know what the component is, what it takes, what it prohibits, how it relates to other components, and what failure modes look like. Human-readable descriptions skip most of this.

The six-section format came from watching AI agents misuse components that had perfectly fine human documentation. Each section addresses a specific class of LLM error.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `integrations.figma`, `integrations.storybook`, `integrations.github` and `integrations.documentation` — which sources Step 0 can read automatically

## Step 0: Check data sources and existing description

Use every source that is available:

1. **Figma** (MCP connected, or `integrations.figma` with a `file_key`): the component node, its variants, layer structure (for composition) and existing description. The official Figma MCP reads the current selection, so if it returns nothing, ask the user to select the component.
2. **Storybook** (`integrations.storybook`): prop types, defaults and arg types from the story metadata.
3. **Source** (repo access or `integrations.github`): prop definitions from TypeScript interfaces or PropTypes, the rendered element, ARIA attributes, key handlers and focus calls. Where Figma, Storybook and source disagree on the API, say so rather than picking one silently.
4. **None of the above:** ask the user. The description can still be written, under the provenance rule below.

If a source is configured but fails (connection error, invalid node, nothing selected), note the error and carry on with what you have. Do not retry in a loop.

**Provenance rule.** Every prop, default, ARIA role, key binding and focus behaviour in the description comes from source, Storybook, Figma or the user. Anything you can't trace is left out or marked "unverified" in the text, the same way inferred anti-patterns are marked "anticipated" (Section 3). Never fill the Props or Accessibility sections from what components of this kind usually do. See "Every figure and fact needs a source" in the output-discipline knowledge note.

**Existing description.** If the description field has content (anything other than null, an empty string or whitespace), quote it to the user before doing anything else: "This component already has a description: [text]. Want me to rewrite it in the six-section format, improve what's there, or start fresh?" If it already follows the six-section format, offer a completeness review instead. Never claim there is no description when there is one, and never silently discard it. Treat it as a starting point, not a source of truth: it often holds institutional knowledge worth keeping, but being there doesn't make it accurate.

---

## Step 1: Gather component information

Confirm the following from the Step 0 sources, and ask the user only for what they didn't supply:

- Component name
- Component category (e.g. navigation, feedback, form, layout, data display)
- Available props/variants and their accepted values
- Default state
- Any composition relationships (what it contains, what it can be placed inside)
- Accessibility requirements already defined for the component
- Known misuse patterns observed in production (if any)

## Step 2: Write the six-section description

Write each section in plain prose. No bullet markers or nested lists inside the description itself: AI agents parse prose better than nested lists in this context, and Figma's plain-text field doesn't render them. Where a section holds parallel items (props, anti-patterns), put each on its own line. Each section should be dense but not padded.

---

### Section 1: Purpose

One to two sentences. What does this component do, and when should it be used? Write this as a contract statement, not a marketing line.

Bad: "A flexible card component for displaying content in a visually appealing way."
Good: "A surface container for grouping related content that belongs together but does not require its own page. Use when content needs visual separation from surrounding context without implying navigational hierarchy."

### Section 2: Props

Document every configurable prop. For each:
- Prop name (exact, as it appears in the component API)
- Accepted values (enumerated where finite, typed where variable)
- Default value
- One-sentence description of what the prop controls

Format: `prop-name; type; default; description`, one prop per line. Separate fields with semicolons, because union types already use `|`. Write "no default" when the source declares none, and "required" for required props.

Do not skip props because they seem obvious. LLMs cannot infer defaults, and neither can you: take each type and default from source, Storybook or Figma (Step 0), and mark any the user supplied without a source as "unverified".

Example (illustrative Button):
```
variant; "primary" | "secondary" | "ghost" | "destructive"; "primary"; Controls visual weight and colour treatment
size; "sm" | "md" | "lg"; "md"; Adjusts padding, font size, and min-touch-target
disabled; boolean; false; Prevents interaction and applies reduced-opacity treatment
loading; boolean; false; Replaces label with loading indicator and prevents further clicks
```

### Section 3: Anti-patterns

What should an AI agent NOT do with this component? List the three to five most common misuse patterns, each as a one-sentence prohibition with a brief reason.

These anti-patterns should be specific to this component, not generic design system guidance. Write them based on actual misuse patterns if known, or inferred from the component's structure and common analogues.

Example (illustrative Button, one prohibition per line):
```
Do not use the destructive variant for actions that are reversible. Destructive implies permanent data loss or deletion.
Do not use ghost variant as the primary action in a flow. Ghost is for secondary or tertiary actions that should not compete with a primary.
Do not place more than one primary variant button in the same visual context.
Do not use size lg in dense form layouts. It creates disproportionate vertical rhythm. (anticipated)
```

#### Anti-pattern inference guide

If observed misuse patterns are not available from production data, infer likely anti-patterns from the component's API structure:

- **Components with a `variant` prop that includes "destructive" or "danger":** Likely misuse — using the destructive variant for reversible actions, or using it as a visual emphasis tool rather than a semantic signal.
- **Components with a `size` prop:** Likely misuse — using large sizes in dense layouts, or mixing sizes inconsistently within the same context.
- **Components with a boolean `disabled` prop:** Likely misuse — using disabled state to hide functionality rather than communicating why it is unavailable (missing `aria-disabled` with explanation).
- **Container components (Card, Modal, Drawer):** Likely misuse — nesting containers inside other containers without semantic justification, or using a container for visual grouping when a simpler layout element would suffice.
- **Components with an `icon` or `iconOnly` prop:** Likely misuse — using icon-only variants without providing an accessible label, or choosing icons based on aesthetics rather than meaning.
- **Components with `onClick` or action props:** Likely misuse — using a button-like component for navigation (should be a link), or attaching actions to non-interactive elements.

Use these inferences as starting points. Mark inferred anti-patterns as "anticipated" in the description — they should be validated against real usage and upgraded to "observed" once confirmed.

### Section 4: Composition rules

How does this component relate to others? Document:
- What this component can contain (if it is a container)
- What this component can be placed inside
- What other components are typically used alongside it
- Any hard constraints on nesting or ordering

Be specific. "Can be used in cards" is not useful. "Can be placed inside Card as an action — always as the last child of Card.Footer, never inside Card.Body" is useful.

### Section 5: Accessibility

Document the accessibility contract for this component:
- ARIA role(s) applied
- Keyboard interaction pattern (Tab, Enter, Space, Arrow keys, Escape — state which apply)
- Focus management behaviour (where does focus go on open/close/activate)
- Required aria attributes and their expected values
- Screen reader announcement pattern

This is not a WCAG checklist. It is the specific accessibility behaviour of this specific component, so take it from what the source actually renders and handles (element, ARIA attributes, key handlers, focus calls) or from the user. Anything you expect but can't confirm is marked "unverified", as anti-patterns are marked "anticipated". An unverified keyboard contract is still useful to the team; one stated as fact is how an agent ships a broken component.

**Why this section requires extra rigour.** Accessibility is where AI-generated components fail most often. LLMs understand accessibility theory but routinely produce code that fails basic testing — missing keyboard handlers, incomplete ARIA attributes, focus management that traps or loses focus. The description must be prescriptive enough that an AI agent generating from it produces accessible output without additional guidance.

Specific requirements:
- Specify semantic HTML elements, not just ARIA roles. If the component should render as a `<button>`, say so — an LLM may default to a `<div>` with role="button" which loses native keyboard behaviour.
- For interactive components: document both `disabled` attribute and `aria-disabled` behaviour, and state which one the component uses and why.
- For icon-only actions: require `aria-label` with a description of the action, not the icon name.
- For focus indicators: specify that focus must be visually apparent (not just functionally present). Custom focus styles must meet 3:1 contrast ratio against adjacent colours.

### Section 6: Usage examples

Two to three examples of correct usage. Each gives the intent and the configuration. For interactive components, at least one example also gives the expected DOM output, which hands an AI agent a validation target rather than just a generation prompt. For non-interactive components the DOM output is optional.

**Example format:**

```
Intent: [What the user is trying to accomplish]
Configuration: [Exact props/values needed]
Expected DOM output (interactive components):
  [The rendered HTML structure an AI agent should produce and can validate against]
```

**Example (illustrative Button):**

```
Intent: Confirm action in a destructive confirmation dialog.
Configuration: variant="destructive", size="md", label="Delete account"
Expected DOM output:
  <button
    type="button"
    class="btn btn-destructive btn-md"
  >
    Delete account
  </button>
```

```
Intent: Secondary cancel action paired with the primary action above.
Configuration: variant="secondary", size="md", label="Cancel"
Expected DOM output:
  <button
    type="button"
    class="btn btn-secondary btn-md"
  >
    Cancel
  </button>
```

```
Intent: Icon-only close button in a modal header.
Configuration: variant="ghost", size="sm", iconOnly=true, icon="close", ariaLabel="Close dialog"
Expected DOM output:
  <button
    type="button"
    class="btn btn-ghost btn-sm btn-icon"
    aria-label="Close dialog"
  >
    <svg aria-hidden="true" class="icon icon-close">...</svg>
  </button>
```

The expected DOM output does not need to be exhaustive — it should include the elements, attributes, and structure an AI agent would need to validate correctness. Include: semantic HTML elements, ARIA attributes, class names (if predictable), and any accessibility-critical attributes. Omit: internal implementation details, event handlers, and styling properties.

**Deduplication rule:** If information in the examples section repeats what was already stated in the Props or Accessibility sections, reference it rather than restating it. The examples section adds contextual usage — it should not be a third place where prop defaults or ARIA roles are listed. If an example uses `variant="primary"`, do not re-explain what the primary variant does — the Props section already covered that.

---

## Step 2b: Prose tightness review

Before formatting, review each section for redundancy. The six sections should be complementary, not overlapping. Apply these rules:

- **Props section** is the single source of truth for what the component accepts. No other section should redefine prop types or defaults.
- **Anti-patterns section** should reference props by name without re-explaining them. "Do not use variant='destructive' for reversible actions" is sufficient — the Props section already explains what the destructive variant does.
- **Accessibility section** should reference the keyboard pattern once, not repeat interaction details from the Props section.
- **Examples section** should add contextual usage, not summarise what other sections already said.
- **Composition section** should focus on relationships, not re-describe the component's purpose.

If any section exceeds 100 words and contains information duplicated elsewhere, trim it. The target is dense precision, not comprehensive coverage through repetition.

## Step 3: Format for Figma MCP

The final description should be written as a single continuous text block suitable for pasting into Figma's component description field. Structure it with clear section headers in plain text (e.g. PURPOSE, PROPS, ANTI-PATTERNS) so an LLM scanning the description via MCP can locate sections without parsing markdown.

Total length: 400 to 700 words. Long enough to be comprehensive, short enough that the full description fits within a reasonable token budget when loaded alongside other components.

If JSON metadata is needed as well, hand off to `metadata-schema-generator`, which owns the machine-readable component files. This skill produces prose only.

## Step 4: Self-test

Before delivering the description, run a mental test: if an LLM received only this description and nothing else, could it:

1. Identify the correct component to use for a given UI requirement?
2. Configure it with the right props for a given context?
3. Avoid the three most common misuse patterns?
4. Understand where it can and cannot be placed?
5. Apply it accessibly without additional guidance?
6. Distinguish this component from the two or three most similar components in the system?
7. Generate a correct usage example that matches real-world application?

If the answer to any of these is no, revise the relevant section before delivering.

## Step 5: Write back to Figma (when a write-capable MCP is available)

If a Figma MCP with write access is connected, write the completed description directly into the Figma component's description field. This closes the loop — the description goes from generation to Figma in a single session, visible in Dev Mode immediately.

**How to write back:**
1. **Figma Console MCP** (Southleft; check for `figma_set_description`): pass the component's `nodeId` and the full six-section text as `description`. For rich formatting in Dev Mode, also pass the markdown-formatted version as `descriptionMarkdown`.
2. **Official Figma MCP** (check for `use_figma`): set the component's description through `use_figma`. Its reads are selection-scoped, so confirm the selected node is the component (or component set) you described.
3. After writing, confirm success by reading the component description back to verify it was saved correctly

**When NOT to write back:**
- If the user asked only for a draft or preview
- If the component is in a published library and the user does not have edit access
- If the user explicitly asked for output in chat only

**When no write-capable Figma MCP is connected:** present the description in chat and tell the user to paste it into the component's description field. If they ask to write it to Figma, point them at the Figma Console MCP or the official MCP's `use_figma` (see the mcp-setup-guide knowledge note).

## Step 6: Summarise in chat

End with a short chat summary:
- **Headline:** the component described and whether it was written to Figma (verified by read-back) or left for pasting
- **Written:** where the description went (Figma node name and ID, or "chat only")
- **Marked in the text:** each item marked "unverified" or "anticipated", so the team knows what to confirm
- **Scope:** the block from the output-discipline knowledge note, naming which sources (Figma, Storybook, source files, user) were actually read

## Quality checks

- Purpose section reads as a contract statement, not a product description
- Every prop found in the sources is documented with name, type, default, and description — no props are omitted
- Anti-patterns are specific to this component, not generic advice
- Composition rules give placement constraints, not just adjacency suggestions
- Accessibility section documents the specific ARIA and keyboard behaviour, not generic WCAG reference
- Final output is a single text block formatted for Figma's description field
- Description passes the seven-question self-test
- Every prop, default, role and key binding traces to source, Storybook, Figma or the user; the rest is marked "unverified" or left out
- If written back to Figma, the description was verified by reading it back from the component
