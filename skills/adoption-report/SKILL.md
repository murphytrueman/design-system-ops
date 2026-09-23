---
name: adoption-report
description: "Adoption report: coverage (what the system provides), reach (teams with access) and adoption (teams shipping with it), design vs engineering, trend and at-risk teams. Triggers: adoption report, usage metrics, which teams use the system. Not docs coverage — use docs-coverage."
references:
  - ../../knowledge-notes/output-discipline.md
  - ../../knowledge-notes/adoption-measurement.md
---


# Adoption report

A skill for producing a design system adoption report that separates coverage (how much of teams' needs the system provides), reach (which teams have access) and adoption (which teams actually ship with it), with trend direction and risk flags for teams where adoption is low or declining.

## Before you begin: verify references

Before doing anything else, confirm that every file listed in this skill's frontmatter `references:` field exists at its relative path from this SKILL.md. If any are missing, stop — the install is incomplete. This usually means a third-party installer (for example `npx skills install`) flattened the skill into a standalone folder and dropped the repo-root `knowledge-notes/` directory this skill depends on. Tell the user to reinstall using a supported method from `1-INSTALL.md` (git clone, or the `.plugin` bundle in Cowork) and to run `verify-install.sh` from the install root to confirm the fix. Only proceed without the references if the user explicitly says to — and if they do, state clearly in your output that it was produced in degraded mode without the pack's reference material.

## Context

Coverage, reach and adoption are three different things, and treating them as one is among the most common ways design system reports mislead:

- **Coverage** is supply: how much of the teams' interface needs the system provides.
- **Reach** is access: which teams have the system available to them (package installed, Figma library enabled, onboarded).
- **Adoption** is use: which teams actually ship product work with it.

A system can reach all twenty product teams while only eight of them ship with it. Both facts are true; only one tells you how the system is performing. And if the system provides only a fraction of what those eight teams need, the constraint is coverage, not adoption. Low coverage is a supply problem the system team fixes by building; low adoption with good coverage is a demand problem the system team fixes by understanding why teams aren't consuming what exists (see the adoption-measurement note).

This skill holds the three measures separately throughout. It also separates adoption across two dimensions that are frequently conflated: design adoption (are designers using the Figma library?) and engineering adoption (is the code being consumed from the system?). High design adoption with low engineering adoption is a specific kind of problem — the design side is working but the handoff is broken. The reverse is also a specific kind of problem.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `system.component_count` — informs small-system behaviour
- `integrations.*` — adoption data sources (see below)
- `recurring.*` — period-over-period comparison (see below)

**Maturity stage:** if a system-health report exists, take the maturity stage from it and cite it. Otherwise ask the user. Don't infer a stage from adoption data alone.

## Auto-pull integrations

**npm registry** (`integrations.npm.enabled: true`):
- Pull weekly/monthly download statistics for `integrations.npm.package_name` over the reporting period
- Calculate trend direction from download data: increasing, flat, or declining
- For monorepos: pull per-package downloads from `integrations.npm.scoped_packages` — directional signals only (see monorepo caveat in component-audit)
- Compare current period downloads against previous period for the engineering adoption trend. Downloads show direction, never a count of adopting teams (see the note's npm caution)

**Figma MCP** (`integrations.figma.enabled: true`):
- Pull library analytics from `integrations.figma.file_key` if available via the Figma REST API
- Extract: number of files using the library, component insertion counts, detach rates
- Detach rates are a design adoption quality signal — high detach rates mean designers are pulling components but modifying them, which is partial adoption at best
- Use library file count as the numerator for design adoption percentage
- Track which teams are using the library by analysing team membership in Figma workspace analytics if available

**GitHub** (`integrations.github.enabled: true`):
- Find which repositories import the design system packages — these are the actively adopting engineering teams (see the note's GitHub caution before counting)
- Pull contribution activity: PRs from consuming teams into the design system repo indicate healthy engagement
- Note recency: repositories with no imports in the last 6 months may indicate disengagement or migration to a competitor solution

**Documentation platform** (`integrations.documentation.enabled: true`):
- If the documentation platform has analytics (Zeroheight, Supernova): pull page views per component doc
- High-view-count pages indicate actively used components; zero-view pages indicate unused or undiscoverable documentation
- Track search logs if available — what terms are teams searching for that return no results? These are adoption blockers.

## Recurring workflow

Follows the recurring-run procedure in the configuration-and-recurring note. Specific to this skill:

- **"Period-over-period comparison" section** showing the deltas against the previous report, which also sets the trend direction:
   - Coverage change: needs served vs. unserved
   - Reach change: +/- teams
   - Adoption change: +/- teams (design and engineering separately)
   - At-risk teams: newly at-risk vs. previously at-risk now recovered
   - Blocker categories: which blockers are persistent vs. newly resolved?
- **Flag persistent blockers** — any blocker category present in 3+ consecutive reports is a systemic issue, not a one-time finding

---

## Step 1: Gather adoption signals

Ask for or confirm (skip questions already answered by auto-pull):
- Which teams or products are in scope?
- What data is available? (Figma library analytics, npm download stats, component usage in codebases, survey data, self-reported figures)
- What is the reporting period? (Quarter, year, or since last report)
- Is there a previous adoption report to compare against for trend direction?
- Who is the audience? The system team gets the team-level report; leadership gets system-level aggregates (see Step 5).

### Step 1a: Adoption signal inventory

Before proceeding, audit which adoption signals are available and their reliability:

**Direct signals (measured data):**
- npm download statistics (direction only — see the caveat above)
- Figma library analytics (files using library, insertion counts, detach rates)
- Code import counts per repository
- Documentation platform analytics (page views per component)
- Support ticket volume by team or component

**Indirect signals (structural inference):**
- Components added to repositories in recent commits (evidence of recent adoption)
- Component usage in shipped products vs. experimental branches
- Design file inventory (how many files reference the design system library)
- Pull request activity between consuming teams and the system repository
- Team interviews or surveys

Document which signals are available and which are unavailable. Adoption assessment is only as strong as the signals used — if only one signal is available, note that the adoption assessment is based on limited data and may be incomplete.

If data is limited: the adoption report can be conducted as a structured assessment based on available signals rather than hard metrics. Label every figure measured (with its source), estimated (with the reasoning) or reported by the team.

### Step 1b: Frame adoption against the maturity stage

Raw adoption figures are misleading without context, and there is no sourced benchmark for what adoption "should" be at each stage. Frame the figures qualitatively against the named stage (from system-health or the user):

- **Ad-hoc or Managed:** direction matters most. Is adoption growing period on period, and are early adopters getting what they need?
- **Systematic:** breadth matters. Are most teams using the system for most of the patterns it covers?
- **Measured:** depth matters. Are teams using the system deeply, not superficially, and are declines being caught early?
- **Optimised:** stability matters. Is adoption holding without active promotion? Declines are the primary concern.

The same figure means different things at different stages: a Managed system with a third of teams adopting and growing is on track; a Measured system at the same figure has a structural problem worth diagnosing.

---

## Step 2: Separate coverage, reach and adoption

Before calculating any metrics, define each measure for this reporting period.

### Coverage (supply)

**Coverage** = how much of the teams' interface needs the system provides.

Signals: an inventory of the patterns teams build against what the system offers; local components that fill needs the system doesn't cover; missing-component requests. A team building a local date picker because the system has none is a coverage gap, not an adoption failure.

### Reach (access)

**Reach** = teams that have the system available to them, whether they use it or not.

Signals:
- Team has the npm package installed in their production codebase
- Team has the Figma library enabled in their workspace
- Team has been formally onboarded or given access
- Team has documentation and knows the system exists

Reach is the easy measure. The challenge is actual use.

### Adoption (use)

**Adoption** = teams actively consuming design system components in shipped product work, not just installed or in explorations.

Different definitions produce different numbers, and comparing reports that use different definitions creates misleading trends. Align on the definition first.

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

### Why separate design from engineering adoption

Design adoption and engineering adoption are independent. Common patterns:

- **High design adoption, low engineering adoption:** Design system is working, but engineering handoff is broken. The components are being designed with the system, but engineers are not implementing them from the code library. Investigate: are the code components available? Are they what designers think they are? Is there a documentation or discovery gap?

- **Low design adoption, high engineering adoption:** Engineers are adopting the system's code, but designers are not using the Figma library. Investigate: is the design library up to date? Is it discoverable? Are there design tokens being used that are not reflected in the code?

- **Both low:** System has not crossed the adoption threshold. The focus is on why — is there a blocker that explains both, or are design and engineering facing different problems?

---

## Step 3: Assess each team

For each team in scope, determine:
1. **Adoption stage** — from the adoption-measurement note: Aware / Installed / Consuming / Contributing / Advocating, or **Not reached** if the team has no access or doesn't know the system exists
2. **Design adoption** — Active / Partial / None
3. **Engineering adoption** — Active / Partial / None
4. **Usage indicators** — specific components used, frequency, recency
5. **Engagement signals** — questions asked, contributions made, documentation viewed

Sources for per-team data:
- Code import analysis (which repos import the system)
- Figma team access logs and component usage
- Support tickets and questions attributed to teams
- Direct interviews or surveys with team leads
- Git commit history (who is merging PRs that add system components)

Each stage carries its intervention from the note: Aware needs onboarding support, not pressure; Installed needs its barriers identified; Consuming needs support and its gaps addressed; Contributing needs a streamlined contribution path; Advocating teams can be enabled to support peers.

For teams with partial adoption, note which areas of the system they use and which they build locally, and whether the local work is a coverage gap (the system doesn't provide it) or a choice (it does). Document the criteria you used so the assessment can be repeated next period.

---

## Step 4: Identify at-risk teams and analyse blockers

### At-risk teams

Flag teams where adoption is declining, where there has been no engagement for an extended period, or where known blockers exist. For each, record:
1. **The signal** — declining usage over time, no recent engagement (6+ weeks without contact), a known issue report, or team communication indicating plans to move away from the system
2. **The likely cause** if known — from blocker analysis, support conversations, or team feedback
3. **Recommended next step** — reach out to discuss the blockers, offer support, gather more information, or schedule a working session

At-risk teams are the most actionable section of the report. Adoption work is most effective early — a team that has disengaged for six months is significantly harder to re-engage than a team that has been quiet for six weeks.

### Adoption blockers

From team interactions, support requests and survey data, group the reasons for non-adoption or partial adoption:

- **Missing components or patterns:** the system does not have what teams need (a coverage gap)
- **Documentation gaps:** teams cannot find how to use what exists
- **Integration friction:** technical barriers to consuming the system (installation, build integration, framework compatibility)
- **Awareness gaps:** teams do not know the system exists or have not discovered what they need (a reach gap)
- **Tooling misalignment:** the system is built for a different tech stack or tooling context than some teams use
- **Governance or process friction:** the contribution process is unclear, or the system feels gatekept rather than collaborative
- **Reliability concerns:** the system has had breaking changes without migration paths, causing teams to maintain local copies for stability

For each category: how many teams or incidents cite it, and what would address it. Flag if one category dominates — "missing components" dominating is a different problem from "awareness gaps" dominating, and the remediation is category-specific.

---

## Step 5: Produce the report

**Audience rule:** the team-by-team breakdown and at-risk teams go to the system team, for targeted support. A version for leadership shows system-level aggregates only (reach, adoption and coverage totals, trend, blocker categories) and names no teams. Never rank teams against each other or publish a league table.

---

### Design system adoption report

[Headline: one or two sentences — the adoption picture. Overall direction (growing, stable, declining or mixed), the most significant finding across coverage, reach and adoption, and what is driving it. Example: "Design adoption is growing but engineering adoption is flat: designers are using the library, but code components aren't reaching shipped products. The handoff is the gap to close this quarter."]

**Period:** [reporting period] · **Previous report:** [link or date, if applicable] · **Maturity stage:** [named stage, with source]
**Adoption definition:** [the agreed definition from Step 2]

---

#### Adoption picture

One paragraph expanding the headline: direction, how it reads against the maturity stage (Step 1b), the design-vs-engineering pattern (Step 2), and what is driving it. If this is the first report, say it establishes the baseline and trend analysis starts next period.

#### Coverage, reach and adoption

| | Design | Engineering |
|---|---|---|
| Teams in scope | [n] | [n] |
| Teams reached (have access) | [n] of [n] | [n] of [n] |
| Teams adopting (shipping with it) | [n] of [n] | [n] of [n] |
| Change from last period | [+/- n] | [+/- n] |

**Coverage:** [what share of teams' interface needs the system provides, and the main unserved needs, with source]

#### Period-over-period comparison (if recurring)

| Measure | This period | Previous period | Change |
|---|---|---|---|
| Teams in scope | [n] | [n] | [+/-] |
| Teams reached | [n] | [n] | [+/-] |
| Teams adopting — design | [n] | [n] | [+/-] |
| Teams adopting — engineering | [n] | [n] | [+/-] |
| At-risk teams | [n] | [n] | [+/-] |

#### Team-by-team breakdown (system team only)

| Team | Stage | Design | Engineering | At risk? | Notes |
|---|---|---|---|---|---|
| [Team] | Aware / Installed / Consuming / Contributing / Advocating / Not reached | Active / Partial / None | Active / Partial / None | Yes / No | [components used; local builds, and whether each is a coverage gap or a choice] |

#### At-risk teams (system team only)

| Team | Signal | Likely cause | Recommended action |
|---|---|---|---|
| [Team] | [signal, with source] | [cause, or "unknown"] | [specific next step] |

#### Reach gaps

| Team | Interest | Likely use case | What access would require |
|---|---|---|---|
| [Team not yet reached] | [expressed / unknown] | [use case] | [framework support, onboarding, etc.] |

#### Adoption blockers

| Blocker category | Cited by | Example | Remediation |
|---|---|---|---|
| [category from Step 4] | [n teams] | [specific example] | [action, and the skill that would do it] |

#### Recommendations

1. **Immediate actions for at-risk teams** — specific teams and specific next steps
2. **Blocker remediation, in priority order** — ranked by teams affected, with effort if known and the skill that would execute it (e.g. component-audit for a missing-components gap)
3. **Coverage and reach extension** — unserved needs to build, and teams to onboard, prioritised by strategic value
4. **Metrics improvements** — where the data is incomplete and what would improve the next report (e.g. "Enable the GitHub integration to track code imports automatically")

#### Platform reliability (staff-level)

Reliability signals explain why adoption is where it is, and predict where it's going. A system with breaking changes, no migration paths and stale documentation will lose adoption even if current figures look healthy.

- **Release reliability:** releases and breaking changes in the period; whether each breaking change shipped with a migration path; median time from system bug report to fix
- **Documentation currency:** components whose documentation matches the current released version ([n] of [n]); documentation-related support requests in the period
- **Time to first production component:** for teams that onboarded this period, the time from deciding to adopt to shipping their first system component, and the most common setup blockers (installation, configuration, framework incompatibility, token integration)

#### AI tooling adoption (staff-level, evidence only)

Include only with evidence: repositories whose AI tooling is configured to use the system's metadata (MCP configuration, rules files referencing the manifest), or reviewed samples of AI-generated code checked for correct component selection and props. Without evidence, omit the section or record it as `[needs data: …]` under metrics improvements. Don't assess the quality of AI-generated output from impressions.

#### Signals used and scope

- **Signals used:** [direct and indirect signals, each with its source]
- **Signals unavailable:** [e.g. "documentation platform analytics not available"]
- **Data completeness:** [all teams, or a sample — e.g. "interviews with 8 of 12 teams; the other 4 estimated from code import analysis"]

**Scope**
- **Inspected:** [repositories, analytics exports, surveys actually read]
- **Not inspected:** [teams, repos or data sources out of reach]
- **Assumptions:** [e.g. team-reported figures taken as given]

---

#### Small-system note (fewer than 5 components)

For systems this size, the three measures still apply but their weight changes. Reach is likely complete — the one or two consuming teams have access to everything. The more useful measure is coverage: what share of the team's actual interface needs does the system serve? A 3-component system that covers most of a team's UI patterns is doing more than a 30-component system that covers a fifth of them.

The team-by-team breakdown may reduce to a single team or two — that is fine, but go deeper per team: which patterns are they using the system for, and which are they building locally?

The "at-risk teams" section may not apply if there is only one consuming team. Replace it with an "unserved needs" section listing the interface patterns the team is building outside the system. These are your roadmap.

For reporting, treat partial adoption as "using the system for [share] of patterns" rather than "using 3 of 5 components."

---

## Quality checks

- The report opens with the adoption-picture headline, not metadata or a table
- Coverage (supply), reach (access) and adoption (use) are reported separately throughout, never combined into a single figure
- Design adoption and engineering adoption are reported separately
- Trend direction is stated, not implied
- Every figure names its source and is labelled measured, estimated or team-reported; npm downloads are used for direction only
- Maturity is a named stage from system-health or the user, framed qualitatively — no expected adoption ranges
- Team-level detail is in the system team's version only; a leadership version shows aggregates and ranks no teams
- Per-team status uses the adoption-measurement stages (Aware → Advocating, or Not reached)
- At-risk teams are flagged with a specific signal, not just a low number
- Adoption blockers are specific and grouped by category, not listed as individual team complaints
- The adoption definition is documented and will enable consistent comparison in the next reporting period
- If period-over-period comparison is included, the previous report was actually loaded and compared
- If platform reliability metrics are included, they are framed as adoption predictors, not separate metrics
- AI tooling adoption appears only with evidence
- At-risk team recommendations are specific and actionable, not generic
- Recommendations include which skill would execute the work, where applicable
- The report ends with the signals used and a Scope block
