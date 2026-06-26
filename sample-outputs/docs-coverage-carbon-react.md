# Sample output: Docs coverage

**Skill:** `skills/docs-coverage`
**Source:** IBM Carbon Design System — React package, public Storybook `index.json` (`react.carbondesignsystem.com/index.json`) + GitHub commit history (`carbon-design-system/carbon`)
**Assessment method:** Storybook static index (v5, 604 entries) joined to the component source directory via `componentPath`; staleness from git commit dates. No integration beyond the public build and repo.
**Library type:** Mature open-source design system (React), used here as a neutral, reproducible example. All figures are real and re-checkable as of the date below.

---

## Docs coverage report

**Date:** 2026-06-26
**Inventory:** 126 components in `packages/react/src/components` · **Surfaces audited:** Storybook (autodocs + MDX usage pages) · **Join confidence:** Tier A for the storied set (`componentPath`), Tier B/C for the code-vs-index diff

Carbon is a strong documentation system, and this report reads like one: almost every component that has a story also has an autodocs page, and most carry a hand-written MDX usage page on top. The coverage floor is not the problem. The two things worth your attention are a **staleness tail in the MDX usage pages** — a handful predate their component's code by nearly a year — and **37 component directories in code with no story**, most of which are sub-components or internal utilities by design, leaving a small number of genuine candidates. Here is the breakdown, with confidence attached to every finding.

### Coverage by rung

| Rung | Count | % of inventory | Notes |
|---|---|---|---|
| **Exists** (≥1 Storybook story) | 89 | 71% | Joined by `componentPath` (Tier A) |
| **Described** (autodocs page) | ~87 of 89 storied | — | Nearly every storied component has an autodocs page |
| **Guided** (hand-written MDX usage page) | partial | — | Present for many components; this is where staleness concentrates |
| **Undocumented** (no story at all) | 37 | 29% | Name-based diff (Tier B/C) — see DC-03, needs confirmation |

> The rung counts are honest about their join. The storied set is matched on resolved file path (`componentPath`) — high confidence. "Undocumented" is a name-based diff of code directories against the storied set, so it is a hypothesis to confirm, not a fact (DC-03).

### Findings

| ID | Severity | Category | Confidence | Finding |
|---|---|---|---|---|
| DC-01 | 🟠 High | Staleness | High (git both sides) | **`Accordion` usage doc predates its code by ~363 days.** `Accordion.mdx` last changed 2025-06-19; the component source last changed 2026-06-17. A year of component changes have shipped since the usage page was touched — confirm the documented props, anatomy, and examples still match. |
| DC-02 | 🟠 High | Staleness | High (git both sides) | **`Tooltip` usage doc predates its code by ~320 days.** `Tooltip.mdx` last changed 2025-06-19; source last changed 2026-05-05. Same risk as DC-01 — verify against the current API. |
| DC-03 | 🟡 Medium | Coverage gap | Tier B/C (name match) | **37 component directories exist in code with no Storybook story.** This is a name diff (code dir vs storied set) and must be triaged before it is treated as a gap — see the breakdown below. The genuine-candidate subset is small. |
| DC-04 | 🟡 Medium | Join quality | Tier B | **9 storied components have no `componentPath` in the index.** These were matched by title/name, not resolved path, so their coverage status is lower-confidence. Worth confirming the stories declare `meta.component` so future audits get a Tier A join. |
| DC-05 | ⚪ Low | Coverage (positive) | Tier A | **The described layer is excellent.** Nearly all 89 storied components carry an autodocs page — the rung-1-to-rung-2 step, where many systems leak, is effectively complete here. Noted so it is not mistaken for an absence. |

### DC-03 triage — the 37 "undocumented" directories

A naive diff would report "37 undocumented components." Most are not gaps. Splitting them by likely intent (Tier C — confirm with the team):

- **Sub-components, documented under a parent (20):** `AccordionItem`, `BadgeIndicator`, `BreadcrumbItem`, `CheckboxGroup`, `DatePickerInput`, `FluidDatePickerInput`, `FluidTimePickerSelect`, `FormItem`, `InlineCheckbox`, `ListBox`, `ListItem`, `OverflowMenuItem`, `RadioButtonGroup`, `RadioTile`, `SelectItem`, `SelectItemGroup`, `Tab`, `TabContent`, `TileGroup`, `TimePickerSelect`. These compose into a parent (`Accordion`, `Tabs`, `Select`…) that *is* documented. Expected, not a gap.
- **Internal utilities / infrastructure / legacy (9):** `Copy`, `FeatureFlags`, `HideAtBreakpoint`, `Icon`, `Icons`, `LayoutDirection`, `Plex`, `Portal`, `ToggleSmall`. Not user-facing components (or, like `ToggleSmall`, deprecated); documenting them as components would be noise.
- **Button variants (3):** `PrimaryButton`, `SecondaryButton`, `DangerButton`. Likely covered by `Button`'s variant docs — confirm the variant is shown there.
- **Genuine candidates to confirm (5):** `PageHeader`, `ExpandableSearch`, `Switch`, `Disclosure`, `FlexGrid`. These are the only entries worth a real "should this have its own story/doc?" conversation.

The point of the skill is this split: 20 + 9 + 3 + 5 = 37. The raw number is 37; the actionable number is closer to 5.

### Orphaned documentation

None detected. Every storied entry resolves to a component directory that still exists in code — no doc pages left behind by a removal.

### Action list

**Immediate**
- Confirm and refresh the stale usage pages: `Accordion` (DC-01) and `Tooltip` (DC-02). Both are ~1 year behind a component that has since changed.

**Planned**
- Walk the 5 genuine candidates from DC-03 with the team — decide per component whether a story/doc is wanted, and close the loop either way.
- Add `meta.component` to the 9 stories missing `componentPath` (DC-04) so future runs get an exact join.

**Review**
- The 21 sub-components and 8 utilities from DC-03: confirm once that they are intentionally not standalone-documented, then add them to an ignore list so they stop surfacing in recurring runs.

---

> **A note on context:** This audit measures the documentation surface against the code — it does not see why a component was left without its own story or why a usage page predates a change. Carbon's overall documentation health is strong; the findings here are the long tail. The sub-component and utility classifications in DC-03 are best-guesses from names (Tier C), not facts — confirm them and I'll calibrate future runs. "Stale" means a doc predates a code change, which is a prompt to verify, not proof the doc is wrong.

---

*Generated by Design System Ops — `skills/docs-coverage` skill*
*Source: IBM Carbon Design System (React) — public Storybook index (v5) + GitHub commit history, as of 2026-06-26*
