---
name: triage
description: "Pick which 3-5 Design System Ops skills to run first, in order, from a quick look at the system. Triggers: where should I start, what should I run first, which audit first, new to this plugin. Not for prioritising audit findings into work (backlog-generator)."
references:
  - ../../knowledge-notes/output-discipline.md
---

# Triage

A skill for quickly assessing a design system's state and recommending which skills to run first, in what order, and why. Prevents the overwhelm of running every skill in the pack when 3–5 would surface the critical findings.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Design System Ops has skills across five categories: audit, validate, document, govern, and communicate. Running all of them is comprehensive but overwhelming — especially for a team encountering the plugin for the first time. The triage skill reads the system's current state and produces a prioritised run plan: which skills to run first, which to skip for now, and which to return to later.

The triage skill is intentionally lightweight. It should take no more than 5 minutes of input-gathering and produce a run plan in under a minute. The value is in sequencing, not in depth — the subsequent skills provide the depth.

## Boundaries

This skill produces a run plan — it does not run other skills itself. If the user wants a full automated sweep, point them to the `/full-diagnostic` agent instead. If the system has a single well-defined problem ("our tokens are a mess"), skip triage and go directly to the relevant skill. Triage is for when the team does not know where to start, not when they already know.

---

## Step 1: Quick system scan

Gather the minimum information needed to assess the system's state. This is NOT a full audit — it is a triage scan.

Ask for or confirm:
- System name and approximate size (number of components)
- Primary tech stack (React, Vue, Twig, Web Components, etc.)
- Token system: does one exist? What format? (SCSS, CSS vars, DTCG, Tailwind, none)
- Documentation: is there any? Where does it live?
- Team size: how many people work on the design system?
- Maturity self-assessment: how would the team describe their system? (New, growing, established, struggling, legacy)
- Current pain: what prompted this assessment? What is the most pressing problem?

If the user provides a codebase or repo path, do a quick scan:
- Count component directories
- Check for token files (*.tokens.json, variables.scss, etc.)
- Check for documentation files (README, docs/, etc.)
- Check for consuming apps (apps/, packages/, etc.)
- Check for drift evidence (override files, fork patterns)

A quick scan can miss things: token files named differently, docs in another repo, components outside the directory you counted. When a check finds nothing, say what pattern you used and where you looked ("no files matching `*.tokens.json` or `variables.scss` under `src/`"), and ask the user rather than recording the system as having no tokens or docs. Carry this into the report's Scope line.

## Step 2: Classify the system state

Based on the scan, classify the system into one of four states:

### State A: New or small system (fewer than 5 components, < 1 year old)
**Profile:** Young system, small team, establishing foundations.
**Primary risk:** Building without foundations (tokens, governance, documentation).
**Typical pain:** "We're not sure if we're doing this right."

### State B: Growing system (5–25 components, active development)
**Profile:** Mid-size system gaining adoption, starting to feel friction.
**Primary risk:** Accumulating debt faster than paying it off.
**Typical pain:** "Things are getting inconsistent" or "new teams are struggling to adopt."

### State C: Established system (25+ components, multiple consuming teams)
**Profile:** Mature system with significant investment, maintaining at scale.
**Primary risk:** Drift, governance gaps, documentation staleness.
**Typical pain:** "We don't know the state of things" or "teams are going off-system."

### State D: Legacy or struggling system (any size, declining adoption or significant debt)
**Profile:** System with accumulated problems, possibly declining adoption.
**Primary risk:** System becomes irrelevant as teams work around it.
**Typical pain:** "It's a mess" or "nobody uses it" or "we inherited this."

## Step 3: Produce the run plan

Based on the state classification, produce a prioritised skill run plan.

---

### Design System Ops — triage report

**System:** [name]
**State classification:** [A/B/C/D] — [one-line description]
**Date:** [date]

---

#### Recommended run order

For each recommended skill:

| Priority | Skill | Why now | What it will tell you | Estimated time |
|---|---|---|---|---|
| 1 | [skill name] | [why this is the right first step for this state] | [what you'll learn] | [5–15 min] |
| 2 | ... | | | |
| 3 | ... | | | |

**Limit the initial run to 3–5 skills.** More than that dilutes focus.

---

#### Skills to skip for now

| Skill | Why skip | When to revisit |
|---|---|---|
| [skill name] | [why it's not useful yet for this state] | [specific trigger for when it becomes relevant] |

---

#### Skills to return to later

| Skill | Prerequisite | When to run |
|---|---|---|
| [skill name] | [what needs to happen first] | [timing — e.g. "after token audit remediation is complete"] |

---

**Scope:** [what the quick scan inspected, which checks came back empty and the patterns they used, and what the user told you rather than what you saw]

---

### Run plans by state

These are starting-point recommendations. Adjust based on the specific pain the team reported.

**State A (New/small):**
1. `system-health` — Establish a baseline status per dimension
2. `token-audit` — Verify the foundation is solid before building on it
3. `contribution-workflow` — Establish governance early, before it becomes a problem
4. Skip: adoption-report (too early), drift-detection (no consuming teams yet), deprecation-process (nothing to deprecate), system-benchmark (nothing to benchmark against yet)

**State B (Growing):**
1. `system-health` — Get the current picture
2. `component-audit` — Understand what you have, what's duplicated, what's missing
3. `component-api-validator` — Catch prop and type inconsistencies while the API surface is still small enough to fix
4. `naming-audit` — Catch convention drift before it compounds
5. `adoption-report` — Understand who's using it and who isn't
6. Skip: system-pitch (you already have investment), designer-onboarding (do after audits)

**State C (Established):**
1. `drift-detection` — The biggest risk for established systems
2. `docs-coverage` — Is the documentation keeping pace with the components, or going stale?
3. `token-compliance` — Are tokens being used correctly at scale?
4. `adoption-report` — Who's drifting and why?
5. `system-health` or `system-benchmark` — Overall picture for quarterly review; the benchmark suits teams tracking dimensions over time
6. Skip: system-pitch (not needed), contribution-workflow (likely exists)

**State D (Legacy/struggling):**
1. `system-health` — Honest assessment of where things stand
2. `token-audit` — Understand the structural foundation (or lack thereof)
3. `component-audit` — Map the duplication and coverage gaps
4. `drift-detection` — Quantify how far consuming teams have diverged
5. Then: `stakeholder-brief` — Translate findings into a business case for investment
6. Skip: documentation skills (don't document dysfunction — fix it first), designer-onboarding (premature), change-communication (nothing to communicate yet)

For any state: add `theme-audit` if the system ships more than one theme or mode (dark mode, brands, density), and swap out the lowest-priority item to stay within five.

---

#### What to do with the results

After running the recommended skills:
1. Read the findings from each skill
2. Identify the top 3 themes that appear across multiple skill outputs
3. Use those themes to decide the next action: remediation, governance establishment, stakeholder communication, or documentation
4. Schedule the "return to later" skills based on the sequencing above

---

## Quality checks

- System state classification is justified with specific evidence from the scan
- Empty scan results say which pattern and location were checked; the report has a Scope line
- Run plan is limited to 3–5 skills, not a full list
- "Skip for now" section explains WHY each skill is skipped, not just that it's skipped
- Run plan addresses the specific pain the team reported, not just the generic state recommendation
- Time estimates are realistic for the system's size
- The plan sequences skills so that later skills can build on earlier findings
