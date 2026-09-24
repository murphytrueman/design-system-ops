---
name: agent-instructions
description: "Write the AGENTS.md that tells coding agents how to use this design system: where things live, sourced rules, how to check work, what not to do; Claude, Cursor or Copilot pointers on request. Triggers: AGENTS.md for our system, make it AI-navigable, agent instructions. Inventory: codebase-index."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*)
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/output-discipline.md
---

# Agent instructions

A skill for writing the file coding agents actually read: an `AGENTS.md` at the repository root that tells an agent where the system's parts live, which rules apply and where each rule comes from, how to check its work, and what not to do. It links to the machine-readable files other skills produce (`.ai/index/`, `.ai/metadata/`, decision pages, token files) rather than copying them, so there is one place to keep current.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Agents working in a codebase read a small set of conventional files first: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`. Design system knowledge that isn't reachable from one of those is invisible at the moment it matters: the agent picks a component, types a colour, or writes a test from what it can see, and what it can see is props and values, not intent. The design system loses the argument it never got to make.

The fix is not more files in `.ai/`. It is one short file the agent will read, with pointers to the rest, and rules that are the team's own. Long instruction files get skimmed; unsourced rules get treated as suggestions or, worse, as policy the team never set.

## Boundaries

This skill writes instructions; it doesn't build the inventory (`codebase-index`), the per-component metadata (`metadata-schema-generator`), the token docs (`token-documentation`) or the choosing-between pages (`component-decision-tree`). It links to those when they exist and names them as the next step when they don't. If the system has no components, tokens or docs to point at yet, there is nothing to instruct; say so.

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`). This skill reads:
- `system.name`, `system.framework`, `system.styling`, `system.component_paths`, `system.tokens`
- `agent_instructions.path` — where to write the file (default `AGENTS.md` at the repo root)
- `agent_instructions.pointers` — extra entry points to write, each a one-line file that says "read AGENTS.md" (default: none; ask)

## Step 1: Inventory what an agent could be pointed at

Look before writing. Record the path of each thing found, or that it wasn't found:

- **Existing instructions:** `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*`, `.github/copilot-instructions.md`, `.windsurfrules`, a `docs/ai/` folder. If any exists, this skill updates it: keep what the files confirm, replace what they contradict, and say what changed. Never write a second file that competes with one the team already maintains.
- **Machine-readable outputs from this pack:** `.ai/index/` (inventory and graph), `.ai/metadata/` (per-component props, a11y contracts), `.ai/decision-trees/` or the markdown choosing pages, `.ai/tokens/` if token-documentation wrote one.
- **The system itself:** component source directories and the barrel export; the token source and its consumption form (custom properties, JS module, Tailwind theme, Sass); the docs site or Storybook URL from the README; `CONTRIBUTING.md`; `CHANGELOG.md`.
- **Enforcement that already exists:** ESLint and Stylelint configs (a `declaration-strict-value` rule, `no-restricted-imports`, `jsx-a11y`), lint and test scripts in `package.json`, CI workflow names. These are the rules that are already true; the file should tell the agent to run them.
- **Written rules:** contribution guidelines, an accessibility policy, a content or voice guide, decision records. Each is a source a rule can cite.

## Step 2: The provenance rule

Every rule in the file carries its source in brackets: a file path, a URL, a decision record id, or `team` when the user stated it in this session. A rule with no source is not written as a rule. If it's worth keeping, it goes in a final "Proposed, not yet policy" list with a one-line reason, for the team to accept or delete. Agents treat the file as the system's actual policy; an invented rule becomes policy the moment it's written down. See "Every figure and fact needs a source" in the output-discipline note.

## Step 3: Write AGENTS.md

Keep it under about 150 lines. Real paths, real names, no placeholders except `[confirm: …]` where the team hasn't answered, listed at the top. Structure:

```markdown
# Working with [System name]

Still to confirm: [list of `[confirm: …]`, or "none"]

## What this is
[Two sentences: what the system provides, who owns it, the docs URL.]

## Where things live
- Components: `src/components/` — exported from `src/index.ts`
- Tokens: `tokens/*.tokens.json` (DTCG), consumed as CSS custom properties from `src/styles/tokens.css`
- Component inventory and dependency graph: `.ai/index/` (run `codebase-index` to refresh)
- Per-component props and accessibility contracts: `.ai/metadata/`
- Choosing between components: `docs/choosing/` [or "not written yet"]
- Docs / Storybook: [URL]

## Use these, not those
- Use exported components from the package; don't re-implement or copy source. [CONTRIBUTING.md#local-components]
- Use semantic tokens (`--color-action-primary`, `--space-inset-md`), never raw values and never primitives (`--color-blue-500`). [tokens/README.md]
- When a component or variant doesn't exist: [the contribution route]. Don't build a local one. [CONTRIBUTING.md]

## Rules
[One line each, each with a source. Only what the team has actually written down or stated.]

## Accessibility
[The system's guarantee and standard, with source; where per-component contracts live; what stays the consumer's job.]

## Check your work
- `npm run lint` (ESLint: `no-restricted-imports`, `jsx-a11y`; Stylelint: `declaration-strict-value`)
- `npm test`
- [any design-system-specific check, from package.json]

## Don't
[Three to six concrete don'ts with sources, e.g. no `!important` on token-driven properties, no `jest.mock` of the design system package.]

## Proposed, not yet policy
[Unsourced rules the team should accept or delete, each with a one-line reason. Delete this section when empty.]
```

Write the content from Step 1's findings. Where a section has nothing to say (no `.ai/metadata/`, no accessibility policy), write the honest one-liner ("not written yet; run `metadata-schema-generator`") rather than inventing a contract.

## Step 4: Entry-point pointers (only when asked)

Some tools read their own file first. If `agent_instructions.pointers` lists them, or the user asks, write each as a pointer, never a copy, so `AGENTS.md` stays the single source:

- `CLAUDE.md`: "Read `AGENTS.md` before working with the design system."
- `.cursor/rules/design-system.mdc`: frontmatter with `alwaysApply: true` and the same one line.
- `.github/copilot-instructions.md`: the same one line.

If one of these already exists with its own content, append the pointer; don't replace the file.

## Step 5: Summarise in chat

- **Headline:** the file written or updated, and how many rules it holds with sources versus proposed
- **Files:** every path written, and every existing file appended to
- **Linked, not copied:** which `.ai/` and docs artefacts the file points at, and which don't exist yet
- **Scope:** the block from the output-discipline note: what was inspected, what wasn't, and every `[confirm]`

## Quality checks

- The file is under about 150 lines and every path in it exists in the repository
- Every rule has a source in brackets; unsourced rules are in "Proposed, not yet policy" or absent
- Token and component names in the examples are the system's real names, taken from the source
- "Check your work" lists commands that exist in `package.json`, not aspirational ones
- Machine-readable files are linked, never duplicated into the instructions
- An existing instructions file was updated in place, and the summary says what changed
- Nothing in the file describes a generic design system; a reader could tell which system it is from any section
