---
name: component-audit
description: "Deep audit of a component library: inventory, usage, duplication, complexity, coverage gaps. Triggers: audit my components, unused components, what components do I have, assess my library. Not for a whole-system view (system-health) or AI index files (codebase-index)."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(npm view:*)
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/component-bestiary-reference.md
  - ../../knowledge-notes/output-discipline.md
---

# Component audit

A skill for auditing a design system's component library across four dimensions: usage signals, complexity distribution, duplication, and coverage gaps. Produces an inventory with tiered findings and a prioritised action list.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Component libraries accumulate silently. New components arrive through contributions. Old components persist because nobody wants to be the one who removes them. Variants proliferate because each edge case adds one more. The result is a library that grows in mass without growing proportionally in value.

A component audit brings the library back into focus: what is there, what is used, what duplicates what, and what is missing that teams have been building around. It is the maintenance work that makes the next year of development faster.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `system.framework` — pre-selects framework-specific inventory guidance
- `system.component_count` — pre-populates the small-system gate
- `severity.*` — finding severity overrides
- `integrations.*` — component data sources (see below)
- `recurring.*` — comparison with the previous audit

## Auto-pull integrations

**Figma MCP** (`integrations.figma.enabled: true`):
- Read the published library from `integrations.figma.file_key` via Figma MCP
- Extract the component inventory: names, variant counts, description status
- Figma library analytics (detach and insertion counts per component) are available only through the REST Library Analytics API on an Enterprise plan. If the team has it, pull detach rates; if not, say so and don't list detach rates as a signal
- Cross-reference the Figma inventory against the code inventory to detect components that exist in design but not in code (or vice versa)

**npm registry** (`integrations.npm.enabled: true`):
- Pull download statistics for `integrations.npm.package_name` (or each package in `integrations.npm.scoped_packages` for monorepos) using `npm view [package] --json` or the npm registry API
- Use download trends (last 30 days, last 90 days) as a usage signal in Dimension 1
- For monorepos: note that per-package downloads are unreliable (see monorepo handling) — use as a directional signal only

**Storybook** (`integrations.storybook.enabled: true`):
- Fetch the story index from `integrations.storybook.url/index.json`
- Extract component list, story counts per component, and documentation status
- Components with zero stories are likely undocumented — flag in Dimension 1

**GitHub** (`integrations.github.enabled: true`):
- Use `gh api search/code` to find consuming repositories that import each component, then read or clone those repos to count (see the note's GitHub caution)
- Pull PR activity for the component library — no PRs in 12+ months is a maintenance signal, not evidence the component is unused
- Pull open issues tagged with component names to surface known problems

**Documentation platform** (`integrations.documentation.enabled: true`):
- If platform is `zeroheight`: use the Zeroheight API to pull page list and last-updated dates per component
- If platform is `supernova`: use the Supernova API to pull component documentation coverage
- If platform is `storybook`: same as Storybook integration above (docs tab status)
- Map documentation coverage to the component inventory — components without docs pages are flagged in Dimension 3

## Step 0: Identify what you're looking at

Before auditing components, determine what kind of shared UI this is. The library type changes which dimensions matter and how findings should be framed.

**Classify from codebase signals:**

- **Design system** — Full template applies. All four audit dimensions (usage, complexity, duplication, coverage) plus composition graph and AI readiness.
- **Component library** — Focus on complexity distribution, duplication, and coverage gaps. Usage signals may not exist yet — note this rather than flagging it as a problem. Skip AI readiness unless the team has signalled interest.
- **Pattern library** — Focus on duplication and documentation completeness per pattern. Complexity distribution is less meaningful because patterns are reference implementations, not consumed packages. Coverage gaps should be framed as "patterns your team builds frequently but hasn't documented" rather than "components missing from the system."
- **Utility collection** — Focus on duplication and naming consistency. A utility collection with overlapping helpers is actively harmful; one with clear, non-overlapping utilities is doing its job. Skip coverage gaps — a utility collection is not trying to be comprehensive.

**Include the classification in the report header** as "Library type: [Design system / Component library / Pattern library / Utility collection]" and skip dimensions that don't apply.

---

## Step 1: Gather the component inventory

Ask for or confirm (skip questions already answered by auto-pull):
- Access to the component library: Figma library, Storybook, npm package, or component documentation
- The framework and component format: React (JSX/TSX), Vue SFC (`.vue`), Twig/Fractal (`.twig`), Svelte (`.svelte`), or Web Components
- Whether this is a monorepo or single-package library (see monorepo handling below)
- Any usage data available: adoption signals, access logs, consumer surveys, or engineering usage stats
- Any known problem areas: components teams avoid, components with open bug reports, components that frequently generate support questions

If usage data is not available, the audit focuses on structural assessment rather than usage analysis. Note in the output which findings are based on direct analysis and which are inferred from structure.

**Small-system note (fewer than 5 components):** With 1–4 components, the audit shifts from pattern detection to per-component deep dive. Skip complexity distribution analysis (Step 3, Dimension 2) — it is not meaningful at this scale. Instead, focus on: completeness of each component's API and state coverage, documentation status per component, and whether the system covers the team's highest-frequency needs. The coverage gaps dimension (Step 3, Dimension 4) becomes the most valuable — what common patterns are teams building locally because the system does not yet provide them? The answer to that question is the system's roadmap.

## Step 1b: Record which usage signals exist

Don't ask the user to choose signals; record which ones are actually in reach, then say what the usage assessment can and can't claim:

- **Code imports** — the one signal that is almost always available: count imports of each component across the repos in reach (with a positive control on a component you know is used). In a design system repo with no consumers checked out, this counts nothing useful; say so
- **Figma instantiations and detach rates** — Enterprise Library Analytics only
- **npm downloads** — direction only, and unreliable for monorepos (below)
- **Support tickets, surveys, production analytics** — only if the user hands them over; never say a team was surveyed unless the user did the survey

If none is in reach, the audit is structural: every component's usage status is "Unknown", the report says so once at the top, and Dimension 1 is skipped rather than filled with inference. If no component source, Figma library or Storybook index is in reach either, stop and ask where the components live; an inventory can't be built from a description.

**Monorepo handling:**

Monorepo structures break standard usage signals. A component published as `@system/button` in its own package may show high npm downloads while `@system/date-picker` shows low — but the download count reflects bundling behaviour, not actual component usage by teams. Apply these adjustments:

- **Per-package download counts are unreliable.** In monorepos, teams often install the umbrella package or a subset of packages. Use import analysis across consuming products instead of download counts where possible.
- **Detect versioning patterns:** Components with `-next` or `-v2` suffixes (e.g. `button-next`, `DataTableV2`) indicate in-flight migrations. Count both versions but flag the pair — the older version is a deprecation candidate, the newer is not yet fully adopted. Neither version's usage number is accurate in isolation.
- **Classify private vs. public components:** Components with underscore prefixes (`_InternalBase`, `_LayoutHelper`), components in directories named `internal/`, `private/`, or `utils/`, and components not re-exported from the package's public barrel file (`index.ts`) are internal implementation details. Exclude them from the public component count and from coverage gap analysis. Count them separately as "internal utilities."
- **Distinguish utility components from user-facing components:** Layout primitives (`Box`, `Stack`, `Flex`, `Grid`, `VisuallyHidden`, `Portal`) are infrastructure components, not user-facing UI. They should be counted in the inventory but categorised separately. A library with 30 components where 15 are layout utilities and 15 are UI components has a different health profile than one with 30 UI components.

**Framework-specific inventory notes:**

- **Vue SFC:** Each `.vue` file in the components directory is typically one component. Check for `<script setup>` vs Options API — mixed patterns across the library are a consistency finding.
- **Twig/Fractal:** Components are organised by Atomic Design convention (`01-atoms/`, `02-molecules/`, `03-organisms/`). The Fractal config (`fractal.config.js`) defines the component engine and paths. Each `.twig` file with an associated `.config.yml` or `.config.js` is a component.
- **Emotion/CSS-in-JS:** Components may be split across multiple files (`Component.tsx` + `styles.ts`). Count by exported component, not by file. Monorepo packages like `@system/core` may contain dozens of components in subdirectories.

## Step 2: Build the inventory

Create a working inventory of all components:
- Component name
- Category (navigation, form, feedback, layout, data display, etc.)
- Variants/configurations available
- Last updated (if accessible)
- Known usage status (actively used / unknown / suspected unused)
- Documentation status (complete / partial / none)

If the inventory does not yet exist, building it is Step 1 of the audit and may be the most valuable output in its own right.

## Step 3: Audit across four dimensions

### Dimension 1: Usage signals

Assess what usage data is available and what it suggests.

Direct signals (if available):
- Import counts across consuming repos (the Step 1b positive control applies)
- npm download stats or package consumption data (direction only)
- Figma library detach rates, if the team has Enterprise Library Analytics
- Support channel questions and frequency, if the user supplies them

Indirect signals (structural inference):
- Components with no documentation are less likely to be found and used
- Components with naming that diverges from the system's conventions may have been added before conventions were established — often early experiments that were never removed

For each component, assign a usage status: Actively used / Likely used / Unknown / Likely unused / Confirmed unused

"Confirmed unused" needs two things: a positive control (the same import search finds a component you know is used, including aliased and namespace imports), and coverage of every consuming repo — or usage data that spans them. If either is missing, the ceiling is "Likely unused", and the report says which consumers weren't checked. A design system repo with no in-repo consumers of a public component tells you nothing about product usage.

Flag all "Likely unused" and "Confirmed unused" for the action list.

### Dimension 2: Complexity distribution

Assess the distribution of component complexity across the library.

**Foundational components** — primitives that serve as building blocks. Buttons, inputs, checkboxes, typography elements, icons. These should make up the largest portion of the library.

**Compound components** — compositions of foundational components. Cards, modals, dropdowns, navigation bars. These should be fewer than foundational components.

**Feature components** — components with significant built-in logic or high specificity to a particular product context. These are the category most likely to proliferate and least likely to be reusable.

Report the count at each level. Then flag, with the numbers:
- Feature components outnumber foundational ones — the system has accumulated product-specific work that belongs locally
- Compound components outnumber foundational ones — missing foundational pieces that teams have compensated for by building up rather than down
- A component whose prop count is more than twice the median for its level — outlier complexity usually means a component doing several jobs

### Dimension 3: Duplication

Find components that solve the same problem with different implementations.

Look for:
- Multiple components with overlapping use cases (e.g. `Toast`, `Snackbar`, and `Alert` all in the same system without clear distinctions)
- Components that are effectively variants of another component rather than distinct components
- Multiple components with names that suggest similar roles (`Modal` and `Dialog`, `Popover` and `Tooltip` — flag these for disambiguation even if they are genuinely distinct, because the distinction needs to be explicit)

For each duplication finding: describe what overlaps, note whether the components are genuinely distinct or redundant, and recommend either documenting the distinction or deprecating the redundant one.

#### Deduplication decision rubric

For each potential duplication finding, use this worksheet to make the decision systematically:

**For each pair of overlapping components (Component A and Component B):**

1. **Problem definition:**
   - What problem does Component A solve? (Be specific: e.g., "Transient feedback to user actions" vs. "Persistent notifications")
   - What problem does Component B solve?
   - Are these the same problem or different problems?

2. **If the problems are the same:**
   - Which component has the better API? (More intuitive prop names, fewer required props, easier to configure the common case)
   - Which has better accessibility? (Keyboard navigation, ARIA attributes, focus management, semantic HTML)
   - Which has wider adoption across consuming teams? (Only if Step 1b found a usage signal; otherwise decide on the first two and say adoption wasn't checked)
   - **Decision:** Keep the component that is strongest across these dimensions. Deprecate the other with a migration path.

3. **If the problems are different:**
   - Document the distinction explicitly in both components' descriptions. The distinction needs to be clear enough that a new team member chooses correctly without asking for help.
   - Flag if the names could be clearer (if they still suggest similarity, rename one or both for clarity).

In the audit output, give only the decision per pair and the one or two reasons that decided it — not the worksheet itself.

### Dimension 4: Coverage gaps

Identify common patterns that teams regularly need but the system does not provide.

Sources for gap identification:
- Components that appear in consumer codebases but not in the system (drift detection is a more focused version of this analysis)
- Patterns referenced in design documentation or prototypes that have no component equivalent
- Common UI patterns (date pickers, data tables, drag-and-drop, infinite scroll) that the system lacks
- Components that are present but lack key variants or states that teams consistently add locally

For each gap: assess whether it is a genuine system gap (the need is common enough to belong in the system) or a local need (one team's requirement that is appropriately local).

#### Tie-in to drift detection: Coverage gaps as system signals

Coverage gaps identified in this dimension often correspond to **Classification E (system gap)** findings in drift-detection. If running both skills in the same session:

- Cross-reference coverage gaps identified here against drift detection findings
- A coverage gap that already has drift evidence is a stronger candidate for system addition than one identified structurally alone
- For example: if the component audit flags "date picker" as a gap, and drift-detection finds three products with local date picker implementations, that is stronger evidence than the gap alone
- Document this cross-reference in the action list: which gaps have supporting drift evidence, and which are identified from structural assessment only

This connection improves prioritisation — gaps with drift evidence indicate teams are already solving the problem locally, which raises the urgency of system provision.

## Step 3b: Composition dependency graph

Build a dependency graph of component composition relationships. This is the blast-radius view for component changes.

**Where the graph comes from.** `codebase-index` is the graph's only producer; it writes `uses`/`usedBy` edges and token bindings to `.ai/index/` with the commit they were computed at. If `.ai/index/` exists and its commit matches `HEAD`, read it. If it's missing or stale, run `codebase-index` first (it is read-only and quick) and then read it. Don't build a second graph by hand here: two graphs built two ways disagree, and the reader can't tell which to trust. When the codebase isn't accessible at all (Figma-only or a manual inventory), say so, skip this step, and list it under "Not inspected". What this step adds is the analysis below.

**For each component, identify:**
- **Composes** — which other system components does this component render internally? (e.g., `Card` composes `Text`, `Button`, `Icon`)
- **Composed in** — which other system components render this component? (e.g., `Icon` is composed in `Button`, `Card`, `NavItem`, `Alert`)
- **Fan-in count** — how many other components depend on this component? High fan-in = high blast radius for breaking changes
- **Fan-out count** — how many other components does this component use? High fan-out = high coupling, fragile to upstream changes

**Identify critical path components:**
- Root components (fan-in of 0) — no other system component renders them. Normal for public components that products use directly; changes don't propagate inside the library
- Leaf components (fan-out of 0) — they render no other system component. Changes upstream don't reach them
- Foundation components (fan-in of 5+) — changes propagate widely; these are the system's load-bearing primitives
- Hub components (high fan-in AND high fan-out) — these are integration risks; they both depend on many things and are depended on by many things
- Standalone components (fan-in 0 and fan-out 0) — both root and leaf. Never a removal signal on its own; only usage evidence from Dimension 1 can make a component a removal candidate

**Token-to-component dependency:**
- From the index's token bindings, identify shared token hotspots: tokens bound by many components in this repo are the most dangerous to change. Give the count; don't pick a threshold, since a 12-component library and a 200-component one differ

**Answering "if I change X, what breaks?"** The graph should be queryable. For any component or token, the report should make it possible to trace: (1) direct consumers — components that import/compose this component, (2) indirect consumers — components that compose the direct consumers, and (3) product-level impact — if integration data is available, which products/teams are affected. Example: "Changing `Icon` directly affects 14 components (Button, Card, NavItem, Alert, ...). Indirectly affects 23 components through Button alone. Products affected: Checkout (12 Icon instances), Dashboard (34 instances), Mobile (8 instances)."

Include the composition graph as a section in the report. For systems with 20+ components, produce a summarised version (top 10 highest fan-in, all hub components, standalone components) with the full graph available as a supplementary output.

## Step 3c: AI readiness and maturity stage

Neither is assessed here. AI readiness is `system-health`'s sixth dimension, judged against the six-dimension checklist in the ai-readiness note; the maturity stage is inferred by system-health from evidence across all dimensions. If a system-health report exists, cite its AI-readiness status and stage in the summary. If not, list both under "Not inspected" and suggest system-health. One audit judging one slice of the system with a different yardstick is how the two reports came to disagree.

## Maturity stage

This audit doesn't assign a maturity stage — one dimension of the system isn't enough evidence. If the user asks, point them to system-health, which infers the stage from evidence across all dimensions.

## Step 4: Produce the audit report

---

### Component audit report

Open with a headline sentence that tells the reader the overall state and where to focus.

**Date:** [date]
**Library type:** [Design system / Component library / Pattern library / Utility collection]
**Library size:** [total component count, public and internal counted separately]
**Audit method:** [direct inspection / structural inference / combined]
**Usage signals used:** [from Step 1b]

---

#### Summary

One paragraph. What is the library's overall condition? What is the most significant finding across the four dimensions?

---

#### Inventory summary

| Category | Count | Actively used | Unknown | Likely/confirmed unused |
|---|---|---|---|---|
| Navigation | | | | |
| Forms | | | | |
| Feedback | | | | |
| Layout | | | | |
| Data display | | | | |
| Other | | | | |
| **Total** | | | | |

---

#### Findings by dimension

Findings formatted as: ID, severity, component or category, evidence (the export's file and line, or the component directory, plus the import count or signal the finding rests on), finding description, recommended action. For duplication, give the decision per pair (Step 3, Dimension 3).

**Severity rubric:**
- 🔴 **Critical** — two exported components solve the same problem with different APIs and nothing documents which to use; or a component marked for removal is composed by other system components
- 🟠 **High** — a duplicate pair with no documented distinction; a coverage gap with drift evidence (local implementations in consuming repos); a feature component carrying product logic in the shared library
- 🟡 **Medium** — a complexity outlier (prop count over twice its level's median); names that suggest overlap between components that are distinct; a public component with no documentation
- ⚪ **Low** — internal utilities miscategorised as public; a standalone component with no usage signal either way

A finding with no evidence column isn't a finding; it goes under "Not inspected" with what would be needed.

---

#### Composition graph (design systems, when source is available)

Top 10 by fan-in, hub components, standalone components, and shared token hotspots (Step 3b). State the method used to build the graph. Full graph as a supplementary output for 20+ components.

---

#### AI readiness and maturity stage

One line: cited from a system-health report if one exists, otherwise "not inspected here; run system-health".

---

#### Action list

Prioritised:

**Immediate:**
- Components to consider for deprecation (Confirmed unused per the rule in Dimension 1, with no migration risk)
- Duplicates to resolve

**Planned:**
- Documentation gaps to address
- Coverage gaps to assess for contribution

**Review:**
- Components with unknown or "Likely unused" status (need usage data from consuming repos before action)
- Feature components that may belong locally

---

**Scope**
- **Inspected:** [files, directories, or data sources actually read]
- **Not inspected:** [what was out of reach, e.g. consuming product repos, Figma analytics]
- **How "none found" was checked:** [for any unused or "no consumers" claim, the positive control and which repos were covered — omit if the report makes no absence claims]
- **Assumptions:** [anything taken as given rather than verified]

End with the closing note below.

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit sees your component library — it does not see the product decisions, team constraints, or historical context behind it. Some findings may flag patterns your team chose deliberately. If any finding describes an intentional decision, let me know — I'll exclude it from future runs and learn your system's conventions. The goal is to surface problems you haven't seen yet, not to second-guess choices you've already made.

---

## Quality checks

- Inventory is complete — no components are described generically ("there are many button variants") without being enumerated
- Usage status is based on available signals, not assumed; no "Confirmed unused" without a positive control and coverage of consuming repos; no survey, ticket or analytics figure appears unless the user supplied it
- Every finding has evidence (file and line, or directory, plus the signal it rests on) and a severity from the rubric
- Duplication findings distinguish between genuinely overlapping components and components that are distinct but similarly named
- Coverage gaps are assessed for whether they belong in the system, not just listed
- Action list prioritises by impact, not by ease
- The Scope block and the closing note about intentional deviations are present
