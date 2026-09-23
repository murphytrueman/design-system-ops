# Sample output: docs-coverage (fixture run)

**Skill:** `skills/docs-coverage`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `59a43fa`
**Eval case:** `undocumented-component` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools. Rerun it with `python3 tests/evals/run_evals.py --case undocumented-component`; runs vary, so expect the same findings in different words.

---

Of the 3 exported components, 2 (Button, Card) have stories with autodocs and 1 (Tooltip) has no documentation at all. Nothing is orphaned, and staleness can't be measured here — the repo has a single commit, so every file shares one timestamp.

---

### Docs coverage report

**Date:** 2026-09-23
**Inventory:** 3 components · **Surfaces audited:** `*.stories.tsx` (source files; no Storybook build or index available) · **Join confidence:** Tier A (resolved file path)

**Summary**

Small library, clean structure, one real gap. The barrel at `src/index.ts` exports exactly three components and the directory glob agrees — no hidden internal components to discount. Button and Card each have a co-located story file with `tags: ['autodocs']`, putting them on rung 2. Tooltip has a source file and a stylesheet but no story, so it ships from the public barrel with nothing on any documentation surface. Nothing reaches rung 3: there's no MDX, no "when to use" prose, and no usage-guidance file anywhere in the repo.

Two signals were **measured**: coverage (file-path join against story files) and orphans. One is **unavailable**: staleness. Git history is a single commit (`c095aa1`, 2026-09-23T22:17:14+10:00) touching all 14 tracked files, so every component and every story carry the identical timestamp. The rule returns a zero-day delta for everything, which is not evidence that docs are keeping pace — it's an artefact of a one-commit history. Treat staleness as unknown until the repo accumulates history.

**Coverage by rung** (each component counted at its highest rung; rows are mutually exclusive)

| Rung | Count | % of inventory |
|---|---|---|
| Guided (usage guidance) | 0 | 0% |
| Described (docs/autodocs page, no usage guidance) | 2 | 67% |
| Exists (≥1 story, no docs page) | 0 | 0% |
| Undocumented (no surface) | 1 | 33% |

**Findings**

**DC-01** · 🟠 High · Coverage gap · Confidence: **Tier A** (file path)
`Tooltip` is exported publicly from `src/index.ts:5` but has no `Tooltip.stories.tsx` in `src/components/Tooltip/`, and no other documentation surface exists in the repo. It's the only component in the library with interaction and accessibility behaviour worth explaining — it renders a `role="tooltip"` element (`src/components/Tooltip/Tooltip.tsx:13`) and takes a `label` + `children` composition that isn't self-evident from the type signature. Consumers currently have to read the source.
**Action:** add `src/components/Tooltip/Tooltip.stories.tsx` matching the Button/Card pattern (`meta.component`, `tags: ['autodocs']`), with at least a default story and one showing the wrapped-trigger composition.

**DC-02** · 🟡 Medium · Coverage gap · Confidence: **Tier A**
No component reaches rung 3. Button's `variant` prop has a one-line JSDoc (`src/components/Button/Button.tsx:5`) and that is the whole of the guidance layer — nothing says when to use `primary` vs `secondary`, when a Card is the wrong container, or what the anti-patterns are. Autodocs will render props and variants; it won't answer "should I use this here?"
**Action:** this is a deliberate next step rather than a defect. If you want it, `usage-guidelines` writes the rung-3 layer per component.

**DC-03** · ⚪ Low · Coverage gap (evidence quality) · Confidence: **Tier A**
Rung 2 for Button and Card rests entirely on `tags: ['autodocs']` in the story files. There is no `.storybook/` config directory in the repo and `package.json` declares no Storybook dependency (only a `react` peer dependency), so nothing here actually builds those docs pages. The declaration is credible — the stories import `@storybook/react` types correctly — but I could not verify a rendered docs page exists.
**Action:** if the Storybook config lives in a parent repo or app workspace, this is a non-finding; tell me and I'll skip it. If not, the described rung is aspirational rather than shipped.

**Staleness** — ⚪ unmeasurable, not clean. All five component and story files last changed at the same instant in the single initial commit. No file is stale under the 90-day default threshold, but with zero history behind it that result carries no information. Re-run once the repo has a few commits.

**Orphaned documentation** — none. Both story files resolve to a component that exists: `Button.stories.tsx` → `./Button` (exists), `Card.stories.tsx` → `./Card` (exists). No story titles point at deleted or renamed symbols.

**Action list**
- **Immediate:** DC-01 — write a Tooltip story. It's the only component a consumer can't discover in the workbench, and it's the one with behaviour that needs showing.
- **Planned:** DC-02 — decide whether rung 3 is in scope for a three-component library. At this size the answer may legitimately be "not yet."
- **Review:** DC-03 — confirm where Storybook is configured. Re-run staleness after the repo builds up commit history.

**Scope**
- **Inspected:** `src/index.ts` (barrel, used as the inventory source), all three component directories under `src/components/`, both `*.stories.tsx` files read in full, `package.json`, and `git log --name-only` over the full history (1 commit, full clone — no `.git/shallow`).
- **Not inspected:** no Storybook static build (`storybook-static/index.json`) or running server exists in this repo, so no index was parsed; no hosted docs platform is configured (`.ds-ops-config.yml` is absent) and none was queried; the `tokens/` directory and `src/styles/tokens.css` are out of scope for docs coverage.
- **How "none found" was checked:** the join key is co-located source path — `<Dir>/<Name>.stories.tsx` alongside `<Dir>/<Name>.tsx`, cross-checked against the story's relative `component` import. Positive control: I opened `Button.stories.tsx` and confirmed it declares `component: Button` importing `./Button`, and the key matched it; same for Card. So the key does find documented components in this codebase, which is what makes Tooltip's miss a real gap rather than a key failure. A repo-wide glob confirms only two `*.stories.tsx` files exist and no `.mdx`, README, or docs directory is present. Rung 3 is reported as **absent**, verified by that same glob; rung 2 is reported from story `tags` and was not verified against a rendered build (DC-03).
- **Assumptions:** the public barrel is the right inventory — all three exports resolve to real files and the directory glob finds no fourth component, so there are no unexported internals being over- or under-counted. `tags: ['autodocs']` is taken as evidence of a docs page. Story files are the sole documentation surface, per your instruction.

> **A note on context:** This audit measures your documentation surface against your code — it does not see why a component was left undocumented or why a doc predates a change. Some gaps are deliberate (internal-only components) and some "stale" docs are still correct after a refactor. Tier C matches are best-guesses, not facts. If a finding describes an intentional choice, let me know — I'll calibrate future runs. The goal is to surface drift you haven't seen, not to second-guess decisions you've already made.

---

Two notes on how this ran: Bash was restricted in this session, so a few command forms were denied — I got the git history I needed through an allowed form, and everything else came from the file tools, so no part of the audit was skipped. All three of the skill's reference notes were present, so this is not a degraded-mode report.
