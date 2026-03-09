---
name: drift-detection
description: "Identify where a design system has diverged from its original intent across the whole system — components implemented differently to spec, tokens overridden locally, patterns forked across teams. This is a system-wide sweep for divergence patterns, NOT a single-component spec comparison. Trigger when someone says: find drift, where has the system diverged, design code inconsistency, what's out of sync, where are teams going off-system, component drift, or anything about identifying gaps between design system intent and actual implementation. Do NOT trigger for checking one specific component against its design spec — use design-to-code-check for that."
references:
  - references/token-architecture.md
  - references/design-to-code-contract.md
  - references/output-discipline.md
---

# Drift detection

A skill for identifying and classifying drift in a design system — the accumulated distance between design system intent and actual implementation across consuming products. Produces a drift report with severity ratings, origin classification, and recommended response for each finding.

## Context

Drift is the normal condition of a used design system. The question is not whether your system has drifted — it has — but whether the drift is intentional, how severe it is, and whether it is compounding.

Not all drift is bad. A product team that made a deliberate, documented exception to an established pattern is making a design decision. A product team that unknowingly re-implemented a design system component with slightly different spacing is creating maintenance debt. The distinction matters, because the response is different: intentional drift might become a contribution, while accidental drift needs to be corrected and its root cause addressed.

This skill distinguishes between drift types and routes each finding to the appropriate response.

---

## Reference material

Before producing output, read the following bundled knowledge notes. These contain the frameworks and mental models that make this skill's output production-grade.

- **Token Architecture Principles** (`references/token-architecture.md`) — Three-tier token model, naming conventions, reference rules, and common failure patterns
- **Design-to-Code Contract Definitions** (`references/design-to-code-contract.md`) — Design, build, documentation, and release contract definitions with common gap patterns

Load and read each reference file listed above before proceeding. The frameworks in these notes inform every check and recommendation this skill produces.

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `severity.*` — overrides for drift finding severity ratings
- `system.styling` — pre-selects token drift detection approach (CSS vars, SCSS, Tailwind, CSS-in-JS)
- `integrations.*` — enables auto-pull for drift comparison data (see below)
- `recurring.*` — enables comparison with previous drift report

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically:

**Figma MCP** (`integrations.figma.enabled: true`):
- Read component specifications from the published library at `integrations.figma.file_key`
- Use as the design-side reference for visual and API drift detection
- Compare Figma component properties against code component props to detect API drift without manual specification

**GitHub** (`integrations.github.enabled: true`):
- Search `integrations.github.repo` for code patterns that indicate drift:
  - Hardcoded colour values outside the design system package
  - Local component re-implementations (component names used outside the system's source)
  - Token overrides using CSS `!important` on design token properties
- Pull recent PRs to identify components changed outside the design system package
- Use commit history on component files to detect version lag

**Chromatic** (`integrations.chromatic.enabled: true`):
- Pull visual diff data — components with accepted visual changes outside a DS release cycle are potential visual drift
- High rates of accepted changes may indicate the team is accepting drift rather than correcting it

If an integration fails, log it and proceed with manual input.

## Recurring workflow

If `recurring` is configured in `.ds-ops-config.yml`:

1. **Load the previous drift report** from `recurring.output_directory`.
2. **Compare against current findings:**
   - New drift instances since last run
   - Resolved drift instances (corrected since last run)
   - Persistent drift (present for 2+ cycles — escalate severity)
   - Classification shift (e.g. accidental drift that became intentional divergence)
3. **Add a "Drift trend" section** to the report:
   - Total drift count: increasing / stable / decreasing
   - Drift velocity: how fast is new drift accumulating vs. being resolved?
   - Classification trend: is the mix shifting toward more system gaps (E) or more accidental drift (C)?
4. **Save output** and prune per `recurring.retain_count`.

## Step 1: Define the scope

Ask for or confirm (skip questions already answered by auto-pull):
- What is being assessed? (Specific product, specific component set, specific token scope, or full system)
- What sources are available for comparison? (Figma files, codebase, documentation, Storybook, token files in any format — JSON, CSS custom properties, SCSS variables, Tailwind config)
- Are there specific areas where drift is already suspected?
- Is there any known intentional divergence that should be documented rather than flagged as a problem?

The more specific the scope, the more actionable the report. A drift detection across "the whole system" surfaces patterns but produces a long list of findings with limited prioritisation signal. Scoping to a specific product or a specific component category produces a more actionable output.

**Small-system note (fewer than 5 components):** For systems this size, scope to the full system — there is no need to sample. Drift patterns are different in small systems: teams are typically smaller and more aligned, so drift is less likely to be accidental and more likely to be intentional divergence (Classification A) or a system gap (Classification E). Simplify the output to a per-component checklist rather than a full drift report. If all components show no drift, state that as the finding and recommend a review cadence.

## Step 2: Establish the reference point

Drift is always relative to something. Confirm the source of truth being used as the reference:

- The design system's Figma library
- The published component package at a specific version
- The documented specification for each component
- All of the above (inconsistencies between these are themselves a drift signal)

If there is no clear single source of truth, that is a finding in itself and should be included at the top of the report.

## Step 3: Identify drift instances

Assess across four dimensions:

### Visual drift
Differences in the visual treatment of a component or pattern compared to the design system reference. Includes spacing, colour (particularly non-token values), typography, border radius, shadow, and icon usage.

For each instance: name the component or pattern, describe the visual difference, and note whether it appears to be intentional or accidental.

### Behavioural drift
Differences in interactive behaviour — state transitions, animation, timing, keyboard behaviour, focus management — compared to the designed and documented component behaviour.

Behavioural drift is often the hardest to detect without direct testing, but it carries the highest risk because it includes accessibility regressions.

### API drift
Components implemented with different props, different prop names, or different prop semantics than the design system's published API. This is most common when teams implement a component locally rather than consuming it from the system, or when a local version was built before the system component existed and was never migrated.

### Token drift
Raw values used where design tokens should be referenced. Tokens referenced at the wrong tier. Local token overrides that conflict with semantic intent. Token names used inconsistently across implementations.

Detection depends on the styling approach: in CSS custom properties, look for raw values outside `var()`. In SCSS, look for raw literals not using `$` variables. In Tailwind, look for arbitrary value brackets (`h-[12px]`, `bg-[#ff0000]`) — standard utility classes that resolve to configured tokens are not drift. In CSS-in-JS, look for raw values outside theme object references. When SCSS variables are the token system, tier can be inferred from naming patterns (e.g. `$color-blue-500` → primitive, `$color-action-primary` → semantic) even without a full SCSS parser.

## Step 4: Classify each drift instance

Classify every finding before assigning a response:

**Classification A: Intentional divergence**
The product team made a deliberate decision to diverge from the system, for a known reason. This may be appropriate (the system does not serve this context) or a contribution candidate (the need is real and should be in the system).

**Classification B: Version lag**
The implementation matches an older version of the design system. The system has moved on; the product has not. This is not a mistake — it is normal entropy — but it accumulates into a migration burden if left unaddressed.

**Classification C: Accidental drift**
The implementation diverged from the system without intent. Most commonly caused by implementing a component locally when the system version was not yet available, then not migrating once it was.

**Classification D: Misunderstanding**
The implementation reflects a misreading of the documentation or specification. The consumer thought they were using the system correctly and did not know they were not.

**Classification E: System gap**
The drift exists because the system did not have what the product team needed. The divergent implementation is the product team's solution to a design system gap, not a mistake.

## Step 4a: Drift impact severity weighting

Not all drift carries equal risk. Weight severity by component criticality:

**Critical path components** (core navigation, authentication, checkout, primary data entry) — drift here is automatically elevated one severity level. A Medium finding on a checkout component becomes High.

**High-traffic components** (buttons, form inputs, cards, modals) — drift here affects the most users. Weight stays as assessed but flag the blast radius.

**Utility components** (layout wrappers, spacing helpers, icon containers) — drift here is lower risk. A Medium finding may be downgraded to Low if the component is not user-facing.

### Recommendation paths by classification

After classifying each drift instance, route it to the appropriate response:

| Classification | Primary response | Skill to run next |
|---|---|---|
| A — Intentional divergence | Document as a decision record | `decision-record` |
| B — Version lag | Offer migration path with effort estimate | `deprecation-process` (for migration guidance) |
| C — Accidental drift | Fix the implementation + review docs that failed to prevent it | `design-to-code-check` |
| D — Misunderstanding | Update documentation + notify affected teams | `change-communication` |
| E — System gap | Route to contribution workflow | `contribution-workflow` |

## Step 4b: Breaking change impact modelling

For drift classified as B (version lag), model the migration impact:

**Per-instance migration cost:**
- How many files/components are affected by this specific drift?
- Is the migration a simple find-and-replace (prop rename, token swap) or a structural refactor (API redesign, composition change)?
- What is the testing surface area — does migrating this instance require regression testing across the consuming application?

**Aggregate migration debt:**
- Total instances of version lag across all assessed products
- Estimated effort to bring all instances current (rough T-shirt sizing: S/M/L per migration)
- Identify migration batches — drift instances that can be resolved together because they share a root cause (e.g., all products still on v2 Button)

**Migration path clarity:**
- For each version lag instance, is the migration path documented? If the design system shipped a breaking change without a migration guide, that is a governance finding (flag it separately).
- Are there migration codemods or scripts available? If not, recommend whether the migration warrants one.

This modelling converts drift from "a list of problems" to "a prioritised migration plan with estimated effort." Include it as a section in the drift report.

## Step 4c: Cross-system drift (multi-system environments)

For organisations with multiple design systems (brand-specific, platform-specific, sub-systems), assess drift between systems:

- **Shared primitive divergence:** Do systems that share a primitive tier (colour palette, spacing scale) still agree on those primitives? Drift at the primitive level propagates to everything above it.
- **Semantic inconsistency:** Do the same semantic token names mean different things in different systems? `color.action.primary` resolving to blue in one system and green in another is a cross-system drift that confuses teams working across products.
- **Component contract conflicts:** Do components with the same name in different systems have different APIs? A `Button` in the marketing system and a `Button` in the product system should either share an API or have different names.

Cross-system drift is typically invisible until a team works across system boundaries. Surface it proactively.

## Step 5: Produce the drift report

Open with a headline sentence. Example: "Drift is moderate and mostly accidental — 3 components have diverged from the system, and 2 of those look like the team didn't know the system version existed. Here's the full picture."

---

### Drift detection report

**Date:** [date]
**Scope:** [what was assessed]
**Reference source:** [what the assessment was compared against]
**Assessment method:** [direct inspection / reported / mixed]

---

#### Summary

What is the overall drift picture? Is the system drifting in a controlled way or compounding? What is the most important finding? Write this like you're debriefing a colleague, not filing a compliance report.

---

#### Drift findings

For each finding:

| ID | Location | Dimension | Classification | Severity | Description | Recommended action |
|---|---|---|---|---|---|---|
| DF-01 | [product/team/component] | [visual/behavioural/API/token] | [A–E] | 🔴/🟠/🟡/⚪ | [specific description] | [specific action] |

**Severity key:** 🔴 Critical · 🟠 High · 🟡 Medium · ⚪ Low

---

#### Findings by classification

**Intentional divergence (A)**
List findings. For each, note whether it is a contribution candidate or an accepted exception. If it is an accepted exception, it should be documented as a decision record.

**Version lag (B)**
List findings. Group by component or token set. Identify whether a migration sprint would address the bulk of these, or whether they are spread too thin for a coordinated migration.

**Accidental drift (C)**
List findings. These are the highest priority for correction because they are unintentional — the product team would want to know.

**Misunderstanding (D)**
List findings. These indicate a documentation or communication gap. The finding should be corrected, and the documentation or onboarding that failed to prevent it should be reviewed.

**System gaps (E)**
List findings. These are contribution candidates. If the same gap appears across multiple products, the case for adding it to the system is stronger. Cross-reference the contribution workflow.

---

#### Root cause patterns

Step back from individual findings and identify patterns:
- Are there recurring drift types that suggest a systemic issue?
- Are there specific teams or products that appear consistently in the findings?
- Are there specific components or tokens that drift more than others?

Root cause patterns are more actionable than individual findings. Addressing a root cause prevents future drift; addressing individual findings only corrects the current state.

---

#### Recommended actions

Prioritised list:
1. Critical and High severity findings: address first, regardless of classification
2. System gap findings: route to contribution workflow
3. Version lag findings: schedule a migration sprint or build into the next release cycle
4. Misunderstanding findings: update documentation and notify affected teams
5. Intentional divergence: document exceptions that are not yet recorded

---

## Step 6: Visual drift comparison (when Figma Console MCP is available)

If the Figma Console MCP from Southleft is connected (check for `figma_capture_screenshot` and `figma_get_component_for_development` tool availability), enhance the drift report with visual evidence.

**Capture design reference:** Use `figma_capture_screenshot` to capture the current state of each drifted component as it appears in Figma. This uses the plugin's `exportAsync` API, which captures the live state — not a cached cloud render. The result is the design-side truth for visual comparison.

**Capture implementation reference:** Use `figma_get_component_for_development` to get dev-optimised component data alongside a rendered image. This gives you the design spec in a format that maps directly to implementation properties.

**Visual diff in report:** For each drift finding classified as "implementation divergence" or "version lag", include both the Figma screenshot and a description of what the code implementation looks like. This gives the reader a visual understanding of the gap, not just a textual description of property mismatches.

**When the standard Figma MCP is connected (read-only):** Screenshots via REST API are available but reflect the last-published cloud state, not the current live state. Note this limitation — if the Figma file has unpublished changes, the screenshot may not reflect the latest design intent.

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This analysis identifies where implementations differ from the system — it cannot always tell why. The classification system (intentional, accidental, version lag, misunderstanding, system gap) is a starting point. If any instance is misclassified, let me know — your corrections make future drift checks more accurate. The goal is to distinguish the drift that needs fixing from the drift that needs documenting.

---

## Quality checks

- Every finding has a classification and a recommended action, not just a description
- Severity ratings are justified by the specific impact, not assigned generically
- Root cause patterns section exists and adds something beyond the individual findings list
- System gap findings are distinguished from mistakes — product teams whose divergence filled a genuine system gap should not be treated as having done something wrong
- The report distinguishes between drift that should be corrected and drift that should be documented as accepted divergence
- If visual comparisons were captured, each finding includes the Figma reference screenshot
- The closing note about intentional deviations is present
