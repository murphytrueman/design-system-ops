# Sample output: theme-audit (fixture run)

**Skill:** `skills/theme-audit`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `59a43fa`
**Eval case:** `dark-theme-controls` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools. Rerun it with `python3 tests/evals/run_evals.py --case dark-theme-controls`; runs vary, so expect the same findings in different words.

---

## Theme audit report

**Date:** 2026-09-23
**Themes audited:** Light (`:root`), Dark (`[data-theme="dark"]`)
**Theming config:** No `.ds-ops-config.yml` found — audited both themes as requested, no severity overrides applied

---

### Summary

Dark mode is in good shape at the semantic tier — all seven theme-dependent colour tokens are properly overridden, elevation reads correctly (raised is lighter than base), and hover direction flips the right way per theme. The problem is one tier down: `--card-border` is a raw hex literal that never themes, so every Card renders a near-white 1px outline on a dark surface. One hardcoded hex in `Card.module.css` compounds it. Both are in the Card, both are small fixes.

---

### Theme discovery

- **Light** — `:root` scope, default, `src/styles/tokens.css:2`
- **Dark** — `[data-theme="dark"]` scope, `src/styles/tokens.css:22`

No resolver files, Tailwind config, SCSS theme maps or JS theme objects found. No third theme or brand variant.

---

### Token inventory

| Category | Total | Coverage |
|---|---|---|
| Semantic tokens | 9 | 7 theme-dependent tokens, all 7 themed in dark |
| Component tokens | 6 | 5 reference the semantic tier; 1 holds a raw value |
| Tier leakage instances | — | 1 (`--card-border`), with no per-theme override |

`--space-inset` and `--space-gap` inherit the light values in dark. Correct — spacing isn't theme-dependent.

---

### Coverage findings

No semantic token is undefined in either theme, and no theme-dependent semantic token silently inherits the default. **Semantic-tier coverage is complete.** The coverage matrix has no gap rows.

---

### Component tier check

- Component tokens examined: 6
- Correctly reference semantic tier: 5
- Tier leakage: 1

**TC-01 | 🔴 Critical | Tier leakage** — `--card-border: #e5e7eb` (`src/styles/tokens.css:17`)

Every other component token aliases a semantic token; this one hardcodes the resolved light value of `{color.gray.200}`. The same leak exists upstream in `tokens/component.tokens.json:9`, where `card.border` references `{color.gray.200}` — a primitive — rather than `{color.border.default}`. The CSS is faithfully generated from a token file that was already wrong.

- **Impact:** `--color-border-default` themes correctly to `#374151` in dark, but Card never sees it. A Card in dark mode gets a `#e5e7eb` border on a `#1f2937` background — 11.9:1 contrast, which reads as a bright outline rather than a subtle edge. Card is 1 of 3 components in the library.
- **Fix:** `tokens/component.tokens.json` → `"border": { "$value": "{color.border.default}" }`, then regenerate. In CSS that becomes `--card-border: var(--color-border-default);`.

**TC-02 | 🟡 Medium | Scoped-theming fragility** — all six component tokens are declared only in `:root`

`--button-background: var(--color-action-primary)` substitutes at computed-value time *on the element where it's declared*, which is `:root`. If `data-theme="dark"` is set on `<html>`, both blocks target the same element and this resolves correctly. If a consumer scopes the theme to a subtree (`<div data-theme="dark">`), the component tokens were already resolved to light values at the root and inherit down as literals — the subtree gets dark semantics but light buttons and cards.

- **Impact:** Blocks per-section theming (a dark sidebar, a theme-preview panel). No effect on whole-page switching.
- **Fix:** If scoped theming is ever needed, redeclare the component-token block inside `[data-theme="dark"]` too, or drop the component aliases and let components reference semantics directly. If theming is root-only by design, mark this accepted.

---

### Visual consistency check

Contrast computed from resolved values against WCAG 2.2 AA (4.5:1 body text, 3:1 large text and non-text).

**Light theme:** ⚠️ WARN
**Dark theme:** ⚠️ WARN

Passing pairs, both themes: text on base and raised surfaces (17.7:1 / 17.0:1 light, 17.0:1 / 14.1:1 dark), text-on-action over primary and hover (5.2:1 / 6.7:1 light, 7.0:1 / 9.8:1 dark), secondary button and focus ring over base (5.2:1 light, 7.0:1 dark), Tooltip (17.7:1 light, 17.0:1 dark — inverts correctly).

Elevation and state logic both pass: dark raised `#1f2937` is lighter than base `#111827`; hover goes darker in light (`#2563eb`→`#1d4ed8`) and lighter in dark (`#60a5fa`→`#93c5fd`).

**TC-10 | 🟠 High | Contrast** — Card title `#1a73e8` (`src/components/Card/Card.module.css:10`)

Against the Card background it lands at **4.31:1 in light** (`#f9fafb`) and **3.26:1 in dark** (`#1f2937`). Both fail the 4.5:1 body-text threshold. They clear the 3:1 large-text threshold only while the `h3` keeps its browser-default bold ~18.7px — any consumer resetting heading sizes drops it below AA. The colour also isn't in the palette at all (nearest primitive is `{color.blue.500}` = `#2563eb`).

- **Fix:** `color: var(--color-text-default)` — 17.0:1 light, 14.1:1 dark. If the title is meant to read as an action colour, `var(--color-action-primary)` gives 5.2:1 light / 7.0:1 dark.

**TC-11 | ⚪ Low | Consistency** — Light theme: `--color-surface-base` `#ffffff` and `--color-surface-raised` `#f9fafb` differ by 1.05:1

The raised surface is marginally *darker* than the page, so elevation rests entirely on `--card-border`. That's a normal light-mode convention, but it means TC-01 also costs Card its only visual boundary in light mode if the border is ever removed. Worth documenting as intentional.

**TC-12 | ⚪ Low | Non-text contrast** — `--color-border-default` `#e5e7eb` on `#ffffff` is 1.24:1 in light (dark themes to 2.32:1 on `#111827`)

Below 3:1 in both themes. Only a violation if a border is the sole means of identifying a control's boundary; for Card's decorative edge it isn't. Flagging so you can decide, not because it's failing today.

---

### DTCG resolver status

Not applicable — no `.resolver.json` files found. The token files use DTCG 2025.10 object value shapes in `primitives.tokens.json` (`colorSpace`/`components`, `{value, unit}`), so the resolver system is available to you if a third theme ever arrives. Today the light/dark split lives only in generated CSS, which means theme parity can't be validated at the token-source level — the tier leakage in TC-01 is exactly the kind of thing a resolver would have caught at build time.

---

### Regression risk assessment

| Pattern | Count | Severity |
|---|---|---|
| Hardcoded colour in component code | 1 (`Card.module.css:10`) | 🟠 High — see TC-10 |
| `rgba(var(--token), α)` | 0 found | — |
| `calc()` on token values | 0 found | — |
| Inline styles with theme conditionals | 0 found | — |
| Missing theme-specific variants | 0 found | — |

The hex search matches `#rgb`/`#rrggbb`, `rgb()`, `rgba()`, `hsl()` and `hsla()`, and does find hex in the token source files, so it works on this codebase. It found exactly one hex outside the token layer. The `rgb()`/`hsl()` and `calc()` branches have no positive control here — the codebase contains no instance of either — so treat those two rows as "scanned the right files, nothing present" rather than independently verified.

Hardcoded `border-radius` values (6px, 8px, 4px) and Button's `1px` border exist across the three stylesheets. They're not theme-dependent and no radius tokens exist to use, so they're out of scope here — that's a `token-audit` finding.

---

### Remediation priority

**Tier 1 — fix now**
1. TC-01 — repoint `card.border` to `{color.border.default}` in `tokens/component.tokens.json:9` and regenerate. This is the only finding that actually breaks dark mode.
2. TC-10 — replace `#1a73e8` with a token in `Card.module.css:10`. Fixes a contrast failure in both themes at once.

**Tier 2 — before a third theme**
3. TC-02 — decide whether scoped theming is supported, and either redeclare component tokens in the dark block or record root-only as the contract.
4. Consider moving the light/dark split into a `.resolver.json` so parity is checkable at build time rather than only in generated CSS.

**Tier 3 — polish**
5. TC-11, TC-12 — document the surface-base/raised proximity and the sub-3:1 border as deliberate, or adjust.

---

**Scope**
- **Inspected:** `src/styles/tokens.css`, all three token source files, all three component stylesheets, all three component `.tsx` files, `Card.stories.tsx`, `package.json`
- **Not inspected:** the consuming application — where `data-theme` is actually set, and any product-level overrides, live outside this repo. TC-02's severity depends entirely on that.
- **How "none found" was checked:** see the regression table note above
- **Assumptions:** the seven colour tokens are theme-dependent and the two `--space-*` tokens are not; WCAG 2.2 AA is the baseline; `Card.module.css` `h3` keeps browser-default sizing

**Small-system note:** Three components, six component tokens. Tier leakage carries outsize weight here — TC-01 is one line, but it affects a third of the library. Fix it before the count grows and the pattern gets copied into the next component.

> **A note on context:** This audit sees your token files and theme scopes — not the reasoning behind them. If TC-11 or TC-12 reflect choices you've already made deliberately, say so and I'll treat them as accepted in future runs.
