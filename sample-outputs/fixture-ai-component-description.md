# Sample output: ai-component-description (fixture run)

**Skill:** `skills/ai-component-description`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `27c301d`
**Eval case:** `describe-button` in `tests/evals/cases.json`
**Date:** 2026-09-24
**Edited:** no. The report below is verbatim from a headless run with read-only tools; `tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case describe-button`; runs vary, so expect the same findings in different words.

---

All four `knowledge-notes/` references resolve, so the skill is fully installed. Here's what I read and what it changed.

**Sources:** `Button.tsx`, `Button.module.css`, `Button.stories.tsx`, plus `Card`/`Modal`/`Dialog`/`Tooltip` and `src/styles/tokens.css` for composition and token facts, and `apps/checkout/` where I found a local re-implementation. No `.ai/metadata/Button.metadata.json`, no `.ds-ops-config.yml`, and no Figma node — so this is source- and Storybook-derived, and the existing Figma description (if any) hasn't been read.

Two things worth flagging before the description: the real `Button` has **one prop** (`variant`, two values) plus native button attributes — none of the `size`/`loading`/`destructive`/`ghost` props in the skill's illustrative example exist, and I've documented only what's in the source. And it sets no `type`, so inside a `<form>` the native `type="submit"` applies.

---

```
PURPOSE
Button issues an action on the current view — submit, confirm, dismiss, apply. It renders a
native button element and nothing else. Use it where an action is triggered, not where a
destination is navigated to; for navigation use an anchor, not Button with an onClick.

PROPS
variant; "primary" | "secondary"; "primary"; Visual emphasis. primary is a filled
  --button-background surface; secondary is transparent with a 1px currentColor border.
className; string; no default; Appended alongside the component's own classes, for layout
  placement by the parent.
children; ReactNode; no default; The label. Rendered verbatim through the props spread; the
  component adds no text or icon of its own.
...rest; ButtonHTMLAttributes<HTMLButtonElement>; no default; Every native button attribute
  (type, disabled, onClick, form, aria-*) is spread onto the element.
No size, loading, icon or destructive prop exists. type has no component-level default, so the
native default type="submit" applies.

ANTI-PATTERNS
Do not re-implement Button locally to get a treatment it lacks.
  apps/checkout/src/CheckoutButton.tsx does this and hardcodes #2563eb instead of the
  --button-* tokens, so it does not follow the dark theme. (observed)
Do not omit type inside a form. With no default, the button submits; pass type="button" for
  anything that is not a submit.
Do not pass a variant value outside the two supported ones. The class lookup silently yields no
  variant class and the button renders with base styles only.
Do not render an icon-only child without aria-label. Button contributes no accessible name.
Do not fake a pending state by swapping children and setting disabled. There is no loading prop,
  and a disabled Button carries no visual treatment (see ACCESSIBILITY).

COMPOSITION
Button is a leaf: it accepts children, exports no sub-parts, and must not nest another Button. It
can sit anywhere in Card's children — Card renders a div with an optional h3 title and no footer
slot, so there is no designated action region. Modal and Dialog each render their own built-in
control ("Close" and "Dismiss"), not a Button instance; Buttons passed as their children sit above
that control, so avoid a second competing dismiss action. Wrapping Button in Tooltip does not label
it: Tooltip renders a sibling span with role="tooltip" and no aria-describedby wiring, so its text
never reaches the button's accessible name or description.

ACCESSIBILITY
Renders a real <button> element — never substitute a div with role="button". Keyboard behaviour is
native and unmodified: Tab moves focus, Enter and Space activate; the source contains no key
handlers, preventDefault or focus() calls. The component moves focus nowhere, so a caller needing
focus returned after the action must manage it. Disabled state uses the native disabled attribute
passed straight through, not aria-disabled: the control leaves the tab order and is announced as
unavailable, but Button.module.css has no :disabled rule, so it looks identical to an enabled
button. Treat that as a gap to fix, not a contract to reproduce. The accessible name comes only
from children or an explicit aria-label. Focus is shown via :focus-visible as a 2px
--color-action-primary outline at 2px offset; keep that ring at 3:1 against the adjacent surface in
every theme (5.2:1 on the default light --color-surface-base; dark theme unverified).

EXAMPLES
Intent: Primary confirm action in a form.
Configuration: variant="primary", type="submit", children="Save changes"
Expected DOM output:
  <button type="submit" class="button primary">Save changes</button>

Intent: Cancel beside it, inside the same form, which must not submit.
Configuration: variant="secondary", type="button", children="Cancel", onClick={close}
Expected DOM output:
  <button type="button" class="button secondary">Cancel</button>

Intent: Icon-only action, which needs a name Button does not supply.
Configuration: variant="secondary", type="button", aria-label="Remove item",
  children={<TrashIcon aria-hidden="true" />}
Expected DOM output:
  <button type="button" class="button secondary" aria-label="Remove item">
    <svg aria-hidden="true">...</svg>
  </button>

Class names shown are the CSS Modules source names; the build hashes them.
```

---

**Headline:** Button described in the six-section format, chat only — not written to Figma.

**Written:** Chat only. No Figma node was identified and no `file_key` is configured. Figma Console MCP does expose `figma_set_description`, so if you select the Button component or paste its node link, I can write this text (plus a `descriptionMarkdown` variant) and read it back to confirm — I'd show the existing description first.

**Marked in the text:**
- "dark theme unverified" — the focus-ring contrast on `[data-theme="dark"]` (`#60a5fa`), not computed.
- One anti-pattern marked "(observed)"; the other four are derived directly from the source, not anticipated from analogues.
- The missing `:disabled` style is stated as a gap in the implementation, not as intended behaviour — worth deciding which way you want it before an agent reproduces it.

**Scope**
- **Inspected:** `src/components/Button/*` (tsx, module.css, stories.tsx), `src/components/{Card,Modal,Dialog,Tooltip}/*.tsx`, `src/index.ts`, `src/styles/tokens.css`, `apps/checkout/src/CheckoutButton.{tsx,module.css}`.
- **Not inspected:** Figma (no node or file key), any `.ai/metadata/` file, running Storybook output, `tokens/*.tokens.json` internals.
- **How "none found" was checked:** the prop list is the full `ButtonProps` interface, which declares only `variant` and extends `ButtonHTMLAttributes`; the absent `type` default, focus calls and `:disabled` rule are absences in files short enough to read in full, all shown above.
- **Assumptions:** `Button.module.css` class names are hashed by the build (standard CSS Modules behaviour, not verified against your bundler config); the 5.2:1 figure is calculated from `#2563eb` on `#ffffff` in `tokens.css`.

If any of this is deliberate — the `submit` default, the unstyled disabled state — tell me and I'll phrase it as intent rather than as a gap.
