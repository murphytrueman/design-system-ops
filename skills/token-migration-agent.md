---
name: token-migration
description: "Plans a token migration (format, tool, naming or tier): chains token-audit, a transformation table, codemod-generator, deprecation-process and change-communication. New names ship with old ones aliased and deprecated; removal waits for a major. Plan only. Invoked by /token-migration."
---

# Token migration

A chained workflow that runs `token-audit`, builds a transformation table, generates codemods with `codemod-generator`, schedules the old tokens' deprecation and removal with `deprecation-process`, and then chains `change-communication` for the announcement and migration guide. Covers format migrations (legacy JSON to DTCG 2025.10), tool upgrades (Style Dictionary 3 to 4, 4 to 5, or to Terrazzo), naming overhauls and tier restructuring. Produces one migration package: transformation table, codemods, a three-stage rollout with entry and exit criteria, and a communication package.

**Output type:** Plan only, with decision points. This agent does not run codemods or change token files. The plan needs human approval before the communication phase and at each stage's entry.

**Run rules:** Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — loading, one inventory, hand-off cards, one report, skipped-permission steps, configuration, and recurring runs. This file holds only what is specific to the migration chain.

---

## When to run this

- Moving token files to DTCG 2025.10
- Upgrading the token build tool (Style Dictionary major version, or to Terrazzo)
- Renaming tokens across the system (a convention change)
- Restructuring tiers or collections
- Any token change that consumers will have to react to

Don't run it for a diagnosis. "What's wrong with our tokens" is `token-audit`. This agent is for when the change is decided and needs to be carried out safely at scale.

---

## The rollout model

Old and new coexist for one release, the old ones are deprecated from the moment the new ones exist, and removal waits for a major. That order matters:

1. **Ship the new tokens and deprecate the old ones together.** The old token becomes an alias of the new one (`{new.path}`), so the two can never resolve to different values, and it is marked deprecated in the source (DTCG `$deprecated: "Use {new.path}"`; a `@deprecated` JSDoc tag on exported token objects; the old custom-property names listed in a Stylelint `declaration-property-value-disallowed-list`). The build warns on every reference to a deprecated token. Codemods ship in the same release, and the migration guide is published with it. This is a minor release: nothing breaks.
2. **Consumers migrate.** They run the codemods, the warnings show what's left, and the count of remaining references per consumer (from `deprecation-process`'s usage audit) is the progress measure.
3. **Remove in the next major.** Delete the aliases. `version-bump-advisor` makes the call; the migration guide already exists.

An earlier version of this agent added deprecation only after every consumer had migrated, which deprecates tokens nothing uses and gives consumers no warning while they still do. Don't reorder the stages.

---

## Configuration and integrations

Configuration and integrations follow the chained-run rules. Specific to this chain:

- `system.tokens` names the token source directories; if it's absent, discovery in `token-audit` Step 0 finds them, and the plan lists the sources it found as a dependency to confirm.
- `integrations.figma`: read Figma variables only if the tools are permitted. Otherwise record the skip under Scope and list Figma as an unverified source in the plan's dependencies. A Figma rename is a coordinated step in Stage 1, never a separate migration.
- `integrations.style_dictionary`: the tool version in use decides the upgrade path and which warning mechanism applies.

---

## Phase 1: Prepare

1. **Confirm what is migrating:** format, tool, naming, tier structure, or a combination. Most real migrations are combinations; name each part.
2. **Identify every token source.** This is the run inventory: code files (JSON, YAML, JS, CSS custom properties, Sass), Figma variable collections, build configs and custom transforms. `token-audit` uses it and skips its own discovery.
3. **Count the scale from the files:** tokens, files, consumers found in the repository or named by the user. No estimates of effort or weeks; the plan carries counts and criteria.
4. **Set the assessment date.**

If access is partial, proceed and list the gaps under Scope and in the plan's dependencies.

---

## Phase 2: Diagnose (chain skill)

### Step 1 — Token audit (`token-audit`)

Run the full audit, including its naming checks (token naming is token-audit's job; `naming-audit` covers components and patterns and isn't in this chain). Capture: tier structure, findings by severity, naming findings and the dominant convention, format assessment (DTCG gaps, value shapes, `$type` resolution), and the file inventory.

From the findings, write the **migration scope**: which tokens change, what kind of change each needs (rename, reformat, restructure, move, delete, create), which changes are required for the migration's goal and which are opportunistic cleanups, and the dependencies between them (a rename of a primitive changes every alias that points at it).

---

## Phase 3: Plan

### Step 2 — Classify the migration

Name the primary type and the parts:

- **Format:** legacy JSON or YAML to DTCG 2025.10 (`$value`, `$type`, object value shapes, `$deprecated`, resolvers for theming)
- **Tool:** Style Dictionary 3 to 4 (config and hook API change, `usesDtcg`), 4 to 5, or to Terrazzo
- **Naming:** convention change across tiers
- **Tier:** adding, removing, splitting or merging collections
- **Combined:** more than one of the above; say which part drives the sequence

Record the constraints the classification imposes on the stages (a tool upgrade has to land before a format change the old tool can't read).

### Step 3 — Transformation table

One row per token that changes:

| Current (name, value, file:line, tier) | New (name, value, file, tier) | Change type | Codemod | Risk | Why |
|---|---|---|---|---|---|

Codemod is Yes, Partial or No. Risk is the standard four levels (Critical: a consumer breaks or themes wrong if this is wrong; High: a visible regression; Medium: build noise or a docs gap; Low: cosmetic) with the specific consumer or integration named in Why. Every token in scope appears exactly once; cross-check the table against the audit's inventory.

### Step 4 — Codemods (`codemod-generator`)

Run `codemod-generator` with the transformation table as its context, for every row marked Yes or Partial. Don't write codemods inline. Capture per codemod: coverage (which rows it handles, which remain manual and why), the dry-run command, the test command, and the rollback from the skill's `MIGRATION.md`. Token renames in template-literal CSS (styled-components, Emotion) are the usual manual remainder; say so if it applies.

### Step 5 — Deprecation and removal (`deprecation-process`)

Run `deprecation-process` for the old tokens with the transformation table as the replacement map. Take from it: the usage audit with its `rg` commands and per-consumer counts, the deprecation notice wording, the minimum deprecation window it derives from the usage footprint, and the removal step. Its mapping table is the same as Step 3's; don't maintain two.

### Step 6 — Staged rollout

Each stage has entry criteria, actions, exit criteria, a rollback and a verification method. No durations: the exit criteria say when a stage is done.

**Stage 1 — Ship new, alias and deprecate old (one minor release)**
- Entry: transformation table approved; codemods pass their tests on a dry run
- Actions: add the new tokens; turn each old token into an alias of its replacement; mark old tokens deprecated in the source (`$deprecated` with the replacement path, `@deprecated` JSDoc on exports, disallowed-list for old custom-property names); configure the build to warn on deprecated references; rename Figma variables to match, in the same window; publish the codemods and the migration guide with the release
- Exit: the build resolves every old name to its new value (diff the generated output before and after: values identical, names doubled); warnings fire on a known reference to an old name; the release notes carry the guide
- Rollback: revert the token files and build config; no consumer changed anything
- Verification: the output diff, the warning probe, `token-audit` re-run showing no new findings

**Stage 2 — Consumers migrate**
- Entry: Stage 1 released; consumers notified through `change-communication`
- Actions: consumers run the codemods and fix the manual remainder; the system team tracks remaining references per consumer with the `deprecation-process` usage commands
- Exit: zero references to old names in each consumer that will take the next major, confirmed by the same search that found them in Stage 1
- Rollback: consumer-side `git revert`; old names still resolve, so a partial migration is safe
- Verification: the per-consumer count, CI green in each consumer

**Stage 3 — Remove (next major)**
- Entry: the deprecation window from Step 5 has passed; the Stage 2 count is zero for every consumer in scope, or the remaining consumers have agreed to pin
- Actions: delete the aliases and the deprecation config; `version-bump-advisor` confirms the major
- Exit: old names absent from generated output; a final search finds no references
- Rollback: restore the aliases from git and ship a patch; this is the one stage with a real cost, and the plan says so
- Verification: the output diff, the final search, consumer CI

### Step 7 — The plan document

Executive summary (what, why, counts, risk level); migration type; audit findings that drive the scope; the transformation table sorted by risk; codemods; the three stages with all criteria visible; the deprecation timeline from Step 5; dependencies (tool versions, CI, Figma permissions, consumer minimum versions); success criteria; rollback per stage. Every verification item is a command or a diff, not "check everything works".

**Stop here.** Present the plan and continue only once the user confirms.

---

## Phase 4: Communicate (chain skill)

Once confirmed, chain `change-communication` with the plan as input. It writes the release notes for the Stage 1 minor, the migration guide (from the transformation table and the codemod instructions), the announcement, and the reminder schedule from Step 5's timeline. It reuses the deprecation notice wording rather than rewriting it.

---

## Phase 5: Synthesise

One package: the plan, the communication package, the audit summary cross-referenced to the table, the timeline, success criteria and per-stage rollback. One headline, one Scope block, one closing note, and the provenance footer. Saving follows the chained-run rules.

---

## Quality checks

- Every token in scope has exactly one row in the transformation table, with a file and line for its current state
- Stage 1 aliases and deprecates the old tokens in the same release as the new ones; Stage 3 is a major
- Codemods come from `codemod-generator` and the deprecation schedule from `deprecation-process`; neither is written inline, and there is one mapping table
- No stage carries an estimated duration; each has entry and exit criteria a command can check
- The run stopped for confirmation before the communication phase
- The package opens with one headline, has one Scope block and one closing note, and ends with the provenance footer
- Dependencies name tool versions, CI changes and access needed before Stage 1

---

## Report template

```
# Token migration plan: [name]

[One headline sentence: what is migrating, the risk level, and the first decision needed]

## Executive summary
## Migration type
## Audit findings
## Transformation table
| Current | New | Change type | Codemod | Risk | Why |
## Codemods
## Rollout
### Stage 1: Ship new, alias and deprecate old
### Stage 2: Consumers migrate
### Stage 3: Remove (next major)
## Deprecation timeline
## Communication package
## Dependencies
## Success criteria
## Rollback per stage

**Scope**
[one combined Scope block per output-discipline]

[Closing note]

*Generated by Design System Ops token-migration agent · [date]*
```

---

## Recurring workflow

Loading, saving and pruning follow the chained-run rules. When a previous package exists, add a "Migration progress" section after the headline: the current stage, which exit criteria are met (with the command output that shows it), the per-consumer reference counts against the last run, and any deviation from the plan.
