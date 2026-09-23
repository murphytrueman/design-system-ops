---
name: system-health
description: "Holistic health check across tokens, components, docs, adoption, governance, AI readiness, platform maturity, with status labels. Triggers: how healthy is my system, system health check, big picture. Not for one area (use its audit) or external comparison (system-benchmark)."
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/adoption-measurement.md
  - ../../knowledge-notes/documentation-coverage.md
  - ../../knowledge-notes/output-discipline.md
---

# System health

A skill for producing a holistic design system health assessment across seven dimensions: tokens, components, documentation, adoption, governance, AI readiness, and platform maturity. Output is a findings-based executive summary with a prioritised action list.

## Before you begin: verify references

Before doing anything else, confirm that every file listed in this skill's frontmatter `references:` field exists at its relative path from this SKILL.md. If any are missing, stop — the install is incomplete. This usually means a third-party installer (for example `npx skills install`) flattened the skill into a standalone folder and dropped the repo-root `knowledge-notes/` directory this skill depends on. Tell the user to reinstall using a supported method from `1-INSTALL.md` (git clone, or the `.plugin` bundle in Cowork) and to run `verify-install.sh` from the install root to confirm the fix. Only proceed without the references if the user explicitly says to — and if they do, state clearly in your output that it was produced in degraded mode without the pack's reference material.

## Context

Token audits find naming violations. Component audits find unused variants. Adoption analysis finds coverage gaps. But none of these in isolation tells you whether the system is healthy. Health is a function of how well all seven dimensions are working together — a system with excellent tokens and terrible governance is still a fragile system, and a well-adopted system with thin documentation is one team member departure away from collapse.

This assessment is designed to give a snapshot of the whole system, not a deep dive into any single area. It is useful as a starting point for prioritisation, as a quarterly review artefact, or as background for a stakeholder conversation about where investment is needed.

For deeper work on any individual dimension, route to the relevant specialist skill (token-audit, component-audit, etc.).

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `system.*` — system size, framework, and theming context
- `severity.*` — finding severity overrides
- `integrations.*` — measured signals across all seven dimensions (see below)
- `recurring.*` — the Health trend section (see below)

## Auto-pull integrations

System health is the broadest assessment, so every configured integration feeds at least one dimension:

**Figma MCP** (`integrations.figma.enabled: true`):
- Pull component count, variant count, and library analytics for the Components and Adoption dimensions
- Pull variable collections for the Tokens dimension

**npm registry** (`integrations.npm.enabled: true`):
- Pull download trends for the Adoption dimension — rising, flat, or declining downloads over the last 4 quarters
- For monorepos, pull per-package stats as directional signals

**GitHub** (`integrations.github.enabled: true`):
- Pull PR frequency and contributor count for the Governance dimension
- Pull issue count and staleness for the Documentation dimension
- Pull commit frequency on token and component files for the Tokens and Components dimensions

**Storybook / Documentation** (`integrations.storybook.enabled` or `integrations.documentation.enabled`):
- Pull documentation coverage percentage for the Documentation dimension
- Compare against component inventory to calculate docs-per-component ratio

These signals are supplementary — the dimension assessment still requires the structured checks in Step 2. But auto-pulled data replaces estimated figures with measured ones, which makes the findings more defensible.

## Recurring workflow

Follows the recurring-run procedure in the configuration-and-recurring note. Specific to this skill:

- **Compare dimension statuses:** which dimensions improved, held steady, or regressed.
- **Add a "Health trend" section** before the action list, with previous status, current status and direction for each dimension. Highlight any dimension that worsened — this is a regression.

## Step 0: Identify what you're looking at

Before assessing health, determine what kind of shared UI this actually is. Not everything is a design system, and the distinction changes what advice is useful.

**Classify the library type from the codebase signals:**

- **Design system** — Tokens + components + documentation + governance. Multiple tiers of tokens, a component library with contribution guidelines, versioned releases, and a documentation site. This is the full template — all seven dimensions apply.
- **Component library** — A shared component package without the broader system infrastructure. Has components, may have tokens, but no formal governance, contribution process, or adoption tracking. Common in mid-size teams. Assess Tokens, Components, and Documentation. Governance and Adoption are stretch goals, not gaps — frame them as "when you're ready" not "you're missing this."
- **Pattern library** — Documented UI patterns, often in Fractal, Storybook, or a static site generator. May use Twig, Nunjucks, or vanilla HTML. Focus is on reference and consistency rather than consumption as a package. Assess Documentation and Components. Token architecture is often absent by design — do not flag it as a gap unless the team is trying to build one.
- **Utility collection** — A grab-bag of shared helpers, mixins, base styles, or layout primitives. Often a developer's first step toward shared UI. Assess what's there without projecting a design system roadmap onto it. The most useful output is "here's what you have, here's what's consistent, here's what's not."

**How to detect:** Look at the codebase structure, not what the README calls it. A repo named "design-system" with 4 components, no tokens, and no docs is a component library in early stages, not a design system with gaps. Signals: presence of token files (JSON, SCSS variables, CSS custom properties), number of components, presence of a documentation platform config (Fractal, Storybook, Zeroheight), package.json publishing config, and whether there are versioned releases.

**Include the classification in the report header** as "Library type: [Design system / Component library / Pattern library / Utility collection]" and calibrate all recommendations to match. A pattern library does not need a "contribution workflow" — it needs its patterns to be findable and accurate.

---

## Step 1: Gather input

A system health assessment can be completed at different levels of depth depending on what information is available. Ask for or confirm (skip questions already answered by auto-pull):

- Access to the token files (JSON, DTCG, CSS custom properties, SCSS variables, Tailwind config, Style Dictionary, or TypeScript objects), component library, and documentation platform (if available)
- Approximate size of the system: number of components, number of tokens, number of teams consuming
- Any known problem areas the person wants the assessment to pay particular attention to
- Whether this is a first-ever assessment or a recurring review

If access to the system itself is limited, the assessment can be conducted through a structured interview. Note in the output that the assessment is based on reported information rather than direct inspection, and flag which findings would benefit from direct verification.

**Small-system note (fewer than 5 components):** The seven-dimension assessment still works at this size, but adjust expectations for the Components dimension. Complexity distribution (foundational vs. compound vs. feature) is not meaningful with 1–4 components — skip it. Focus the Components dimension on API clarity, state coverage, and documentation completeness per component instead. For the Adoption dimension, redefine "active adoption" in terms of what percentage of the team's actual needs the system serves, not raw component count. A system with 3 components that covers 80% of a team's interface needs is healthier than a system with 30 components that covers 20%.

## Step 1b: Maturity stage — infer it, don't ask for it

Don't ask the user to place the system and then assess against their answer; the report would just hand their view back to them. Calibrate expectations by library type (Step 0) while assessing, then infer the stage from the Step 2 evidence using the named stages in the component-governance note: Ad-hoc / Managed / Systematic / Measured / Optimised. Place the system at the highest stage whose criteria the evidence meets, and name the dimension that stops it reaching the next.

If the user has said where they'd place it, note in the report where the evidence differs and why — that gap is often the most useful conversation.

Use the inferred stage when writing the summary — frame findings as "appropriate for this stage" or "below expectations for this stage". A Managed system with no AI readiness is expected. A Measured system with no AI readiness is a significant gap.

## Step 2: Assess each dimension

For each dimension, assess the current state and assign a status:
- **Strong:** Meeting or exceeding expectations for this library type
- **Functional:** Working but with notable gaps
- **Weak:** Present but causing problems or significantly behind expectations
- **Absent:** Not addressed or non-functional

### Dimension 1: Tokens

Assess:
- Are primitive and semantic tiers both present? Component tokens are optional (see the token-architecture note), but if the system uses them, are they applied consistently?
- Do semantic tokens describe intent rather than appearance?
- Are raw values hardcoded anywhere at the semantic or component tier?
- Is the token set consistent across platforms or contexts where multiple exist?
- Is there a clear owner for the token architecture?

Key questions to ask or check:
- How many tokens are in the system? Is the count growing faster than the product footprint?
- Are tokens stored in a single source of truth, or scattered?

### Dimension 2: Components

Assess:
- Is there a clear principle for what belongs in the system vs what stays local?
- Are component APIs documented with props, types, and defaults?
- Are there components with no known usage?
- Is the complexity distribution reasonable — are most components foundational, with fewer compound and feature-level components?
- Are interactive states covered (hover, focus, active, disabled, error)?

Key questions:
- What is the oldest un-updated component, and why has it not been updated?
- Are there components that exist in multiple variants where a single flexible component would do?

### Dimension 3: Documentation

Assess:
- Does every component have usage guidelines (not just a Storybook entry)? For the coverage ladder and staleness rules, see the documentation-coverage note, or run docs-coverage for depth.
- Are anti-patterns documented alongside recommended usage?
- Is documentation discoverable — can a new team member find what they need without help?
- Is documentation maintained after component changes?
- Is there a documented contribution process?

Key questions:
- When was the documentation last updated?
- Is there a process for flagging documentation gaps?

### Dimension 4: Adoption

Assess:
- What percentage of product teams are actively using the system?
- Are teams able to use the system without regularly working around it?
- Is there evidence of parallel solutions being built outside the system?
- Is the system used by design and engineering, or primarily one of the two?

Key questions:
- Where are teams going when the system does not have what they need?
- Are there product areas or team contexts where adoption is consistently low?

Note: keep coverage and adoption separate — see the adoption-measurement note.

### Dimension 5: Decision-making

**Label this dimension based on the library type identified in Step 0:**
- **Design system** → label as "Governance" in the report. The full governance framework applies.
- **Component library or Pattern library** → label as "Decision-making" in the report. Use plain language: "how decisions get made" rather than "governance model." A small team with a Slack channel and a clear owner has functional decision-making even without a documented governance framework.
- **Utility collection** → label as "Ownership" in the report. The only question that matters is: does someone own this, and can they say no to bad additions?

Assess:
- Is there a clear process for contributing new components?
- Is there a clear process for deprecating and removing components?
- Are breaking changes communicated in advance?
- Is there a documented decision-making process for system-wide changes?
- Is there a named owner or team responsible for the system's health?

**Calibrate for team size:** For teams under 5 people, a documented governance framework is overhead, not maturity. What matters is whether someone is responsible and whether decisions are reversible. Frame recommendations accordingly — "make sure someone owns this" rather than "establish a governance model."

Key questions:
- What happens when a product team needs something the system does not have?
- When was the last significant decision about the system made, and how was it communicated?

### Dimension 6: AI readiness (staff-level)

Assess:
- Do components have structured, machine-readable metadata (JSON manifest, Custom Elements Manifest, or equivalent)?
- Are component descriptions formatted consistently for LLM consumption (six-section format or equivalent)?
- Are semantic tokens documented with intent descriptions, not just name-value pairs?
- Is there a component manifest that AI tools can query to find the right component for a given need?
- Are Figma descriptions and code documentation in sync?

Key questions:
- Can an AI agent, given only the system's documentation, reliably select the correct component and configure it correctly?
- What percentage of components have structured, machine-readable descriptions?
- Are token files in a format AI tools can parse without transformation (DTCG, JSON, CSS custom properties)?

### Dimension 7: Platform maturity (staff-level)

Assess:
- Are component APIs versioned with semantic versioning?
- Is there a predictable release cadence that consuming teams can plan around?
- Are breaking changes accompanied by blast radius analysis and migration paths?
- Are there defined response time expectations for bug reports and support requests?
- Do consuming teams treat the system as infrastructure they depend on, or as a toolkit they use optionally?

Key questions:
- What is the median time from bug report to acknowledgement? From acknowledgement to resolution?
- When was the last breaking change? How was it communicated? Did it include a migration path?
- Do consuming teams have a way to pin to a specific version?

## Step 3: Produce the health report

Open with a headline sentence that tells the reader how worried they should be and where to focus — before any tables or structure. Example: "Your system is strong on components and tokens, but governance and documentation are the bottleneck. Here's the dimension-by-dimension picture."

---

### Design system health report

**Date:** [date]
**Assessment type:** Direct inspection / Reported information / Mixed
**Assessed by:** [if applicable]

---

#### Overall health

| Dimension | Status | Key finding |
|-----------|--------|-------------|
| Tokens | 🟢 / 🟡 / 🟠 / 🔴 | [One-sentence summary] |
| Components | | |
| Documentation | | |
| Adoption | | |
| Governance / Decision-making / Ownership | | |
| AI readiness | | |
| Platform maturity | | |

*Use the dimension label that matches the library type from Step 0: "Governance" for design systems, "Decision-making" for component/pattern libraries, "Ownership" for utility collections.*

Status key: 🟢 Strong · 🟡 Functional · 🟠 Weak · 🔴 Absent

**Maturity stage (inferred from evidence):** [Ad-hoc / Managed / Systematic / Measured / Optimised] — [one sentence of evidence]. To reach the next stage, the system needs [specific action]. [If the user placed it differently: one sentence on where the evidence differs.]

---

#### Summary

Two to three sentences. What is the honest state of this system? What is the most important thing to pay attention to? Write this like you're briefing a peer, not filing a report.

---

#### Dimension findings

For each dimension: the status emoji, two to four specific findings with evidence, and a one-sentence summary of the most important action. Skip dimensions with no findings — a single line in the summary table ("🟢 Strong — no issues found") is enough.

---

#### Prioritised action list

Group recommendations into three tiers:

**Immediate (next 4 weeks)**
Actions that, left unaddressed, will make other improvements harder or will actively erode system trust.

**Near-term (next quarter)**
Structural improvements that require planning but are clearly worth doing.

**Longer-term (6+ months)**
Investments that will pay dividends once the immediate and near-term work is done.

---

**Scope**
- **Inspected:** [files, directories, or data sources actually read]
- **Not inspected:** [what was out of reach, and therefore cannot be commented on]
- **How "none found" was checked:** [for any absence claim, how the search was shown to work — omit if the report makes no absence claims]
- **Assumptions:** [anything taken as given rather than verified, including anything reported rather than inspected]

End with the closing note below.

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This assessment sees your system's artefacts — it does not see the history, constraints, or trade-offs behind them. Some findings may flag gaps your team has already considered and accepted. If any finding describes an intentional decision or a known limitation, let me know — I'll calibrate future assessments to your system's actual priorities rather than a generic ideal. The goal is to surface blind spots, not to question choices you've already made deliberately.

## Quality checks

- Each dimension status has specific evidence behind it, not a general impression
- The overall summary is honest — a dimension marked "Functional" is not described as healthy if the findings show structural problems
- The action list is ordered by impact, not by ease
- If the assessment was conducted without direct system access, this is clearly noted throughout
- Dimension findings are specific: named problems, not categories of problems
- The maturity stage is inferred from the evidence, not taken from the user's self-placement
- The Scope block and the closing note about intentional deviations are present
