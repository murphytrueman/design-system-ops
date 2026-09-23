# Sample output: accessibility-per-component (fixture run)

**Skill:** `skills/accessibility-per-component`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `59a43fa`
**Eval case:** `tooltip-a11y` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools. Rerun it with `python3 tests/evals/run_evals.py --case tooltip-a11y`; runs vary, so expect the same findings in different words.

---

References verified, and both absence searches are proven to work on this codebase. Here's the audit.

---

## Accessibility audit: Tooltip

**Your Tooltip isn't a tooltip yet — it renders its content permanently, never associates it with a trigger, and has no show, hide, or dismiss behaviour. Every dimension except colour contrast fails. Fix the trigger association and the show/hide lifecycle first; everything else follows from those.**

**Audit date:** 2026-09-23
**WCAG level:** 2.2 AA
**Assessment method:** Source code only — `Tooltip.tsx`, `Tooltip.module.css`, and the token files. The package has no build, test, or Storybook tooling (`package.json` declares no scripts or devDependencies), so the component could not be rendered or tested with assistive technology.
**Config:** No `.ds-ops-config.yml` found — defaults apply. `severity.missing_aria` = critical, and keyboard and contrast gates block release.

---

### Overall status

❌ **FAIL** — four critical findings, each of which independently prevents a screen reader or keyboard user from receiving the tooltip's content as a tooltip.

---

### Results by dimension

| Dimension | Criterion | Result | Finding | Remediation |
|---|---|---|---|---|
| **Keyboard** 🔴 | Show on focus | ❌ FAIL | No `onFocus`/`onBlur` anywhere in `src`. Nothing shows or hides. (2.1.1) | F2 — add focus/blur handlers driving open state |
| | Trigger contract | ❌ FAIL | `children: ReactNode` is rendered untouched. The component neither requires nor guarantees a focusable trigger, and can't attach anything to one. (2.1.1) | F1 — narrow to `ReactElement`, clone with props |
| | Escape to dismiss | ❌ FAIL | No `onKeyDown` in `src`. No dismissal path. (1.4.13) | F3 — Escape handler on the trigger |
| | Arrow keys, skip/bypass | — | N/A. A tooltip is not a composite widget and holds no focus stops. | — |
| **Screen reader** 🔴 | Description association | ❌ FAIL | `Tooltip.tsx:13` has `role="tooltip"` but no `id`, and no `aria-describedby` exists anywhere in `src`. The role is inert. (1.3.1, 4.1.2) | F1 |
| | Role announcement | ❌ FAIL | Because it's unreferenced and always rendered, the label is exposed as stray static text next to the trigger on every page load, not as a description. (4.1.2) | F1 + F2 |
| | Name vs description | 🟡 Medium | For an icon-only trigger the tooltip is the trigger's *only* name and needs `aria-labelledby`, not `aria-describedby`. The API offers no way to express that. (2.5.3, 4.1.2) | F6 — add a `describes`/`labels` prop |
| | State, groups, live regions | — | N/A. Tooltips carry no state, no grouping, and must not be live regions. | — |
| **Contrast** 🟢 | Text, light theme | ✅ PASS | `#ffffff` on `#111827` = **17.74:1** (computed from `src/styles/tokens.css`). | — |
| | Text, dark theme | ✅ PASS | `#111827` on `#f9fafb` = **16.97:1** (computed from the `[data-theme="dark"]` block). | — |
| | Bubble boundary (1.4.11) | ✅ PASS | No border, but the fill contrasts against the page surface at the same ratios — well above 3:1 in both themes. | — |
| | Contrast durability | 🟡 Medium | The bubble binds `--color-text-default` as a *background*. It passes today by coincidence; a change to the text token silently changes the tooltip surface. | F5 — component-tier tokens |
| | Colour as sole indicator | — | N/A. No state is conveyed by colour. | — |
| **Focus mgmt** 🔴 | Show/hide lifecycle | ❌ FAIL | There is no open/close behaviour to manage. Note the APG requires the tooltip *not* take focus — focus stays on the trigger — so "focus moves into the layer" doesn't apply here. | F2 |
| | Focus not obscured (2.4.11) | ⚠️ WARN | `position: absolute` with no inset properties, no `z-index`, always rendered. The bubble will sit at its static position and overlay adjacent content — including, very likely, a focused control. Unverified: not rendered. | F4 |
| | Focus trap, focus visibility | — | N/A. Tooltips must not trap focus and contain no focusable elements. | — |
| **ARIA** 🔴 | Required attributes | ❌ FAIL | `role="tooltip"` requires an `id` referenced by the trigger. Neither exists. (4.1.2) | F1 |
| | Wrapper semantics | 🟡 Medium | `<span>` wrapping arbitrary `ReactNode`. A consumer passing a `<div>` produces invalid nesting and unpredictable layout. | F1 (also fixes this) |
| | Landmarks | — | N/A. | — |
| **Other** | Content on hover/focus (1.4.13) | ❌ FAIL | None of the three requirements met: not dismissible (no Escape), not hoverable (no pointer handlers, so no way to move onto the bubble), persistence undefined. | F2, F3 |
| | Text spacing (1.4.12) | ⚠️ WARN | No fixed heights found — good — but also no `max-width` or `width` constraint, so a long label is unbounded. Unverified: not rendered. | F4 |
| | Target size (2.5.8) | — | N/A to the tooltip itself. The trigger is consumer-supplied; document the 24×24 expectation. | — |

**Status key:** ✅ PASS / ⚠️ WARN / ❌ FAIL · 🔴 Critical / 🟠 High / 🟡 Medium

---

### Critical findings

**These four block release under the default keyboard gate.** All are the same root cause seen from different angles: the component renders tooltip *content* without implementing tooltip *behaviour*.

1. **The tooltip is invisible to assistive technology as a tooltip.** `role="tooltip"` does essentially nothing on its own — screen readers surface it only when a trigger points at it via `aria-describedby`. As written, the label is permanently present as loose text.
2. **There is no show/hide behaviour at all.** No state, no handlers. The bubble is always in the DOM and always painted.
3. **There is no dismissal path**, so 1.4.13 cannot be satisfied.
4. **The component cannot reach its own trigger.** With `children: ReactNode` it can't clone props onto the trigger, which is what makes fixes 1–3 possible. This is the one to fix first.

---

### Remediation

**F1–F3 — trigger association, show/hide lifecycle, Escape dismissal**

```
Before (violation): Tooltip.tsx
  export interface TooltipProps { label: string; children: ReactNode; }

  export function Tooltip({ label, children }: TooltipProps) {
    return (
      <span className={styles.wrapper}>
        {children}
        <span role="tooltip" className={styles.bubble}>{label}</span>
      </span>
    );
  }
```

```tsx
// After (fixed): Tooltip.tsx
import { cloneElement, useId, useState } from 'react';
import type { HTMLAttributes, KeyboardEvent, ReactElement } from 'react';
import styles from './Tooltip.module.css';

export interface TooltipProps {
  /** Tooltip text. Becomes the trigger's accessible description. */
  label: string;
  /** A single focusable element — receives aria-describedby and the handlers. */
  children: ReactElement<HTMLAttributes<HTMLElement>>;
}

export function Tooltip({ label, children }: TooltipProps) {
  const id = useId();
  const [open, setOpen] = useState(false);

  const handleKeyDown = (event: KeyboardEvent<HTMLElement>) => {
    if (event.key === 'Escape' && open) {
      event.stopPropagation();   // don't also close a surrounding dialog
      setOpen(false);
    }
    children.props.onKeyDown?.(event);
  };

  const trigger = cloneElement(children, {
    'aria-describedby': open ? id : undefined,
    onMouseEnter: () => setOpen(true),
    onFocus: () => setOpen(true),
    onBlur: () => setOpen(false),
    onKeyDown: handleKeyDown,
  });

  // onMouseLeave sits on the wrapper, not the trigger, so the pointer can
  // travel onto the bubble without dismissing it — 1.4.13 "hoverable".
  return (
    <span className={styles.wrapper} onMouseLeave={() => setOpen(false)}>
      {trigger}
      {open && <span id={id} role="tooltip" className={styles.bubble}>{label}</span>}
    </span>
  );
}
```

```
Why this fixes it:
  aria-describedby connects the trigger to the tooltip so the role becomes
  meaningful (4.1.2); focus/blur make it keyboard-operable (2.1.1); Escape
  and wrapper-level mouseleave satisfy dismissible and hoverable (1.4.13);
  ReactElement guarantees a single cloneable trigger rather than arbitrary
  nodes in a <span>.
```

**F4 — positioning, stacking, and width**

```
Before (violation): Tooltip.module.css
  .wrapper { position: relative; }
  .bubble  { position: absolute; padding: var(--space-gap); ... border-radius: 4px; }
```

```css
/* After (fixed) */
.wrapper {
  position: relative;
  display: inline-block;
}

.bubble {
  position: absolute;
  bottom: calc(100% + var(--space-gap));   /* was: no offsets at all */
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
  width: max-content;
  max-width: 20rem;                         /* bounds long labels */
  padding: var(--space-gap);
  background: var(--tooltip-background);
  color: var(--tooltip-text);
  border-radius: var(--tooltip-radius);
}
```

```
Why this fixes it:
  Explicit offsets and z-index lift the bubble clear of adjacent content
  instead of overlaying it at its static position, which is what puts a
  focused control at risk (2.4.11). max-width with width: max-content lets
  long labels wrap rather than run unbounded (1.4.12).
```

**F5 — component tokens (Medium; contrast durability, not a WCAG failure)**

`component.tokens.json` covers `button` and `card` only — there is no `tooltip` entry, which is why the CSS reaches for `--color-text-default` as a surface and hardcodes `border-radius: 4px`. Adding a tooltip block means the contrast pair is declared rather than incidental:

```json
"tooltip": {
  "background": { "$value": "{color.surface.inverse}" },
  "text":       { "$value": "{color.text.inverse}" },
  "radius":     { "$value": "{radius.sm}" }
}
```

`[needs data: color.surface.inverse, color.text.inverse and a radius scale don't exist in semantic.tokens.json or primitives.tokens.json — they need adding before this block resolves. The inverse pair should alias the same greys in use today (gray.900 / white) so the 17.74:1 and 16.97:1 ratios are preserved.]`

**F6 — name vs description (Medium)** — add a prop so an icon-only trigger can take the tooltip as its *name*: when set to label, emit `aria-labelledby={id}` instead of `aria-describedby={id}`. Without it, wrapping an icon button leaves it announced as just "button" (4.1.2), and a visible-label trigger risks a 2.5.3 Label in Name mismatch.

---

### Verifying the fix

Dimension 2 has FAILs, so confirm with a screen reader once the component can be rendered:

- **VoiceOver (macOS):** Cmd + F5 to toggle, then Tab to the trigger. You should hear the trigger's name and role, then the tooltip text as a description — not as separate text you have to arrow to.
- **NVDA (Windows, free from nvaccess.org):** Tab to the trigger and listen for the same.
- In both: press Escape and confirm the tooltip disappears and focus stays on the trigger.

---

**Scope**

- **Inspected:** `src/components/Tooltip/Tooltip.tsx`, `src/components/Tooltip/Tooltip.module.css`, `src/styles/tokens.css`, all three files in `tokens/`, `src/index.ts`, `package.json`. `Button.tsx` and `Card.tsx` were read only as comparison for the library's conventions.
- **Not inspected:** No rendered output, no assistive technology testing, no consuming application. `Tooltip` has no Storybook story — `Button.stories.tsx` and `Card.stories.tsx` exist, so the glob does find stories in this repo — and no test file or build tooling exists, so there is no way to render it from this repo.
- **How "none found" was checked:** The search for `onFocus|onBlur|onMouseEnter|onMouseLeave|onKeyDown|useState|useRef|aria-|tabIndex|cloneElement` returned zero matches across all of `src/`. A control search for `role=|onClick|onFocus|aria-describedby` over the same path does match `Tooltip.tsx:13`, so the attribute pattern works on this codebase — the absence is real, not a broken search. The CSS search for `:focus|:hover|display|visibility|z-index|max-width|inset|top:|left:|outline` matches `Button.module.css:8-18` but nothing in `Tooltip.module.css`, confirming the tooltip has no state styling or positioning.
- **Assumptions:** Contrast ratios are computed from the hex values in `src/styles/tokens.css` under the WCAG relative-luminance formula, assuming that file is the stylesheet loaded at runtime and that no consumer overrides the custom properties. Both themes were computed; no other theme was found.

If any of this is deliberate — for example if Tooltip is a known stub awaiting a positioning library like Floating UI, or if the trigger association is handled by consumers rather than the component — tell me and I'll treat it as accepted in future runs. The contrast result is genuinely good and needs no work; it's the behaviour layer that's missing.
