# Sample output: token-compliance (fixture run)

**Skill:** `skills/token-compliance`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it
**Eval case:** `hardcoded-hex` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools. Rerun it with `python3 tests/evals/run_evals.py --case hardcoded-hex`.

---

Audit complete. Here's the report.

---

# Token compliance report

**Your components are mostly well-tokenised — 12 of 13 styled declarations resolve through tokens. The one that doesn't (`#1a73e8` in Card) is a theming break, and there's a second, sneakier one: Card's border is wired to a token that was itself hardcoded upstream, so Card won't render correctly in dark mode at all.**

**Date:** 2026-09-23
**Scope:** `src/components` — Button, Card, Tooltip (source + CSS Modules)
**Assessment method:** Direct codebase inspection, cross-referenced against `tokens/*.tokens.json` and `src/styles/tokens.css`

---

## Summary

Violations are few and concentrated: **Card carries both the critical and the highest-impact issue**, Tooltip has one semantic misuse, Button has a minor tier inconsistency. This is not a system with an adoption problem — the token plumbing works and is being used. What it has is three specific defects plus one genuine gap in the token set (no radius scale).

The pattern worth your attention: **both Card findings only bite under theming.** Your dark theme block in `tokens.css` is live, which means these aren't latent debt — they're shipping bugs in dark mode.

---

## Violation counts

| Check | Violations | 🔴 Critical | 🟠 High | 🟡 Medium | ⚪ Low |
|---|---|---|---|---|---|
| Hardcoded colour values | 1 | 1 | — | — | — |
| Hardcoded dimension values (radius) | 3 | — | — | 3 | — |
| Hardcoded typography values | 0 | — | — | — | — |
| Wrong-tier token references | 0 | — | — | — | — |
| Inconsistent token application | 2 | — | 1 | 1 | — |
| **Total** | **6** | **1** | **1** | **4** | **0** |

---

## Violation log

| ID | Check | Severity | Location | Raw value / incorrect reference | Correct token | Notes |
|---|---|---|---|---|---|---|
| TC-01 | Colour | 🔴 Critical | `src/components/Card/Card.module.css:10` | `color: #1a73e8` | none — nearest: `var(--color-action-primary)` (`#2563eb`) | Off-system. Severity upgraded from High: theming is live and this value cannot follow it. See note below. |
| TC-02 | Dimension | 🟡 Medium | `src/components/Card/Card.module.css:5` | `border-radius: 8px` | none — no radius token exists | Off-system; system gap, not misuse |
| TC-03 | Dimension | 🟡 Medium | `src/components/Button/Button.module.css:4` | `border-radius: 6px` | none — no radius token exists | Off-system; system gap |
| TC-04 | Dimension | 🟡 Medium | `src/components/Tooltip/Tooltip.module.css:10` | `border-radius: 4px` | none — no radius token exists | Off-system; system gap |
| TC-05 | Inconsistent | 🟡 Medium | `src/components/Button/Button.module.css:19` | `var(--color-action-primary)` | `var(--button-border)` or `var(--button-text-secondary)` (neither exists yet) | `.primary` uses the component tier, `.secondary` reaches past it to semantic. Not wrong-tier — but inconsistent within one component. |
| TC-06 | Inconsistent | 🟠 High | `src/components/Tooltip/Tooltip.module.css:8-9` | `background: var(--color-text-default)`; `color: var(--color-surface-base)` | `var(--color-surface-inverse)` / `var(--color-text-inverse)` (neither exists yet) | Borrows a *text* token's value for a *background*. Works today by coincidence; breaks the moment text colour is retuned independently. |

**On TC-01:** `#1a73e8` matches no token in your system — it's Google's blue, not your `#2563eb`. Two things follow. It won't flip in dark mode, so a blue title lands on `#1f2937` at roughly **3.2:1** contrast; in light mode on `#f9fafb` it's about **4.3:1** — both under 4.5:1 for normal text. And you need a decision the audit can't make for you: if the card title is meant to read as *heading text*, the right token is `var(--color-text-default)`; if it's meant to read as an *action*, it's `var(--color-action-primary)`. The hardcoded value is ambiguous between the two.

**Excluded as structural:** `border: 1px solid` (Button, Card — divider width), `border: 0` (Button reset), `position: relative/absolute` (Tooltip), `margin: 0` (Card title reset), `cursor: pointer`. Exempt keywords `transparent` and `currentColor` (Button `.secondary`) are not violations.

---

## Cross-reference: the root cause behind Card's border

This sits **outside `src/components`**, so it is not in the log above — but it's the reason a file inside your scope misbehaves, and it's the highest-value fix here:

- `tokens/component.tokens.json:9` — `card.border` → `{color.gray.200}` references a **primitive**, skipping the semantic tier. This is the textbook wrong-tier violation.
- `src/styles/tokens.css:17` — consequently generates `--card-border: #e5e7eb` as a literal, while its sibling `--color-border-default` *does* flip to `#374151` under `[data-theme="dark"]`.
- `src/components/Card/Card.module.css:3` consumes `var(--card-border)` in good faith.

**Net effect: Card keeps a light-gray border on a dark surface in dark mode.** Card.module.css is doing everything right — the defect is upstream. Fix is one line: point `card.border` at `{color.border.default}`. Token *definitions* are token-audit's remit, so run that skill if you want the tier structure swept properly.

---

## Pattern analysis

- **Concentrated, not distributed.** Card holds the critical finding and the cross-reference root cause. Two files fixed clears most of the risk.
- **The dominant category is "no token exists," not "token ignored."** Four of six findings (TC-02/03/04, and the token-less remediation targets for TC-05/06) point at genuine gaps: no radius scale, no inverse surface pair, no secondary-button tokens. Your team isn't bypassing the system — in three places the system has nothing to offer them. That's a token-set expansion job, not an enforcement job.
- **Three radii, three values, no scale** (4/6/8px). Divergence here is a symptom of the missing scale, not carelessness.
- **Adoption is healthy.** All 12 `var()` references resolve to semantic or component tier; padding, margin and gap are fully tokenised across all three components.

---

## Remediation priority

**Immediate** — architectural / theming impact:
1. `card.border` → `{color.border.default}` in `tokens/component.tokens.json`, then regenerate `tokens.css` (fixes dark-mode Card borders)
2. TC-01 — replace `#1a73e8` after deciding heading vs. action intent

**Planned** — needs tokens added first:
3. Add a radius scale (`radius.sm/md/lg`) → resolves TC-02/03/04 together
4. Add `color.surface.inverse` + `color.text.inverse` semantics → resolves TC-06 properly
5. Add secondary-variant button tokens → resolves TC-05

**Review** — your call:
6. Whether Button `.secondary` should use component tokens at all. Referencing semantics directly from component code is legitimate; the issue is only that `.primary` and `.secondary` do it differently. Picking one convention for the file is enough.

---

## Remediation approach

Six violations across three files is **manual-fix territory — don't build a codemod.** Sequence matters more than tooling: add the missing tokens first (radius scale, inverse pair), then the component edits become one-line substitutions rather than judgement calls.

The one thing worth automating is prevention. A Stylelint rule banning raw hex and `px` outside `src/styles/` would have caught TC-01 at the point it was written, and would keep the radius scale honest once it exists.

---

**Scope**
- **Inspected:** `src/components/**` — 3 `.tsx`, 3 `.module.css`, 2 `.stories.tsx`. Reference material: `tokens/{primitives,semantic,component}.tokens.json`, `src/styles/tokens.css`, `src/index.ts`, `package.json`.
- **Not inspected:** No token-consuming code exists outside `src/components` in this repo. `src/styles/tokens.css` was read as reference and root-cause evidence, but excluded from the violation log as generated build output. Stories were excluded per the skill's fixture rule — they contain no styling anyway.
- **How "none found" was checked:**
  - *Colour:* the hex/`rgb()`/`hsl()`/`oklch()` pattern returns 20 hits in `tokens/primitives.tokens.json` and `src/styles/tokens.css`, so it demonstrably works on this codebase. Exactly one hit in `src/components`.
  - *Wrong-tier (zero):* structurally backed — `tokens.css` exposes no primitive-level custom properties at all (no `--color-blue-*`, `--color-gray-*`, `--spacing-*`), so a component→primitive CSS reference is not expressible here. A search for those names across `src/components` returns nothing.
  - *Typography (zero):* **unconfirmed rather than clean.** The pattern (`font-size|font-weight|line-height|font-family|letter-spacing`) returns zero across the *entire repo*, token source included — there is no typography tier to comply with. Nothing was found because nothing exists, not because components are compliant.
- **Assumptions:** `src/styles/tokens.css` is current with `tokens/*.tokens.json` (the header comment says it's generated; I did not verify the build). The `[data-theme="dark"]` block means dark mode is a live requirement — this drove the TC-01 upgrade to Critical. No `.ds-ops-config.yml` is present, so default severities apply.

If any of these are deliberate — the Google blue as a one-off, or the radii as intentionally untokenised — tell me and I'll exclude them in future runs.
