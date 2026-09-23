# Sample output: token-compliance (fixture run)

**Skill:** `skills/token-compliance`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `59a43fa`
**Eval case:** `hardcoded-hex` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools. Rerun it with `python3 tests/evals/run_evals.py --case hardcoded-hex`; runs vary, so expect the same findings in different words.

---

# Token compliance report

Two findings will break your dark theme, and only one of them is visible as a hardcoded value. The other — Card's border — looks fully tokenised in the component CSS but resolves to a frozen literal.

**Date:** 2026-09-23
**Scope:** `src/components/` (Button, Card, Tooltip)
**Assessment method:** codebase — CSS Modules with CSS custom properties
**Config:** no `.ds-ops-config.yml` found; default severities, no integrations auto-pulled

---

## Summary

Three components, seven violations, no volume problem — this is a small and mostly well-behaved surface. Spacing is fully tokenised everywhere; no component reaches past the semantic tier into primitives.

The two that matter both concern theming. `Card.module.css:10` hardcodes `#1a73e8`, a colour that exists nowhere in your palette. And `card.border` is defined in `component.tokens.json` as a reference to the primitive `{color.gray.200}` rather than the semantic `{color.border.default}` — so `var(--card-border)` in `Card.module.css:3` stays `#e5e7eb` when every other border in the system flips to `#374151` under `[data-theme="dark"]`.

The remaining five are a system gap rather than team behaviour: there is no border-radius token, so three components invented three radii.

---

## Violation counts

| Check | Violations found | 🔴 Critical | 🟠 High | 🟡 Medium | ⚪ Low |
|---|---|---|---|---|---|
| Hardcoded colour values | 1 | 1 | 0 | 0 | 0 |
| Hardcoded spacing/dimension values | 4 | 0 | 0 | 3 | 1 |
| Hardcoded typography values | 0 | 0 | 0 | 0 | 0 |
| Wrong-tier token references | 1 | 1 | 0 | 0 | 0 |
| Inconsistent token application | 1 | 0 | 0 | 1 | 0 |
| **Total** | **7** | **2** | **0** | **4** | **1** |

---

## Violation log

| ID | Check | Severity | Location | Raw value / incorrect reference | Correct token | Notes |
|---|---|---|---|---|---|---|
| TC-01 | Colour | 🔴 Critical | `src/components/Card/Card.module.css:10` | `#1a73e8` | none — nearest: `var(--color-action-primary)` (`#2563eb`) | Off-system. Upgraded from High: the system ships a dark theme and this value doesn't participate, so the card title stays mid-blue on a `#1f2937` surface. Also worth asking whether an *action* colour belongs on a non-interactive `<h3>` — `var(--color-text-default)` may be the right answer. |
| TC-02 | Wrong-tier | 🔴 Critical | `src/components/Card/Card.module.css:3` (root cause: `tokens/component.tokens.json:9`) | `card.border: {color.gray.200}` | `card.border: {color.border.default}` | The component reference is correct; the token definition skips the semantic tier. Emitted as the literal `--card-border: #e5e7eb` at `src/styles/tokens.css:17`, and `[data-theme="dark"]` never overrides it. Definition fix is `token-audit` territory — flagged here because it's reached through consuming code and is invisible in component review. |
| TC-03 | Dimension | 🟡 Medium | `src/components/Button/Button.module.css:4` | `border-radius: 6px` | none — no radius token exists | Off-system |
| TC-04 | Dimension | 🟡 Medium | `src/components/Card/Card.module.css:5` | `border-radius: 8px` | none — no radius token exists | Off-system |
| TC-05 | Dimension | 🟡 Medium | `src/components/Tooltip/Tooltip.module.css:10` | `border-radius: 4px` | none — no radius token exists | Off-system |
| TC-06 | Dimension | ⚪ Low | `src/components/Button/Button.module.css:9-10` | `outline: 2px`, `outline-offset: 2px` | none — no focus-ring token exists | Ambiguous: 2px is a reasonable accessibility floor and may be deliberate. Only becomes a problem when a second component defines a focus ring differently. |
| TC-07 | Consistency | 🟡 Medium | `src/components/Button/Button.module.css:9,14,19,24` | mixes `--button-background` / `--button-text` (component tier) with `--color-action-primary` (semantic tier) for the same colour role | — | Not wrong-tier — semantic references from component code are valid. But the same role is expressed two ways in one file because the component tier only covers the primary variant; there's no `button.background.secondary`, `button.border`, or `button.focus-ring`. Either complete the tier or drop to semantics throughout. |

**Excluded as structural:** `border: 0` and `border: 1px solid currentColor` (Button), `border: 1px solid` (Card) — border widths, not design values. `transparent` and `currentColor` are exempt keywords.

---

## Pattern analysis

Violations are **concentrated in Card** — it holds both critical findings and is the only component with an off-system colour. Button and Tooltip are otherwise clean.

Three patterns are worth separating:

1. **Card is the outlier, not the trend.** `#1a73e8` is Google's blue, not a near-miss of your `#2563eb`. That reads as copy-paste from outside the system rather than drift within it.
2. **Border-radius is a missing token tier, not a compliance failure.** Three components, three values, zero tokens to reference. Nobody could have complied. Same for the focus ring.
3. **Spacing compliance is genuinely clean.** Every padding, margin and gap across all three components routes through `--space-inset` or `--space-gap`. Nothing to fix.

Era analysis doesn't apply here: the repo has a single commit (`987d56d Initial commit`), so `git blame` can't distinguish pre-token from post-token values. The codebase also doesn't meet the messy-codebase indicators — one styling approach, one naming convention, no legacy palette — so the extended protocol was skipped.

**On typography:** zero violations, but read that carefully. The search for `font-size`, `font-weight`, `line-height`, `font-family` and `letter-spacing` returned no hits *anywhere* in `src/`, including the token source — and `tokens/` defines no typography tokens at all. So this is "no typography is declared" rather than "all typography is tokenised." Components inherit type from somewhere outside this package. Worth confirming that's intentional.

---

## Remediation priority

**Immediate** — both break under theming:
- **TC-02:** change `card.border` to `{color.border.default}` in `component.tokens.json` and regenerate. No component change needed; `Card.module.css` is already correct. This is a one-line fix with the highest payoff.
- **TC-01:** decide the intended role of the card title, then use `var(--color-text-default)` or `var(--color-action-primary)`. Don't add `#1a73e8` as a token.

**Planned:**
- **TC-03/04/05:** add a radius scale (your three existing values suggest `radius.sm: 4px`, `radius.md: 6px`, `radius.lg: 8px`) — or decide two of the three were arbitrary and collapse them. The audit can't tell which; the design intent can.
- **TC-07:** complete the button component tier or drop to semantics. Pick one and apply it consistently.

**Review:**
- **TC-06:** confirm whether the 2px focus ring is a deliberate accessibility floor. If so, promote it to a token so the next component inherits it rather than reinventing it.

---

## Remediation approach

Seven violations across three files is too small for a codemod — the write-and-test cost exceeds fixing by hand. Do TC-01 and TC-02 now as a single small PR; they're two lines and they close both theming holes.

The radius and focus-ring findings aren't really remediation work, they're **token architecture work**: five of seven violations point at gaps in the token set rather than at anyone bypassing it. Worth running `token-audit` before fixing them, because TC-02 suggests the primitive-vs-semantic discipline in `component.tokens.json` may not be isolated to `card.border`.

Going forward, a CI grep for hex literals in `src/components/**` would catch the TC-01 class cheaply. It would *not* have caught TC-02 — that needs a tier-reference check against the token tree.

---

**Scope**
- **Inspected:** `src/components/**` — `Button.module.css`, `Button.tsx`, `Card.module.css`, `Card.tsx`, `Tooltip.module.css`, `Tooltip.tsx`. Cross-referenced against `tokens/primitives.tokens.json`, `tokens/semantic.tokens.json`, `tokens/component.tokens.json` and `src/styles/tokens.css`.
- **Not inspected:** `*.stories.tsx` (excluded as fixtures), `src/index.ts`, `src/styles/tokens.css` as a violation target (generated token source — read as reference only). No Figma file, Storybook build or design spec was available, so design-side compliance is out of reach.
- **How "none found" was checked:** the colour pattern (`#hex`, `rgb()`, `hsl()`, `oklch()`) returns 15 hits in `src/styles/tokens.css`, confirming it works on this codebase — so the single hit in `src/components/` is a real count, not a pattern failure. The typography pattern returns **zero hits in the token source too**, so that zero is reported above as "no typography declared" rather than as clean.
- **Assumptions:** `src/styles/tokens.css` is current output of `tokens/*.tokens.json` (its header says generated, but no build script exists in `package.json` to verify). `[data-theme="dark"]` is an actively shipped theme — the two Critical severities rest on that; if dark mode is abandoned, both drop to Medium.

If any of these are deliberate — the Google blue on the card title, the three distinct radii, the mixed tiers in Button — tell me and I'll exclude them in future runs.
