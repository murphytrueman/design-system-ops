---
name: pattern-documentation
description: "Write documentation for a design system pattern — a multi-component recipe covering use cases, anti-patterns, composition, and related patterns. Patterns span multiple components working together (e.g. a form pattern, a data table pattern). Trigger when someone says: document this pattern, write the pattern page, usage pattern, when to use this, pattern guidelines, document how this works, or anything about creating documentation for a reusable UI pattern rather than a single component. Do NOT trigger for writing usage guidelines for a single named component — use usage-guidelines for that."
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
---

# Pattern documentation

A skill for writing documentation for design system patterns. Patterns are distinct from components: a component is a discrete, reusable UI element; a pattern is a recurring solution composed from multiple components that addresses a specific user or product problem. Form validation, empty states, error handling, progressive disclosure — these are patterns.

## Context

Pattern documentation is systematically underdone in most design systems. Teams document components in detail and leave patterns as implicit knowledge — accumulated through convention, absorbed during onboarding, and lost when people leave. The result is parallel local solutions that drift apart over time, and product teams that rebuild the same interaction in slightly different ways because no one wrote down the shared answer.

Good pattern documentation does two things. It explains the pattern clearly enough that a designer or developer encountering it for the first time can apply it correctly. And it explains the edges: when this pattern is not the right choice, what alternatives exist, and how to handle the cases that do not fit neatly.

---

## Step 0: Pattern discovery guide

Before documenting a pattern, confirm it is worth documenting. Not every recurring UI solution is a pattern — some are conventions, some are coincidences, and some are too specific to generalise.

**A UI solution is a documentable pattern if:**
- [ ] It appears in three or more distinct product contexts (not just three instances in the same product)
- [ ] It solves a user-facing problem, not just a layout convenience
- [ ] It composes two or more design system components in a specific relationship
- [ ] Teams have independently arrived at similar solutions (convergent evolution is the strongest signal)
- [ ] Getting it wrong has real consequences (accessibility, usability, consistency)

**A UI solution is NOT a documentable pattern if:**
- It appears in only one product context (it is a local convention)
- It is a single component used in a standard way (that belongs in the component's usage guidelines)
- It varies so much between instances that no shared structure can be extracted

**Where to find undocumented patterns:**
1. Look at drift-detection findings classified as E (system gap) — these often reveal patterns teams are building independently
2. Review support channel questions — recurring "how do I..." questions about multi-component interactions signal undocumented patterns
3. Ask product teams: "What do you build most often that is not a single component?" The answers are pattern candidates
4. Review design file reuse — Figma frames that appear across multiple files without being components are likely patterns

## Step 1: Establish the pattern scope

Ask for or confirm:
- Pattern name (clear, descriptive, not jargon)
- The user problem or product need this pattern addresses
- Which components from the design system are involved
- Any known product contexts where this pattern is already in use
- Any known edge cases or exceptions the documentation should address

If the pattern does not yet have a name, propose one before writing the documentation. Pattern names should describe the interaction or function, not the visual treatment: "confirmation dialog" not "modal with two buttons."

## Step 2: Write the pattern documentation

---

### [Pattern name]

**Category:** [navigation / forms / feedback / layout / data display / other]
**Components used:** [list the design system components this pattern draws on]
**Last updated:** [date]

---

#### What this pattern does

One to two sentences. Describe the pattern in terms of what it accomplishes for the user, not how it looks or which components it uses.

Example (form validation): Communicates the status of user input during and after form interaction, surfacing specific errors in the context where they occur so users can correct them without losing their progress.

Example (empty state): Guides users when a view has no content to display — whether because data does not exist yet, a search returned no results, or content was removed — and offers a clear path to the next action.

---

#### When to use this pattern

Describe the conditions under which this pattern is the right choice. Be specific about the context. Avoid "use this when you need to show an error" — that is not a usage condition, it is a circular definition.

Good format: "Use this pattern when [user or product situation]. It is appropriate when [specific conditions that make this the right choice over alternatives]."

Include the most important conditions, not an exhaustive list. Three to five is usually right.

---

#### When not to use this pattern

As important as the above. Describe the conditions where a different pattern or approach is more appropriate.

For each exclusion, name the alternative: "If [condition], use [pattern or component name] instead."

This section prevents misapplication more than any amount of positive guidance.

---

#### Composition

Describe how the pattern is assembled from its component parts. This is not a code implementation guide — it is a structural description that works for designers and developers alike.

Cover:
- Which components are required vs optional
- The structural relationship between components (which wraps which, what order, what dependencies)
- Any layout or spacing rules that are part of the pattern
- Responsive behaviour: does the pattern change structure at different breakpoints?

If the pattern has multiple variants (e.g. an inline form validation and a summary form validation are both valid sub-patterns), document each variant's composition separately.

---

#### State coverage

Document every state the pattern can be in. AI agents cannot build what they do not understand, and patterns fail most often at state boundaries — the transitions between states, not the states themselves.

For each state the pattern can occupy:
- Name the state clearly (e.g. Empty, Loading, Populated, Error, Submitting, Success)
- Describe what the user sees and can do in this state
- Describe the transition to the next state (what triggers it, what changes)
- Identify which components are visible, hidden, or change variant in this state

Common states to check for: default/resting, loading/pending, empty/no data, populated/active, error/invalid, success/complete, disabled/locked, partially complete.

If a state is not applicable, say so explicitly — "This pattern does not have an error state because [reason]." Silence is ambiguity. Ambiguity is drift.

---

#### Accessibility

Document the specific accessibility requirements for this pattern — not generic WCAG principles, but the specific keyboard behaviour, focus management, and screen reader experience that this pattern needs to implement.

Patterns often carry accessibility requirements that no individual component owns. A confirmation dialog pattern needs to manage focus on open, trap focus while open, and return focus on close — none of which a single component is responsible for, but the pattern as a whole must get right.

Cover:
- Keyboard interaction flow through the pattern
- Focus management: where focus goes when the pattern opens, changes state, or resolves
- Screen reader announcements: what gets announced and when
- Any ARIA attributes that the pattern adds at the composition level (not the component level)

---

#### Anti-patterns

Name the three to five most common ways this pattern is misapplied. Each anti-pattern should be specific to this pattern, not generic design advice. Write each as a one-sentence description of the misapplication, followed by one sentence on why it creates a problem.

If the pattern has visual examples available, a do/don't pairing is more effective than prose here. If not, write the anti-patterns as clearly as possible in text.

---

#### Related patterns

Cross-references to other patterns that are closely related, commonly confused with this one, or often used alongside it. For each:
- Pattern name
- One sentence on how it relates (often confused with, commonly used alongside, should be used instead when)

---

#### Examples in production

If available: two to three named product contexts where this pattern is in use. This grounds the pattern in reality and gives teams a reference point for correct application.

If no production examples are available, note that and invite consuming teams to contribute examples after the documentation is published.

---

## Step 3: Check for gaps

Before delivering the documentation, verify:

- The "when not to use" section has real alternatives, not just conditions
- Accessibility covers focus management, not just static ARIA roles
- Anti-patterns are specific to this pattern, not recycled from a generic design principles page
- Related patterns include at least one "often confused with" to disambiguate

#### Documentation impact measurement

After publishing pattern documentation, note the expected impact and how to measure it:
- **Reduced drift:** If this pattern was identified through drift-detection, monitor whether new instances of that drift decrease after documentation is published.
- **Reduced support questions:** Track whether the pattern-specific questions in support channels decrease.
- **Increased consistency:** In the next drift-detection run, check whether implementations of this pattern are more consistent.

If none of these signals improve within two quarters of publishing, the documentation may not be discoverable enough — review its placement and promotion.

## Step 4: Flag for the `ai-component-description` skill

If the pattern involves a primary component that does not yet have an AI-optimised description, flag that. Pattern-level documentation and component-level AI descriptions work together: the pattern documentation explains the composition, and the AI description explains each component's contract within it.

## Quality checks

- Pattern name describes the interaction or function, not the visual treatment
- "When to use" and "when not to use" are genuinely distinct and not circular
- Composition section covers responsive behaviour and variant differences
- State coverage section names every state the pattern can occupy — no implicit states
- Accessibility section covers focus management as a pattern-level concern
- Anti-patterns are specific, not generic
- Related patterns include disambiguation for commonly confused alternatives
- Document works as a standalone reference — does not require additional context to follow
