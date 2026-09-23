# Sample output: accessibility-per-component (fixture run)

**Skill:** `skills/accessibility-per-component`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it
**Eval case:** `tooltip-a11y` in `tests/evals/cases.json`
**Date:** 2026-09-23
**Edited:** no. Everything below the line is exactly what the skill produced in a headless run with read-only tools. Rerun it with `python3 tests/evals/run_evals.py --case tooltip-a11y`.

---

Skill install verified (`knowledge-notes/output-discipline.md` present). No `.ds-ops-config.yml` in the repo, so defaults apply: missing/incorrect ARIA = 🔴 Critical, keyboard and contrast FAILs block release.

---

# Accessibility audit: Tooltip

**This component does not currently work as a tooltip for anyone using a keyboard or a screen reader** — the label is permanently rendered with no show/hide state, and nothing connects it to the element it describes. Contrast is the one dimension that's genuinely clean. Start with findings A and B; everything else follows from them.

**Audit date:** 2026-09-23
**WCAG level:** 2.2 AA
**Assessment method:** source inspection only — `Tooltip.tsx`, `Tooltip.module.css`, `src/styles/tokens.css`. No Storybook story, test, or build tooling exists for this component (`Button` and `Card` both have `.stories.tsx`; `Tooltip` has none, and `package.json` declares no scripts or devDependencies), so there is no running component to test.
**Additional context:** No assistive technology testing performed.

---

## Overall status

❌ **FAIL**

Per the evidence rule, behavioural criteria assessed from code alone cannot be marked PASS. Contrast is the only ✅ here because it comes from computed ratios against the token file.

---

## Results by dimension

| Dimension | Criterion | Result | Finding | Remediation |
|---|---|---|---|---|
| Keyboard | Trigger focusability | ❌ FAIL | `children: ReactNode` is rendered untouched inside a `<span>`. Nothing guarantees the trigger is focusable, and the component adds no `tabIndex`. A non-interactive child (icon, text) is unreachable by keyboard. (2.1.1) | Require a focusable element as the trigger; clone it to attach handlers. See **Fix C**. |
| Keyboard | Show on focus | ❌ FAIL | No `onFocus`/`onBlur` handlers anywhere in `Tooltip.tsx`. | **Fix C** |
| Keyboard | Escape dismissal | ❌ FAIL | No `onKeyDown` or key handling in the file. (1.4.13) | **Fix C** |
| Screen reader | Trigger↔tooltip association | ❌ FAIL | `Tooltip.tsx:13` sets `role="tooltip"` but the bubble has no `id` and nothing sets `aria-describedby`. `role="tooltip"` on its own conveys nothing — it is inert without a reference from the described element. The label text is read as stray adjacent content instead. (1.3.1, 4.1.2) | **Fix B** |
| Screen reader | State announcement | ❌ FAIL | There is no open/closed state to announce, because there is no state. (4.1.2) | **Fix A** |
| Contrast | Text contrast, light theme | ✅ PASS | Bubble is `--color-text-default` (#111827) behind `--color-surface-base` (#ffffff). Computed: **17.7:1** — well past the 4.5:1 AA minimum, and past AAA. | None |
| Contrast | Text contrast, dark theme | ✅ PASS | `[data-theme="dark"]` flips both tokens, so the bubble becomes #111827 text on #f9fafb. Computed: **17.0:1**. The token indirection gives correct theme inversion for free. | None |
| Contrast | Colour as sole indicator | ✅ PASS | The tooltip conveys meaning through text, not colour. | None |
| Focus | Focus indicator | ⚠️ WARN | No `:focus` or `:focus-visible` rule exists in `Tooltip.module.css` — or anywhere under `src/`. The trigger is consumer-supplied, so this may be the consumer's job, but the library sets no baseline. (2.4.7) | Document the focusable-trigger contract; consider a library-wide focus ring. |
| Focus | Focus not obscured | ⚠️ WARN | `.bubble` is `position: absolute` with **no `top`/`left`/`bottom` and no `z-index`** (`Tooltip.module.css:5–11`). It renders at its static position, overlapping whatever follows, permanently. A focused control behind it would be obscured. (2.4.11) | **Fix D** |
| ARIA | Role appropriateness | ⚠️ WARN | `role="tooltip"` is the right role for the APG tooltip pattern, but the pattern requires the trigger to reference it. Correct role, incomplete pattern. | **Fix B** |
| ARIA | Content on hover or focus | ⚠️ WARN | 1.4.13 does not bind today — nothing is hover- or focus-triggered, so the label is just static content. It becomes a hard requirement (dismissible, hoverable, persistent) the moment show/hide lands. | **Fix A** + **Fix C** |
| ARIA | Text spacing | ⚠️ WARN | No `max-width` or `width` on `.bubble`. Long labels stretch to the containing block and may overflow the viewport under increased spacing. (1.4.12) | **Fix D** |
| Keyboard | Target size (2.5.8) | — N/A | The Tooltip renders no pointer target of its own; the trigger is consumer-owned. | — |

**Status key:** ✅ PASS / ⚠️ WARN / ❌ FAIL

---

## Critical findings

**A. 🔴 The tooltip is never hidden.** `Tooltip.tsx:13` renders the bubble unconditionally, and `Tooltip.module.css` contains no `display`, `visibility`, `opacity`, or `:hover` rule. There is no `useState` in the file. As shipped, the label is always on screen and always in the accessibility tree.

This is the finding I'd most like your read on. If consuming apps are expected to supply their own visibility CSS, say so and I'll treat it as accepted — but it isn't documented anywhere I inspected, and the component is exported from `src/index.ts` as if it were complete. I've assumed it's a gap and written the remediation accordingly.

**B. 🔴 `role="tooltip"` with no `aria-describedby`.** Under the team's default severity config, missing ARIA is critical. A screen reader user gets the label as loose text near the trigger, with no indication of what it describes — and in a list of several tooltips, no way to tell which belongs to which.

**C. 🔴 No keyboard path at all.** No focus handlers, no Escape, no guarantee the trigger is focusable. A keyboard-only user has no route to this content once A is fixed, and no route out of it before then.

---

## Remediation

### Fix A + B + C — state, association, and keyboard (`Tooltip.tsx`)

```
Finding: A, B, C — no show/hide state, no aria-describedby, no keyboard support

Before (violation):
  export function Tooltip({ label, children }: TooltipProps) {
    return (
      <span className={styles.wrapper}>
        {children}
        <span role="tooltip" className={styles.bubble}>{label}</span>
      </span>
    );
  }

After (fixed):
  import { cloneElement, useEffect, useId, useState } from 'react';
  import type { ReactElement } from 'react';

  export interface TooltipProps {
    label: string;
    /** Must be a single focusable element — the tooltip describes it. */
    children: ReactElement;
  }

  export function Tooltip({ label, children }: TooltipProps) {
    const id = useId();
    const [open, setOpen] = useState(false);

    useEffect(() => {
      if (!open) return;
      const onKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') setOpen(false);
      };
      document.addEventListener('keydown', onKeyDown);
      return () => document.removeEventListener('keydown', onKeyDown);
    }, [open]);

    const trigger = cloneElement(children, {
      'aria-describedby': open ? id : undefined,
      onFocus: () => setOpen(true),
      onBlur: () => setOpen(false),
    });

    return (
      <span
        className={styles.wrapper}
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
      >
        {trigger}
        {open && <span id={id} role="tooltip" className={styles.bubble}>{label}</span>}
      </span>
    );
  }

Why this fixes it:
  aria-describedby links the trigger to the tooltip so it is announced as that
  element's description (1.3.1, 4.1.2); onFocus/onBlur give keyboard users the
  same access as pointer users (2.1.1); Escape makes it dismissible and the
  hover handlers on the wrapper — rather than the trigger — keep it open while
  the pointer moves onto the bubble, satisfying all three parts of 1.4.13.
```

Two things to verify with a real screen reader rather than trust from code: that the description is announced on focus (the reference is added in the same render that mounts the bubble, and AT timing here varies), and that `cloneElement` doesn't clobber an `onFocus` the consumer already passed — if consumers do that, compose the handlers instead of overwriting.

### Fix D — positioning and width (`Tooltip.module.css`)

```
Finding: D — bubble has no offset, stacking context, or width bound

Before (violation):
  .bubble {
    position: absolute;
    padding: var(--space-gap);
    background: var(--color-text-default);
    color: var(--color-surface-base);
    border-radius: 4px;
  }

After (fixed):
  .bubble {
    position: absolute;
    bottom: 100%;
    left: 0;
    z-index: 1;
    width: max-content;
    max-width: 20rem;
    padding: var(--space-gap);
    background: var(--color-text-default);
    color: var(--color-surface-base);
    border-radius: 4px;
  }

Why this fixes it:
  An explicit offset and z-index stop the bubble resolving to its static
  position and sitting over adjacent focusable content (2.4.11); max-content
  with a max-width lets long labels wrap instead of clipping or overflowing
  under increased text spacing (1.4.12).
```

`.wrapper` already has `position: relative`, so it is a correct containing block once offsets are set — no change needed there.

---

## Verifying the screen reader fixes

Dimension 2 has FAILs, so confirm these by ear before closing them out:

- **VoiceOver (macOS):** Cmd + F5 to toggle. Tab to the trigger and listen for the label as a *description* following the trigger's own name and role — not as separate text.
- **NVDA (Windows, free from nvaccess.org):** Tab to the trigger; the description should follow the role announcement.
- In both: Tab onto the trigger, confirm the tooltip appears and is announced, press Escape, confirm it disappears and focus stays put.

A `Tooltip.stories.tsx` would make this repeatable — `Button` and `Card` already have one, so the convention exists.

---

**Scope**
- **Inspected:** `src/components/Tooltip/Tooltip.tsx`, `src/components/Tooltip/Tooltip.module.css`, `src/styles/tokens.css`, `src/index.ts`, `package.json`. Cross-checked `Button.module.css` for the library's styling conventions.
- **Not inspected:** No running component, Storybook, or build — none exists in this repo. No screen reader, keyboard, or browser testing. No consuming application, so I can't see what triggers teams actually pass as `children`. No design file.
- **How "none found" was checked:** The absence claims for `:focus`, `onKeyDown`, `useState`, and `aria-describedby` come from a single regex across `src/` that also included `Tooltip` as a control term — it returned the `Tooltip` matches, so the search reaches these files. `Button.module.css:13` contains a `:hover` rule, confirming the pattern form matches pseudo-classes in this codebase. `src/components/Tooltip/` contains exactly two files, so there is no separate story or test file I missed.
- **Assumptions:** The token values in `src/styles/tokens.css` are what actually renders (the file's own header says it is generated from `tokens/*.tokens.json`, which I did not diff against it). Contrast ratios assume the bubble renders over its own opaque background, which the CSS sets. Finding A assumes the always-visible rendering is unintentional.

If any of this is deliberate — particularly the always-visible bubble, or leaving trigger focusability and focus rings to consumers — tell me and I'll mark those accepted so future runs skip them and focus on what's actually open.
