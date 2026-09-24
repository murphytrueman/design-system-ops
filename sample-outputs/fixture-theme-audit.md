# Sample output: theme-audit (fixture run)

**Skill:** `skills/theme-audit`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `27c301d`
**Eval case:** `dark-theme-controls` in `tests/evals/cases.json`
**Date:** 2026-09-24
**Edited:** no. The report below is verbatim from a headless run with read-only tools; `tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case dark-theme-controls`; runs vary, so expect the same findings in different words.

---

# Theme audit report

**Date:** 2026-09-24
**Themes audited:** Light (default), Dark
**Theming enabled:** assumed yes (no config file; a dark scope exists in the source)

## Summary

The dark theme's *values* are good — someone thought about them, flipped `text-on-action` correctly, and made raised surfaces lighter than the base, which is the right instinct for dark elevation. The problem is everything around those values. The dark theme exists **only** in the generated CSS with no source that produces it, so the next regeneration deletes it. One component token bypasses the semantic tier and turns the card border into a near-white outline in dark mode. And the component tier only themes at all under a precondition nothing in the repo states or enforces. Semantic coverage itself is complete — all seven theme-dependent semantic tokens are themed.

## Token inventory

| Category | Total | Coverage |
|---|---|---|
| Semantic tokens | 9 (7 colour, 2 space) | 7 of 7 theme-dependent tokens themed in dark |
| Component tokens | 6 | 5 reference the semantic tier; 1 references a raw primitive |
| Per-theme component overrides | — | 0 of 6 |
| Tier leakage | — | 1 (`--card-border`), with no per-theme override |

`--space-inset` and `--space-gap` inherit the light value in dark. Correct — they aren't theme-dependent.

## Coverage findings

Gap rows only. Every semantic token is themed, so the only row here is in the component tier.

| Token | Light | Dark |
|---|---|---|
| `--card-border` | ✓ (raw hex) | ↳ inherits light |

---

**TH-01** | 🔴 Critical | Coverage / provenance | **The dark theme has no source of truth.**

`src/styles/tokens.css:1` says the file is generated from `tokens/*.tokens.json`. But `tokens/semantic.tokens.json:1-23` is a single flat value set — no modes, no `$extensions`, no theme structure — and no `.resolver.json` exists anywhere in the repo. So the seven dark values at `tokens.css:23-29` cannot have come from the token sources. They're hand-edits to a generated file.

The corroborating evidence is in `tokens/primitives.tokens.json`: `blue.300` (#93c5fd), `blue.400` (#60a5fa), `gray.700` (#374151) and `gray.800` (#1f2937) are exactly the four dark-theme colours, and **no semantic token references any of them**. They were added to serve dark mode, but the mapping that would consume them was never written.

- **Impact:** Re-running the generator drops the entire `[data-theme="dark"]` block. Dark mode disappears in one build, silently — nothing errors, the selector just stops existing.
- **Action:** Give dark a source before anything else on this list. Either add a DTCG resolver with a `theme` modifier (`light` default / `dark`) over per-context semantic sets, or split `semantic.tokens.json` into `semantic.light` / `semantic.dark` and have the generator emit both scopes. Until that lands, put a comment on `tokens.css:21` saying the block is hand-maintained, so nobody regenerates over it.

**TH-02** | 🔴 Critical | Tier leakage | **`--card-border` bypasses the semantic tier and never themes.**

`tokens.css:17` sets `--card-border: #e5e7eb` — a raw primitive value, not a reference. The source agrees: `tokens/component.tokens.json:9` has `card.border: "{color.gray.200}"`, pointing at the primitive tier instead of `{color.border.default}`. It's the only one of six component tokens that does this; the other five alias semantics correctly. It's also not overridden in the dark block, which is what makes it Critical rather than a maintenance nit.

Resolved values, and the contrast against the card's own fill (`--card-background` → `--color-surface-raised`):

| Theme | Card fill | Border | Contrast |
|---|---|---|---|
| Light | #f9fafb | #e5e7eb | 1.18:1 — nearly invisible |
| Dark | #1f2937 | #e5e7eb | **11.85:1 — a near-white outline on a dark card** |

- **Impact:** `Card` (`Card.module.css:3`) renders a glaring light-grey box outline in dark mode. The inversion is the tell: the border is too faint in the theme it was designed for and far too loud in the one it wasn't.
- **Action:** Fix it in `component.tokens.json:9` — `card.border: "{color.border.default}"` — not in the generated CSS, or it'll come back. That resolves to #e5e7eb in light (identical to today) and #374151 in dark.

**TH-03** | 🟠 High | Regression | **The component tier themes only if `data-theme` sits on the same element as `:root`.**

The five aliasing component tokens (`tokens.css:13-16,18`) are declared in `:root` only, and the dark block redefines no component token. Custom-property substitution resolves at computed-value time *on the element that declares the property* — so `--button-background` is computed on `<html>` against whatever `--color-action-primary` is on `<html>`.

- If `data-theme="dark"` goes on `<html>`, the dark block wins there (equal specificity, later in source order) and everything resolves correctly.
- If it goes on `<body>` or any wrapper `<div>`, `--button-background` is already computed from the light value on `<html>` and inherits down as that resolved colour. `Button` and `Card` stay light-blue and light-grey in dark mode. The semantic tokens would flip; the component tokens wouldn't.

I searched the whole repo for `data-theme` and found it only at `tokens.css:22` — there's no theme-switching code here to tell me which way you apply it.

- **Action:** Pick one and make it explicit. Simplest is documenting that the attribute belongs on `<html>` and adding a lint rule or a comment at `tokens.css:21`. The robust alternative is redeclaring the component tokens inside the dark scope too, which also removes the dependency on placement. Whichever you choose, this is the kind of contract that wants to be written down — it's invisible until a consumer puts the attribute on a wrapper for a scoped dark region, which is a normal thing to want.

**TH-04** | 🟠 High | Consistency / missing token | **The modal backdrop inverts to a white scrim in dark mode.**

`Modal.module.css:4` — `background: var(--color-text-default)` at `opacity: 0.5`.

- Light: #111827 at 50% → a dark scrim. Correct.
- Dark: #f9fafb at 50% → a **white** scrim washing out a dark app.

The root cause is a missing token, not a careless component: the system has no scrim or backdrop semantic, so the component reached for the darkest thing available. That worked until the darkest thing stopped being dark.

- **Action:** Add `color.backdrop` (or `color.scrim`) to the semantic tier, themed per context — dark-with-alpha in both themes, since a scrim should dim in dark mode too, not lighten.

**TH-05** | 🟠 High | Regression | **3 hardcoded colours in the checkout app won't theme.**

`apps/checkout/src/CheckoutButton.module.css:2,3,11` — `#2563eb`, `#ffffff`, `#1d4ed8`. These are precisely the light-theme values of `--color-action-primary`, `--color-text-on-action` and `--color-action-primary-hover`, so this is a `Button` re-implementation frozen at light values. It stays light-blue with white text in dark mode. Contrast happens to remain fine (5.17:1), so it looks intentional rather than broken — which makes it likelier to survive review.

- **Action:** Replace with the `Button` component, or at minimum the three tokens. Run `token-compliance` for the per-file sweep across other consumers — this repo has one app, but the pattern rarely appears alone.

**TH-06** | 🟡 Medium | Regression / contrast | **Card title uses an off-system hardcoded blue.**

`Card.module.css:10` — `color: #1a73e8`. That isn't a value in your primitives at all (nearest is `blue.500` #2563eb), so it's drift, not a shortcut. It won't theme.

As an `<h3>` with no `font-size` set (`Card.tsx:11`), it inherits the UA default of ~18.7px bold, which qualifies as WCAG large text at the 3:1 threshold: **4.31:1** on the light card, **3.26:1** on the dark card. Both pass — but both fail the 4.5:1 body-text threshold, and nothing in the component pins the font-size that earns the large-text exemption. A consumer setting `font-size: 16px` on the title drops it to a failure in both themes.

- **Action:** Use `--color-text-default`, or add a `card.title` component token if the title is meant to be accent-coloured.

**TH-07** | 🟡 Medium | Consistency | **Tooltip inverts by borrowing the text and surface tokens.**

`Tooltip.module.css:8-9` uses `--color-text-default` as a background and `--color-surface-base` as a foreground. Contrast passes comfortably in both themes (17.74:1 light, 16.96:1 dark), and the bubble does invert plausibly — dark bubble on a light page, light bubble on a dark page. But that's a side effect of the two tokens swapping roles, not a designed inverse surface, and it'll break the moment either token moves independently. Same missing-token gap as TH-04.

- **Action:** Fold into the TH-04 fix — an inverse surface pair (`color.surface.inverse` / `color.text.on-inverse`) covers both this and the scrim.

**TH-08** | 🟡 Medium | Consistency | **`--color-border-default` is low-contrast in both themes.**

Light #e5e7eb: 1.24:1 on base, 1.18:1 on raised. Dark #374151: 1.72:1 on base, 1.42:1 on raised. Symmetrical, so this isn't a parity bug — it's a design choice that reads the same either way, and it's fine for decorative dividers (WCAG 1.4.11 covers boundaries *required* to identify a control, which these aren't).

Worth a look anyway because `Dialog` (`Dialog.module.css:3`) uses this border as its only boundary — no backdrop, unlike `Modal` — so at 1.18:1 the dialog has essentially no visible edge against the page. If it's meant to read as a distinct surface, it needs a stronger border or a shadow.

**TH-09** | 🟡 Medium | Structural | **Modal contrast can't be computed — `opacity` applies to the whole subtree.**

`.backdrop` has `opacity: 0.5` (`Modal.module.css:5`) and `.modal` is its **child** (`Modal.tsx:17-18`). Opacity creates a new stacking context and applies to descendants, so the entire modal — title, body, close button — renders at 50%, composited over the scrim over whatever page content is behind. I can't resolve that background from the tokens, so per the contrast rules I'm reporting these ratios as not computed rather than guessing. On the token values alone they'd be 14.02:1; in practice they'll be materially worse.

This is a structural bug rather than a theming one, but it's here because it blocked the dark-theme contrast check on your most contrast-sensitive component.

- **Action:** Move the scrim to a `::before` on `.backdrop`, or to a sibling element behind the modal, so the opacity stops inheriting. Then TH-04's contrast becomes measurable.

⚪ **Low** — `apps/checkout/src/Summary.module.css:2` overrides `--card-padding` with a raw `24px`. Not theme-dependent, so it doesn't affect theming; it's component-token drift, and `drift-detection` is the better home for it.

## Visual consistency check

**Light theme:** ⚠️ WARN — card border effectively invisible at 1.18:1 (TH-02); off-system title colour (TH-06).
**Dark theme:** ❌ FAIL — near-white card border at 11.85:1 (TH-02); backdrop inverts to a white scrim (TH-04).

What's right, for the record: dark elevation reads correctly (`--color-surface-raised` #1f2937 is lighter than `--color-surface-base` #111827 — tokens.css:26-27), `--color-text-on-action` correctly flips to #111827 in dark (tokens.css:25), and every text and focus-indicator pair that resolves through the semantic tier passes AA in both themes:

| Pair | Light | Dark |
|---|---|---|
| `text-default` on `surface-base` | 17.74:1 | 16.96:1 |
| `text-default` on `surface-raised` | 16.96:1 | 14.02:1 |
| `text-on-action` on `action-primary` | 5.17:1 | 6.97:1 |
| `text-on-action` on `action-primary-hover` | 6.70:1 | 9.84:1 |
| Secondary button / focus ring on `surface-raised` | 4.94:1 | 5.77:1 |

Computed in sRGB from resolved values; all sources are opaque hex, so no compositing was needed except in `Modal` (TH-09).

## DTCG resolver status

Not applicable — no `.resolver.json` found anywhere in the repo, and the token files carry no modes or `$extensions`. This absence *is* TH-01.

## Regression risk assessment

| Pattern | Count | Severity |
|---|---|---|
| Hardcoded colours in component/app code | 4 (CheckoutButton ×3, Card ×1) | 🟠 High |
| Theme-inverting use of non-theme-role tokens | 2 (Modal backdrop, Tooltip bubble) | 🟠 High |
| `rgba(var(--token), a)` with non-channel tokens | 0 | — |
| `calc()` on token values | 0 | — |
| Inline styles with theme branching | 0 | — |

The zeros are trustworthy: the hex/`rgb()`/`hsl()` pattern does match the known literals in `tokens.css:3-29`, so the search works on this codebase, and it ran over every `.module.css` and `.tsx` file in `src/` and `apps/`.

## Remediation priority

**Tier 1 — before the next build of `tokens.css`:**
1. TH-01 — give the dark theme a source (a resolver, or per-context semantic sets). Everything else is wasted work if a regeneration can delete dark mode.
2. TH-02 — `card.border` → `{color.border.default}` in `component.tokens.json:9`. One-line fix, fixes the worst visible dark-mode defect.
3. TH-03 — decide and document where `data-theme` lives.

**Tier 2 — before dark mode ships to users:**
4. TH-04 + TH-07 — add scrim and inverse-surface semantics; repoint `Modal` and `Tooltip`.
5. TH-09 — restructure the backdrop so opacity stops cascading into the modal.
6. TH-05 — replace the checkout button's hardcoded colours.

**Tier 3 — polish:**
7. TH-06 — card title colour.
8. TH-08 — review border visibility, particularly for `Dialog`.
9. The `--card-padding` override in `Summary.module.css`.

---

**Scope**
- **Inspected:** `src/styles/tokens.css`; `tokens/primitives.tokens.json`, `semantic.tokens.json`, `component.tokens.json`; all 5 component stylesheets and their `.tsx` in `src/components/`; both stylesheets in `apps/checkout/src/`; `package.json`; a repo-wide search for `data-theme`, colour literals, `rgba(var())`, `calc()` and inline styles.
- **Not inspected:** no theme-switching or app-shell code exists in this repo, so I couldn't verify where `data-theme` is applied at runtime (TH-03) — that likely lives in a consuming app. No Figma library was linked, so design-side parity is unchecked. No generator config or build script exists here, so I inferred the generation relationship from the `tokens.css:1` header.
- **How "none found" was checked:** the colour-literal search matches the known hex values at `tokens.css:3-29`, confirming the pattern works on this codebase; the `rgba(var())`, `calc()` and inline-style searches ran over the same complete file set.
- **Assumptions:** the 7 colour semantics are theme-dependent and the 2 space tokens are not; `tokens.css` really is generated as its header claims; `Card`'s `<h3>` title keeps the UA default size, which is what qualifies TH-06 as large text; WCAG 2.2 AA as the baseline.

> **A note on context:** this audit sees your token files and stylesheets, not the decisions behind them. If any of these are deliberate — a fixed border colour, a tooltip that's meant to borrow the text token — tell me and I'll treat them as accepted next run.
