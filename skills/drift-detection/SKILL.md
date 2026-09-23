---
name: drift-detection
description: "System-wide sweep for divergence: local re-implementations, token overrides, forked patterns, classified by cause. Triggers: find drift, where are teams going off-system, what's out of sync. Not for one component vs its spec (design-to-code-check)."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(diff:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(npm view:*)
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/output-discipline.md
---

# Drift detection

A skill for identifying and classifying drift in a design system — the accumulated distance between design system intent and actual implementation across consuming products. Produces a drift report with severity ratings, origin classification, and recommended response for each finding.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Drift is the normal condition of a used design system. The question is not whether your system has drifted — it has — but whether the drift is intentional, how severe it is, and whether it is compounding.

Not all drift is bad. A product team that made a deliberate, documented exception to an established pattern is making a design decision. A product team that unknowingly re-implemented a design system component with slightly different spacing is creating maintenance debt. The distinction matters, because the response is different: intentional drift might become a contribution, while accidental drift needs to be corrected and its root cause addressed.

This skill distinguishes between drift types and routes each finding to the appropriate response.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `severity.*` — drift finding severity overrides
- `system.styling` — pre-selects the token drift detection approach (CSS vars, SCSS, Tailwind, CSS-in-JS)
- `integrations.*` — drift comparison data (see below)
- `recurring.*` — drift trend (see Recurring workflow)

## Auto-pull integrations

**Figma MCP** (`integrations.figma.enabled: true`):
- Read component specifications from the published library at `integrations.figma.file_key`
- Use as the design-side reference for visual and API drift detection
- Compare Figma component properties against code component props to detect API drift without manual specification

**GitHub** (`integrations.github.enabled: true`):
- Search `integrations.github.repo` for code patterns that indicate drift (see the note's GitHub caution):
  - Hardcoded colour values outside the design system package
  - Local component re-implementations (component names used outside the system's source)
  - Token overrides using CSS `!important` on design token properties
- Pull recent PRs to identify components changed outside the design system package
- Detect version lag by comparing the design system version each consumer declares in `package.json` and resolves in its lockfile against the latest published version (`npm view [package] version`). Commit history doesn't tell you which version a consumer runs

**Chromatic** (`integrations.chromatic.enabled: true`):
- Pull visual diff data — components with accepted visual changes outside a DS release cycle are potential visual drift
- High rates of accepted changes may indicate the team is accepting drift rather than correcting it

## Recurring workflow

Follows the recurring-run procedure in the configuration-and-recurring note. Specific to this skill:

- **Persistent drift** (present for 2+ cycles): escalate severity.
- **Classification shift:** flag drift whose classification changed, e.g. accidental drift that became intentional divergence.
- **Add a "Drift trend" section** to the report:
   - Total drift count: increasing / stable / decreasing
   - Drift velocity: how fast is new drift accumulating vs. being resolved?
   - Classification trend: is the mix shifting toward more system gaps (E) or more accidental drift (C)?

## Step 1: Define the scope

Ask for or confirm (skip questions already answered by auto-pull):
- What is being assessed? (Specific product, specific component set, specific token scope, or full system)
- What sources are available for comparison? (Figma files, codebase, documentation, Storybook, token files in any format — JSON, CSS custom properties, SCSS variables, Tailwind config)
- Are there specific areas where drift is already suspected?
- Is there any known intentional divergence that should be documented rather than flagged as a problem?

The more specific the scope, the more actionable the report. A drift detection across "the whole system" surfaces patterns but produces a long list of findings with limited prioritisation signal. Scoping to a specific product or a specific component category produces a more actionable output.

**Drift needs a consumer.** If the only code in reach is the design system's own repository, there is nothing to have drifted from it. Stop and say so, then point to the skills that do apply: `token-compliance` for raw values in the system's own components, `component-audit` for duplication and gaps inside the library, `design-to-code-check` for one component against its spec. Ask for a consuming product (a path, a repo, or a Figma file of a product) before continuing.

**Small-system note (fewer than 5 components):** For systems this size, scope to the full system — there is no need to sample. Drift patterns are different in small systems: teams are typically smaller and more aligned, so drift is less likely to be accidental and more likely to be intentional divergence (Classification A) or a system gap (Classification E) — though each still needs the evidence Step 4 asks for. Simplify the output to a per-component checklist rather than a full drift report. If all components show no drift, state that as the finding and recommend a review cadence.

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
Raw values used where design tokens should be referenced, local token overrides that conflict with semantic intent, and token names used inconsistently across implementations.

The per-file search for raw values is `token-compliance`'s job, with its styling-approach rules and positive control. Don't re-implement it here. If a token-compliance report exists for the product, import its violation table as the token dimension. If not, run `token-compliance` on the consuming product first, then continue. What this skill adds is the consumer-versus-system reading of each violation: a raw value that equals a system token's resolved value is usually class C or D (someone typed the number instead of the name); a raw value that matches nothing in the system is class A or E and needs the evidence rule in Step 4. Local overrides of system tokens (`--color-action-primary: #...` redefined in the product, `!important` on token-driven properties) aren't in token-compliance's remit, so search for those here with a positive control.

## Step 4: Classify each drift instance

Classify every finding before assigning a response. Classes A, C and D are claims about the team's intent, which the code alone rarely shows. Assign a class only when its evidence rule is met; otherwise mark the finding **Unclassified — needs team input** and list what would settle it.

**Classification A: Intentional divergence**
The product team made a deliberate decision to diverge from the system, for a known reason. This may be appropriate (the system does not serve this context) or a contribution candidate (the need is real and should be in the system).
*Evidence required:* a code comment, ADR, PR description, or statement from the team recording the decision.

**Classification B: Version lag**
The implementation matches an older version of the design system. The system has moved on; the product has not. This is not a mistake — it is normal entropy — but it accumulates into a migration burden if left unaddressed.
*Evidence required:* the consumer's installed version (lockfile) is behind the latest published version, and the drifted behaviour matches the installed version.

**Classification C: Accidental drift**
The implementation diverged from the system without intent. Most commonly caused by implementing a component locally when the system version was not yet available, then not migrating once it was.
*Evidence required:* something that shows the divergence wasn't chosen, e.g. the local version predates the system one (git history) and nothing records a decision, or the team confirms it.

**Classification D: Misunderstanding**
The implementation reflects a misreading of the documentation or specification. The consumer thought they were using the system correctly and did not know they were not.
*Evidence required:* the usage matches a plausible reading of the docs (quote the ambiguous passage), or the team confirms it.

**Classification E: System gap**
The drift exists because the system did not have what the product team needed. The divergent implementation is the product team's solution to a design system gap, not a mistake.
*Evidence required:* no system component or token covers the need at the version the consumer runs.

**Unclassified — needs team input**
The evidence doesn't support any class above. Report the finding with its severity and the question that would classify it ("Was the 12px padding on CheckoutCard a deliberate choice?"). Don't guess.

## Step 4a: Drift impact severity weighting

Start from a base severity, then weight it:

- 🔴 **Critical** — an accessibility or behavioural regression on a critical path (focus lost in checkout, missing error announcement on sign-in)
- 🟠 **High** — an accessibility or behavioural regression elsewhere, or token drift that breaks theming (a hardcoded colour in a themed product)
- 🟡 **Medium** — visual or API divergence users or developers would notice, with no functional impact
- ⚪ **Low** — cosmetic divergence in a single instance, or drift in a non-user-facing utility

Then weight by component criticality:

**Critical path components** (core navigation, authentication, checkout, primary data entry) — drift here is automatically elevated one severity level. A Medium finding on a checkout component becomes High.

**High-traffic components** (buttons, form inputs, cards, modals) — drift here affects the most users. Weight stays as assessed but flag the blast radius.

**Utility components** (layout wrappers, spacing helpers, icon containers) — drift here is lower risk. A Medium finding may be downgraded to Low if the component is not user-facing.

### Recommendation paths by classification

After classifying each drift instance, route it to the appropriate response:

| Classification | Primary response | Skill to run next |
|---|---|---|
| A — Intentional divergence | Document as a decision record | `decision-record` |
| B — Version lag | Point at the release's migration guide; if the gap is mechanical, offer a codemod | `codemod-generator`, or the `token-migration` command for token renames |
| C — Accidental drift | Fix the implementation + review docs that failed to prevent it | `design-to-code-check` |
| D — Misunderstanding | Update documentation + notify affected teams | `change-communication` |
| E — System gap | Route to contribution workflow | `contribution-workflow` |
| Unclassified | Ask the team the question that would classify it | — |

## Step 4b: Version lag, grouped

For drift classified as B, group the instances by the release that introduced the change (read the system's CHANGELOG or git tags between the consumer's installed version and the latest). For each group say three things, all from evidence: how many files in the consumer are affected (count them); whether the change is mechanical (a rename or prop swap a codemod could do) or structural; and whether the release shipped a migration guide. A breaking release with no migration guide is a governance finding in its own right; flag it separately. Don't estimate hours or T-shirt sizes; the count of files and the mechanical/structural call are what the team needs to plan.

## Step 4c: Cross-system drift (only when more than one system is in scope)

If the user has put two or more design systems in scope (brand systems, platform systems), also compare them to each other: shared primitives that no longer agree, the same semantic name resolving to different intents, and same-named components with different APIs. Skip this step, and say so under Scope, when a single system is in scope.

## Step 5: Produce the drift report

Open with a headline sentence. Example: "Drift is moderate and mostly accidental — 3 components have diverged from the system, and 2 of those look like the team didn't know the system version existed. Here's the full picture."

---

### Drift detection report

**Date:** [date]
**Subject:** [what was assessed]
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
| DF-01 | [repo path:line, or Figma node id; and the component] | [visual/behavioural/API/token] | [A–E / Unclassified] | 🔴/🟠/🟡/⚪ | [specific description: the system value and the consumer value] | [specific action] |

Location is evidence, not a label: a file and line the reader can open, or a Figma node. A finding with no location is a suspicion, and goes in the Unclassified list with the question that would confirm it.

**Severity key:** 🔴 Critical · 🟠 High · 🟡 Medium · ⚪ Low (rubric in Step 4a)

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

**Unclassified — needs team input**
List findings with the question that would classify each.

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
6. Unclassified findings: put the open questions to the owning teams

---

**Scope**
- **Inspected:** [repos, packages, Figma files, and versions actually read]
- **Not inspected:** [products or sources out of reach, and therefore not commented on]
- **How "none found" was checked:** [e.g. the token-drift search's positive control — omit if the report makes no absence claims]
- **Assumptions:** [anything taken as given rather than verified]

End with the closing note below.

---

## Step 6: Visual drift comparison (when Figma Console MCP is available)

If the Figma Console MCP from Southleft is connected (check for `figma_capture_screenshot` and `figma_get_component_for_development` tool availability), enhance the drift report with design-side visual evidence.

**Capture design reference:** Use `figma_capture_screenshot` to capture the current state of each drifted component as it appears in Figma. This uses the plugin's `exportAsync` API, which captures the live state — not a cached cloud render. The result is the design-side truth for visual comparison.

**Capture the design spec:** Use `figma_get_component_for_development` to get dev-optimised design data alongside a rendered image. This is still the design side — it gives you the spec in a form that maps to implementation properties, not the implementation itself. For the implementation side, use a Storybook or Chromatic snapshot where one exists, or describe the code.

**Visual diff in report:** For each visual or API drift finding (any class), include the Figma screenshot alongside the implementation snapshot or a description of what the code renders. This gives the reader a visual understanding of the gap, not just a textual description of property mismatches.

**When the standard Figma MCP is connected (read-only):** Screenshots via REST API are available but reflect the last-published cloud state, not the current live state. Note this limitation — if the Figma file has unpublished changes, the screenshot may not reflect the latest design intent.

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This analysis identifies where implementations differ from the system — it cannot always tell why. The classification system (intentional, accidental, version lag, misunderstanding, system gap) is a starting point. If any instance is misclassified, let me know — your corrections make future drift checks more accurate. The goal is to distinguish the drift that needs fixing from the drift that needs documenting.

---

## Quality checks

- Every finding has a classification and a recommended action, not just a description
- Every finding has a location the reader can open (file and line, or Figma node)
- Token-dimension findings come from token-compliance's table, not a second search; the report cites its IDs
- The run stopped, with a redirect, if no consuming product was in scope
- Severity ratings are justified by the specific impact, not assigned generically
- Root cause patterns section exists and adds something beyond the individual findings list
- System gap findings are distinguished from mistakes — product teams whose divergence filled a genuine system gap should not be treated as having done something wrong
- The report distinguishes between drift that should be corrected and drift that should be documented as accepted divergence
- If visual comparisons were captured, each finding includes the Figma reference screenshot
- Every A, C or D classification cites the evidence its rule requires; anything else is Unclassified
- The Scope block and the closing note about intentional deviations are present
