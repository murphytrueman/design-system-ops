---
name: full-system-diagnostic
description: "Chains token, naming, component, drift and docs-coverage audits (plus theme and Figma variable audits where they apply), then system-health, into one diagnostic report with cross-skill patterns and a ranked action list. Invoked by /full-diagnostic."
---

# Full system diagnostic

A chained workflow that runs six audit skills in sequence and synthesises their outputs into a single, unified diagnostic report. Covers tokens, components, naming, drift, documentation coverage, and overall system health, with conditional theme and Figma-variable audits when the system supports theming or has Figma connected. Produces a ranked action list with cross-skill patterns identified that no single skill would surface alone.

**Output type:** Proposal only. This agent produces analysis and recommendations. It does not make changes. Every action item requires human decision and execution.

**Run rules:** Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — loading, one inventory, hand-off cards, one report, skipped-permission steps, configuration, and recurring runs. This file holds only what is specific to the diagnostic chain.

---

## When to run this

- Quarterly system reviews
- Before a significant investment conversation with stakeholders
- When a new design systems lead joins and needs an honest picture
- When adoption is declining and the cause is unclear
- Before a major version or platform migration

Do not run the full diagnostic when you need a specific, focused answer. If the question is "are my tokens named correctly," run `naming-audit`. If the question is "why isn't this team using the system," run `adoption-report`. The full diagnostic is for when you need to understand the whole.

---

## Configuration

Configuration and integrations follow the chained-run rules. Specific to this chain: `theme-audit` runs only when `system.theming: true` (or theming is detected), and `figma-variable-audit` runs only when `integrations.figma` is configured and the Figma tools are permitted. When a gate isn't met, the step is skipped and the report marks it not applicable — not a gap.

## Phase 1: Prepare

Before running any skill, establish scope and access:

1. Confirm what is in scope: which products, which system version, which consuming teams
2. Confirm what sources are available: token files, component library, codebase, documentation platform, usage data
3. Note any known problem areas to flag for cross-skill correlation
4. Set the assessment date — this is the point-in-time snapshot
5. **Build the inventory.** Build the single run inventory (component source paths, token files, documentation sources) per the chained-run rules. Every step below uses it instead of running its own discovery or inventory step.
6. **Count components** from the inventory. The count determines which workflow path to follow.

If access is partial, proceed and list the gaps in the Scope block.

---

## Small-system gate

**If the system has fewer than 5 components, stop here.** The full diagnostic chain is designed for systems with enough surface area that cross-skill patterns emerge — concentrated debt, documentation gaps, governance gaps, structural gaps. A system with 1–4 components does not have the complexity to produce meaningful cross-skill synthesis, and running all six skills will generate repetitive findings at disproportionate cost.

Instead, recommend individual skills based on what the person actually needs:

| If the concern is… | Run this instead |
|---|---|
| Token quality or structure | `token-audit` |
| Naming consistency | `naming-audit` |
| Component coverage or duplication | `component-audit` |
| Documentation falling behind the code | `docs-coverage` |
| Implementation diverging from spec | `drift-detection` or `design-to-code-check` |
| Overall maturity assessment | `system-health` (which works well as a standalone at any system size) |
| Pre-release quality for a specific component | `component-to-release` agent |

**What counts:** Count distinct components in the published library (Button, Card, Modal = 3 components). Variants of a single component do not count separately (Button with 9 variants = 1 component). Utility components (layout wrappers, visually-hidden helpers, etc.) count only if they are published as part of the system's public API.

**If the system has 5–15 components:** Proceed with the full diagnostic, but expect the cross-skill synthesis (Phase 3) to surface fewer patterns. Note in the report that the system's small size limits the pattern-detection value of the full chain, and that findings from individual skills may be more actionable than the synthesis.

**If the system has 15+ components:** Proceed normally.

---

## Phase 2: Run the skill sequence

Run the skills in this order, passing a hand-off card between steps. The five core audits run first (tokens, naming, components, drift, docs-coverage), then any conditional audits that apply, and finally system-health — which runs last so it can synthesise everything upstream.

### Step 1 — Token audit (`token-audit`)

Run the full token audit. Capture:
- Tier structure assessment (which tiers are present)
- Total violation count by severity
- The three highest-priority findings

Carry forward into subsequent steps: any token naming violations that may correspond to component naming violations (same team, same era, same pattern).

### Step 2 — Naming audit (`naming-audit`)

Run the naming audit across components, tokens, and patterns. Capture:
- Convention inventory (what conventions are actually in use)
- Violation counts by category
- Any naming patterns that correlate with findings from the token audit

At this point, check: are token naming violations and component naming violations concentrated in the same area of the system? If yes, this is a cross-skill finding — note it.

### Step 3 — Component audit (`component-audit`)

Run the component audit. Capture:
- Library size and usage distribution
- Unused or likely unused components
- Duplication findings
- Coverage gaps

Cross-reference: do coverage gaps correspond to areas where the token audit found missing semantic tiers? A system with no semantic feedback tokens and no feedback components has a structural gap, not just a missing component.

### Step 4 — Drift detection (`drift-detection`)

Run drift detection. Capture:
- Classification breakdown (A–E)
- Severity distribution
- Root cause patterns

Cross-reference with component audit coverage gaps: are teams building locally because the system does not have what they need (Classification E — system gap)? How much of the drift is the system's fault vs. the teams' fault?

### Step 5 — Docs coverage (`docs-coverage`)

Run the docs-coverage audit. Capture:
- Coverage by rung (exists / described / guided / undocumented)
- Undocumented components, with the join-confidence tier on each
- Staleness findings (docs predating a component's last code change) and orphaned docs

Cross-reference with the component audit: do the undocumented components overlap with the unused or recently-added ones? Newly-added components with no docs are an onboarding-velocity problem; widely-used components with stale docs are a trust problem. Carry both forward — docs-coverage is the direct evidence for the documentation dimension that system-health would otherwise have to infer.

### Conditional steps — run only when applicable

These two audits are gated on configuration. Run each only if its gate is met; otherwise skip it and record "not applicable" in the report (an absent theming or Figma setup is not a finding).

**Theme audit (`theme-audit`) — if `system.theming: true` or theming is detected.** Capture theme coverage per mode, component-tier propagation gaps, and cross-theme consistency violations. Cross-reference with token-audit: missing semantic theming tokens found there should correspond to propagation gaps here.

**Figma variable audit (`figma-variable-audit`) — if `integrations.figma` is configured.** Capture code-vs-Figma variable discrepancies and orphaned variables. Cross-reference with token-audit: this is the design-side view of the same token architecture, and divergence between the two is a source-of-truth finding.

### Step 6 — System health (`system-health`)

Run the system health assessment last. It now has the full picture from all prior skills to draw on.

Cross-reference each dimension status against the evidence:
- Tokens status should reflect token audit findings (and theme-audit / figma-variable-audit, where they ran — the latter is the design-side view of the same token architecture)
- Components status should reflect component audit findings
- Documentation status should reflect docs-coverage findings directly — coverage by rung, staleness, and undocumented components — rather than inferring documentation health from naming
- Adoption status: this chain doesn't run `adoption-report`, so use adoption data only if the user supplied it. Otherwise infer adoption from the drift findings (widespread drift often signals adoption problems) and mark it as inferred in Scope
- Governance status should incorporate whether decision records exist for the problems the other skills surfaced

---

## Phase 3: Synthesise cross-skill findings

This is the step that the individual skills cannot do. Look across all the skill outputs for patterns that only emerge when you see everything together.

### Synthesis decision tree

Before looking for patterns, use this decision tree to focus the synthesis:

1. **Are violations from multiple skills concentrated in the same area?** (Same components, same team, same era)
   - Yes → Pattern 1 (Concentrated debt). The root cause is localised.
   - No → Continue.

2. **Is system health strong on core dimensions but adoption or drift weak?**
   - Yes → Pattern 2 (Documentation gap). The system is good but not legible.
   - No → Continue.

3. **Is drift accumulating faster than it is being resolved?** (Needs adoption or drift history — skip if neither was supplied.)
   - Yes → Pattern 3 (Governance gap). Process is broken.
   - No → Continue.

4. **Do token, component, and drift findings all point to the same missing capability?**
   - Yes → Pattern 4 (Structural gap). The system is incomplete.
   - No → Continue.

5. **Do components pass individual quality checks but lack machine-readable metadata?**
   - Yes → Pattern 5 (AI-readiness gap). Human-ready but not machine-ready.
   - No → Continue.

6. **Do components pass quality checks but the system lacks release infrastructure?** (Only if release data — changelog, tags, release history — was supplied or is in the inventory.)
   - Yes → Pattern 6 (Platform maturity gap). Toolkit, not platform.
   - No → Continue.

7. **Are high fan-in components drifting?**
   - Yes → Pattern 7 (Dependency cascade). Foundation is cracking.
   - No → No dominant cross-skill pattern. Report individual skill findings as the primary output.

Use the first "Yes" as the primary framing for the executive summary. If multiple patterns are present, lead with the one that has the highest impact.

### Pattern 1: Concentrated debt

Are the violations from multiple skills clustered in a specific area — a particular component category, a specific team's contributions, a particular era of the system?

If yes: this is not a distributed maintenance problem. It is a localised problem with a specific origin. The action is targeted, not systemic.

### Pattern 2: The documentation gap

Do the skills collectively show a system that is technically sound but poorly communicated? Good tokens, reasonable components, but low adoption and high drift?

docs-coverage is the direct evidence for this pattern — read it before concluding. A low described/guided rung distribution, a coverage gap concentrated in widely-used components, or a staleness tail where docs predate code changes all confirm a legibility problem rather than a quality one.

If yes: the system's quality is not the problem. The problem is legibility — teams cannot find or understand what is there. The action is documentation and communication, not rebuilding.

### Pattern 3: The governance gap

Do the skills show a system that drifts faster than it is maintained? New components added without deprecation of what they replace? Flat or declining engagement over time — only if adoption data was supplied, since this chain doesn't run `adoption-report`?

If yes: the system has a governance problem. Individual fixes will not help — the process around the system is broken. The action is governance investment before technical investment.

### Pattern 4: The structural gap

Do token violations, component gaps, and high drift all point in the same direction — the system does not serve a significant use case that teams have?

If yes: the system is not failing. It is incomplete. The action is a contribution plan for the missing area, not a maintenance plan for what exists.

### Pattern 5: The AI-readiness gap (staff-level)

Do components have good implementations but poor metadata? Are descriptions inconsistent, manifests missing, and token documentation lacking intent descriptions?

If yes: the system works for human consumers but is opaque to AI tooling. This is a staff-level observation — the individual skills might show strong results on their traditional dimensions but the system is not machine-readable. The action is a metadata and documentation sprint, not a component quality sprint.

### Pattern 6: The platform maturity gap (staff-level)

Only assess this pattern if release data (changelog, tags, release history) was supplied or is in the inventory; otherwise note it as not assessed in Scope. Do individual components pass quality checks but the system as a whole lacks infrastructure maturity? Symptoms: no semantic versioning, unpredictable release cadence, breaking changes without migration paths, no consumer contract testing.

If yes: the system is a toolkit, not a platform. Individual component quality is necessary but not sufficient. The action is governance and release infrastructure investment.

### Pattern 7: The dependency cascade (staff-level)

Cross-reference the component audit's dependency graph with the drift detection findings. Are foundation components (high fan-in) drifting? If a component used by 15 others has a token compliance violation, that violation is structurally amplified.

If yes: prioritise foundation component fixes over leaf component fixes. The blast radius makes the ROI of fixing foundation issues disproportionately high.

---

## Phase 4: Produce the diagnostic report

---

### Design system diagnostic report

Open with one headline sentence: how worried should the reader be, and what should they look at first.

---

#### Executive summary

Three to four sentences. What is the honest state of this system? What is the single most important finding? What is the recommended first action?

This section should stand alone. A stakeholder who reads only this should understand the situation and the priority.

---

#### Skill results summary

| Skill | Key metric | Top finding | Severity |
|---|---|---|---|
| Token audit | [violation count] | [top finding] | [🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low] |
| Naming audit | [violation count] | [dominant pattern] | |
| Component audit | [library size, % unused] | [top finding] | |
| Drift detection | [finding count, distribution] | [dominant class] | |
| Docs coverage | [coverage by rung, undocumented count] | [top gap or staleness finding] | |
| Theme audit *(if run)* | [coverage per mode] | [top propagation gap] | |
| Figma variable audit *(if run)* | [code-vs-Figma discrepancies] | [top discrepancy] | |
| System health | [overall status] | [weakest dimension] | |

If a conditional audit (theme or Figma) was not applicable or not permitted, retain its row and mark it "n/a — not applicable" or "skipped — not permitted" rather than deleting it or leaving it blank — so a reader can tell "skipped by design" from "failed to run."

---

#### Cross-skill patterns

State which pattern(s) from the synthesis decision tree were identified (concentrated debt / documentation gap / governance gap / structural gap / AI-readiness gap / platform maturity gap / dependency cascade). For each pattern identified:
- The evidence across skills
- The single recommended response
- Why addressing the pattern is more valuable than addressing individual findings

---

#### Ranked action list

**Immediate (next 4 weeks)**
Actions that address Critical findings or that, left unaddressed, make other work harder.

**Near-term (next quarter)**
Structural improvements with high return on investment.

**Longer-term (6+ months)**
Investments that require the immediate and near-term work to be done first.

---

#### Per-skill detail available on request

List each step that ran, with one line on what its full findings cover (for example, "Token audit — all 23 violations with file paths"). Don't attach the full outputs; the user can ask for any step's detail.

---

#### Suggested stakeholder brief

If the findings warrant a stakeholder communication (multiple Weak or Absent dimensions, critical findings, or a significant investment recommendation is implicit in the action list), note that the `stakeholder-brief` skill should be run next, using this report as input. Include the system's maturity stage (Ad-hoc / Managed / Systematic / Measured / Optimised) and the specific actions needed to reach the next stage — this gives stakeholders a concrete progression framework.

---

#### Scope, closing note and footer

One combined Scope block covering every step (per output-discipline), including skipped steps and inferred dimensions. Then one closing note inviting the user to flag intentional deviations. End with a one-line provenance footer:

*Generated by Design System Ops full-system-diagnostic agent · [date] · assessment method: [direct inspection / reported / mixed, by skill]*

---

## Recurring workflow

Loading, saving and pruning follow the chained-run rules; if session memory is enabled, save the combined report once at the end. When a previous full diagnostic exists:

1. **Compare the full reports:**
   - System health status changes (overall and per-dimension)
   - Violation count trends across token-audit, naming-audit, component-audit
   - Documentation coverage trend (rung distribution, undocumented count, staleness) from docs-coverage
   - Drift classification trend (is the system drifting faster or slower?)
   - Cross-skill pattern changes (did a pattern from last quarter resolve, persist, or worsen?)
2. **Add a "Diagnostic trend" section** before the action list:
   - Previous dimension statuses, current statuses, and direction of change
   - One sentence per cross-skill pattern: resolved / persistent / new
   - Highlight any metric that significantly worsened — this is the priority escalation

## Quality checks

- Cross-skill patterns section exists and contains findings that no single skill would produce
- Report opens with one headline sentence; provenance is a one-line footer
- One combined Scope block and one closing note — no per-skill headlines, Scope blocks or closing notes
- Executive summary stands alone without the per-skill detail
- Action list prioritises by impact, not by ease or by the order skills were run
- Skipped steps (not applicable or not permitted) are recorded in Scope
- Patterns 3 and 6 are assessed only when adoption or release data was supplied
- The report explicitly notes which findings are based on direct inspection and which are inferred
- The proposal boundary is clear: this is analysis, not a change plan
