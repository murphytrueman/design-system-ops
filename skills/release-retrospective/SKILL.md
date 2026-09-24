---
name: release-retrospective
description: "Review how a shipped release, migration or deprecation went against its plan: blast radius, comms, migration, timeline, support load, each gap classed. Triggers: release retro, post-mortem, how did the deprecation go. Planning a new deprecation: deprecation-process."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(ls:*), Bash(git log:*), Bash(git tag:*), Bash(git diff:*), Bash(rg:*), Bash(grep:*)
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/output-discipline.md
---

# Release retrospective

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Governance currently looks forward: plan the deprecation, estimate the blast radius, write the migration guide. There's no structured skill for reviewing how it actually went. Did the blast radius estimate hold? What did the communication miss? Where did teams get stuck despite the migration guide? A release retrospective completes the governance loop and builds institutional knowledge that keeps a system from repeating the same mistakes across team transitions.

The retrospective is not a blame exercise. It's a learning artifact. The goal is: what changes to our governance process will prevent this specific gap next time? Foreseeable gaps reveal process failures. Unforeseeable gaps become new guardrails.

## Key principles

The release plan is a hypothesis; the retrospective tests it. Plans usually break on five dimensions: blast radius, communication, migration path, timeline and support burden. For each gap, the useful question is whether better analysis would have caught it or whether it was genuinely novel.

The plan was made with incomplete information. The retrospective reveals what was missing. That gap is the insight, not a failure.

Every figure in the retrospective comes from the plan, a tool result or the user. Where a dimension has no data, write "not measured" rather than estimating it. Never estimate reach or completion percentages.

## Configuration

Before writing the retrospective, gather these inputs:

1. **Release or deprecation:** Component name, token set change, system-level refactor, or major version bump. What changed?
2. **Original plan:** Link to the deprecation plan, migration guide, communication package, or governance decision record. Paste key dates, blast radius estimate, phased rollout plan if one existed.
3. **Actual execution:** When did it ship? What was the actual timeline? Which teams/codebases were affected (names or counts)?
4. **Quantitative data:** Instances affected (actual vs estimated). Migration completion rate. Support tickets or Slack threads related to the change.
5. **Qualitative data:** If quantitative isn't available: "three teams asked the same question about X", "one team skipped the codemod and manually updated", "unexpected platform dependency broke the migration".
6. **Communications received:** Which channels reached teams? Did they read the message? Evidence: Slack emoji reactions, email click-through rates, questions showing people didn't read.
7. **Support load:** How many questions in Slack? Escalations? Pattern categories (e.g., "5 questions about X", "2 teams didn't know about the codemod").
8. **Unplanned events:** Platform changes, team reorganizations, urgent hotfixes, or other novel circumstances that affected the release.

## Steps

**Step 1: Gather inputs**

Request the original plan (deprecation plan, migration guide, communication package or decision record) and the execution data listed above. Don't reconstruct the plan from memory or from what you think it probably said; if the user can't supply it, say the comparison is against their recollection and label it that way.

**Step 1b: Measure what the repository can tell you**

Before asking for figures, take the ones git and a search can give:
- **Timeline:** `git tag --list --format='%(refname:short) %(creatordate:short)'` for when the release actually shipped, against the plan's dates
- **Migration completion:** the deprecation plan's usage commands (`rg` for the old component, token or prop) run now over the consumers in reach give the count of references still on the old API; run the same over the plan's baseline commit (`git log -1 --before=<announcement>`) for the starting count. "Completion" is those two counts, not a percentage estimate
- **Consumer activity:** `git log --since=<announcement> --oneline -- <consumer paths>` shows when each consumer migrated, and whether anyone touched the codemod's output by hand

Anything the repository can't show (support load, who read the announcement) comes from the user or is "not measured".

**Step 2: Compare plan and reality, dimension by dimension**

For each dimension where you have data, fill this template once:

```
**[Dimension]**

Planned: [from the plan]
Actual: [from execution data, or "not measured"]
Gap: [what differed]
Class: Foreseeable / Unforeseeable / Process
Specific gaps: [1–3 items, each with its evidence]
Insight: [one sentence: what should we have known, asked or done?]
```

Prompts per dimension:
- **Blast radius:** consumers and instances affected, planned vs actual; unexpected impacts
- **Communication:** channels planned vs used; evidence teams saw it before the deadline (replies, questions that show they didn't); unclear or badly timed messages
- **Migration path:** codemod and manual steps planned vs what teams actually did; edge cases the guide or codemod missed
- **Timeline:** planned milestone dates vs actual; cause of each slip or acceleration
- **Support burden:** support approach planned vs actual load; question patterns by category, not just totals

Gap classes (defined once, used everywhere):
- **Foreseeable:** the analysis was incomplete. Better consumer interviews, codemod testing, platform validation or edge-case exploration would have caught it.
- **Unforeseeable:** a genuinely novel circumstance: reorganisation, platform release, urgent security incident, an unexpected architectural pattern in a consumer.
- **Process:** the analysis was sound but execution faltered: message sent but not read, guide clear but not followed, capacity not available.

**Step 3: Write the retrospective report**

Open with a one-line headline: did it go to plan, and what's the one change that matters most next time. Examples below are illustrative; never carry their figures into real output.

Use this structure:

```markdown
# Release Retrospective: [Release name]

[Headline: one sentence on whether it went to plan and the change that matters most next time]

**Open placeholders:** [list any `[needs data: …]` gaps left in this report, or "none"]

**Release:** [What shipped — component deprecation, token refactor, major version, etc.]
**Date:** [Announcement → Migration deadline → Completion]
**Status:** [On schedule / Delayed / Completed early]

## Summary

[1 paragraph: What was released, when, what actually happened. 
Overall assessment: did it go as planned?]

Example: "We deprecated the legacy Button component on [date]. 
The migration deadline was [date]. All discovered consumers completed migration [n] days early. 
Communication reach: not measured. 
We found two unplanned edge cases in webpack configurations and one incomplete codemod scenario."

## Plan vs Reality

| Dimension | Planned | Actual | Gap | Class |
|---|---|---|---|---|
| **Blast radius** | X teams, Y instances | A teams, B instances | [Describe] | Foreseeable / Unforeseeable / Process |
| **Communication** | [Channels, timing] | [Evidenced reach, or "not measured"] | [Describe] | Foreseeable / Unforeseeable / Process |
| **Migration path** | [Codemod + manual steps, est. time] | [Actual approach, time] | [Describe] | Foreseeable / Unforeseeable / Process |
| **Timeline** | [Key dates] | [Actual dates] | [Describe] | Foreseeable / Unforeseeable / Process |
| **Support burden** | [Planned support approach] | [Actual load, patterns] | [Describe] | Foreseeable / Unforeseeable / Process |

## What worked well

[Items the evidence supports. Keep doing these next time. If nothing clearly worked, say so.]

Example:
- The codemod handled [n] of [n] call sites automatically
- Phased rollout meant we could respond to early feedback before the hard deadline
- Daily office hours during week 1 of migration prevented escalations
- Pre-migration dry-run period (2 weeks) let teams test in their own repos first

## What didn't work

[Items the evidence supports. Stop or change these next time.]

Example:
- FAQ didn't mention webpack configuration workarounds — caused three escalations
- Two teams said they missed the Slack announcement; the email distribution list was outdated
- Migration guide showed code examples for React/Vue but not Svelte consumers
- Support burden on one person created a bottleneck in week 2

## Recommendations for next release

[Specific, actionable changes to governance or process. Each one solves a gap from above and has an owner and a date, or `[needs data: owner]`.]

| Recommendation | Solves | Owner | By |
|---|---|---|---|
| Test the codemod in representative consumer repos (webpack, custom Rollup) before the announcement | foreseeable gap in webpack compatibility | [name] | [date or next release] |
| Refresh the consumer distribution list before each major announcement | process gap in communication reach | [name] | [date] |

## Decision record update

[Only if the retrospective reveals a standing decision should change.]

Example: "Decision record D-004 (Release timing strategy) should be updated 
to require platform-specific validation testing. Current guidance assumes 
standard tooling; update to add complexity estimate for non-standard consumer setups."

Link to updated decision record or create one.

---

**Retrospective completed:** [Date]  
**Prepared by:** [Your name/team]  
**Reviewed by:** [System team lead, key consumer representative]

**Scope**
- **Inspected:** [plan documents, execution data and feedback actually provided]
- **Not inspected:** [dimensions with no data, marked "not measured" above]
- **Assumptions:** [anything taken as given rather than verified]
```

## Quality Checks

1. **Every gap is classified:** No gaps listed without foreseeable/unforeseeable/process mark. Classification is clear.
2. **Recommendations are implementation-ready and owned:** Each recommendation can be turned into a task without additional context, and has an owner and a date or an explicit `[needs data: owner]`. Not "communicate better" but "add platform-specific migration testing to CI before release announcement."
7. **Measured before asked:** timeline and migration completion came from git and the usage search where a repository was in reach; the Scope block says which figures came from the user.
3. **Plan vs reality references original plan:** Not reconstructed from memory. Links to or quotes from the actual plan document.
4. **Findings are evidenced, not balanced for tone:** Include what worked where the evidence shows it; don't invent a positive to soften the report. Missing data is "not measured"; reach and completion percentages appear only if measured.
5. **Support burden identifies patterns, not just totals:** "5 questions about X" is better than "20 total support questions." Patterns drive recommendations.
6. **Gaps are visible:** Fill what's known; list open placeholders at the top; never invent dates, links, owners, rationale or percentages. Opens with a headline and ends with the Scope block.

## Small-system note

For very small system releases (single component deprecation, single token rename):

- Compress the report to a single page: one-line summary per dimension, what worked and what didn't (if evidenced), one recommendation.
- Skip the table format if there's only one or two gaps total; use prose instead.
- Tie the recommendation directly to the next release (e.g., "next time we deprecate a component, use this checklist").
- Focus on process: small releases have small blast radii, so insights are mostly about governance efficiency, not breadth.
