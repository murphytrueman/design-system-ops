# Sample output: drift-detection (fixture run)

**Skill:** `skills/drift-detection`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `27c301d`
**Eval case:** `consumer-drift` in `tests/evals/cases.json`
**Date:** 2026-09-24
**Edited:** no. The report below is verbatim from a headless run with read-only tools; `tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case consumer-drift`; runs vary, so expect the same findings in different words.

---

# Drift detection report

**Date:** 2026-09-24
**Subject:** `apps/checkout` (`@fixture/checkout` 0.9.0) — 4 source files
**Reference source:** `@fixture/ui` 2.3.0 in this repo — `src/components/`, `src/styles/tokens.css`, `tokens/*.tokens.json`
**Assessment method:** Direct inspection of all consumer and system source files (the consumer is 4 files; nothing was sampled)

## Summary

The checkout app consumes the design system correctly in two places and bypasses it in one. `Summary.tsx:1` imports `Card` from `@fixture/ui`, and `Summary.module.css:8` uses the semantic token `var(--color-text-default)` — so the package is installed, reachable, and the team knows how tokens work. Against that, `CheckoutButton.tsx` is a from-scratch re-implementation of the system's `Button`, styled with three raw hex values and off-scale padding, with no focus treatment.

That matters most in dark mode. The system ships a `[data-theme="dark"]` block; the system `Button` follows it because it reads `--button-background`. `CheckoutButton` hardcodes `#2563eb`, so in dark mode the single most important button in the product renders in the light-theme brand colour while every other action switches around it.

Separately, and not the checkout team's fault, the design system itself leaks raw values at its own component-token tier — which means `Card` also renders incorrectly in dark mode *when used correctly*. Those are listed apart from the drift findings.

## Drift findings

| ID | Location | Dimension | Classification | Severity | Description | Recommended action |
|---|---|---|---|---|---|---|
| DF-01 | `apps/checkout/src/CheckoutButton.tsx:4` | API | Unclassified | 🟠 High | Local `CheckoutButton` re-implements the system `Button` (`src/components/Button/Button.tsx:9`). Accepts bare `ButtonHTMLAttributes`; the system component adds `variant?: 'primary' \| 'secondary'`. Consumers of checkout cannot select a secondary emphasis. | Replace with `<Button variant="primary">` from `@fixture/ui`; delete the local component and its stylesheet |
| DF-02 | `apps/checkout/src/CheckoutButton.module.css:2,3,11` | Token | Unclassified | 🔴 Critical | Raw hex where component tokens exist: `#2563eb` = `--button-background`, `#ffffff` = `--button-text`, `#1d4ed8` = `--button-background-hover`. All three equal the light-theme resolved values, so the button is invisible to the theme: under `[data-theme="dark"]` the system button becomes `#60a5fa`/`#111827` and this one stays `#2563eb`/`#ffffff`. | Fixed by DF-01. If the local component must survive, swap the three hex values for the `--button-*` variables |
| DF-03 | `apps/checkout/src/CheckoutButton.module.css:1-8` | Behavioural | Unclassified | 🟠 High | No `:focus-visible` rule. The system `Button` defines `outline: 2px solid var(--color-action-primary); outline-offset: 2px` (`Button.module.css:8-11`). The designed focus indicator is absent on the checkout CTA. | Fixed by DF-01. Confirm with design whether the browser default ring is acceptable in the interim |
| DF-04 | `apps/checkout/src/CheckoutButton.module.css:6,7,1` | Visual | Unclassified | 🟡 Medium | `padding: 12px 20px` vs the system's `var(--space-gap) var(--space-inset)` = `8px 16px`; neither 12px nor 20px exists in the system scale. Adds `font-weight: 600` (system sets none) and omits `cursor: pointer`. `border-radius: 6px` does match. | Fixed by DF-01 |
| DF-05 | `apps/checkout/src/Summary.module.css:2` | Token | E — system gap | 🟡 Medium | Overrides the system component token `--card-padding` to `24px`. The system resolves it to `var(--space-inset)` = 16px. 24px is not a value the system can express — `tokens/primitives.tokens.json:19-23` defines only `spacing.2` (8px) and `spacing.4` (16px). | Route to contribution workflow: add a 24px spacing step, or give `Card` a `padding`/`size` prop |

**Severity key:** 🔴 Critical · 🟠 High · 🟡 Medium · ⚪ Low

**On severity:** every finding sits on the checkout critical path, so each was elevated one level from its base rating per Step 4a. Base ratings were DF-01 Medium, DF-02 High (token drift breaking theming in a themed product), DF-03 Medium, DF-04 Low, DF-05 Low. DF-02 is Critical on theme-integrity grounds, not accessibility — `#ffffff` on `#2563eb` is ≈5.2:1 and still passes AA.

## Findings by classification

**Intentional divergence (A)** — none. No code comment, ADR, PR description or contribution doc anywhere in the repo records a decision to fork the button.

**Version lag (B)** — none established, and not measurable here. `apps/checkout/package.json:7` declares `@fixture/ui: ^2.2.0`; the system is at 2.3.0, which that range admits. There is no lockfile, so the resolved version cannot be verified, and no CHANGELOG or git tags, so releases cannot be diffed. No drifted behaviour matches an older system version, so nothing meets B's evidence rule.

**Accidental drift (C)** — none proven, though DF-01 to DF-04 are most consistent with it. See Unclassified.

**Misunderstanding (D)** — none. D requires quoting a passage that was plausibly misread. `Button` has no usage documentation to misread — only `Button.stories.tsx`, which shows the correct API. Absent docs is a root cause (below), not a D classification.

**System gaps (E)** — DF-05. Two verifiable facts support it: the spacing scale has no 24px step, and `Card` exposes no padding or size prop (`src/components/Card/Card.tsx:4-6`), leaving the CSS variable as the only lever. The team used the only mechanism available to them. Contribution candidate, not a mistake. Caveat: if 24px was picked arbitrarily rather than required, this is class C instead — the question below settles it.

**Unclassified — needs team input**

- **DF-01 through DF-04** (all one cause: `CheckoutButton` exists). Class A is out — nothing records a decision. Class E is out — `Button` demonstrably covers the need, with the same 6px radius and a token-driven primary variant. Class C's evidence rule cannot be met: it asks whether the local version predates the system one, and this repo has a single commit (`065a20d Initial commit`), so there is no history to read. One piece of evidence narrows it: `Summary.tsx` imports `Card` from `@fixture/ui` on line 1 and the local `CheckoutButton` on line 2 — the package was installed and working when the local button was written, which rules out "the system component wasn't available yet," the usual cause of C.
  **Question that classifies it:** *Was `CheckoutButton` written deliberately in preference to `@fixture/ui`'s `Button` — and if so, what did `Button` not do? Or was the team simply unaware `Button` was exported?* Deliberate with a reason → class A, and DF-04's padding becomes a contribution candidate. Unaware → class C.
- **DF-05.** *Was 24px card padding a requirement from design, or a value someone reached for because 16px looked tight?*

## Reference-integrity findings (design system, not drift)

These are defects in the reference itself. They are out of the drift scope you asked about, but two of them change how checkout renders today, so leaving them out would be misleading.

| ID | Location | Description |
|---|---|---|
| R-01 | `src/components/Card/Card.module.css:10` | `.title { color: #1a73e8 }` — a raw hex that is **not in the system palette** (nearest is `blue.500` `#2563eb`). It renders the "Order summary" heading in checkout, and does not respond to the dark theme. |
| R-02 | `src/styles/tokens.css:17` + `tokens/component.tokens.json:9` | `card.border` references the primitive `{color.gray.200}`, skipping the semantic tier that its sibling `card.background` → `{color.surface.raised}` uses. The generated CSS inlines it as `--card-border: #e5e7eb`. Consequence: **`Card`'s border does not change in dark mode** — it stays light grey while `--color-border-default` switches to `#374151`. Affects checkout's `Summary` card. |
| R-03 | `src/components/Modal/Modal.tsx` vs `src/components/Dialog/Dialog.tsx` | Near-duplicate components with divergent prop naming (`open`/`onClose`/`title` vs `isOpen`/`onDismiss`/`heading`). Neither is used by checkout, but it weakens the claim to a single source of truth. → `component-audit`, `component-api-validator`. |

## Root cause patterns

1. **The guardrail gap is at component creation, not token knowledge.** The checkout team used a semantic token correctly in the file next door. What failed is that a brand-new local component could land with three raw hex values and no focus style, and nothing objected — no lint rule, no CI check, no CODEOWNERS on the styling surface. Fixing DF-01 removes today's drift; adding the guardrail is what stops the next one.
2. **No governance artefacts exist, so drift is structurally unclassifiable.** No lockfile, no tags, no CHANGELOG, no ADRs, no contribution docs, no `.ds-ops-config.yml`. This is why four of five findings are Unclassified and why version lag can't be measured at all. It is the highest-leverage fix: it makes every future drift check answerable from evidence instead of from a conversation.
3. **The consumer copies a habit the system models.** The system hardcodes `#1a73e8` in `Card`, inlines `#e5e7eb` for `--card-border`, and hardcodes `border-radius` in both `Button` (6px) and `Card` (8px) with no radius token anywhere. A consumer that hardcodes a hex is imitating the reference, not defying it. Compliance asks of the consumer are hard to sustain while the system itself leaks.
4. **Where the scale is thin, consumers override.** The spacing scale has exactly two steps, and the one override in checkout supplies a third. Off-scale values in a consumer are usually a reading of the scale's coverage, not carelessness — DF-05 is the visible symptom.

## Recommended actions

1. **DF-02 (Critical) and DF-01/DF-03 (High) — one change.** Replace `CheckoutButton` with `Button` from `@fixture/ui` and delete `CheckoutButton.tsx` + `.module.css`. This closes DF-01 through DF-04 in a single small edit. → `design-to-code-check` to confirm the swap.
2. **Fix R-02 and R-01 in the system before asking checkout to comply.** Point `card.border` at `{color.border.default}` and replace `Card`'s `#1a73e8` title colour with a text token. Both are dark-theme correctness bugs affecting the checkout app right now. → `token-audit`, `theme-audit`.
3. **DF-05 (E) → contribution workflow.** Decide between a 24px spacing step and a `Card` padding prop. Either way the override at `Summary.module.css:2` is removed rather than blessed. → `contribution-workflow`.
4. **Put the two classification questions to the checkout team.** The answer to the DF-01 question determines whether DF-04's 12px/20px padding is a contribution candidate or a bug to erase.
5. **Add the guardrail and the governance baseline.** A Stylelint rule rejecting raw hex and off-scale px outside `src/styles/`, plus a lockfile, git tags and a CHANGELOG. → `governance-encoder`, `cicd-integration`.
6. **Address R-03** on its own track — it is library hygiene, not checkout drift.

## Scope

- **Inspected:** `apps/checkout` in full (4 files, all lines); `@fixture/ui` 2.3.0 — all 5 components, `src/index.ts`, `src/styles/tokens.css`, all 3 token files; `git log --all`, `git tag`.
- **Not inspected:** No Figma library was in scope, so Step 6's visual comparison was not run and no design-side screenshot evidence is in this report — visual findings are code-vs-code against the system's stylesheets. No other consuming product exists in this repo, so no cross-product pattern can be claimed. Step 4c (cross-system) was skipped: one system in scope.
- **How "none found" was checked:** The raw-value search over `apps/checkout` used one regex covering hex, `px` and `!important` together. It returned 7 hits for hex/px and 0 for `!important` in the same run — the hits are the positive control that makes the `!important` zero meaningful. A separate search for local custom-property declarations returned exactly 1 hit (`--card-padding`), confirming that search was live too.
- **Deviation from the skill:** the token dimension should normally import a `token-compliance` report rather than re-running the search here. No such report exists, and the consumer's entire styling surface is two files totalling 13 lines, every one of which I read. A separate run would have added a step without adding evidence. DF-02 and DF-05 therefore carry drift IDs, not token-compliance IDs.
- **Assumptions:** `src/styles/tokens.css` is the built artefact the app actually loads (its header says it is generated from `tokens/*.tokens.json`, and the two agree). `--card-padding` set on `.summary` does reach `Card` — verified: `Summary.tsx:7` passes the class to `Card`, which merges it onto the same element that reads the variable.

---

> **A note on context:** This analysis identifies where implementations differ from the system — it cannot always tell why. The classification system (intentional, accidental, version lag, misunderstanding, system gap) is a starting point. If any instance is misclassified, let me know — your corrections make future drift checks more accurate. The goal is to distinguish the drift that needs fixing from the drift that needs documenting.
