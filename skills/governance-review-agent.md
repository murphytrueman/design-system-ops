---
name: governance-review
description: "Chains adoption-report, drift detection scoped to at-risk teams, and stakeholder-brief into a periodic governance package: an internal assessment linking adoption to drift causes, plus a ready-to-review leadership brief. Invoked by /governance-review."
---

# Governance review

A chained workflow for periodic design system governance reviews. Combines adoption analysis, focused drift detection, and stakeholder communication into a complete package: an honest internal assessment and a ready-to-send external brief. Designed to run quarterly, but useful at any natural review point.

**Output type:** Proposal and communication package. This agent produces analysis and pre-drafted communications. Nothing is sent or published automatically. All outputs require human review.

**Provenance:** The package ends with a one-line provenance footer.

**Run rules:** Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — loading, one inventory, hand-off cards, one report, skipped-permission steps, configuration, and recurring runs. This file holds only what is specific to the governance chain.

---

## When to run this

- Quarterly governance reviews
- Before a budget or headcount conversation where the system's performance needs to be evidenced
- When adoption is declining and you need to understand why before deciding what to do
- When a team or product lead asks "how's the design system doing?"
- Before a design systems retrospective

The governance review is deliberately outward-facing as well as inward. The `full-system-diagnostic` agent answers "what is wrong with the system." The governance review answers "how is the system performing for the teams who use it, and how do we communicate that."

**Small-system note (fewer than 5 components):** For systems this size, a quarterly governance review is almost certainly too frequent — the system does not change fast enough to warrant it. Run semi-annually or annually, or trigger ad hoc when something significant changes (a new component is added, a team is onboarded, or adoption stalls). The Phase 1 adoption report simplifies: with one or two consuming teams, adoption is a conversation, not a metrics exercise. Ask the teams directly how the system is serving them. Drift detection at this scale is a per-component walkthrough rather than a sampling exercise. The stakeholder brief may not be needed at all — if the stakeholder is the same person as the system maintainer, skip Phase 2 and produce only the internal assessment. If a brief is needed, see the stakeholder-brief small-system note for framing guidance.

---

## Configuration and integrations

Configuration and integrations follow the chained-run rules. Specific to this chain: adoption-report uses npm and Figma integrations, drift-detection uses GitHub and Chromatic, and stakeholder-brief uses none (it is a writing skill). If configured, much of the list below auto-resolves. Figma library analytics need the Figma tools to be permitted; if they aren't, record the skip in Scope.

## What you need before starting

- The previous governance report or adoption report, if one exists (auto-loaded from `recurring.output_directory` if configured)
- Access to adoption signals: library usage data, engineering consumption stats, or survey data (auto-pulled from npm/Figma if configured)
- Access to a sample of consuming team work (for drift detection)
- The reporting period (typically the previous quarter)
- Any known changes since the last review: new teams onboarded, components released, changes made
- The system's maturity stage (Ad-hoc / Managed / Systematic / Measured / Optimised), from a system-health report if one exists (there is no config key for it). If none exists, ask the user, and label the stage as reported

---

## Phase 1: Assess

### Step 1 — Adoption report (`adoption-report`)

Run the full adoption report for the reporting period. The adoption-report skill handles calibrating adoption figures against the maturity stage; pass it the stage from the list above. Capture:
- Coverage vs. adoption split
- Design vs. engineering adoption split
- Trend direction vs. last period
- At-risk teams
- Adoption blockers by category

This is the quantitative core of the governance review. If no team has a measured signal, adoption-report stops with a data-collection plan; this review then stops too, with that plan as its output, rather than writing a brief on estimates.

### Step 2 — Drift detection (`drift-detection`)

Run drift detection, scoped specifically to:
- At-risk teams identified in Step 1
- Areas where adoption appears low
- Any product areas that have shipped without using the system

The focus here is different from the full-system-diagnostic's drift detection, which assesses the whole system. Here the focus is: what does drift tell us about *why* adoption is low, and which classifications dominate?

Cross-reference with the adoption report:
- If Classification E (system gap) dominates: the system is failing the teams, not the other way around. Low adoption has a structural cause.
- If Classification C (accidental drift) dominates: awareness and documentation are the issue. Teams are not deliberately going off-system.
- If Classification A (intentional divergence) with no decision records dominates: governance process is not being followed. The contribution workflow is either too heavy or not well understood.
- If Classification B (version lag) dominates: the migration burden is too high, or the benefits of updating are not clear.

This cross-reference — adoption data + drift classification — is the diagnostic insight that neither skill produces alone.

### Step 3 — Synthesise the internal assessment

Before producing any external-facing outputs, synthesise what the two skills have found into an honest internal assessment:

**Adoption picture:** Growing / stable / declining / mixed. What is driving the direction?

**Primary blocker:** From the adoption report's blocker categories and the drift classification pattern, what is the single most important thing limiting adoption?

**At-risk teams:** Who needs attention, and why?

**System gaps identified:** What does the drift evidence show the system needs that it does not have?

**What is working:** Governance reviews that only surface problems are not useful. Note what is working well — teams with strong adoption, patterns with high usage, recent releases that are being picked up quickly.

**Stop here.** Present the internal assessment and continue to the brief only once the user confirms it. The brief goes outward; the framing decisions in Step 4 are the user's to make on the evidence, not the agent's.

---

## Phase 2: Communicate

### Step 4 — Stakeholder brief (`stakeholder-brief`)

Brief purpose: status update with a recommendation.

Use the internal assessment to frame the brief. Key framing decisions:
- If adoption is growing: lead with the growth, then note where investment would accelerate it
- If adoption is stable: lead with coverage and the business value being delivered, then note what would expand it
- If adoption is declining: lead with what is driving the decline honestly, then present the recommended response

The stakeholder brief should not be a sanitised version of the internal assessment. It should be honest about where the system is underperforming and specific about what would change it. A brief that reports only good news when the internal assessment shows problems will erode credibility when the problems become visible.

The brief's ask should be specific to what the internal assessment says is most needed:
- If system gaps are the primary blocker: the ask is contribution support or team capacity for specific additions
- If awareness is the primary blocker: the ask is time and access for onboarding and communication
- If governance process is not being followed: the ask is alignment and clarification, possibly a governance working session
- If version lag is dominant: the ask is engineering time to migrate, with a clear case for why it matters

---

## Phase 3: Produce the governance package

---

### Governance review package

Open with one headline sentence: how the system is performing for its teams this period, and the one thing to act on.

**Period:** [reporting period] | **Previous review:** [date, if applicable]
**Sign-off:** a person must approve the brief before it is distributed; the internal assessment is for the system team

---

#### Internal assessment

**Adoption summary**

| Measure | This period | Last period | Change |
|---|---|---|---|
| Teams in scope | [n] | [n] | |
| Teams reached (have access) | [n] of [n] | [n] of [n] | [+/-] |
| Teams adopting — design | [n] of [n] | [n] of [n] | [+/-] |
| Teams adopting — engineering | [n] of [n] | [n] of [n] | [+/-] |
| At-risk teams | [n] | [n] | |

**Coverage** (supply: the share of teams' interface needs the system provides, with its source) is stated in a sentence, as adoption-report defines it; the definitions are adoption-report's, so the two documents agree.

**Trend:** [Growing / Stable / Declining / Mixed]

**Drift summary**

| Classification | Count | % of total | Interpretation |
|---|---|---|---|
| A — Intentional divergence | | | |
| B — Version lag | | | |
| C — Accidental drift | | | |
| D — Misunderstanding | | | |
| E — System gap | | | |

**Cross-skill interpretation:** [One paragraph synthesising what the adoption data and drift classifications reveal together — the insight neither skill produces alone]

**Primary blocker:** [Single sentence]

**What is working:** [Two to three specific things]

**Recommended actions:**

1. [Immediate — for at-risk teams]
2. [Near-term — addressing the primary blocker]
3. [Longer-term — addressing system gaps if identified]

---

#### At-risk team detail

For each at-risk team: the adoption signal, the likely cause based on drift classification, and the specific recommended next step.

---

#### Stakeholder brief

[Ready-to-send brief, produced by the stakeholder-brief skill, using the internal assessment as input]

Include a note: *Review this brief before sending. Confirm tone, framing, and ask are appropriate for the specific audience.*

---

#### Suggested follow-up

Based on the governance review findings, note which additional skills would be valuable to run:
- If system gaps are significant: `component-audit` for gap analysis → `contribution-workflow` for the contribution plan
- If drift is widespread: `full-system-diagnostic` for a comprehensive assessment
- If documentation is the primary blocker: `usage-guidelines` and `pattern-documentation` for the highest-traffic components
- If version lag is significant: `change-communication` to make the migration case to consuming teams

---

#### Scope, closing note and footer

One combined Scope block covering all three steps (per output-discipline), marking which adoption figures were measured and which estimated. Then one closing note inviting the user to flag intentional deviations. End with a one-line provenance footer:

*Generated by Design System Ops governance-review agent · [date]*

---

## Recurring workflow

Loading, saving and pruning follow the chained-run rules. When a previous governance package exists:

1. **Auto-populate trend fields** in the adoption summary table (This period vs. Last period).
2. **Compare internal assessments:**
   - Primary blocker: same as last period, changed, or resolved?
   - At-risk teams: newly at-risk, still at-risk, or recovered?
   - Drift classification trend: is the mix shifting?
3. **Flag persistent issues** — any primary blocker present in 3+ consecutive reviews is a structural problem requiring escalated investment, not incremental action. Note this explicitly in the stakeholder brief.

## Quality checks

- Cross-skill interpretation section contains insight that neither the adoption report nor the drift detection produces alone
- Internal assessment includes what is working, not just what is not
- Stakeholder brief is honest about underperformance — not a sanitised summary
- At-risk team detail is specific: named teams, specific signals, specific next steps
- Package opens with one headline sentence, has one combined Scope block and one closing note, and ends with the provenance footer
- The run stopped for the user's confirmation between the internal assessment and the brief
- Adoption figures are counts of teams, as adoption-report reports them, never percentages
- Suggested follow-up is based on findings, not a generic list
