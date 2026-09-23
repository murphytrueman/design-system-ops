# Sample output: token-audit (fixture run)

**Skill:** `skills/token-audit`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it
**Eval case:** `tier-leakage` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools, against the fixture as of commit `bc84ffe`. The fixture has changed since, so a rerun won't match line for line. Rerun it with `python3 tests/evals/run_evals.py --case tier-leakage`.

---

No `.ds-ops-config.yml`, Style Dictionary config, or resolver files found — running with defaults.

**Token sources found:**
```
- tokens/primitives.tokens.json    10 tokens  DTCG 2025.10  primitive tier
- tokens/semantic.tokens.json       9 tokens  DTCG          semantic tier
- tokens/component.tokens.json      6 tokens  DTCG          component tier
- src/styles/tokens.css            15 custom properties + 4 dark overrides (generated view)
Total: 25 logical tokens; the CSS is a derived projection (9 semantic + 6 component = 15 exactly;
primitives are inlined as hex at build time).
```

```
Orphan detection:
- 25 tokens declared (JSON graph)
- 22 referenced by another token or by an in-repo component stylesheet
- 3 orphan candidates: color.gray.700, color.gray.800, color.border.default
  Positive control: --color-action-primary found in 2 files by the var(--…) pattern;
  JSON aliases traced exhaustively by hand (25 tokens) rather than by pattern.
  Not checked: consuming product repos, the token build script (not in this repo).
```

---

# Token audit report

**Your three-tier structure is sound and your generated CSS matches your token source exactly — but one component token skips the semantic tier, and that single line produces a live dark-mode bug.** Behind it sits a bigger issue: your dark theme doesn't exist in your token files at all.

## Tier structure

| Tier | Status | Notes |
|---|---|---|
| Primitive | 🟡 Functional | Correctly shaped, DTCG 2025.10 value objects, proper `color.blue.500` / `spacing.4` naming. No radius or border-width scale. |
| Semantic | 🟡 Functional | Every token is an alias — zero raw values. But states stop at `hover`, and there are no feedback roles or theme modes. |
| Component | 🟠 Weak | 1 of 6 tokens leaks to a primitive; state naming is asymmetric. |

**Tier leakage instances: 1**

**Value integrity: ✅ PASS.** All 9 hex/dimension values in `:root` resolve correctly to their primitives (`#2563eb`=`blue.500`, `#e5e7eb`=`gray.200`, `16px`=`spacing.4`, …). No drift between JSON and CSS.

**DTCG 2025.10: ✅ largely aligned.** Primitives use 2025.10 object value shapes (`{colorSpace, components, hex}`, `{value, unit}`) and group-level `$type`. Semantic and component files carry no `$type`, but every value is an alias, so type resolves through the reference chain — **not a finding**. No composite tokens present. All colours are sRGB-with-hex, which is fine. The one real gap is resolvers — see TA-02.

## Findings

**TA-01 | 🔴 Critical | Value / Tier leakage — `card.border` skips the semantic tier and breaks dark mode**

`component.tokens.json:9` — `"border": { "$value": "{color.gray.200}" }` references a primitive instead of `{color.border.default}`.

Because your generator only emits CSS custom properties for semantic and component tokens (primitives are inlined), this compiles to a literal: `tokens.css:17` → `--card-border: #e5e7eb;` while every sibling emits a `var()` reference. In `[data-theme="dark"]`, `--color-border-default` correctly flips to `#374151`, but `--card-border` stays `#e5e7eb`. **Every Card keeps a near-white border on a dark surface.** The correctly-themed token exists and is simply unused (see TA-07).

**Action:** change `card.border` to `{color.border.default}`, which emits `var(--color-border-default)` and inherits the dark override. One line.

---

**TA-02 | 🟠 High | Coverage — the dark theme has no representation in the token source**

`tokens.css:22-27` defines four dark overrides. Nothing in `tokens/*.tokens.json` declares them: no `$extensions` modes, no `.resolver.json`. The values are traceable (`#111827`=`gray.900`, `#1f2937`=`gray.800`, `#374151`=`gray.700`, `#f9fafb`=`gray.50`) but nothing in the source maps them, and `gray.700`/`gray.800` exist *only* to serve this block — they're orphans in the JSON graph.

The file header says "Generated from `tokens/*.tokens.json`", which can't be true of this block. So it's hand-edited after generation and will be lost on the next regeneration, or the header is stale. Either way, dark mode is currently unowned by your token pipeline, and only 4 of 9 semantic colour tokens have a dark value at all.

**Action:** add a DTCG resolver (`.resolver.json`) with `light`/`dark` modes and give all 9 semantic colour tokens a value in each. Spacing tokens correctly don't need modes.

---

**TA-03 | 🟠 High | Value — hardcoded colour with no semantic token behind it**

`src/components/Card/Card.module.css:10` — `color: #1a73e8` on `.title`. It's not in your palette: `#1a73e8` vs your `color.action.primary` `#2563eb`. It won't theme, and it's the only raw colour in any component stylesheet.

The root cause is a coverage gap — there's no semantic token for emphasised or heading text, so the component invented one.

**Action:** decide the intent. If the title should be body text, point it at `var(--color-text-default)`. If headings warrant their own role, add `color.text.heading` to the semantic tier.

---

**TA-04 | 🟠 High | Coverage — no focus, active, or disabled state tokens**

Standard states expected: default, hover, active, disabled, focus, error, success, warning. You have default and hover. `Button.module.css` has `.primary:hover` and nothing else — no `:focus-visible` rule anywhere in the library, so keyboard users get only the UA default, which is invisible against a `#2563eb` button.

Relatedly: in dark mode `.secondary` renders `var(--color-action-primary)` (`#2563eb`) as text on `--color-surface-base` (`#111827`). That calculates to ~3.4:1 — below WCAG AA's 4.5:1 for normal text. `color.action.primary` has no dark-mode value (TA-02), which is why.

**Action:** add `color.action.primary-active`, `color.focus.ring`, and a disabled treatment to the semantic tier, then bind them in the component tier. Run `theme-audit` for a full per-theme contrast sweep.

---

**TA-05 | 🟡 Medium | Coverage — no radius or border-width scale**

You have colour and spacing primitives but nothing for radius. Three components picked three values independently: Button `6px`, Card `8px`, Tooltip `4px`. Border widths (`1px`) are likewise untokenised.

**Action:** add a `radius` primitive scale and semantic roles (`radius.control`, `radius.container`), then migrate the three literals.

---

**TA-06 | 🟡 Medium | Naming — component token states are asymmetric**

`button.background` has no state segment; `button.background-hover` does. Per `category.role.variant.state`, the base should be `button.background.default`. Your states are also hyphenated suffixes (`background-hover`, `primary-hover`) rather than path segments — applied consistently, so it's defensible, but it prevents grouping states under a shared parent.

**Action:** if you're standardising, go to `button.background.default` / `button.background.hover`. This renames CSS custom properties, so it's breaking for consumers — batch it with TA-08.

---

**TA-07 | ⚪ Low | Coverage — 3 orphan tokens**

`color.gray.700`, `color.gray.800` (referenced by no token; values appear hand-written in the dark CSS block) and `color.border.default` / `--color-border-default` (declared, themed, consumed by nothing). All three are symptoms of TA-01 and TA-02 — fixing those clears all three. 12% of declared tokens, below the threshold that would warrant a cleanup pass.

Orphan status is in-repo only. This is a library package (`@fixture/ui`), so external consumers weren't checked.

---

**TA-08 | ⚪ Low | Naming — category name changes between tiers**

Primitives use `spacing.*`; semantics use `space.*`. Same category, two words, which breaks the readability of the path. Pick one.

---

**TA-09 | ⚪ Low | Naming — `default` as a generic qualifier**

`color.text.default`, `color.border.default`. The architecture note flags `default` as describing nothing at semantic level. That said, it's a widespread convention for base-state tokens and you apply it consistently. If it's your house style, tell me and I'll drop it from future runs.

## Remediation priority

**Fix first — structural, affects downstream consumers**
TA-01 (dark-mode break), TA-02 (unowned theme), TA-04 (focus + contrast)

**Fix next — compounding debt**
TA-03 (hardcoded colour), TA-05 (no radius scale), TA-06 (state naming)

**Address eventually**
TA-07 (clears automatically), TA-08, TA-09

## Effort estimates

| Finding | Effort | Assumptions | Confidence |
|---|---|---|---|
| TA-01 | 1–2 hrs | Includes hand-editing `tokens.css` because the generator isn't in this repo; visual check of Card in both themes | Medium |
| TA-02 | 2–4 days | Design sign-off on dark values for the 5 semantic colours that lack them; assumes your build tool supports DTCG resolvers — unverified, the generator wasn't inspected | Low — scope the generator first |
| TA-03 | 1–2 hrs | A design decision on heading colour, not just a swap | Medium |
| TA-04 | 1–3 days | Focus, active and disabled across 3 components: tokens, CSS, and a11y verification | Medium |
| TA-05 | 2–4 hrs | Agreeing a radius scale; 3 call sites to migrate | High |
| TA-06 | 2–4 hrs | Token-side only. Renaming CSS custom properties is breaking — consumer migration is extra and unscoped | Medium |
| TA-08 + TA-09 | 1–3 hrs | Same breaking-rename caveat; batch with TA-06 | Medium |

**Caveat on every estimate:** the token build script is not in this repository and `package.json` declares no `scripts`. Until it's located, each JSON change needs a matching hand-edit to `tokens.css`, and TA-02 can't be properly scoped. Find the generator before committing any of this to a sprint.

## Scope

- **Inspected:** all 14 files in the repo — `tokens/primitives.tokens.json`, `tokens/semantic.tokens.json`, `tokens/component.tokens.json`, `src/styles/tokens.css`, the three `*.module.css` files, the three `*.tsx` components, both `*.stories.tsx`, `src/index.ts`, `package.json`.
- **Not inspected:** the token build/generator script (absent from this repo), consuming product repos, Figma. Figma Console MCP is connected, but no file was specified and I didn't guess one — give me a file key and I'll run the code-vs-Figma variable comparison.
- **How "none found" was checked:** the hardcoded-colour search (hex, `rgb()`, `hsl()`) ran across all of `src/` and does find the hex values in `tokens.css`, so it works on this codebase; it returns exactly one hit in component code (TA-03). The `var(--…)` reference search finds `--color-action-primary` in 2 files (positive control). No inline styles exist in the `.tsx` files — confirmed by reading all three in full, each styles only via CSS-module `className`.
- **Assumptions:** `tokens.css` is intended to be generated from the JSON, per its header comment. The dark-theme block contradicts this (TA-02).

> **A note on context:** This audit sees your token files — it does not see the decisions behind them. Some findings may flag patterns your team chose deliberately. If any finding describes an intentional decision, let me know — I'll exclude it from future runs and learn your system's conventions. The goal is to surface problems you haven't seen yet, not to second-guess choices you've already made.

---

Want me to fix TA-01? It's a one-line change to `component.tokens.json` plus the matching `tokens.css` edit, and it clears the dark-mode Card border bug and one of the three orphans.
