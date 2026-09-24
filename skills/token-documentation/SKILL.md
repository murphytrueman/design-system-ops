---
name: token-documentation
description: "Write reference docs for existing design tokens: semantic intent, use/do-not-use, references, used-by, theming contract, misuse list. Triggers: document our tokens, token reference, what is this token for. Token structure/architecture audit: use token-audit; file validation: schema-validator."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(grep:*), Bash(rg:*)
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Token documentation

A skill for writing documentation for design tokens that communicates semantic intent, usage context, and application rules across all three tiers. Output is reference documentation that tells consumers what a token means and how to use it correctly — not just what value it resolves to.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Token documentation has a chronic problem: it stops at the value. A token reference that says `color.action.primary: #0066CC` tells a consumer the resolved colour, but not when to use it, what it communicates to users, which components it belongs on, or what happens when it is misapplied. Teams that rely purely on value-level documentation make naming decisions based on colour proximity rather than semantic intent, and the system drifts.

The goal is documentation that makes the semantic contract legible. A consumer reading these docs should come away understanding not just what a token resolves to, but why it exists and where it belongs.

## Boundaries

This skill documents existing tokens. It does not create new tokens, redesign the token architecture, or validate token file structure (use `schema-validator` for structural validation, `token-audit` for architectural assessment). If the token set is empty or has not been defined yet, this skill does not apply — help the team establish their token architecture first. If only primitive tokens exist (no semantic tier), note that the documentation value is limited since primitive tokens are largely self-documenting, and suggest establishing a semantic tier before investing in documentation.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `integrations.style_dictionary` — the token tree, parsed automatically
- `integrations.figma` — Figma variables to cross-reference
- `integrations.documentation` — existing token docs to update rather than rewrite

## Auto-pull integrations

**Style Dictionary (4 or 5) or Terrazzo** (`integrations.style_dictionary.enabled: true`, or a config in the repo):
- Parse the config to extract the complete token tree with resolved references
- Auto-detect tier structure, token names, values, and reference chains
- This replaces the manual "provide your token files" step

**Figma MCP** (`integrations.figma.enabled: true`):
- Pull Figma variable collections and modes (light/dark, brand variants)
- Cross-reference Figma variables against code tokens for completeness check

**Documentation platform** (`integrations.documentation.enabled: true`):
- Check for existing token documentation to incorporate rather than overwrite

## Step 1: Gather the token set

Ask for or confirm (skip questions already answered by auto-pull):
- The tokens to be documented (a specific set, a full tier, or the entire system)
- The source format: JSON, DTCG, Tokens Studio export, Style Dictionary configuration, CSS custom properties (`:root { --token: value; }`), SCSS/Sass variables (`$token: value;`), TypeScript/JavaScript token objects, Tailwind config (`theme` / `extend` block), or listed by name
- Any existing documentation or notes on intent that should be incorporated
- The audience for the documentation (designers only, developers only, or both — this affects the technical depth)

For CSS custom properties and SCSS variables: infer token hierarchy from naming patterns (e.g. `--color-blue-500` → primitive, `--color-action-primary` → semantic, `--button-bg-default` → component). For Tailwind configs, the `theme` block is the token source. For TypeScript/JavaScript token objects: the exported object hierarchy maps directly to token tiers — nested keys are the path (e.g. `tokens.color.brand.blue[500]` → `color.brand.blue.500`). Include both the object key path and resolved value in the documentation. For `as const` objects, the literal types provide exact values without runtime ambiguity.

If the full system is being documented, suggest starting with the semantic tier. Semantic tokens are where intent documentation does the most work. If the system uses component tokens, include those after semantics.

**Provenance rule.** Names, values and references come from the token files. Intent comes from token descriptions (`$description` or equivalent), the team's docs, or the user; intent you write from the name alone is marked "proposed". "Used by" and misuse entries follow the rules in Step 2 and Step 4. See "Every figure and fact needs a source" in the output-discipline knowledge note.

## Step 2: Document by tier

### Primitive tokens

Primitive token documentation is lightweight. The goal is to establish what the scale looks like and what it is derived from — not to explain when to use `color.blue.400` vs `color.blue.500`, because that is the semantic tier's job.

Document:
- Scale overview: how the scale is structured and what increments mean
- Source: where the values come from (a specific palette tool, a brand colour system, a typographic scale)
- Usage constraint: one sentence stating that primitive tokens should not be used directly in components — they are referenced by semantic tokens

Format per primitive group:
```
[Token group name]
Scale: [describe the scale — e.g. 50–950 in 50-point increments, or T-shirt sizing]
Source: [where values come from]
Values: [list or reference to the token file]
Usage: Reference via semantic tokens only.
```

### Semantic tokens

Semantic tokens carry the intent contract. This is where most documentation effort belongs.

For each semantic token or semantic token group, document:

**Intent:** What does this token communicate to users? One sentence. Not what it looks like — what it means.
Example: `color.action.primary` — Identifies the primary interactive action in a given context. Signals that an element is the most important or most expected next step for the user.

**Resolved value:** What value does this token produce in the default theme? (And in other themes if theming is supported.)

**Tier reference:** Which primitive token does this semantic token reference?

**Usage context:** Where this token belongs — which component surfaces, which states, which user-facing roles.

**Usage constraint:** Where this token should not be used — specific misuse patterns to avoid.

**Component associations:** Which components reference this token. Build this by searching component source (styles, token bindings, component token files) for each token's name in the forms the codebase uses (e.g. `color.action.primary`, `--color-action-primary`, `tokens.color.action.primary`). Before writing "no components use this token", confirm the search finds a token you know is used; if it can't, write "not determined" instead.

Format per semantic token:
```
[token.name]

Intent: [one sentence on what this token communicates]
Resolved value: [value(s) by theme]
References: [primitive token(s)]

Use on: [list of appropriate surfaces or component types]
Do not use on: [specific misuse contexts]

Used by: [component names found referencing this token, or "not determined"]
```

### Component tokens (include only if the system uses them)

Not every system has a component token tier — many systems bind semantic tokens directly in component code, and that is a valid architecture. If the system does use component tokens, they are the most specific tier and the most commonly under-documented because they feel obvious. "Of course `button.background.default` is the button's default background" — but what should happen if a product team wants to override it? Which semantic token should they route through? Are there states the documentation has not covered?

If the system does not use component tokens, skip this section entirely. Do not recommend introducing them unless the context calls for it (white-labelling, multi-brand, complex components with many token bindings).

For component tokens, document:
- Which component this token belongs to
- Which prop or state it controls
- Which semantic token it references (and why — if the mapping is not obvious)
- Whether overriding this token at the product level is expected or discouraged

Group component token documentation by component. Do not produce a flat alphabetical list of component tokens — it is unusable.

Format per component group:
```
[Component name] tokens

[token.name] — [prop or state it controls]
References: [semantic token]
Override guidance: [expected / discouraged / never — with one-sentence reason]
```

## Step 3: Document the theming contract (if applicable)

If the system supports multiple themes (light/dark, brand variants, platform-specific themes), document how the semantic tokens resolve across themes and what the contract is for adding a new theme.

This documentation is often missing entirely, which means teams learn the theming system by reading the token files rather than by reading a clear contract. The contract should answer:
- Which tokens change across themes and which stay fixed
- How a new theme is added and what tokens are required
- What happens if a token is not defined in a custom theme (fallback behaviour)

## Step 4: Add the misuse reference

At the end of the documentation, include a brief misuse reference: the most common incorrect token usages, with the correct alternative for each. Take entries from `token-compliance` or `drift-detection` findings, or from the user. Anything else is labelled "anticipated" so it isn't read as an observed problem.

Format:
```
Common misuse: Using [wrong token] to achieve [visual outcome] ([source] or anticipated)
Why it's wrong: [one sentence — what the wrong token communicates that conflicts with the intended use]
Use instead: [correct token]
```

Five to ten entries is usually enough to cover the most frequent errors.

## Step 4b: Token governance note

At the top of the token documentation, include a governance section that answers the question every consumer eventually asks: "Who do I talk to when I need a token that does not exist?"

Ask the user for each field; leave `[TBC]` for anything they don't know rather than naming an owner or cadence yourself.

**Token governance:**
- **Token owner:** [Named person or team responsible for the token architecture]
- **Request process:** [How to request a new token — contribution workflow reference, Slack channel, or issue template]
- **Change cadence:** [How often are token changes released? Is there a review cycle?]
- **Documentation updates:** When a token changes, the documentation is updated by [owner / contributor / automated from token source]. If documentation lags behind token changes, report it to [channel].

This note prevents the common failure mode where token documentation is accurate at publication but becomes stale because no one owns the update process.

## Step 5: Write intent back into the source

The token file is where intent survives. Docs pages drift; a `$description` travels with the token into Style Dictionary, Terrazzo, Tokens Studio, Figma variable sync and any docs generator. So the machine-readable output of this skill is the source itself, not a parallel file:

- **DTCG files:** put the one-sentence intent in each semantic (and component) token's `$description`. Put the use/do-not-use guidance under `$extensions` with a reverse-domain key the team chooses, for example `"com.<org>.usage": { "useOn": [...], "doNotUseOn": [...] }`, so tools that don't know it preserve it. Group-level `$description` covers a scale.
- **Style Dictionary 3 files:** the `comment` property.
- **CSS, Sass, TypeScript token sources:** a comment above the declaration in the file's own comment syntax.
- **Figma variables** (Console MCP connected): write the same sentence to the variable description with `figma_update_variable`, so designers read what engineers read.

Show the diff and write only after the user confirms. Intent marked "proposed" is written as `[proposed] …` so nobody mistakes a guess for a decision. A separate JSON reference is a copy that drifts: produce `.ai/tokens/token-reference.json` only if the user asks for it, and then generate it from the source after the write-back, never by hand.

**DTCG alignment (only if the system uses or is migrating to DTCG).** One short section: the token types in use and any composite sub-value conventions; for resolvers, each set's purpose and files, each modifier and its contexts, and the resolution order (a diagram if there are more than three sets or contexts); and, if partly migrated, which categories are done and what remains.

## Step 6: Write the documentation files

Unless `integrations.documentation` names a platform, write markdown the docs site can ingest:

```
docs/tokens/
  README.md            index: tiers explained, governance note (Step 4b), theming contract (Step 3), links
  primitives.md        per group: scale, source, "reference via semantic tokens only"
  semantic.md          grouped by function (actions, feedback, text roles, surfaces, spacing roles), the Step 2 format per token
  components.md        only if the system uses component tokens; grouped by component
  quick-reference.md   Step 6b
  misuse.md            Step 4
```

If token docs already exist, update them in place and say what changed; don't leave two sets. The semantic reference is the most-used page: it comes first in the index and its groups are the jobs consumers do, not the token categories.

## Step 6b: Quick reference by semantic function

In addition to the full documentation, produce a one-page quick reference organised by what the consumer is trying to do, not by token category:

Illustrative lines:
- **"I need a colour for a primary action":** `color.action.primary`
- **"I need spacing between sections":** `spacing.lg`
- **"I need a page heading":** `typography.heading.lg`

Use the system's real token names, grouped by the jobs consumers actually do (colour, spacing, typography). Publish it alongside the full documentation as a fast-lookup tool.

## Step 7: Summarise in chat

End with a short chat summary:
- **Headline:** how many tokens were documented, by tier
- **Files written:** doc paths, the token source files whose `$description` (or comments) were updated, and `.ai/tokens/token-reference.json` only if the user asked for it
- **Marked:** intents marked "proposed", misuse entries marked "anticipated", "Used by" entries left "not determined", and `[TBC]` governance fields
- **Scope:** the block from the output-discipline knowledge note, including how the "Used by" search was shown to work

## Quality checks

- Every semantic token has an intent description, not just a value and name
- Usage context and usage constraint are both present — not just "use this for buttons"
- Component tokens reference their semantic parent and include override guidance
- The theming contract is documented if theming is supported
- The misuse reference exists and is specific, with each entry sourced or labelled "anticipated"
- "Used by" comes from a source search with a positive control, not from token names
- Format is appropriate for the documentation platform — navigable, not just comprehensive
- Intent was written back into the token source (with confirmation), so the docs and the files can't disagree; no parallel JSON was produced unasked
