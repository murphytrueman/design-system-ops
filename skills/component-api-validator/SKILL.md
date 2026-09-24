---
name: component-api-validator
description: "Audit prop APIs across a component library: naming consistency, boolean/default patterns, type coverage, exported types, breaking changes between versions. Trigger: component API audit, are our props consistent, prop naming review. For semver calls use version-bump-advisor."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(npm pack:*), Bash(npx react-docgen-typescript:*), Bash(npx custom-elements-manifest:*), Bash(npx vue-component-meta:*)
references:
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/output-discipline.md
---

# Component API validator

A skill for auditing the public API surface of a component library — prop naming consistency, type coverage, default value patterns, breaking change detection, and alignment with the design-to-code contract. Treats the component API as infrastructure: the public contract that consuming teams depend on.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

A component library's most important output is not its visual rendering — it is its API. The props, types, defaults, and composition patterns form a contract with every consuming team. When that contract is inconsistent (some components use `variant`, others use `type`, others use `appearance` for the same concept), unclear (prop types are `any` or undocumented), or unstable (breaking changes ship without versioning), consuming teams lose trust. And when trust erodes, teams start wrapping system components in local abstractions, which is the beginning of drift.

API validation is not about enforcing a single naming convention. It is about detecting where the library's public surface is working against the teams consuming it. A library where every component follows the same patterns for sizing, variants, event handlers, and composition is a library that teams can learn once and apply everywhere. A library where each component invents its own conventions is a library that requires re-learning for every component.

This skill evaluates the API surface as a whole — not one component at a time, but the patterns that emerge across the library. Individual component reviews are useful but miss the cross-library inconsistencies that frustrate consumers most.

**Do NOT use this skill for:** deciding the semver bump for a release (use version-bump-advisor) or checking one component against its design spec (use design-to-code-check).

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `system.framework` — determines the prop extraction method
- `system.styling` — styling approach
- `severity.api_*` — overrides for API finding severity
- `integrations.github` — component source (see below)
- `integrations.storybook` — prop metadata (see below)

## Auto-pull integrations

**GitHub** (`integrations.github.enabled: true`):
- Pull component source files from the configured repository if there's no local checkout

**Storybook** (`integrations.storybook.enabled: true`):
- Extract argTypes metadata for structured prop information
- Cross-reference Storybook's prop documentation with source code types

**Figma** (`integrations.figma.enabled: true`):
- Pull component property definitions from Figma
- Cross-reference Figma properties against code props for design-to-code alignment

---

## Step 1: Gather component sources

Read before asking. `package.json` gives the package name, `version`, `exports`, `main` and `types`; the entry point gives the public component list; `tsconfig.json` or the presence of `.d.ts`, PropTypes or JSDoc gives the typing approach; the framework shows in the dependencies. Confirm what you found in one line and ask only for:

1. **Previous version source** (optional) — for breaking change comparison. Prefer the published type declarations of the previous release (`npm pack <pkg>@<prev>` and read its `.d.ts` files, or an api-extractor report); a git tag or release branch works if nothing was published
2. **Deliberate exceptions** — legacy names kept for compatibility, so they're reported as accepted rather than as deviations

If no component source is in reach (no path, no checkout, no package to unpack), stop and ask for one; an API audit of described components produces guesses.

## Step 2: Extract API surface

For each component in the source path:

1. **Identify exported components** — components that are part of the public API (exported from index files or package entry points)
2. **Extract props/attributes with the tool that fits, and hand-parse only when none does.** Tool output is complete and consistent; a hand read of forty interfaces is neither.
   - **React with TypeScript:** `react-docgen-typescript` (`npx react-docgen-typescript` or its API) gives name, type, required, default and description per prop from the interfaces. Storybook `argTypes` (from `integrations.storybook`) are the same data if the docs addon is set up.
   - **Vue:** `vue-component-meta` for `<script setup>` and `defineProps`; fall back to reading `defineProps` by hand.
   - **Web Components:** the Custom Elements Manifest (`npx custom-elements-manifest analyze`, or an existing `custom-elements.json`) lists attributes, properties, events, slots and CSS custom properties; it is the standard, so read it rather than re-deriving it.
   - **Svelte:** exported `let` declarations, events, slots (read by hand; note that in the Scope block).
   - **Untyped or PropTypes-only React:** read PropTypes and JSDoc; record every prop with no type as untyped.
3. **For each prop, capture:**
   - Name
   - Type (specific type or `any`/`unknown`/untyped)
   - Required or optional
   - Default value (if any)
   - Description (from JSDoc, TSDoc, or inline comment)
4. **Identify composition patterns:**
   - Does the component accept `children`/`slots`?
   - Does it forward refs?
   - Does it spread remaining props to a root element?
   - Does it accept render props or scoped slots?

## Step 3: Assess cross-library consistency

This is the core of the skill. Evaluate patterns across the entire library, not within individual components.

### 3a. Prop naming consistency

Look for the same concept implemented with different names across components:

| Concept | Consistent pattern | Inconsistent examples |
|---------|-------------------|----------------------|
| Visual variant | All use `variant` | Some use `variant`, others `type`, others `appearance`, others `kind` |
| Size | All use `size` | Some use `size`, others `scale`, others `dimension` |
| Disabled state | All use `disabled` | Some use `disabled`, others `isDisabled` |
| Loading state | All use `loading` | Some use `loading`, others `isLoading`, others `pending` |
| Event handlers | All use `onAction` | Some use `onChange`, others `handleChange`, others `onValueChange` |
| Colour/intent | All use `intent` | Some use `intent`, others `color`, others `severity`, others `status` |

For each inconsistency, report:
- The concept
- Which convention is most common (the likely "correct" one)
- Which components deviate
- Suggested normalisation

### 3b. Boolean prop patterns

Boolean props are a common source of API inconsistency:

1. **Prefix convention** — does the library use `isDisabled` or `disabled`? Pick one, flag deviations.
2. **Negative booleans** — the working convention is that a boolean prop defaults to `false`, so the common case needs no prop. `hideLabel` is the right shape when labels usually show; `showLabel` defaulting to `true` forces `showLabel={false}` at every call site that hides one. Flag a boolean whose default is `true`, and flag a library that uses both forms for the same concept (`hideLabel` on one component, `showLabel` on another). Don't flag a negative name on its own.
3. **Boolean vs. enum** — a prop that started as boolean (`compact`) but should be an enum (`density: 'compact' | 'default' | 'comfortable'`). Flag booleans that limit future extensibility.

### 3c. Default value patterns

1. **Presence** — do all optional props have explicit defaults? Missing defaults are implicit API decisions.
2. **Consistency** — does `size` default to `'medium'` in some components and `'md'` in others?
3. **Sensible defaults** — does `variant` default to the most common use case? Flag surprising defaults.

### 3d. Type coverage

1. **TypeScript/PropTypes completeness** — what percentage of props have explicit types?
2. **Specificity** — are types specific (`'sm' | 'md' | 'lg'`) or vague (`string`)?
3. **Exported types** — are component prop types exported for consumers who need them?
4. **Generic patterns** — if some components use generics (e.g., `Select<T>`), are they consistently applied?

### 3e. Event handler patterns

1. **Naming convention** — `onChange` vs `onValueChange` vs `handleChange`. Identify the library's convention and flag deviations.
2. **Callback signature** — do event handlers pass the event, the value, or both? Is this consistent?
3. **Controlled vs. uncontrolled** — if the library supports controlled components, is the pattern consistent (`value`/`onChange` vs `defaultValue`)?

### 3f. Composition patterns

1. **Children vs. render props** — is the composition model consistent across components?
2. **Ref forwarding** — do all interactive components forward refs?
3. **Prop spreading** — do components spread remaining props? Is this consistent?
4. **Slot naming** (Vue/Web Components) — are slot names consistent across components?

## Step 4: Breaking change detection

If a previous version is available, compare the published type declarations of both versions, not the source. Source can differ from what shipped, and declarations show the whole public surface. Diff the package exports (components, hooks, types, utilities) as well as props — a removed export breaks consumers just as surely as a removed prop.

1. **Removed exports and props** — anything in the previous version's declarations that is gone
2. **Renamed props** — report these as a removal plus an addition, then check whether a deprecated alias for the old name still exists. Without an alias, it is breaking; don't guess at renames from type similarity
3. **Type narrowing** — prop type changed from wider to narrower (`string` → `'a' | 'b'`)
4. **Default value changes** — default changed in a way that alters existing behaviour
5. **Required prop additions** — new props that are required (existing consumers will break)
6. **Behavioural changes** — same prop name but different behaviour (hardest to detect — flag for manual review)

Classify each:
- **Breaking** — consuming code will fail at compile time or behave differently at runtime
- **Potentially breaking** — may break depending on usage pattern (flag for review)
- **Non-breaking** — addition only, existing code unaffected

## Step 5: Design-to-code contract alignment (only with a design source)

Only when a Figma library or exported spec is in reach. Otherwise write "skipped: no design source" under Scope and move on; don't infer design variants from prop names. With a source, cross-reference the API surface against the design-to-code contract:

1. **Prop coverage vs. design spec** — does every design variant have a corresponding prop? Are there props with no design equivalent (engineering-added functionality)?
2. **State coverage** — does the API support every prop-driven state in the spec (disabled, loading, error, selected)? Hover, focus, and active are CSS/interaction states, not props — don't flag them as missing props
3. **Token alignment** — do any props accept raw values (colours, spacing) that should reference tokens?
4. **Accessibility props** — are `aria-*` attributes passed through to the underlying element? Do icon-only variants require an accessible label (e.g. a required `aria-label` or `label` prop in the type for the icon-only case)? A consumer-settable `role` prop is not required, and usually a smell

## Step 6: Produce the validation report

```
# Component API Validation Report

[Headline sentence: the most important API problem and how widespread it is]

## Executive Summary
[Library name, component count, framework, TypeScript coverage, headline findings]

## API Inventory
| Component | Props | Typed | Required | Optional | Defaults | Description coverage |
|-----------|-------|-------|----------|----------|----------|---------------------|
[One row per component]

## Cross-Library Consistency

### Prop Naming
[Table of concept → dominant convention → deviations → ✅ PASS / ⚠️ WARN / ❌ FAIL per pattern]
[Counts, e.g. "14 of 19 components use `variant`; 4 use `type`; 1 uses `appearance`" (illustrative)]

### Boolean Patterns
[Findings: negative booleans, boolean-should-be-enum, prefix inconsistency]

### Default Values
[Findings: missing defaults, inconsistent defaults]

### Type Coverage
[Overall: X of Y props explicitly typed]
[Breakdown: full TypeScript / JSDoc / PropTypes / untyped per component]

### Event Handlers
[Convention identified, deviations listed]

### Composition Patterns
[Ref forwarding coverage, children vs render props consistency, slot naming]

## Breaking Change Analysis
[If previous version available]
| Change | Component | Prop | Type | Impact |
|--------|-----------|------|------|--------|
[One row per change]

## Design-to-Code Contract
[Findings: design variants without props, props without design equivalents, missing state coverage]

## Findings Summary
| ID | Severity | Component | Prop | Evidence | Finding | Remediation |
|---|---|---|---|---|---|---|
| AV-01 | 🟠 High | Badge | `type` | `src/components/Badge/Badge.tsx:12` | 14 of 19 components use `variant`; Badge uses `type` for the same concept | Rename to `variant`, keep `type` as a deprecated alias for one minor |

Severity: 🔴 Critical for a breaking change that shipped without a major, or `any`/untyped on a public prop of an interactive component; 🟠 High for one concept named two ways across the library, a missing exported prop type, or a required prop with no description; 🟡 Medium for inconsistent defaults, missing descriptions, or a boolean that should be an enum; ⚪ Low for style (prefix conventions, slot naming). Evidence is the file and line of the prop's declaration, or the `.d.ts` line when comparing versions.

## Prioritised Recommendations
[Grouped: 🔴 Critical (breaking/type safety) → 🟠 High (consistency) → 🟡 Medium (documentation) → ⚪ Low (style)]

**Scope**
- **Inspected:** [source paths, entry points, declaration files, previous version compared against]
- **Not inspected:** [components not exported from the entry point, runtime behaviour, packages out of reach]
- **How "none found" was checked:** [e.g. "no breaking changes" — both versions' `.d.ts` exports were diffed and the diff did pick up the props added in this release]
- **Assumptions:** [e.g. the entry point defines the public API]

If any of these inconsistencies are deliberate (a legacy name kept for compatibility, a convention you've chosen on purpose), tell me and I'll treat them as accepted in future runs.
```

---

## Quality checks

Before delivering the report, verify:

1. **Every exported component is included** — no components skipped
2. **Cross-library patterns are identified** — the report doesn't just list individual component issues but identifies library-wide patterns
3. **Consistency is counted, not scored** — not "some props are inconsistent" or a percentage rating, but "14 of 19 components use `variant`, 4 use `type`, 1 uses `appearance`"
4. **Breaking changes are correctly classified** — removals are breaking, additions are non-breaking, type changes depend on direction
5. **Fix suggestions include the specific rename or type change** — not "make this consistent" but "rename `type` to `variant` in AlertDialog, Badge, Toast"
6. **TypeScript type coverage is measured per-component** — not just a library-wide average
7. **Findings reference specific component and prop names with a file and line** — never "some components have inconsistent naming"
8. **Props came from tooling where a tool exists** (docgen, component-meta, a Custom Elements Manifest), and the Scope block names which

## Small-system note

For libraries with fewer than 10 components: run the same analysis but present as a single consolidated view. Every finding gets individual attention. Consistency is easier to achieve in a small library — the bar should be 100% consistency, not "mostly consistent."
