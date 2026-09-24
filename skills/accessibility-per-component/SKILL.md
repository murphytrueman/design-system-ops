---
name: accessibility-per-component
description: "Audit one design system component's accessibility against WCAG 2.2 AA: keyboard, screen reader, contrast, focus, ARIA, target size. Trigger: a11y audit, is this accessible, WCAG check, screen reader support, keyboard navigation check. Not for page- or product-wide audits."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(npx axe:*), Bash(npx test-storybook:*), Bash(npx playwright:*)
references:
  - ../../knowledge-notes/output-discipline.md
---

# Accessibility per component

A skill for running a structured accessibility audit on a design system component, covering five dimensions: keyboard navigation, screen reader experience, colour and contrast, focus management, and ARIA implementation. Produces a PASS/FAIL/WARN per criterion with specific remediation guidance.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Accessibility audits at the component level are more valuable than page-level or system-level assessments because they fix the problem at its source. A component with a correct accessibility implementation propagates that correctness to every product that uses it. A component with an accessibility bug propagates that bug at the same scale.

This skill audits against WCAG 2.2 AA as the baseline. Some legal baselines (e.g. EN 301 549) still reference WCAG 2.1 AA; use that if it's the team's obligation. Where a criterion is more stringent at AAA and the difference matters practically (particularly around colour contrast and keyboard accessibility), this is noted. 4.1.1 Parsing is obsolete in WCAG 2.2 — don't cite it. The output is not a compliance report — it is a practical guide to what needs to change and why.

**Evidence rule.** PASS requires evidence from the running component or a computed ratio. Code-only inference is ⚠️ WARN (unverified). Overall status = the worst criterion result.

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `severity.missing_aria` — severity for missing or incorrect ARIA findings (default: critical)
- `gates.accessibility.keyboard_blocks_release` and `gates.accessibility.contrast_blocks_release` — whether keyboard and contrast FAILs block release (both default: true). If a gate is set to false, still report the FAIL, and note that it does not block release under the team's config.

## Boundaries

This skill audits a single component at a time. If the request is for a page-level or full-product accessibility audit, escalate to a dedicated accessibility review process — this skill is not designed for that scope. If no specific component is identified, ask which component to audit before proceeding. If the component has no implementation yet (design only, no code), note that the audit covers design intent only and flag code-level checks as pending.

---

## Step 1: Gather component information

Ask for or confirm:
- Component name and its design system context
- Access to the component for testing: Storybook, a live implementation, or a design file
- The component's interactive states (default, hover, focus, active, disabled, error, etc.)
- Any existing accessibility documentation for the component
- Whether the component is used in any assistive technology-sensitive contexts (financial, medical, government — these warrant extra rigour)

**Find the runtime evidence before auditing.** PASS needs the running component, so look for what can run it: a Storybook with the test-runner or the a11y addon (`npx test-storybook --url <storybook>` runs axe per story), `jest-axe` or `vitest-axe` tests in the repo, a Playwright setup with `@axe-core/playwright`, or a dev server. If any exists, run it for this component and use its output as evidence. If none exists, ask the user for one of: a Storybook URL, a screen-reader transcript of the primary task, or screenshots of each state. Without any of these, every keyboard, screen-reader and focus criterion is ⚠️ WARN (unverified), the report says so in its first line, and only contrast (computed from the resolved token values) can be PASS or FAIL. Don't run the whole audit from source and present it as verified.

If the component can only be assessed from a design file rather than a live implementation, note that the keyboard and screen reader dimensions are being assessed against the specification rather than the built behaviour. These findings should be verified against the implementation before being marked as passing.

## Step 2: Run the five-dimension audit

### Dimension 1: Keyboard navigation

Every interactive component must be fully operable by keyboard alone. Assess:

**Tab order**
- Does the component receive keyboard focus in a logical order relative to surrounding content?
- If the component is a composite widget (e.g. a modal, a menu, a tab panel), is the internal tab order logical?

**Activation**
- Can the component's primary action be triggered with Enter?
- If the component behaves like a button (not a link), can it also be triggered with Space?
- For components with multiple actions (e.g. a dropdown with options), are all actions keyboard accessible?

**Arrow key navigation**
- For composite widgets (menus, tab panels, radio groups, listboxes), is arrow key navigation implemented correctly per the ARIA Authoring Practices Guide (APG) pattern for this widget type?

**Escape key**
- For components that open a layer (modal, popover, tooltip, dropdown), does Escape close it and return focus correctly?

**Reaching past large content**
- If the component contains a large block of focusable content (a data table, a long list), can a keyboard user reach the controls after it without tabbing through every cell? (This is a 2.1.1 usability check at component level; 2.4.1 Bypass Blocks is page-level and isn't cited here.)

Result per criterion: PASS / FAIL / WARN (warn = partially implemented, needs verification in a specific context, or inferred from code without running the component)

### Dimension 2: Screen reader experience

Assess the experience for a screen reader user navigating with keyboard focus:

**Role announcement**
- Does the component announce the correct ARIA role? Is the role appropriate for how the component behaves?
- FAIL example: a custom dropdown built from a `<div>` with no role — announces as nothing
- PASS example: `role="combobox"` on an autocomplete input

**State announcement**
- Are interactive states announced correctly? Expanded/collapsed, checked/unchecked, selected, disabled, required, invalid
- FAIL example: a toggle switch with no `aria-checked` — the state is not communicated
- PASS example: `aria-checked="true"` toggling to `aria-checked="false"` with a live region or label change

**Name computation**
- Does the component have an accessible name? Is it descriptive enough to be meaningful out of context?
- For form elements: is the label correctly associated (via `for`/`id`, `aria-labelledby`, or `aria-label`)?
- For icon-only buttons: is there an accessible name via `aria-label` or visually hidden text?
- FAIL example: an icon button with no accessible name — announces only as "button"

**Group labelling**
- If the component is part of a group (radio group, checkbox group, fieldset), is the group correctly labelled?

**Live regions**
- If the component produces dynamic content changes (error messages appearing, status updates), are these communicated via `aria-live` or an appropriate role?

**Instructions and descriptions**
- If the component requires usage instructions to be usable (e.g. a date picker, a password field with requirements), are these instructions programmatically associated via `aria-describedby`?

Result per criterion: PASS / FAIL / WARN

### Dimension 3: Colour and contrast

**Text contrast**
- All text within the component must meet a minimum 4.5:1 contrast ratio against its background at WCAG AA (3:1 for large text — 18pt regular or 14pt bold).
- Check all text at all states: default, hover, disabled, error, success.
- Note: disabled state text is exempt from WCAG AA contrast requirements, but low-contrast disabled text should still be flagged as a WARN if it is likely to be read by users with low vision.

**Non-text contrast (UI components)**
- Active UI component boundaries (input borders, checkbox borders, button outlines where the shape communicates the control) must meet a 3:1 minimum contrast ratio against adjacent colours. (WCAG 1.4.11)

**Focus indicator contrast**
- The focus indicator must meet 3:1 contrast against adjacent colours (WCAG 1.4.11 Non-text Contrast) and be visible (2.4.7 Focus Visible). 2.4.13 Focus Appearance (AAA) sets a stricter size and contrast-change bar — note it as an AAA recommendation, not an AA failure.

**Colour as the only means of conveying information**
- If the component uses colour to convey state or meaning (e.g. a red border for an error, a green icon for success), is colour supplemented by another indicator (icon, text label, pattern)?

Result per criterion: PASS / FAIL / WARN with specific contrast ratio figures where assessable

### Dimension 4: Focus management

Focus management is a component-level concern whenever a component opens, closes, moves, or otherwise changes the focus context.

Assess:

**Focus on open**
- When the component opens a layer (modal, dialog, drawer, dropdown), where does focus move?
- Correct: focus moves to the first focusable element within the layer, or to the layer container if it has a defined ARIA role that accepts focus
- Incorrect: focus stays on the trigger, leaving keyboard users unable to interact with the new content

**Focus trap**
- For modal dialogs: is focus trapped within the modal while it is open? Can a keyboard user accidentally tab out of the modal into the obscured page content behind it?

**Focus on close**
- When the component closes, where does focus return?
- Correct: focus returns to the trigger element that opened the layer
- Incorrect: focus moves to the top of the page, loses position, or becomes undefined

**Focus visibility**
- Is the focus indicator visible at all focusable elements within the component?
- Is the focus indicator styled in a way that clearly distinguishes it from the hover state?

**Focus not obscured**
- When an element receives focus, is it at least partly visible — not hidden behind a sticky header, cookie banner, or the component's own overlay? (WCAG 2.4.11 Focus Not Obscured (Minimum), AA)

Result per criterion: PASS / FAIL / WARN

### Dimension 5: ARIA implementation

Assess the correctness of ARIA usage:

**Role appropriateness**
- Are the ARIA roles used appropriate for the component's function? (Reference the APG for the correct role pattern for each widget type)
- Are any roles being used in ways that conflict with their defined semantics?

**Required ARIA attributes**
- Are all required attributes for the component's ARIA role present? (e.g. `aria-expanded` for a disclosure, `aria-selected` for a tab, `aria-controls` linking a trigger to its content)

**Prohibited ARIA patterns**
- Is ARIA being used to fix an inaccessible native implementation when a semantic HTML element would be more appropriate? (First rule of ARIA: do not use ARIA if a native HTML element provides the correct semantics)
- Are there redundant or conflicting ARIA attributes?

**Landmark regions**
- If the component occupies a significant section of a page (a navigation, a main content area, a complementary region), is it correctly wrapped in the appropriate landmark element or role?

Result per criterion: PASS / FAIL / WARN

### Other component-level criteria

Check these where the component type makes them relevant, and report them under the closest dimension:
- **2.5.8 Target Size (Minimum):** pointer targets are at least 24×24 CSS px, or have enough spacing to meet the exception. Watch icon buttons, close buttons, chips, and pagination.
- **2.5.7 Dragging Movements:** anything operated by dragging (sliders, sortable lists, resizable panels) has a single-pointer alternative such as click-to-position or move buttons.
- **2.5.3 Label in Name:** where a control has a visible label, its accessible name contains that text.
- **1.4.13 Content on Hover or Focus:** tooltips and popovers can be dismissed without moving pointer or focus (usually Escape), stay open while hovered, and don't vanish until dismissed.
- **1.4.12 Text Spacing:** content doesn't clip or overlap when line, paragraph, letter, and word spacing are increased. Fixed-height containers are the usual cause.
- **3.3.7 Redundant Entry:** for multi-step form components, information already entered is auto-filled or selectable rather than re-typed.
- **4.1.3 Status Messages:** dynamic results (error text appearing, "3 results", "saved") are announced without moving focus, via `aria-live` or `role="status"`/`role="alert"`. This is the criterion behind the live-region check in Dimension 2; cite it.
- **3.3.1 Error Identification and 3.3.2 Labels or Instructions:** for inputs, an error is described in text (not colour alone) and associated with the field; required fields and formats are stated before the user submits.
- **1.4.10 Reflow and 1.4.4 Resize Text:** the component still works at 320 CSS px wide (or 400% zoom) without two-dimensional scrolling, and at 200% text size. Fixed widths and heights are the usual failures.
- **Forced colours (Windows High Contrast):** under `@media (forced-colors: active)` the component's boundaries, focus indicator and state indicators survive, because backgrounds and box-shadows are removed. Check for `forced-color-adjust` and system-colour keywords where a border or outline carries meaning.
- **Motion:** animations respect `prefers-reduced-motion` (2.3.3 is AAA; note it as a recommendation, and flag any flashing over three times a second as 2.3.1, which is A).

## Step 2b: Screen reader testing guide

When Dimension 2 has any FAIL or WARN, include a short verification guide so the team can confirm the fix:
- **VoiceOver (macOS):** Cmd + F5 to toggle; Tab through interactive elements, VO + Right Arrow for content.
- **NVDA (Windows, free from nvaccess.org):** Tab for interactive elements, arrow keys for content.
- Listen for role, name, and state on every interactive element, then try to complete the component's primary task with keyboard and screen reader alone.

## Step 3: Produce the audit report

---

### Accessibility audit: [component name]

Open with a headline sentence that tells the reader the overall state and where to focus.

**Audit date:** [date]
**WCAG level:** 2.2 AA (or 2.1 AA where that is the team's legal obligation)
**Assessment method:** [live component / design specification / Storybook]
**Additional context:** [e.g. tested with VoiceOver/macOS, NVDA/Windows — if applicable]

---

#### Overall status

✅ PASS / ⚠️ WARN / ❌ FAIL — the worst result across all criteria. Criteria inferred from code alone are ⚠️ WARN (unverified), never PASS.

---

#### Results by dimension

| Dimension | Criterion | Result | Severity | Evidence | Finding | Remediation |
|---|---|---|---|---|---|---|
| Keyboard | Tab order | ✅ PASS / ⚠️ WARN / ❌ FAIL | 🔴/🟠/🟡/⚪ or — | [file:line, story id, axe rule id, computed ratio, or transcript line] | [specific finding] | [specific fix] |
| ... | | | | | | |

**Status key:** ✅ PASS / ⚠️ WARN / ❌ FAIL. Severity applies to FAIL and WARN rows:
- 🔴 **Critical** — the component can't be operated by keyboard; a control has no accessible name; a modal doesn't trap or return focus; body text below 4.5:1. These block release under the default gates
- 🟠 **High** — a state isn't announced; the focus indicator is below 3:1 or hidden; a target is under 24 CSS px; a tooltip fails 1.4.13; a role is missing a required attribute
- 🟡 **Medium** — disabled-state contrast; redundant or conflicting ARIA; clipping under text spacing or reflow
- ⚪ **Low** — AAA recommendations (focus appearance, reduced motion)

Evidence is where the result came from: the source line, the Storybook story or axe rule, the computed ratio with both colours, or the transcript line. A row with no evidence is WARN, never PASS.

---

#### Critical findings

Pull out any FAIL results that create significant barriers — particularly any that prevent a user from completing a task using only a keyboard or screen reader. These need to be fixed before the component ships or remains in the system.

---

#### WCAG criterion references

For each FAIL or WARN finding, include the relevant WCAG criterion (e.g. 1.4.3 Contrast Minimum, 2.1.1 Keyboard). This makes it easier to prioritise against compliance requirements and to communicate findings to stakeholders.

---

**Scope**
- **Inspected:** [component source files, Storybook stories, running build, or design file actually examined]
- **Not inspected:** [e.g. assistive technologies not tested, states or variants not reachable, consuming-product contexts]
- **How "none found" was checked:** [for any criterion reported as clean, the evidence: screen reader output heard, computed contrast ratio, keyboard walk-through]
- **Assumptions:** [e.g. token values assumed to match the rendered colours]

If any of these findings are deliberate decisions (for example, a pattern that departs from the APG for a documented reason), tell me and I'll treat them as accepted in future runs.

---

## Step 3b: Remediation code examples

For every FAIL or WARN finding, include a concrete code example showing the fix, placed directly under the finding it fixes, before the Scope block. Remediation guidance without code is advice; remediation guidance with code is a pull request waiting to happen. Write the example against the component's own source and stack, not a generic one, and don't replace the consumer's existing handlers: a fix that clones a child element must merge `onFocus`, `onBlur`, `onMouseEnter` and the rest with any the child already had.

**Format for each code example:**

```
Finding: [finding ID and short description]
Before (violation):
  [The exact code pattern that causes the failure]

After (fixed):
  [The corrected code with the specific change highlighted]

Why this fixes it:
  [One sentence explaining what changed and which WCAG criterion it satisfies]
```

**Examples by dimension:**

Screen reader — missing accessible name on icon button:
```
Before:
  <button><Icon name="close" /></button>

After:
  <button aria-label="Close dialog"><Icon name="close" aria-hidden="true" /></button>

Why: aria-label provides the accessible name. aria-hidden on the icon prevents
the icon name from being announced alongside the label. (WCAG 4.1.2)
```

Include the appropriate code example pattern for every FAIL finding. For WARN findings, include the example if the fix is clear; omit it if the finding requires contextual judgment that code alone cannot resolve.

---

## Step 3c: Complex component deep-dive protocol

Simple components (buttons, badges, basic inputs) tend to pass most checks. The real value of this skill is exposed on complex, high-CR components where accessibility failures are subtle and compound. When the target component is one of the following types, apply the extended protocol:

### Combobox / Autocomplete
Additional checks beyond the standard five dimensions:
- Does the listbox open on focus, on typing, or on a specific trigger? Is this consistent with the APG combobox pattern?
- Is the filtered result count announced as results change? (a polite live region; `aria-activedescendant` conveys the active option, not the count)
- Can the user select with Enter without the form submitting prematurely?
- What happens when no results match? Is this announced?
- Is the selected value persistent after closing and reopening?
- Can the user clear the selection with keyboard alone?

### DatePicker / Calendar
Additional checks:
- Is the calendar grid navigable with arrow keys (day-by-day horizontally, week-by-week vertically)?
- Does the month/year navigation wrap correctly at boundaries?
- Are disabled dates announced as disabled, not just visually greyed?
- Can the user type a date directly into the input field as an alternative to the calendar?
- Is each day's accessible name a spoken-form date in the user's locale (e.g. "Tuesday 9 March 2026"), not a numeric string that reads as digits?
- Is the calendar grid marked with `role="grid"` with correct row/cell roles?

### Data table
Additional checks:
- Are column headers marked with `scope="col"` or equivalent ARIA?
- Is sort state announced (aria-sort)?
- If it is an interactive grid (`role="grid"`), can the user navigate cell-by-cell with arrow keys? A static `<table>` should not add arrow-key cell navigation — screen readers already provide table navigation.
- Are action buttons within cells reachable without tabbing through every cell?
- Does pagination announce the new page content?
- Are row selection checkboxes grouped correctly?

### Modal / Dialog
Additional checks:
- Custom dialogs: is `aria-modal="true"` set, and is background content made `inert`? A native `<dialog>` opened with `showModal()` satisfies both — don't flag it for missing `aria-modal`.
- Can the user reach the close button without tabbing through all dialog content?
- Does the dialog have a visible, announced title?
- Are nested modals (dialog within dialog) handled correctly?

### Tabs
Additional checks:
- Does the implementation use `role="tablist"`, `role="tab"`, `role="tabpanel"` correctly?
- Are tabs navigable with arrow keys (not Tab)?
- Does focus stay on the tab when it is activated? Per the APG, arrow keys move between tabs and Tab moves into the panel; activation should not move focus to the panel.
- Is the `aria-selected` state correctly toggled between tabs?
- Disabled tabs: the APG allows either focusable-but-`aria-disabled` or removed from the arrow-key sequence; check the implementation picks one, applies it consistently, and announces the disabled state

For any component matching these types, run both the standard five-dimension audit AND the extended protocol. The extended protocol findings should be interleaved into the main report by dimension, not presented as a separate section.

---

## Quality checks

- All five dimensions are covered, not just contrast and keyboard navigation
- Focus management is assessed for every interactive state, not just the default state
- ARIA findings reference the APG pattern for the component type where relevant
- Contrast findings include actual contrast ratio figures, not just pass/fail
- Every PASS cites evidence from the running component or a computed ratio; code-only inferences are WARN
- The report ends with the Scope block and the invitation to flag deliberate deviations
- Every FAIL finding has a specific, actionable remediation with a code example
- The distinction between specification-level and implementation-level findings is clear
- Complex components (Combobox, DatePicker, DataTable, Modal, Tabs) receive the extended protocol in addition to the standard audit
- Code examples show both before (violation) and after (fix) with the specific WCAG criterion referenced, and preserve the consumer's existing handlers
- Runtime evidence (test-runner, axe, a transcript, screenshots) was found or asked for before the audit, and its absence is stated in the first line
