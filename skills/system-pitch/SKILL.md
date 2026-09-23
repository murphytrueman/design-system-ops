---
name: system-pitch
description: "Investment pitch for a new or continuing design system: cost of current state, ROI with visible assumptions, objections, the ask. Triggers: pitch the system, business case, justify the investment, sell this to leadership. For a routine status update use stakeholder-brief."
references:
  - ../../knowledge-notes/executive-communication.md
  - ../../knowledge-notes/output-discipline.md
---


# System pitch

A skill for writing a design system investment pitch that leads with a business problem, builds an honest ROI case, and addresses likely objections. Output is a pitch document that works for an audience who has never heard of a design system and does not need to.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Design system pitches usually fail for one of two reasons. They lead with the design system — its components, its tokens, its Storybook — rather than with the business problem it solves. Or they oversell: promising a design system will solve problems it cannot solve, which creates scepticism or, worse, expectation debt that damages credibility when the system ships and the promised outcomes do not materialise.

The pitch that works leads with the cost of the current state. It makes the reader feel the friction of inconsistency, the waste of duplicated effort, the risk of inaccessible interfaces — before it introduces the design system as the solution. Then it is specific about what the investment costs, honest about the timeline, and precise about what success looks like.

Audience calibration, framing patterns, metric translation, anti-patterns and the numbers-honesty rules are shared with stakeholder-brief and live in the executive-communication note. This skill covers what is specific to an investment case.

## Workflow overview

1. **Understand the context and gather evidence** — the situation, the audience, the likely objection, and what data exists
2. **Estimate the cost of the current state** — quantify the problem from labelled inputs
3. **Write the pitch** — the five-part template, problem first
4. **Calculate ROI and payback** — one loaded rate, recomputed arithmetic, visible assumptions
5. **Address the likely objections** — the four-step method
6. **Calibrate to the audience** — from the executive-communication note
7. **Choose the investment model** — dedicated, federated or community
8. **Frame the cost of inaction** — only from figures already sourced
9. **Quality checks**

---

## Step 1: Understand the context and gather evidence

Ask for or confirm:
- Is this a pitch for a new design system, or a pitch to continue investing in an existing one?
- What is the current state? (Multiple teams building the same things independently / an existing system with low adoption / no system at all)
- What is the organisation? (Size, product count, team structure)
- Who is the audience for this pitch? (Executive, product leadership, engineering leadership, combined)
- What is the likely objection? (Cost, timeline, team capacity, "we tried this before")
- What data exists? (Time spent on inconsistent work, accessibility incident history, customer complaints about inconsistency, hiring plans, loaded salary rates)

If system-health or adoption-report output exists, use its figures and cite them. Claims about the user's system come from inspected files, prior skill output, or the user — never from what a typical organisation looks like. Anything the pitch needs and nobody can supply stays as `[needs data: …]`.

The "likely objection" is important. A pitch that does not address the elephant in the room leaves the reader thinking about it instead of engaging with the argument.

**Small-system note (fewer than 5 components):** For small teams or products, the pitch faces a different objection: "Why do we need a design system? Can't we just coordinate?" The answer is that coordination without a system is coordination without a contract — it works until someone is on holiday, until a new team member joins, or until the product grows past the point where everyone can hold the conventions in their heads. The ROI framing shifts from "eliminate duplicated effort across 20 teams" to "protect consistency as the team grows, reduce onboarding time for new designers and developers, and make accessibility compliance a default rather than a per-feature effort." If the system already exists at this size, the pitch is usually for continued investment or formalisation — frame the ask around what has already been achieved informally and why it is worth making durable.

---

## Step 2: Estimate the cost of the current state

Before writing the pitch, estimate the cost of the current state. These numbers power the "cost of the current state" section and make the ROI argument concrete. Every line is labelled measured, estimated (with reasoning) or assumed, and every hour is costed at the same loaded hourly rate used for the investment in Step 4.

### Business metrics worksheet

**Loaded hourly rate (assumed, one rate for everything):** ___ — salary plus overheads, divided by working hours a year (2,080 for a 40-hour week)

**1. Duplicated effort:** How many teams are independently building the same UI patterns?
   - Engineers doing duplicated work: ___
   - Estimated weeks per engineer per year on duplicated work: ___
   - Annual cost: ___ engineers × ___ weeks × 40 hours × loaded rate = ___/year

**2. Inconsistency cost:** How many customer-facing inconsistencies exist?
   - Known support tickets related to UI inconsistency: ___
   - Average handling hours per ticket: ___
   - Annual cost: ___ tickets × ___ hours × loaded rate = ___/year
   - Customer trust and churn impact: qualitative unless the user has data

**3. Onboarding cost:** How long does it take a new designer or developer to learn current conventions?
   - Current onboarding time for conventions: ___ weeks
   - Estimated onboarding time with a documented system: ___ weeks
   - Hires per year: ___
   - Annual savings: ___ hires × ___ weeks saved × 40 hours × loaded rate = ___/year

**4. Accessibility risk:** What is the current compliance state?
   - Known accessibility violations (from an audit — cite it): ___
   - Estimated remediation hours if addressed per product: ___
   - Estimated remediation hours if addressed at system level: ___
   - Legal and reputational exposure: qualitative unless the user supplies an estimate

**5. Speed cost:** How much longer do features take without shared components?
   - Estimated additional days per feature: ___
   - Features shipped per quarter: ___
   - Annual cost: ___ days × 8 hours × ___ features × 4 quarters × loaded rate = ___/year

**6. Competitive positioning:** Are competitors shipping faster or with more consistent experiences? Qualitative only, unless the user supplies a sourced comparison.

Not all of these will have hard numbers. Use conservative estimates where data is not available, and state the reasoning. A pitch with honest estimates and visible reasoning is more credible than one with precise numbers and hidden assumptions.

**Total estimated annual cost of current state:** ___ [sum of the quantified lines above, recomputed]

---

## Step 3: Write the pitch using the five-part template

---

### [Title — frames the problem, not the solution]

**Prepared by:** [name]
**Date:** [date]
**For:** [audience]
**Open placeholders:** [list every `[needs data: …]` left in the document, or "none"]

---

#### The cost of the current state

Start with the problem. Do not name the solution in the first section.

Describe what is happening now that is costing time, money, quality, or trust. Use specific examples where available. If data is available, use it and cite it. If estimates must be used, frame them conservatively and show the reasoning.

Common angles that land with business audiences:
- Duplicated effort: "We estimate that [n] engineering teams have each built their own version of [core pattern]. That represents [n] weeks of duplicated work."
- Quality inconsistency: "Customers encounter [n] distinct visual treatments for the same interaction type across our products. This creates confusion and erodes trust."
- Accessibility risk: "Our current approach leaves accessibility compliance to each team individually. [n] of [n] audited flows have accessibility violations." (Cite the audit.)
- Onboarding cost: "New product designers and developers spend [n] weeks building up context about our interface conventions that could be available on day one."
- Speed: "New features take [n] weeks longer to design and build because [reason], based on [internal measurement]." No industry benchmarks unless the user supplies a source.

Pick the 2–3 angles that hit hardest for this audience. A pitch that lists every possible benefit sounds like it is trying too hard.

---

#### What a design system does

One paragraph. No jargon. The clearest possible description of what the investment delivers.

The goal is not to explain what a design system is technically. It is to describe what changes for the business. "A shared library of interface components that every product team uses" is half of it. "So that each team builds faster, more consistently, and without solving the same problems twice" is the other half. Together, one sentence.

---

#### The investment

Be specific about what is being asked for. Avoid vague requests for "resources" or "support."

Frame the investment in terms the audience understands:
- Headcount: "We are asking for 1 FTE dedicated design systems engineer, 0.5 FTE designer"
- Time allocation: "We are asking for [n]% of each product team's engineering capacity for the first two quarters"
- Budget: "We are asking for $[amount] for tooling and [n] weeks of external expertise"
- Timeline: "The initial build is [n] weeks, followed by [n] months of active maintenance, then [n] months of standard operations"

Present the investment as proportional to the problem, with the arithmetic from Step 4 visible: current-state cost per year, investment per year, and the recomputed payback month.

---

#### What success looks like

Be specific and honest. Define success in business terms and set a realistic timeline.

Not: "Teams will be more consistent and efficient."
But: "Within six months, all three web product teams will be building new features from the shared component library. Within twelve months, time-to-first-review for new feature designs will decrease by [estimate] because designers will be composing from existing patterns rather than designing from scratch."

Name what the investment will not solve. "This investment will not resolve our accessibility debt overnight — it will prevent new debt from accumulating and create a path to addressing the existing issues systematically."

Define the metrics by which success will be measured, each with a baseline measured before the build starts:
- Adoption: "[target]% of new feature work built with system components by [date]"
- Speed: "Time from design to code review decreases from [baseline] to [target] weeks"
- Consistency: "Inconsistency-related support tickets decrease from [baseline] to [target] per quarter"
- Onboarding: "Time for a new team member to ship their first feature decreases from [baseline] to [target] weeks"
- Maintenance: "Hours per quarter spent maintaining duplicate components decrease from [baseline] to [target]"

Use one adoption target throughout the pitch; the same figure feeds the benefit ramp in Step 4.

---

#### Addressing the likely objections

One to two paragraphs directly engaging with the most predictable counter-argument, using the method in Step 5. Name the objection explicitly — "The most likely concern is: [state it clearly]" — then respond with data or reasoning.

---

#### The ask

One sentence. What is needed, and by when? Then the specific items. No more than three.

End the pitch with `Based on: [sources, with dates]`.

---

## Step 4: Calculate and present ROI

The pitch should make the ROI calculation transparent and credible. Follow the numbers-honesty rules in the executive-communication note: one loaded hourly rate for costs and benefits, every input labelled, every derived figure recomputed.

**ROI** = (Annual benefit − Annual cost) / Annual cost

**Annual benefit** = the share of the current-state cost the system removes that year (the adoption assumption from the success metrics)

**Annual cost** = the cost of building, operating and maintaining the system

**Payback** = the first month in which cumulative benefit is at least cumulative cost

### Worked example

Every input below is an illustrative assumption. Never carry these numbers into a real pitch; replace them with the user's figures and recompute.

**Loaded hourly rate (assumed):** $75/hour, used for both costs and benefits. One FTE = 2,080 hours × $75 = $156,000/year.

**Cost of current state (annual):**
- Duplicated work: 9 engineers across 3 teams × 15 weeks × 40 hours = 5,400 hours × $75 = $405,000
- Onboarding: 5 hires × 2 weeks saved × 40 hours = 400 hours × $75 = $30,000
- Inconsistency support tickets: 50 tickets × 4 hours = 200 hours × $75 = $15,000
- **Total: 6,000 hours × $75 = $450,000/year**

**Investment (annual, same in year 1 and year 2+):**
- 1 FTE design systems engineer: 2,080 hours × $75 = $156,000
- 0.5 FTE product designer: 1,040 hours × $75 = $78,000
- Tooling and infrastructure (assumed): $20,000
- **Total: $254,000/year**

**Adoption assumption:** 50% of the benefit realised in year 1 (ramp-up), 90% from year 2.

**Year 1:** benefit $450,000 × 50% = $225,000; cost $254,000. ROI = ($225,000 − $254,000) / $254,000 = −11.4%.

**Year 2:** benefit $450,000 × 90% = $405,000; cost $254,000. ROI = ($405,000 − $254,000) / $254,000 = 59.4%.

**Payback:** monthly cost is $254,000 / 12 = $21,167. Monthly benefit is $18,750 in year 1 and $33,750 in year 2. After 12 months the shortfall is $254,000 − $225,000 = $29,000. Year 2 closes it at $33,750 − $21,167 = $12,583 a month: month 14 cumulative benefit $292,500 against cost $296,333; month 15 cumulative benefit $326,250 against cost $317,500. **Payback in month 15.**

### Presenting ROI in the pitch

Include a small table that shows:
- Current annual cost to the organisation
- Investment required
- Payback month
- Annual ROI once adoption reaches the target

Make the assumptions visible: "These calculations assume [year 1]% of the benefit in year 1 and [target]% from year 2, at a loaded rate of [rate]. If adoption is slower, payback moves out; if faster, ROI improves." The adoption figures here are the same ones stated in the success metrics.

### Conservative case

For sceptical audiences, rerun the calculation with lower adoption, a longer ramp, and hard benefits only (time savings, support cost), and show both cases side by side. If the conservative case does not pay back within a period the audience cares about, say so and narrow the ask — a smaller first phase with a shorter payback. Never fill a figure without a source; leave `[needs data]`.

### Soft benefits

These are real but hard to quantify. Mention them only after the hard ROI is established, and never put a number on them without data:
- Improved developer satisfaction
- Reduced decision fatigue (teams do not have to reinvent patterns)
- Improved hiring and retention
- Improved customer perception of polish
- Faster response to design trends

---

## Step 5: Address the likely objections

A pitch that does not address the elephant in the room leaves the reader thinking about it instead of engaging with the argument. For each objection that fits this context:

1. Name it explicitly (do not dance around it)
2. Acknowledge the concern is valid
3. Respond with data or reasoning that addresses the core concern
4. Offer a concrete path to resolution

Common objections and where the response starts:

- **"We tried this before and it didn't stick."** Name the previous failure mode and the specific change that answers it: built by one team (co-design with consuming teams), abandoned after launch (committed ongoing maintenance), too rigid (extension points without forking), unclear governance (contribution and deprecation documented before launch). Don't overpromise what has changed.
- **"We don't have the capacity right now."** The current state is not free; it is paid in duplicated work. Put the two annual costs from Step 4 side by side. For cash-constrained organisations, offer a smaller first phase with its own payback. For capacity-constrained ones, show the capacity allocation next to the duplicated effort it replaces, and claim it nets out only if the figures show it.
- **"This will slow teams down while they learn it."** Acknowledge the dip and offer pairing with the first team. Give a ramp timeline only from the organisation's own data (a previous pilot, the first team's experience), or label it as an assumption.
- **"A component library isn't a design system — this is over-complicated."** The library is the code; the system is the library plus standards, contribution process, support and metrics. List what is being built, so the reader sees the parts that make teams trust it.
- **"This will constrain innovation."** The system is a floor, not a ceiling: standard problems are solved once, teams innovate on top, and proven local experiments are promoted into the system.
- **"It'll be out of date immediately."** Core patterns change slowly; the system evolves through a stated release cadence ([cadence]) and a proposal route, based on evidence rather than fashion.
- **"How will we know it works?"** Point to the success metrics, commit to measuring baselines before the build, name the reporting cadence, and say what happens if a metric moves the wrong way (fix the system, or add support).

---

## Step 6: Calibrate the pitch to the audience

Use the audience calibration table and framing patterns in the executive-communication note: what each audience cares about, what to lead with, the language that lands, and what to avoid. Check the draft against the anti-patterns in the same note before delivering it.

---

## Step 7: Investment models — how to structure the ask

The pitch should specify not just how much investment, but what model of investment you are proposing.

### Model 1: Dedicated team

**Structure:** Create a dedicated design systems team that owns the system. Product teams contribute, but the design systems team is responsible for maintenance and governance.

**Pros:**
- Clear ownership and accountability
- Dedicated focus on system quality
- Predictable evolution

**Cons:**
- Highest headcount cost
- Design systems team can become a bottleneck
- May not reflect product team needs closely

**Investment:** 1–3 FTE depending on organisation size

**Frame in pitch:** "Dedicated ownership ensures the system evolves intentionally and maintains quality standards. The design systems team works closely with product teams to ensure the system serves real needs."

### Model 2: Federated model

**Structure:** Design systems work is distributed across product teams, coordinated by a lightweight governance process. Each product team contributes components and maintains them.

**Pros:**
- Distributed ownership (no bottleneck)
- Components stay close to the teams that use them
- Lower headcount cost

**Cons:**
- Requires discipline to maintain consistency
- Governance overhead to prevent divergence
- Harder to enforce standards

**Investment:** 0.5 FTE coordinator + time allocation from each product team

**Frame in pitch:** "Distributed ownership keeps the system close to product needs and eliminates bottlenecks. Governance processes ensure consistency even though ownership is distributed."

### Model 3: Community model

**Structure:** The system exists as an open platform that any team can contribute to, but there is no dedicated team. Maintenance is volunteer or part of product work.

**Pros:**
- Lowest headcount cost
- System evolves based on real team needs
- High autonomy for teams

**Cons:**
- System may stagnate (no dedicated maintainer)
- Quality is inconsistent
- Contributions happen sporadically

**Investment:** Minimal (just a lightweight coordinator role, maybe 0.2 FTE)

**Frame in pitch:** "This is a community-driven system where teams contribute and share. Success depends on teams seeing clear value and choosing to contribute."

### Model comparison table for pitch

| Model | Headcount | Governance overhead | Quality consistency | Scalability | Risk |
|---|---|---|---|---|---|
| Dedicated | High | Low | High | High | Bottleneck if team is understaffed |
| Federated | Medium | Medium | Medium | Medium | Requires strong governance |
| Community | Low | High | Low | Low | May stagnate without contributions |

**In the pitch, state which model you recommend and why:** "For an organisation of our size [n teams, n products], the [model] approach is appropriate because [reason]. As we grow to [n] teams, we will likely transition to [new model]."

---

## Step 8: Risk framing — the cost of inaction

Not investing in a design system has costs. Make them explicit, using only figures already sourced in Step 2; anything not quantified there stays qualitative or `[needs data: …]`.

**If we do nothing:**

1. **Duplicated work compounds.** The engineering hours spent on duplicated components this year recur next year: over 18 months, that is 1.5 × the annual duplicated-effort figure from Step 2.
2. **Inconsistency accumulates.** Every new product launches with its own interface patterns, and customer experience fragments further.
3. **Technical debt grows.** As products diverge, the effort required to unify them later grows.
4. **Onboarding friction persists.** New teams and team members keep learning conventions that could be documented once.
5. **Accessibility risk compounds.** Without a system-level approach, fixes found in one team do not propagate to the others.
6. **Competitive positioning weakens.** Qualitative unless the user supplies a sourced comparison.

**Comparison:** "The investment costs [amount] over 18 months. Doing nothing costs [amount from Step 2 × 1.5] over the same period." Recompute both figures from the same inputs as Step 4.

---

## Step 9: Quality checks

Before delivering the pitch, verify all of these:

- The pitch leads with the business problem, not the design system solution
- Every figure about the user's system traces to a named source (file, tool output, prior skill output, or the user) and is labelled measured, estimated or assumed
- One loaded hourly rate is used for both costs and benefits, and it is stated as an assumption
- Every derived figure (totals, ROI, payback, FTE equivalents) has been recomputed from the inputs shown; payback is the month cumulative benefit reaches cumulative cost
- The adoption assumption is the same in the success metrics and the ROI ramp
- No industry benchmark appears without a source the user supplied
- If the conservative case does not pay back, the pitch says so and the ask is narrowed
- Open placeholders are listed at the top; the pitch ends with a `Based on:` line
- Investment ask is specific: headcount, time, or budget — not vague "resources"
- Success definition is in business terms with a timeline and measured baselines
- The likely objection is directly addressed, not avoided
- No design system jargon that is unexplained
- The pitch is honest about what the investment will not solve
- The ask is three items or fewer and is stated in one sentence before the detail
- Investment model (dedicated/federated/community) is named and justified
- Pitch is calibrated to the audience, and none of the anti-patterns in the executive-communication note are present
- The pitch is honest about dependencies (e.g., team buy-in, governance processes) that are required for success
