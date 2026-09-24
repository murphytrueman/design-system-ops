# Sample output: component-audit (fixture run)

**Skill:** `skills/component-audit`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `27c301d`
**Eval case:** `duplicate-components` in `tests/evals/cases.json`
**Date:** 2026-09-24
**Edited:** no. The report below is verbatim from a headless run with read-only tools; `tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case duplicate-components`; runs vary, so expect the same findings in different words.

---

# Component audit report

**The library is small and structurally clean, but it ships two components that do the same job with different APIs, and its one consuming app has hand-rolled its own copy of `Button` rather than importing the one you provide — those two facts are where the value is.**

**Date:** 24 September 2026
**Library type:** Design system (early stage) — it ships a token layer with light/dark modes (`src/styles/tokens.css`), a component-token tier (`tokens/component.tokens.json`) and components, not components alone
**Library size:** 5 public components, 0 internal utilities (all 5 are exported from `src/index.ts:1-10`)
**Audit method:** Combined — direct source inspection of all 5 components; usage analysis limited to the one consuming app present in the repo
**Usage signals used:** Code imports across the library and `apps/checkout`, with a positive control. Not available: npm downloads (package is `"private": true`, `package.json:4` — never published, so no download data exists), Figma library analytics (no Figma file configured; no `.ds-ops-config.yml`), Storybook index (story files exist but there is no `.storybook` config or built index), support tickets / surveys / production analytics (none supplied)

---

## Summary

For 5 components the structural condition is good: consistent file layout, one component per directory, every component exported from a single barrel, CSS Modules throughout, and 4 of 5 documented with Storybook stories. The significant finding is duplication: `Modal` and `Dialog` solve the same problem — an overlay with a heading, a body and a dismiss action — with divergent prop vocabularies (`open`/`onClose`/`title` vs `isOpen`/`onDismiss`/`heading`), both publicly exported, with nothing telling a consumer which to reach for. The second-order finding is that the library has no foundational layer: 4 of its 5 components are compound, nothing composes anything else, and both overlays restyle their own dismiss button in CSS rather than using `Button`. That absence shows up in the consuming app too, where `CheckoutButton` reproduces `Button` with light-theme hex values frozen in place.

---

## Inventory summary

| Category | Count | Actively used | Unknown | Likely/confirmed unused |
|---|---|---|---|---|
| Navigation | 0 | — | — | — |
| Forms | 0 | — | — | — |
| Feedback / overlay | 3 | 0 | 0 | 3 (Tooltip, Modal, Dialog) |
| Layout | 0 | — | — | — |
| Data display | 1 | 1 (Card) | 0 | 0 |
| Other — actions | 1 | 0 | 0 | 1 (Button) |
| **Total** | **5** | **1** | **0** | **4** |

Per-component detail:

| Component | Own props | Level | Stories | Usage status |
|---|---|---|---|---|
| Button | 1 (`variant`) + native button attrs | Foundational | ✅ 2 stories | Likely unused |
| Card | 1 (`title`) + native div attrs | Compound | ✅ 1 story | Actively used |
| Tooltip | 2 (`label`, `children`) | Compound | ❌ none | Likely unused |
| Modal | 4 (`open`, `onClose`, `title`, `children`) | Compound | ✅ 1 story | Likely unused |
| Dialog | 4 (`isOpen`, `onDismiss`, `heading`, `children`) | Compound | ✅ 1 story | Likely unused |

No component exceeds twice the median own-prop count for its level, so there are no complexity outliers. At 5 components the complexity distribution is thin evidence in general — the one shape worth reading from it is the foundational-to-compound ratio (CA-03), not the counts themselves.

---

## Findings by dimension

### Dimension 1 — Usage signals

**CA-02 · 🟠 High · Button (drift evidence)**
`apps/checkout/src/CheckoutButton.tsx:4-6` defines a local button instead of importing `Button`. The same file's sibling `apps/checkout/src/CheckoutButton.module.css:2-3,11` hardcodes `#2563eb` and `#1d4ed8` — exactly the light-theme values of `--color-action-primary` and `--color-action-primary-hover` (`src/styles/tokens.css:3-4`). The local copy is therefore a light-theme-only snapshot of `Button` and will not respond to `[data-theme="dark"]`. The app is not unaware of the package: `apps/checkout/src/Summary.tsx:1` imports `Card` from `@fixture/ui` and then places `CheckoutButton` inside it (`Summary.tsx:9`). That combination rules out discoverability as the cause and makes this a genuine adoption failure rather than a missing capability — `Button`'s `variant="primary"` default already produces what the local component produces.
**Action:** Replace `CheckoutButton` with `Button` and delete the local module; then find out why it was written, because the reason will apply to the next component too.

**CA-09 · ⚪ Low · Button, Card, Tooltip, Modal, Dialog**
All four components other than `Card` have no consumer import anywhere in reach, and the four are all standalone in the composition graph. This is recorded for completeness, not as a removal signal: with only one consuming app checked out, absence of an import here is not evidence of absence in production.
**Action:** None yet. See the Review section of the action list.

No component reaches "Confirmed unused". The positive control passed — the same search that found nothing for `Button`, `Tooltip`, `Modal` and `Dialog` did find `Card` imported from `@fixture/ui` at `apps/checkout/src/Summary.tsx:1` — but coverage of consuming repos is incomplete: `apps/checkout` is the only consumer in this repo, and its `@fixture/ui: ^2.2.0` dependency range (`apps/checkout/package.json:7`) against the library's own `2.3.0` (`package.json:3`) suggests the package is consumed somewhere that has not tracked the latest minor. The ceiling for all four is therefore "Likely unused".

### Dimension 2 — Complexity distribution

Foundational: 1 (`Button`). Compound: 4 (`Card`, `Tooltip`, `Modal`, `Dialog`). Feature: 0.

**CA-03 · 🟠 High · Library-wide (`src/components/`)**
Compound components outnumber foundational ones 4:1, which is the inversion the dimension looks for: teams have built upward without the pieces to build on. Three pieces of evidence, all inside the library: `src/components/Modal/Modal.module.css:24-30` and `src/components/Dialog/Dialog.module.css:17-22` each restyle a dismiss button from scratch (both setting `background: var(--color-action-primary)`, `color: var(--color-text-on-action)`, `border: 0` and the same padding pair) rather than composing `Button`; and `src/components/Card/Card.tsx:11` hand-rolls an `<h3>` with its own `.title` rule because there is no text or heading primitive. There is no `Text`, `Heading`, `Icon`, `Stack`, `Box` or `VisuallyHidden`.
**Action:** Add the missing primitives, starting with the one with three call sites already waiting for it — have `Modal` and `Dialog`'s dismiss control compose `Button`.

Zero feature components is a healthy signal: no product-specific logic has leaked into the shared library.

### Dimension 3 — Duplication

**CA-01 · 🔴 Critical · Modal / Dialog**
`src/components/Modal/Modal.tsx:14` and `src/components/Dialog/Dialog.tsx:14` solve one problem — an overlay carrying a heading, a body and a single dismiss action — with two prop vocabularies: `open`/`onClose`/`title` against `isOpen`/`onDismiss`/`heading`. Both are public (`src/index.ts:7-10`), both carry `tags: ['autodocs']` stories whose args differ only in those names (`Modal.stories.tsx:8`, `Dialog.stories.tsx:8`), and nothing in either file, story or description states which a consumer should choose. Their stories even suggest the same use cases — "Discard changes?" and "Remove item?" are the same confirmation pattern.

**Decision: keep `Modal`, deprecate `Dialog`.** Two reasons decided it. `Modal` actually asserts modal semantics — `role="dialog"`, `aria-modal="true"` and a backdrop (`Modal.tsx:17-18`) — whereas `Dialog` renders `<dialog open>` (`Dialog.tsx:16`), which is the *non-modal* form of the element: no top layer, no backdrop, no focus trap, no inert background. And `open`/`onClose`/`title` is the conventional React overlay API, so it is the one a new team member guesses correctly. Adoption did not decide it: neither component has a consumer import in reach.

One caveat to carry into the migration: `Dialog`'s choice of the native `<dialog>` element is the better long-term foundation. Fold it into `Modal`'s implementation via `showModal()` rather than discarding it — that is how `Modal` gets the focus trap and top-layer behaviour neither component has today.
**Action:** Deprecate `Dialog` with a codemod-able prop mapping (`isOpen`→`open`, `onDismiss`→`onClose`, `heading`→`title`); reimplement `Modal` on native `<dialog>` + `showModal()`.

No other duplication pair exists. `Tooltip` has no `Popover` counterpart to disambiguate against.

### Dimension 4 — Coverage gaps

**CA-04 · 🟠 High · Forms category (empty)**
The package describes itself as "Shared UI components and design tokens for the web app" (`package.json:5`) but provides no form components at all — no `Input`, `Select`, `Checkbox`, `Radio`, `Field` or `Label`. For a shared library serving a checkout app, input and field are among the highest-frequency needs there are. This is a genuine system gap rather than a local one. Flagged from structure only: the one consumer in reach (`apps/checkout`) builds no form components locally, so there is no drift evidence corroborating it here.
**Action:** Assess `Field` + `Input` for contribution; confirm the need against the other consuming repos before committing.

**CA-08 · 🟡 Medium · Card**
`apps/checkout/src/Summary.module.css:2` sets `--card-padding: 24px` on the Card instance, reaching past the component's public API into its component token to get padding the API does not offer. `Card`'s only own prop is `title` (`Card.tsx:4-6`). A consumer overriding a component token is the system's contract being worked around, and it is the state-and-variant form of a coverage gap: the component exists but lacks a variant teams need.
**Action:** Add a `density` or `padding` prop to `Card` and migrate the override.

**CA-06 · 🟡 Medium · Tooltip (completeness)**
`src/components/Tooltip/Tooltip.tsx:9-15` renders its bubble unconditionally — there is no hover, focus or `open` state, no visibility logic, and no `aria-describedby` tying the bubble to the element it describes. As shipped, the tooltip is always visible. This is a component that exists in the inventory but cannot do its job.
**Action:** Add the trigger and visibility model, or withdraw it from the public barrel until it has one.

**CA-07 · 🟡 Medium · Modal, Dialog (completeness)**
Both overlays hardcode the element id that labels them: `modal-title` (`Modal.tsx:18-19`) and `dialog-heading` (`Dialog.tsx:16-17`). Two instances rendered on one page produce duplicate ids and an `aria-labelledby` pointing at the wrong heading.
**Action:** Generate the id per instance (`useId`).

**CA-05 · 🟡 Medium · Tooltip (documentation)**
`Tooltip` is the only public component with no `*.stories.tsx` — the other four have one (`Button.stories.tsx`, `Card.stories.tsx`, `Modal.stories.tsx`, `Dialog.stories.tsx`). It is exported at `src/index.ts:5`, so it is discoverable by import but documented nowhere.
**Action:** Add stories, after CA-06 gives it behaviour worth documenting.

CA-06 and CA-07 sit on the boundary with accessibility; they are recorded here as API-and-state completeness, which is what this audit judges at this library size. They are not a substitute for an accessibility pass — `accessibility-per-component` owns that, and neither overlay traps focus or handles `Escape`, which is outside this audit's rubric.

---

## Composition graph

**Method:** No `.ai/index/` exists in this repo, and I did not run `codebase-index` to create one — it writes index files into the project, which is beyond an audit request. Instead the edge set is read directly from the complete enumeration of import statements in the library (every `.ts`/`.tsx` import line in the repo was listed, not sampled), which at 5 components is exhaustive rather than partial. Offer stands to run `codebase-index` if you want the graph as queryable files.

**The graph has no edges.** No component in the library imports another. Consequently:

- **Standalone (fan-in 0, fan-out 0):** all five — `Button`, `Card`, `Tooltip`, `Modal`, `Dialog`. Each imports only React types and its own CSS module.
- **Foundation components (fan-in ≥ 5):** none.
- **Hub components:** none.
- **Blast radius of any component change:** confined to the component itself plus its external consumers. "If I change `Button`, what breaks?" — nothing inside the library, and in reach, nothing outside it either, because the one consumer that would use it wrote its own instead (CA-02).

An all-standalone graph at this size is not a defect by itself, but read against CA-03 it is the same finding seen from the other side: nothing composes `Button` because the compound components each rebuilt its styling in CSS.

**Shared token hotspots** — the tokens most dangerous to change, by how many of the 5 components bind them:

| Token | Components | Sites |
|---|---|---|
| `--space-gap` | 5 of 5 | `Button.module.css:2`, `Card.module.css:9`, `Tooltip.module.css:7`, `Modal.module.css:16,25,29`, `Dialog.module.css:10,14,21` |
| `--color-text-default` | 3 (+1 consumer) | `Modal.module.css:4,17,21`, `Dialog.module.css:6`, `Tooltip.module.css:8`, `apps/checkout/src/Summary.module.css:8` |
| `--color-action-primary` | 3 | `Button.module.css:9,24` (and via `--button-background`, `tokens.css:13`), `Modal.module.css:26`, `Dialog.module.css:18` |
| `--space-inset` | 3 (+1 alias) | `Button.module.css:2`, `Modal.module.css:11`, `Dialog.module.css:4`, aliased by `--card-padding` (`tokens.css:18`) |
| `--color-surface-raised` | 3 | `Modal.module.css:9`, `Dialog.module.css:2`, `Card.module.css:2` via `--card-background` (`tokens.css:16`) |

`--space-gap` is bound by every component in the library; it is the single change with system-wide reach.

---

## AI readiness and maturity stage

Not inspected here — neither is this audit's to judge, and no `system-health` report exists in the repo to cite. Run `system-health` for both.

---

## Action list

**Immediate**
1. **CA-01** — Resolve the `Modal`/`Dialog` duplication: deprecate `Dialog`, map its props onto `Modal`, reimplement `Modal` on native `<dialog>` + `showModal()`. Nothing composes `Dialog`, so there is no internal migration risk; external consumers are unverified, so treat it as a deprecation rather than a removal.
2. **CA-02** — Replace `apps/checkout`'s `CheckoutButton` with `Button`. This one is both a correctness fix (the local copy is dark-theme-broken) and the cheapest available adoption win, and the reason it was written is worth asking about before it recurs.

**Planned**
3. **CA-03** — Add the foundational layer, beginning with the three dismiss/heading call sites already waiting for `Button` and a text primitive.
4. **CA-08** — Give `Card` a density or padding API and migrate the consumer's token override.
5. **CA-06 → CA-05** — Give `Tooltip` a visibility model, then document it. In that order.
6. **CA-07** — Per-instance ids in both overlays (`useId`).
7. **CA-04** — Assess `Field` + `Input` for contribution, after checking the need against the consuming repos this audit could not see.

**Review**
8. **CA-09** — `Button`, `Tooltip`, `Modal` and `Dialog` are all "Likely unused" on one consumer's evidence. Before any of them is deprecated on usage grounds, get import data from every repo that depends on `@fixture/ui`. The `^2.2.0` range against a `2.3.0` library says at least one consumer exists that this repo does not contain.
9. No feature components to relocate — the library is clean on that axis.

One finding outside this audit's rubric, noted in passing because it sits in a file I read: `src/components/Card/Card.module.css:10` sets `color: #1a73e8`, a hardcoded hex that is not any value in `tokens.css` and will not theme. `token-compliance` owns that class of finding.

---

**Scope**

- **Inspected:** all 5 component sources and CSS modules under `src/components/`; `src/index.ts`; `src/styles/tokens.css`; `tokens/component.tokens.json`; all 4 story files; `package.json`; the whole of `apps/checkout` (`package.json`, `Summary.tsx`, `Summary.module.css`, `CheckoutButton.tsx`, `CheckoutButton.module.css`). Import analysis covered every `.ts`/`.tsx` file in the repo.
- **Not inspected:** consuming repositories other than `apps/checkout` — none are present; Figma library and Figma analytics (none configured, and detach rates need an Enterprise plan regardless); a built Storybook index (no `.storybook` config in the repo); npm download data (does not exist — the package is private and unpublished); `tokens/primitives.tokens.json` and `tokens/semantic.tokens.json` beyond what `tokens.css` resolves, which belong to `token-audit`; support tickets, surveys and production analytics, none of which were supplied.
- **How "none found" was checked:** the import search ran over all `.ts`/`.tsx` files in the repo, matching both bare component names and `@fixture/ui` import lines (no namespace or aliased imports exist in the repo to miss). Positive control: the same search found `Card` imported from `@fixture/ui` at `apps/checkout/src/Summary.tsx:1`. Repo coverage is one consumer of unknown total, which is why no component is marked "Confirmed unused".
- **Assumptions:** that `src/index.ts` is the public API boundary and all 5 exports are public (no `internal/`, `private/` or underscore-prefixed components exist to separate out); that story files are the documentation surface, since no other docs platform is configured; that `apps/checkout` is a real consumer rather than a fixture app.

---

> **A note on context:** This audit sees your component library — it does not see the product decisions, team constraints, or historical context behind it. Some findings may flag patterns your team chose deliberately. If any finding describes an intentional decision, let me know — I'll exclude it from future runs and learn your system's conventions. The goal is to surface problems you haven't seen yet, not to second-guess choices you've already made.
