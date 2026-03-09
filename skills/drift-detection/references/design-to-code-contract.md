# Design-to-code contract definitions

**Knowledge note for Design System Ops**
**Auto-loaded by:** design-to-code-check, contribution-workflow, drift-detection, system-health

---

## What "done" means in a design system context

Design systems work has an ambiguity problem at the handoff. A component can be "done" in many different senses: the design is approved, the component is built, Storybook is running, the tokens are correct, the documentation is written, the accessibility is compliant. Each of these is a different kind of done, and conflating them produces quality gaps that surface as production bugs, accessibility regressions, and documentation debt.

A design-to-code contract makes "done" explicit. It defines what must be true at each stage of the component lifecycle for work to move to the next stage. Teams that have a shared contract spend less time debating readiness and more time building.

---

## The design contract

A component design is complete when:

**The specification is implementable.** A developer can build the component from the design file without needing to ask for clarification on spacing, states, or behaviour. This means: all interactive states are designed (default, hover, active, focus, disabled, loading, error — whichever apply), responsive behaviour is specified at relevant breakpoints, and edge cases (long strings, empty states, maximum data density) are addressed.

**Token usage is explicit.** Colours, spacing, and typography in the design reference the correct design system tokens. A design file where the developer must infer which token applies from the resolved value is not ready to build.

**The component API is defined.** Before build begins, the props, types, defaults, and states the component will accept are agreed. Changes to the API after build begins are expensive.

**Accessibility is addressed at the design stage.** Focus indicator visibility, colour contrast, touch target size, and the ARIA contract (role, keyboard pattern, labelling strategy) are not build-phase decisions. They belong in the design specification.

---

## The build contract

A component build is complete when:

**All specified states are implemented.** Not just the happy path — all interactive states, responsive breakpoints, and edge cases specified in the design.

**Token references are correct.** Every colour, spacing value, and typographic property references the appropriate token at the appropriate tier. No hardcoded values at the semantic or component level.

**Accessibility is implemented and tested.** Keyboard navigation, ARIA roles and attributes, focus management, colour contrast. Not reviewed — tested, with evidence.

**The component matches the design specification.** Alignment reviewed against the specification, not inferred from memory.

**Unit tests exist.** All props, all states, all interactive behaviours have corresponding tests.

**Storybook (or equivalent) is complete.** One story per documented state, sufficient to verify the component in isolation.

---

## The documentation contract

A component is documented when:

**Usage guidelines exist.** When to use, when not to use, and the most common anti-patterns — written for a designer or developer who was not in any of the design conversations.

**The props reference is complete.** Every prop with its name (exact, as used in code), type, default value, and a one-sentence description of what it controls.

**Accessibility is documented.** Keyboard interaction, focus behaviour, screen reader announcements — the specific behaviour of this component, not a reference to WCAG.

**The AI-optimised description is written.** The six-section Figma MCP description is complete and added to the Figma component. (This is a Design System Ops requirement; it may not apply to all teams.)

**Examples cover the primary use case and at least one edge case.** Documentation that only shows the ideal state is documentation that fails teams as soon as they step off the happy path.

---

## The release contract

A component is ready to release when:

**All three contracts above are met.** Design complete, build complete, documentation complete.

**Community review is complete.** For new components and breaking changes, affected teams have been given visibility and the opportunity to raise concerns.

**Release notes are written.** The change is described clearly enough that a consuming team can understand what changed and whether they are affected.

**The migration path is documented (if applicable).** For breaking changes, the path from old to new is explicit, not implied.

---

## Common contract gaps

**Designs delivered as screenshots rather than Figma files.** A developer implementing from a screenshot cannot inspect token references, verify spacing values, or check that all states are defined. This is not a design contract — it is a visual reference.

**"Just copy the existing component."** When a new component is built by copying an old one, the design specification is the previous implementation. This produces a circular reference that propagates any existing problems.

**Accessibility deferred to QA.** Accessibility issues found in QA cost significantly more to fix than issues caught in design. The design contract should require accessibility to be addressed before build begins.

**Documentation written after the release.** Documentation written under pressure after a component has already shipped tends to describe the component as built rather than as intended. It also arrives after the teams who needed it most have already developed their own understanding — sometimes incorrectly.

**No agreed definition of done.** When "done" is undefined, each team defaults to their own interpretation. What the design system team considers complete and what the consuming team expects are different things, and the gap surfaces as support burden.

---

## The API contract (staff-level)

At the senior level, the contract governs component quality. At the staff level, the component's public API is itself a contract — with consumers, with tooling, and with future versions of itself.

**Prop API as a public contract.** Every prop name, type, accepted value, and default is a promise to every consuming team. A prop renamed from `isDisabled` to `disabled` is a breaking change, regardless of how minor it seems internally. Staff-level work treats the prop API with the same seriousness that backend engineering treats a REST API.

**Semantic versioning at the component level.** Component changes should follow semver: patch (bug fix, no API change), minor (new prop or variant, backward-compatible), major (renamed prop, removed variant, changed default). The `change-communication` skill calibrates by change type — staff-level work connects this directly to the component's version.

**Consumer contract testing.** A staff-level system does not assume that a component works correctly in every consuming context. Consumer contract tests verify that consuming applications call the component with props the component actually accepts, and that the component's output matches what consuming applications expect. The `design-to-code-check` skill should flag consumer contract gaps as a validation dimension.

**Breaking change blast radius.** Before shipping a breaking change, map the blast radius: how many consuming applications, how many instances, how complex is the migration. The `deprecation-process` skill should include blast radius analysis, and the `component-to-release` agent should surface it during the release gate.

---

## Platform-level SLA thinking

A design system at the staff level operates as infrastructure. Infrastructure has service level expectations.

**Availability.** Components should not break consuming applications during upgrades. This means backward-compatible defaults, deprecation notices before removal, and migration paths that can be followed incrementally.

**Responsiveness.** Bug reports and support requests from consuming teams should have expected response times. A system that takes three weeks to acknowledge a bug report is not functioning as infrastructure.

**Stability.** Consuming teams should be able to depend on the system's API not changing unpredictably. This means predictable release cadences, versioned changelogs, and no "stealth" changes that modify behaviour without documentation.

**Documentation currency.** Documentation should reflect the currently released version, not the version that existed when documentation was last updated. Stale documentation is a reliability problem.

The `system-health` skill assesses these as part of the governance dimension. The `stakeholder-brief` skill should communicate them in terms that leadership recognises as infrastructure reliability.

---

## The contract as communication tool

A design-to-code contract is not primarily a quality gate. It is a communication tool.

It reduces the negotiation that happens at handoffs when expectations are misaligned. It prevents the slow erosion of quality that comes from "good enough" becoming the de facto standard. And it gives the design systems team a common language with product teams about what is included in the system and what is the product team's responsibility.

The contract should be visible. Teams that know what the standard is can work toward it. Teams that are guessing cannot.
