---
name: documentation-coverage
type: knowledge
---

# Documentation coverage principles

**Knowledge note for Design System Ops**
**Auto-loaded by:** docs-coverage

---

## Code is the source of truth

The documentation surface is measured *against* the code, never the other way around. Code is the authoritative answer to "what components exist." The documentation platform — Storybook, Zeroheight, Supernova, a custom site — is a derived surface that should keep pace with it.

This direction matters because it determines what counts as a finding. A component in code with no documentation is a **coverage gap** (the surface fell behind). A documentation page for a component that no longer exists in code is an **orphan** (the surface didn't keep up with a removal). Both are drift; they point in opposite directions and have different fixes.

Never treat the doc platform's component list as the inventory. Platforms lag, and a missing platform entry is the very thing being audited.

---

## The three rungs of "documented"

"Documented" is not binary. A component sits on one of three rungs, and the audit should say which:

1. **Exists** — there is at least one Storybook story (or equivalent). This proves the component renders and is discoverable in the workbench. It is the floor, not real documentation.
2. **Described** — there is a docs/autodocs page or MDX: props, variants, anatomy. A developer can use the component without reading source.
3. **Guided** — there is usage guidance: when to use it, when not to, anti-patterns, accessibility notes. A team can use it *correctly* without asking.

A system where every component has a story but nothing reaches rung 3 has a coverage number that looks healthy and a documentation surface that isn't. Report the distribution across rungs, not a single percentage.

---

## The join-key reliability hierarchy (trust-critical)

Coverage analysis is a join between two lists: components in code, and entries in the doc surface. The audit is only as trustworthy as that join. Always attach the join confidence to every coverage finding — a false "undocumented!" flag costs more trust than a missed one.

**Tier A — high confidence: resolved file path.**
Storybook `index.json` schema v5 (SB 8.1+) carries `componentPath` — the resolved source path of `meta.component`. Normalise to repo-relative, forward-slash, and match directly against the components glob. This is an exact structural join. Prefer it whenever it exists.

**Tier B — medium confidence: symbol name.**
When `componentPath` is absent (older v3/v4 indexes, or metas without `component`), join on the component export name or the last segment of the story `title`. `title` is a display string and can be renamed or regrouped independently of the component, so this can drift. Usable, but flag it.

**Tier C — low confidence: fuzzy name match.**
For platforms with no structural link to code (Zeroheight, a custom docs site, free-form Supernova pages), match the component name against page titles or headings. This is heuristic and prone to false positives (a "Button" page may document three button variants; a "Buttons" guideline page may not map to any single component). Never present a Tier C result as fact — phrase it as "no page found mentioning X" and recommend manual confirmation.

Rule: **file-path match beats name match beats nothing.** Degrade loudly, not silently.

---

## Staleness is a risk flag, computed from change dates

Staleness asks: did the documentation fall behind the component? Compute it from change timestamps, not content.

- **Component last change:** `git log -1 --format=%cI -- <component source path>`. "Change" is the last commit touching the component's source — a deliberately blunt proxy. A test-only, story-only, or comment-only commit moves this date too, so it can over-flag; that is the safe direction for a risk signal (better than missing real drift), but when a flag looks cosmetic, inspect the commit (`--name-only`) and lower confidence rather than hard-excluding file types.
- **Doc last change:** the git timestamp of the story/MDX file, or a platform-supplied timestamp (Zeroheight `updated_at`; Supernova page metadata where it exists).
- **Stale** when `component_last_change − doc_last_change > grace window` — the component changed and the doc has not caught up. If the doc is the same age as or newer than the component, it is never stale. Default grace: `staleness_threshold_days` (90 if unset) — small enough to catch real drift, large enough to ignore same-sprint lag.

Two disciplines keep this honest:

- **Staleness is a risk, not a defect.** A code change can be an internal refactor that needs no doc update. Frame stale findings as "doc predates a code change — confirm it still matches," not "doc is wrong."
- **Confidence varies by timestamp source.** Git-backed story staleness and Zeroheight `updated_at` are high confidence. Where a platform exposes no per-page timestamp (Supernova does not reliably), staleness is **unknown** — say so, don't guess. Fall back to version-level publish state only as a coarse signal.
- **Staleness confidence and join confidence are independent axes.** A Zeroheight `updated_at` can tell you a page is genuinely old (high staleness confidence) while the page-to-component link is still a Tier C name guess (low join confidence). Report both — "confident the page is stale, less sure it maps to this component" is a more honest finding than collapsing the two.

A component not tracked in git (untracked, or outside the repo) cannot be dated — mark its staleness unknown rather than assuming fresh.

---

## What each surface actually exposes

The skill must degrade to what is reachable. The honest matrix:

| Surface | Coverage gap | Staleness | Join confidence |
|---|---|---|---|
| **Storybook (static `index.json`)** | Yes — `componentPath` ↔ code glob | Via git on the story/MDX file | Tier A (v5) / Tier B (older) |
| **Storybook (official MCP)** | Yes, but needs a running server; React-only, experimental | Same as static | Tier A |
| **Supernova (MCP "Relay" / SDK)** | Yes — component list vs doc-page list, but link is heuristic | Often **unknown** — page timestamps unconfirmed | Tier B/C |
| **Zeroheight (REST API, Enterprise)** | No components endpoint — reconstruct the diff from code/Storybook/Figma | Yes — `updated_at` per page | Tier C |
| **Custom docs site** | Crawl sitemap/HTML, name-match only | Page-level dates if present in markup | Tier C |

The zero-integration baseline — components glob ∪ Storybook static `index.json` ∪ git — answers coverage and staleness for the majority of teams with no API, no plan tier, and no running server. Hosted platforms are layers on top, not prerequisites. Do not block the audit on an integration; log the gap and proceed with what is available.

---

## Coverage is not usage

A page existing is not a page read. This audit measures whether the surface *keeps pace* with the components — not whether anyone consumes it. Documentation analytics (page views, search-gap analysis, helpfulness ratings) are an adoption signal and belong to the adoption report, which has the platform analytics hooks. See [[adoption-measurement]]. When both run, coverage answers "is it documented?" and adoption answers "is the documentation working?" — keep the two questions separate.

---

## What a docs-coverage audit should not do

- **Do not cry wolf on Tier C joins.** An unconfirmed name match presented as a hard gap is the fastest way to lose a team's trust in the whole skill.
- **Do not treat refactor-driven staleness as a defect.** Surface it as a prompt to confirm, with the change dates shown.
- **Do not rank teams or components competitively.** Report gaps to the system team for action, not as a leaderboard.
- **Do not silently assume.** State, per component, which signals were measured and which were estimated or unavailable. An audit that admits its blind spots is more useful than one that hides them.
