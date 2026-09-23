# Sample output: AI component description

**Skill:** `skills/ai-component-description`
**Source:** Product design system (name withheld) — Dialog component (React 18, TypeScript, Radix UI primitives, Tailwind v3)
**Output format:** Figma MCP description field (plain text, six sections)
**Existing description:** "A modal overlay for confirmations and decisions." (Shown to user before writing — user chose to replace with full AI-optimised description.)

---

## Figma component description

The following text block is the complete output, formatted for pasting into a Figma component description field. Section headers are plain text (not markdown) because Figma's description field does not render markdown.

---

PURPOSE

A modal overlay that interrupts the current workflow to require a decision or confirmation before the user can continue. Use it for confirmations, destructive action gates, form collection that blocks the parent flow, or critical information that must be acknowledged. For non-blocking information use Toast (success confirmations), Banner (persistent warnings) or Popover (contextual details that need no decision). For long-form content, or when the user needs to reference the page behind, use Sheet.

PROPS

open; boolean; false; Controls visibility. Use as a controlled component with onOpenChange. When true, renders a backdrop overlay and traps focus inside.
onOpenChange; (open: boolean) => void; required; Called with false on Escape, backdrop click or the close button. The parent decides whether to actually close.
title; string; required; Header title, announced via aria-labelledby. Under 60 characters; describe the decision ("Delete 12 items?"), not the content.
description; string; no default; Optional secondary text below the title, announced via aria-describedby. Use for consequences or context.
size; "sm" | "md" | "lg"; "md"; Max-width: sm 400px (simple confirmations), md 520px (forms), lg 680px (complex multi-step content).
closeOnBackdropClick; boolean; true; Set to false for destructive confirmations to force an explicit button choice.
children; ReactNode; required; Body content between header and footer. Dialog does not provide a form element; wrap forms yourself.
footer; ReactNode; no default; Action area, accepting Button components. Cancel on the left, confirm on the right. If omitted, only the header close button renders.

ANTI-PATTERNS

Do not use Dialog for success messages. "Saved successfully" with only an OK button is an unnecessary interruption; use Toast.
Do not nest dialogs. Close the first, then open the second.
Do not use size lg for simple yes/no confirmations. Two sentences in a 680px dialog look empty; use sm.
Do not put scrollable content in Dialog without visual scroll indicators. Use Sheet for long-form content, or add a visible scroll shadow to the body.
Do not rely on backdrop click as the only dismissal. Keyboard and screen reader users need an explicit close button or cancel action; Escape works but is not discoverable.

COMPOSITION

Dialog is a compound component (backdrop, container, header, body, footer) used as a single unit; sub-parts are not exposed.
It renders into a React portal at the document root and can be triggered from any context.
Footer patterns: confirmations use a secondary cancel (left) and a primary or destructive confirm (right). Information dialogs use a single primary button ("Got it" or "Close"). Multi-step flows use Back (secondary, left) and Next (primary, right) with step indicators in the body.
With a form in the body, the confirm button is type="submit" and the form's onSubmit calls onOpenChange(false) on success.

ACCESSIBILITY

Role: dialog, from the Radix UI Dialog primitive. The container has role="dialog", aria-modal="true", aria-labelledby pointing to the title, and aria-describedby pointing to the description if present. The backdrop has aria-hidden="true" and is not announced.
Focus: on open, focus moves to the first focusable element inside the dialog. Tab and Shift+Tab cycle within the dialog and cannot reach the page behind. On close, focus returns to the trigger.
Keyboard: Escape calls onOpenChange(false). Enter activates the focused button or submits a form.
Close button: the header close icon button has aria-label="Close dialog". It is always present, even when the footer has a cancel button.

EXAMPLES

Intent: destructive confirmation from a settings page row action menu.
Configuration: title "Delete workspace?", description "This will permanently delete the workspace and all 47 projects inside it. This action cannot be undone.", size sm, closeOnBackdropClick false, footer with secondary "Cancel" (left) and destructive "Delete workspace" (right).
Expected DOM output:
  <div role="dialog" aria-modal="true" aria-labelledby="[title id]" aria-describedby="[description id]">
    [title, description]
    <button aria-label="Close dialog">...</button>
    <button>Cancel</button>
    <button>Delete workspace</button>
  </div>

Intent: form collection from a list view.
Configuration: title "Create new project", size md, body form with name input, description textarea and team select, footer with secondary "Cancel" (left) and primary "Create project" as type="submit" (right). On success the dialog closes and a toast confirms creation.

Intent: information acknowledgement in onboarding.
Configuration: title "Your trial starts today", description "You have 14 days to explore all features. No credit card required.", size sm, footer with a single primary "Got it" button.

---

## Self-test result

1. **Can an LLM identify this component for a given requirement?** Yes — the purpose section routes between Dialog and its alternatives.
2. **Can it configure the right props?** Yes — all 8 user-facing props are documented with accepted values, defaults, and the controlled component pattern.
3. **Can it avoid the common misuse patterns?** Yes — 5 anti-patterns cover success messages in dialogs, nested dialogs, oversized simple confirmations, unindicated scrolling, and missing close mechanisms.
4. **Does it understand placement constraints?** Yes — composition covers portal rendering, footer layout conventions, and form integration.
5. **Can it apply the component accessibly?** Yes — focus trapping, focus restoration, keyboard behaviour, aria labelling, and the always-present close button are documented.
6. **Can it distinguish Dialog from similar components?** Yes — Toast, Banner, Popover and Sheet are each named with the case they cover instead.
7. **Can it generate a correct usage example?** Yes — three examples cover destructive confirmation, form collection and acknowledgement, and the first gives an expected DOM structure to validate against.

**Word count:** ~690 (within the 400–700 target)

---

*Generated by [Design System Ops by Murphy Trueman](https://www.murphytrueman.com) — `skills/ai-component-description` skill*
*Source: Product design system, name withheld (React 18, TypeScript, Radix UI, Tailwind v3)*
