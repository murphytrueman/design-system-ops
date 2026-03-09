---
name: stakeholder-brief
description: "Write a one-page stakeholder brief translating design system health or status into business language. Trigger when someone says: stakeholder update, exec brief, leadership summary, status report for leadership, system status for non-designers, write a brief for the business, or anything about communicating design system status to an audience that does not have a design systems background."
references:
  - references/output-discipline.md
---

# Stakeholder brief

A skill for writing a one-page stakeholder brief that translates design system health, status, or a specific recommendation into business language. Output requires no design systems knowledge to read, leads with business impact, and ends with a clear ask.

## Context

Design systems teams are often better at building systems than at communicating their value to the people who fund and prioritise them. The result is that design systems work gets under-resourced, and the case for investment gets made reactively — when something breaks — rather than proactively, when there is time to think clearly.

A stakeholder brief is not a technical report with a summary at the top. It is a business communication that happens to be about design systems work. The reader should be able to understand the situation, the recommendation, and the ask without any prior knowledge of what a design system is or how it works. If a term requires explanation, the explanation belongs in the brief, not in a separate glossary.

## Step 0: Check for existing context

Before asking the user for the situation and findings, check whether another skill has already produced output in this session:

- If a **system-health** report exists in context, pull the dimension statuses, maturity stage, and top findings directly. Do not re-ask for the situation — the health report is the situation.
- If a **token-audit**, **component-audit**, **drift-detection**, or **naming-audit** report exists, pull the key findings and translate them into business language for the brief.
- If a **system-benchmark** report exists, use the comparison findings to frame the recommendation.

When pulling from another skill's output, cite it: "Based on the system health assessment completed earlier..." This connects the brief to the evidence and makes the chain of work visible.

If no prior output exists, proceed to Step 1 as normal.

## Step 1: Establish the brief's purpose

Ask for or confirm:
- What is this brief for? (Status update / investment ask / specific recommendation / incident summary / launch announcement)
- Who is the primary audience? (VP, C-suite, product director, budget owner — this determines the level of business abstraction)
- What is the one thing the reader should do or believe after reading it?
- What is the underlying situation? (Health report findings, a specific blocker, a proposed investment, a recent achievement)
- Is there a deadline or decision this brief is feeding into?

The brief should have a single primary purpose. A brief that tries to deliver a status update and make an investment ask and announce a new feature is three briefs, and it will not do any of them well.

**Small-system note (fewer than 5 components):** For systems with fewer than 5 components, the brief needs to frame the system as a deliberate, focused investment rather than something that is small because it is under-resourced. Use "specialised system" or "targeted component library" framing. The ROI argument shifts from scale efficiency ("20 teams reuse the same components") to quality consistency ("every customer-facing surface uses the same interaction patterns") and speed ("new features compose from proven components instead of starting from scratch"). Avoid metrics that make a small system look weak by enterprise standards — "3 components" sounds unimpressive without context. Instead, lead with what those components cover: "Our component library handles 80% of our interface patterns, ensuring consistent experience across all product surfaces."

## Step 2: Write the brief

---

### [Brief title — describes the situation and the ask in plain language]

**Date:** [date]
**Prepared by:** [name]
**For:** [audience]
**Regarding:** [one-sentence description of the subject]

---

#### The situation

Two to four sentences. What is the current state of affairs that makes this brief necessary? Write in terms of business impact, not design system mechanics.

Not: "The design system has 42 components and a 60% engineering adoption rate across product teams."
But: "Three product teams are currently maintaining separate, inconsistent versions of core interface components. This creates inconsistent customer experiences and duplicates development effort across the organisation."

If the situation requires a brief explanation of what a design system is: include one sentence, maximum. Do not assume the reader knows. Do not spend three sentences explaining — one sentence is the limit. "A design system is the shared library of interface components that product teams reuse instead of rebuilding." That is enough. If the reader needs more, they will ask. Every word spent explaining what a design system is costs a word that could be spent on why this brief matters.

---

#### Why this matters

Two sentences. Not three. Two. This section is the sharpest paragraph in the brief — it must create urgency, not explain context. Write the first sentence as the cost of inaction. Write the second sentence as the opportunity cost.

Pattern: "[What is being lost/risked right now]. [What could be gained if this is addressed]."

Example: "Every sprint, three teams spend an estimated 40 engineering hours maintaining separate versions of components the system already provides. That effort could instead ship two additional product features per quarter."

Avoid design system metrics as evidence. "Low token adoption" is not a business problem. "Inconsistent interfaces are generating 15% more support tickets on pages that diverge from the system" is a business problem. Find the number and the consequence.

If you have data, lead with it — numbers in this section are more persuasive than anywhere else in the brief. If you do not, be honest about what is estimated and state the basis: "Based on the team's sprint velocity and the duplicated work visible in the codebase, we estimate..."

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

## Step 2b: Business metrics translation guide

Design system health metrics do not land with stakeholders unless they are translated into business consequences. Use this reference when writing the "Why this matters" section:

| Design system metric | Business translation |
|---|---|
| Low token adoption | "Visual inconsistency across products is creating a fragmented brand experience" |
| High component drift | "Teams are maintaining separate versions of the same interface elements, duplicating engineering effort" |
| Poor documentation coverage | "New team members take longer to become productive because system knowledge is tribal, not documented" |
| Low accessibility scores | "We have measurable compliance gaps that create legal exposure and exclude users with disabilities" |
| Declining adoption | "Teams are choosing to build independently rather than use shared infrastructure — the system is not serving their needs" |
| No AI-readiness | "Our component library cannot be consumed by AI development tools, which means we are not benefiting from AI-assisted coding workflows" |
| Version lag across teams | "Multiple teams are running outdated versions, which means bug fixes and improvements are not reaching users" |
| Missing governance process | "There is no defined process for how the system evolves, which creates unpredictability for teams that depend on it" |

When writing the brief, choose the 1–2 translations most relevant to the audience's priorities. Do not list all of them — a brief with eight business consequences reads as a list of complaints, not a focused argument.

## Step 3: Review for business language

Before delivering the brief, read it from the perspective of a VP or director who has no design background. Flag any term or concept that requires prior knowledge to understand. Translate or remove.

Common terms that need translation in stakeholder briefs:
- "Design system" — explain briefly on first use
- "Design tokens" — "the shared variables that control visual consistency across products"
- "Component library" — "the shared set of pre-built interface elements"
- "Storybook" — name is fine, explain it is a documentation and testing environment
- "WCAG" — "the international accessibility standard"
- "Technical debt" — can usually stay, but be specific about what the debt is

## Step 4: Confirm the one-page constraint

Stakeholder briefs should fit on one page or the equivalent — approximately 400 to 500 words. If the brief exceeds this, cut:
- First: background that the reader already has
- Second: technical detail that is not required for the decision
- Third: qualifications and caveats that do not change the recommendation

If the full context genuinely requires more space, produce the brief as the primary document and attach supporting material separately. The brief should be complete without the attachments — attachments are for readers who want more depth, not for information required to understand the ask.

## Step 5: Platform and maturity framing (staff-level)

At the staff level, stakeholder briefs should frame the design system as infrastructure, not as a design convenience. This changes how the situation, recommendation, and outcome are written.

**Infrastructure language:**
- Instead of "the design system needs investment" → "our component infrastructure has reliability gaps that are creating downstream production cost"
- Instead of "teams are building outside the system" → "teams are creating parallel infrastructure because the shared platform doesn't cover their needs — each parallel implementation costs [X] and creates a maintenance liability"
- Instead of "we need a dedicated team" → "the infrastructure needs a defined SLA: expected response time for bug reports, predictable release cadence, and documented API contracts"

**Maturity stage context:**
If a system-health assessment has been completed, reference the maturity stage in the brief. Frame the recommendation as moving from the current stage to the next:
- "We are currently at the Managed stage — the system exists and is used, but governance is informal and documentation is inconsistent. The recommendation moves us to Systematic, which requires [specific actions]."
- Stakeholders respond to clear progression frameworks. Maturity stages make the investment concrete and the progress visible.

**AI-readiness as a competitive/efficiency argument:**
If relevant to the organisation, include the AI-readiness angle: "Design systems that are machine-readable enable AI-assisted development — code generation, automated testing, and design-to-code workflows. Our current system is not structured for AI consumption. The proposed investment includes making the system machine-readable, which positions the organisation to benefit from AI tooling without a separate initiative."

## Quality checks

- No design system jargon that is unexplained
- The situation section describes a business problem, not a design system metric
- A specific recommendation is present, not a general direction
- The ask is three items or fewer, each specific and actionable
- The brief fits on one page
- A reader with no design systems background can understand the situation and the ask
- The expected outcome is honest about timeline and scope
- If maturity level is referenced, it is explained in plain terms with evidence
- If AI-readiness is referenced, the business value is framed in terms the audience understands (efficiency, speed, competitive positioning), not in technical terms
