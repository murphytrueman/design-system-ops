# Component Bestiary reference

**Knowledge note for Design System Ops**
**Auto-loaded by:** pattern-documentation, usage-guidelines, ai-component-description, component-audit

---

## What the Component Bestiary is

The Component Bestiary (thecomponentbestiary.com) catalogues UI components as D&D-style creatures, with Challenge Ratings (CR) assigned based on implementation danger rather than visual complexity. A component with a high Challenge Rating is not necessarily large or visually complex — it is dangerous to implement incorrectly, with proportional consequences for users and the system when it goes wrong.

The Bestiary is referenced by Design System Ops as a signal system for documentation and validation priorities. High-CR components need more rigorous usage guidelines, more thorough accessibility audits, and more explicit anti-patterns, because the cost of getting them wrong is higher.

---

## How Challenge Ratings map to design system work

**CR 1–2: Low danger**
Implementation is straightforward. Misuse creates minor inconsistency but not user harm or serious accessibility regressions. Documentation can be lighter — usage guidelines, basic anti-patterns, standard accessibility notes.

Examples: Static text components, dividers, badges, avatars, skeleton loaders

**CR 3–4: Moderate danger**
Implementation requires care. Common misuse patterns exist and have visible consequences. Documentation should include specific anti-patterns and edge case coverage. Accessibility should be explicitly tested rather than assumed.

Examples: Buttons (variant misuse), form inputs (labelling), tooltips (trigger/keyboard issues), cards (composition ambiguity)

**CR 5–6: Significant danger**
Implementation is non-trivial. Multiple failure modes exist. Misuse creates genuine user harm through accessibility regressions, misleading affordances, or navigational confusion. Usage guidelines require full anti-pattern coverage and specific accessibility documentation. AI component descriptions must be thorough and include explicit composition constraints.

Examples: Modals and dialogs (focus trap, scroll behaviour, accessibility contract), select/combobox (keyboard complexity), navigation components (landmark roles, current state)

**CR 7+: High danger**
Implementation requires expertise. Getting it wrong creates significant accessibility regressions, security concerns, or serious UX breakdown. These components should trigger:
- Mandatory accessibility audit before release
- Decision record documenting the implementation choices made
- Enhanced documentation including failure mode documentation
- Active monitoring after release for misuse patterns

Examples: Date pickers (keyboard complexity, internationalisation, accessibility), data tables (complex ARIA relationships, responsive behaviour), rich text editors (ARIA, focus management, paste behaviour), drag-and-drop interfaces

---

## Using Challenge Ratings in documentation

When writing component documentation, the Challenge Rating is a calibration signal for documentation depth.

**For low-CR components:** A complete usage guidelines document, standard props reference, and basic accessibility notes are usually sufficient. Anti-patterns can be brief.

**For moderate-CR components:** Anti-patterns deserve full treatment — specific misuse scenarios with consequences. Edge cases should be explicitly addressed. Accessibility should cover the full keyboard interaction pattern.

**For high-CR components:** Every section in the documentation should be treated as load-bearing. Anti-patterns should include real failure scenarios. Accessibility documentation should be comprehensive. Composition rules should be explicit about what is and is not permitted. The AI component description for high-CR components should be longer and more detailed than for low-CR components — the cost of an AI tool getting a modal wrong is higher than the cost of it getting a badge wrong.

---

## Using Challenge Ratings in validation

When prioritising accessibility audits, use the Challenge Rating to sequence the work:

1. High-CR components first — they carry the most accessibility risk
2. Components with known interactive state complexity (anything with keyboard patterns, focus management, or complex ARIA)
3. Moderate-CR components with incomplete accessibility documentation
4. Low-CR components as part of routine maintenance

This is not an argument for skipping accessibility work on low-CR components. It is an argument for sequencing it — and for investing more time per component on the high-CR end of the spectrum.

---

## Component categories and their typical CR ranges

These are illustrative ranges, not fixed values. A specific implementation may have a higher or lower CR based on its particular design.

| Category | Typical CR range | Primary danger |
|---|---|---|
| Typography and text | 1–2 | Low; main risk is token misuse |
| Layout primitives | 1–3 | Moderate for grid/flex; composition complexity |
| Static display (avatars, badges, chips) | 1–3 | Low; mainly variant misuse |
| Form inputs (text, checkbox, radio) | 3–5 | Labelling, error state, keyboard |
| Buttons and interactive controls | 3–5 | Variant misuse, affordance signalling |
| Navigation (tabs, breadcrumbs, menus) | 4–7 | ARIA patterns, current state, keyboard |
| Overlay (tooltip, popover) | 4–6 | Trigger interaction, keyboard, dismissal |
| Modal and dialog | 6–8 | Focus trap, scroll, accessibility contract |
| Select and combobox | 6–8 | Keyboard complexity, ARIA roles |
| Date and time pickers | 7–9 | Full accessibility complexity |
| Data tables | 6–8 | ARIA relationships, sorting, selection |
| Drag-and-drop | 7–9 | Accessibility nearly always incomplete |

---

## The Bestiary as a contribution filter

When reviewing a contribution proposal, the Challenge Rating of the proposed component is a signal for the contribution process:

- Low-CR contributions can move through the process more quickly — the implementation risk is lower and the review can be lighter
- High-CR contributions should trigger additional review gates: accessibility review at the design stage, not just the build stage; explicit accessibility testing before release; consideration of whether the team has the expertise to implement it correctly

A high-CR component contributed without adequate expertise is worse than no component, because it provides false confidence while introducing real risk.

---

## Reference

The Component Bestiary is maintained at thecomponentbestiary.com. Volume I covers the most common UI components with full creature entries. For components not yet in the Bestiary, use the category ranges above as a starting estimate and apply professional judgment.
