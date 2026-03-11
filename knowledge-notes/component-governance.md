---
name: component-governance
type: knowledge
---

# Component governance frameworks

**Knowledge note for Design System Ops**
**Auto-loaded by:** contribution-workflow, deprecation-process, decision-record, component-audit, system-health

---

## What component governance is

Component governance is the set of decisions and processes that determine what belongs in a design system, how it gets there, how it changes, and how it leaves. Without it, a design system accumulates components by inertia rather than by intent, and the maintenance burden grows faster than the value delivered.

Governance is not bureaucracy. The goal is not to make contribution harder — it is to make the system trustworthy. A system that accepts anything is a system nobody trusts.

---

## Decision records

Every significant design system decision should be recorded. Significant means: a decision that a new team member would need to understand to work effectively with the system, or a decision that a future team might reverse without knowing it was already considered.

Decisions worth recording:
- Why a component was added (the use cases it serves, the alternatives that were not built)
- Why a component was not added (the reasons a reasonable proposal was declined)
- Why a naming convention was chosen
- Why a token architecture decision was made a specific way
- Why a deprecation was scheduled and on what timeline

The value of decision records compounds over time. A team that has maintained records for two years knows why their system looks the way it does. A team that has not is perpetually re-litigating the same questions.

**Decision record format:** See the `decision-record` skill for the full format. The minimum viable record is: context, options considered, decision, consequences.

---

## Contribution criteria

A contribution is worth adding to the system if it meets all of the following:

**Recurrence.** The need appears across multiple products or teams, not just one. A component that solves one team's specific problem is a local component, not a system component. The threshold varies — a small system serving two products might accept something used by both; a large system serving twenty products should require a higher bar.

**Generality.** The component or pattern is general enough to be used by future teams and contexts, not just the team that proposed it. This requires some abstraction: the contribution should solve the category of problem, not the specific instance.

**Accessibility.** The component can be implemented in an accessible way without significant design compromise. If accessibility is only achievable through workarounds that undermine the component's design intent, the design needs to change before the component belongs in the system.

**Ownership.** Someone is willing to own the build, documentation, and maintenance. Contributions without owners become technical debt.

**Fit.** The contribution is consistent with the system's existing patterns, conventions, and architecture. A contribution that requires the system to contradict itself to accommodate it is not a contribution — it is a fork.

---

## Deprecation triggers

A component should be considered for deprecation when any of the following is true:

**It has been superseded.** A better alternative exists in the system that covers all of the deprecated component's use cases. The migration path to the new component is clear.

**It has zero or near-zero usage.** A component with no known consumers has no reason to be maintained. This applies particularly to components that were added speculatively and never adopted.

**It carries unresolvable accessibility debt.** If a component cannot be made accessible without a complete redesign, and the redesign produces something that would be a different component, the original should be deprecated rather than patched.

**It creates maintenance burden disproportionate to its value.** Some components require ongoing maintenance effort — responsive behaviour updates, token migration, accessibility improvements — that is not proportional to how much they are used.

**It is no longer consistent with the system's direction.** Design systems evolve. A component from an earlier era of the system may not fit the current component contract, token architecture, or design language. The decision to deprecate is a decision to acknowledge that evolution explicitly.

---

## The full component lifecycle

**Proposal.** A need is identified and articulated. The criteria above are evaluated. The decision is recorded — including declined proposals.

**Design.** The component is designed against the system's existing patterns, tokens, and conventions. The API is defined before implementation begins.

**Build.** Implementation against the agreed spec. Accessibility is addressed in the build phase, not added afterward.

**Documentation.** Usage guidelines, anti-patterns, and accessibility notes are written before release. The `ai-component-description` skill should be run at this stage for Figma MCP readiness.

**Release.** Component ships with a version note and a communication to consuming teams.

**Active maintenance.** Component is maintained, bug-reported, and improved over its life in the system.

**Deprecation notice.** Deprecation is announced with a timeline and a migration path.

**Removal.** Component is removed after the deprecation window has closed.

---

## Contribution vs local implementation

The contribution process is not the only path for product teams that need something the system does not have. Local implementations are a legitimate response to a genuine system gap — the system serves most needs, not all needs, and local work fills the edges.

The difference between a healthy local implementation and problematic divergence:
- A healthy local implementation is documented, intentional, and does not conflict with system patterns
- It is flagged as a contribution candidate if the need is general enough to belong in the system
- It is maintained alongside the product that uses it, not abandoned

The `drift-detection` skill categorises divergence to distinguish accidental drift from intentional local work. Intentional local implementations should become decision records.

---

## Component dependency graph

At the staff level, governance requires understanding how components depend on each other. A change to a primitive component (Button, Icon, Text) has a different blast radius than a change to a leaf component (DateRangePicker).

**Composition mapping.** Every component that renders other components from the system creates a dependency. `Card` may compose `Text`, `Button`, and `Icon`. A breaking change to `Icon` affects `Card` — and every component that composes `Card`. The `component-audit` skill should build a composition graph and identify: root components (composed by nothing), leaf components (compose nothing), and high-fan-in components (composed by many others, meaning changes propagate widely).

**Token dependency mapping.** Components are also linked through shared tokens. Two components that both bind to `color.action.primary` are implicitly coupled. A token value change affects both. The `token-audit` skill should produce a token-to-component dependency map showing which token changes affect which components.

**Cross-system dependency.** In organisations with multiple design systems (brand-specific systems, sub-systems, platform-specific implementations), components may depend on shared primitives or tokens across system boundaries. Staff-level governance tracks these cross-system dependencies and flags when a change in one system affects another.

---

## Design system maturity model

Staff-level practitioners assess where a system sits on a maturity spectrum and identify what the next stage requires. This is distinct from a system-health assessment — maturity describes the sophistication of the system's practices, not just its current state.

**Ad-hoc.** Components exist but are not governed. No shared tokens, no contribution process, no documentation standard. Components are added by whoever builds them.

**Managed.** A component library exists with some governance. Token architecture is established (at least primitives and some semantics). Documentation exists for most components but is inconsistent in depth. Contribution process exists but is informal.

**Systematic.** Three-tier token architecture is enforced. Components follow a consistent API contract. Documentation follows a standard format. Contribution and deprecation processes are documented. Release cadence is predictable.

**Measured.** Adoption is tracked quantitatively. Drift is detected and classified. System health is assessed across dimensions. Recurring reviews happen on a cadence. Decisions are recorded.

**Optimised.** The system operates as platform infrastructure. Component APIs are versioned with semver. AI-ready metadata is maintained. Machine-readable manifests exist. Consumer contract testing is in place. The system's quality bar is calibrated to the team's specific needs.

The `system-health` skill should include a maturity stage assessment. The `stakeholder-brief` skill should frame progress in terms of maturity stage transitions.

---

## Common governance failure patterns

**No clear ownership.** Without a named owner or responsible team, governance decisions default to whoever happens to be paying attention. This produces inconsistent outcomes and unrecorded decisions.

**Governance as gatekeeping.** A contribution process that exists to protect the system from contributors rather than to help contributors build the system well. The signal: contribution rates are low and teams build locally instead.

**Undocumented decisions.** The system looks the way it does for reasons that nobody can articulate. New team members learn by collision. The same decisions get re-litigated every eighteen months.

**Deprecation avoidance.** Components are never deprecated because deprecations feel disruptive. The system accumulates components indefinitely. Maintenance burden grows. Trust declines because teams cannot predict what will and will not be there in six months.

**Contribution criteria that are never articulated.** Contributions are accepted or declined based on implicit judgment that producing teams cannot predict or prepare for. The system appears arbitrary from the outside.
