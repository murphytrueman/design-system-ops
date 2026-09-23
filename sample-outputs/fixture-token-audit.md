# Sample output: token-audit (fixture run)

**Skill:** `skills/token-audit`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `59a43fa`
**Eval case:** `tier-leakage` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools. Rerun it with `python3 tests/evals/run_evals.py --case tier-leakage`; runs vary, so expect the same findings in different words.

---

I have everything I need. Here's the audit.

---

# Token audit report

**The token files are in good shape; the CSS that ships alongside them is not.** `tokens/*.tokens.json` is clean, well-tiered DTCG 2025.10 — but `src/styles/tokens.css` claims to be generated from it and isn't, and the two have already drifted far enough to produce a visible dark-mode bug. Fix the pipeline first; most other findings collapse once it exists.

## Token sources found

| Source | Tokens | Format |
|---|---|---|
| `tokens/primitives.tokens.json` | 12 (10 colour, 2 dimension) | DTCG 2025.10 |
| `tokens/semantic.tokens.json` | 9 (7 colour, 2 space) | DTCG aliases |
| `tokens/component.tokens.json` | 6 | DTCG aliases |
| `src/styles/tokens.css` | 15 `:root` properties + 7 dark overrides | CSS custom properties |

27 tokens in JSON; 15 of them mirrored by hand into CSS.

## Tier structure

- **Primitive:** 🟢 Strong — group-level `$type`, explicit `colorSpace`, 2025.10 object value shapes, numeric scale naming. Textbook.
- **Semantic:** 🟡 Functional — every token is a real alias and names are role-based (`action`, `surface`, `border`, `text`). Held back by state coverage and one orphan.
- **Component:** 🟠 Weak — 6 tokens, one of which leaks to the primitive tier and is hardcoded in CSS. (Button and Card have component tokens, Tooltip doesn't. With three components that's too small to call inconsistent — if it's deliberate scoping, ignore it.)
- **Tier leakage instances:** 1 (`card.border`), duplicated as a hardcoded value in CSS.

## Findings

**TA-01 | 🔴 Critical | Value** — `src/styles/tokens.css:1` says "Generated from tokens/*.tokens.json", but nothing generates it. `package.json` has no `scripts` and no dependencies beyond `react`; there is no Style Dictionary config, resolver, or any other build config in the repo. The CSS is hand-maintained, and it has already diverged: it carries a dark theme the JSON doesn't have, and hardcodes a value the JSON expresses as an alias. Right now the token files are documentation, not a source of truth. → Wire up Style Dictionary v4 (or equivalent) to emit `tokens.css`, keeping the existing custom-property names so no consumer has to change. Root cause of TA-02, TA-03, TA-04.

**TA-02 | 🟠 High | Value** — Card borders break in dark mode. `tokens/component.tokens.json:9` sets `card.border: {color.gray.200}`, skipping the semantic `color.border.default`. In CSS, `tokens.css:17` hardcodes `--card-border: #e5e7eb` and the `[data-theme="dark"]` block doesn't override it — so every `.card` keeps a light `#e5e7eb` border against a `#1f2937` surface. → Change to `{color.border.default}` and `var(--color-border-default)`.

**TA-03 | 🟠 High | Coverage** — The dark theme exists only in CSS. All six dark values are already in your primitive palette — `#60a5fa`=`blue.400`, `#93c5fd`=`blue.300`, `#374151`=`gray.700`, `#1f2937`=`gray.800`, `#111827`=`gray.900`, `#f9fafb`=`gray.50` — but they're copied by value, not referenced, and no `.resolver.json` exists. The token layer can't currently express your theming contract. → Add a resolver with `light`/`dark` modes over the semantic set; the primitives are already there.

**TA-04 | 🟡 Medium | Coverage** — `color.border.default` / `--color-border-default` is declared in both tiers and referenced by nothing, because TA-02 routes around it. Fixing TA-02 fixes this.

**TA-05 | 🟡 Medium | Coverage** — Interaction states stop at hover. No `active`, `disabled`, or `focus` semantics, and no feedback family (error/success/warning). `Button.module.css:9` borrows `--color-action-primary` for its focus ring, and there's no disabled treatment anywhere. → Needs design input on the new values before tokenising.

**TA-06 | 🟡 Medium | Coverage** — No typography, radius, or border-width tokens at all. Three components use three different raw radii (`6px`, `8px`, `4px`) and `1px` borders. The spacing scale is also only two steps (`8px`, `16px`).

**TA-07 | 🟡 Medium | Naming** — Primitives use `spacing.*`, semantics use `space.*`. Two prefixes for one concept, which makes the alias chain read as a mistake. → Pick one; `spacing` matches the primitive file.

**TA-08 | 🟡 Medium | Value** — `Card.module.css:10` hardcodes `color: #1a73e8`, which isn't in the palette at all (your blue is `#2563eb`). It won't theme, and on the dark `#1f2937` surface it'll be low contrast. → `var(--color-action-primary)`.

**TA-09 | ⚪ Low | Coverage** — `src/index.ts` exports components only; `tokens.css` isn't part of the package's public surface, and no component stylesheet uses `var()` fallbacks. A consumer who imports `@fixture/ui` without separately importing the stylesheet gets components with unset backgrounds. Consuming apps weren't inspected — their build may already handle this.

**TA-10 | ⚪ Low | Naming** — `default` / `base` qualifiers (`color.text.default`, `color.border.default`, `color.surface.base`). Flagged because the checklist calls them out, but this is a mainstream convention — if it's your house style, say so and I'll skip it.

**TA-11 | ⚪ Low | Naming** — `button.background-hover` hyphenates the state into the property segment; the dot-path convention used elsewhere would give `button.background.hover`.

## DTCG 2025.10 alignment

Better than most systems at this stage. Every token resolves a `$type` (primitives via group-level `$type`, semantics and component tokens via alias resolution) — no untyped tokens. Values already use 2025.10 object shapes for both `color` and `dimension`, and `colorSpace` is declared explicitly. No composite tokens are in use, so there's nothing to validate there.

The one gap is resolvers: you have a theming contract in CSS with no resolver to express it (TA-03). That's the only DTCG work outstanding, and it's additive — nothing needs restructuring.

## Remediation priority

**Fix first** — TA-01, TA-02, TA-03. These are the source-of-truth break and the bug it already produced.
**Fix next** — TA-07, TA-08, TA-04 (free with TA-02). Naming debt and the one stray hex, cheap while the file count is small.
**Address eventually** — TA-05, TA-06, TA-09, TA-10, TA-11. Real gaps, but they need design decisions rather than mechanical fixes.

## Effort estimates

Token-side only; consumer migration is extra and unscoped (see Scope).

| Finding | Effort | Assumptions | Confidence |
|---|---|---|---|
| TA-01 | 4–8 hrs | Style Dictionary v4, web-only output, existing custom-property names preserved so consumers don't change | Medium |
| TA-02 | 15–30 min | One alias change, regenerated by TA-01's pipeline | High |
| TA-03 | 3–6 hrs | The 6 dark values are the complete intended palette; TA-01 landed first | Medium |
| TA-04 | 0 | Resolved by TA-02 | High |
| TA-07 | 1–2 hrs | Rename in token files; 2 CSS property names used across 3 in-repo files | Medium |
| TA-08 | 15 min | `--color-action-primary` is the intended colour | Medium |
| TA-05 | 4–8 hrs | Excludes design time to choose disabled/focus/feedback values, which will expand the primitive palette | Low — scope the design decision first |
| TA-06 | 1–3 days | Type scale, radius scale and spacing extension all decided together | Low — worth a timeboxed spike |
| TA-09 | 1–2 hrs | Adding a stylesheet export plus `var()` fallbacks | Medium |
| TA-10 + TA-11 | 1–2 hrs | Breaking rename; do it alongside TA-07 in one pass | Medium |

At 27 tokens and one repo, no spike is needed before sprint planning except TA-06.

## Scope

- **Inspected:** `tokens/primitives.tokens.json`, `tokens/semantic.tokens.json`, `tokens/component.tokens.json`, `src/styles/tokens.css`, all four component stylesheets, all three component `.tsx` files, `src/index.ts`, `package.json`. Globbed the repo for Style Dictionary configs, `.resolver.json`, Tailwind and any other build config — none exist.
- **Not inspected:** Consuming product repos, Figma (no Figma file key configured; no `.ds-ops-config.yml` present), git history, the `.stories.tsx` files.
- **How "none found" was checked:** The orphan search matched `var(--token)` across `src/` and found `--color-action-primary` in 2 files and `--space-gap` in 3 — it works on this codebase — and returned zero hits for `--color-border-default`. The hex search (`#hex`, `rgb()`, `hsl()`, `oklch()`) found 15 values in `tokens.css`, confirming it works, and exactly one in component styles (`Card.module.css:10`). Orphans here mean "no in-repo consumer" — this is a shared package (`@fixture/ui`), so external consumers may use tokens I've marked unreferenced.
- **Assumptions:** `[data-theme="dark"]` is the intended theming mechanism; the `:root` block is the light theme; the dark values were chosen deliberately rather than approximated.

> **A note on context:** This audit sees your token files — it does not see the decisions behind them. Some findings may flag patterns your team chose deliberately. If any finding describes an intentional decision, let me know — I'll exclude it from future runs and learn your system's conventions. The goal is to surface problems you haven't seen yet, not to second-guess choices you've already made.

---

Two things worth noting outside the report: the **claude.ai Google Calendar and Slack** connectors need authorizing before their tools work, and this session can't run the OAuth flow — that's via your claude.ai connector settings. Neither was needed here.

If you want, I can follow up with `token-compliance` (to sweep consuming code for hardcoded values properly) or `theme-audit` (dark-mode parity and contrast), which would go deeper on TA-03 and TA-08.
