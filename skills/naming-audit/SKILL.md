---
name: naming-audit
description: "Audit component and pattern naming for consistency and clarity, with rename suggestions. Triggers: naming review, are our component names consistent, fix our naming. Token names: token-audit. Prop names: component-api-validator. Figma variable names: figma-variable-audit."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*)
references:
  - ../../knowledge-notes/output-discipline.md
---

# Naming audit

A skill for auditing naming conventions across a design system's components and documented patterns. Produces a violation report with specific examples, ambiguity flags, and rename suggestions with rationale. Token names are audited by `token-audit`, prop names by `component-api-validator` and Figma variable names by `figma-variable-audit`; this skill cites their findings rather than repeating them.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Naming is the primary interface between a design system and its consumers. A name is the first piece of information a designer or developer gets about what a component does, what a token means, or how a pattern behaves. Good names are predictable: consumers can guess what a name refers to before they look it up. Bad names require lookup, then clarification, then occasionally a conversation to confirm what was meant.

Naming problems accumulate. A single ambiguous component name is an inconvenience. Twenty ambiguous names spread across a library, with some following one convention and others following three others, is a system that new team members cannot navigate and experienced team members cannot trust.

This audit covers naming for components and any documented patterns. It does not mandate a specific naming convention — it assesses whether the naming is consistent, unambiguous, and fit for its purpose.

## Step 0: Identify what you're looking at

Before auditing names, determine what kind of shared UI this is. The library type changes how strict the consistency expectations should be and what recommendations are proportionate.

**Classify from codebase signals:**

- **Design system** — Full audit applies. Naming conventions should be documented, consistent, and enforced. Recommend creating a decision record for any undocumented conventions.
- **Component library** — Naming consistency matters, but the recommendation to "create a decision record" should be scaled down to "write down the convention you're already following, even if it's just a comment in the README." A 5-component library does not need a formal governance artefact.
- **Pattern library** — Naming conventions often follow the documentation tool's conventions (Fractal's folder numbering, Storybook's story hierarchy). Audit against the tool's conventions as well as internal consistency. Pattern names tend to describe what the pattern shows rather than what it does — flag this only if it creates confusion, not as a blanket violation.
- **Utility collection** — Naming is the primary interface. Every utility name needs to be unambiguous and predictable because there's no documentation site to fall back on. The audit should be strict on clarity and lenient on formal convention — a utility called `clamp-width` is better than one called `u-cw` even if the latter follows a prefix convention.

**Include the classification in the report header** as "Library type: [Design system / Component library / Pattern library / Utility collection]" and calibrate recommendation weight accordingly.

---

## Step 1: Gather the name inventory

Pull names from the source before asking:
- **Component names** — the public barrel exports (`index.ts` / `index.js` at the package root, or each package's entry point in a monorepo). Exports are the names consumers actually type; internal files aren't. Fall back to component directories if there's no barrel. Record the file and line of each export: that is the finding's evidence
- **Pattern names** — the docs site or Storybook hierarchy, if documented
- **Existing naming convention documentation** — README, CONTRIBUTING, ADRs
- **Neighbouring reports** — a `token-audit` report (token naming findings) or `component-api-validator` report (prop naming) if either has been run; cite their IDs in the summary rather than re-auditing

Only ask the user for a list if you can't reach the source, and say which names came from where. If no barrel, component directory or docs hierarchy can be found, stop and ask where the components live rather than auditing file names.

If naming convention documentation exists, assess against it. If it does not, derive the implicit conventions from the existing names and note where they are inconsistent with each other.

**Small-system note (fewer than 5 components):** A naming audit on a system this size is more of a naming workshop than a compliance audit. The consistency check (Step 2) becomes trivial — with 1–4 components, either every name follows the same convention or the inconsistencies are immediately visible. Focus the audit on purpose clarity and ambiguity flags rather than pattern detection. Offer to capture the convention as a decision record (`decision-record`) now, while the system is small enough to rename without migration cost.

## Step 1b: Derive the dominant convention

If no naming convention documentation exists, don't stop to establish one first. Derive the dominant convention from the inventory — the pattern most names already follow — and show it in the report's convention inventory so the team can confirm or correct it:

- **Components:** casing, specificity direction (`ButtonPrimary` vs `PrimaryButton`), abbreviation use, prefix/suffix rules
- **Patterns:** whether names describe the user's task (`Sign in`, `Filter a list`) or the components involved (`Form with validation`), and whether the docs tool's hierarchy is followed

Audit against that derived convention, and say it's derived. Where no convention dominates, report that as the finding rather than picking one. At the end, offer to capture the convention as a decision record using the `decision-record` skill.

## Step 2: Assess component naming

### Consistency check

Are component names following a consistent convention? Identify which conventions are in use:
- Casing: PascalCase, camelCase, kebab-case, or mixed
- Specificity pattern: general-to-specific (`ButtonPrimary`) or category-first (`NavigationPrimary`)
- Abbreviation policy: are abbreviations used, and are they consistent (`Btn` vs `Button`, `Nav` vs `Navigation`)

List the components that break from the pattern the rest of the library follows — worth aligning when they're next touched. Where the difference might be a deliberate naming decision, say so and ask rather than assuming it's an oversight.

### Purpose clarity check

A component name should communicate what the component does without requiring context.

Flag names that:
- Are generic to the point of meaninglessness for what they do: `Wrapper`, `Base`, `Thing`, `Item` on a component with a specific job. Layout primitives are exempt — `Box`, `Stack`, `Flex`, `Grid`, `Container` and `Layout` are well-understood names for general-purpose layout components
- Describe visual treatment rather than function: `BlueCard`, `LargeText`, `RoundedButton`
- Use internal team jargon: names that would not be understood by someone new to the organisation
- Are ambiguous between similar components: `Modal` and `Dialog` in the same system, `Tooltip` and `Popover` without clear distinction

For each flagged name: describe the ambiguity and suggest a rename. The rename suggestion should follow the system's established convention and improve rather than just change.

### Suffix and prefix conventions

If the system uses suffixes or prefixes to indicate category, variant, or role, are they applied consistently?

Common patterns to check:
- Size suffixes: `ButtonSm`, `ButtonMd`, `ButtonLg` — are sizes applied consistently across components?
- State suffixes: `-active`, `-disabled`, `-loading` — are state names consistent across components?
- Category prefixes: `Form-`, `Nav-`, `Data-` — are prefixes applied to all relevant components?

Flag any component that should have a prefix or suffix based on the system's conventions but does not.

## Step 3: Assess pattern naming

Only if the system documents patterns (a docs site section, a Storybook "Patterns" hierarchy, a `patterns/` folder). Skip and say so otherwise.

- **Task versus assembly** — a pattern name should say what the user is doing (`Confirm a destructive action`), not list the parts (`Modal with two buttons`). Flag assembly names only where two patterns would be indistinguishable by their names
- **Consistency with the docs tool** — Storybook hierarchies and Fractal folder numbering impose an order; flag patterns filed outside it
- **Collisions with components** — a pattern and a component sharing a name (`Wizard` the pattern, `Wizard` the component) confuse search and Figma; flag and suggest which one to rename

### Cross-checks with other audits

Token naming belongs to `token-audit`, prop naming to `component-api-validator`. If either report exists, quote the count and IDs of its naming findings in the summary so the reader sees the whole naming picture in one place. If neither exists and the user asked for "all our naming", say which parts this report doesn't cover and offer to run them.

## Step 4: Produce the naming audit report

Open with a headline sentence. Example: "Your component naming is consistent but your token naming has three competing conventions — here's where the friction is."

---

### Naming audit report

**Date:** [date]
**Covers:** [components / patterns / both], plus [token-audit / component-api-validator findings cited, or "not run"]
**Convention documentation:** [exists and used as reference / does not exist — conventions derived from inventory]

---

#### Summary

One paragraph. What is the overall naming quality? Is the inconsistency concentrated (a specific era of the system, a specific team's contributions) or distributed? What is the most important finding? Be direct — if naming is a mess, say so plainly.

---

#### Convention inventory

What naming conventions are currently in use? List the dominant conventions and any divergent conventions found. This section tells the team what they are actually doing, which is the baseline for any improvement.

---

#### Findings

**Component naming violations**

| ID | Component name | Evidence | Issue | Rename suggestion | Severity |
|---|---|---|---|---|---|
| NA-01 | [name] | [export file:line] | [specific issue] | [suggested name] | 🔴/🟠/🟡/⚪ |

**Pattern naming violations** (if patterns are documented)

| ID | Pattern name | Evidence | Issue | Rename suggestion | Severity |
|---|---|---|---|---|---|
| NA-[n] | [name] | [docs path or story id] | [specific issue] | [suggested name] | 🔴/🟠/🟡/⚪ |

**Severity rubric:**
- 🔴 Critical — the name actively misleads: it describes something the component doesn't do, or two exported components share a name
- 🟠 High — ambiguity creates real misuse risk (two components a consumer can't tell apart by name)
- 🟡 Medium — inconsistent with the dominant convention but not misleading
- ⚪ Low — a casing or abbreviation slip with no effect on understanding

---

#### Recommendations

**If convention documentation does not exist:**
Confirm the derived convention with the team and write it down before making naming changes. Without it, rename decisions have no stable reference point and the same inconsistencies will accumulate again.

**Sequencing renames:**
Renaming components and tokens is a breaking change. Recommendations:
1. Fix new additions first — apply the correct conventions going forward
2. Rename in order of severity: high-priority violations before medium and low
3. Use the deprecation process for component renames — the old name should be deprecated with a migration path, not removed immediately
4. Announce renames as breaking changes — see the `change-communication` skill

**Connection to decision-record:** Offer to capture a newly derived or changed convention as a decision record using the `decision-record` skill. It's the governance decision consumers look up most often, so it earns a record, but the offer is the user's to take.

---

**Scope**
- **Inspected:** [barrel exports and docs sources actually read; neighbouring reports cited]
- **Not inspected:** [what was out of reach, e.g. Figma layer names, internal-only components]
- **How "none found" was checked:** [for any "no violations" claim, how the check was shown to work — omit if the report makes no absence claims]
- **Assumptions:** [e.g. the derived convention is the intended one]

End with the closing note below.

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit checks naming patterns against common conventions — it does not know why a name was chosen. Some inconsistencies may be deliberate distinctions. If any finding flags a naming choice your team made intentionally, let me know — I'll learn your conventions and skip those patterns in future runs. The goal is to catch accidental inconsistency, not to override deliberate decisions.

---

## Quality checks

- Every violation has evidence (the export's file and line, or the docs path) and a specific rename suggestion with rationale, not just a flag
- Token and prop naming are cited from their owning skills, never re-audited here
- Rename suggestions follow the system's established conventions — they improve the naming while maintaining consistency
- The convention inventory section describes what the system is actually doing, not what it should be doing
- Severity ratings reflect real impact: a misleading name is high priority, a minor casing inconsistency is low
- The recommendations section addresses sequencing — naming changes are breaking changes and should be treated accordingly
- The Scope block and the closing note about intentional deviations are present
