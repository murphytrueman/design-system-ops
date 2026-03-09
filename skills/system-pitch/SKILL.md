---
name: system-pitch
description: "Write a design system investment pitch with a business case and ROI framing. Trigger when someone says: pitch the design system, make the case for the system, sell this to leadership, justify the investment, business case for design systems, why should we invest in a design system, or anything about building an argument for design system investment or continuation."
---

# System pitch

A skill for writing a design system investment pitch that leads with a business problem, builds an honest ROI case, and addresses likely objections. Output is a pitch document that works for an audience who has never heard of a design system and does not need to.

## Context

Design system pitches usually fail for one of two reasons. They lead with the design system — its components, its tokens, its Storybook — rather than with the business problem it solves. Or they oversell: promising a design system will solve problems it cannot solve, which creates scepticism or, worse, expectation debt that damages credibility when the system ships and the promised outcomes do not materialise.

The pitch that works leads with the cost of the current state. It makes the reader feel the friction of inconsistency, the waste of duplicated effort, the risk of inaccessible interfaces — before it introduces the design system as the solution. Then it is specific about what the investment costs, honest about the timeline, and precise about what success looks like.

## Step 1: Understand the context

Ask for or confirm:
- Is this a pitch for a new design system, or a pitch to continue investing in an existing one?
- What is the current state? (Multiple teams building the same things independently / an existing system with low adoption / no system at all)
- What is the organisation? (Size, product count, team structure)
- Who is the audience for this pitch? (Executive, product leadership, engineering leadership, combined)
- What is the likely objection? (Cost, timeline, team capacity, "we tried this before")
- Is there any existing data available? (Time spent on inconsistent work, accessibility incident history, customer complaints about inconsistency)

The "likely objection" is important. A pitch that does not address the elephant in the room leaves the reader thinking about it instead of engaging with the argument.

**Small-system note (fewer than 5 components):** For small teams or products, the pitch faces a different objection: "Why do we need a design system? Can't we just coordinate?" The answer is that coordination without a system is coordination without a contract — it works until someone is on holiday, until a new team member joins, or until the product grows past the point where everyone can hold the conventions in their heads. The ROI framing shifts from "eliminate duplicated effort across 20 teams" to "protect consistency as the team grows, reduce onboarding time for new designers and developers, and make accessibility compliance a default rather than a per-feature effort." If the system already exists at this size, the pitch is usually for continued investment or formalisation — frame the ask around what has already been achieved informally and why it is worth making durable.

## Step 1b: Business metrics worksheet

Before writing the pitch, estimate the cost of the current state. These numbers power the "cost of the current state" section and make the ROI argument concrete.

**Cost estimation worksheet:**

1. **Duplicated effort:** How many teams are independently building the same UI patterns?
   - Teams: ___
   - Estimated hours per team per quarter on duplicated work: ___
   - Estimated cost: ___ teams × ___ hours × hourly rate = ___/quarter

2. **Inconsistency cost:** How many customer-facing inconsistencies exist?
   - Known support tickets related to UI inconsistency: ___
   - Estimated impact on customer trust: [qualitative assessment]

3. **Onboarding cost:** How long does it take a new designer/developer to learn current conventions?
   - Current onboarding time for conventions: ___ days
   - Estimated onboarding time with a documented system: ___ days
   - Savings per new hire: ___ days × daily rate = ___

4. **Accessibility risk:** What is the current compliance state?
   - Known accessibility violations: ___
   - Estimated remediation cost if addressed per-product: ___
   - Estimated remediation cost if addressed at system level: ___

5. **Speed cost:** How much longer do features take without shared components?
   - Estimated additional time per feature: ___ days
   - Features shipped per quarter: ___
   - Total additional cost: ___ days × ___ features × daily rate = ___/quarter

Not all of these will have hard numbers. Use conservative estimates where data is not available, and state the assumptions. A pitch with honest estimates and visible reasoning is more credible than one with precise numbers and hidden assumptions.

## Step 2: Write the pitch

---

### [Title — frames the problem, not the solution]

**Prepared by:** [name]
**Date:** [date]
**For:** [audience]

---

#### The cost of the current state

Start with the problem. Do not name the solution in the first section.

Describe what is happening now that is costing time, money, quality, or trust. Use specific examples where available. If data is available, use it. If estimates must be used, frame them conservatively and show the reasoning.

Common angles that land with business audiences:
- Duplicated effort: "We estimate that [n] engineering teams have each built their own version of [core pattern]. That represents [n] weeks of duplicated work."
- Quality inconsistency: "Customers encounter [n] distinct visual treatments for the same interaction type across our products. This creates confusion and erodes trust."
- Accessibility risk: "Our current approach leaves accessibility compliance to each team individually. [n] of [n] audited flows have accessibility violations."
- Onboarding cost: "New product designers and developers spend [n] weeks building up context about our interface conventions that could be available on day one."
- Speed: "New features take [n] weeks longer to design and build than comparable work at organisations with mature design systems, based on [benchmark or internal data]."

Use the best angle for the audience and the context. Avoid using all of them — a pitch that lists every possible benefit sounds like it is trying too hard.

---

#### What a design system does

One paragraph. No jargon. The clearest possible description of what the investment delivers.

The goal is not to explain what a design system is technically. It is to describe what changes for the business. "A shared library of interface components that every product team uses" is half of it. "So that each team builds faster, more consistently, and without solving the same problems twice" is the other half. Together, one sentence.

---

#### The investment

Be specific about what is being asked for. Avoid vague requests for "resources" or "support."

Frame the investment in terms the audience understands:
- Headcount (if asking for team members)
- Time allocation (if asking for engineers to contribute)
- Budget (if tooling or external support is involved)
- Timeline (what the investment looks like over time)

Present the investment as proportional to the problem. If the cost-of-current-state section identified [n] weeks of duplicated effort per year, and the investment is [n] weeks of initial build effort, the arithmetic should be visible.

---

#### What success looks like

Be specific and honest. Define success in business terms and set a realistic timeline.

Not: "Teams will be more consistent and efficient."
But: "Within six months, all three web product teams will be building new features from the shared component library. Within twelve months, time-to-first-review for new feature designs will decrease by [estimate] because designers will be composing from existing patterns rather than designing from scratch."

Name what the investment will not solve. Pitches that leave this implicit invite disappointment. "This investment will not resolve our accessibility debt overnight — it will prevent new debt from accumulating and create a path to addressing the existing issues systematically."

---

#### Addressing the likely objection

One to two paragraphs directly engaging with the most predictable counter-argument.

Common objections and honest responses:

**"We tried this before and it didn't stick."**
Acknowledge it. "The previous attempt [describe what happened] for specific reasons. This proposal differs in [specific ways that address the previous failure mode]." Do not dismiss the concern.

**"We don't have the capacity right now."**
"The question is not whether we have capacity to build a design system. It is whether we can afford to keep paying the cost of not having one. The current approach is not free — it is just paying in a different currency."

**"This will slow teams down while they learn the system."**
"There is a short onboarding period. Based on comparable implementations, teams typically reach parity within [n] sprints and operate faster than pre-system pace within [n] quarter(s)."

---

#### The ask

One sentence. What is needed, and by when?

Then the specific items. No more than three.

---

## Quality checks

- The pitch leads with the business problem, not the design system solution
- Cost-of-current-state section uses specific examples or conservative estimates with visible reasoning
- Investment ask is specific: headcount, time, or budget — not "resources"
- Success definition is in business terms with a timeline
- The likely objection is directly addressed, not avoided
- No design system jargon that is unexplained
- The pitch is honest about what the investment will not solve
- The ask is three items or fewer and is stated in one sentence before the detail
