---
name: schema-validator
description: "Validate token files structurally against DTCG 2025.10 (including resolvers), Style Dictionary 3 to 5 or Tokens Studio: parse errors, $type/$value, name rules, broken or circular aliases. Trigger: validate token JSON, DTCG compliance, are my token files valid. Naming or architecture: token-audit."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(npx style-dictionary:*), Bash(npx terrazzo:*)
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Schema validator

A skill for validating that design token files conform to their expected format — DTCG 2025.10 (token files and resolver documents), Style Dictionary 3, 4 or 5, Tokens Studio, or a custom schema. Catches structural issues before they break build pipelines, cause silent failures, or produce incorrect output.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Token files are infrastructure. When a token file is malformed — a missing `$type` declaration, a `$value` that resolves to nothing, an alias that points to a deleted token — the failure mode is rarely loud. The build might still succeed. The wrong value might ship. The design intent might be silently lost.

Schema validation is the first line of defence. It answers a simple question: do these files meet the structural contract they claim to meet? A DTCG file must have `$value` on every token. A Style Dictionary file must have valid reference syntax. A Tokens Studio export must preserve group hierarchy.

This skill is not about naming conventions or architectural quality — those belong in `token-audit`. This skill is about structural integrity: can the file be parsed, transformed, and consumed by downstream tools without error?

## Boundaries

This skill validates token file structure only. It does not assess naming quality (use `naming-audit`), token architecture health (use `token-audit`), or token usage in code (use `token-compliance`). If the token source format is not recognisable as DTCG, Style Dictionary, Tokens Studio, or a declared custom schema, ask the user to identify the format before proceeding. If no token files are provided or accessible, there is nothing to validate — stop and confirm the file location with the user.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `system.token_format` — pre-selects the primary format to validate against (dtcg, style-dictionary-v3, style-dictionary-v4, tokens-studio, custom)
- `integrations.style_dictionary` — if enabled, use Style Dictionary's built-in validation as a cross-check
- `severity.schema_*` — overrides for finding severity (e.g. `schema_missing_type: critical`)

## Auto-pull integrations

**Run the tool the repo already has, first.** Hand-validation is the fallback, not the method.
- **Style Dictionary 4 or 5** (`integrations.style_dictionary.enabled: true`, or a config file in the repo): run `npx style-dictionary build --config [path]` into a scratch output directory to get its own reference and parse errors. Version 5 reads DTCG natively; version 4 needs `usesDtcg: true`; version 3 uses `value`/`type` and doesn't read DTCG at all.
- **Terrazzo** (a `terrazzo.config.*` file, or `@terrazzo/cli` in `package.json`): run `npx terrazzo lint` for DTCG validation and `npx terrazzo build` for alias resolution.
- Reconcile: every error the tool reports appears in this report with the tool named as its source; anything this skill finds that the tool didn't is reported as this skill's own check.

---

## Step 1: Identify files and target format

Ask for or confirm:

1. **Path to token files** — directory or specific files to validate
2. **Target format** — which specification to validate against:
   - **DTCG 2025.10** (W3C Design Token Community Group specification)
   - **Style Dictionary v3** (legacy JSON with `value` property)
   - **Style Dictionary v4 or v5** (JSON with DTCG alignment, `$value` property; v5 reads DTCG natively)
   - **Tokens Studio** (Figma Tokens plugin export format)
   - **Custom** — if custom, ask for the schema or describe the expected structure
3. **Strictness level** — strict (every violation is an error) or lenient (warnings for non-critical issues)

If the token files contain format indicators (e.g., `$type` fields suggest DTCG), auto-detect the format and confirm with the user.

## Step 2: Parse and inventory

For each file in the provided path:

1. **Attempt to parse** — JSON, YAML, JS module, or CSS custom properties
2. **Record parse status** — parsed successfully, failed with error, or empty file
3. **Count tokens** — total token definitions found
4. **Identify format signals** — which format the file appears to use (based on property names, structure)

Produce the file inventory:

| File | Format detected | Tokens | Parse status |
|------|----------------|--------|-------------|
| colors.json | DTCG 2025.10 | 47 | ✅ Parsed |
| spacing.json | Style Dictionary v3 | 12 | ✅ Parsed |
| broken.json | Unknown | 0 | ❌ Parse error: unexpected token at line 23 |

Figures in this and later examples are illustrative.

## Step 3: Validate against target format

For each successfully parsed file, run format-specific validation:

### DTCG 2025.10 checks

1. **$value required** — every leaf token must have a `$value` property
2. **$type resolvable** — resolve each token's type in order: its own `$type`; if its value is an alias, the resolved type of the target; otherwise the closest parent group's `$type`. Flag only tokens with none of these.
3. **$type values valid** — must be one of the 13 DTCG 2025.10 types listed in the token-architecture note. `fontStyle` is not a type.
4. **$description optional but typed** — if present, must be a string
5. **Alias syntax correct** — aliases must use `{group.token}` syntax with curly braces
6. **Alias targets exist** — every alias must resolve to a real token (no broken references)
7. **No circular aliases** — alias chain must terminate at a concrete value
8. **Composite token structure** — the six composite types (strokeStyle, border, shadow, typography, transition, gradient) must have correct sub-properties; `strokeStyle` also accepts a plain keyword such as `"dashed"`
9. **Value shapes** — in 2025.10, `color` is an object (`colorSpace`, `components`, optional `alpha` and `hex`), `dimension` is `{ value, unit }` with `px` or `rem` only, and `duration` is `{ value, unit }` with `ms` or `s` (see the token-architecture note). String values such as `"#ff0000"` or `"16px"` are the older draft format: report them as a migration item, not a broken file.
10. **Units valid** — `em`, `%` and other units in a `dimension` are outside the spec; flag them
11. **No `$` prefix on non-spec properties** — custom properties should not start with `$` to avoid confusion with spec properties
12. **Extensions namespace** — custom metadata should live under `$extensions` if present, keyed by reverse-domain name
13. **Name rules** — token and group names must not begin with `$` and must not contain `{`, `}` or `.`; a dotted name breaks alias syntax and is an error, not a style point
14. **`$deprecated`** — if present, must be `true`, `false` or a string; a group's value applies to its children unless a token overrides it

### DTCG 2025.10 resolver checks

For every `*.resolver.json`:
1. **`version`** must be the string `"2025.10"`
2. **`sets`** is a map of named sets, each with an array of token sources (inline objects or file paths); every file path resolves
3. **`modifiers`** is a map; each modifier has a required `contexts` map of name → array of token sources, and an optional `default` that names one of its contexts
4. **`resolutionOrder`** is present and every entry names an existing set or modifier, each at most once
5. **Alias targets** in any source resolve somewhere earlier in the resolution order
6. A context that doesn't redefine a token is inheritance, not an error; don't report it here (`theme-audit` decides whether an inherited theme-dependent token is a gap)

### Style Dictionary v3 checks

1. **`value` required** — every leaf token must have a `value` property (not `$value`)
2. **Reference syntax** — aliases use `{group.token}`; the older `{group.token.value}` form is also accepted
3. **Reference resolution** — all references resolve to existing tokens
4. **Category-Type-Item (CTI)** — if using CTI convention, validate hierarchy consistency
5. **No reserved property collisions** — `value`, `original`, `name`, `comment`, `themeable`, `attributes`, `path`, `filePath` and `isSource` are reserved

### Style Dictionary v4 and v5 checks

v4 still accepts the legacy `value`/`type` format; v5 reads DTCG natively and treats `usesDtcg` as on. Apply the DTCG checks above only when the project opts into DTCG format (e.g. `usesDtcg`, or its files use `$value`); otherwise apply the v3 checks. Plus:
1. **Format consistency** — a file doesn't mix `$value` and `value` tokens
2. **Preprocessor compatibility** — if preprocessors are configured, validate custom property shapes
3. **Platform-specific overrides** — if present, validate they follow the platform config schema

### Tokens Studio checks

1. **Group hierarchy preserved** — nested groups maintain parent-child relationships
2. **Token types valid** — type field matches the Tokens Studio type set, including color, dimension, number, boolean, text, asset, border, typography, borderRadius, sizing, spacing, opacity, borderWidth, boxShadow, fontFamilies, fontWeights, lineHeights, fontSizes, letterSpacing, paragraphSpacing, textDecoration, textCase, composition, and other. Check the plugin version's docs before flagging an unfamiliar type
3. **Math expressions valid** — if tokens use math expressions (`{size.base} * 2`), validate syntax
4. **Reference syntax** — uses `{group.token}` without `.value` suffix
5. **Set structure** — if multi-set, validate set names and token assignments
6. **Theme configuration** — if themes are defined, validate theme-to-set mappings

## Step 4: Cross-format consistency

If files use multiple formats (common during migration):

1. **Identify format boundaries** — which files are which format
2. **Flag inconsistencies** — same token in two formats with different values
3. **Migration readiness** — if migrating from v3 to DTCG, how many files still need conversion

## Step 5: Produce the validation report

Structure the report as:

```
# Token Schema Validation Report

[Headline sentence: how many files are valid, and the most serious problem to fix first]

## Summary
- Files scanned: X
- Files valid: Y
- Files with errors: Z
- Target format: [DTCG 2025.10 / Style Dictionary v3 / etc.]
- Strictness: [strict / lenient]

## File Inventory
[Table from Step 2]

## Validation Results

### ✅ Valid Files
[List each valid file with token count]

### ❌ Files with Errors

#### [filename.json]
| # | Check | Severity | Evidence | Detail | Fix |
|---|-------|----------|----------|--------|-----|
| SV-01 | $type resolvable | 🟠 High | `colors.json:14,31,58` | 3 tokens have no own, alias-derived, or group `$type`: `color.brand.accent`, `spacing.page.gutter`, `font.body.family` | Add `$type: "color"`, `$type: "dimension"`, `$type: "fontFamily"` respectively, or set `$type` on the parent group |
| SV-02 | Alias resolution | 🔴 Critical | `semantic.json:22` | `{color.legacy.blue}` referenced by `color.semantic.info` does not exist | Either create `color.legacy.blue` or update the reference to `{color.primitive.blue.500}` |

Severity: 🔴 Critical for a parse error or a broken alias (the build fails, or a value silently resolves to nothing); 🟠 High for an unresolvable `$type`, an invalid unit, a circular alias, or a name that breaks alias syntax; 🟡 Medium for pre-2025.10 string values and mixed formats in one file (migration items); ⚪ Low for a missing `$description` or a non-`$` custom property. Evidence is the file and line where the parser or the check found the problem.

### ⚠️ Warnings
[Non-critical issues: missing $description, custom $ properties, etc.]

## Format compliance
- [Counts, e.g. "10 of 12 files valid; 3 tokens with no resolvable $type; 1 broken alias"]
- [If migrating] Legacy tokens remaining: N files, M tokens (e.g. string colour values still to convert)

## Recommendations
[Prioritised list of fixes, grouped by: parse errors first, then broken references, then missing declarations]

**Scope**
- **Inspected:** [files and directories parsed]
- **Not inspected:** [files skipped, formats not recognised, build config not run]
- **How "none found" was checked:** [e.g. every alias resolved against the parsed token tree — N aliases in total — so "no broken aliases" covers all of them]
- **Assumptions:** [target format, strictness level]

If any of these are deliberate (e.g. string colour values kept for a tool that can't read the object form yet), tell me and I'll skip them in future runs.
```

## Step 6: Produce machine-readable output (optional)

If the user requests it or if the output will feed into another tool:

```json
{
  "format": "dtcg-2025.10",
  "files_scanned": 12,
  "files_valid": 10,
  "files_invalid": 2,
  "findings": [
    {
      "id": "SV-01",
      "file": "colors.json",
      "token": "color.brand.accent",
      "check": "$type_required",
      "status": "FAIL",
      "fix": "Add $type: \"color\""
    }
  ]
}
```

---

## Quality checks

Before delivering the report, verify:

1. **Every file in the path was scanned** — no files skipped without explanation
2. **Parse errors include line numbers or error positions** — not just "invalid JSON"
3. **Fix suggestions are specific and copy-pasteable** — not "add the missing type" but "add `$type: \"color\"` to token `color.brand.accent`
4. **Counts are facts, not ratings** — report "10 of 12 files valid", never a compliance percentage or score; checks that don't apply (e.g. no composite tokens) are left out
5. **Alias chains are fully traced** — broken reference errors identify the full chain, not just the immediate reference
6. **Cross-format issues are flagged** — if the same token exists in two files with different formats, this is noted
7. **Findings reference specific token names and file paths with line numbers** — never "some tokens are missing types"
8. **The repo's own tool ran first** where one exists, and its errors are in the report with the tool named

## Small-system note

For systems with fewer than 5 token files: run the same validation but present results as a single-page summary rather than a per-file breakdown. Include the specific fix for every single issue rather than grouping by pattern.
