---
name: stakeholder-brief
description: "Turns design system status or a recommendation into a one-page brief in business language. Use it whenever someone wants an update, summary or note on the system for a VP, exec or stakeholder, however short. Investment case: system-pitch. Charts: visual-report."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(ls:*)
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/executive-communication.md
  - ../../knowledge-notes/output-discipline.md
---

# Stakeholder brief

A skill for writing a one-page stakeholder brief that translates design system health, status, or a specific recommendation into business language. Output requires no design systems knowledge to read, leads with business impact, and ends with a clear ask.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Design systems teams are often better at building systems than at communicating their value to the people who fund and prioritise them. The result is that design systems work gets under-resourced, and the case for investment gets made reactively — when something breaks — rather than proactively, when there is time to think clearly.

A stakeholder brief is not a technical report with a summary at the top. It is a business communication that happens to be about design systems work. The reader should be able to understand the situation, the recommendation, and the ask without any prior knowledge of what a design system is or how it works. If a term requires explanation, the explanation belongs in the brief, not in a separate glossary.

Audience calibration, framing patterns, metric translation, anti-patterns and the numbers-honesty rules are shared with system-pitch and live in the executive-communication note.

## Workflow overview

1. **Establish the brief's purpose** — Confirm the context, the sources and the single ask
2. **Write the brief** — The five-part template with business framing
3. **Calibrate to the audience and choose the frame** — From the executive-communication note
4. **Frame maturity (staff-level)** — Named stages and the next transition, when an assessment exists
5. **Quality checks** — No jargon, one page, every figure sourced

---

## Step 1: Establish the brief's purpose

Ask for or confirm:
- What is this brief for? (Status update / specific recommendation / incident summary / launch announcement). A full investment case with cost of current state and ROI is a pitch, not a brief — use system-pitch.
- Who is the primary audience? (VP, C-suite, product director, budget owner — this determines the level of business abstraction)
- What is the one thing the reader should do or believe after reading it?
- What is the underlying situation? (Health report findings, a specific blocker, a proposed investment, a recent achievement)
- Is there a deadline or decision this brief is feeding into?
- What are the sources? If system-health, adoption-report or other skill output exists, use its figures and cite it. Facts about the system come from those outputs, inspected files, or the user; anything else stays as `[needs data: …]`.

The brief should have a single primary purpose. A brief that tries to deliver a status update and make an investment ask and announce a new feature is three briefs, and it will not do any of them well.

**Small-system note (fewer than 5 components):** For systems with fewer than 5 components, the brief needs to frame the system as a deliberate, focused investment rather than something that is small because it is under-resourced. Use "specialised system" or "targeted component library" framing. The ROI argument shifts from scale efficiency ("20 teams reuse the same components") to quality consistency ("every customer-facing surface uses the same interaction patterns") and speed ("new features compose from proven components instead of starting from scratch"). Give the size plainly and give it context in the same sentence: "three components, covering [share of interface patterns, from an inventory or audit]". Choosing which true figures to show is framing; leaving out a figure because it sounds small is the "only good news" anti-pattern in the executive-communication note, and a reader who later learns the number stops trusting the brief.

---

## Step 2: Write the brief using the five-part template

---

### [Brief title — describes the situation and the ask in plain language]

**Date:** [date]
**Prepared by:** [name]
**For:** [audience]
**Regarding:** [one-sentence description of the subject]
**Open placeholders:** [every `[needs data: …]` left in the brief, or "none"]

---

#### The situation

Two to four sentences. What is the current state of affairs that makes this brief necessary? Write in terms of business impact, not design system mechanics.

Not: "The design system has 42 components and a 60% engineering adoption rate across product teams."
But: "Three product teams are currently maintaining separate, inconsistent versions of core interface components. This creates inconsistent customer experiences and duplicates development effort across the organisation."

If the situation requires a brief explanation of what a design system is: include one sentence. Do not assume the reader knows. Do not patronise them with a long explanation. "A design system is the shared library of interface components and visual standards that product teams use to build consistently without building from scratch each time" is usually sufficient.

---

#### Why this matters

Two to three sentences. What is the business consequence of the situation? Translate into the currency that matters to this audience: time, money, customer experience, risk, competitive position.

Avoid design system metrics as the evidence of impact. "Low token adoption" is not a business problem. "Inconsistent interfaces are generating support tickets and reducing customer trust" is a business problem. Find the business translation.

If you have data, use it and name its source. If you do not, label the figure as estimated and show why the estimate is reasonable, or leave `[needs data: …]`. Derived figures (FTE equivalents, totals) are recomputed from the inputs shown.

---

#### What we recommend

One sentence stating the recommendation. Then two to four sentences explaining why this recommendation over the alternatives.

Be specific. "Invest in the design system" is not a recommendation. "Dedicate one engineering day per sprint to design system integration across the three product teams, for the next two quarters, to consolidate the parallel component implementations" is a recommendation.

If there are alternatives, acknowledge the most plausible one and explain why the recommendation is preferred. A brief that presents only one option looks like it has not considered the problem fully.

---

#### What we need

The ask. One to three specific items. Each item should be concrete: a decision, a resource allocation, an approval, or a timeline confirmation.

Format:
- [Specific ask 1]
- [Specific ask 2]
- [Specific ask 3, if needed]

No more than three items. A brief with six asks does not get any of them approved.

---

#### Expected outcome

Two to three sentences. If the recommendation is followed and the ask is granted: what changes, when, and what does success look like?

Be honest about timelines and realistic about what the investment will and will not solve. Overpromising in a stakeholder brief erodes trust faster than almost anything else.

---

Close with one line: `Based on: [sources, with dates]` — for example, "Based on: system-health assessment, 10 March 2026; adoption figures reported by the design systems team."

---

## Step 3: Calibrate to the audience and choose the frame

Use the executive-communication note for this step:
- **Audience calibration** — what engineering, product, design and executive readers care about, what to lead with, the language that lands, and what to avoid
- **Framing patterns** — lead with growth, risk or cost, matched to the reader's priorities
- **Translating system metrics** — choose the one or two business translations most relevant to the reader for "Why this matters"

---

## Step 4: Maturity-stage framing (staff-level)

At the staff level, frame the design system as infrastructure, not as a design convenience (the infrastructure language is in the executive-communication note).

If a system-health assessment has been completed, use the maturity stage it gave, by name: Ad-hoc, Managed, Systematic, Measured or Optimised. Never numbered levels. Explain the stage in one plain sentence, cite the assessment, and frame the recommendation as the transition to the next stage. If no assessment exists, don't infer a stage for the brief; leave maturity out or ask the user.

What the next stage requires comes from the evidence checklist in the component-governance note; quote the one or two items the system is missing, not the whole list.

Example: "We are currently at the Managed stage — the system exists and is used, but governance is informal and documentation is inconsistent (Q1 system-health assessment). The recommendation moves us to Systematic, which requires documented contribution and deprecation processes."

**AI readiness:** mention it only if the reader has asked about AI tooling, and only with the system-health AI-readiness status as the source, in one plain sentence about what it enables (coding agents that pick the right component and use the right tokens). Don't add it as an unprompted selling point; it reads as a pitch in a status brief.

---

## Step 5: Quality checks

Before delivering the brief, verify all of these:

- No design system jargon that is unexplained
- The situation section describes a business problem, not a design system metric
- A specific recommendation is present, not a general direction
- The ask is three items or fewer, each specific and actionable
- The brief fits on one page (approximately 400-500 words)
- A reader with no design systems background can understand the situation and the ask
- The expected outcome is honest about timeline and scope
- Every figure traces to a named source (file, tool output, prior skill output, or the user) and is labelled measured, estimated or assumed; derived figures are recomputed
- Open placeholders are listed at the top, and the brief ends with a `Based on: [source, date]` line
- If maturity is referenced, it is a named stage from a cited assessment, explained in plain terms
- If AI-readiness is referenced, the business value is framed in terms the audience understands (efficiency, speed, competitive positioning), not in technical terms
- Tone and framing pattern (growth/risk/cost) match the audience's priorities
- None of the anti-patterns in the executive-communication note are present

---

## Recurring briefs

For quarterly stakeholder briefs:
1. Run this skill after `system-health` completes
2. Pass the health assessment findings as input, and cite the assessment in the `Based on:` line
3. Output is a brief ready for leadership distribution once its open placeholders are resolved
4. Archive the brief alongside the project's decision records
