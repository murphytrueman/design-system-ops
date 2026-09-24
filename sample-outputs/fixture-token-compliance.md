# Sample output: token-compliance (fixture run)

**Skill:** `skills/token-compliance`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `27c301d`
**Eval case:** `hardcoded-hex` in `tests/evals/cases.json`
**Date:** 2026-09-24
**Edited:** no. The report below is verbatim from a headless run with read-only tools; `tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case hardcoded-hex`; runs vary, so expect the same findings in different words.

---

## Token compliance report

**Date:** 2026-09-24
**Scope:** `src/components/` (5 components — Button, Card, Dialog, Modal, Tooltip)
**Assessment method:** Codebase — full read of every file in scope, plus pattern searches
**Styling approach:** CSS Modules consuming CSS custom properties from `src/styles/tokens.css`

---

### Summary

Adoption is genuinely good — 8 violations across 10 files, and every spacing value in the library already routes through `--space-gap` / `--space-inset`. But **this system ships two themes**, and two findings break under the dark theme rather than merely looking untidy: a hardcoded blue in `Card` and a backdrop in `Modal` painted with the *text* colour, which inverts to near-white in dark mode. Those two are the report.

The rest is a tier-discipline story: `Button` and `Card` style themselves from component-tier tokens while `Dialog` and `Modal` reach past that tier to semantics for the identical roles. Nothing is broken today; it means a change to `--button-background` silently misses two of the three buttons in the library.

---

### Violation counts

| Check | Violations found | 🔴 Critical | 🟠 High | 🟡 Medium | ⚪ Low |
|---|---|---|---|---|---|
| Hardcoded colour values | 1 | 1 | 0 | 0 | 0 |
| Hardcoded spacing/dimension values | 3 | 0 | 0 | 0 | 3 |
| Hardcoded typography values | 0 | 0 | 0 | 0 | 0 |
| Wrong-tier token references | 0 | 0 | 0 | 0 | 0 |
| Inconsistent token application | 4 | 1 | 0 | 2 | 1 |
| **Total** | **8** | **2** | **0** | **2** | **4** |

---

### Violation log

**Hardcoded colour**

| ID | Check | Severity | Location | Raw value | Correct token | Notes |
|---|---|---|---|---|---|---|
| TC-01 | Colour | 🔴 Critical | `src/components/Card/Card.module.css:10` | `#1a73e8` | none — nearest: `var(--color-action-primary)` (`#2563eb`) | Off-system. Critical under the multi-theme rule: no dark-theme counterpart, so the card title stays Google-blue on a `#1f2937` surface in dark mode. The value is close to but *not* the brand blue — confirm with design whether it was meant to be `--color-action-primary` or is a genuine one-off |

**Hardcoded spacing / dimension**

| ID | Check | Severity | Location | Raw value | Correct token | Notes |
|---|---|---|---|---|---|---|
| TC-05 | Dimension | ⚪ Low | `Card.module.css:5`, `Dialog.module.css:5`, `Modal.module.css:12` (`8px`); `Button.module.css:4` (`6px`); `Tooltip.module.css:10` (`4px`) | `border-radius` | none — no radius tier exists | Off-system. Three distinct radii with no token to reference. This is a **token system gap**, not contributor error — the scale needs defining before this is fixable |
| TC-06 | Dimension | ⚪ Low | `Button.module.css:9-10` | `2px` (outline), `2px` (offset) | none — no focus-ring token exists | Off-system. Intent ambiguous: plausibly a deliberate fixed a11y dimension. Flagged because focus rings are usually tokenised and this one can't follow a brand change |
| TC-07 | Dimension | ⚪ Low | `Modal.module.css:5` | `opacity: 0.5` | none — no opacity/scrim token exists | Off-system. Paired with TC-02 below |

**Hardcoded typography** — none found. See the note in Scope: this is a true zero, but a weak signal, because the components set no typography properties at all and the token system defines none either.

**Wrong-tier token references** — none found in consuming code. Every `var()` in `src/components` resolves to a semantic or component-tier token; no component reaches for a primitive such as `var(--color-blue-500)`. See Scope for a related *definition*-side issue handed to `token-audit`.

**Inconsistent token application**

| ID | Check | Severity | Location | Incorrect reference | Correct token | Notes |
|---|---|---|---|---|---|---|
| TC-02 | Consistency | 🔴 Critical | `src/components/Modal/Modal.module.css:4` | `var(--color-text-default)` used as the backdrop fill | none — no `color.surface.scrim` / `.inverse` token exists | Right tier, wrong semantic role. Severity assigned by the theming rule, not the hardcoded-colour rule: `--color-text-default` flips `#111827` → `#f9fafb` under `[data-theme="dark"]`, turning a dark scrim into a white wash at 50% opacity. Needs a new semantic token, not a swap |
| TC-03 | Consistency | 🟡 Medium | `Dialog.module.css:18-19`; `Modal.module.css:26-27` | `var(--color-action-primary)` + `var(--color-text-on-action)` | `var(--button-background)` + `var(--button-text)` | Same role (primary action button) implemented at two different tiers. `Button.module.css:14-15` uses the component tier; these bypass it. Resolves identically today, so a component-tier change reaches one button of three |
| TC-04 | Consistency | 🟡 Medium | `Dialog.module.css:2-4`; `Modal.module.css:9-11` | `var(--color-surface-raised)`, `var(--color-border-default)`, `var(--space-inset)` | `var(--card-background)`, `var(--card-border)`, `var(--card-padding)` — or a new `--surface-*` set | Same raised-surface role as `Card.module.css:2-4`, implemented at the semantic tier instead. Worth a decision rather than a blind swap: `--card-*` is named for Card, so the fix may be a shared surface token, not reuse of Card's |
| TC-08 | Consistency | ⚪ Low | `Tooltip.module.css:8-9` | `var(--color-text-default)` as background, `var(--color-surface-base)` as text | none — no `color.surface.inverse` token exists | Off-system but **not a bug**: verified it inverts correctly in both themes. Logged only as evidence for the missing inverse role (same gap as TC-02) |

**Excluded as structural:** `border: 1px solid <token>` (Card:3, Dialog:3, Modal:10, Button:25) and `border: 0` (Button:3, Dialog:20, Modal:28) — divider/reset widths; `position: fixed; inset: 0` (Modal:1-2) and `position: relative/absolute` (Tooltip:2,6) — layout; `margin: 0` resets (Card:9, Dialog:10, Modal:16). `transparent` and `currentColor` (Button:23,25) are exempt keywords, not violations.

---

### Context-aware severity

**No adjustments were applied**, and the reason matters for reading the table above:

- **Critical-path elevation:** not applied. No critical-path list was supplied for this run. There is an `apps/checkout/` directory in the repo, but the skill forbids inferring criticality from a directory name, and it is outside the requested scope regardless. If `Button` or `Modal` sits on checkout or auth, TC-03 and TC-07 rise a level — tell me and I'll re-rank.
- **Fan-in elevation:** not applied. `.ai/index/` does not exist, so there is no fan-in data. Running `codebase-index` would enable it.
- **Era-based adjustment:** not applied, and **not possible**. The repository has a single commit (`5ef6762 Initial commit`), so `git log -S` and `git blame` cannot distinguish pre-token, migration-era and post-token code. Every violation is therefore reported at its base severity, with none reduced as inherited debt and none elevated as an active post-token failure.
- **Deprecation reduction:** not applied — no component was named as scheduled for deprecation.

---

### Pattern analysis

**The violations are not a contributor-discipline problem; they are a token-coverage problem.** Six of the eight findings (TC-02, TC-05, TC-06, TC-07, TC-08, and TC-01's off-system status) exist because **no token covers the property**. The token system has exactly four colour roles, two spacing steps, and nothing else: no radius scale, no opacity or scrim role, no focus-ring dimension, no inverse surface. Contributors reaching for a raw value there had no compliant option. A lint rule alone would fail these files without offering a fix.

**The distribution is flat, not concentrated.** Every component carries one to three findings; no hotspot file dominates. That rules out "one legacy area" and points at a system-wide gap. The single exception is `Card.module.css:10` (TC-01) — the only true raw hex in the library, isolated, and reading as a one-off paste rather than a pattern.

**Two components diverge in tier discipline.** `Button` and `Card` consume component-tier tokens; `Dialog` and `Modal` consume semantics directly for the same roles (TC-03, TC-04). `Dialog` and `Modal` are also near-duplicates of each other — same structure, same tokens, different prop names (`isOpen`/`open`, `onDismiss`/`onClose`). The token divergence is a symptom; the duplication is the cause, and it belongs to `component-audit`, not here.

**The theming failures cluster on "using a text colour as a background."** TC-02 and TC-08 are the same move; only one of them breaks. That is the signature of a missing `inverse`/`scrim` semantic role that people are approximating with whatever dark token exists.

---

### Remediation priority

**Immediate — theme-breaking:**
- **TC-02** (`Modal` backdrop) — a visible dark-mode regression today. Needs a new `color.surface.scrim` semantic token that does *not* invert, then a swap. Fixing this also resolves TC-07.
- **TC-01** (`Card` title `#1a73e8`) — confirm intent with design, then either point it at `--color-action-primary` or add a token for it. Do not blind-swap: the value differs from the brand blue.

**Planned — tier discipline:**
- **TC-03**, **TC-04** — mechanical once a decision is made on whether `Dialog`/`Modal` adopt `--card-*`/`--button-*` or a new shared surface token is introduced. Resolve the `Dialog`/`Modal` duplication first, or you will fix the same thing twice.

**Review — needs design input before any code changes:**
- **TC-05** (radius), **TC-06** (focus ring), **TC-08** (inverse surface). These are scale-definition decisions. Three radii in five components suggests the real answer is a two- or three-step radius scale, not five individual fixes.

---

### Remediation approach

At 8 violations, **a codemod is not worth writing** — this is an afternoon of manual work. The sequencing matters more than the tooling:

1. **Extend the token system first.** Add `color.surface.scrim`, `color.surface.inverse`, a radius scale, and a focus-ring dimension. Six of eight findings are unfixable until these exist; attempting the cleanup first produces churn.
2. **Then fix TC-02 and TC-01** — the only two findings with user-visible impact.
3. **Then resolve `Dialog`/`Modal`**, and let TC-03/TC-04 fall out of that consolidation.
4. **Add a lint rule last**, once compliant options exist. `stylelint-declaration-strict-value` on `color`, `background`, `background-color`, `border-radius` and `padding`, with `ignoreValues` set to `/^var\(--/` plus the exempt keywords, holds the line. `governance-encoder` writes that config.

A **token architecture review is warranted before remediation** — the semantic tier is too thin to reference correctly, which is the root cause of most of this report. `token-audit` is the right next skill.

---

**Scope**

- **Inspected:** `src/components/**` — all 10 files (5 `.module.css`, 5 `.tsx`), read in full, plus pattern searches for hex/rgb/hsl/oklch, `px`/`rem`/`em`, and typography and CSS-in-JS/inline-style constructs.
- **Not inspected:** `src/styles/tokens.css` and `tokens/*.tokens.json` (token source and generated output — excluded by the skill, used here as the reference for what tokens exist); `*.stories.tsx` are excluded as fixtures, though the colour search covered them and found nothing; `apps/checkout/**` is outside the requested scope and was not assessed — it contains its own `.module.css` files and would likely change the totals materially.
- **How "none found" was checked:** The colour pattern was run as a positive control against `src/styles/tokens.css` and returned **15 hits**, confirming it matches this codebase — so the single colour hit in `src/components` is a real result, not a broken pattern. The spacing control likewise matched `16px`/`8px` in the token source. **The typography zero has no valid positive control**, because the token system defines no typography tokens for the pattern to find; that zero rests on the full read of all 10 files instead, which on a library this size is the stronger check.
- **Handed to `token-audit`:** `tokens/component.tokens.json:9` defines `card.border` against the primitive `{color.gray.200}` instead of `{color.border.default}`, and the generated `tokens.css:17` emits `--card-border: #e5e7eb` as a raw hex with **no dark-theme override**. That is a token *definition* problem, not consuming-code compliance, so it carries no TC- id here — but note it has a real consequence: `Card`'s border stays light grey in dark mode while `Dialog` and `Modal` borders correctly darken to `#374151`.
- **Assumptions:** `src/styles/tokens.css` is current and regenerated from `tokens/*.tokens.json`; light and dark are the only shipped themes.

If any of these values are deliberate — the `#1a73e8` title, the fixed radii, the 2px focus ring — tell me and I'll exclude them in future runs.

---

Want me to publish this as a shareable page for the team, or run `token-audit` next to cover the definition-side gaps this report keeps pointing at?
