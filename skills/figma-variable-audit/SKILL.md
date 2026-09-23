---
name: figma-variable-audit
description: "Audit Figma variable collections: tier mapping, naming, alias chains, modes, orphans; can fix in place with Figma Console MCP. Triggers: audit my Figma variables, review variable collections, Figma variable health. For token files in code use token-audit."
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Figma variable audit

A skill for auditing Figma variable collections against three-tier token architecture principles. Produces a structured report with severity-rated findings and a prioritised remediation list. For teams whose source of truth lives in Figma variables rather than code.

## Before you begin: verify references

Before doing anything else, confirm that every file listed in this skill's frontmatter `references:` field exists at its relative path from this SKILL.md. If any are missing, stop — the install is incomplete. This usually means a third-party installer (for example `npx skills install`) flattened the skill into a standalone folder and dropped the repo-root `knowledge-notes/` directory this skill depends on. Tell the user to reinstall using a supported method from `1-INSTALL.md` (git clone, or the `.plugin` bundle in Cowork) and to run `verify-install.sh` from the install root to confirm the fix. Only proceed without the references if the user explicitly says to — and if they do, state clearly in your output that it was produced in degraded mode without the pack's reference material.

## Context

This skill applies the three-tier token architecture model to Figma variables: primitives encode raw values, semantic variables encode intent, and component-tier variables map intent to specific UI contexts. Figma-native teams treat variables as their token source of truth — this audit reads Figma directly and validates the same structural dimensions as the code-based token-audit: naming conventions, tier separation, alias chains, mode coverage, orphaned variables, and DTCG readiness.

The audit is not about enforcing a particular naming convention. It's about identifying where the variable structure is working against the teams using it.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `severity.*` — finding severity overrides
- `integrations.figma` — Figma file key, default branch for mode selection
- `integrations.code_tokens` — code token source for the Step 6 cross-reference
- `recurring.*` — the previous variable audit, for trend comparison

---

## Step 0: Check Figma availability

This skill needs to read whole variable collections. Before proceeding, check which Figma access is available by attempting a lightweight call (such as `figma_get_status` or listing available Figma tools). Two limits decide what's possible:

- **The official Figma MCP can't list collections.** Its read tools are selection-scoped — `get_variable_defs` returns only the variables a selected node uses. It can show a sample, not run a collection-wide audit. If it's the only Figma connection, say the audit would be partial and offer the alternatives below.
- **The Figma REST Variables API is Enterprise-only.** Don't suggest it to teams on other plans.

A full audit needs the Figma Console MCP (Desktop Bridge plugin), which reads every collection through the Plugin API.

**If the Console MCP is not available:**
- Explain that this skill needs collection-wide read access to Figma variables
- Offer two alternatives:
  1. The user can provide an exported variables JSON file (from a variables-export plugin, or the Variables REST API on an Enterprise plan) — the audit can run against that
  2. The user can run the code-based `token-audit` skill instead, which audits token files in the codebase without needing Figma
- Do not fail silently. Do not retry the connection in a loop.

**If the Console MCP is available, proceed to Step 1.**

---

## Step 1: Connect to Figma and gather variables

Ask the user for a Figma file URL, file key, or node ID. Acceptable inputs:
- A complete Figma design file URL (e.g. `https://figma.com/design/abc123/Design%20System`)
- A file key alone (e.g. `abc123`)
- A node ID if auditing a specific component set (e.g. `123:456`)

If `.ds-ops-config.yml` specifies `integrations.figma.file_key`, use it automatically without asking.

**Pull Figma data:**
1. Use `figma_get_variables` with `resolveAliases: true` to extract all variable collections, modes, names, and resolved values
2. Use `figma_get_styles` to extract all color, text, effect, and grid styles for cross-reference (styles are sometimes used instead of or alongside variables)
3. Use `figma_get_component` for component metadata to identify component-tier variables

Request confirmation before reading. Once confirmed, connect and pull the data.

---

## Step 2: Map collections to token tiers

Identify which variable collections map to which tiers:

**Primitive tier** — raw values, no semantic meaning. Examples: `Primitives`, `Colors`, `Spacing`, `Font Sizes`, `Raw Colors`

**Semantic tier** — intent-driven references to primitives. Examples: `Semantic Colors`, `Theme`, `Intent Colors`, `Tokens`

**Component tier** — scoped to a specific component context. Examples: `Button`, `Card`, `Form Input`, `Navigation`

For each collection:
- Note its name and the tier it belongs to
- Flag collections that don't map cleanly to any tier (e.g. `Misc`, `Exports`, `Legacy`)
- Flag collections that mix tiers (primitives and semantics in the same collection)
- Count variables per collection per tier

Produce a brief tier map:
```
Collection → Tier:
- Primitives (142 variables) → Primitive
- Semantic (67 variables) → Semantic
- Button (18 variables) → Component
- Card (12 variables) → Component
Mixed: System (54 variables) → contains both primitives and semantic
Unmapped: Legacy (8 variables) → no clear tier
```

If any collection is unmapped or mixed, flag this as a finding.

---

## Step 3: Audit naming conventions

Figma groups variables with `/` — a variable named `color/action/primary` appears as `primary` inside the `color` → `action` groups. Expect `/` as the path separator; it maps to `.` in code token names. For each variable name in each collection, check:

**Hierarchical naming** — do names follow a path-like convention (category/role/variant/state)?
- PASS example: `color/action/primary`, `spacing/component/gap/sm`
- FAIL example: `colorPrimary`, `primary_color`, `button_bg_default` (flat names, no groups)

**Intent-based naming at semantic tier** — do semantic names describe purpose, not appearance?
- FAIL example: `color/semantic/blue` (describes colour, not intent)
- PASS example: `color/action/primary` (describes role)

**Reserved term avoidance** — flag colour names in semantic tiers (blue, red, green) and size terms (small, medium, large)
- These belong only in the primitive tier
- Flag each occurrence with suggested rename

**Naming consistency** — are casing, separators, and phrase ordering consistent across collections?
- Check for: camelCase vs snake_case vs kebab-case within segments, `/` groups vs dots or hyphens used as separators, segment order (role/variant/state vs variant/role/state)
- If inconsistency exists, identify the dominant pattern and flag deviations

**Ambiguity checks** — flag names that could mean multiple things:
- Examples: `default`, `base`, `normal`, `alt`, `variant`, `misc`, `other`
- Each flagged token should include a suggested rename or clarification

---

## Step 4: Audit alias chains

Trace the reference structure of every variable:

**Correct chain direction** — do component variables reference semantic variables (not primitives directly)?
- FAIL example: `button/bg/default` (Button collection) aliases `blue/500` (Primitives collection)
- PASS example: `button/bg/default` (Button collection) aliases `color/action/primary` (Semantic collection)

**Semantic references** — do semantic variables reference primitives?
- WARN example: `color/primary` (Semantic) aliases `color/other` (Semantic) — a semantic-to-semantic hop adds a layer without adding meaning
- PASS example: `color/primary` (Semantic) aliases `blue/500` (Primitives)

**Upward references** — are there any primitives or semantics referencing component-tier variables?
- These invert the dependency direction and are structural failures

**Chain length** — flag chains longer than 3 hops (component → semantic → primitive is 2 hops; 3 is tolerable; more than 3 usually means unnecessary abstraction layers)

**Broken chains** — are there any aliases pointing to non-existent variables?
- These are errors that prevent the variable from resolving

Produce a chain summary for at least one complete chain per tier:
```
Chain example: button/background/default (Button)
  button/background/default → color/action/primary (Semantic, 1 hop)
    → blue/500 (Primitives, 2 hops)
      → #0066CC (resolved value)
Status: ✅ PASS (correct direction, 2 hops)
```

---

## Step 5: Audit modes and theme coverage

For each collection, list all modes and check coverage:

**Mode definition** — do modes match what the collection varies by?
- Colour and theme collections: modes should be themes or brands (`Light`, `Dark`, `High Contrast`)
- Spacing and typography collections: breakpoint or density modes (`Desktop`, `Tablet`, `Mobile`, `Compact`) are legitimate
- WARN example: `iOS`, `Android` modes on a colour collection — platform differences belong in the transform layer, not in modes

**Unthemed values** — Figma gives every variable a value in every mode as soon as the mode is added (copied from the default), so "missing values" rarely exist. Check instead for semantic and component variables whose value in a non-default mode is identical to the default mode — for colour and shadow variables in a theme collection, that usually means the variable was never themed.
- Flag each with the collection, mode, and shared value; ⚠️ WARN, since some values legitimately don't change (a brand colour, a transparent overlay) — ask rather than assume
- Skip primitives: they aren't expected to vary by mode

**Mode consistency** — are all variables updated together when a mode changes, or are some stale?
- Spot-check: pick a semantic variable and verify that all components referencing it remain consistent across modes

Produce a mode coverage summary (figures illustrative):
```
Values identical to the default mode (Light):
            Dark   High Contrast
Semantic      2         5    (e.g. color/feedback/pending: #F5A623 in all modes)
Button        0         1    (button/border/focus)
```

---

## Step 6: Cross-reference with code tokens (if available)

If `.ds-ops-config.yml` specifies `integrations.code_tokens`, pull the code token source and compare:

**Name alignment** — do Figma variable names match code token names?
- Normalise before comparing: treat `/`, `.`, `-` and `_` as the same separator, drop prefixes like `$` and `--`, and compare case-insensitively. `color/action/primary`, `$color-action-primary` and `--color-action-primary` are the same name
- List only the mismatches that survive normalisation, with the Figma name and code name

**Value alignment** — do resolved Figma values match code token values?
- List instances where the same variable has different values in Figma and code
- Example: Figma `color/action/primary: #0066CC` vs Code `#0064CC`

**Coverage gaps** — variables existing in Figma but not in code (and vice versa)
- Figma-only variables are incomplete (no implementation)
- Code-only tokens are missing from design (designers lack visibility)

If no code tokens are found, document that and skip this step. Note in the output: "Code token cross-reference skipped — no code token source configured."

---

## Step 7: Audit for orphans and duplicates

**Orphaned variables** — variables with no consumers in this file
- Variables not referenced by any other variable (in any collection)
- Variables not bound to any component, frame, or style in this file
- Positive control: confirm the same check finds bindings for a variable you know is used (e.g. the primary action colour on Button). If it doesn't, the check isn't reading bindings and the orphan list is unconfirmed
- A published library is consumed by other files that this audit can't see. Report orphans as "no consumers in this file", not unused, unless library analytics or the consuming files were checked
- Count and list the top 10 orphans
- Severity: ⚪ Low if count <5, 🟡 Medium if 5–20, 🟠 High if >20

**Duplicate values** — multiple variables resolving to the same value
- Identify which duplicates are intentional (e.g. two variants of the same semantic intent)
- Identify which are accidental (same value, same name, declared twice)
- Example: `blue/500: #0066CC` and `navy/base: #0066CC` (both Primitives)

**Style overlap** — variables that duplicate style definitions
- Example: two text styles both defining the same font family, size, and weight
- Severity: ⚪ Low (these are maintainability burdens, not functional failures)

---

## Step 8: DTCG 2025.10 readiness assessment

If the team is considering or has declared DTCG migration, run these checks:

**Type declarations** — DTCG 2025.10 tokens need a resolvable type. Figma variables carry a `resolvedType` (COLOR, FLOAT, STRING, BOOLEAN) and `scopes` (e.g. `CORNER_RADIUS`, `GAP`, `FONT_SIZE`), so check:
- Can each variable's DTCG type be derived from `resolvedType` plus `scopes`? COLOR → color; FLOAT scoped to `GAP`, `WIDTH_HEIGHT` or `CORNER_RADIUS` → dimension; FLOAT scoped to `FONT_WEIGHT` → fontWeight
- Flag FLOAT variables left on `ALL_SCOPES` — they can't be typed without guessing
- Recommendation: set precise scopes (which also cleans up Figma's variable pickers) and map them to DTCG types in the export transform. Don't encode types in variable names

**Composite types** — Figma doesn't have native composite types (typography, shadow, border). Check:
- Are semantic variables referencing multiple primitives to construct composites? (e.g. a text style combining font family, size, weight)
- How would these be represented in DTCG format?
- Recommendation: define composite variable structures and naming

**Mode compatibility** — DTCG resolver files require mode consistency. Check:
- Are semantic variables actually themed in each mode (the unthemed-values check in Step 5)?
- Are mode names DTCG-compatible (no spaces, no slashes)?

**Migration effort estimate:**
- Count variables needing type inference
- Estimate naming changes needed
- Recommend sequence: 1. Audit naming (this step), 2. Set precise scopes, 3. Plan composite structure, 4. Prepare transform layer for DTCG export

---

## Step 9: Produce the audit report

Open with a headline sentence that tells the reader the overall state and where to focus. Example: "Your variable structure is sound, but 9 component variables skip the semantic tier and 5 semantic colours were never themed for Dark."

Structure the report as follows:

### Figma variable audit report

**Summary**

One paragraph. What is the overall state of the Figma variable architecture? What is the most urgent problem? (One sentence for critical findings.)

**Tier structure**
- Primitive tier: 🟢 Strong / 🟡 Functional / 🟠 Weak / 🔴 Absent
- Semantic tier: 🟢 Strong / 🟡 Functional / 🟠 Weak / 🔴 Absent
- Component tier: 🟢 Strong / 🟡 Functional / 🟠 Weak, or "not used" (not a finding)
- Tier leakage instances: [count]

**Findings**

List each finding with:
- Finding ID (e.g. FVA-01)
- Severity: 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low
- Category: Naming / Structure / Coverage / DTCG
- Description: One sentence
- Evidence: Specific variables or collections affected
- Remediation: Specific and actionable

Example:
```
FVA-02 | 🟠 High | Naming | Primitive tier contains semantic-like names.
Evidence: color/action/primary, color/feedback/success (Primitives collection)
Remediation: Move intent-based colours to the Semantic collection. Rename primitives: color/blue/500, color/green/600
```

**Remediation priority**

Group findings into three tiers:
1. Fix first — structural problems affecting downstream consumers (tier leakage, broken alias chains)
2. Fix next — naming debt that compounds over time (reserved terms, ambiguity)
3. Address eventually — coverage gaps and nice-to-haves (orphans, DTCG migration)

**Mode coverage analysis** (if modes exist)

Show coverage matrix and gaps.

**DTCG readiness** (if applicable)

Structural changes needed for clean DTCG export. Effort estimate and recommended migration sequence.

**Scope**
- **Inspected:** [Figma file, collections, and modes actually read, and the MCP used]
- **Not inspected:** [e.g. files consuming the published library, code tokens if not configured]
- **How "none found" was checked:** [e.g. the orphan check's positive control — omit if the report makes no absence claims]
- **Assumptions:** [anything taken as given rather than verified]

End with the closing note below.

---

## Small-system note

For files with fewer than 50 variables:
- Shift from statistical audit to per-variable review
- Name every variable in the findings
- Compress the findings table into inline annotations (variable name | severity | finding)
- Focus on manual traceability rather than pattern detection

---

## Step 10: Fix in place (when Figma Console MCP is available)

If the Figma Console MCP from Southleft is connected (check for `figma_rename_variable`, `figma_update_variable`, and `figma_add_mode` tool availability), offer to fix findings directly in Figma after presenting the audit report. This turns the audit from a report into a remediation session.

**What can be fixed in place:**
- **Naming violations:** Use `figma_rename_variable` to rename variables that violate conventions. Rename preserves all values, modes, and alias references.
- **Missing modes:** Use `figma_add_mode` to add modes that should exist but don't (e.g. a collection has Light but not Dark).
- **Missing semantic variables:** Use `figma_create_variable` to create semantic-tier variables that the audit identified as gaps.
- **Incorrect values:** Use `figma_update_variable` to correct values in specific modes.

**What should NOT be fixed automatically:**
- Deleting variables (destructive — always confirm with the user first)
- Restructuring entire collections (too broad — present a migration plan instead)
- Creating alias chains (requires design intent that the audit cannot infer)

**Workflow:**
1. Present the audit report first — always show findings before acting
2. Ask the user which findings they want fixed in place: "I found 12 naming violations and 3 missing modes. Want me to fix these directly in Figma?"
3. Fix confirmed items one category at a time (all renames, then all mode additions, etc.)
4. After fixing, re-read the affected variables to verify the changes took effect
5. Update the audit summary to distinguish "fixed" from "remaining" findings

**When only the official Figma MCP is connected:** the audit can't run collection-wide (see Step 0), so there's no full findings list to fix from. Present what the selection-scoped read showed, say it's partial, and recommend the Figma Console MCP from Southleft for both the full audit and in-place fixes.

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit compares Figma variables against structural best practices — it does not see why variables were structured the way they are. Some findings may flag deliberate choices. If any finding describes an intentional decision, let me know — I'll calibrate future audits to your team's conventions. The goal is to surface problems, not to second-guess decisions you've already made.

---

## Quality checks

1. Every finding references a specific variable name and collection, not generic advice
2. Alias chain analysis covers at least one complete chain from component → semantic → primitive
3. Mode analysis includes every mode in every collection, and checks for unthemed values rather than "missing" ones
4. Cross-reference with code tokens attempted (document result: found/not found/not configured)
5. DTCG readiness section includes at least one concrete structural recommendation
6. Severity ratings are consistent with token-audit severity for equivalent findings
7. Report can be understood by someone who has not seen the Figma file
8. If fixes were applied via Figma Console MCP, each fix was verified by reading back the changed variable
9. Orphan claims show their positive control and say that consuming files weren't checked
10. The Scope block and the closing note about intentional deviations are present
