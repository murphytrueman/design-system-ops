# Sample output: theme-audit (fixture run)

**Skill:** `skills/theme-audit`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it
**Eval case:** `dark-theme-controls` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools, against the fixture as of commit `bc84ffe`. The fixture has changed since, so a rerun won't match line for line. Rerun it with `python3 tests/evals/run_evals.py --case dark-theme-controls`.

---

Verified the skill's `references:` are present (`knowledge-notes/` is intact alongside the skill). No `.ds-ops-config.yml` in the repo, so I audited with skill defaults. Themes discovered: **Light** (`:root`) and **Dark** (`[data-theme="dark"]`) — exactly the two you named, so I proceeded without a scoping question.

---

# Theme audit report

**Date:** 2026-09-23
**Themes audited:** Light (default), Dark
**System theming enabled:** no config file — inferred `true` from the `[data-theme="dark"]` scope

---

## Summary

Dark mode is half-built. Four semantic colour tokens are themed and the elevation direction is right, but three theme-dependent tokens were never overridden, and the one component token that bypasses the semantic tier — `--card-border` — is a raw hex that survives the theme switch and paints every Card with a near-white outline on a dark surface (11.85:1 against the card background, where the themed border would be 1.72:1). Alongside it, the un-themed `--color-action-primary` drops the secondary Button's label to **3.43:1** on the dark page and **2.84:1** on a dark Card — both fail WCAG 2.2 AA. Underneath all of this is an architectural problem: `tokens/*.tokens.json` has no theme dimension at all, so the dark block in `tokens.css` has no source and cannot be regenerated from the files the header claims generated it.

---

## Theme discovery

- **Light** — default, `:root` scope (`src/styles/tokens.css:2`)
- **Dark** — `[data-theme="dark"]` scope (`src/styles/tokens.css:22`)

No resolver files, no Tailwind config, no SCSS theme maps, no JS theme objects. Two themes total.

---

## Token inventory

| Category | Total | Coverage |
|---|---|---|
| Semantic tokens | 9 | 4 themed in dark; 3 theme-dependent tokens inherit light; 2 (spacing) correctly shared |
| Component tokens | 6 | 5 correctly reference the semantic tier |
| Tier leakage instances | — | 1 component token (`card.border`) references a primitive, with **no** per-theme override |

---

## Coverage findings

Gap rows only. ✓ themed · ↳ inherits default · ✗ undefined

| Token | Light | Dark |
|---|---|---|
| `--color-action-primary` | ✓ | ↳ |
| `--color-action-primary-hover` | ✓ | ↳ |
| `--color-text-on-action` | ✓ | ↳ |

`--space-inset` and `--space-gap` also inherit, which is correct — spacing is not theme-dependent.

**TC-01 | 🔴 Critical | `--color-action-primary` is not themed for dark**
Stays `#2563eb` on `#111827`. Consumed directly by `Button.module.css:19` (`.secondary` label colour) and indirectly by `--button-background`.
- Resolved contrast, dark theme: **3.43:1** against `--color-surface-base`, **2.84:1** against `--color-surface-raised` (a Card). AA needs 4.5:1 for this body-sized label; the Card case misses even the 3:1 non-text floor, so the `currentColor` border fails too.
- Light theme is fine: 5.17:1 on white, 4.94:1 on the raised surface.
- **Action:** add a dark value. Lifting to roughly `#60a5fa`-level lightness clears 4.5:1 on both dark surfaces; verify against `--color-surface-raised`, which is the harder of the two.

**TC-02 | 🟠 High | `--color-action-primary-hover` is not themed for dark**
Stays `#1d4ed8`, which is *darker* than the default state. In a dark theme that moves the button toward the background — 2.65:1 against `--color-surface-base`, down from the default's 3.43:1. Hover reads as receding rather than responding.
- **Action:** define a dark hover that is lighter than the dark default, mirroring the light theme's darker-on-hover logic in reverse.

**TC-03 | ⚪ Low | `--color-text-on-action` is not themed for dark**
Stays `#ffffff`. White on `#2563eb` is 5.17:1 and passes, so this is currently harmless — but it is only safe because the button background is also un-themed. It becomes a live dependency the moment TC-01 is fixed.
- **Action:** re-check this pairing as part of the TC-01 fix; theme it if the new dark primary is light enough to need dark label text.

---

## Component tier check

- Component tokens examined: **6**
- Correctly reference the semantic tier: **5**
- Tier leakage: **1**

**TC-10 | 🔴 Critical | Tier leakage | `card.border`**
`tokens/component.tokens.json:9` sets `card.border` to `{color.gray.200}` — a primitive — and `src/styles/tokens.css:17` emits it as the literal `#e5e7eb`. There is no `[data-theme="dark"]` override, so the value is identical in both themes.
- **Impact:** every Card renders a near-white 1px outline in dark mode. Resolved contrast against the dark card background (`#1f2937`) is **11.85:1**; the themed `--color-border-default` would give **1.72:1**. This is the single most visible dark-mode defect — it is not subtle, it outlines the component.
- Its sibling `--card-background` correctly uses `var(--color-surface-raised)`, which makes the border the only part of the Card that ignores the theme.
- **Action:** `card.border: {color.border.default}` in the token file, emitting `--card-border: var(--color-border-default)`.

---

## Visual consistency check

**Light theme:** ⚠️ WARN
**Dark theme:** ❌ FAIL

Passing, in both themes: text contrast is strong everywhere it is themed (`--color-text-default` scores 17.74:1 / 16.96:1 on light surfaces and 16.96:1 / 14.02:1 on dark). Dark elevation is directionally correct — `--color-surface-raised` (`#1f2937`) is lighter than `--color-surface-base` (`#111827`), so raised surfaces read as raised.

**TC-20 | 🟠 High | Hardcoded colour breaks in both themes | `Card.module.css:10`**
`.title { color: #1a73e8 }` is not a token at all, so it is identical in light and dark. Resolved: **4.31:1** on the light card (`#f9fafb`) and **3.26:1** on the dark card (`#1f2937`). Both fail the 4.5:1 body-text baseline. They clear 3:1 only if the `h3` renders at large-text size — at the browser default (`1.17em` bold ≈ 18.7px) it sits right on the 18.66px bold threshold, so any reduction in heading size drops it below even the large-text allowance in dark.
- **Action:** replace with `var(--color-text-default)`, or introduce a themed accent-text semantic token if the blue is deliberate. Note that `#1a73e8` is not `--color-action-primary`'s `#2563eb` — it is a fourth blue with no token behind it.

**TC-21 | 🟡 Medium | Tooltip inverts by coincidence | `Tooltip.module.css:8-9`**
The bubble uses `--color-text-default` as its background and `--color-surface-base` as its text colour. Contrast is excellent in both themes (17.74:1 light, 16.96:1 dark) and the inversion flips correctly — but only because those two tokens happen to be near-opposites in both themes. There is no semantic contract holding that true; the first theme that darkens `--color-text-default` less aggressively silently breaks the tooltip. In dark mode it also produces a near-white block, which may or may not be the intended inverted-tooltip treatment.
- **Action:** add `color.surface.inverse` / `color.text.inverse` semantic tokens and point the Tooltip at those.

**TC-22 | ⚪ Low | Light-theme surfaces are nearly indistinguishable**
`--color-surface-base` (`#ffffff`) and `--color-surface-raised` (`#f9fafb`) differ by 1.05:1. Since Card also draws a border, the hierarchy still reads — but the surface token is doing almost no work in light mode. Likely intentional; worth confirming.

Borders in both themes are low-contrast by design (1.24:1 light, 1.72:1 dark) and I have **not** flagged them as failures — decorative borders are outside WCAG 1.4.11. If the Card border is ever meant to delineate an interactive region, both themes would need to reach 3:1.

---

## DTCG resolver status

**Not applicable — and that is itself the finding.**

**TC-30 | 🟠 High | No theme dimension exists in the token source**
No `.resolver.json` files, no `$modes`, no per-theme token files. `tokens/semantic.tokens.json` defines exactly one value per token, and the dark theme exists *only* as a hand-written CSS block. Yet `src/styles/tokens.css:1` declares the file "Generated from tokens/\*.tokens.json", and `package.json` has no build script or Style Dictionary dependency to do that generation.
- **Impact:** if anyone regenerates `tokens.css` from the JSON, the entire dark theme disappears. Dark mode is currently unreproducible from the source of truth.
- Secondary: `semantic.tokens.json` and `component.tokens.json` declare no `$type` (only `primitives.tokens.json` does), so they are not DTCG-valid as they stand.
- **Action:** decide whether the JSON or the CSS is authoritative, then make it so. If JSON, add a mode dimension (resolver or per-theme sets) and a real build step before the next edit to `tokens.css`.

---

## Regression risk assessment

| Pattern | Count | Severity |
|---|---|---|
| Hardcoded colour in component code | 1 (`Card.module.css:10`) | 🟠 High — see TC-20 |
| Hardcoded colour in a token definition | 1 (`--card-border`) | 🔴 Critical — see TC-10 |
| `rgba(var(--token), α)` opacity hacks | 0 | — |
| `calc()` on token values | 0 | — |
| Inline styles with theme conditionals | 0 | — |
| Missing theme-specific component variants | 0 identified | — |

All three token consumers use `var()` for spacing, and both spacing tokens carry `px` units in every theme, so there is no calc-unit fragility. The `border-radius` values in `Button.module.css:4` (`6px`) and `Card.module.css:5` (`8px`) are hardcoded, but radius is not theme-dependent — that is a token-coverage issue for `token-audit`, not a theming one.

**Positive control for the absence claims:** the same search that returned zero `rgba(var())` and `calc()` hits did return all nine hex literals in `tokens.css` plus the one in `Card.module.css`, so the pattern search is working over these files.

---

## Remediation priority

**Tier 1 — fix immediately (blocks dark mode shipping):**
1. TC-10 — `card.border` tier leakage. One-line fix, largest visual payoff.
2. TC-01 — theme `--color-action-primary` for dark. Fixes the secondary Button's AA failure.
3. TC-30 — establish where the dark theme actually lives before any further token edits, or the fixes above get overwritten.

**Tier 2 — fix before the next theme:**
4. TC-20 — replace `#1a73e8` with a token (fails AA in *both* themes today).
5. TC-02 — dark hover direction.
6. TC-21 — give Tooltip real inverse semantic tokens.

**Tier 3 — polish:**
7. TC-03 — re-verify `--color-text-on-action` after TC-01.
8. TC-22 — confirm light surface separation is intentional.
9. Add `$type` to the semantic and component token files.

---

## Scope

- **Inspected:** `src/styles/tokens.css` (both theme scopes), all three `tokens/*.tokens.json` files, all three component stylesheets and their `.tsx` files, `src/index.ts`, `package.json`. Contrast computed from resolved values (aliases followed to final hex per theme) against WCAG 2.2 AA.
- **Not inspected:** `*.stories.tsx` files (read only for the hardcoded-value sweep, not reviewed as consumers); any product repo consuming `@fixture/ui`; runtime theme-switching code, which does not exist in this repo — nothing sets `data-theme`.
- **How "none found" was checked:** positive control described in the regression section.
- **Assumptions:** colour, shadow and border-colour tokens are theme-dependent; spacing and radius are not. The Card `h3` was evaluated at browser-default heading size. Card and Button borders were treated as decorative, not as control boundaries.

**Small-system note:** with three components, tier leakage has outsized impact — `--card-border` is one token, but it is one-third of your library's surfaces. Prioritise the tier-1 items even though the absolute counts are low.

> **A note on context:** This audit sees your token files and theme scopes — it doesn't see why some values are shared across themes. If a finding flags something you've deliberately kept constant (a fixed brand blue, an intentionally bright inverted tooltip), tell me and I'll treat it as accepted in future runs.
