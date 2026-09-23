---
name: theme-audit
description: "Audit theme parity: tokens missing or unchanged per theme, component tokens bypassing semantics, contrast within each theme, resolver modes, theme-switch regressions. Triggers: dark mode audit, theme coverage, brand variant parity. For general token structure use token-audit."
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Theme audit

A skill for auditing theme coverage and visual consistency across multiple design system themes. Identifies tokens missing from specific themes, component tier propagation failures, internal consistency violations within each theme, DTCG resolver coverage gaps, and components likely to break on theme switches. Produces a theme coverage report with severity-rated findings.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Theming is where the three-tier token architecture proves its value or reveals its failures. When a system switches themes correctly, the change ripples through every component that references the semantic tier. When it does not — when components hardcode primitives or when the semantic tier is incomplete — a theme switch becomes a hunt through hundreds of files for missed overrides.

A theme audit is not about validating a single theme's visual appearance. It is about ensuring every token consumed by every component exists and is correctly defined across every theme the system claims to support. It is about catching cases where the component tier skips the semantic tier entirely, making theme switches invisible to that component.

The audit surfaces three categories of problems: coverage gaps (token defined in Theme A but not Theme B), architectural failures (component tokens that bypass the semantic tier), and internal consistency breaks (within a single theme, visual logic is violated — e.g. in dark mode, a raised surface that's darker than the base background, which reads as sunken).

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:

- `system.theming` — if false, exit early with a note that this skill applies only to systems with theming enabled. If true, proceed.
- `severity.*` — overrides for theme-specific findings (e.g. `missing_theme_value: critical` for a system about to launch dark mode)
- `integrations.style_dictionary` — parse tokens via Style Dictionary v4 to extract all semantic and component tokens and their resolver-defined mode values
- `integrations.figma` — Figma variables and their modes as the theme source
- `recurring.*` — the previous theme audit, for trend comparison

## Step 0: Theme discovery and scope

Before auditing, discover what themes the system actually defines:

**Discover themes:**
1. **Resolver files** — if DTCG format, scan the project for `.resolver.json` files and extract mode names (e.g. `light`, `dark`, `brand-a`, `brand-b`)
2. **CSS custom property scopes** — if using CSS variables, scan for theme selectors like `:root`, `.dark`, `[data-theme="light"]`, `[data-theme="dark"]`, `[data-brand="brand-a"]` — each scope is a theme variant
3. **SCSS variable maps** — if using SCSS, look for `$themes: (...)` or separate theme files (`_theme-light.scss`, `_theme-dark.scss`)
4. **JavaScript theme objects** — if using CSS-in-JS, look for exported theme objects or theme switching functions (e.g. `export const lightTheme = { ... }; export const darkTheme = { ... }`)
5. **Tailwind mode declarations** — check `tailwind.config.js` or `tailwind.config.ts` for `darkMode` configuration and any theme extends
6. **Figma modes** — if Figma integration is configured, list all variable modes in the linked file

**Present discovered themes to user:**

Produce a brief inventory:
```
Themes discovered:
- Light (default, CSS root scope, Figma mode)
- Dark (CSS .dark scope, Figma mode)
- Brand A (data-theme="brand-a" scope)
- Brand B (data-theme="brand-b" scope)
Total: 4 themes
```

Ask: "I found these [N] themes. Should I audit all of them, or focus on specific variants?"

If no themes are discovered and theming is marked as `true` in config, ask the user to name the themes they intend to support.

## Step 1: Identify tokens in scope

Gather the semantic and component tiers across all discovered themes:

**For DTCG format:**
- Parse resolver files and extract all semantic tokens and their mode-specific values
- Extract all component tokens and their mode-specific values
- Verify that every token in every set has values defined for every declared mode

**For CSS custom properties:**
- Extract `:root` (or default theme scope) as the reference set of all semantic tokens
- Extract theme-scoped selectors (`.dark`, `[data-theme="dark"]`, etc.) and their token definitions
- Map which tokens are defined in each scope

**For SCSS variables:**
- Extract variables from the base/default theme file as the reference set
- Extract variables from each theme file
- Identify which variables are redefined per theme

**For JavaScript theme objects:**
- Extract the reference theme object's keys as the token inventory
- For each theme variant, identify which tokens are redefined

**For Tailwind:**
- Extract `theme` and `darkMode` blocks
- Identify which theme values are overridden in each mode
- Note which breakpoints or variants redefine token values

Output a token inventory (figures illustrative). With CSS scopes, SCSS theme files and JS theme objects, a token not redefined in a theme inherits the default — "not overridden" is not the same as "missing":
```
Semantic tokens: 156 total
- Overridden in every theme: 118
- Inherit the default in one or more themes: 34 (fine for spacing, radius, type; check colour and shadow)
- Defined only in a non-default theme scope: 4 (undefined in the default theme — a real gap)

Component tokens: 287 total
- Defined in all themes: 278
- Coverage gaps: 9
```

This checkpoint reveals the scale of coverage problems before the detailed audit.

## Step 2: Theme coverage check

Inheriting the default is correct for tokens that shouldn't change between themes — spacing, radius, font sizes, durations usually don't. Flag only:
- **Theme-dependent tokens that aren't themed** — colour, shadow, border colour, and anything else the theme is meant to change, which inherit the default (CSS/SCSS/JS) or hold the same value as the default (resolver modes, Figma modes). A dark theme inheriting the light `--color-text-default` is a real gap
- **Tokens undefined in some theme** — defined only in a non-default scope, or missing a value for a declared resolver mode, so they don't resolve at all there

If the team has said a token is deliberately the same across themes (a fixed brand colour), treat it as accepted.

**Coverage matrix:**

Show only the rows with a gap — not every semantic token. Columns are themes. Mark each cell as:
- ✓ Themed (token has its own value in this theme)
- ↳ Inherits default (flag only if the token is theme-dependent)
- ✗ Undefined (token doesn't resolve in this theme)

**Summarise gaps per theme (figures illustrative):**

```
Dark theme: 4 theme-dependent tokens not themed (--color-feedback-info, --color-feedback-warning, --color-border-subtle, --shadow-raised)
Brand A: 2 not themed (--color-feedback-warning, --color-action-secondary); 1 undefined (--text-heading-display)
Brand B: no gaps
```

For each gap, flag:
- Finding ID (e.g. TC-01)
- Severity: 🔴 Critical if the token is undefined in a shipped theme, or a component token consumes it without its own per-theme override; 🟠 High if used by multiple components; 🟡 Medium if used by few components; ⚪ Low if no in-repo consumers were found
- Description: Semantic token [name] is not defined in [theme]
- Impact: Which components depend on this token and may render incorrectly
- Recommended action: Define the token in the missing theme. If the token should not apply to this theme, document that decision.

## Step 3: Component tier propagation check

Verify that component tokens correctly inherit from the semantic tier across all themes:

**For each component token:**
1. Trace its reference — does it point to a semantic token, or to a primitive?
2. If it points to a primitive: this is tier leakage. The component token bypasses theming.
3. If it points to a semantic token: verify that the semantic token has values defined in all themes where the component is used.

**Tier leakage detection:**

Flag any component token that references a primitive (rather than a semantic token):

```
TC-10 | 🔴 Critical | Tier leakage | button.background.default references {color.blue.500} (primitive) instead of semantic tier, with no per-theme override
- Impact: Button background will not change on theme switch (dark mode will show blue on blue)
- Recommended action: Redefine as button.background.default: {color.action.primary}
```

Quantify the scope:
```
Component tokens examined: 287
- Correctly reference semantic tier: 276
- Tier leakage (reference primitives): 11
```

Tier leakage is the most dangerous category of theme bug — everything appears to work until someone activates a new theme. It's 🔴 Critical only when the component token isn't itself overridden per theme. If each theme sets its own value for the component token, theming works; the leakage is then a 🟡 Medium maintenance finding (every new theme has to remember that override).

## Step 4: Visual consistency check within each theme

For each theme, validate internal logical consistency:

**Consistency rules (apply per theme, not across themes):**

For every theme, compute contrast from resolved values (follow aliases to the final colour in that theme) rather than judging by name. The baseline is WCAG 2.2 AA: 4.5:1 for body text, 3:1 for large text and for non-text elements such as borders, focus indicators and icons. (Some legal baselines, e.g. EN 301 549, still reference WCAG 2.1 AA; use that if it's the team's obligation.)

For **light theme:**
- Raised surfaces are usually lighter than or equal to the page background, separated by border or shadow
- Text colours meet the contrast baseline against the backgrounds they're used on
- Action colours should be visually distinct from neutral colours
- Hover states should be visually different from default states (e.g. darker, not lighter)

For **dark theme:**
- Raised surfaces should be lighter than the base background — elevation reads as lightness in dark themes, since shadows barely show. A surface darker than the background reads as sunken
- Text colours meet the contrast baseline against dark backgrounds
- Action colours may need adjustment to maintain contrast in dark mode

For **brand variants:**
- Primary action colour should be consistent with brand guidelines
- Secondary actions should be visually subordinate to primary actions
- Error/warning/success states should be visually distinct from brand primary

**Consistency violations to flag:**

Run visual spot-checks on high-impact token groups:
- Does `color.feedback.error` meet 4.5:1 (as text) or 3:1 (as an icon or border) against `color.background.default` in this theme, computed from resolved values?
- Are `color.surface.primary` and `color.background.default` visually distinct (same value is sometimes OK, but should be documented as intentional)?
- Is `color.action.primary` visually more prominent than `color.action.secondary` in this theme?

Flag violations:
```
TC-22 | 🟡 Medium | Consistency | Dark theme: color.background.default and color.surface.primary are identical (#121212)
- This may be intentional (both are neutral backgrounds), but it reduces visual hierarchy
- Recommended action: Review with design team. If intentional, document the decision. If not, adjust surface token.
```

## Step 5: DTCG resolver validation

If the system uses DTCG format with resolver files:

**Resolver file structure check:**
1. Verify `.resolver.json` files exist and are well-formed JSON
2. Extract the `sets` and `modes` blocks
3. Verify that every semantic token listed in `sets` has a value defined for every declared `mode`

**Mode coverage per token:**

For each semantic token:
```
color.action.primary:
  light: {color.blue.500}    ✓
  dark:  {color.blue.300}    ✓
  brand-a: {color.purple.600}  ✓
  brand-b: [missing]         ✗
```

Flag missing mode values:
```
TC-30 | 🔴 Critical | Resolver coverage | color.action.primary missing value in brand-b mode
- When brand-b theme is active, color.action.primary will resolve to light mode default (fallback)
- Recommended action: Add mode-specific value to brand-b mode in resolver
```

**Set composition check:**
- Verify that all semantic tokens are included in at least one resolver set
- Identify tokens declared in token files but not included in any resolver set
- If component tokens exist, verify they are composed into the same resolver sets as their semantic dependencies

Tokens outside every resolver set are maintenance burden — they appear in IDE autocomplete but produce no runtime value.

## Step 6: Theme switching regression check

Identify patterns in the codebase that are likely to break on theme switch:

**Regression patterns:**

Search for common failures:

1. **Hardcoded values in component code** — even if tokens exist, if components use raw colours/spacing instead of tokens, theme switches are invisible to those components
2. **Opacity hacks** — `rgba(var(--color-action-primary), 0.5)` only works if the token holds bare RGB channels (`37, 99, 235`). If it holds a hex or `rgb()` value, as most colour tokens do, the declaration is invalid and silently dropped. Check what each referenced token actually holds in every theme
3. **CSS calc() on token values** — `padding: calc(var(--spacing-component-gap) * 2)` works when the token carries units (`16px * 2` is `32px`). It fails when a theme defines the token as a unitless number, because the result isn't a length. Check that every theme gives these tokens units
4. **Inline styles with theme assumptions** — `style={{ backgroundColor: isDark ? darkColor : lightColor }}` is not using the token system at all
5. **Missing component variants for theme-specific rendering** — some components may need different structures or properties per theme (e.g. borders visible in dark mode but not light)

**Regression output:**

Flag high-risk patterns:
```
TC-40 | 🟠 High | Regression | Found 23 instances of hardcoded hex values in component code
- These will NOT change on theme switch even though token values exist
- Recommended action: Replace hardcoded values with token references

TC-41 | 🟡 Medium | Regression | Found 7 instances of rgba(var(--token), alpha) where the token holds a hex value
- The declaration is invalid, so the browser drops it and falls back
- Recommended action: Use `color-mix(in srgb, var(--color-action-primary) 50%, transparent)`, which works with any colour format. If named opacity steps are needed, add tokens like `color.action.primary-alpha-50` (no `%` in token names — it isn't valid in a CSS custom property name without escaping)
```

Before reporting that a pattern wasn't found, confirm the search finds a known instance (a hex value in the token source files is a good positive control). If it can't, report the result as unconfirmed.

## Step 7: Produce the theme audit report

Open with a headline sentence that tells the reader how worried to be and where to focus. Example: "Dark mode is close — four colour tokens were never themed and two component tokens bypass the semantic tier. Brand B is complete."

Structure the report as follows:

---

### Theme audit report

**Date:** [date]
**Themes audited:** [themes in scope]
**System theming enabled:** [yes/no from config]

---

#### Summary

Overall theme health. What is the most significant gap? Is coverage consistent across themes, or are some themes neglected? Are component tokens correctly inheriting from semantic tier?

One paragraph. Honest about severity.

---

#### Theme discovery

List all themes discovered and confirmed in scope:
- Light (default, CSS root)
- Dark (CSS .dark scope)
- Brand A (data-theme="brand-a")
- Brand B (data-theme="brand-b")

---

#### Token inventory

| Category | Total | Coverage |
|---|---|---|
| Semantic tokens | [n] | [n] theme-dependent tokens themed in every theme |
| Component tokens | [n] | [n] correctly reference semantic tier |
| Tier leakage instances | — | [n] component tokens reference primitives ([n] without per-theme override) |

---

#### Coverage findings

**Semantic token gaps (gap rows only):**

| Token | Light | Dark | Brand A | Brand B |
|---|---|---|---|---|
| color.feedback.info | ✓ | ↳ | ↳ | ✓ |
| text.heading.display | ✓ | ✓ | ✗ | ✓ |

For each missing token, include:
- Finding ID
- Severity
- Token name and which themes are missing it
- Components that depend on this token
- Recommended action

---

#### Component tier check

**Tier propagation:**
- Component tokens examined: 287
- Correctly reference semantic tier: 276
- Tier leakage (reference primitives): 11

**Tier leakage violations:**

For each violation:
- Finding ID
- Component token name
- Primitive it references instead of semantic
- Severity: 🔴 Critical if the component token has no per-theme override (blocks theming); 🟡 Medium if it's overridden per theme
- Recommended action

---

#### Visual consistency check

**Light theme consistency:** [✅ PASS / ⚠️ WARN / ❌ FAIL]
**Dark theme consistency:** [✅ PASS / ⚠️ WARN / ❌ FAIL]
**Brand variant consistency:** [✅ PASS / ⚠️ WARN / ❌ FAIL]

List any violations:
- Finding ID
- Consistency rule violated
- Specific token values at fault
- Recommended action

---

#### DTCG resolver status (if applicable)

**Resolver files found:** [count and paths]
**Mode coverage:** [summary of mode-to-token coverage]
**Tokens outside every resolver set:** [count and examples]
**Missing mode values:** [count and severity by theme]

Include resolver-specific findings with severity ratings.

---

#### Regression risk assessment

**Hardcoded values in components:** [count by severity]
**rgba(var()) opacity patterns:** [count, and how many reference tokens that don't hold bare channels]
**Calc() on tokens:** [count and contexts]
**Missing theme-specific variants:** [count and affected components]

Each category should include:
- Count of instances found
- Severity (🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low)
- Recommended remediation approach (codemod, manual refactoring, architectural change)

---

#### Remediation priority

**Tier 1 — Fix immediately:**
- Tier leakage (blocks theme switching entirely)
- Missing semantic tokens in active themes (causes fallback errors)
- Resolver coverage gaps in production modes

**Tier 2 — Fix before next theme launch:**
- Visual consistency violations within themes
- Coverage gaps in beta or upcoming themes
- Regression patterns in high-fan-out components

**Tier 3 — Address in polish phase:**
- Tokens outside every resolver set
- Hardcoded values in low-usage components
- calc() fragility and rgba(var()) patterns that currently work

---

**Scope**
- **Inspected:** [token files, theme scopes, resolver files, component source actually read]
- **Not inspected:** [what was out of reach, e.g. consuming product repos, runtime theme-switching code]
- **How "none found" was checked:** [e.g. the hardcoded-value search's positive control — omit if the report makes no absence claims]
- **Assumptions:** [e.g. which tokens were treated as theme-dependent]

> **A note on context:** This audit sees your token files and theme scopes — it doesn't see why some values are shared across themes. If a finding flags a token you've deliberately kept the same (a fixed brand colour, a shared shadow), tell me and I'll treat it as accepted in future runs.

---

#### Small-system note

If `system.component_count` in config is < 5, or if component count is inferred to be small from theme coverage:

"This is a small system. Component-tier propagation problems (tier leakage) have outsize impact because each component token affects user-facing surfaces directly. Prioritise tier leakage findings even if absolute violation count is low."

---

## Recurring workflow

Follows the recurring-run procedure in the configuration-and-recurring note. Specific to this skill:

1. **Compare against the previous theme audit:**
   - Coverage gap count: increasing, stable, or decreasing?
   - New coverage gaps (themes missing tokens that previously had them)
   - Resolved gaps (tokens now defined in previously missing themes)
   - Tier leakage count: stable or growing?
   - Regression risk patterns: new hardcoded values appearing?
2. **Add a "Trend since last audit" section** to the report header:
   - Coverage delta (+/- n semantic tokens missing across all themes)
   - Tier leakage delta (+/- n instances)
   - Regression risk delta (+/- n hardcoded values)
   - List newly introduced tier leakage (these are recent regressions)

## Quality checks

- Coverage matrix shows only gap rows, across all discovered themes; inherited values are flagged only for theme-dependent tokens
- Tier leakage findings are clearly separated from coverage gaps — they are architectural problems, not just missing values
- Visual consistency checks reference specific token values, not generic observations
- Regression patterns include specific code examples or counts, not abstract descriptions
- Remediation priority is honest about which findings actually block theming
- DTCG resolver findings (if applicable) validate mode-to-token coverage, not just file structure
- Small-system note is present and contextualised if applicable
- Contrast findings are computed from resolved values against the stated WCAG baseline
- If values were not available for visual consistency check, the report notes which checks were skipped
- The Scope block and the closing note about intentional deviations are present
