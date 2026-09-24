# Sample output: system-health (fixture run)

**Skill:** `skills/system-health`
**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `27c301d`
**Eval case:** `health-baseline` in `tests/evals/cases.json`
**Date:** 2026-09-24
**Edited:** no. The report below is verbatim from a headless run with read-only tools; `tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case health-baseline`; runs vary, so expect the same findings in different words.

---

# Design system health report

**Date:** 24 September 2026
**Assessment type:** Direct inspection (full repo, 25 files)
**Library type:** Component library — a shared, versioned component package with a token source, but no documentation platform, contribution process, or governance artefacts found in the repo

---

Your tokens are better structured than most libraries this size, and one broken reference in them is causing a live dark-mode bug. The bigger problem is that nobody is holding the surface: you have two modal components with incompatible APIs, and your only consumer has forked your Button. Both are symptoms of the same gap.

---

#### Overall health

| Dimension | Status | Key finding |
|-----------|--------|-------------|
| Tokens | 🟡 Functional | Three clean tiers, DTCG-2025.10 value shapes — but `card.border` points at a primitive and freezes the Card border in dark mode |
| Components | 🟠 Weak | Modal and Dialog do the same job with divergent props; overlay a11y and state coverage are thin |
| Documentation | 🟠 Weak | Stories for 4 of 5 components, nothing above "exists"; no Storybook config or scripts to run them |
| Adoption | 🟠 Weak | One consumer, which re-implemented Button in raw hex because the system has no size or weight affordance |
| Decision-making | 🟠 Weak | No owner, contribution route, or decision record found — the duplication above is what that looks like |
| AI readiness | 🔴 Absent | No manifest or metadata; tokens are the one machine-legible layer. Expected at this stage |
| Platform maturity | 🟠 Weak | Semver-shaped version with no CHANGELOG, no build, no CI |

Status key: 🟢 Strong · 🟡 Functional · 🟠 Weak · 🔴 Absent

**Maturity stage (inferred): Managed, provisionally.** The evidence for Managed is there — a versioned package (`@fixture/ui` 2.3.0) consumed by a real app, a token source with primitives *and* semantics, documentation for most components. The one Managed criterion I can't confirm is a contribution route: nothing in the repo names an owner or a way in, and a Slack channel or named person wouldn't show up in code. To reach **Systematic**, the system needs tier references enforced (see Tokens), one API contract that Modal and Dialog both follow, and a CHANGELOG.

---

#### Dimension findings

### 🟡 Tokens

The architecture is genuinely good. Three tiers with mostly correct downward references, semantic names that encode intent (`color.action.primary`, `color.text.on-action`, `color.surface.raised` — not a colour name among them), and primitives using DTCG 2025.10 object value shapes (`{colorSpace, components, hex}`, `{value, unit}`) rather than the older string draft. That last point puts you ahead of most libraries.

**🔴 One token breaks dark mode, and it's the one that breaks the tier rule.** `tokens/component.tokens.json:9` has `card.border` → `{color.gray.200}`, a primitive, while every sibling references a semantic. The generated CSS faithfully reflects that: `src/styles/tokens.css:17` emits `--card-border: #e5e7eb` as a literal, where `--card-background` and `--card-padding` emit `var(...)` aliases. The `[data-theme="dark"]` block (lines 22–30) redefines `--color-border-default` to `#374151`, but `--card-border` is a literal, so it never moves. Every Card renders a light-grey border on a dark surface. Fix is one character-level edit in the JSON plus the regenerated line — `{color.border.default}` / `var(--color-border-default)`.

**🟠 Nothing in the repo generates `tokens.css`.** The file header says "Generated from tokens/*.tokens.json", but `package.json` has no `scripts` and no `devDependencies`, and no Style Dictionary or Terrazzo config exists. The two representations are hand-synced, which is why a defect in the JSON can sit undetected in the CSS.

**🟠 A hardcoded off-palette colour in the library itself.** `src/components/Card/Card.module.css:10` sets the title to `#1a73e8`, which isn't in your primitive set (your blue-500 is `#2563eb`) and doesn't theme.

**🟡 The primitive scale is too thin to cover real use.** Spacing has exactly two values (8px, 16px). There are no radius tokens despite four distinct radii hardcoded across components (6px Button, 8px Card/Modal/Dialog, 4px Tooltip), and no typography tokens at all. This is the supply-side cause of two of the adoption findings below.

### 🟠 Components

**🔴 Modal and Dialog are the same component with incompatible APIs.** Both render a heading, a body, and a dismiss button over a raised surface; their stylesheets are near-identical (`surface-raised` background, `border-default`, `space-inset` padding, 8px radius). Their props diverge on every single axis: `open`/`isOpen`, `onClose`/`onDismiss`, `title`/`heading`. Both are exported from `src/index.ts` and nothing tells a consumer which to reach for. Both also hardcode a DOM id (`modal-title`, `dialog-heading`), so two instances on a page produce duplicate ids and a broken `aria-labelledby`.

**🔴 Modal renders half-transparent.** `Modal.module.css:1–6` puts `opacity: 0.5` on `.backdrop`, and `Modal.tsx:17–18` nests the modal *inside* that backdrop. Opacity applies to the whole subtree — the dialog content, not just the scrim, renders at 50%. The backdrop also has no centring, so the modal sits in the top-left.

**🟠 Overlay accessibility is incomplete in both.** No focus trap, no focus restore, and no Escape handling in either. Dialog uses `<dialog open>` (`Dialog.tsx:16`), which renders the element non-modally — no top layer, no backdrop, no focus containment. That needs `showModal()`, not the `open` attribute.

**🟠 Interactive states stop at Button.** Button has `:hover` and `:focus-visible`. It accepts `disabled` through `ButtonHTMLAttributes` but has no disabled or active styling. The Modal close and Dialog dismiss buttons have no focus styles at all.

**🟠 Tooltip is a stub.** `Tooltip.tsx` renders the bubble unconditionally with no show/hide logic, no `aria-describedby` linking it to its trigger, and `position: absolute` with no offsets. It's also the only component with no story.

I've skipped complexity distribution — with five components it isn't a meaningful signal.

### 🟠 Documentation

**Coverage sits on the bottom rung.** Four of five components have a Storybook story (Tooltip has none). All four use `tags: ['autodocs']`, so prop tables can be derived from the TypeScript interfaces — and Button, Modal and Dialog do carry JSDoc on their props, which is more than most. But nothing reaches "guided": no when-to-use, no anti-patterns, no accessibility notes, anywhere.

**🔴 The stories can't actually run.** There's no `.storybook/` directory, no `devDependencies`, and no scripts. The stories import `@storybook/react`, which isn't installed. So even the "exists" rung is aspirational — the workbench isn't wired up.

**No prose documentation of any kind exists in the repo** — no README at root or in either package, no CONTRIBUTING, no CHANGELOG. If documentation lives in Notion, Zeroheight or a wiki, it wasn't in scope here.

**Staleness is uncomputable.** The repo has a single commit ("Initial commit"), so every file shares one timestamp and doc-vs-code drift can't be dated.

### 🟠 Adoption

Keeping coverage and adoption separate: coverage (does the system provide what's needed?) is the weaker of the two here, and it's driving the adoption number.

**🔴 The one consumer forked your Button.** `apps/checkout/src/CheckoutButton.module.css` hardcodes `#2563eb`, `#ffffff` and `#1d4ed8` — the exact resolved values of `--button-background`, `--button-text` and `--button-background-hover`. It won't follow dark mode. `Summary.tsx` imports `Card` from `@fixture/ui` but reaches for the local button instead.

**This looks like a genuine gap, not carelessness.** CheckoutButton needs `padding: 12px 20px` and `font-weight: 600`. Your Button has fixed padding of `var(--space-gap) var(--space-inset)` (8px/16px) with no size prop, and you have no font-weight token. They needed something the system doesn't offer. That makes this a supply problem — the fix is in the library, not in a conversation about compliance.

**🟡 The same story in the Card override.** `Summary.module.css:2` sets `--card-padding: 24px` locally. Component tokens exist precisely to be override points, so this is the architecture working — but 24px isn't on your spacing scale, which only goes 8 and 16. Two independent off-scale values in one small consumer is a clear signal the scale needs extending.

**Version currency is fine.** The consumer declares `^2.2.0` against a 2.3.0 library — the range still admits current, no action needed.

**Design-side adoption is unknown.** No Figma file or library reference appears in the repo.

### 🟠 Decision-making

I'm using "decision-making" rather than "governance" — for a library this size a governance framework would be overhead. The question is just whether someone is holding the surface.

Right now the evidence says no. No owner is named anywhere (`package.json` has no `author`, `maintainers` or `repository` field), no contribution route, no decision records. The consequence isn't abstract — it's the two findings above. Two modal components with contradictory prop names shipped side by side, and a consumer's fork of a core component landed unchallenged. Both are things one person with a view on the library would have caught in a five-minute conversation.

The ask here is small: name an owner, and write down the two or three rules you already follow informally.

### 🔴 AI readiness

No component manifest, no `.ai/` metadata, no AGENTS.md or equivalent, no six-section descriptions. Component descriptions don't exist beyond per-prop JSDoc on three components.

The concrete cost today: an agent asked for "a modal" sees two exports with near-synonymous names, no purpose statements, and near-identical CSS. It has no basis for choosing, so it picks one at random — and half the time it writes `title=` where the component wants `heading=`.

The one bright spot is the token layer: DTCG-shaped JSON with intent-encoding semantic names is directly parseable and reasonable for an agent to reason about. Adding `$description` intent fields to the semantic tier would be a cheap, high-leverage start.

For a Managed component library, absent AI readiness is the expected state. This is future work, not an urgent gap — and it's blocked on settling Modal vs Dialog anyway.

### 🟠 Platform maturity

The version is semver-shaped (2.3.0) and the consumer can pin against it — that part works. Beyond that:

- **No CHANGELOG.** A package already at 2.x with no record of what any release contained. The consumer has no way to know what 2.2 → 2.3 changed.
- **No build.** `main` points at `src/index.ts`, so consumers compile raw TypeScript. No `exports`, `files` or `publishConfig`; `private: true` with no registry target.
- **No CI, no tests, no lint config.**
- **No stated support expectations**, and no migration convention in place — which matters, because consolidating Modal and Dialog will be a breaking change.

---

#### Prioritised action list

**Immediate (next 4 weeks)**

1. **Repoint `card.border` at `{color.border.default}`** and change `--card-border` to `var(--color-border-default)`. Two lines, removes a live dark-mode defect.
2. **Fix the Modal backdrop.** Move the scrim to a `::before` or use a colour with alpha, so the dialog content isn't rendered at 50% opacity.
3. **Decide between Modal and Dialog.** Pick one, deprecate the other, record why. This blocks progress in three other dimensions — you can't document, consolidate an API contract, or write agent metadata around an unresolved duplicate.
4. **Replace `#1a73e8`** in the Card title with a semantic token.

**Near-term (next quarter)**

5. **Give Button what the consumer forked it for** — a size or emphasis prop, plus radius and font-weight tokens — then retire `CheckoutButton`. Fixing the cause is worth more than flagging the symptom.
6. **Wire up Storybook properly:** devDependencies, scripts, `.storybook/`, and a Tooltip story. Right now the stories are source files nothing can run.
7. **Name an owner and write a short README:** what's in the library, what stays local, how to ask for something.
8. **Start a CHANGELOG at 2.4.0.** Even starting from now is worth more than nothing.
9. **Finish the overlay accessibility contract** on whichever component survives: focus trap, focus restore, Escape, unique ids, and `showModal()` if it's the native `<dialog>`.

**Longer-term (6+ months)**

10. **Extend the primitive scale** — spacing beyond 8/16, radius, typography. The two off-scale values in one consumer are your evidence for what's missing.
11. **Add CI gates:** a scan for raw hex outside `tokens/` would have caught findings 1, 4 and the Button fork automatically.
12. **AI readiness:** a component manifest and six-section descriptions, once the Modal/Dialog question is settled.

---

**Scope**
- **Inspected:** all 25 non-git files in the repo — `package.json`, `tokens/*.tokens.json` (3), `src/styles/tokens.css`, `src/index.ts`, all 14 files under `src/components/`, and all 5 files under `apps/checkout/`.
- **Not inspected:** anything outside this repo — Figma libraries, a documentation platform, issue trackers, chat channels, or other consuming applications. Adoption findings describe the one consumer present here, not your full consumer set.
- **How "none found" was checked:** the absence claims (no README/CONTRIBUTING/CHANGELOG, no `.storybook/`, no CI config, no tests, no `.ai/` metadata, no AGENTS.md) rest on a full recursive file listing of the repo, which enumerated all 25 files — not on a pattern search that could have missed them. The hardcoded-colour search matched hex, and does find values in `tokens.css` and the component stylesheets, so it works on this codebase.
- **Assumptions:** the single-commit history is a fixture artefact rather than the real history, so I treated staleness and release cadence as unmeasurable rather than as findings. I've read `apps/checkout` as the only consumer visible to me, not as the only consumer that exists.

> **A note on context:** This assessment sees your system's artefacts — it does not see the history, constraints, or trade-offs behind them. Some findings may flag gaps your team has already considered and accepted. If any finding describes an intentional decision or a known limitation, let me know — I'll calibrate future assessments to your system's actual priorities rather than a generic ideal. The goal is to surface blind spots, not to question choices you've already made deliberately.
