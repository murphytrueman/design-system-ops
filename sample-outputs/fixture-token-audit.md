# Sample output: token-audit (fixture run)

**Skill:** `skills/token-audit`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `27c301d`
**Eval case:** `tier-leakage` in `tests/evals/cases.json`
**Date:** 2026-09-24
**Edited:** no. The report below is verbatim from a headless run with read-only tools; `tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case tier-leakage`; runs vary, so expect the same findings in different words.

---

# Token audit report

**Your dark theme is the problem.** It exists only inside the file that claims to be generated output, and one component token has a raw hex that the theme switch can't reach — so Cards render a light border in dark mode today. Three critical findings, all in the same blast radius. The naming and tier discipline underneath is genuinely good.

## Token sources found

```
tokens/primitives.tokens.json    12 tokens (DTCG 2025.10, colour + spacing)
tokens/semantic.tokens.json       9 tokens (DTCG, all aliases)
tokens/component.tokens.json      6 tokens (DTCG, all aliases)
src/styles/tokens.css            15 custom properties + 7 dark-theme overrides
Total: 27 declared tokens, one generated CSS output
```

No Style Dictionary config, no Tailwind config, no SCSS, no `.resolver.json`, no `.ds-ops-config.yml`, and no `scripts` block in either `package.json`. **There is no build pipeline in this repo** — despite `src/styles/tokens.css:1` saying "Generated from tokens/*.tokens.json". That matters for TA-01.

## Orphan detection

```
27 tokens declared (JSON), 15 custom properties (CSS)
CSS:  15 of 15 consumed by a component — 0 orphans
JSON: 8 of 12 primitives referenced by a semantic token
      4 orphan candidates: color.blue.300, color.blue.400, color.gray.700, color.gray.800
Positive control: var(--color-action-primary) found in 4 files / 5 sites, so the pattern works here
Not checked: consuming repos outside this one
```

Those 4 orphans aren't dead. Their hex values (`#93c5fd`, `#60a5fa`, `#374151`, `#1f2937`) all appear in the hand-written dark block at `src/styles/tokens.css:22-30`. They are the dark palette — used by CSS, invisible to the token graph. That's TA-01 from the other direction.

## Tier structure

| Tier | Status | Why |
|---|---|---|
| Primitive | 🟡 Functional | Correct 2025.10 value shapes, clean scale naming. Spacing has 2 steps; radius absent entirely |
| Semantic | 🟡 Functional | Genuinely intent-named, all references downward, no appearance names anywhere. Missing states |
| Component | 🟠 Weak | 6 tokens; 1 of 6 leaks to a primitive, and that one breaks theming |

**Tier leakage instances: 1** (plus its flattened consequence in generated CSS).

## Findings

**TA-01 · 🔴 Critical · Value** — The dark theme exists only in generated output.
`src/styles/tokens.css:22-30` declares `[data-theme="dark"]` with 7 hand-written hex values. No dark theme exists in `tokens/` — no second value per token, no dark set, no `.resolver.json`. Line 1 of that file declares it generated from `tokens/*.tokens.json`. Anyone who regenerates it deletes your dark theme, and no build config exists in the repo to tell them otherwise.
→ Move theming into the source. DTCG 2025.10 resolvers are the mechanism: a `theme` modifier with `light`/`dark` contexts over the semantic file. The 4 orphan primitives already hold the values you need.

**TA-02 · 🔴 Critical · Value** — `--card-border` is a raw value at the component tier, and it breaks dark mode.
`src/styles/tokens.css:17` — `--card-border: #e5e7eb;`. Every other component property on that line range aliases (`--card-background: var(--color-surface-raised)`). The dark block redefines `--color-border-default` to `#374151` at line 28, but `--card-border` neither aliases it nor gets redefined. `Card.module.css:3` consumes it. **Cards keep a light-grey border in dark mode right now.**
→ `--card-border: var(--color-border-default);`

**TA-03 · 🔴 Critical · Naming** — `card.border` skips the semantic tier.
`tokens/component.tokens.json:9` — `"border": { "$value": "{color.gray.200}" }`. The other five component tokens reference semantics correctly. This is the source-side cause of TA-02: primitives are never emitted as CSS custom properties, so the primitive reference had nowhere to point and got flattened to a literal hex.
→ `{color.border.default}` — same resolved value today, but it themes. Fixing this fixes TA-02 at the root. **Sequencing note: don't regenerate to apply this until TA-01 is resolved, or you'll lose the dark theme.**

**TA-04 · 🟡 Medium · Naming** — The spacing category has two names.
`tokens/primitives.tokens.json:19` uses `spacing`; `tokens/semantic.tokens.json:19` uses `space`. One category, two prefixes across adjacent tiers — autocomplete and search split in half.
→ Pick one. `space.*` at both tiers is the smaller diff (2 primitive tokens to rename).

**TA-05 · 🟡 Medium · Coverage** — Only `default` and `hover` states exist.
No `active`/`pressed`, `disabled`, or `focus`; no feedback roles (`error`, `success`, `warning`). This isn't hypothetical: `Button.module.css:8-10` builds its focus ring from `var(--color-action-primary)` because no focus token exists. The ring and the fill are now the same colour by necessity, not by choice.
→ Add `color.focus.ring` and `color.action.disabled` first — those two have live consumers.

**TA-06 · 🟡 Medium · Coverage** — No radius tokens at any tier.
Three distinct values hardcoded across five components: `4px` (Tooltip:10), `6px` (Button:4), `8px` (Card:5, Modal:12, Dialog:5). A whole token category is missing, not just values within one.
→ Add `radius.sm/md/lg` primitives and a semantic mapping.

**TA-07 · 🟡 Medium · Coverage** — The spacing scale is too thin to reference.
Two steps only: `spacing.2` (8px), `spacing.4` (16px). Consumers reach past it — `apps/checkout/src/Summary.module.css:2` sets `--card-padding: 24px`, `apps/checkout/src/CheckoutButton.module.css:6` uses `padding: 12px 20px`. Three off-scale values because the scale has no 12, 20, or 24.
→ Fill the 4px-grid steps (`spacing.1/3/5/6`). The override at `Summary.module.css:2` is otherwise a legitimate use of a component token — that's what they're for.

**TA-08 · 🟡 Medium · Coverage** — Component tokens cover Card but not its siblings.
`Modal.module.css:9-12` and `Dialog.module.css:2-5` are the same container recipe as Card — `surface-raised` background, `border-default` border, `space-inset` padding, 8px radius — but reference semantics directly while Card gets `--card-*`. If Card's component tokens exist because consumers needed an override point (and `Summary.module.css:2` suggests they did), Modal and Dialog have the same need and no hook. If the scoping is deliberate, say so and I'll drop it.

**TA-09 · ⚪ Low · Coverage** — 4 of 12 primitives are unreferenced by the token graph (below the 20% threshold). All four are the stranded dark palette — see TA-01. They resolve themselves when theming moves into source.

**TA-10 · ⚪ Low · Naming** — State is flattened into the property segment: `button.background-hover` (`component.tokens.json:4`) rather than `button.background.hover`. Consistent with `color.action.primary-hover` at the semantic tier, so this reads as a deliberate convention rather than drift — flagging only because it means the tree can't be queried by state. Your call.

**Checks that passed:** no appearance-named semantic tokens; no upward references; no duplicate primitive values; no ambiguous names (`default`/`base` here sit beside real roles, which is correct); no platform suffixes in names.

## DTCG 2025.10 alignment

Your primitives are genuinely 2025.10, not an older draft — colours use the `colorSpace`/`components` object form, dimensions use `{value, unit}`. Names are clean of `$`, `{`, `}`, `.`.

**Don't "fix" the missing `$type` in the semantic and component files.** Every token in both is an alias, so its type resolves through the referenced token per the 2025.10 type-resolution order. Those files are valid as they stand.

The real DTCG gap is the absent resolver — it's the spec's mechanism for exactly the theming problem in TA-01, and building one is the fix, not an extra.

I did not run `schema-validator`, so these are surface observations. Run it for real structural validation (alias integrity, composite shapes) before any migration work.

## Remediation priority

**Fix first** — theming is broken in production
1. TA-01 → build the resolver, move dark into source
2. TA-03 → repoint `card.border` to `{color.border.default}`
3. TA-02 → regenerate (only after TA-01)

**Fix next** — compounds as the system grows
4. TA-04 (`space`/`spacing`), TA-05 (focus + disabled states)

**Address eventually**
5. TA-06 (radius), TA-07 (spacing steps), TA-08 (Modal/Dialog tokens), TA-10

## Effort estimates

| Finding | Effort | Assumptions | Confidence |
|---|---|---|---|
| TA-01 | 6–12 h | Includes standing up a build step, since none exists. Token-side only — consumer migration extra | Medium |
| TA-02 + TA-03 | 30–60 min | Done together; assumes TA-01 landed first | High |
| TA-04 | 1–2 h | 2 primitive renames + 2 semantic references; no external consumers on `spacing.*` | Medium |
| TA-05 | 3–6 h | Adding tokens only; retrofitting Button's focus ring is extra | Medium |
| TA-06 | 2–4 h | Assumes 3 steps suffice and 4/6/8px are intentional, not accidental | Medium |
| TA-07 | 2–3 h | Assumes a 4px grid; 20px in CheckoutButton needs a call | Low — scope whether 20px is deliberate |
| TA-08 | 2–4 h | Assumes Modal/Dialog should match Card; needs a decision first | Low — decision, not just work |

Under 30 tokens and one in-repo consumer, so no spike needed before sprint planning.

## Scope

- **Inspected:** `tokens/primitives.tokens.json`, `tokens/semantic.tokens.json`, `tokens/component.tokens.json`, `src/styles/tokens.css`, all 5 component stylesheets in `src/components/`, both stylesheets in `apps/checkout/src/`, all `.tsx` files (grepped for hex/inline styles — none found), `src/index.ts`, both `package.json` files.
- **Not inspected:** consuming repos outside this one; Figma; `schema-validator` and `codebase-index` were not run.
- **How "none found" was checked:** the `var(--…)` orphan pattern resolves `--color-action-primary` across 4 files / 5 sites, so it works on this codebase. The hex pattern finds values in `tokens.css` and `CheckoutButton.module.css`, so its zero result in `.tsx` is real.
- **Assumptions:** `src/styles/tokens.css` is intended as generated output (its own header says so); `apps/checkout` is a representative consumer; the 4px grid is intended.

**Two things I deliberately left to other skills:** hardcoded values in consuming code are `token-compliance`'s job, and there are live ones — `Card.module.css:11` uses `#1a73e8`, a blue that isn't in your primitive scale at all, and `CheckoutButton.module.css:2-11` re-types three exact token values as hex. Blast-radius mapping needs `codebase-index` run first. You have no Figma file configured; if you do have one, I can run `figma-variable-audit` against this same token source so the two reports line up by name.

> **A note on context:** This audit sees your token files — it does not see the decisions behind them. Some findings may flag patterns your team chose deliberately. If any finding describes an intentional decision, let me know — I'll exclude it from future runs and learn your system's conventions. The goal is to surface problems you haven't seen yet, not to second-guess choices you've already made.
