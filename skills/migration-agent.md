---
name: migration
description: "Plans a token migration (format, tool, naming or tier): chains token-audit and naming-audit, builds the transformation table, then codemod-generator, deprecation-process and change-communication for codemods, deprecation and comms. Plan only. Invoked by /migration."
---

# Token migration

A chained workflow that runs token-audit and naming-audit, builds a transformation table and staged rollout plan, generates codemods with `codemod-generator`, plans the deprecation of old tokens with `deprecation-process`, and then chains `change-communication` for the communication package. Covers format migrations, naming overhauls, tool upgrades, tier restructuring, and composite transformations. Produces a migration package with a transformation table, codemods, rollback checkpoints, and verification checklists.

**Output type:** Plan only, with decision points. This agent does not run codemods or change token files. The plan requires human approval before the communication phase and at each rollout stage's entry point.

**Provenance:** The package ends with a one-line provenance footer.

**Run rules:** Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — loading, one inventory, hand-off cards, one report, skipped-permission steps, configuration, and recurring runs. This file holds only what is specific to the migration chain.

---

## When to run this

- Planning a token format upgrade (legacy JSON to DTCG 2025.10)
- Executing a Style Dictionary v3 to v4 migration
- Renaming tokens across the system (convention overhaul)
- Restructuring token tiers or collections
- Coordinating a multi-team token transformation
- Before any large-scale token change affecting consumers

Do not run this agent when you need only a diagnostic. If the question is "what's wrong with our tokens," run `token-audit`. If the question is "are our tokens named correctly," run `naming-audit`. The migration agent is for when you have already identified the problem and need to execute the fix at scale.

---

## Configuration and integrations

Configuration and integrations follow the chained-run rules. Specific to this chain:

- **Token source specification is critical.** The migration plan enumerates sources (code files, Figma variables, or both). Confirm that `.ds-ops-config.yml` specifies `token_sources` — if it does not, the plan notes this as a dependency before rollout.
- **Figma variables** are read only if the Figma tools are permitted; otherwise record the skip in Scope and list Figma as an unverified source in the plan's dependencies.

---

## Phase 1: Prepare

Before running any skill, establish scope and identify sources:

1. **Confirm what is being migrated:**
   - Format only? (JSON → DTCG)
   - Tool only? (Style Dictionary v3 → v4)
   - Naming only? (convention change)
   - Tier structure? (adding/removing/splitting collections)
   - Composite? (multiple of the above)
2. **Identify all token sources** — this is the run inventory; token-audit and naming-audit use it and skip their own discovery:
   - Code file locations (JSON, YAML, JS, CSS variables, etc.)
   - Figma variables (collection name, file URL if applicable)
   - Style Dictionary configs, preprocessors, or custom transforms
3. **Estimate scale:**
   - Total token count
   - Total consumer count (teams, applications, libraries)
   - Estimated files affected
   - Integration points (CI/CD, design tools, documentation generators)
4. **Check `.ds-ops-config.yml`:**
   - Integration list (Figma, Style Dictionary, etc.)
   - Severity settings for violation classification
   - Token source specifications
   - Recurring output directory (for checkpoint tracking)
5. **Set assessment date.** This is the point-in-time snapshot for the migration plan.

If access is partial, proceed and list the gaps in the Scope block and the plan's dependencies section.

---

## Phase 2: Diagnose and scope (chain skills)

Run the two diagnostic skills in sequence, passing a hand-off card between them.

### Step 1 — Token audit (`token-audit`)

Run the full token audit. Capture:
- Tier structure assessment (which tiers are present, which are violations)
- Total violation count by severity
- Format assessment (DTCG gaps, missing $value/$type/$description fields)
- Token file locations and count per file

Carry forward into Step 2: violations that will inform naming audit priorities and any structural issues (missing tiers, orphaned tokens).

### Step 2 — Naming audit (`naming-audit`)

Run the naming audit across tokens and patterns. Capture:
- Convention inventory (what naming patterns are actually in use)
- Violation counts and categories
- Tokens that must be renamed as part of the migration
- Any naming patterns that correlate with violations from Step 1

At this point, combine findings from both audits into a **migration scope document:**
- Which tokens need to change (by violation type)
- What kind of change each requires (rename, reformat, restructure, move, create)
- Which changes are critical vs. optional
- Any dependencies between changes (some tokens depend on others)

---

## Phase 3: Plan the migration

This phase generates the core migration strategy document. Do not skip steps.

### Step 3a — Classify migration type

Determine the primary migration category. Most real-world migrations are composite — multiple types combined. Classify as:

- **Format migration:** Legacy JSON/YAML → DTCG 2025.10 (add $value, $type, $description fields; restructure nesting if needed)
- **Tool migration:** Style Dictionary v3 → v4 (config format change, hook API change, custom transforms deprecated)
- **Naming overhaul:** Convention change across tiers (e.g., legacy.color.* → system.color.*)
- **Tier restructuring:** Adding/removing/splitting/merging collections (e.g., splitting semantic into feedback + state + interaction)
- **Composite:** Multiple of the above

Document the rationale for the classification and any constraints it creates for the rollout stages.

### Step 3b — Transformation specification

For each token that needs to change, produce a row in the transformation table with:
- **Before state:** Exact current name, value, file path, and tier
- **After state:** Exact new name, value, file path, and tier
- **Transformation type:** Rename, reformat, restructure, move, delete, or create
- **Codemod feasibility:** Can this be automated? (Yes/Partial/No)
- **Risk level:** What breaks if this transformation is wrong? (None / Low / Medium / High / Critical)
- **Risk description:** Specific consumers, downstream impact, or integration points

The transformation table is the source of truth for the migration. Every affected token must appear. Cross-reference against the audit outputs to ensure completeness.

### Step 3c — Codemod generation (`codemod-generator`)

Run `codemod-generator` with the transformation table as its migration context, covering every row marked codemod-feasible (Yes or Partial). Don't write codemods inline. Capture for each codemod:
- **Coverage:** how many affected tokens it handles, and which remain for manual work (for example, "80 via codemod, 20 manual")
- **Manual remainder:** the category of tokens it can't handle and why
- **Testing command:** the dry-run command to verify it before committing
- **Rollback:** how to revert it, from the rollback section of the skill's MIGRATION.md

### Step 3d — Staged rollout strategy

All migrations follow a four-stage rollout. (Stages are the rollout; Phases are this agent's own workflow.) Each stage has entry criteria, exit criteria, rollback checkpoint, estimated duration, and verification method.

**Stage 1 — Non-breaking additions**
- Entry: Audit complete, migration plan approved by stakeholders
- Action: Add new tokens alongside old. Both work simultaneously. No consumer changes required.
- Exit: All new tokens exist, resolve correctly in all integration points, no build warnings
- Rollback: Delete new tokens, revert token files to pre-Stage-1 state. No consumer changes to roll back.
- Estimated duration: 1–2 weeks (depends on token count and integration points)
- Verification:
  - All new tokens compile/resolve in token build system
  - Figma variables created (if applicable) and sync correctly
  - Build passes with both old and new tokens in scope
  - No deprecation warnings emitted (they will be added in Stage 3)

**Stage 2 — Consumer migration**
- Entry: Stage 1 complete, new tokens verified in staging, no build errors, all teams notified
- Action: Update all consumers (code, components, docs) to use new token references. Run the Step 3c codemods. Manual cleanup for what codemods miss.
- Exit: No consumer references old token names, no build warnings, all code tests pass
- Rollback: Revert all consumer changes (git reset, git revert), confirm old tokens still resolve. This is a code rollback, not a token rollback.
- Estimated duration: 3–6 weeks (depends on consumer count and codemod coverage)
- Verification:
  - Grep/automated search finds no remaining references to old token names in code
  - All CI pipelines pass (unit tests, integration tests, builds)
  - Figma components updated to reference new variables (manual verification per team)
  - Design documentation updated with new naming and examples

**Stage 3 — Deprecation (`deprecation-process`)**

Run `deprecation-process` for the old tokens, passing the transformation table as the replacement map. Use its timeline, deprecation notices and warning mechanism for this stage, and its removal steps for Stage 4. Don't write a separate deprecation plan.
- Entry: Stage 2 complete, all consumers migrated, no old token references in production
- Action: Mark old tokens as deprecated per the deprecation-process plan. Emit build warnings when old tokens are imported or referenced.
- Exit: Deprecation warnings active in all builds, timeline communicated in release notes and teams pinged
- Rollback: Remove deprecation markers from token files, silence build warnings. (Rarely needed; this is a communication phase, not a code change.)
- Estimated duration: 1 week (setup); 4–8 weeks (deprecation period)
- Verification:
  - Deprecation warnings appear in CI logs when old tokens are used
  - Release notes document the timeline and link to migration guide
  - Teams acknowledge receipt of notification in a shared channel or survey

**Stage 4 — Removal**
- Entry: Deprecation period expired, zero references to old tokens in production, no warnings in the last build cycle
- Action: Delete old tokens from token files. Run a final grep to confirm no references remain. Update token build to exclude old tokens.
- Exit: Old tokens deleted, no build errors, token build output contains only new tokens
- Rollback: Restore old tokens from git, revert token build config. (Rarely needed; performed only if critical failure occurs post-removal.)
- Estimated duration: 1 week
- Verification:
  - Old tokens do not appear in generated token output (CSS variables, Style Dictionary exports, etc.)
  - Final grep confirms zero references in codebase
  - All builds pass, no missing-token errors

Document each stage in a table or section with all criteria visible at once.

### Step 3e — Migration plan document

Generate a comprehensive migration plan document structured as:

**Executive summary** (2–3 sentences)
- What is being migrated and why
- Total scope (token count, consumer count, estimated effort)
- Recommended timeline and risk level

**Migration type classification**
- Primary classification (format / tool / naming / tier / composite)
- Rationale and constraints

**Audit findings**
- Summary of token-audit findings (violations, structure issues)
- Summary of naming-audit findings (naming inconsistencies, convention mismatches)
- Tokens specifically identified as needing change

**Transformation table**
- Every affected token with before → after → type → codemod → risk
- Sorted by risk level (Critical first, then High, Medium, Low)

**Codemods** (from `codemod-generator`)
- The codemod files and run commands, with testing and rollback for each
- Coverage and manual remainder per codemod

**Staged rollout plan**
- Four stages with all entry/exit/rollback/duration/verification details
- Deprecation timeline from `deprecation-process` (Stage 3)
- Timeline visualisation (Gantt or table)
- Rollback checkpoint and success criteria for each stage

**Communication strategy**
- Teams that must be notified (with contacts)
- Content of the notification (migration guide, timeline, FAQ)
- Support plan (who to ask for help, escalation path)
- Schedule for follow-up check-ins

**Dependencies**
- What must be true before migration starts (minimum consumer version, CI updated, token build toolchain version, Figma permissions, etc.)
- What must be completed before each stage entry

**Verification checklist**
- Testable criteria for each stage (specific commands, grep patterns, or checks — not "verify everything works")
- Owner of each verification step
- Pass/fail criteria for moving to the next stage

**Stop here.** Present the plan, and continue to the communication phase only once the user confirms.

---

## Phase 4: Communicate (chain skill)

Once the user has confirmed the plan, chain the `change-communication` skill:

- Input: The migration plan document from Phase 3
- Output: Complete communication package (release notes, migration guide for consumers, team notifications, follow-up schedule)
- The change-communication skill reformats the technical migration plan for each audience (designers, developers, product managers)
- Ensure the communication package explicitly references the migration plan's timeline and checkpoint schedule, and reuses the deprecation-process notices rather than rewriting them

---

## Phase 5: Synthesise

Combine all outputs into a single migration package:

1. **Migration plan document** (from Phase 3)
2. **Communication package** (from Phase 4)
3. **Audit findings summary** (from Phase 2) — cross-referenced with the migration plan
4. **Timeline visualisation** — showing all four rollout stages with checkpoints and dependencies
5. **Success criteria** — how do we know the migration is complete?
6. **Rollback procedures** — one per stage, with exact commands and conditions for rollback

Saving follows the chained-run rules (one save at the end).

---

## Quality checks

- Every token in scope has exactly one entry in the transformation table
- Codemods come from `codemod-generator` and the deprecation plan from `deprecation-process`, not written inline
- Every codemod includes a test command and a rollback command
- Staged rollout includes explicit entry/exit/rollback/duration/verification for all four stages
- The run stopped for the user's confirmation before the communication phase
- Package opens with one headline sentence, has one combined Scope block and one closing note, and ends with the provenance footer
- Communication package references the migration plan timeline specifically
- Estimated effort accounts for manual work remaining after codemods (e.g., "80 tokens via codemod, 20 manual")
- Verification checklist is testable — specific grep patterns, commands, or checks, not vague assertions
- Dependencies section exists and lists prerequisites (minimum versions, CI updates, access requirements)
- Risk assessment for each transformation includes specific consumer or integration impact
- Rollback conditions are explicit: "Rollback if Stage 2 verification fails to find zero old token references in codebase"

---

## Report template structure

```
# Token Migration Plan: [migration name]

[One headline sentence: what is migrating, the risk level, and the first decision needed]

## Executive summary
[scope, effort, timeline, risk level, key assumption]

## Migration type classification
[format/tool/naming/tier/composite with rationale]

## Audit findings
[summary from token-audit and naming-audit; cross-reference with transformation table]

## Transformation table
| Current token | New token | Type | Codemod available | Risk | Risk description |
|---|---|---|---|---|---|

## Codemods
[from codemod-generator: commands with testing and rollback steps]

## Staged rollout plan
### Stage 1: Non-breaking additions
- Entry criteria: [specific conditions]
- Exit criteria: [specific verification steps]
- Rollback: [exact commands or procedures]
- Estimated duration: [days/weeks]
- Verification checklist: [testable steps]

### Stage 2: Consumer migration
[same structure]

### Stage 3: Deprecation
[same structure, timeline from deprecation-process]

### Stage 4: Removal
[same structure]

## Timeline
[visual representation of all stages with checkpoints and dependencies]

## Communication package
[from change-communication skill; one section per audience type]

## Dependencies
[prerequisites that must be true before migration starts]

## Success criteria
[how to know when migration is complete, measurable outcomes]

## Rollback procedures
[one per stage, with conditions and exact commands]

**Scope**
[one combined Scope block per output-discipline]

[Closing note inviting the user to flag intentional deviations]

*Generated by Design System Ops migration agent · [date]*
```

---

## Recurring workflow

Loading, saving and pruning follow the chained-run rules. When a previous migration package exists:

1. **Track stage progress:**
   - Which rollout stage is currently active?
   - Have entry/exit criteria been met for the current stage?
   - Any blockers encountered?
2. **Add a "Migration progress" section** straight after the headline, before the executive summary:
   - Current stage and estimated time remaining
   - Completed checkpoints (with dates)
   - Any deviations from the plan
   - Updated effort estimates based on actual progress

---

## Note on rollback

Each rollout stage is designed with rollback in mind. Stages 1 and 3 are reversible token changes. Stage 2 is a code change and requires git revert. Stage 4 is permanent unless git history is available. The migration plan must make the rollback cost explicit for each stage so stakeholders understand the commitment they are making.
