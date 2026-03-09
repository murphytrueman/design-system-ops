---
name: adoption-report
description: "Produce a design system adoption report separating coverage from actual adoption, with trend direction and risk flags. Trigger when someone says: adoption report, how much is the system being used, usage metrics, adoption status, coverage report, which teams are using the system, who's not using the system, or anything about measuring or reporting on how widely the design system is being used."
references:
  - references/output-discipline.md
  - references/adoption-measurement.md
---

# Adoption report

A skill for producing a design system adoption report that distinguishes coverage (who has access and can use the system) from adoption (who is actively using it), with trend direction and risk flags for teams where adoption is low or declining.

## Context

Coverage and adoption are not the same thing, and treating them as equivalent is one of the most common ways design system reports mislead. A system available to twenty product teams has 100% coverage. If only eight of those teams are actively using it, adoption is 40%. Both numbers are true. Only one of them tells you how the system is actually performing.

This skill produces a report that holds both numbers separately and distinguishes between them throughout. It also separates adoption across two dimensions that are frequently conflated: design adoption (are designers using the Figma library?) and engineering adoption (is the code being consumed from the system?). High design adoption with low engineering adoption is a specific kind of problem — the design side is working but the handoff is broken. The reverse is also a specific kind of problem.

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `system.component_count` — informs small-system behaviour
- `integrations.*` — enables auto-pull for adoption data (see below)
- `recurring.*` — enables trend comparison against previous reports

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically:

**npm registry** (`integrations.npm.enabled: true`):
- Pull weekly/monthly download statistics for `integrations.npm.package_name` over the reporting period
- Calculate trend direction from download data: increasing, flat, or declining
- For monorepos: pull per-package downloads from `integrations.npm.scoped_packages` — note these are directional signals (see monorepo caveat in component-audit)
- Compare current period downloads against previous period for the engineering adoption trend

**Figma MCP** (`integrations.figma.enabled: true`):
- Pull library analytics from `integrations.figma.file_key` if available via the Figma REST API
- Extract: number of files using the library, component insertion counts, detach rates
- Detach rates are a design adoption quality signal — high detach rates mean designers are pulling components but modifying them, which is partial adoption at best
- Use library file count as the numerator for design adoption percentage

**GitHub** (`integrations.github.enabled: true`):
- Count import references for design system packages across consuming repositories using `gh api search/code`
- Track which repositories import the system — these are the actively adopting engineering teams
- Pull contribution activity: PRs from consuming teams into the design system repo indicate healthy engagement

**Documentation platform** (`integrations.documentation.enabled: true`):
- If the documentation platform has analytics (Zeroheight, Supernova): pull page views per component doc
- High-view-count pages indicate actively used components; zero-view pages indicate unused or undiscoverable documentation

If an integration fails, log it and proceed with manual data gathering.

## Recurring workflow

If `recurring` is configured in `.ds-ops-config.yml`:

1. **Load the previous adoption report** from `recurring.output_directory`.
2. **Auto-populate the trend direction** by comparing current period data against the previous report:
   - Coverage change: +/- teams
   - Adoption change: +/- teams (design and engineering separately)
   - At-risk teams: newly at-risk vs. previously at-risk now recovered
   - Blocker categories: which blockers are persistent vs. newly resolved?
3. **Add a "Period-over-period comparison" section** to the report header showing the deltas
4. **Flag persistent blockers** — any blocker category present in 3+ consecutive reports is a systemic issue, not a one-time finding
5. **Save output** and prune per `recurring.retain_count`.

## Step 1: Define scope and gather data

Ask for or confirm (skip questions already answered by auto-pull):
- Which teams or products are in scope?
- What data is available? (Figma library analytics, npm download stats, component usage in codebases, survey data, self-reported figures)
- What is the reporting period? (Quarter, year, or since last report)
- Is there a previous adoption report to compare against for trend direction?

If data is limited: the adoption report can be conducted as a structured assessment based on available signals rather than hard metrics. Note clearly in the output where figures are estimated rather than measured.

## Step 1b: Adoption definition worksheet

Before calculating any metrics, align on what "adoption" means for this context. Different definitions produce different numbers — and comparing reports that use different definitions creates misleading trends.

**Adoption definition worksheet:**

1. **What counts as "using the system"?**
   - [ ] Installed the package (weakest signal — installed is not adopted)
   - [ ] Imported at least one component in production code
   - [ ] Using 3+ components in production
   - [ ] Using the system for 50%+ of interface patterns
   - [ ] Other: ___

2. **What counts as "design adoption"?**
   - [ ] Figma library is enabled
   - [ ] Components from the library appear in current design files
   - [ ] Designers are using library components without detaching
   - [ ] Other: ___

3. **What counts as "engineering adoption"?**
   - [ ] Package is installed
   - [ ] Components are imported in production code
   - [ ] Token references are used (not hardcoded values)
   - [ ] Other: ___

4. **What is the threshold for "partial" vs "full" adoption?**
   - Partial: ___
   - Full: ___

Document the chosen definitions at the top of the report. Use the same definitions for every subsequent report to enable meaningful trend comparison.

## Step 2: Establish the adoption baseline

Before calculating any metrics, define what "adopting the design system" means for this context. This definition should be agreed upon before reporting, because it determines which teams appear in which column.

Proposed baseline definition:
A team is considered to be adopting the design system if it is actively consuming design system components in shipped product work — not just installed, not just in explorations, but in production or production-equivalent environments.

Teams that have the system installed but are not shipping with it, or that use only a small subset of peripheral components, may warrant a separate "partial adoption" category.

Document the definition used so that comparisons across reporting periods use a consistent measure.

**Small-system note (fewer than 5 components):** For systems this size, the coverage-vs-adoption framing still works but the metrics change. Coverage is likely 100% — if you have three components, every team that uses the system has access to all of them. Adoption is better measured as scope coverage: what percentage of the team's actual interface needs does the system serve? A system with 3 components that covers 80% of a team's UI patterns has stronger adoption than a 30-component system covering 20%. The team-by-team breakdown may reduce to a single team or two — that is fine, but go deeper per team: which patterns are they using the system for, and which are they building locally? The "at-risk teams" section may not apply if there is only one consuming team. Replace it with an "unserved needs" section listing the interface patterns the team is building outside the system. These are your roadmap.

## Step 3: Produce the report

---

### Design system adoption report

Open with a headline sentence that tells the reader the overall state and where to focus.

**Period:** [reporting period]
**Date:** [date]
**Previous report:** [link or date, if applicable]
**Adoption definition:** [the agreed definition from Step 2]

---

#### Coverage vs adoption summary

| | Design | Engineering | Combined |
|---|---|---|---|
| Teams in scope | [n] | [n] | [n] |
| Teams with access (coverage) | [n] ([%]) | [n] ([%]) | [n] ([%]) |
| Teams actively adopting | [n] ([%]) | [n] ([%]) | [n] ([%]) |
| Change from last period | [+/- n] | [+/- n] | [+/- n] |

---

#### Trend direction

State the overall direction in one sentence: growing, stable, declining, or mixed. A mixed signal (design adoption growing while engineering adoption is flat) is worth naming explicitly.

If this is the first report: no trend direction is available. Flag that this report establishes the baseline and that trend analysis will be available from the next reporting period.

#### Baseline establishment protocol

When this is the first adoption report (no previous report exists), the standard trend analysis is not possible. Instead of producing a thin baseline report, use this protocol to establish a comprehensive foundation for future measurement:

**1. Metrics infrastructure audit**

Before reporting numbers, document what data sources exist and what gaps remain:

| Data source | Available? | Quality | Gap |
|---|---|---|---|
| npm download stats | Y/N | [reliable/partial/unreliable] | [what's missing] |
| Figma library analytics | Y/N | [reliable/partial/unreliable] | [what's missing] |
| Codebase import analysis | Y/N | [reliable/partial/unreliable] | [what's missing] |
| Team survey data | Y/N | [reliable/partial/unreliable] | [what's missing] |
| Support channel data | Y/N | [reliable/partial/unreliable] | [what's missing] |

**2. Tracking recommendations**

For each data gap identified, recommend a specific action to close it before the next reporting period:

- If npm stats are unavailable: set up download tracking or add analytics to the package
- If Figma analytics are unavailable: enable library analytics in Figma or add a manual quarterly count
- If codebase analysis is unavailable: recommend a code search tool or a quarterly grep-based audit
- If survey data is unavailable: provide a template adoption survey (5 questions, 2 minutes) to send to consuming teams

**3. Baseline snapshot**

Document the current state with maximum precision given available data. For each metric, note:
- The current value
- The data source and its reliability
- The measurement method (so it can be repeated identically next period)
- Any caveats or known inaccuracies

**4. Target setting**

Based on the baseline snapshot, propose targets for the next reporting period:
- Adoption growth target (e.g. "2 additional teams actively adopting")
- Coverage growth target (e.g. "extend access to the mobile team")
- Blocker resolution target (e.g. "resolve the top 2 adoption blockers")
- Metrics infrastructure target (e.g. "close 2 of 3 data source gaps")

The baseline establishment protocol turns a first-run adoption report from "here are some numbers" into "here is a measurement system that will produce meaningful trends from the next period onward."

---

#### Team-by-team breakdown

For each team in scope:

| Team | Design adoption | Engineering adoption | Status | Notes |
|---|---|---|---|---|
| [Team name] | ✅ Active / ⚠️ Partial / ❌ Not adopting | ✅ Active / ⚠️ Partial / ❌ Not adopting | ✅ On track / ⚠️ At risk / ❌ No engagement | [relevant context] |

For teams with "Partial" adoption: note which areas of the system are being used and which are not. Partial adoption often indicates that the system does not yet serve a specific use case this team has, which is actionable information.

---

#### At-risk teams

Flag teams where adoption is declining, where there has been no engagement for an extended period, or where known blockers exist.

For each at-risk team: the specific signal (declining usage, no recent engagement, active parallel solution being built), the likely cause if known, and a recommended next step.

At-risk teams are the most actionable section of the report. Adoption work is most effective early — a team that has disengaged for six months is significantly harder to re-engage than a team that has been quiet for six weeks.

---

#### Coverage gaps

Which teams do not yet have access to the system? This is a different category from teams that have access but are not adopting — these teams have not been onboarded at all.

For each uncovered team: whether they have expressed interest, what their likely use case would be, and what would be required to extend coverage.

---

#### Adoption blockers

Based on what is known from team interactions, support requests, and survey data: what are the most commonly cited reasons for non-adoption or partial adoption?

Group blockers into categories:
- Missing components or patterns: the system does not have what teams need
- Documentation gaps: teams cannot find how to use what exists
- Integration friction: technical barriers to consuming the system
- Awareness gaps: teams do not know the system exists or has what they need
- Tooling misalignment: the system is built for a different tech stack or tooling context than some teams use

For each category: how many teams or incidents cite this as a blocker, and what would address it.

---

#### Recommendations

Prioritised actions based on the report findings:

1. Immediate actions for at-risk teams
2. Coverage extension opportunities
3. Adoption blocker remediation in priority order
4. Metrics improvements: where is the data incomplete, and what would improve future reporting accuracy?

---

#### Platform reliability metrics (staff-level)

At the staff level, adoption reports should include infrastructure reliability signals alongside usage metrics. These help explain WHY adoption is where it is.

**Release reliability:**
- Number of releases in the reporting period
- Number of breaking changes in the reporting period
- Were breaking changes accompanied by migration paths? (Y/N per breaking change)
- Median time from bug report to fix for system-level bugs

**Documentation currency:**
- % of components where documentation matches the current released version
- Number of documentation-related support requests in the period (high number = documentation is stale or unclear)

**Integration friction score:**
- Average time from "team decides to adopt" to "first component in production" for teams that onboarded in this period
- What were the most common setup blockers? (Installation, configuration, framework incompatibility, token integration)

Frame these as leading indicators: reliability metrics predict future adoption trends. A system with two breaking changes, no migration paths, and stale documentation will lose adoption even if current numbers look healthy.

#### AI tooling adoption (staff-level)

If the system has AI-ready metadata (structured descriptions, machine-readable manifests, MCP integration):

- Are AI tools (Claude, GitHub Copilot, Cursor, etc.) using the system's metadata to generate component usage?
- What is the quality of AI-generated output? (Are AI agents selecting the right components, configuring them correctly, avoiding anti-patterns?)
- Are teams using AI-assisted workflows with the system, or is the AI metadata unused?

This is a forward-looking metric. Even if AI tooling adoption is currently zero, documenting AI readiness positions the system for the next wave of tooling.

---

## Quality checks

- Coverage and adoption are reported separately throughout — they are never combined into a single figure
- Design adoption and engineering adoption are reported separately
- Trend direction is stated, not implied
- At-risk teams are flagged with a specific signal, not just a low number
- Adoption blockers are specific and grouped by category, not listed as individual team complaints
- The adoption definition is documented and will enable consistent comparison in the next reporting period
- Where figures are estimated rather than measured, this is stated
- If platform reliability metrics are included, they are framed as adoption predictors, not separate metrics
- If AI tooling adoption is included, it is framed as forward-looking and not penalised if currently zero
- If this is the first report (no previous report exists), the baseline establishment protocol is used — including metrics infrastructure audit, tracking recommendations, baseline snapshot, and target setting
