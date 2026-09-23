---
name: component-to-release
description: "Chains design-to-code, accessibility and token-compliance checks (three release gates), then the AI description, usage guidelines and change communication, into a release package awaiting human sign-off. Adds blast-radius analysis for breaking changes. Invoked by /release-check."
---

# Component to release

A chained workflow that takes a component from the end of build through to release-ready: validating implementation quality, checking accessibility, confirming token compliance, generating AI-optimised documentation, writing usage guidelines, and producing the release communication. Produces a release package — all documentation and communication ready to go, pending human sign-off.

**Output type:** Proposal and documentation package. This agent produces validation findings and ready-to-publish documentation. It does not publish anything. Every output requires human review before it goes live.

**Provenance:** Each AI-generated document carries a generation marker, and the package ends with a one-line provenance footer. AI-generated documentation should be reviewed and refined by a human before publication — the marker makes this visible.

**Run rules:** Follow the chained-run rules in ${CLAUDE_PLUGIN_ROOT}/knowledge-notes/agent-orchestration-guide.md — loading, one inventory, hand-off cards, one report, skipped-permission steps, configuration, and recurring runs. This file holds only what is specific to the release chain.

---

## When to run this

- Before releasing a new component to the system
- Before releasing a significant update to an existing component (new variants, breaking API change, major accessibility work)
- As part of a contribution review for team-contributed components

Do not run this for minor bug fixes or documentation corrections. For those, run `change-communication` directly.

**Small-system note (fewer than 5 components):** Adding a component to a system with 1–4 existing components is a significant event — you are expanding the system by 25–100%. The full pipeline still applies, but be aware of the proportional impact: this component will define the system's conventions as much as it follows them. If this is the second or third component, pay extra attention to whether its API patterns are consistent with the existing components — inconsistencies at this size become the system's default conventions. The accessibility audit (Step 2) and token compliance check (Step 3) are non-negotiable regardless of system size. The community review stage (referenced via change-communication) can be a direct conversation with the consuming team rather than a formal announcement, since the audience is small enough to talk to directly.

---

## Configuration and integrations

Configuration and integrations follow the chained-run rules. Specific to this chain:

- **Gate overrides** from `gates.*` determine which findings block release. For example, `gates.accessibility.contrast_blocks_release: false` allows a colour contrast WARN during a brand transition.
- If Figma MCP is configured and permitted, the design specification auto-resolves for design-to-code-check. If it isn't permitted, record the skip in Scope and assess the implementation only.

## What you need before starting

- The component implementation, accessible via Storybook, a live environment, or a design file
- The design specification (Figma file or equivalent — auto-pulled if Figma MCP is configured)
- The agreed component API (props, types, defaults — auto-pulled from Storybook or GitHub if configured)
- The component's accessibility requirements (or this agent will derive them)
- The Figma component for the AI description step (auto-pulled if Figma MCP is configured)

If the design specification is not available and Figma MCP is not configured, the design-to-code check is partially impaired. Note this and proceed with implementation assessment only.

---

## Phase 0: Component type decision

Before entering the validation pipeline, classify the component change. This determines the depth of each phase.

**What type of change is this?**

| Type | Description | Validation depth | Documentation depth | Communication depth |
|---|---|---|---|---|
| **New component** | Component that does not exist in the system | Full — all 3 validation steps | Full — AI description + usage guidelines | Full — release notes + announcement |
| **Enhancement** | New variant, prop, or behaviour on existing component | Standard — design-to-code + accessibility | Update — revise existing docs | Standard — release notes |
| **Breaking change** | API change that requires consumer migration | Full + blast radius analysis (Step 3b) | Full — update all docs + migration guide | Full + direct notification |
| **Bug fix** | Correcting a defect in existing behaviour | Focused — only the affected dimension | Minimal — note the fix | Patch — release notes entry only |

Classify the change before proceeding. The classification flows through every subsequent phase — a bug fix should not go through the full documentation pipeline, and a breaking change must not skip the blast radius analysis.

---

## Phase 1: Validate

Steps 1–3 are gates. **When a gate blocks, the pipeline stops there:** don't run the remaining steps. Produce the release package with the decision BLOCKED, the blocking findings and what would fix each one, and list the steps that didn't run in the Scope block. Documentation and announcements for a component that has to change first would be written for the wrong component.

### Step 1 — Design-to-code check (`design-to-code-check`)

Compare the implementation against the design specification. Capture:
- Discrepancy log with classifications (Type I: implementation error / Type II: spec gap / Type III: system inconsistency / Type IV: accepted divergence)
- Any critical or high severity findings

**Gate:** Critical findings (accessibility regression, significant visual divergence) block. Stop the pipeline here.

If only medium and low findings exist: document them, proceed, and include them in the release notes as known minor differences if they are not being corrected before release.

### Step 2 — Accessibility per component (`accessibility-per-component`)

Run the full five-dimension accessibility audit. Capture:
- Overall status (✅ PASS / ⚠️ WARN / ❌ FAIL)
- Any FAIL findings across keyboard navigation, screen reader, colour contrast, focus management, ARIA

**Gate:** Any FAIL on keyboard navigation, focus management or ARIA blocks, unless `gates.accessibility.keyboard_blocks_release` is false. A colour contrast FAIL blocks too, unless `gates.accessibility.contrast_blocks_release` is false or the failing state is documented as an accepted exception with a timeline for correction. When this gate blocks, stop the pipeline here.

WARN findings should be documented in the release notes.

### Step 3 — Token compliance (`token-compliance`)

Check for hardcoded values, wrong-tier token references, and inconsistent token application. Capture:
- Violation count by type
- Any wrong-tier references (architecturally critical)
- Any hardcoded values that would break under theming

**Gate:** Wrong-tier references and hardcoded colour values block for systems with active theming (see `gates.token_compliance.*`); when they do, stop the pipeline here. For systems without theming, they are High priority items to be noted in the release notes with a remediation plan.

### Step 3b — Blast radius (breaking changes only)

Run only when Phase 0 classified the change as Breaking. Two inputs:
- **Semver and changelog** — run `version-bump-advisor` on the change to confirm the major bump and flag edge cases.
- **Consumers affected** — search the consuming repositories in the inventory for imports of the component (for example, `grep -rn "import.*[ComponentName]"`). If a component-audit dependency graph from this session exists, reuse it instead. Report the count of consuming apps and files, and list which repositories were searched; if none were available, write `[needs data: consuming repositories]` rather than estimating.

This step produces the blast radius figure used in the API contract summary, the migration guide in Step 6, and the sign-off checklist.

---

## Phase 2: Document

### Step 4 — AI component description (`ai-component-description`)

Generate the six-section AI-optimised component description for Figma MCP. This is the canonical component description — it becomes the source of truth for the component's contract.

This agent publishes nothing, so skip the skill's write-back-to-Figma step. Writing the description to Figma goes on the sign-off checklist instead. If the team needs JSON metadata, suggest running `metadata-schema-generator` after sign-off; this chain produces prose only.

The description should incorporate findings from Phase 1:
- Anti-patterns section should include any Type IV accepted divergences from the design-to-code check
- Accessibility section should incorporate findings from the accessibility audit
- Any WARN findings from accessibility should be noted as edge cases

Add provenance marker to the description:

```
// Generated: [date] — Design System Ops component-to-release agent
// Review before publishing. AI-generated draft requires human refinement.
```

### Step 5 — Usage guidelines (`usage-guidelines`)

Write the component usage guidelines. Draw on validation findings:
- Anti-patterns section should include any misuse patterns surfaced during the design-to-code check or accessibility audit
- Edge cases section should include any states that had WARN findings in the accessibility or design-to-code checks
- Accessibility section should be directly informed by the audit output from Step 2

The usage guidelines and AI component description should be consistent — the same anti-patterns, the same accessibility guidance, the same prop descriptions. If they contradict each other, the AI component description takes precedence as the canonical contract.

---

## Phase 3: Release

### Step 6 — Change communication (`change-communication`)

Classify the change and produce the communication package.

For a new component: Minor enhancement classification. Release notes + announcement.
For a breaking API change: Breaking change classification. Full package including migration guide.
For a non-breaking update to an existing component: Minor enhancement or Patch, depending on scope.

The release notes should reference:
- Any known issues from the validation phase that are not blocking release (with timelines for resolution)
- Any WARN findings from accessibility that are being tracked but not blocking
- The availability of the AI-optimised component description for teams using Figma MCP

---

## Phase 4: Produce the release package

---

### Component release package

Open with one headline sentence: is this component clear to release, and if not, what is blocking it.

**Component:** [name]
**Release type:** [New component / Enhancement / Breaking change / Bug fix — from Phase 0]
**Sign-off:** a person must approve this package before anything is published, whatever the release decision below.

---

#### Validation summary

| Check | Result | Blockers | Notes |
|---|---|---|---|
| Design-to-code | ✅ PASS / ⚠️ WARN / ❌ FAIL | [count] | [key findings] |
| Accessibility | ✅ PASS / ⚠️ WARN / ❌ FAIL | [count] | [key findings] |
| Token compliance | ✅ PASS / ⚠️ WARN / ❌ FAIL | [count] | [key findings] |

**Release decision:** CLEAR TO RELEASE / BLOCKED (list blocking findings) / CLEAR WITH NOTES (list tracked items). This is the only verdict in the package.

If a gate stopped the pipeline, the package ends after the validation summary and the blocking findings: leave out the documentation and communication sections, and list the steps that didn't run in the Scope block.

---

#### Documentation package

Contents:
1. AI component description (Figma MCP format) — ready to paste into Figma
2. Usage guidelines — ready for documentation platform
3. Release notes — ready to publish with the release
4. Announcement copy — ready to send

Each document includes its provenance marker.

---

#### API contract summary (staff-level)

| Contract element | Status |
|---|---|
| Props documented with types, defaults, intent | COMPLETE / PARTIAL / MISSING |
| Semver classification | [patch / minor / major] |
| Breaking changes | [none / list with migration paths] |
| Consumer blast radius | [consuming apps and files affected, from Step 3b, if breaking] |
| Component manifest entry | UPDATED / NEEDS UPDATE / N/A |

For breaking changes: include the Step 3b blast radius and migration effort estimate. For new components: include the recommended manifest entry to add to the component manifest file.

---

#### Sign-off checklist

Before publishing:

- [ ] Validation findings reviewed — blocking issues resolved
- [ ] AI component description reviewed for accuracy — technical details confirmed by the component author
- [ ] Description written to the Figma component (this agent does not write to Figma)
- [ ] Usage guidelines reviewed — anti-patterns and edge cases reflect real observed behaviour
- [ ] Release notes reviewed — version numbers, migration guidance, and dates confirmed
- [ ] Announcement copy reviewed — channel selection confirmed
- [ ] Semver classification confirmed — release type matches the actual scope of change
- [ ] Component manifest updated (if maintained) — new entry for new components, updated entry for changes
- [ ] Consumer contract impact assessed (if breaking change) — Step 3b blast radius documented and migration path verified

---

#### Scope, closing note and footer

One combined Scope block covering every step (per output-discipline), including any step skipped because its tools weren't permitted. Then one closing note inviting the user to flag intentional deviations. End with a one-line provenance footer:

*Generated by Design System Ops component-to-release agent · [date]*

---

## Quality checks

- All three gates (Steps 1–3) are applied — a blocking finding stops the pipeline at that step, and the steps that didn't run are listed in Scope
- Breaking changes have a Step 3b blast radius with the searched repositories listed
- Package opens with one headline sentence, has one combined Scope block and one closing note, and ends with the provenance footer
- Nothing is written to Figma or published; the Figma write-back is on the sign-off checklist
- Documentation is internally consistent — AI description and usage guidelines do not contradict each other
- Provenance markers are present on all AI-generated documentation
- The package states that a person must sign off before publication, and the release decision is its only verdict
- The sign-off checklist is specific to this component, not generic
