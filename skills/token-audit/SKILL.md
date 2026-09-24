---
name: token-audit
description: "Audit how design tokens are defined: tiers, naming, alias chains, raw values, orphans, DTCG readiness. Triggers: audit my tokens, token architecture review, token health check. Not for code consuming tokens (token-compliance), theme parity (theme-audit) or Figma variables (figma-variable-audit)."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(npx style-dictionary:*), Bash(npx terrazzo:*)
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Token audit

A skill for auditing design token architecture across whichever tiers are in use — typically primitives and semantics, with component tokens where the system uses them. Produces a structured report with severity-rated findings and a prioritised remediation list.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

This skill draws on the tiered token architecture model: primitives encode raw values, semantic tokens encode intent, and — where present — component tokens map intent to specific UI contexts. Not every system uses component tokens, and the absence of a component tier is not a finding. Most token debt accumulates when tiers blur — when component contexts reference primitives directly, when semantic names describe appearance rather than purpose, or when the primitive layer is treated as the only layer.

The audit is not about enforcing a particular naming convention. It's about identifying where the token structure is working against the teams using it.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `severity.*` — overrides for finding severity ratings (e.g. `hardcoded_color: critical` instead of the default `high`)
- `system.theming` — if true, elevate hardcoded colour findings to the severity specified in config
- `system.styling` — pre-selects the format-specific guidance to apply
- `integrations.style_dictionary` — parse tokens via Style Dictionary 4 or 5 (see below)
- `integrations.figma` — Figma variables as an additional token source
- `recurring.*` — the previous report, for trend comparison (see recurring workflow below)

## Auto-pull integrations

**Style Dictionary 4 or 5, or Terrazzo** (`integrations.style_dictionary.enabled: true`, or a config in the repo):
- Parse the config at `integrations.style_dictionary.config_path`
- Extract the full token tree with resolved references and tier structure
- Use this as the primary token source — skip the manual "provide your token files" question
- Run `npx style-dictionary build --config [path]` into a scratch output directory (or `npx terrazzo build`) to let the tool resolve every alias before you reason about the tree; its errors are findings with the tool named as the source

**Figma variables** (`integrations.figma.enabled: true`):
- Use the Figma MCP server to read variables from the file at `integrations.figma.file_key`
- Extract variable collections, modes, and resolved values
- Cross-reference Figma variables against code token files to detect mismatches (Figma says `--color-primary` is `#0066CC` but the code says `#0064CC` — that is a finding)

**GitHub** (`integrations.github.enabled: true`):
- Pull the token file directly from the default branch if no local file is provided

## Step 0: Token discovery

Before asking the user for files, search the codebase for token-like patterns. This step lowers activation energy for teams where tokens exist but are not centralised — the user does not have to know where all their tokens live.

**What to search for:**

1. **CSS custom properties** — scan all `.css` files for `:root` blocks or `--` prefixed properties. Include scoped variants (`.dark`, `[data-theme="..."]`, `.theme-*`).
2. **SCSS/Sass variables** — scan all `.scss` and `.sass` files for `$`-prefixed names. Follow `@import` and `@use` chains to find partial files (`_colors.scss`, `_variables.scss`, `_tokens.scss`).
3. **JSON/YAML token files** — scan for files matching common token naming patterns: `tokens.json`, `tokens.yaml`, `*.tokens.json`, `design-tokens/**`, `src/tokens/**`, `tokens/**`. Also look for DTCG-formatted files containing `$type` or `$value` keys.
4. **Style Dictionary configs** — scan for `style-dictionary.config.json`, `config.json` in a `style-dictionary/` directory, or `.style-dictionary.json`.
5. **TypeScript/JavaScript token objects** — scan `.ts` and `.js` files for exports matching common patterns: `export const tokens`, `export const theme`, `export default { color`, `as const` typed objects with token-like key hierarchies.
6. **Tailwind configurations** — scan for `tailwind.config.js`, `tailwind.config.ts`, or `tailwind.config.mjs` and extract the `theme` and `extend` blocks.
7. **Figma Tokens / Tokens Studio** — scan for `tokens.json` in a `.tokens` or `tokens` directory, or files exported from Tokens Studio.

**How to search:**

Use file system access (glob patterns, file reads) to scan the project. If GitHub integration is configured and there's no local clone, use `gh api search/code` only to locate candidate files, then read them. If Figma integration is configured, pull Figma variables as an additional token source.

Prioritise by specificity: a dedicated `tokens/` directory is more reliable than scattered CSS files. A Style Dictionary config is more reliable than raw JSON. But collect everything — fragmented token sources are themselves a finding.

**Discovery output:**

Produce a brief inventory before continuing:

```
Token sources found:
- src/tokens/colors.json (94 tokens, JSON, likely primitives)
- src/tokens/semantic.json (67 tokens, JSON, likely semantic tier)
- src/styles/variables.scss (43 variables, SCSS)
- tailwind.config.ts (theme block with 28 custom values)
Total: ~232 token-like declarations across 4 sources
```

If discovery finds nothing, proceed to Step 1 and ask the user for manual input. If discovery finds scattered sources across multiple formats, flag this as a finding: "Tokens exist in [N] different formats across [M] files. This fragmentation is structural debt — consider centralising to a single source of truth."

Present the discovered sources to the user and ask: "I found these token sources. Should I audit all of them, or focus on specific files?" This gives the user control without requiring them to have assembled the inventory manually.

---

## Step 0b: Orphan detection checkpoint

Before running the full audit, do one pass to identify token usage. This is the only orphan pass — Step 3c reuses its results.

1. **Declared tokens** — count every token found in Step 0 (or provided manually in Step 1).
2. **Referenced tokens** — search for references to each declared token, both from other tokens and from components in this repo. For CSS custom properties, search for `var(--token-name)`. For SCSS variables, search for `$variable-name` outside their declaration files. For JSON/DTCG tokens, search for alias references (`{token.path}`). For TypeScript objects, search for import and access patterns (`tokens.color.primary`, `theme.spacing.md`).
3. **Positive control** — before trusting the result, pick one token you know is used and confirm each search pattern finds it. If a pattern finds nothing for a known-used token, the pattern doesn't fit this codebase; fix it or report orphans for that format as unconfirmed.
4. **Orphan candidates** — tokens not referenced by another token or by any component in the scanned repo.

In a design system repo, most tokens are consumed by product repos that weren't scanned. An orphan here means "no in-repo consumer", not "unused". Report orphans as unconfirmed for external consumers unless the user has given you access to the consuming repos or usage data.

Produce a checkpoint summary (figures illustrative):

```
Orphan detection:
- 232 tokens declared
- 189 tokens referenced in-repo (at least once)
- 43 orphan candidates (no reference from another token or an in-repo component)
  Top candidates: --color-legacy-teal, --spacing-xl-deprecated, $font-heading-alt (3 more)
  Positive control: --color-action-primary found in 14 files by the same patterns
  Not checked: consuming product repos
```

This tells the user the scale of the question before the full audit begins. Confirmed orphans are maintenance burden without value — they clutter autocomplete, confuse new team members, and inflate the token count. Include orphan candidates as findings in the main audit (category: Coverage, severity: Low unless count exceeds 20% of total, then Medium), and say which consumers were checked.

If the orphan count is high (>30% of total tokens), flag this prominently: "Over a third of declared tokens are unreferenced. Before auditing token quality, consider whether a cleanup pass would simplify the architecture."

---

## Step 1: Gather the token source

If Step 0 discovered token sources, use them as the primary input — skip the manual question unless the user wants to override. If Step 0 found nothing (or was skipped because no codebase access was available), ask for the token source. Acceptable inputs:
- A JSON, YAML, or DTCG-formatted token file
- A Figma file or Tokens Studio export
- A pasted list of token names and values
- A Style Dictionary configuration
- A CSS file with custom properties (e.g. `:root { --color-primary: #5e4890; }` or theme variants scoped to `.dark { }`, `[data-theme="dark"]`, or similar selectors)
- An SCSS/Sass file with variables (e.g. `$color-primary: #5e4890;`)
- A TypeScript or JavaScript token object (e.g. `export const tokens = { color: { ... } }`)
- A Tailwind CSS configuration file (`tailwind.config.js` or `tailwind.config.ts`) with a `theme` or `extend` block defining custom tokens

**Format-specific guidance:**

For **CSS custom properties**: treat each `--` prefixed property as a token. Infer tier from naming patterns — properties like `--color-blue-500` are likely primitives, `--color-action-primary` are semantic, `--button-background-default` are component-tier. Where properties are scoped to selectors (`:root`, `.dark`, `[data-theme="dark"]`), treat each scope as a theme variant. References between CSS custom properties using `var(--other-token)` indicate tier relationships — map these the same way as JSON token references.

For **SCSS variables**: treat each `$` prefixed variable as a token. SCSS variables that reference other variables (e.g. `$color-primary: $blue-500`) indicate tier relationships. If variables are split across partials (`_colors.scss`, `_spacing.scss`), the file organisation may signal tier structure.

For **TypeScript/JavaScript objects**: treat the exported object's key hierarchy as the token structure. Nested objects map to tiers the same way JSON tokens do. For Emotion or styled-components themes, the theme object is the token source. Common patterns include: flat exports (`export const backgroundColor = { scene: '#FFF', primary: '#206EF6' }`), `as const` typed objects (`const tokens = { ... } as const`), aggregated barrel exports (`export const tokens = { breakpoint, fontSize, spacing }`), and theme-to-CSS-variable mapping functions (`mapThemeToVars()`). Helper functions like `theme.spacing(4)` or `theme.colors.primary` that resolve to token values are valid token references.

For **Tailwind configurations**: the `theme` block defines primitives, `extend` adds semantic overrides. Tailwind utility classes that reference custom tokens (e.g. `bg-primary`, `text-color-content-default`) are token references, not hardcoded values. Arbitrary values in square brackets (e.g. `h-[12px]`, `bg-[#ff0000]`) are the actual hardcoded violations.

If the person pastes raw token names without values, proceed with a naming and structure audit only. Note in the output that value analysis was not possible.

## Step 2: Map the tier structure

Identify which tiers are present:

**Primitive tier** — raw values, no semantic meaning. Examples: `color.blue.500`, `spacing.4`, `font-size.base`

**Semantic tier** — intent-driven references. Examples: `color.action.primary`, `spacing.component.gap`, `text.body.size`

**Component tier** — scoped to a specific component context. Examples: `button.background.default`, `card.padding.inner`

Flag a missing primitive or semantic tier. A system with only primitives has no semantic contract. A system with only semantic tokens has no single source of truth for raw values. Both are structural problems worth naming. A missing component tier is not a finding — see the token-architecture note.

## Step 3: Run the audit checks

For each check, produce a PASS, WARN, or FAIL rating with specific examples. Every finding carries evidence: the token path and the file and line where it is defined (`tokens/component.tokens.json:9`, `src/styles/tokens.css:17`).

**Severity rubric** (the `severity.*` config keys override these defaults):
- 🔴 **Critical** — a token file that isn't the source of truth it claims to be (generated output has drifted from it); tier leakage or a raw value at the semantic or component tier in a system that ships more than one theme, because the theme switch silently misses it
- 🟠 **High** — tier leakage or a raw value at the semantic or component tier in a single-theme system; an upward reference (semantic → component); a semantic token that names an appearance (`color.semantic.blue`)
- 🟡 **Medium** — convention inconsistency within a tier; a missing interaction state for a role the components already use; duplicate raw values with no documented distinction; orphan candidates above the 20% threshold
- ⚪ **Low** — ambiguity flags, platform suffixes, orphan candidates below the threshold, DTCG migration signals

### Naming checks

**Descriptive vs prescriptive naming**
Semantic tokens should describe purpose, not appearance.
- FAIL example: `color.semantic.blue` — describes colour, not intent
- PASS example: `color.action.primary` — describes role

**Tier leakage**
Component tokens should reference semantic tokens, not primitives.
- FAIL example: `button.background.default: {color.blue.500}` — skips the semantic tier
- PASS example: `button.background.default: {color.action.primary}` — correct reference chain

**Ambiguity flags**
Token names that could mean multiple things or require context to interpret (the token-architecture note has the full rule and its exceptions):
- Examples to flag: `normal`, `alt`, `variant`, `misc`, `other`, and `default` or `base` when they are the entire role (`color.default`)
- Not flagged: `default`/`base` as a state or level segment beside a role (`color.action.default`, `color.surface.base`), and t-shirt or numeric scale steps (`spacing.sm`, `radius.lg`)
- Each flagged token should include a suggested rename

**Convention consistency** (this skill owns token naming; `naming-audit` covers components and patterns)
Within each tier, identify the dominant casing, separator and segment order, and flag the tokens that break from it: `color.blue-500` beside `color.blue.500`, `hover/active` beside `hover/pressed`, `button.background-hover` beside `button.background.hover`. Report the dominant convention in the findings so the team can confirm it's the intended one.

**Platform suffix abuse**
Token names that encode platform specifics in the name rather than in the transformation layer:
- Examples: `color.primary.ios`, `spacing.mobile.gap` — these belong in transforms, not names

### Value checks (if values are available)

**Hardcoded values at semantic or component tier**
Any semantic or component token with a raw value rather than a reference is structural debt.
- Flag each occurrence with: token name, raw value found, and suggested reference target

**Duplicate raw values without token aliases**
Identical raw values appearing at the primitive tier under different names without explanation.
- Flag potential duplicates and ask whether the distinction is intentional

**Out-of-tier references**
Any token referencing a token from a higher-specificity tier.
- Example: a semantic token referencing a component token — this inverts the dependency direction

### Coverage checks

**Missing interaction states**
Review whether semantic tokens exist for all standard states: default, hover, active, disabled, focus, error, success, warning.

**Missing dark mode / theme aliases**
If the system intends to support theming, check whether semantic tokens exist as theme-aware aliases or whether raw values are used directly.

**Inconsistent component tier (only if the system uses component tokens)**
If the system has adopted component tokens and they exist for some components but not others in the same category, flag the inconsistency. If the system does not use component tokens at all, this is not a finding — a two-tier architecture (primitives and semantics) is a valid and common choice.

## Step 3b: DTCG 2025.10 alignment assessment (conditional — include only if relevant)

**Skip this section entirely** if the token source is not DTCG format and the team has not mentioned DTCG migration. Most teams don't need this. Include it when the token source uses DTCG format, when the team asks about DTCG compliance, or when migration planning is the purpose of the audit.

If the token source uses DTCG format, or if the team is considering DTCG migration:

**Structural validation is `schema-validator`'s job.** Type resolution, `$type` values outside the 13 types, 2025.10 value shapes, composite sub-value integrity, broken and circular aliases, and resolver document validity all belong there. If a schema-validator report exists, cite its finding IDs in this section; if not, run it (it's quick and mechanical) rather than re-checking by hand. This section reports what those results *mean* for the architecture, and adds the two checks below that need the tier map.

**Alias tier in composites.** A composite token whose sub-values mix references and raw values (`typography.body` with `fontFamily: {font.family.body}` but `fontSize: "16px"`) is the composite form of a raw value at the semantic tier: it can't theme. schema-validator reports the shape; this audit rates it. Severity: 🟡 Medium, 🟠 High if the composite is used by a themed component.

**Resolver contexts and theming.** If `.resolver.json` files exist, read each modifier's `contexts` and its `resolutionOrder` (the note describes the structure; the spec's term is context, not mode). A context that doesn't redefine a token inherits the earlier value, which is the design, not a gap. What this audit reports: theme-dependent semantic tokens (colour, shadow, border colour) that no non-default context redefines, so the theme silently keeps the default value; and token files that no set includes. Severity: 🟠 High for an inherited colour token in a shipped theme (contrast risk), ⚪ Low for a token file outside every set. `theme-audit` goes deeper on this when the team has more than one theme; cite it rather than duplicating.

**Migration signal (informational).** For teams not yet on DTCG 2025.10, give one paragraph: how many tokens would need `$type` (after type resolution), how many composites need restructuring into object values, whether string values need converting to object shapes, and whether resolver files would be needed for theming. Name the lowest-risk first step (usually annotating primitives with `$type`, which changes no resolved values). Then offer the full phased migration plan with effort ranges if they want it — don't produce it unasked.

## Step 3c: Token dependency map (conditional — include when codebase access is available)

**Skip this section** if there is no codebase access or if the audit is focused on token naming/structure only. Include it when the user has a codebase connected and wants to understand blast radius before making changes.

The dependency graph has one producer: `codebase-index`, which writes token-to-component edges to `.ai/index/`. If that directory exists, read the token edges from it, mark the orphan candidates from Step 0b on them, and list the high-fan-out tokens (bound by many components in this repo; say how many, and remember consumers outside the repo aren't counted). If it doesn't exist, say the blast-radius view wasn't built and suggest running `codebase-index` first; don't build a second graph here. Token-versus-Figma consistency is `figma-variable-audit` Step 6's job.

## Step 4: Produce the audit report

Open with a headline sentence that tells the reader the overall state and where to focus. Example: "Your token architecture has three structural issues — two in the semantic tier and one cross-tier collision. Here's the full breakdown."

Structure the report as follows:

---

### Token audit report

**Summary**
One paragraph. What is the overall state of the token architecture? What is the most urgent problem? Write this like a peer review, not a compliance filing.

**Tier structure**
- Primitive tier: 🟢 Strong / 🟡 Functional / 🟠 Weak / 🔴 Absent
- Semantic tier: 🟢 Strong / 🟡 Functional / 🟠 Weak / 🔴 Absent
- Component tier: 🟢 Strong / 🟡 Functional / 🟠 Weak, or "not used" (not a finding)
- Tier leakage instances: [count]

**Findings**

List each finding with:
- Finding ID (e.g. TA-01)
- Severity: 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low
- Check category: Naming / Value / Coverage
- Description: One sentence
- Evidence: the token path(s) and the file and line where each is defined
- Recommended action: Specific and actionable, naming the replacement

**Remediation priority**
Group findings into three tiers:
1. Fix first — structural problems affecting downstream consumers
2. Fix next — naming debt that compounds over time
3. Address eventually — coverage gaps and nice-to-haves

**Effort estimates**
For each remediation tier, provide calibrated effort estimates with explicit assumptions and caveats:

| Finding | Estimated effort | Assumptions | Confidence |
|---|---|---|---|
| [Finding ID] | [range, e.g. 4–8 hours] | [what this estimate assumes] | [High/Medium/Low] |

Always give a range ("4–8 hours", not "6 hours"), state what it assumes, and rate confidence High / Medium / Low with what would need scoping for Low. For "Fix first" items, note that the estimate covers the token-side change only and consumer migration is extra. Over 200 tokens or more than 3 consuming apps, suggest a timeboxed spike before committing to sprint planning.

The goal is estimates a project manager can defend in sprint planning, not optimistic targets that erode trust when overrun.

**Scope**
- **Inspected:** [token files, configs, and directories actually read]
- **Not inspected:** [what was out of reach, e.g. consuming product repos, Figma]
- **How "none found" was checked:** [e.g. the orphan search's positive control — omit if the report makes no absence claims]
- **Assumptions:** [anything taken as given rather than verified]

End with the closing note below.

---

## Recurring workflow

Follows the recurring-run procedure in the configuration-and-recurring note. Specific to this skill:

- Compare total violation count: increasing, stable, or decreasing?
- Flag persistent findings left unaddressed for 2+ cycles.
- Add a "Trend since last audit" section to the report header with the violation count delta (+/- n) and the list of newly introduced violations (these are the priority — they are recent debt).

## Step 5: Figma variables

Comparing code tokens with Figma variables, and creating or renaming variables in Figma, is `figma-variable-audit`'s job (its Step 6 does the cross-reference, its Step 10 the writes). If a Figma file is configured or the user mentions Figma, say the code-side audit is done and offer to run figma-variable-audit against the same token source, so the two reports line up by name. Don't compare or write to Figma from here.

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit sees your token files — it does not see the decisions behind them. Some findings may flag patterns your team chose deliberately. If any finding describes an intentional decision, let me know — I'll exclude it from future runs and learn your system's conventions. The goal is to surface problems you haven't seen yet, not to second-guess choices you've already made.

## Quality checks

- Every finding has a specific example with a file and line, not a generic description, and a severity from the rubric
- The summary paragraph is honest about severity rather than diplomatic
- Remediations are specific: "rename `color.semantic.blue` to `color.action.primary`" not "improve naming"
- The tier structure assessment covers primitive and semantic tiers, and the component tier where the system uses one
- If values were not available, the report notes which checks were skipped and why they matter
- Structural DTCG checks, the dependency graph and the Figma comparison are cited from schema-validator, codebase-index and figma-variable-audit, not redone here
- Orphan claims show their positive control and say which consumers weren't checked
- The Scope block and the closing note about intentional deviations are present
