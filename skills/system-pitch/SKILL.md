---
name: system-pitch
description: "Write a design system investment pitch with a business case and ROI framing. Trigger when someone says: pitch the design system, make the case for the system, sell this to leadership, justify the investment, business case for design systems, why should we invest in a design system, or anything about building an argument for design system investment or continuation."
---


# System pitch

A skill for writing a design system investment pitch that leads with a business problem, builds an honest ROI case, and addresses likely objections. Output is a pitch document that works for an audience who has never heard of a design system and does not need to.

## Context

Design system pitches usually fail for one of two reasons. They lead with the design system — its components, its tokens, its Storybook — rather than with the business problem it solves. Or they oversell: promising a design system will solve problems it cannot solve, which creates scepticism or, worse, expectation debt that damages credibility when the system ships and the promised outcomes do not materialise.

The pitch that works leads with the cost of the current state. It makes the reader feel the friction of inconsistency, the waste of duplicated effort, the risk of inaccessible interfaces — before it introduces the design system as the solution. Then it is specific about what the investment costs, honest about the timeline, and precise about what success looks like.

## Workflow overview

The system pitch workflow follows seven distinct steps:

1. **Understand the context** — Assess the situation and likely objections
2. **Estimate the cost of the current state** — Quantify the problem
3. **Structure and write the pitch** — Build the five-part template with business framing
4. **Calculate and present ROI** — Show the financial return
5. **Address likely objections** — Preempt the 5–7 most common objections
6. **Frame by audience** — Calibrate the pitch for different stakeholders
7. **Review for clarity and quality** — Ensure the pitch leads with problem, not solution

---

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

---

## Step 2: Estimate the cost of the current state

Before writing the pitch, estimate the cost of the current state. These numbers power the "cost of the current state" section and make the ROI argument concrete.

### Business metrics worksheet

Use this worksheet to gather the data you will need:

**1. Duplicated effort:** How many teams are independently building the same UI patterns?
   - Teams: ___
   - Estimated hours per team per quarter on duplicated work: ___
   - Estimated cost: ___ teams × ___ hours × hourly rate = ___/quarter
   - Annual cost: ___ × 4 quarters = ___/year

**2. Inconsistency cost:** How many customer-facing inconsistencies exist?
   - Known support tickets related to UI inconsistency: ___
   - Estimated support cost per ticket: ___
   - Estimated customer churn impact from inconsistency: [qualitative or quantitative]
   - Customer trust/brand impact: [qualitative assessment]

**3. Onboarding cost:** How long does it take a new designer/developer to learn current conventions?
   - Current onboarding time for conventions: ___ days
   - Estimated onboarding time with a documented system: ___ days
   - Savings per new hire: ___ days × daily rate = ___
   - Hires per year: ___
   - Annual savings: ___ × ___ = ___/year

**4. Accessibility risk:** What is the current compliance state?
   - Known accessibility violations: ___
   - Estimated remediation cost if addressed per-product: ___
   - Estimated remediation cost if addressed at system level: ___
   - Potential legal/reputational cost of continued non-compliance: [estimate]

**5. Speed cost:** How much longer do features take without shared components?
   - Estimated additional time per feature: ___ days
   - Features shipped per quarter: ___
   - Total additional cost: ___ days × ___ features × daily rate = ___/quarter
   - Annual cost: ___ × 4 quarters = ___/year

**6. Competitive positioning:** Are competitors shipping faster or with more consistent experiences?
   - Time-to-market comparison: [our product vs. competitor]
   - Estimated impact on market position: [qualitative]

Not all of these will have hard numbers. Use conservative estimates where data is not available, and state the assumptions. A pitch with honest estimates and visible reasoning is more credible than one with precise numbers and hidden assumptions.

**Total estimated annual cost of current state:** ___ [sum of quantified costs above]

---

## Step 3: Structure and write the pitch using the five-part template

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

Use the best angle for the audience and the context. Avoid using all of them — a pitch that lists every possible benefit sounds like it is trying too hard. Pick 2–3 that hit hardest.

---

#### What a design system does

One paragraph. No jargon. The clearest possible description of what the investment delivers.

The goal is not to explain what a design system is technically. It is to describe what changes for the business. "A shared library of interface components that every product team uses" is half of it. "So that each team builds faster, more consistently, and without solving the same problems twice" is the other half. Together, one sentence.

Do not lead with tooling. Bad: "We will implement a Figma-based design system with Storybook documentation and a component library built in React." Good: "Every team will build from a shared set of proven interface components, eliminating the need to recreate standard patterns and ensuring all customers have a consistent experience."

---

#### The investment

Be specific about what is being asked for. Avoid vague requests for "resources" or "support."

Frame the investment in terms the audience understands:
- Headcount (if asking for team members): "We are asking for 1 FTE dedicated design systems engineer, 0.5 FTE designer"
- Time allocation (if asking for engineers to contribute): "We are asking for 20% of each product team's engineering capacity for the first two quarters"
- Budget (if tooling or external support is involved): "We are asking for $[amount] for tooling and [n] weeks of external expertise"
- Timeline (what the investment looks like over time): "The initial build is [n] weeks, followed by [n] months of active maintenance, then [n] months of standard operations"

Present the investment as proportional to the problem. If the cost-of-current-state section identified [n] weeks of duplicated effort per year, and the investment is [n] weeks of initial build effort, the arithmetic should be visible: "The cost of maintaining the current state is [n] weeks per year. The initial investment is [n] weeks. This pays for itself within [timeline]."

---

#### What success looks like

Be specific and honest. Define success in business terms and set a realistic timeline.

Not: "Teams will be more consistent and efficient."
But: "Within six months, all three web product teams will be building new features from the shared component library. Within twelve months, time-to-first-review for new feature designs will decrease by [estimate] because designers will be composing from existing patterns rather than designing from scratch."

Name what the investment will not solve. Pitches that leave this implicit invite disappointment. "This investment will not resolve our accessibility debt overnight — it will prevent new debt from accumulating and create a path to addressing the existing issues systematically."

Define the metrics by which success will be measured:
- Adoption rate: "80%+ of new components used within 3 months of release"
- Speed gain: "Time-to-design decreases from [n] weeks to [n] weeks"
- Consistency: "Visual inconsistency support tickets decrease by [n]%"
- Onboarding: "New team member time-to-productivity decreases from [n] weeks to [n] weeks"

---

#### Addressing the likely objections

One to two paragraphs directly engaging with the most predictable counter-argument. See Step 5 below for the full objection-handling framework.

Name the objection explicitly. "The most likely concern is: [state it clearly]." Then respond directly with an honest answer grounded in data or reasoning.

---

#### The ask

One sentence. What is needed, and by when?

Then the specific items. No more than three.

---

## Step 4: Calculate and present ROI

ROI is the return on investment expressed as a ratio or percentage. The pitch should make the ROI calculation transparent and credible.

### ROI calculation framework

**Formula:** (Annual benefit - Annual cost) / Annual cost = ROI %

**Annual benefit** = Cost of current state that the design system will eliminate or reduce

**Annual cost** = Cost of operating and maintaining the design system

### ROI calculation example

**Cost of current state (annual):**
- Duplicated work across 3 teams: 12 weeks/year × 5 engineers × $150/hour = $360,000/year
- Onboarding time for new hires: 5 new hires/year × 2 weeks saved × $150/hour × 40 hours = $60,000/year
- Support tickets from inconsistency: 50 tickets/year × 4 hours avg × $150/hour = $30,000/year
- **Total annual cost of current state: $450,000/year**

**Investment cost (annual, year 1):**
- 1 FTE design systems engineer: $150,000
- 0.5 FTE product designer: $75,000
- Tooling and infrastructure: $20,000
- **Total first-year investment: $245,000**

**Ongoing cost (year 2+):**
- 1 FTE design systems engineer: $150,000
- 0.5 FTE product designer: $75,000
- Tooling and infrastructure: $20,000
- **Total ongoing annual cost: $245,000**

**ROI calculation (year 1):**
- Benefit realized in year 1: assume 50% of potential (ramp-up period): $225,000
- Cost: $245,000
- ROI: ($225,000 - $245,000) / $245,000 = -8.2% (breaks even in month 10)

**ROI calculation (year 2+):**
- Benefit realized: $450,000 (full realization once system is mature)
- Cost: $245,000
- ROI: ($450,000 - $245,000) / $245,000 = **83.7% return annually**

**Payback period:** 10 months

### Presenting ROI in the pitch

Include a small table or visual that shows:
- Current annual cost to the organisation
- Investment required
- Timeline to payback
- Annual ROI once mature

Make the assumptions visible: "These calculations assume 50% adoption in year 1 and 90% adoption by year 2. If adoption is slower, payback extends. If adoption is faster, ROI improves."

### Conservative ROI framing

For skeptical audiences, present a conservative scenario:
- Lower adoption estimates (60% instead of 80%)
- Longer timeline (18 months to full benefit instead of 12)
- Exclude soft benefits (like improved developer morale)
- Include only quantifiable hard benefits (time savings, reduced support cost)

Even the conservative case should show positive ROI within 12–18 months.

### Soft benefits to exclude (or footnote)

These are real benefits but harder to quantify. Do not lead with them; mention them only after the hard ROI is established:
- Improved developer satisfaction
- Reduced decision fatigue (teams do not have to reinvent patterns)
- Improved hiring/retention (standard patterns attract quality engineers)
- Improved customer perception of polish
- Faster response to design trends

---

## Step 5: Address the likely objections — framework for 5–7 common objections

A pitch that does not address the elephant in the room leaves the reader thinking about it instead of engaging with the argument. Anticipate the most likely objections for your context and address them directly.

### Framework for objection handling

For each objection:
1. Name it explicitly (do not dance around it)
2. Acknowledge the concern is valid
3. Respond with either data or reasoning that addresses the core concern
4. Offer a concrete path to resolution

---

### Objection 1: "We tried this before and it didn't stick."

**Why this objection comes up:** Past failures create skepticism. The audience assumes this pitch will end the same way.

**How to respond:**

Acknowledge it directly. "You are right — the previous attempt [describe what happened] for specific reasons. This proposal differs in [specific ways that address the previous failure mode]."

**Common failure modes and how to address them:**

- *"The system was designed by one team and teams didn't use it"* → "This pitch includes [n] teams as co-designers from the start. Ownership is distributed, not centralized."
- *"The system was abandoned after the initial build"* → "We are committing [ongoing FTE] to maintenance and evolution, not treating this as a one-time project."
- *"Teams found it too rigid for their needs"* → "We are building the system to [n] levels of customization, allowing teams to extend without forking."
- *"Governance was unclear, so teams ignored it"* → "We are documenting clear contribution and deprecation processes before launch, not figuring them out as we go."

Do not dismiss the concern. Do not over-promise about what has changed. Be specific about what you learned and how this attempt will be different.

---

### Objection 2: "We don't have the capacity right now."

**Why this objection comes up:** The organisation feels stretched. Any new initiative feels like a burden.

**How to respond:**

"The question is not whether we have capacity to build a design system. It is whether we can afford to keep paying the cost of not having one. The current approach is not free — it is just paying in a different currency."

Then show the math: "We are currently paying [cost] in duplicated effort every year. The design system investment is [cost] per year. The difference is [savings] in year 2+. We can choose to pay in duplicated work or in infrastructure investment — but we are paying either way."

**For cash-constrained organisations:** "We can phase this. Start with [small scope] that pays for itself within [n] months, then expand. The first phase requires [smaller investment] and delivers [immediate benefit]."

**For capacity-constrained organisations:** "This does not require hiring. It requires [n] teams allocating [n]% capacity to system work. In return, they will save [n]% on duplicated work — net zero new capacity required."

---

### Objection 3: "This will slow teams down while they learn the system."

**Why this objection comes up:** Onboarding friction is real. Teams worry about short-term disruption to shipping.

**How to respond:**

"There is a short onboarding period. Based on comparable implementations, teams typically reach parity within [n] sprints and operate faster than pre-system pace within [n] quarter(s)."

Provide a timeline:
- Weeks 1–2: Learning the system, building first component with design systems team paired
- Weeks 3–6: Teams building new features at 80% pre-system speed (slower, but learning)
- Weeks 7–12: Teams building at 100% pre-system speed (caught up on learning)
- Month 4+: Teams building faster than pre-system pace (benefit from composition)

For product teams worried about shipping: "We will pair with the first team for [n] weeks to get them productive. Subsequent teams will onboard faster because they learn from that team's experience."

---

### Objection 4: "A component library is not the same as a design system. This feels over-complicated."

**Why this objection comes up:** Confusion between "component library" (a code artifact) and "design system" (a shared approach to design and engineering). Some teams think they can just publish components and call it done.

**How to respond:**

"You are right that there is a difference. A component library is just the code. A design system is the library plus the standards, governance, and support that make teams *want* to use it and keep using it. The code without the system is a repository nobody trusts."

"Here is what we are building:
- [n] shared components (that is the library)
- Standards for how we build ([design and API contract](link))
- A documented process for contributing and changing ([governance](link))
- Support for teams using the system ([office hours, documentation](link))
- Metrics so we know whether it is working ([adoption tracking, health metrics](link))

The components are just the visible part. The system is everything that makes the components valuable instead of just available."

---

### Objection 5: "This will constrain innovation. Teams need freedom to experiment."

**Why this objection comes up:** Some teams (especially product or design) fear that standardization will force conformity and kill good ideas.

**How to respond:**

"The system is not a constraint on innovation. It is a floor, not a ceiling. Teams can innovate on top of the system once they have solved the standard problems consistently."

"Here is the difference:
- **Without a system:** Every team solves every problem independently. Most of this effort is duplicated. Innovation gets buried in the noise.
- **With a system:** Every team solves standard problems the same way (once, at the system level). Teams are free to innovate on top of the system, knowing their innovations will compose with standard components and will not introduce inconsistency.

The pattern: core components are standardized. Advanced components (that push the design forward) can be added to the system or can be local experiments. Once a local experiment proves valuable, it becomes a system component."

---

### Objection 6: "The system will be out of date immediately. Design trends move fast."

**Why this objection comes up:** Design and product move quickly. Some stakeholders worry the system will become a ball and chain instead of an accelerant.

**How to respond:**

"A design system is not supposed to be the cutting edge. It is supposed to be the stable foundation that teams build on top of. Design trends do move fast — which is exactly why we need a system. Trends change, but core patterns (buttons, inputs, navigation, cards) stay relatively stable. The system locks in the foundation so teams can focus their innovation energy on what actually changes."

"We are building a [release cadence] for evolving the system. Minor updates (new variants, tokens) ship every [period]. Major updates (new patterns, architecture changes) ship every [period]. Design teams can propose new patterns at any time. Proven patterns get added to the system. Experimental patterns stay local until they prove themselves."

For more design-focused audiences: "The system is a living artifact, not a museum piece. Teams can propose changes. The bar for change is: 'Does this new direction serve teams better than the old one?' not 'Is this trendy?' We evolve the system based on evidence, not fashion."

---

### Objection 7: "Measuring success here is hard. How will we know if this works?"

**Why this objection comes up:** Executives want to be able to measure whether an investment paid off. Design system benefits can seem soft or hard to quantify.

**How to respond:**

"You are right that some benefits are hard to measure. But the main ones are not. We will track:

1. **Adoption rate:** Percentage of new components using system patterns. Target: 80%+ within 12 months.
2. **Speed:** Time from design to code review for new features. Target: [baseline] to [target] weeks.
3. **Support cost:** Support tickets from inconsistency or misuse. Target: [baseline] to [target] reduction.
4. **Onboarding time:** Time for new team members to ship their first feature. Target: [baseline] to [target] weeks.
5. **Maintenance cost:** Engineering hours per quarter spent on component maintenance (single source vs. distributed). Target: [baseline] to [target] reduction.

We will report on these metrics [quarterly/monthly]. If a metric is trending the wrong way, we will adjust — either the system is not serving teams (fix the system) or teams need better support (add training or documentation)."

Offer to establish baseline metrics early: "Before we build, let's measure where we are today on these metrics. Then in 12 months, we measure again and compare."

---

## Step 6: Calibrate the pitch by audience

Different audiences care about different things. Adjust the pitch's framing based on who is reading.

### For Engineering Leadership

**What they care about:** Technical debt, velocity, reliability, maintenance burden, engineering productivity.

**Pitch emphasis:**
- Lead with duplicated work (efficiency waste): "We estimate [n] engineering weeks per quarter spent on duplicate component implementations."
- Frame as platform infrastructure: "This is not a design initiative — it is shared platform infrastructure."
- Quantify the velocity gain: "Teams using shared components ship [n]% faster than teams building independently."
- Address technical sustainability: "Local implementations create technical debt that compounds over time. The system eliminates this debt."

**Language to use:**
- "Platform infrastructure"
- "Engineering velocity"
- "Technical debt"
- "Maintenance burden"
- "System reliability"

**Language to avoid:**
- Design-specific jargon ("design tokens," "design language")
- Aesthetic arguments without engineering translation
- Abstract efficiency claims without numbers

### For Product Leadership

**What they care about:** Customer experience, time-to-market, competitive positioning, feature velocity.

**Pitch emphasis:**
- Lead with inconsistent customer experience: "Customers encounter [n] different interface patterns for the same interaction."
- Frame as enabling speed: "Teams building from shared components ship features [n]% faster."
- Quantify feature velocity: "Without duplicated component work, we can ship [n] additional features per quarter."
- Connect to competitive positioning: "Consistency and speed are competitive differentiators. The system enables both."

**Language to use:**
- "Customer experience"
- "Feature velocity"
- "Time-to-market"
- "Competitive positioning"
- "Customer trust"

**Language to avoid:**
- Technical implementation details
- Code-level specifics
- Governance processes (except as they enable faster shipping)

### For Design Leadership

**What they care about:** Design quality, design consistency, design scalability, design standards.

**Pitch emphasis:**
- Lead with design inconsistency: "We currently have [n] different approaches to [core pattern] across products."
- Frame as design leverage: "A well-maintained system frees design teams to focus on novel problems instead of recreating standard patterns."
- Quantify design impact: "Designers spend [n]% of their time on pattern work that could be handled by the system."
- Reference design standards: "The system is the mechanism for enforcing [n] core design standards across the organisation."

**Language to use:**
- "Design consistency"
- "Design quality"
- "Design scalability"
- "Design standards"
- "Design leverage"

**Language to avoid:**
- Engineering-only metrics
- Implementation details (what matters is the design, not the code)
- Process-heavy governance language

### For Executive/C-level

**What they care about:** Strategic alignment, risk mitigation, financial return, organisational efficiency, competitive positioning.

**Pitch emphasis:**
- Lead with strategic alignment: "This system is foundational to [strategic goal — scaling to n products, becoming faster to market, entering new markets]."
- Quantify financial impact: "Annual cost of the current state is [amount]. Investment is [amount]. Payback is [timeline]."
- Frame as infrastructure: "This is infrastructure investment, not a design initiative."
- Address risk: "The current approach creates [specific risk] that undermines [strategic priority]."

**Language to use:**
- "Strategic alignment"
- "Return on investment"
- "Operational efficiency"
- "Risk mitigation"
- "Platform infrastructure"
- "Competitive positioning"
- "Scalability"

**Language to avoid:**
- Design and engineering jargon equally
- Assume any prior knowledge of design systems
- Implementation details
- Process-heavy governance language

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

Not investing in a design system has costs. Make them explicit.

### Cost of inaction over 18 months

**If we do nothing:**

1. **Duplicated work compounds.** The engineering hours spent on duplicated components this year become next year's problem too. In 18 months, that is [n] additional engineering weeks of wasted effort.

2. **Inconsistency accumulates.** Every new product launches with its own interface patterns. Customer experience fragments further. Support tickets from inconsistency increase by [estimated %].

3. **Technical debt grows.** As products diverge, the effort required to unify them later grows exponentially. A system that would cost [investment] now will cost [higher cost] in 18 months.

4. **Onboarding friction persists.** New teams and new team members spend [n] weeks learning conventions that could be documented once instead of learned repeatedly.

5. **Accessibility risk compounds.** Without a system-level approach, accessibility improvements happen team-by-team. Gaps discovered in one team do not automatically propagate fixes to other teams.

6. **Competitive positioning weakens.** Competitors with consistent, fast-shipping products gain market advantage. We become slower and less consistent.

**Financial cost of inaction (18-month view):**
- Duplicated work: [amount]
- Support cost from inconsistency: [amount]
- Engineering velocity loss vs. competitors: [estimated impact]
- **Total cost of inaction: [amount]**

**Comparison:** "The design system investment costs [amount]. The cost of doing nothing over 18 months is [larger amount]. The system pays for itself in [timeline] and delivers [amount] in value over 18 months."

---

## Step 9: Common anti-patterns in pitching

Avoid these mistakes — they destroy credibility:

### Anti-pattern 1: Leading with tooling instead of business outcomes

**The mistake:** "We will implement Figma as our design source of truth with Storybook for documentation and a React component library with TypeScript."

**Why it fails:** Nobody cares about the tools. They care about what changes for the business.

**The fix:** Lead with the outcome, mention the tools in passing if relevant. "Every team will build from a library of proven components, shipping features [n]% faster. We will use React, TypeScript, and Figma to implement this."

### Anti-pattern 2: Asking for too much too soon

**The mistake:** "We need 2 FTE design systems engineers, 1 FTE product designer, a design tool license upgrade, a component library rebuild, a Storybook instance, API versioning, an adoption tracking tool, and a governance process."

**Why it fails:** The ask is so large it feels unmovable. Readers think, "This will never ship."

**The fix:** Phase the ask. "Phase 1 (3 months): Build [core components] with [n] FTE. Phase 2 (3 months): Expand to [n] teams. Phase 3 (ongoing): Maintenance and evolution."

### Anti-pattern 3: Presenting a component library as a design system

**The mistake:** "We are shipping a library of [n] components in a Storybook. Teams can use it."

**Why it fails:** A library without governance, documentation standards, or adoption support is just a code artifact. Teams will not use it.

**The fix:** Frame the library as one part of the system. "The component library is the visible part. Behind it is [governance process], [documentation standards], [support], and [metrics]. Together, these make teams want to use the system."

### Anti-pattern 4: Overpromising on outcomes

**The mistake:** "This investment will eliminate all design inconsistency, reduce engineering time by 50%, and double feature shipping velocity."

**Why it fails:** When you ship and the promised outcomes do not fully materialise (they rarely do), you lose credibility permanently.

**The fix:** Be honest and specific. "This investment will eliminate duplicated component work, reducing engineering time by [n]% on component-related work. It will not eliminate legacy inconsistency — that is a separate effort. It will prevent new inconsistency from accumulating."

### Anti-pattern 5: Ignoring the "we tried this before" objection

**The mistake:** Pretending the previous failed attempt did not happen.

**Why it fails:** Readers remember. You look either uninformed or dishonest.

**The fix:** Acknowledge it, learn from it, explain how this time is different.

### Anti-pattern 6: Mixing the investment ask with the vision

**The mistake:** Asking for funding for year 1, year 2, and year 3 in the same pitch, with different scope and cost each year.

**Why it fails:** Readers get confused about what you are actually asking for. They approve something different from what you meant.

**The fix:** Ask for what you need for the first phase only. Once that phase is complete and delivering value, ask for the next phase.

---

## Step 10: Quality checks

Before delivering the pitch, verify all of these:

- The pitch leads with the business problem, not the design system solution
- Cost-of-current-state section uses specific examples or conservative estimates with visible reasoning
- Investment ask is specific: headcount, time, or budget — not vague "resources"
- Success definition is in business terms with a timeline
- The likely objection is directly addressed, not avoided
- No design system jargon that is unexplained
- The pitch is honest about what the investment will not solve
- The ask is three items or fewer and is stated in one sentence before the detail
- ROI calculation is transparent (benefits and costs are both stated)
- Payback timeline is clear
- Investment model (dedicated/federated/community) is named and justified
- Cost of inaction is quantified
- Pitch is calibrated to the audience (language, emphasis, framing match)
- No anti-patterns from Step 9 are present
- The pitch is honest about dependencies (e.g., team buy-in, governance processes) that are required for success

---

## Configuration for recurring pitches

If this skill runs as part of a recurring workflow (e.g., annual budget planning), configure it as follows:

```yaml
skills:
  system-pitch:
    trigger: "annual-budget-planning"     # or "on-demand"
    audience: "executive"                  # or "engineering-leadership", "product-leadership"
    investment_model: "dedicated"          # or "federated", "community"
    phase: 1                               # phase of the system
    refresh_metrics: true                  # re-run system health before pitching
```

---

## Summary: From pitch to funding decision

A pitch is only valuable if it leads to a funding decision. The pitch should:

1. Be sent to the budget owner or decision-maker (not their staff) directly
2. State when a funding decision is needed
3. Offer a follow-up conversation if there are questions
4. Arrive 2–3 weeks before the budget deadline (enough time for questions)

If the pitch does not result in a decision after 2 weeks, follow up: "I wanted to check whether you have questions about the pitch or whether we need to adjust the proposal."

If the decision is no: ask why. Often the objection is not about the investment itself, but about something else (timing, competing priority, lack of product buy-in). Understanding the real objection lets you address it.

If the decision is yes: confirm the investment model, the timeline, and the success metrics. Announce the decision to the organisation. Set up the first phase kickoff.
