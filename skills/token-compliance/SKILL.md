---
name: token-compliance
description: "Find hardcoded colour, spacing and type values and wrong-tier token references in consuming code. Trigger: find hardcoded values, any hex in the code, are we using tokens correctly, token compliance. Do NOT use for token definitions — token-audit; token file format — schema-validator."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(grep:*), Bash(rg:*), Bash(git log:*), Bash(git blame:*)
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Token compliance

A skill for identifying token compliance violations in a codebase or implementation: hardcoded raw values where tokens should be used, wrong-tier token references, and inconsistent token application. Produces a violation report with file references and remediation guidance.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Token compliance problems compound quietly. A single hardcoded hex value does not break anything. Two hundred of them, distributed across a codebase by dozens of contributors over two years, mean that a brand refresh or a dark mode implementation becomes a manual find-and-replace operation through thousands of files rather than a token update.

The compliance check exists to catch violations before they accumulate, and to understand the pattern of violations when they already have. The pattern matters: if hardcoded values are concentrated in one product area or one team's contribution, the response is different than if they are evenly distributed.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `severity.*` — overrides for violation severity. Especially: `hardcoded_color`, `wrong_tier_reference`, `tier_leakage`
- `system.theming` — if true, elevate hardcoded colour violations to the configured severity (typically `critical`)
- `system.styling` — pre-selects the detection approach
- `integrations.github` — the repo to check out and search (see below)
- `integrations.style_dictionary` — the parsed token tree, as the reference for what tokens exist and their correct tiers
- `gates.*` — when running as part of `component-to-release`, which violations block release

## Auto-pull integrations

**GitHub** (`integrations.github.enabled: true`):
- Search a local checkout of `integrations.github.repo`, not GitHub's code search API (see the note's GitHub caution): code search drops `#`, so a colour search there returns nothing and reads as clean.
- Broad colour search before the manual checks:
  ```bash
  rg -n --glob '*.{css,scss,less,ts,tsx,js,jsx,vue}' --glob '!**/tokens/**' --glob '!**/{dist,node_modules}/**' \
    '#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|oklch\('
  ```
  Without ripgrep: `grep -rnE --include='*.css' --include='*.scss' --include='*.tsx' [etc.] --exclude-dir=tokens --exclude-dir=node_modules --exclude-dir=dist '<same pattern>' .` Adjust the globs to where tokens actually live. Expect some false positives (CSS ID selectors such as `#add` or `#faded`) and weed them out by hand.
- **Positive control:** run the same pattern over the token source files. It must find hits there before a zero anywhere else is reported as zero. If it finds nothing in the token source either, the pattern doesn't fit this codebase — say the result is unconfirmed.
- Search for `px` values in styling files as a spacing compliance signal
- Use the results to quantify scope before the detailed audit — "approximately 340 hardcoded hex values across 47 files" (illustrative figures) is a useful framing for the report summary

**Style Dictionary v4** (`integrations.style_dictionary.enabled: true`):
- Parse the token tree to build a complete map of available tokens per tier
- Use this as the authoritative "what token should this reference?" lookup when flagging violations
- If a hardcoded value exactly matches a known token's resolved value, include the token name in the remediation guidance automatically

**Figma MCP** (`integrations.figma.enabled: true`):
- Pull Figma variable definitions as a cross-reference — if a colour is defined as a Figma variable but hardcoded in code, that is a compliance violation with a known correct token

## Step 0b: Messy codebase protocol

Token compliance has the most value on messy codebases — the ones with years of accumulated hardcoded values, inconsistent styling approaches, and multiple token migration attempts. For these codebases, apply the extended detection protocol:

**Indicators of a messy codebase:**
- Multiple styling approaches in the same project (CSS custom properties AND SCSS variables AND inline styles)
- Token files exist but significant portions of the codebase pre-date them
- Multiple naming conventions visible in style files (camelCase, kebab-case, BEM — mixed)
- Legacy colour palettes coexisting with current tokens
- Inline `style=` attributes in component templates

**Extended detection for messy codebases:**

1. **Legacy value mapping.** Before flagging violations, build a map of legacy values to current tokens. Many hardcoded values in legacy code were correct at the time they were written — they pre-date the token system. Map `#0066CC` to `var(--color-action-primary)` so remediation guidance is specific, not just "use a token."

2. **Violation age estimation.** Use `git log -S'<value>' -- <file>` (the commit that introduced the value) or `git blame -w -C` to estimate when violations were introduced. Plain `git blame` and file modification dates point at the last reformat or file move, not the original author — check for bulk formatting commits before trusting a date. Group violations by era:
   - **Pre-token era** (before the token system existed) — these are expected debt, not compliance failures
   - **Migration era** (during token adoption) — partially migrated files where some values use tokens and others do not
   - **Post-token era** (after tokens were established) — these are genuine compliance failures and should be higher severity

3. **Hotspot detection.** Identify the 5–10 files with the most violations. These are the high-value remediation targets — fixing them reduces the violation count disproportionately. Present as:
   ```
   Compliance hotspots (illustrative):
   1. src/legacy/checkout/styles.scss — 47 hardcoded values (pre-token era)
   2. src/components/Card/Card.styles.ts — 23 hardcoded values (migration era)
   3. src/pages/Dashboard/index.tsx — 19 inline styles (post-token era — PRIORITY)
   ```

4. **Intentional override detection.** Not every hardcoded value is a violation:
   - Values with comments like `/* override */` or `/* intentional */`: list them separately as "Marked intentional in code", with the comment, so the team can confirm.
   - Values that match no token are still violations, logged once in the violation log with their severity like any other. In the Correct token column, write "none — nearest: `<token>`" and mark the row off-system in Notes: the value may be a one-off design requirement or a gap in the scale, and the team should decide which, not the tool.

---

## Step 1: Define the scope and access

Ask for or confirm (skip questions already answered by auto-pull):
- What is being assessed? (Full codebase, specific product area, specific component set)
- Access to the implementation: codebase, Figma file, Storybook, or described properties
- The token system in use: what tokens exist, what tiers are defined, and how tokens are consumed in code
- The styling approach: CSS custom properties (`var(--token)`), SCSS variables (`$token`), Tailwind utility classes, CSS-in-JS theme objects, or a mix
- Any known compliance hotspots the check should prioritise
- Whether this is a baseline audit or a follow-up to a previous check
- **Codebase age and migration history:** When were tokens introduced? Has there been a previous migration? Are there known legacy areas? (This determines whether the messy codebase protocol applies.)

**Styling approach matters for how violations are detected:**

- **CSS custom properties:** Token references look like `var(--color-action-primary)`. Hardcoded values are raw hex/rgb/px values outside of `var()`.
- **SCSS variables:** Token references look like `$color-action-primary` or `map-get($tokens, 'action-primary')`. Hardcoded values are raw literals not using `$` variables.
- **Tailwind utility classes:** Token references are utility classes that map to the design system's Tailwind config (e.g. `bg-primary`, `text-color-content-default`, `gap-4`). These are NOT hardcoded values — they are token references expressed as utility classes. Hardcoded values in Tailwind are arbitrary value brackets: `h-[12px]`, `bg-[#ff0000]`, `p-[7px]`. Flag arbitrary values as violations; do not flag standard utility classes that resolve to configured tokens.
- **CSS-in-JS (Emotion, styled-components):** Token references look like `theme.colors.action.primary` or `tokens.spacing[4]`. Hardcoded values are raw literals in style objects.

**Framework-specific detection notes:**

- **If using Vue SFC:** Token violations appear inside `<style lang="scss" scoped>` blocks. Look for raw `px` values where `$token` variables or `var(--token)` should be used. Vue's scoped styles may also contain token references via `v-bind()` for dynamic CSS — these are valid token usage if bound to a token-backed prop.
- **If using Twig/Fractal:** Token violations appear as inline `style=""` attributes in templates (e.g. `style="background-color: {{ item.color }}"`), hardcoded hex values in SVG `fill`/`stroke` attributes, and raw pixel values in HTML dimension attributes. Twig components typically reference tokens via BEM utility classes — audit the SCSS that backs those classes, not just the template.
- **If using Emotion/styled-components with TypeScript tokens:** Token references look like `theme.colors.primary`, `theme.spacing(4)`, or `theme.typography.body`. Hardcoded violations are string literals in style objects: `color: '#FF0000'`, `padding: '16px'`. Tokens accessed via the codebase's own helper functions (e.g. `theme.spacing(4)`) are valid token usage — find those helpers first so they aren't flagged.

## Step 2: Run the compliance checks

**Excluded from all checks:** token source files, generated CSS (build output), SVG assets, and stories/test fixtures. Say in the Scope block which paths were excluded.

**Exempt values, everywhere:** `transparent`, `currentColor`, `inherit`, `none`, and CSS-wide keywords (`initial`, `unset`, `revert`). These are never violations.

### Check 1: Hardcoded colour values

Find and flag all colour values that are not token references:
- Hex values (e.g. `#0066CC`, `#FFF`)
- RGB and RGBA values (e.g. `rgb(0, 102, 204)`, `rgba(0,0,0,0.5)`)
- HSL values
- Named colour values (e.g. `red`, `white`) — the exempt keywords above excepted

For each finding: file reference or context, the raw value found, and the token it should reference.

If the assessment is conducted against a design file rather than code: look for any colour styles applied as raw values rather than library styles.

### Check 2: Hardcoded spacing values

Find and flag spacing values that are not token references:
- Raw pixel values in padding, margin, gap, width, or height properties (e.g. `padding: 16px`, `gap: 8px`)
- Rem values that correspond to spacing scale values (e.g. `1rem` when there is a spacing token for `16px/1rem`)
- Percentage values where a spacing token would be more appropriate

Note: not all pixel values are compliance violations. Border widths, minimum touch targets, and other fixed dimensions may be intentionally hardcoded. Where intent is ambiguous, log it as ⚪ Low and say why.

### Check 3: Hardcoded typography values

Find and flag typography values that are not token references:
- Raw font-size values (e.g. `font-size: 14px`)
- Raw font-weight values (e.g. `font-weight: 700`)
- Raw line-height values (e.g. `line-height: 1.5`)
- Raw font-family values (e.g. `font-family: 'Inter', sans-serif`)
- Raw letter-spacing values

### Check 4: Wrong-tier token references

Find and flag component-level code that references primitive tokens directly rather than routing through semantic tokens:

Violation example: `background-color: var(--color-blue-500)` in a button implementation
Should be: `background-color: var(--color-action-primary)` → `var(--color-blue-500)`

This is the subtlest compliance violation and the most architecturally damaging. It appears correct on the surface — the right colour is being used — but it breaks the semantic contract and means a semantic change (e.g. changing what "action primary" means) does not propagate to the component.

For each finding: the token being referenced, the semantic token that should be used instead, and the context.

### Check 5: Inconsistent token application

Find and flag cases where the same visual property is implemented differently across components or contexts:
- The same semantic role implemented with different tokens in different components (e.g. `color.action.primary` in some places, `color.brand.500` in others, for the same role)
- The same spacing context using different spacing tokens across similar components
- Interactive states (hover, focus, active) implemented differently across components that should share the same token

These violations are often invisible in a per-component review but surface clearly when components are compared.

## Step 3: Produce the violation report

---

### Token compliance report

Open with a headline sentence that tells the reader the overall state and where to focus.

**Date:** [date]
**Scope:** [what was assessed]
**Assessment method:** [codebase / design file / Storybook / described properties]

---

#### Summary

Overall compliance picture. What is the most significant finding? Is the violation pattern concentrated or distributed?

---

#### Violation counts

| Check | Violations found | 🔴 Critical | 🟠 High | 🟡 Medium | ⚪ Low |
|---|---|---|---|---|---|
| Hardcoded colour values | | | | | |
| Hardcoded spacing values | | | | | |
| Hardcoded typography values | | | | | |
| Wrong-tier token references | | | | | |
| Inconsistent token application | | | | | |
| **Total** | | | | | |

---

#### Violation log

Group by check type. For each violation:

| ID | Check | Severity | Location | Raw value / incorrect reference | Correct token | Notes |
|---|---|---|---|---|---|---|
| TC-01 | Colour | 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low | [file path or context] | `#0066CC` | `var(--color-action-primary)` | |

Each value appears once. Off-system values (no matching token) stay in this table with their severity; put "none — nearest: `<token>`" in the Correct token column and "off-system" in Notes. Don't repeat them in a separate list.

**Excluded as structural:** one line listing the values left out and why — e.g. `max-width: 960px` (layout container), `border: 1px solid` (divider), test-wrapper padding. Don't log these as violations.

---

#### Context-aware violation severity

Not all violations carry equal weight. Adjust severity based on component importance. This is the feature that distinguishes a compliance check from a simple grep — without context-aware severity, every violation looks the same.

**Elevated severity (upgrade one level):**
- Violations in components on critical user paths (checkout, authentication, primary navigation)
- Violations in components with high fan-in (used by 5+ other components — from the component-audit dependency graph)
- Violations in components that are theming-sensitive (brand-facing surfaces, dark mode targets)
- Violations in post-token-era code (introduced after the token system was established — these are active compliance failures, not inherited debt)

**Standard severity:**
- Violations in general-purpose components with moderate usage
- Violations in migration-era code (partially migrated — compliance improvement is in progress)

**Reduced severity (downgrade one level):**
- Violations in internal/utility components not directly user-facing
- Violations in components that are already scheduled for deprecation
- Violations in legacy code areas with a known migration timeline
- Violations in pre-token-era code (introduced before the token system existed — these are expected debt)
- Layout utilities that use raw pixel values for structural concerns unrelated to design tokens (e.g., `max-width: 1200px` for a container, `height: 1px` for a divider) — not violations; list them on the "Excluded as structural" line

Apply the adjustment after the initial severity assignment. Note the adjustment and reason in the violation log — "Severity upgraded from Medium to High: component is on the checkout critical path."

#### Pattern analysis

Step back from individual violations and describe the pattern:
- Are violations concentrated in specific files, components, or product areas?
- Are there recurring raw values that appear frequently and clearly correspond to a specific token?
- Is there a particular check type that dominates the violation count?

Pattern analysis turns a violation log into actionable intelligence. "Hardcoded spacing violations are concentrated in the legacy product area — likely pre-dates the token system" leads to a different response than "hardcoded spacing violations are evenly distributed and increasing — the token system is not being adopted."

---

#### Remediation priority

**Immediate:** Wrong-tier token references and any hardcoded values that would break under theming or brand change. These have architectural impact.

**Planned:** Consistent hardcoded values that correspond clearly to existing tokens. These can be resolved in a systematic pass.

**Review:** Ambiguous values (raw percentages, context-dependent px values, intentional overrides). These need human judgment before remediation.

---

#### Remediation approach

Recommend the most efficient approach for the volume and pattern of violations found:

- If violations are high-volume and repetitive: a migration script or codemod is more efficient than manual correction
- If violations are concentrated in a specific area: a focused refactoring sprint on that area
- If violations are sparse and distributed: add to the team's ongoing code review criteria and address as work touches each area
- If wrong-tier references are significant: a token architecture review may be warranted before remediation to ensure the semantic tier is complete enough to reference correctly

---

**Scope**
- **Inspected:** [directories and file types searched]
- **Not inspected:** [excluded paths — token source, generated CSS, SVG assets, stories/fixtures — and anything out of reach]
- **How "none found" was checked:** [for any check reporting zero, the positive control: the same pattern found hits in the token source]
- **Assumptions:** [e.g. the token tree used as the reference is current]

If any of these values are deliberate (a one-off the design called for, or a legacy area you've accepted), tell me and I'll exclude them in future runs.

---

Token definitions are out of scope for this skill: for DTCG format and alias integrity use schema-validator; for tier structure and cross-system consistency use token-audit.

## Quality checks

- All five checks are covered
- Wrong-tier references are checked separately from hardcoded values — they are a different category of violation
- Pattern analysis section exists and describes the distribution of violations, not just the total
- Remediation priority distinguishes between architectural violations and surface-level ones
- The report is specific enough to act on: file references or context for each violation, not just "hardcoded values found"
- Any zero count is backed by a positive control against the token source
- Exempt keywords and excluded paths are never logged as violations
- The report ends with the Scope block and the invitation to flag deliberate values
