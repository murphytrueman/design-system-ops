# Sample output: docs-coverage (fixture run)

**Skill:** `skills/docs-coverage`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `27c301d`
**Eval case:** `undocumented-component` in `tests/evals/cases.json`
**Date:** 2026-09-24
**Edited:** no. The report below is verbatim from a headless run with read-only tools; `tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case undocumented-component`; runs vary, so expect the same findings in different words.

---

All five components resolved cleanly against the story files. Here's the audit.

---

### Docs coverage report

**Date:** 2026-09-24
**Inventory:** 5 components (`src/index.ts` barrel) · **Surface audited:** Storybook CSF source (`*.stories.tsx`) · **Join confidence:** Tier A for all 5

**Summary**

Of 5 exported components, 4 have a story and 1 (`Tooltip`) has nothing. All 4 stories carry `tags: ['autodocs']`, so all 4 generate a docs page — but `Card`'s page documents no props, leaving it at the "exists" floor. Nothing in the library reaches the guided rung: there are no MDX files, no README, and no usage prose anywhere in the repo, so "when to use this" currently has nowhere to live. Coverage and rung placement are **measured**; staleness is **unmeasurable here** — the repo has a single commit, so every file shares one timestamp and git carries no drift signal. Nothing was estimated.

**Coverage by rung** — each component counted at the highest rung it reaches.

| Rung | Count | % of inventory |
|---|---|---|
| Guided (usage guidance) | 0 | 0% |
| Described (docs page + prop descriptions) | 3 | 60% |
| Exists (story, not clearing the described bar) | 1 | 20% |
| Undocumented (no surface) | 1 | 20% |

Per-component detail:

| Component | Story | Autodocs page | Own props described | Rung |
|---|---|---|---|---|
| Button | ✅ 2 stories | ✅ | 1/1 (`variant`) | Described |
| Modal | ✅ 1 story | ✅ | 3/4 (`children` undocumented) | Described |
| Dialog | ✅ 1 story | ✅ | 3/4 (`children` undocumented) | Described |
| Card | ✅ 1 story | ✅ | 0/1 (`title` undocumented) | Exists |
| Tooltip | ❌ | ❌ | 0/2 | Undocumented |

Ratios count props declared on each component's own interface; props inherited from `ButtonHTMLAttributes`/`HTMLAttributes` are excluded, since react-docgen's treatment of those varies by config.

**Findings**

**DC-01** 🟠 **High** · Coverage gap · Confidence: Tier A
`Tooltip` is exported from the public barrel with no story and no docs page.
*Evidence:* `src/components/Tooltip/Tooltip.tsx` exists and is exported at `src/index.ts:5`. `src/components/Tooltip/` contains only `Tooltip.tsx` and `Tooltip.module.css` — no sibling `.stories.tsx`. The four tracked story files (`git ls-files '*.stories.*'`) cover Button, Card, Dialog, Modal only.
*Action:* Add `Tooltip.stories.tsx` with `tags: ['autodocs']` and JSDoc on `label` and `children`. It renders `role="tooltip"` on an always-present span with no hover/focus trigger — a story would make that behaviour visible to whoever picks it up next.

**DC-02** 🟡 **Medium** · Coverage gap · Confidence: Tier A
`Card` has an autodocs page that describes none of its props.
*Evidence:* `Card.stories.tsx:4` sets `tags: ['autodocs']`, so a page generates; `CardProps` at `src/components/Card/Card.tsx:4-6` declares `title?: ReactNode` with no JSDoc and no `argTypes` in the story. The generated page will list `title` with an empty description column.
*Action:* One JSDoc line on `title` moves Card to the described rung. It's the only component with a real consumer in this repo (`apps/checkout/src/Summary.tsx:7`), so it's the cheapest win here.

**DC-03** 🟡 **Medium** · Coverage gap · Confidence: Tier A
No component reaches the guided rung, and `Modal` / `Dialog` show the cost.
*Evidence:* No `.md` or `.mdx` files exist anywhere in the repo (`find` over the tree, excluding `.git`), and a case-insensitive search for "when to use", "anti-pattern", "do not use" and "accessibility" across all files returned no matches. Meanwhile `Modal` and `Dialog` are both exported, both documented at the described rung, and near-identical in purpose — differing mainly in prop naming (`open`/`onClose`/`title` vs `isOpen`/`onDismiss`/`heading`) and element (`<div role="dialog">` vs `<dialog>`). Nothing on either surface tells a consumer which to pick.
*Action:* The duplication itself is a component-audit question, but either way the docs surface needs a decision recorded — a "when to use" section on both pages, or a decision page routing between them.

**Staleness: no signal available**

Not a finding, a measurement limitation. Every tracked file was introduced in the single commit `04ad19d` (2026-09-24T14:46:21+10:00), so every component-to-doc date delta is 0 days. That is zero by construction, not evidence that docs are current — I'd treat staleness as **unknown** for all 5 components until this repo has real change history.

**Orphaned documentation**

None. All 4 story files resolve to a component that exists in code.

**Action list**
- **Immediate:** DC-01 — add a Tooltip story.
- **Planned:** DC-02 (one JSDoc line); DC-03 (record the Modal/Dialog decision on both pages).
- **Review:** none — no Tier C matches were needed.

**Scope**
- **Inspected:** `src/index.ts` (inventory source); all 5 component sources and 4 story files under `src/components/`; `git log` over full history (1 commit, non-shallow); `find` for `.md`/`.mdx`/`docs/`; grep for usage-guidance prose across the tree; `apps/checkout/` for consumer fan-in.
- **Not inspected:** No Storybook `index.json` — there is no `.storybook/` config and no `storybook-static/` build, so the inventory came from CSF source rather than a built index. No Figma library, Zeroheight, Supernova or hosted docs site was configured (`.ds-ops-config.yml` absent), so designer-facing descriptions and any externally hosted pages are outside this audit.
- **How "none found" was checked:** The join resolves each story's relative `component` import to a source path — `Button.stories.tsx:2` imports `./Button` → `src/components/Button/Button.tsx`, which matches the inventory entry exactly. It also separates `Modal` and `Dialog` into distinct matches rather than collapsing the two similar components, so it discriminates. Applied to `Tooltip` it finds nothing because no story imports it. Rung 3's absence rests on there being no prose files in the repo at all, not on a pattern that might have missed them.
- **Assumptions:** The `src/index.ts` barrel is the public API, so all 5 exports need public docs. `tags: ['autodocs']` is taken at face value as generating a docs page; I did not build Storybook to confirm rendering.

> **A note on context:** This audit measures your documentation surface against your code — it does not see why a component was left undocumented or why a doc predates a change. Some gaps are deliberate (internal-only components) and some "stale" docs are still correct after a refactor. Tier C matches are best-guesses, not facts. If a finding describes an intentional choice, let me know — I'll calibrate future runs. The goal is to surface drift you haven't seen, not to second-guess decisions you've already made.
