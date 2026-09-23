# Sample output: docs-coverage (fixture run)

**Skill:** `skills/docs-coverage`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it
**Eval case:** `undocumented-component` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools, against the fixture as of commit `bc84ffe`. The fixture has changed since, so a rerun won't match line for line. Rerun it with `python3 tests/evals/run_evals.py --case undocumented-component`.

---

Here's the audit.

---

### Docs coverage report

**Date:** 2026-09-23
**Inventory:** 3 components (from the `src/index.ts` barrel) · **Surfaces audited:** `*.stories.tsx` source files (per your instruction) · **Join confidence:** Tier A-equivalent — path-resolved

**Summary**

Two of your three exported components (Button, Card) have a story with `tags: ['autodocs']`, so they reach *described*. Tooltip has no story at all — it's the one real gap. Nothing in the library reaches *guided*: there's no MDX, no "when to use" prose, no usage-guidance surface of any kind. Coverage and orphans are measured facts here; **staleness is not testable** — the repo has a single commit (`3ab46e4 Initial commit`), so every component and every story carries the identical timestamp `2026-09-23T21:01:14+10:00`. No doc can predate its component in a one-commit history, so a "0 stale docs" result would be meaningless rather than clean.

**Coverage by rung**

| Rung | Count | % of inventory |
|---|---|---|
| Guided (usage guidance) | 0 | 0% |
| Described (autodocs page, no usage guidance) | 2 | 67% |
| Exists (≥1 story, no docs page) | 0 | 0% |
| Undocumented (no surface) | 1 | 33% |

**Findings**

**DC-01** · 🟠 High · Coverage gap · Join: Tier A-equivalent (path-resolved)
`Tooltip` is exported from `src/index.ts:5` and implemented at `src/components/Tooltip/Tooltip.tsx`, but `src/components/Tooltip/` contains only `Tooltip.tsx` and `Tooltip.module.css` — no `Tooltip.stories.tsx`. It's a public component at rung 0: consumers get it from the barrel with nothing to look at. Not rated Critical because it isn't foundational in the Button/Input/Text/Icon sense, but it's the only component on the shelf with no surface at all.
**Action:** add `Tooltip.stories.tsx` with `tags: ['autodocs']`, matching the Button/Card pattern. Tooltip's props are minimal (`label`, `children`), but its behaviour isn't — the bubble is always rendered with `role="tooltip"` and no hover/focus trigger or `aria-describedby` link, which is exactly the kind of thing a story plus usage notes should pin down.

**DC-02** · 🟡 Medium · Coverage gap · Join: Tier A-equivalent
No component reaches rung 3. Both story files are pure CSF with no companion MDX, and there are no `.mdx` files anywhere in the repo. Autodocs will generate props tables from the TS types, which gets Button and Card to *described*, but nothing tells a consuming team when to reach for a Card versus a plain container, or which Button variant means what.
**Action:** this is the layer to raise once Tooltip is covered — an MDX page per component, or `parameters.docs.description`, starting with Button.

**DC-03** · ⚪ Low · Coverage gap (story depth) · Join: Tier A-equivalent
`Card.stories.tsx` exports one story (`Default`) that always passes `title`. `CardProps.title` is optional (`src/components/Card/Card.tsx:5`), so the untitled rendering path — the `title ? … : null` branch at line 11 — is never shown. Button is better here: both `variant` values have a story.
**Action:** add an untitled Card story when convenient.

**DC-04** · ⚪ Low · Scope observation
Both story files import from `@storybook/react`, but `package.json` declares no `devDependencies` and no Storybook dependency, and the repo has no `.storybook/` config and no `storybook-static/` build. The stories are valid CSF source and I audited them as the documentation surface as you asked — but nothing in this repo currently builds or serves them, so "documented" here means "a story file exists," not "a page a developer can open."

**Staleness**

Not assessed — **unknown**, not clean. Git history is one commit deep; `git log -1 --format=%cI` returns `2026-09-23T21:01:14+10:00` for all five files checked (both components with stories, both story files, and Tooltip). Every doc is exactly the same age as its component, so the `component_last_change − doc_last_change > 90 days` rule cannot fire. Re-run this once the repo has real history.

**Orphaned documentation**

None. Both story files resolve to a component that exists: `Button.stories.tsx:2` imports `./Button`, `Card.stories.tsx:2` imports `./Card`, and both targets are present and exported from the barrel.

**Action list**
- **Immediate:** DC-01 — write `Tooltip.stories.tsx`.
- **Planned:** DC-02 — add usage guidance to lift Button and Card off rung 2; DC-03 — untitled Card story.
- **Review:** DC-04 — decide whether Storybook is meant to run from this package or lives in a consuming app.

**Scope**
- **Inspected:** `src/index.ts` (barrel, used as the inventory source); all three component sources under `src/components/`; both `*.stories.tsx` files, read in full; `package.json`; a full glob of the repo tree; `git log -1 --format=%cI` per file.
- **Not inspected:** no hosted docs platform was configured or reachable — there is no `.ds-ops-config.yml` in the repo, so no Zeroheight, Supernova or custom site was queried. No `storybook-static/index.json` and no `.storybook/` config exist, so the join was made from CSF source rather than a built Storybook index. If documentation for these components lives outside this repo, it isn't in this report.
- **How "none found" was checked:** the join reads each story's default-export `meta.component` together with its relative import, which resolves to an exact file path — Tier A-equivalent, though derived from source rather than an `index.json` `componentPath`. Positive control: it matches `Button.stories.tsx` → `src/components/Button/Button.tsx`, a pairing I confirmed by reading both files, so the key fits this codebase. Tooltip's gap was then confirmed by a full-tree glob: `src/components/Tooltip/` holds only `Tooltip.tsx` and `Tooltip.module.css`. The rung-3 absence rests on the same glob (zero `.mdx` files repo-wide) plus reading both story files end to end. Rung 2 is a genuine reading of `tags: ['autodocs']` in each meta — not an unknown.
- **Assumptions:** the `src/index.ts` barrel is the public API, so the inventory is 3 components and contains no internal-only components; `tags: ['autodocs']` counts as reaching *described*, on the basis that autodocs generates a props table from the exported TS interfaces.

> **A note on context:** This audit measures your documentation surface against your code — it does not see why a component was left undocumented or why a doc predates a change. Some gaps are deliberate (internal-only components) and some "stale" docs are still correct after a refactor. Tier C matches are best-guesses, not facts. If a finding describes an intentional choice, let me know — I'll calibrate future runs. The goal is to surface drift you haven't seen, not to second-guess decisions you've already made.

---

Two notes on how this run went: the `git log` calls succeeded, but my first `ls`/`cat` call was denied by permission mode, so the inventory came from Glob and Read instead — same result, no degradation. All three knowledge-note references the skill depends on were present, so this is a full-fidelity run, not degraded mode.
