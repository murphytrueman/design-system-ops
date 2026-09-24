---
name: docs-coverage
description: "Audit whether docs keep pace with components: undocumented components, stale docs, orphaned pages, with join confidence. Triggers: docs coverage, which components are undocumented, stale docs check. Not for writing docs (usage-guidelines) or doc analytics (adoption-report)."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(git log:*), Bash(git ls-files:*)
references:
  - ../../knowledge-notes/documentation-coverage.md
  - ../../knowledge-notes/output-discipline.md
  - ../../knowledge-notes/adoption-measurement.md
---

# Docs coverage

A skill for auditing whether a design system's documentation surface keeps pace with its components. It measures the code (the source of truth for what exists) against each documentation surface and reports three things: **coverage gaps** (components with no documentation), **staleness** (documentation that predates the component's last code change), and **orphaned docs** (pages for components that no longer exist). Produces a severity-rated finding table with per-signal confidence labelling.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Code is the source of truth for what components exist; the documentation surface is measured against it. A component in code with no docs is a coverage gap; a page for a deleted component is an orphan; a page older than the component's last change is a staleness risk.

This skill is built to work with **no integration at all**: a components directory plus a Storybook build plus git history answer coverage and staleness for most teams. Hosted platforms (Zeroheight, Supernova, custom docs sites) are optional layers that light up when configured — never prerequisites. The audit never blocks on an integration; it logs what is unavailable and proceeds with what it can reach.

The hard part is trust. Coverage is a join between two lists — components in code and entries in the doc surface — and the join is only as reliable as the key that links them. Every coverage finding carries a confidence tier so a fuzzy guess is never presented as a fact. See `documentation-coverage.md` for the full model.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `system.framework` — affects how component files are discovered (e.g. `.tsx` / `.vue` / `.twig`)
- `severity.*` — severity-rating overrides
- `integrations.storybook.static_path` — local Storybook build directory (e.g. `storybook-static`); the preferred source
- `integrations.storybook.url` — published Storybook URL for pulling `/index.json` when no local build exists
- `integrations.documentation` — optional hosted platform: `platform`, `url`, `api_key_env`, plus `styleguide_id` (Zeroheight) or `design_system_id` (Supernova)
- `integrations.github` — change history when the audit runs outside a local clone
- `docs_coverage.staleness_threshold_days` — grace window before a doc is flagged stale (default 90)
- `recurring.*` — trend comparison (see Recurring workflow)

## Auto-pull integrations

**Storybook — the primary surface (`integrations.storybook.enabled: true` or a local build):**
- Prefer a local static build: read the index from `integrations.storybook.static_path` (default `storybook-static/index.json`). No server, no auth.
- If only a URL is configured, fetch `<url>/index.json`.
- **No build and no URL:** read the CSF files directly. `*.stories.*` grouped by their `title` (or the default export's `component`) give rung 1; a `tags: ['autodocs']` entry or a sibling MDX file gives a docs page. Say under Scope that the inventory came from story source, not an index, and that `componentPath` joins weren't available.
- Branch on the top-level `v` field, which tracks the Storybook version: `v: 3` is the SB 6 `stories.json` (entries under the `stories` key); `v: 4` and `v: 5` are the SB 7+ `index.json` (entries under `entries`), and `v: 5` (SB 8.1+) adds `componentPath`. `componentPath` is opt-in and not guaranteed even on recent Storybook — use it for the Tier A join when present, and **fall back to the Tier B name join whenever it is absent, regardless of `v`**. A `v: 3` `stories.json` has no `type: 'docs'` entries at all, so it can't show rung 2: mark rung 2 **unknown** for v3, unless you read the MDX files or each story's `parameters.docs` directly.
- The official Storybook MCP (`@storybook/addon-mcp`) is **optional** — at the time of writing it needs a running server and is React-only/experimental. Use it only if the tools are already available; never make it a dependency.

**Documentation platform — optional layers (`integrations.documentation.enabled: true`):**
- `zeroheight`: use the REST API (Enterprise) — `GET /styleguides/{id}/pages` and `GET /pages/{id}` give the documented-page set and `updated_at` per page (high-confidence staleness). There is no components endpoint, so reconstruct the coverage diff by name-matching pages against the code/Storybook inventory (Tier C).
- `supernova`: use the MCP "Relay" or `@supernovaio/sdk` — `get_design_system_component_list` vs `get_documentation_page_list` gives a coverage diff (heuristic link, Tier B/C). Per-page staleness timestamps are not reliably exposed — mark staleness unknown unless a page timestamp is actually present.
- `custom`: crawl the sitemap or rendered HTML for page titles; name-match only (Tier C).

## Step 0: Build the component inventory (the source of truth)

Establish what components exist before looking at any documentation.

1. If a `codebase-index` output exists (`.ai/index/`), use its component list — it is already resolved and classified.
2. Otherwise, if the package has a public barrel (`src/index.ts`, or each package's entry point in a monorepo), use its component exports as the inventory — that's what consumers see and what needs docs. Internal building blocks that aren't exported don't need public docs; count them separately if at all.
3. Only if there's no barrel, glob the components directory. Common roots: `src/components/**`, `packages/*/src/**`, `lib/components/**`, `app/components/**`. Treat each component file/symbol as a candidate (e.g. `Button.tsx`, not `Button.test.tsx`, `Button.stories.tsx`, or `index.ts` barrels), and say the inventory may include internal components.
4. Record, per component: name, resolved file path (repo-relative, forward-slash), and category if a classification is available.

Produce a brief inventory line before continuing: `N components found across M directories.` If discovery finds nothing, ask the user where components live.

## Step 1: Build the documentation inventory

For each available surface, list what is documented.

- **Storybook:** parse `index.json`. Group entries by `title`. For each component, record: has a `type: 'story'` entry (rung 1, *exists*); has a docs page — autodocs or MDX via `tags` (unknown for a v3 `stories.json`, see above); and the resolved `componentPath` and `importPath`. A docs page alone doesn't make a component *described*: the `autodocs` tag generates a page even when no prop has a description. Rung 2 needs the page **and** descriptions on most props, from `argTypes` in the CSF file or JSDoc on the props interface. Record the prop-description ratio per component (described props of total) and report it; a page with 0 of 12 props described is rung 1 with a docs page, not rung 2. Also note `play` presence (interaction tests) where the CSF is read.
- **Figma component descriptions** (Console MCP `figma_get_component`, or the official MCP's `get_design_context` on the library node): a documentation surface for designers. Record which components have a non-empty description and report it as its own column, not merged into the Storybook rungs.
- **Hosted platform (if configured):** list documented pages and, where exposed, their `updated_at`/last-modified timestamp.
- **Usage guidance (rung 3):** if the system documents usage separately (a `usage-guidelines` output, MDX "When to use" sections, a Zeroheight guideline page), record which components reach rung 3.

## Step 2: Join the inventories

Join code components to documentation entries using the Tier A / B / C reliability hierarchy in `documentation-coverage.md` (file path, then symbol name, then fuzzy title match), and **record the tier on every match**. Never state a Tier C result as fact.

Before reporting anything as undocumented, run a positive control: confirm the join matches a component you can see is documented (open its story or page). If the join misses it, the key doesn't fit this codebase — fix it before reporting gaps.

## Step 3: Coverage gap analysis

From the join, produce:

- **Undocumented components** — in code, no entry on any surface. Report each with the join tier that found (or failed to find) it. Group by the documentation rung they fall short of.
- **Rung distribution** — how many components reach *exists* / *described* / *guided*. A high story count with few described/guided components is itself a finding.
- **Orphaned docs** — pages/stories whose component no longer exists in code. These point the opposite direction and are usually quick removals. Before calling a page orphaned, search the codebase for the name it documents (including renamed or re-exported symbols) — a Tier B/C "orphan" is often just a title that drifted from the component name.

## Step 4: Staleness analysis

For each documented component, compare change dates:

- Component last change: `git log -1 --format=%cI -- <component source path>`. If the latest commit looks test-only or cosmetic, check it with `git log -1 --name-only -- <component path>` and lower confidence rather than excluding file types.
- Doc last change: `git log -1 --format=%cI -- <story/MDX file>`, or the platform timestamp (`updated_at`).
- Flag **stale** when `component_last_change − doc_last_change > staleness_threshold_days` (default 90). A doc the same age as or newer than the component is never stale.
- `git log` returns **empty output (not an error)** for a file with no commits in the current branch/clone. Treat an empty result as untracked and mark staleness **unknown** — never as fresh. Do the same when a platform exposes no timestamp. Prefer a full clone: shallow clones and renames without `--follow` give misleading dates.

See `documentation-coverage.md` for why this proxy over-flags, how staleness and join confidence combine, and how to frame stale findings as a risk ("docs predate a code change on [date] — confirm they still match", with both dates shown) rather than a defect.

## Step 5: Produce the report

Open with a headline sentence stating overall state and where to focus. Example: "Of 84 components, 71 have a story but only 38 have a docs page, and 9 docs pages predate a code change. The coverage floor is solid; the described/guided layer and 9 staleness risks are where to focus."

Structure the report:

---

### Docs coverage report

**Date:** [date]
**Inventory:** [N components] · **Surfaces audited:** [Storybook / Zeroheight / Supernova / custom] · **Join confidence:** [the tier used for most components — A, B, or C]

**Summary**
One paragraph. Overall state, the most urgent gap, and an explicit note on which signals were measured vs estimated or unavailable. Write it like a peer review, not a compliance filing.

**Coverage by rung** — count each component at the **highest rung it reaches**. The rows are mutually exclusive (a "guided" component is not also counted under "described" or "exists"), so they sum to the full inventory. "Undocumented" is the rung-0 bucket: components on none of the three documentation rungs.
| Rung | Count | % of inventory |
|---|---|---|
| Guided (usage guidance) | | |
| Described (docs/autodocs page, no usage guidance) | | |
| Exists (≥1 story, no docs page) | | |
| Undocumented (no surface) | | |

**Findings**
List each finding with:
- Finding ID (e.g. DC-01)
- Severity: 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low
  - 🔴 Critical — a foundational component (Button, Input, Text, Icon, or anything with high fan-in) with no documentation on any surface (rung 0)
  - 🟠 High — any other public component at rung 0; a foundational component stale on a high-confidence timestamp; any component stale on a high-confidence timestamp where the code change touched its props interface or rendered element (the doc is now wrong, not just old)
  - 🟡 Medium — a public component stuck at rung 1 (a story but no docs page), or a stale doc on a lower-confidence timestamp
  - ⚪ Low — orphaned docs, internal components, and Tier C gaps awaiting confirmation
  - Only weight by traffic or usage if adoption data exists (see the adoption-measurement note); otherwise use foundational status, which the code can show
- Category: Coverage gap / Staleness / Orphan
- Confidence: Tier A / B / C (and timestamp source for staleness)
- Evidence: the component's file path and the docs entry it was joined to (story id, docs page URL) or the surfaces searched when none was found; for staleness, both change dates with their sources
- Description, affected component(s), and recommended action

**Orphaned documentation**
List pages/stories with no matching component, with the suggested removal.

**Action list**
- **Immediate:** undocumented foundational components (or high-usage ones, where adoption data exists); orphans
- **Planned:** raising the described/guided layer; resolving staleness risks
- **Review:** Tier C matches needing manual confirmation

**Scope**
- **Inspected:** [inventory source (barrel, index, or glob), Storybook index version, platforms queried, git history depth]
- **Not inspected:** [surfaces out of reach, e.g. a docs platform without API access]
- **How "none found" was checked:** [the join's positive control, and which rungs were unknown rather than absent — omit if the report makes no absence claims]
- **Assumptions:** [anything taken as given rather than verified]

End with the closing note below.

---

## Recurring workflow

Follows the recurring-run procedure in the configuration-and-recurring note. Specific to this skill:

- Compare coverage-by-rung deltas, newly undocumented components (regressions — these are the priority), newly resolved gaps, and staleness count trend.
- Add a "Trend since last audit" section to the header: previous date, rung deltas, and one sentence — "Documentation coverage is improving / stable / declining since [date]."

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit measures your documentation surface against your code — it does not see why a component was left undocumented or why a doc predates a change. Some gaps are deliberate (internal-only components) and some "stale" docs are still correct after a refactor. Tier C matches are best-guesses, not facts. If a finding describes an intentional choice, let me know — I'll calibrate future runs. The goal is to surface drift you haven't seen, not to second-guess decisions you've already made.

## Quality checks

- Every coverage finding carries a join confidence tier; no Tier C result is stated as fact
- Staleness findings show both change dates and name the timestamp source; unavailable timestamps are marked unknown, not assumed fresh
- The report distinguishes the rungs (exists / described / guided, plus the undocumented rung-0 bucket), counted at highest-attained — not a single coverage percentage; "described" rests on prop descriptions, not on the presence of a docs page
- Orphaned docs are reported separately from coverage gaps — they point the opposite direction
- The summary states which signals were measured vs estimated or unavailable
- The audit ran on whatever was available and did not block on a missing integration
- "Undocumented" claims rest on a join that passed its positive control
- The Scope block and the closing note about intentional choices are present
