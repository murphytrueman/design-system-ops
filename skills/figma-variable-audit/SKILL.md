---
name: figma-variable-audit
description: "Audit Figma variable collections against token architecture best practices. Trigger when someone says: audit my Figma variables, check my Figma tokens, are my variables structured correctly, Figma variable health, review my variable collections, variable naming check, or anything about auditing the quality or structure of Figma variables."
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Figma variable audit

A skill for auditing Figma variable collections against three-tier token architecture principles. Produces a structured report with severity-rated findings and a prioritised remediation list. For teams whose source of truth lives in Figma variables rather than code.

## Context

This skill applies the three-tier token architecture model to Figma variables: primitives encode raw values, semantic variables encode intent, and component-tier variables map intent to specific UI contexts. Figma-native teams treat variables as their token source of truth — this audit reads Figma directly and validates the same structural dimensions as the code-based token-audit: naming conventions, tier separation, alias chains, mode coverage, orphaned variables, and DTCG readiness.

The audit is not about enforcing a particular naming convention. It's about identifying where the variable structure is working against the teams using it.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `severity.*` — overrides for finding severity ratings
- `integrations.figma` — Figma file key, default branch for mode selection
- `integrations.code_tokens` — path to code token source (if cross-referencing is desired)
- `recurring.*` — if this is a recurring run, load the previous report for trend comparison

If no config file exists, proceed with defaults and manual input as before.

---

## Step 0: Check Figma availability

This skill requires a Figma MCP connection. Before proceeding, verify that Figma tools are available by attempting a lightweight call (such as `figma_get_status` or listing available Figma tools).

**If Figma is not available:**
- Explain that this skill needs a live connection to Figma to read variable collections
- Offer two alternatives:
  1. The user can provide an exported variables JSON file (exported from Figma's local variables panel or via the Variables REST API) — the audit can run against that
  2. The user can run the code-based `token-audit` skill instead, which audits token files in the codebase without needing Figma
- Do not fail silently. Do not retry the connection in a loop.

**If Figma is available, proceed to Step 1.**

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

**Semantic tier** — intent-driven references to primitives. Examples: `Semantic Colors`, `Theme`, `Component Tokens`, `Intent Colors`

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

For each variable name in each collection, check:

**Hierarchical naming** — do names follow a path-like convention (category.role.variant.state)?
- PASS example: `color.action.primary`, `spacing.component.gap.sm`
- FAIL example: `colorPrimary`, `primary_color`, `button_bg_default`

**Intent-based naming at semantic tier** — do semantic names describe purpose, not appearance?
- FAIL example: `color.semantic.blue` (describes colour, not intent)
- PASS example: `color.action.primary` (describes role)

**Reserved term avoidance** — flag colour names in semantic tiers (blue, red, green) and size terms (small, medium, large)
- These belong only in the primitive tier
- Flag each occurrence with suggested rename

**Naming consistency** — are casing, separators, and phrase ordering consistent across collections?
- Check for: camelCase vs snake_case, dot notation vs hyphen, variable order (role.variant.state vs variant.role.state)
- If inconsistency exists, identify the dominant pattern and flag deviations

**Ambiguity checks** — flag names that could mean multiple things:
- Examples: `default`, `base`, `normal`, `alt`, `variant`, `misc`, `other`
- Each flagged token should include a suggested rename or clarification

---

## Step 4: Audit alias chains

Trace the reference structure of every variable:

**Correct chain direction** — do component variables reference semantic variables (not primitives directly)?
- FAIL example: `button.bg.default: {Primitives.blue.500}`
- PASS example: `button.bg.default: {Semantic.color.action.primary}`

**Semantic references** — do semantic variables reference primitives?
- FAIL example: `Semantic.color.primary: {Semantic.color.other}`
- PASS example: `Semantic.color.primary: {Primitives.blue.500}`

**Upward references** — are there any primitives or semantics referencing component-tier variables?
- These invert the dependency direction and are structural failures

**Chain length** — flag chains deeper than 3 hops (component → semantic → primitive is 2 hops; 3+ indicates unnecessary abstraction layers)

**Broken chains** — are there any aliases pointing to non-existent variables?
- These are errors that prevent the variable from resolving

Produce a chain summary for at least one complete chain per tier:
```
Chain example: button.background.default
  button.background.default → Semantic.color.action.primary (1 hop)
    → Primitives.blue.500 (2 hops)
      → #0066CC (resolved value)
Status: PASS (correct direction, 2 hops)
```

---

## Step 5: Audit modes and theme coverage

For each collection, list all modes and check coverage:

**Mode definition** — are modes named after semantic contexts (light/dark, brand variants) or implementation details?
- FAIL example: `Desktop`, `Mobile`, `iOS` (platform-specific, not theme-specific)
- PASS example: `Light`, `Dark`, `High Contrast` (semantic context)

**Mode completeness** — does every variable have a value in every mode?
- Flag any variable with missing values in one or more modes
- For semantic and component tiers, missing values are FAIL (system will fall back unpredictably)
- For primitive tiers, missing values may be intentional (a primitive only needed in dark mode)

**Mode consistency** — are all variables updated together when a mode changes, or are some stale?
- Spot-check: pick a semantic variable and verify that all components referencing it remain consistent across modes

Produce a mode coverage matrix:
```
Variables per mode:
         Light   Dark   High Contrast
Primitive  142    142     142 (complete)
Semantic    67     65      67 (1 missing in Dark: color.feedback.pending)
Button      18     18      18 (complete)
```

---

## Step 6: Cross-reference with code tokens (if available)

If `.ds-ops-config.yml` specifies `integrations.code_tokens`, pull the code token source and compare:

**Name alignment** — do Figma variable names match code token names?
- List mismatches with the Figma name and code name
- Example: Figma `color.action.primary` vs Code `$color-action-primary`

**Value alignment** — do resolved Figma values match code token values?
- List instances where the same variable has different values in Figma and code
- Example: Figma `color.action.primary: #0066CC` vs Code `#0064CC`

**Coverage gaps** — variables existing in Figma but not in code (and vice versa)
- Figma-only variables are incomplete (no implementation)
- Code-only tokens are missing from design (designers lack visibility)

If no code tokens are found, document that and skip this step. Note in the output: "Code token cross-reference skipped — no code token source configured."

---

## Step 7: Audit for orphans and duplicates

**Orphaned variables** — variables with no consumers
- Variables not referenced by any other variable (in any collection)
- Variables not applied to any Figma components or frames
- Count and list the top 10 orphans
- Severity: Low if count <5, Medium if 5–20, High if >20

**Duplicate values** — multiple variables resolving to the same value
- Identify which duplicates are intentional (e.g. two variants of the same semantic intent)
- Identify which are accidental (same value, same name, declared twice)
- Example: `Primitives.blue.500: #0066CC` and `Primitives.navy.base: #0066CC`

**Style overlap** — variables that duplicate style definitions
- Example: two text styles both defining the same font family, size, and weight
- Severity: Low (these are maintainability burdens, not functional failures)

---

## Step 8: DTCG 2025.10 readiness assessment

If the team is considering or has declared DTCG migration, run these checks:

**Type declarations** — DTCG 2025.10 requires `$type` annotations. Figma variables do not natively support this, so check:
- Can variable names infer a `$type`? (e.g. `color.*` → color, `spacing.*` → dimension)
- Are variable values consistent with their inferred type?
- Recommendation: define a naming convention that encodes DTCG types, or prepare a transformation layer

**Composite types** — Figma doesn't have native composite types (typography, shadow, border). Check:
- Are semantic variables referencing multiple primitives to construct composites? (e.g. a text style combining font family, size, weight)
- How would these be represented in DTCG format?
- Recommendation: define composite variable structures and naming

**Mode compatibility** — DTCG resolver files require mode consistency. Check:
- Do all semantic variables have values in all modes?
- Are mode names DTCG-compatible (no spaces, no slashes)?

**Migration effort estimate:**
- Count variables needing type inference
- Estimate naming changes needed
- Recommend sequence: 1. Audit naming (this step), 2. Add type inference to names, 3. Plan composite structure, 4. Prepare transform layer for DTCG export

---

## Step 9: Produce the audit report

Structure the report as follows:

### Figma variable audit report

**Summary**

One paragraph. What is the overall state of the Figma variable architecture? What is the most urgent problem? (One sentence for critical findings.)

**Tier structure**
- Primitive tier: present / absent / partial
- Semantic tier: present / absent / partial
- Component tier: present / absent / partial
- Tier leakage instances: [count]

**Findings**

List each finding with:
- Finding ID (e.g. FVA-01)
- Severity: Critical / High / Medium / Low
- Category: Naming / Structure / Coverage / DTCG
- Description: One sentence
- Evidence: Specific variables or collections affected
- Remediation: Specific and actionable

Example:
```
FVA-02 | High | Naming | Primitive tier contains semantic-like names.
Evidence: Primitives.color.action.primary, Primitives.color.feedback.success
Remediation: Move intent-based colours to Semantic tier. Rename primitives: color.blue.500, color.green.600
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

**When the standard Figma MCP is connected (read-only):** The audit runs normally but cannot apply fixes. Present findings and note that the user will need to make changes in Figma manually. If the user asks "can you fix these?", explain that the standard Figma MCP is read-only and recommend the Figma Console MCP from Southleft for direct remediation.

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit compares Figma variables against structural best practices — it does not see why variables were structured the way they are. Some findings may flag deliberate choices. If any finding describes an intentional decision, let me know — I'll calibrate future audits to your team's conventions. The goal is to surface problems, not to second-guess decisions you've already made.

---

## Quality checks

1. Every finding references a specific variable name and collection, not generic advice
2. Alias chain analysis covers at least one complete chain from component → semantic → primitive
3. Mode analysis includes every mode in every collection
4. Cross-reference with code tokens attempted (document result: found/not found/not configured)
5. DTCG readiness section includes at least one concrete structural recommendation
6. Severity ratings are consistent with token-audit severity for equivalent findings
7. Report can be understood by someone who has not seen the Figma file
8. If fixes were applied via Figma Console MCP, each fix was verified by reading back the changed variable
9. The closing note about intentional deviations is present
