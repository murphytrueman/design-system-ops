---
name: deprecation-process
description: "Plan a deprecation end to end for a component, token, variant or pattern: usage audit, migration path, timeline to a major-version removal, notices. Triggers: deprecate, sunset, phase out, retire, remove, replace X with Y. Announcing non-deprecation changes: change-communication."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(grep:*), Bash(rg:*)
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/output-discipline.md
---

# Deprecation process

A skill for planning and executing the deprecation of components, tokens, or patterns in a design system. Produces a deprecation plan with timeline, consumer communication, and migration guidance.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Deprecation is the maintenance work that never gets prioritised until it becomes a crisis. Components accumulate. Tokens multiply. Patterns fork. The longer a team waits to deprecate, the more existing usage entrenches, and the more a removal feels disruptive rather than healthy.

A deprecation done well is a contract with consumers: clear notice, a migration path, and a credible timeline. A deprecation done badly is a surprise, and it erodes trust in the system faster than almost anything else.

This skill produces a deprecation plan that is honest about the timeline, specific about migration, and structured to communicate clearly to the teams affected.

---

## Step 1: Identify what is being deprecated

Clarify:
- What is being deprecated? (component, token, pattern, variant, API)
- Why is it being deprecated? (superseded by a better option, unused, causing maintenance burden, design direction change, accessibility non-compliance, etc.)
- What replaces it, if anything?
- Is there a hard removal date in mind, or is this open-ended?

If nothing replaces it: the deprecation plan needs an extra step addressing why the use case should no longer be served and what teams who relied on it should do instead.

## Step 2: Audit current usage

Before writing the plan, understand the exposure. Do not estimate when you can measure.

**Automated usage counting (if codebase access is available):**

Run these searches to produce a measured count rather than an estimate. Search every package root that consumes the system (apps, packages, monorepo workspaces), not just `src/`. Before trusting any count, run the pattern against one file you know uses the item and confirm it matches; if it doesn't, fix the pattern before reporting anything.

The patterns use whole-word matching so `Button` doesn't match `ButtonGroup`, and ripgrep's multiline mode so imports split across lines are caught. Even so, treat every count as a lower bound: dynamic imports, string-built class names and usage in other repositories won't show up. Say so in the summary.

For component deprecation:
```bash
ROOTS="apps packages src"   # every consuming package root in this repo
GLOBS=(-g '*.{ts,tsx,js,jsx}')

# Files that import or re-export it, including multiline and aliased imports
rg -l -U "${GLOBS[@]}" '(import|export)\s+(type\s+)?\{[^}]*\bComponentName\b[^}]*\}\s*from' $ROOTS | wc -l

# Local aliases (`ComponentName as Foo`) — search for each alias's JSX usage too
rg -o -U --no-filename "${GLOBS[@]}" '\bComponentName\s+as\s+\w+' $ROOTS | sort -u

# JSX instances (occurrences, not lines; may exceed files if used several times per file)
rg -o "${GLOBS[@]}" '<ComponentName\b' $ROOTS | wc -l

# Files with any usage (for blast radius mapping)
rg -l -U "${GLOBS[@]}" '\bComponentName\b' $ROOTS
```

For token deprecation:
```bash
# CSS custom properties, including var(--token-name, fallback)
rg -o -g '*.{css,scss,less,ts,tsx,js,jsx}' 'var\(\s*--token-name\s*[,)]' $ROOTS | wc -l

# SCSS variables, without matching $token-name-light
rg -o -g '*.scss' '\$token-name(?:[^\w-]|$)' $ROOTS | wc -l

# JS/TS token references (adjust the path to your token object)
rg -o -g '*.{ts,tsx,js,jsx}' '\b(tokens|theme)\.path\.to\.token\b' $ROOTS | wc -l
```

Use `rg -l … | wc -l` when you mean files and `rg -o … | wc -l` when you mean occurrences, and label the result accordingly. If ripgrep isn't available, `grep -rlE` works for single-line patterns but misses multiline imports; note that in the summary.

**Present the usage count as a structured summary** (numbers below are illustrative):

```
Usage audit: DatePicker
─────────────────────────
Files importing:      23 files
JSX instances:        47 usages
Unique consuming apps: 4 (checkout, dashboard, settings, admin)
Critical paths:       2 (checkout date selection, appointment booking)
Test files with refs: 12
Storybook stories:    3
Documentation refs:   5
─────────────────────────
Total blast radius:   at least 47 instances across 23 files in 4 applications
Searched:             apps/, packages/ (pattern confirmed against a known usage)
```

If codebase access is not available, ask the user to run the search commands and provide the output. If neither is possible, flag the usage audit as outstanding and required before soft removal.

**Per-consumer breakdown:** For each consuming application, produce a row showing (illustrative values):

| Consumer | Instances | Critical path? | Estimated migration effort | Contact |
|---|---|---|---|---|
| Checkout | 12 | Yes (date selection) | Medium (1–3 days) | [team/person] |
| Dashboard | 18 | No | Low (<1 day) | [team/person] |
| Settings | 8 | No | Low (<1 day) | [team/person] |
| Admin | 9 | No | Medium (prop differences) | [team/person] |

This table is the deprecation plan's most operationally useful artifact. It tells the deprecation owner exactly who to contact, how much work each team faces, and where the blockers will be.

Effort tiers, estimated from the prop mapping and any behavioural differences (label them as estimates):
- **Low (< 1 day):** simple find-and-replace, props map 1:1, no behavioural differences
- **Medium (1–3 days):** some prop changes, minor behavioural differences needing targeted testing
- **High (3+ days):** significant API or composition differences; consuming code needs refactoring

**Small-system note (fewer than 5 components):** Deprecating one component when you only have four is removing 25% of the system. The usage audit (this step) becomes mandatory, not optional — the blast radius is proportionally much larger. Consider whether the component should be archived or hidden rather than fully deprecated, since small systems have fewer alternatives and consumers may have no migration path. The communication step should be a direct conversation with every affected team, not a written announcement — with a system this size, you know who is using what.

## Step 3: Write the deprecation plan

---

### Deprecation plan: [component/token/pattern name]

**Item being deprecated:** [name]
**Deprecated in version:** [version number or date]
**Planned removal:** [version or date, or "TBD — see timeline"]
**Replacement:** [name of replacement, or "none — see migration guidance"]
**Owner:** [who is responsible for this deprecation]

---

#### Why this is being deprecated

One to three sentences. Be direct. "This component has a higher-quality replacement that covers all existing use cases and is more accessible" is more useful than "this component has reached the end of its lifecycle."

Include the decision record reference if one exists.

#### What replaces it

If there is a direct replacement: name it, link to it, and describe in one sentence what makes it the right choice for teams currently using the deprecated item.

If there is no direct replacement: explain what teams should do instead. This might be composing from more primitive components, using a pattern that does not require a specific component, or accepting that a particular UI pattern is being retired.

Do not leave this section vague. "Use the updated component instead" without specifics is not a migration path.

#### Migration path decision tree

Not every deprecation has a clean 1:1 replacement. When the replacement does not cover 100% of the deprecated item's use cases, use this decision tree:

1. **Does the replacement cover 80%+ of use cases?**
   - Yes → Proceed with standard deprecation. Document the uncovered use cases in the "Exceptions and edge cases" section with recommended workarounds.
   - No → Go to step 2.

2. **Are the uncovered use cases still valid needs?**
   - Yes → Go to step 3.
   - No → Proceed with deprecation. Document why the uncovered use cases are no longer supported and what teams should do instead.

3. **Can the uncovered use cases be served by a composition of existing components?**
   - Yes → Proceed, and document the composition pattern as part of the migration guide. Consider whether the composition should become a documented pattern (use the `pattern-documentation` skill).
   - No → The deprecation is premature. Extend the replacement to cover the gap, or keep both items until it does; pause the timeline rather than leave teams to build local solutions.

The key principle: never deprecate without a path. A deprecation that leaves teams with no alternative is not a deprecation — it is an abandonment.

#### Migration inputs

The migration guide itself is written once, by `change-communication`, as part of the breaking-change package; this plan supplies what that guide needs, so the two never disagree. Record here:

- **Replacement:** [component, token or pattern], and the cases it doesn't cover (from the decision tree above)
- **Mapping table:** every deprecated prop or token against its replacement, with `[no equivalent]` where there is none

  | Deprecated | Replacement | Note |
  |---|---|---|
  | `<Old size="compact">` | `<New size="sm">` | value rename only |
  | `--color-legacy-teal` | `--color-action-secondary` | resolved values differ: `#0f766e` → `#0d9488` |

- **Behavioural differences to test:** [what changes at runtime, from the source of both]
- **Local overrides to remove:** [known workarounds consumers added for the deprecated item's weaknesses]
- **Help:** a codemod (Step 3, below), a channel, a pairing offer

Then run `change-communication` with this plan; its migration guide goes in the announcement and the docs.

#### Timeline

**Deprecation notice date:** [date]
**Migration support window:** [start – end] — during this period, the design systems team will actively support migration
**Soft removal date:** [date] — deprecated item will generate warnings but remain functional
**Hard removal date:** [date] — deprecated item is removed from the system

Hard removal ships in a major release; use `version-bump-advisor` for the call. Deprecation warnings themselves can ship in a minor.

The minimum deprecation window should be proportional to the usage footprint. A rarely-used internal component might have a four-week window. A foundational component used across dozens of products needs at least one full release cycle, possibly two.

**Timeline visual:**

Include a visual timeline in the deprecation plan output. Use this Mermaid gantt chart format that renders in GitHub, GitLab, Notion, and most documentation platforms:

```mermaid
gantt
    title Deprecation timeline: [Component name]
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Notice
    Deprecation announced           :milestone, m1, [date], 0d
    Teams notified                  :active, notify, [date], 3d

    section Migration
    Migration support window        :active, migrate, after notify, [duration]
    Reminder: 2 weeks to soft removal :milestone, m2, [date], 0d

    section Soft removal
    Warnings enabled, still functional :crit, soft, [date], [duration]
    Reminder: 2 weeks to hard removal  :milestone, m3, [date], 0d

    section Hard removal
    Component removed               :milestone, m4, [date], 0d
```

Replace the bracketed values with the actual dates and durations from the timeline above; where a date isn't agreed yet, leave `[needs data: date]` rather than inventing one. If the team's documentation platform does not render Mermaid, add a one-line text fallback: `Notice [date] → migration support [range] → soft removal [date] → hard removal [date, major version]`.

The visual timeline should be included in both the deprecation plan document and the communication announcement. It is the single most referenced artifact in a deprecation — teams pin it, share it, and check it weekly.

#### Communication plan

Who needs to know, and how will they be told?

- **Immediate notice:** [channels — e.g. Slack #design-system, release notes, direct outreach to high-usage teams]
- **In-system warning:** Add deprecation notice to the component's documentation and, if possible, a code-level deprecation warning in the component itself
- **Follow-up reminders:** Two weeks before soft removal, two weeks before hard removal

The announcement and migration guide are `change-communication`'s output; hand it this plan rather than drafting a second announcement here. This section fixes the channels and the reminder dates that the announcement will carry.

#### Exceptions and edge cases

Are there any known uses that cannot follow the standard migration path? Document them here and note how they will be handled — extended timeline, custom migration support, or accepted divergence.

---

#### Indirect blast radius

Step 2 covers direct usage. Before committing to a timeline, also check:
- Does any other system component compose the deprecated component? Those components need migration too, and they block consumer migration.
- Do any token aliases or theme configurations reference the deprecated item?
- Are there third-party integrations, design tool configurations, or CI pipelines that reference it?

**Codemod recommendation:**
If the migration is a mechanical transformation (rename a prop, swap one component for another with predictable prop mapping), recommend running the `codemod-generator` skill. A codemod that handles most cases and flags the rest for manual review is usually worth producing once usage runs to dozens of instances.

The timeline should be proportional to the blast radius: not just the usage count, but the migration effort in the per-consumer table.

#### Rollback contingency

Document what happens if the deprecation fails:
- Under what conditions would the deprecation be reversed? (e.g., migration proves impossible for a critical consumer within the timeline)
- Can the deprecated item be un-deprecated without data loss or version confusion?
- Is there a version pinning strategy that allows consumers to stay on the old version beyond the hard removal date if needed?

This is not an invitation to avoid deprecations. It is an acknowledgement that infrastructure changes sometimes fail and having a rollback plan is responsible engineering.

## Step 4: Add the deprecation notice to documentation

The deprecated item's documentation page should be updated immediately with:
- A deprecation banner at the top of the page
- A note stating what replaces it and linking to the replacement
- The planned removal date
- A link to this deprecation plan

Do not remove the documentation page until hard removal. Teams often discover deprecations through documentation during unrelated work, and the page needs to be there when they look.

## Quality checks

- A migration path exists for every current use case, or the absence of one is explicitly acknowledged
- The timeline is realistic given the usage footprint
- The communication plan names specific channels, not just "notify affected teams"
- The deprecation notice on the documentation page is ready to publish alongside this plan
- Usage audit has been completed or flagged as outstanding
- Exceptions and edge cases are explicitly documented, not glossed over
