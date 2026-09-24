---
name: contribution-workflow
description: "Design or document how new work enters a design system: contribution types, proposal criteria, review stages, sign-off and release. Triggers: contribution process, how should someone contribute, contribution guidelines, adding a new component. Not for audit findings to tickets (backlog-generator)."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(ls:*), Bash(find:*)
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/output-discipline.md
---

# Contribution workflow

A skill for creating a structured contribution workflow covering the full journey from proposal to release. Output is a document teams can actually follow — not a policy statement, but a process with named stages, decision criteria, and clear ownership at each gate.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Most design systems have one of two contribution problems. Either there is no process, so contributions arrive inconsistently and the design systems team becomes a bottleneck because every request is a negotiation. Or there is a process that is so heavy it discourages contribution entirely, and teams build locally rather than bother.

The goal here is a workflow that is lightweight enough to not be a burden, structured enough to produce consistent quality, and honest enough to tell contributors what will and will not make it into the system.

The six-stage structure below reflects the full lifecycle of a contribution; it is the shape most published contribution models share (Nathan Curtis and Brad Frost have both written it up), not this pack's invention. Not every contribution needs all six stages at the same depth — a small enhancement to an existing component is lighter than a new foundational component. The workflow scales accordingly, and the output notes where the path diverges by contribution type.

---

## Step 1: Understand the current state

Ask for or confirm:
- Does a contribution process already exist? If so, what is working and what is not?
- Who is responsible for design system maintenance — a dedicated team, shared responsibility, or a single person?
- What types of contributions are most common? (New components, enhancements, token changes, documentation, bug fixes)
- What is the team's capacity for reviewing and integrating contributions?

Capacity is the variable most contribution processes ignore. A six-stage review process designed for a four-person dedicated team will break immediately if there is only one part-time maintainer. So decide the shape before writing, from the answers above:

- **Lightweight** (one maintainer, or part-time ownership): Propose (a paragraph) → Build (maintainer review) → Ship (docs and a release note). Three stages, no SLAs beyond "the maintainer replies within [n] days".
- **Standard** (a small dedicated team, a handful of consuming teams): the six stages, with community review abbreviated to a release-note preview for all but new components.
- **Full** (a dedicated team, many consuming teams): all six stages at full depth, with the versioning and consumer-check sections.

Say which shape you chose and why in the document's header. Writing the full process and "calibrating it down" afterwards leaves a document nobody follows.

**If nobody owns the system** (the user can't name who would review a proposal), the workflow has no reviewer and there is nothing to write yet. Say so and stop: the first decision is ownership, and `decision-record` can capture it.

Read `CONTRIBUTING.md`, the PR template and `.github/ISSUE_TEMPLATE/` before asking; if a process exists, this skill updates it and says what changed.

**Small-system note (fewer than 5 components):** For systems this size, the full six-stage workflow is almost certainly too heavy. Produce a lightweight three-stage workflow instead: Propose (async, one paragraph) → Build (with review from the maintainer) → Ship (documentation + release note). The community review stage and the detailed assessment stage add overhead that small teams cannot absorb. The contribution criteria should still be documented — but they can be a short checklist, not a policy document. Ask: "Is there one person maintaining this, or is it shared?" If one person, the workflow is essentially "talk to them first."

## Step 2: Write the contribution workflow

---

### Design system contribution workflow

**Version:** [version number or date]
**Owner:** [who maintains this document]
**Last reviewed:** [date]

---

#### Contribution types

Before the stages, establish the contribution types. Different types move through the process at different speeds.

**Type A: Bug fix or small enhancement**
Scope: Correcting a documented error, adding a missing state, fixing a token reference.
Path: Lightweight — skips proposal and community review, moves directly to build.

**Type B: Component enhancement**
Scope: Adding a new variant, prop, or behaviour to an existing component.
Path: Standard — proposal, design review, build, documentation, release.

**Type C: New component**
Scope: A component that does not currently exist in the system.
Path: Full — all six stages.

**Type D: System-level change**
Scope: Token architecture changes, naming convention updates, governance policy changes.
Path: Full, with extended community review. These changes have the widest blast radius.

---

#### Stage 1: Proposal

**Purpose:** Establish whether a contribution is worth building before anyone builds it.

**What the contributor submits:**
- What they want to add or change, in one sentence
- The problem it solves and for which product contexts
- Evidence of the need: two or more distinct product use cases, not just a single team's request
- Whether they are aware of anything in the current system that partially addresses this need

**Proposal template:**

```
## Contribution proposal

**What:** [One sentence — what you want to add or change]
**Why:** [The problem this solves, in business or user terms]
**Evidence:** [Two or more distinct product use cases demonstrating the need]
**Existing awareness:** [What currently exists in the system that partially addresses this? Why is it insufficient?]
**Ownership:** [Who will own the build, documentation and ongoing maintenance? Name a person or team for each]
```

Also write the template where proposals will actually be filed. On GitHub that is an issue form, `.github/ISSUE_TEMPLATE/contribution-proposal.yml`, with one field per line above (the `Evidence` and `Ownership` fields required) and a `contribution` label; on a docs platform, the same fields as that platform's template. A process whose entry point is a wiki page gets proposals in Slack.

**What happens next:**
The design systems team reviews the proposal within [SLA — e.g. five working days]. Three outcomes are possible:
- Accepted: proceed to Stage 2
- Deferred: the need is real but the timing or scope is wrong — include a reason and a re-evaluation date
- Declined: the need is better served by a local solution or does not meet the contribution criteria — include a reason

**Deferred proposals:** Proposals marked as "deferred" are real needs with wrong timing. To prevent them from being forgotten:
- Assign a re-evaluation date (typically next quarter or next planning cycle)
- Log the proposal in the system's backlog with the original evidence
- Notify the contributor when the re-evaluation date arrives
- If the same need surfaces from a second team before the re-evaluation date, bring the re-evaluation forward — repeated need is strong evidence, but it still has to meet the criteria below

**Contribution criteria checklist:**
A proposal meets the criteria if it satisfies all five from the component-governance note:
- [ ] **Recurrence:** the need appears across multiple products or teams, not just one
- [ ] **Generality:** it solves the category of problem, not one team's instance
- [ ] **Accessibility:** it can be implemented accessibly without significant design compromise
- [ ] **Ownership:** someone is named to own the build, documentation and maintenance
- [ ] **Fit:** it is consistent with the system's existing patterns, conventions and architecture, and doesn't duplicate something already in the system or another active proposal

Document why each declined proposal was declined. This creates a record that protects the team from re-litigating the same decisions and gives contributors an honest answer.

---

#### Stage 2: Design

**Purpose:** Establish the design direction and component API before any build work begins.

**What the contributor produces:**
- Design exploration covering the primary use case and at least two edge cases
- Proposed component API: props, types, defaults, and states
- Accessibility considerations: keyboard interaction, ARIA role, focus behaviour
- Token usage: which existing tokens will be used, and whether any new tokens are needed

**Review:**
Design review with the design systems team and, where possible, a representative from each product team that raised the original need. One round of structured feedback, then sign-off.

Sign-off criteria:
- Component API is stable enough to build against
- No known accessibility blockers
- Token usage is consistent with existing patterns or new tokens are justified
- Edge cases have been considered and handled, not deferred

If new tokens are needed, the token decision runs in parallel and must be resolved before Stage 3 begins.

---

#### Stage 3: Build

**Purpose:** Implement the component to the agreed spec.

**What the contributor produces:**
- Component implementation against the agreed API
- Unit tests covering all props, states, and interactive behaviour
- Accessibility tests: keyboard navigation, screen reader, colour contrast
- Storybook or equivalent — one story per documented state

**Handshake points:**
Mid-build check with the design systems team when the happy path is functional but before edge cases and tests are complete. Catch misalignments early.

Build is considered complete when:
- All agreed states are implemented and tested
- Accessibility tests pass at WCAG 2.2 AA. Some legal baselines (e.g. EN 301 549) still reference WCAG 2.1 AA; use that if it's the team's obligation.
- Design-to-code alignment has been reviewed by the original designer

---

#### Stage 4: Documentation

**Purpose:** Make the component usable by teams who were not in the room when it was designed.

**What must be documented before release:**
- Usage guidelines: when to use, when not to use, and two to three common anti-patterns
- Props reference: every prop with type, default, and one-sentence description
- Accessibility: the specific keyboard and screen reader behaviour for this component
- Examples: at least the primary use case and one edge case

The `ai-component-description` skill should also be run at this stage to produce the Figma MCP-optimised description.

Documentation is not complete until someone who was not involved in the build can follow the guidelines to use the component correctly. Consider a brief documentation review with a designer from a consuming team.

---

#### Stage 5: Community review

**Purpose:** A final check before release, giving consuming teams visibility before the component ships.

For Type A and B contributions, this stage can be abbreviated to a release note preview.

For Type C (new components) and Type D (system-level changes): share the component and documentation with consuming teams at least [SLA — e.g. one week] before release. Invite feedback. Document any significant responses. Make the rationale for any changes or non-changes explicit.

This stage is not a veto mechanism. It is a courtesy that reduces post-release surprises and builds contributor trust.

---

#### Stage 6: Release

**Purpose:** Ship the contribution with enough communication that consuming teams know it exists and can use it.

**What ships:**
- Component in the system at its documented version
- Release notes covering what is new, any migration considerations, and links to documentation
- Announcement through the team's standard channels

Release notes for a new component should name the contributor. Contribution is a social act as much as a technical one.

After release: log the contribution in the system's change history and update the proposal record with the outcome.

---

#### What does not go into the system

As important as the stages above: be explicit about what the contribution process is not for.

The system does not accept:
- Components that solve a single team's specific problem without broader applicability
- Components that duplicate existing functionality without a clear migration path for the old version
- Components that cannot be implemented accessibly
- Work that the contributor is not willing to document

Saying no clearly is part of a healthy contribution process. A system that accepts everything eventually becomes a system no one trusts.

#### Rejection decision record

When a proposal is declined, document the decision using the `decision-record` skill. The record should include:
- The proposal that was declined
- The specific criteria it did not meet
- The alternative recommended to the contributor
- Under what conditions the decision might be revisited

Rejection records serve two purposes: they give the contributor a clear, written explanation, and they prevent the same proposal from being re-litigated without new evidence. A healthy contribution process produces rejection records as often as it produces new components.

---

#### Versioning and consumer checks

`version-bump-advisor` makes the semver call at the Release stage for every contribution type; this document doesn't restate its rules. Two expectations belong here: a Type B enhancement is additive (existing props, defaults and behaviour don't change; if they must, it's a breaking change and `deprecation-process` plans the old behaviour's removal), and a Type C component ships with its public API named in the release notes (props, types, defaults) and marked alpha or beta if it may still change.

For Type C and Type D in the **full** shape, add a consumer check between community review and release: in a monorepo, run the consuming applications' test suites against the change; across repositories, ask each consuming team to run theirs on a pre-release tag, and record who did. It turns "we told them" into "we checked".

## Step 3: Check the shape against capacity

Reread the document against the capacity from Step 1: every SLA has a named owner who has the time, and no stage exists that the team can't staff. If a stage doesn't survive that check, remove it rather than leaving it as aspiration.

## Quality checks

- Contribution types are defined before the stages — different types have different paths
- Every stage has a clear output and a clear sign-off condition
- SLA placeholders are flagged and must be filled in before the document is used
- Decline criteria exist and are documented — the process can say no
- The shape (lightweight, standard, full) was chosen from capacity before writing, and every stage has an owner who can staff it
- The proposal template was written as an issue form or platform template, not only in the document
- The document is written for contributors, not for the design systems team to hide behind
