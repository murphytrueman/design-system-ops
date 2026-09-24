# Sample output: accessibility-per-component (fixture run)

**Skill:** `skills/accessibility-per-component`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `27c301d`
**Eval case:** `tooltip-a11y` in `tests/evals/cases.json`
**Date:** 2026-09-24
**Edited:** no. The report below is verbatim from a headless run with read-only tools; `tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case tooltip-a11y`; runs vary, so expect the same findings in different words.

---

# Accessibility audit: Tooltip

**This component has no runtime evidence available, so only contrast could be verified — and it's the one thing that's fine.** Everything else reads as broken in source: the tooltip is never associated with its trigger, has no show/hide behaviour at all, and can't be dismissed. Under this skill's evidence rule those stay ⚠️ WARN (unverified) rather than FAIL, but I'd expect all four 🔴 rows to confirm the moment you put a story in front of axe.

**Audit date:** 2026-09-24
**WCAG level:** 2.2 AA
**Assessment method:** source only — `Tooltip.tsx`, `Tooltip.module.css`, resolved token values from `src/styles/tokens.css`
**Runtime evidence:** none found. `Tooltip` is the only component in `src/components/` without a `.stories.tsx` (Button, Card, Modal and Dialog each have one), and `package.json` declares no devDependencies, scripts, or test tooling — no Storybook config, no `jest-axe`/`vitest-axe`, no Playwright. Per the skill's evidence rule, every keyboard, screen-reader and focus criterion below is **WARN (unverified)**; only contrast, computed from resolved token values, can PASS or FAIL.

---

## Overall status

⚠️ **WARN** — no criterion could be confirmed against a running component. Four rows carry 🔴 Critical severity.

---

## Results by dimension

| Dimension | Criterion | Result | Severity | Evidence | Finding | Remediation |
|---|---|---|---|---|---|---|
| Keyboard | Trigger / activation (2.1.1) | ⚠️ WARN | 🔴 | `Tooltip.tsx:9-15`; `Tooltip.module.css:5-11` | No state, no `onFocus`/`onMouseEnter`, and no `display`/`opacity`/`visibility` rule — the bubble renders unconditionally. There is nothing to activate, by keyboard or pointer | Add open state driven by focus and hover — see **Fix 1** |
| Keyboard | Escape to dismiss (1.4.13) | ⚠️ WARN | 🟠 | `Tooltip.tsx:9-15` | No `onKeyDown`; Escape does nothing | **Fix 1** |
| Keyboard | Tab order (2.1.1) | ⚠️ WARN | 🟡 | `Tooltip.tsx:11-14` | The wrapper `<span>` adds no `tabindex` and passes `children` through untouched, so it neither helps nor harms tab order. But nothing in the API requires the child to be focusable — a consumer wrapping an icon `<span>` gets a tooltip no keyboard user can reach | Type `children` as a single `ReactElement` and document that it must be focusable — **Fix 1** |
| Screen reader | Description association (4.1.2, 1.3.1) | ⚠️ WARN | 🔴 | `Tooltip.tsx:13` | `role="tooltip"` is set, but the element has no `id` and nothing points at it with `aria-describedby`. A tooltip role is only surfaced to AT when referenced — as written, the label is never announced as the trigger's description | **Fix 1** |
| Screen reader | Reading order (1.3.2) | ⚠️ WARN | 🟠 | `Tooltip.tsx:13` + no hide rule in CSS | Because the bubble is permanently in the DOM *and* visible, a screen reader browsing linearly reads the label as loose text after the trigger, unattached to it. A user navigating by Tab hears nothing | **Fix 1** (hiding it until open removes the stray text) |
| Screen reader | State announcement (4.1.2) | ⚠️ WARN | 🟡 | `Tooltip.tsx:4-7` | No expanded/collapsed state exists to announce. Once **Fix 1** lands, `aria-describedby` carries the description and no extra state attribute is needed — don't add `aria-expanded`, it isn't part of the APG tooltip pattern | Covered by **Fix 1** |
| Contrast | Text contrast, light theme (1.4.3) | ✅ **PASS** | — | `#ffffff` on `#111827` = **17.7:1** (`--color-surface-base` on `--color-text-default`, `tokens.css:5,8`) | Well clear of 4.5:1 | — |
| Contrast | Text contrast, dark theme (1.4.3) | ✅ **PASS** | — | `#111827` on `#f9fafb` = **17.0:1** (`tokens.css:28-29`) | Token inversion holds up in both themes | — |
| Contrast | Bubble boundary (1.4.11) | ✅ **PASS** | — | Same pairs as above against `--color-surface-base` and `--color-surface-raised` (`#f9fafb`, 17.0:1) | The background carries the boundary; no border needed at these ratios | — |
| Contrast | Forced colours | ⚠️ WARN | 🟡 | `Tooltip.module.css:5-11` | No border and no `forced-color-adjust`. Under `@media (forced-colors: active)` both `background` and `color` are replaced by system colours, so the bubble flattens into whatever it overlaps | Add a transparent border that picks up `CanvasText` — **Fix 3** |
| Contrast | Colour alone (1.4.1) | ✅ PASS | — | `Tooltip.tsx:13` — content is the `label` string | Meaning is carried by text | — |
| Focus | Focus not obscured (2.4.11) | ⚠️ WARN | 🟠 | `Tooltip.module.css:6` | `position: absolute` with no `inset`/`top`/`left` and no `z-index`. The bubble sits at its static position but out of flow, overlapping whatever follows it — including, potentially, a focused control's focus ring | Position it explicitly above the trigger with a stacking context — **Fix 2** |
| Focus | Focus on open / close | ⚠️ WARN | 🟠 | `Tooltip.tsx:9-15` | No open/close cycle exists, so there is no focus-triggered show path — the "on focus" half of 1.4.13 is simply absent. Note the APG tooltip pattern deliberately does *not* move focus into the bubble; **Fix 1** keeps focus on the trigger | **Fix 1** |
| Focus | Focus visibility (2.4.7) | ⚠️ WARN | 🟡 | `Tooltip.module.css` (no `:focus`/`:focus-visible` rule) | Component defines no focus styling, inheriting whatever the consumer's trigger provides. Defensible for a wrapper, but it means the tooltip makes no guarantee | Leave to the trigger; state it in the component docs |
| ARIA | Required attributes for role | ⚠️ WARN | 🔴 | `Tooltip.tsx:13` | `role="tooltip"` without the referencing `aria-describedby` is the incomplete half of a two-part contract. There's no `id` prop and no ref/prop plumbing to the child that would let a consumer complete it themselves | **Fix 1** |
| ARIA | Prohibited patterns | ⚠️ WARN | 🟠 | `Tooltip.tsx:13` | ARIA is present but inert — the role is on a `<span>` nothing references. This is worse than no ARIA, because it reads as handled in review | **Fix 1** |
| ARIA | Landmarks | ✅ N/A | — | — | Not a page region | — |
| Other | Reflow / text spacing (1.4.10, 1.4.12) | ⚠️ WARN | 🟡 | `Tooltip.module.css:5-11` | No `max-width` and no `width` constraint on an absolutely positioned box. A long `label` can run past the viewport at 320 CSS px. No fixed height, so clipping is unlikely | Constrain width — **Fix 2** |
| Other | Target size (2.5.8) | ✅ N/A | — | `Tooltip.tsx:12` | The trigger is consumer-supplied; the component adds no pointer target | — |

**Status key:** ✅ PASS / ⚠️ WARN / ❌ FAIL. Severity: 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low.

---

## Critical findings

Nothing can be recorded as FAIL without a running component, but these four 🔴 rows share a single root cause and would each block release under the default gates (`gates.accessibility.keyboard_blocks_release: true`, `severity.missing_aria: critical`):

1. **The tooltip is never connected to its trigger.** `role="tooltip"` with no `id` and no `aria-describedby` on the child means the label is not exposed as a description to any assistive technology.
2. **There is no show/hide behaviour whatsoever.** No state, no handlers, no CSS hiding rule — the bubble is always rendered and always visible. It isn't a tooltip yet; it's a permanently visible label positioned on top of adjacent content.
3. **No Escape dismissal**, required by 1.4.13.
4. **No keyboard path**, because there is nothing to trigger.

All four are fixed by Fix 1.

---

## Remediation

### Fix 1 — associate, gate on focus/hover, dismiss on Escape

Covers: trigger/activation, Escape, tab order, description association, reading order, state announcement, focus on open/close, required ARIA attributes, prohibited patterns.

**Before (violation)** — `src/components/Tooltip/Tooltip.tsx`:

```tsx
import type { ReactNode } from 'react';
import styles from './Tooltip.module.css';

export interface TooltipProps {
  label: string;
  children: ReactNode;
}

export function Tooltip({ label, children }: TooltipProps) {
  return (
    <span className={styles.wrapper}>
      {children}
      <span role="tooltip" className={styles.bubble}>{label}</span>
    </span>
  );
}
```

**After (fixed):**

```tsx
import { cloneElement, isValidElement, useId, useState } from 'react';
import type { FocusEvent, KeyboardEvent, ReactElement } from 'react';
import styles from './Tooltip.module.css';

export interface TooltipProps {
  label: string;
  /** A single focusable element. The tooltip describes it via aria-describedby. */
  children: ReactElement;
}

export function Tooltip({ label, children }: TooltipProps) {
  const id = useId();
  const [open, setOpen] = useState(false);

  if (!isValidElement(children)) {
    throw new Error('Tooltip expects a single focusable element as its child.');
  }

  // Merge with whatever the consumer already passed — never replace their handlers.
  const childProps = children.props as Record<string, unknown>;
  const describedBy = [childProps['aria-describedby'], id].filter(Boolean).join(' ');
  const chain = <E,>(theirs: unknown, mine: (event: E) => void) => (event: E) => {
    (theirs as ((event: E) => void) | undefined)?.(event);
    mine(event);
  };

  const trigger = cloneElement(children, {
    'aria-describedby': describedBy,
    onFocus: chain<FocusEvent>(childProps.onFocus, () => setOpen(true)),
    onBlur: chain<FocusEvent>(childProps.onBlur, () => setOpen(false)),
  });

  return (
    <span
      className={styles.wrapper}
      // Hover lives on the wrapper so the bubble stays open while the pointer
      // is over the bubble itself (1.4.13 Hoverable).
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      onKeyDown={(event: KeyboardEvent) => {
        if (event.key === 'Escape' && open) {
          event.stopPropagation();
          setOpen(false);
        }
      }}
    >
      {trigger}
      <span id={id} role="tooltip" hidden={!open} className={styles.bubble}>
        {label}
      </span>
    </span>
  );
}
```

**Why this fixes it:** `aria-describedby` pointing at the tooltip's `id` is what makes `role="tooltip"` reachable by assistive technology, so the label is announced with the trigger (4.1.2, 1.3.1). Gating on `onFocus`/`onBlur` gives keyboard users the same access as pointer users (2.1.1). Escape handling plus wrapper-level hover satisfies 1.4.13's dismissible and hoverable requirements, and `hidden` removes the stray text from the reading order (1.3.2). Focus never leaves the trigger, per the APG tooltip pattern. `chain()` calls the consumer's handler before ours, so an existing `onFocus` on the child still runs.

### Fix 2 — position explicitly and constrain width

Covers: focus not obscured, reflow/text spacing.

```
Before:
  .wrapper { position: relative; }
  .bubble  { position: absolute; padding: var(--space-gap); … }

After:
  .wrapper {
    position: relative;
    display: inline-block;   /* an inline box is an unreliable containing block */
  }

  .bubble {
    position: absolute;
    bottom: calc(100% + var(--space-gap));   /* above the trigger, out of the way */
    left: 50%;
    transform: translateX(-50%);
    z-index: 1;
    width: max-content;
    max-width: 24ch;                          /* survives 320px and 200% text */
    padding: var(--space-gap);
    …
  }

  .bubble[hidden] { display: none; }
```

**Why this fixes it:** an absolutely positioned box with no `inset` stays at its static position, overlapping following content and any focus ring under it. Anchoring it above the trigger with an explicit stacking context keeps focused controls visible (2.4.11); `max-width` stops a long label overflowing at 320 CSS px (1.4.10, 1.4.12).

### Fix 3 — survive forced colours

```
Before:
  .bubble { background: var(--color-text-default); color: var(--color-surface-base); }

After:
  .bubble { …; border: 1px solid transparent; }

  @media (forced-colors: active) {
    .bubble { border-color: CanvasText; }
  }
```

**Why this fixes it:** Windows High Contrast replaces `background` and `color` with system colours, flattening the bubble into the content beneath it. A border that resolves to `CanvasText` keeps the boundary visible without changing the default rendering.

---

## Verifying the fixes with a screen reader

Dimension 2 has no confirmed results, so check these by hand once Fix 1 lands:

- **VoiceOver (macOS):** Cmd + F5 to toggle. Tab to the trigger — you should hear the trigger's own name and role, then the tooltip label as its description. Press Escape; Tab away and back to confirm it reappears.
- **NVDA (Windows, free from nvaccess.org):** Tab to the trigger and listen for the same three parts. Then browse the page with arrow keys and confirm the label is *not* read as stray text when the tooltip is closed.

The faster route: add `Tooltip.stories.tsx` alongside the four existing story files and run `npx test-storybook --url <storybook>`, which runs axe per story. That would turn most of the WARN rows above into confirmed results. I can write that story if useful.

---

**Scope**

- **Inspected:** `src/components/Tooltip/Tooltip.tsx`, `src/components/Tooltip/Tooltip.module.css`, `src/styles/tokens.css` (light and dark), `src/index.ts`, `package.json`, `tokens/component.tokens.json`.
- **Not inspected:** no assistive technology was run; no browser rendering, no axe pass, no keyboard walk-through. Consuming usage in `apps/checkout/` — a grep for `Tooltip` across the repo returns only `src/index.ts` and the component's own files, so no in-repo consumer exercises it. Any Figma spec for this component.
- **How "none found" was checked:** the runtime-evidence claim rests on a case-insensitive grep for `storybook|axe|jest|vitest|playwright|test` across the repo, which *does* match the four existing `.stories.tsx` files — so the search works here — and returns no config, dependency, or test file for Tooltip. The "no hide rule" claim comes from reading all 11 lines of `Tooltip.module.css`; there is no `display`, `opacity`, `visibility`, or `:hover` selector in it.
- **Assumptions:** the two contrast ratios assume `src/styles/tokens.css` resolves to the rendered colours and that no consumer overrides `--color-text-default` or `--color-surface-base`. Tooltip has no component-tier tokens (`tokens/component.tokens.json` covers only `button` and `card`), so it consumes semantic tokens directly — worth a separate look under token-compliance, not an accessibility issue.

If any of this is deliberate — for instance, if the always-visible bubble is a placeholder mid-build rather than shipped behaviour — tell me and I'll treat it as accepted in future runs.
