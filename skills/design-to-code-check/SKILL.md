---
name: design-to-code-check
description: "Compares a component or screen's design spec with its code and logs each gap as a build error or spec gap. Use it whenever someone asks if something matches its design or spec, even one component with the spec pasted in. System-wide drift: drift-detection."
references:
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/output-discipline.md
---

# Design-to-code check

A skill for reviewing the alignment between a design specification and its code implementation, producing a structured discrepancy report catalogued by dimension and severity.

## Before you begin: verify references

Before doing anything else, confirm that every file listed in this skill's frontmatter `references:` field exists at its relative path from this SKILL.md. If any are missing, stop — the install is incomplete. This usually means a third-party installer (for example `npx skills install`) flattened the skill into a standalone folder and dropped the repo-root `knowledge-notes/` directory this skill depends on. Tell the user to reinstall using a supported method from `1-INSTALL.md` (git clone, or the `.plugin` bundle in Cowork) and to run `verify-install.sh` from the install root to confirm the fix. Only proceed without the references if the user explicitly says to — and if they do, state clearly in your output that it was produced in degraded mode without the pack's reference material.

## Context

Design-to-code alignment reviews catch two different categories of problem. The first is implementation error — the developer built something different from what was specified, either by mistake or because the specification was unclear. The second is specification ambiguity — the design did not define behaviour completely enough for the developer to implement it correctly, and the developer made a reasonable guess that turned out to be wrong.

Both categories matter, but they require different responses. An implementation error needs to be corrected in the code. A specification ambiguity needs to be corrected in the design and documented, so the same guess does not get made again.

This skill produces a report that distinguishes between the two.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `severity.*` — discrepancy severity overrides, especially `specification_gap` and `missing_interaction_state`
- `system.framework` and `system.styling` — pre-select framework-specific checking guidance
- `integrations.figma` — the design specification (see below)
- `integrations.chromatic` — visual regression data as a supplementary signal
- `integrations.github` — the component source
- `gates.design_to_code` — if running as part of `component-to-release`, determines which findings block release

## Auto-pull integrations

**Figma MCP** (`integrations.figma.enabled: true`):
- Pull the component specification directly from `integrations.figma.file_key` via Figma MCP
- Read component properties, variant definitions, and layer structure as the design reference
- This replaces the need for the user to provide a Figma file link — the skill can say "I pulled the Button specification from your Figma library" and proceed immediately

**Chromatic** (`integrations.chromatic.enabled: true`):
- Pull the latest visual snapshots for the component being checked
- Use visual diffs between the Chromatic baseline and the current implementation as a supplementary signal for Dimensions 1–3 (spacing, colour, typography): it surfaces differences the manual review should confirm, never marks a dimension as matching

**GitHub** (`integrations.github.enabled: true`):
- If the component implementation is in the configured repo, pull the component source files directly
- Identify the component's last update date and recent changes to contextualise findings

## Step 1: Gather the comparison materials

Ask for or confirm (skip questions already answered by auto-pull):
- The design reference: Figma file link, exported specs, or described specification (skip if pulled from Figma MCP)
- The implementation reference: component in code (React, Vue, Twig, etc.), a link to a running implementation, or a description of what was built. Note the styling approach — CSS custom properties, SCSS variables, Tailwind utility classes, or CSS-in-JS — as this affects how token references are identified during the check.
- The component or screen being reviewed
- Whether this is a first-pass review or a follow-up check after a previous round of corrections
- Any known areas of concern the review should pay particular attention to

If both design and implementation are available directly, proceed to the check. If only one is available, note in the report which side of the comparison is inferred rather than directly inspected — dimensions that depend on the inferred side are reported as "not checked", not ✅.

## Step 1b: Design specification checklist

Before running the check, verify the design specification is complete enough to check against. Incomplete specs are the root cause of Type II (specification gap) findings — catching them upfront reduces noise in the report.

**Design specification completeness checklist:**
- [ ] All interactive states are defined (default, hover, active, focus, disabled, error, loading)
- [ ] Spacing values are specified using token names, not pixel values
- [ ] Colour values are specified using token names, not hex values
- [ ] Typography is specified using type scale tokens
- [ ] Responsive behaviour is defined for at least two breakpoints
- [ ] Focus indicator style is specified
- [ ] Content overflow behaviour is defined (truncation, wrapping, scrolling)
- [ ] Touch target sizes are specified for mobile breakpoints

**If the specification fails this checklist:** Note the missing items and proceed with the check. Missing specification items will appear as Type II findings in the report — but flagging them upfront sets the right expectation: these are design gaps, not implementation errors.

Share this checklist with designers as a pre-handoff tool. A specification that passes this checklist before handoff will produce a cleaner design-to-code check.

## Step 2: Run the check across all dimensions

Review alignment across five dimensions. For each dimension, the goal is not to produce a list of every difference — minor sub-pixel differences in a rounding pass are not discrepancies worth reporting. The goal is to identify differences that affect visual consistency, user experience, or system integrity.

### Dimension 1: Spacing and layout

Check:
- Padding and margin values: do they match design specifications, and are they using the correct spacing tokens?
- Element alignment: horizontal and vertical alignment of components within their containers
- Gap between elements in flex or grid layouts
- Component sizing: width and height where specified, or proportional behaviour where not fixed
- Responsive behaviour: does the implementation respond to breakpoints as specified?

Flag raw pixel values where spacing tokens should be used.

**Framework-specific notes for spacing checks:**
- **Vue SFC:** Check `<style>` blocks for raw `px` values. Token references may be SCSS variables (`$space-4`) or CSS custom properties (`var(--space-4)`).
- **Twig/Fractal:** Spacing is typically applied via BEM modifier classes or utility classes — check the backing SCSS, not just the template markup. Inline `style` attributes with pixel values are always violations.
- **Emotion/CSS-in-JS:** Check style objects and `css` prop values. Token references look like `theme.spacing(4)` or `theme.spacing.md`. String literals like `'16px'` or `'1rem'` are violations.
- **Tailwind:** Arbitrary values (`p-[13px]`, `bg-[#fff]`) are violations. Standard utility classes mapped to the token scale in the Tailwind config (`p-4`, `bg-primary`) count as token use.

### Dimension 2: Colour and visual treatment

Check:
- Background colours, border colours, text colours: are they referencing the correct design tokens?
- Shadow and elevation: correct values, correct token references
- Border radius: correct values, consistent with the design system's radius scale
- Opacity: correct values and applied to the correct element
- Gradient or background treatments if present

Flag any raw hex values, rgba values, or other hardcoded colour references where tokens should be used.

### Dimension 3: Typography

Check:
- Font family: correct typeface applied
- Font size: correct size, using the correct type token
- Font weight: correct weight at each text role
- Line height: correct leading, using the correct token or documented value
- Letter spacing: correct tracking where specified
- Text alignment: left, centre, right, or justified as designed
- Text truncation or overflow handling: does the implementation handle long strings as designed?

### Dimension 4: Interactive states

Check:
- Default state: visual treatment matches design
- Hover state: correct treatment applied on hover
- Active/pressed state: correct treatment on click or touch
- Focus state: visible, compliant focus indicator applied (this is also an accessibility check)
- Disabled state: correct reduced-prominence treatment
- Loading state: if designed, correctly implemented
- Error state: if applicable, correctly applied and correctly associated with the relevant element
- Empty state: if applicable, correctly implemented

Interactive states are the most commonly under-implemented dimension. Flag any state that was designed but is not present in the implementation.

### Dimension 5: Responsive and adaptive behaviour

Check:
- Breakpoint transitions: does the layout change at the designed breakpoints?
- Component behaviour at narrow viewports: does anything break, overflow, or truncate unexpectedly?
- Touch target sizing: are interactive elements at least 24×24 CSS px (WCAG 2.5.8, AA)? 44×44 CSS px is the AAA bar (2.5.5). Platform guidance is 44pt on iOS and 48dp on Android — use whichever the spec or team adopts, and say which.
- Content reflow: does text reflow correctly at all breakpoints?

## Step 3: Classify each discrepancy

For each discrepancy found, classify it:

**Type I: Implementation error**
The specification was clear. The implementation does not match it. Correct in code.

**Type II: Specification gap**
The design did not define this case. The implementation made a reasonable assumption. Update the design specification to document the intended behaviour, then align the implementation.

**Type III: System inconsistency**
The design itself diverges from the design system (uses a non-system colour, a spacing value not on the scale, etc.). The issue is in the design file, not the implementation.

**Type IV: Accepted divergence**
A known, intentional difference — typically a technical constraint the design did not account for. Should be documented if it is not already.

## Step 3b: Hand-offs (only on request)

- **Prop API contract** (missing, undocumented, or mis-defaulted props): run component-api-validator rather than checking it here.
- **AI description drift** (six-section description no longer matches the build): run ai-component-description to regenerate or validate it.

## Step 4: Produce the report

---

### Design-to-code check report

Open with a headline sentence that tells the reader the overall state and where to focus.

**Component/screen:** [name]
**Design reference:** [Figma link or description]
**Implementation reference:** [link or description]
**Review date:** [date]
**Review round:** [first pass / follow-up]

---

#### Summary

One paragraph. What is the overall alignment? Are discrepancies concentrated in a particular dimension? Is the work concentrated in a few fixes, or does it need significant rework?

---

#### Discrepancy log

| ID | Dimension | Type | Severity | Element | Design spec | Implementation | Action |
|---|---|---|---|---|---|---|---|
| DC-01 | [dimension] | [I–IV] | 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low | [specific element] | [what the design says] | [what was implemented] | [who does what] |

Severity guidance:
- 🔴 Critical: accessibility regression — focus that isn't visible (outline removed with nothing replacing it), insufficient colour contrast, or a component that can't be reached or operated by keyboard
- A focus style the spec never defined, where the browser's default focus ring still shows, is a 🟠 High Type II spec gap rather than a regression: focus is visible, it just isn't designed. Check the CSS for `outline: none` / `outline: 0` before calling it Critical
- 🟠 High: visible to end users, affects perceived quality or usability
- 🟡 Medium: system inconsistency (hardcoded value, wrong token), visible under close inspection
- ⚪ Low: minor difference without user-facing impact

---

#### Summary by dimension

One line per dimension: ✅ PASS (compared, no discrepancies, with the evidence named), ⚠️ WARN (Medium or Low discrepancies only), ❌ FAIL (any Critical or High discrepancy), or **not checked** (one side was inferred or unavailable — say which). Helps the team understand where the work is concentrated.

---

#### Specification gaps identified

List any Type II findings separately. These require action from the designer, not the developer, and should be tracked as design tasks rather than development bugs.

---

**Scope**
- **Inspected:** [design source (Figma node, export, description) and implementation files or running build actually compared]
- **Not inspected:** [states, breakpoints, or variants not available on one side]
- **How "none found" was checked:** [for any ✅ dimension, what was compared — e.g. computed styles against Figma values for each state]
- **Assumptions:** [e.g. the Figma frame is the current approved spec]

If any of these discrepancies are deliberate (a known constraint or an agreed divergence), tell me and I'll log them as Type IV in future runs.

---

## Quality checks

- Discrepancies include both what the design specifies and what was implemented — not just "colour is wrong"
- Type I (error) and Type II (spec gap) findings are clearly distinguished — they need different owners
- Interactive states are checked thoroughly, not just the default state
- Token compliance is checked as part of the colour and spacing dimensions — not just visual correctness
- Accessibility regressions (invisible focus, insufficient contrast, no keyboard access) are always Critical; an undesigned focus style with the browser default still visible is High
- The report is specific enough to act on without a follow-up conversation
