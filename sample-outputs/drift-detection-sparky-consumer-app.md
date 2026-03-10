# Drift detection report

**Skill:** `skills/drift-detection`
**Source:** PetSmart Sparky Design System — Consumer app product (iOS app + web companion)
**Reference source:** Sparky Figma library v2.1.0 (published 2026-01-15)
**Assessment date:** 2026-03-10
**Assessment method:** Direct code inspection + visual diff analysis
**Scope:** Consumer-facing interfaces (sign-in, product catalog, cart, checkout, account)

---

## Summary

The Sparky consumer app has accumulated 11 drift instances across visual, behavioural, and token dimensions. The most significant finding is version lag: the app is running Sparky v1.8.0, released six weeks ago, while the system has shipped two minor releases (v1.9.0, v1.10.0) with bug fixes and new states. Visual drift is confined to a small set of instances and is either intentional divergence (documented locally) or accidental visual differences in edge cases (empty states, error states). Token drift is minimal — the system's three-tier token architecture is consistently applied. No API drift detected. Overall: the app is in good standing, but version lag should be addressed in the next release cycle to benefit from system improvements.

---

## Drift findings

| ID | Location | Dimension | Classification | Severity | Description | Recommended action |
|---|---|---|---|---|---|---|
| DF-01 | Product card component | Visual | B — Version lag | High | Product card in v1.8.0 uses 12px corner radius; v1.9.0 updated to 8px (design update). App still uses 12px. | Update Sparky dependency to v1.10.0 (latest). Corner radius will update automatically. Effort: dependency bump + test regression suite. |
| DF-02 | Checkout confirmation | Behavioural | E — System gap | Critical | After placing order, app shows custom success animation (Lottie, 2-second auto-close) not present in Sparky. Sparky has Toast component but no success confirmation pattern for checkout. | Propose the custom animation as a contribution to Sparky as `CheckoutConfirmation` component variant. Pattern is reusable. Reference: checkout flow is used by 3+ future products. |
| DF-03 | "Empty cart" state | Visual | C — Accidental drift | Medium | Empty state shows generic illustration (not from Sparky). Sparky has empty-state illustration component (added in v1.10.0) but app was built before it existed and never migrated. | Add the Sparky empty-state illustration component to cart UI. Single file change + one import. Effort: <1 hour. Schedule for next sprint. |
| DF-04 | Loading skeleton in product list | Token | C — Accidental drift | Medium | Skeleton uses hardcoded `#E5E7EB` (light gray) for skeleton background. Should reference `color.feedback.loading` token from Sparky. | Replace hardcoded hex with `theme.colors.feedback.loading`. ~3 files affected. Effort: <1 hour. |
| DF-05 | Focus ring on form inputs | Visual | D — Misunderstanding | Low | Input focus ring is a custom 3px blue ring instead of Sparky's standard 2px ring-color ring. Specification calls for `box-shadow` implementation; app used `border` instead. Accessible but inconsistent. | Update input styles to use `box-shadow` with Sparky's focus ring specifications. This is a presentation detail; no behaviour change. 2 files. |
| DF-06 | Pagination component | API | B — Version lag | High | App implements custom pagination component (`<Pagination isCompact={boolean} />`) before Sparky had one. Sparky v1.10.0 shipped `Pagination` (`size: "compact" | "default"`). Custom version has different API. | Migrate to Sparky `Pagination` component. Custom component can be deleted. Requires identifying all callsites (estimated 4–6 locations). Effort: 2–3 hours. |
| DF-07 | Product rating display | Token | C — Accidental drift | Low | Star icon uses hardcoded `#FDB022` (yellow) instead of `color.feedback.success` token. Resolves to same value but not referenced through token system. | Replace hardcoded hex with token reference. 1 file. <30 minutes. |
| DF-08 | Toast notifications (errors) | Visual | A — Intentional divergence | Medium | App shows custom error toast with custom layout (icon + two-line text instead of Sparky's single-line icon + text). Based on stakeholder feedback that Sparky's toast is too compact for error messages. | Document as a decision record: "Error Toast divergence for improved readability" (1 issue). Propose as a contribution: wider error toast variant in Sparky for critical error states. 2–3 products would benefit. |
| DF-09 | Icon sizing in buttons | Token | A — Intentional divergence | Low | Buttons contain icons sized at 18px instead of Sparky's standard 16px (size-4). Team decision to improve button icon visibility on smaller screens. Documented in code comment. | Acceptable intentional divergence. Document in the component's README as a decision record if not already done. No action required. |
| DF-10 | Validation error message typography | Visual | D — Misunderstanding | Medium | Error message text is 12px, 500 weight, dark red. Sparky specifies 12px, 400 weight (normal), semantic error colour token. Specification was misread; team thought "bold" was required for error emphasis. | Update error message styles to match Sparky specification (font-weight: 400, color: token). Error colour is sufficient for semantic emphasis. 3–4 files. |
| DF-11 | Badge component (unused) | Visual | C — Accidental drift | Low | Badge component exists in codebase (old code path) but is not used in the product. Implements custom styles instead of using Sparky Badge. No user-facing impact. | Delete the unused Badge implementation. Code cleanup only. No functional impact. <1 hour. |

---

## Findings by classification

### Intentional divergence (A) — 2 instances

**DF-08 (Error Toast):** The app's error toast is wider and shows two lines of text, while Sparky's toast is compact. This was an intentional decision based on feedback that error messages need more space to be readable. The divergence is appropriate for this product's context and the error messaging pattern would be valuable as a system contribution.

**DF-09 (Icon sizing in buttons):** Icons in buttons are 18px instead of 16px. Team decision to improve touch target visibility on mobile. Documented in code. This is intentional and acceptable. No action needed.

**Status:** DF-08 should become a decision record and a contribution proposal. DF-09 is acceptable as-is.

---

### Version lag (B) — 2 instances

**DF-01 (Product card corner radius):** The app is using corner radius from Sparky v1.8.0. System v1.10.0 updated corner radius to 8px based on design refinement. Cost to update: dependency bump + regression testing. Benefit: alignment with latest design, bug fixes from v1.9.0 and v1.10.0.

**DF-06 (Pagination component):** The app has a custom pagination implementation that predates Sparky's pagination component. Sparky v1.10.0 now provides the pagination component. The custom version can be deleted and replaced with Sparky's. Effort: 2–3 hours to identify all usage and migrate.

**Status:** Both should be addressed in the next release cycle (target: end of Q1). DF-06 is higher priority because it unblocks a dependency removal and reduces maintenance burden.

---

### Accidental drift (C) — 4 instances

**DF-03 (Empty cart state):** App shows a generic empty state. Sparky added the empty-state illustration component in v1.10.0. The app was built before this component existed and was never updated. This is a simple migration (one file, one import).

**DF-04 (Skeleton loading token):** Skeleton background uses hardcoded `#E5E7EB` instead of `color.feedback.loading` token. This is accidental — the developer hardcoded the value without checking whether a token existed.

**DF-07 (Rating icon colour):** Star icon uses hardcoded yellow instead of the `color.feedback.success` token. Same root cause as DF-04 — the hardcoded value happens to match the token's current value, but the reference is absent.

**DF-11 (Unused badge):** Old Badge implementation exists in the codebase but is not used. Code cleanup, no functional impact.

**Status:** DF-03, DF-04, DF-07 can be fixed in a "drift cleanup" sprint (2–3 hours total). DF-11 is code hygiene (cleanup without priority).

---

### Misunderstanding (D) — 2 instances

**DF-05 (Focus ring implementation):** Input focus rings use `border` instead of `box-shadow`. The specification calls for `box-shadow`; the developer implemented `border` without checking the spec. Functionally equivalent but visually inconsistent.

**DF-10 (Error message typography):** Error messages use bold font (500 weight) when the spec calls for normal (400 weight). The developer assumed error text needed bold emphasis; the specification achieves semantic emphasis through colour alone. Misreading of the design spec.

**Status:** Both indicate documentation gaps. DF-05 suggests the focus ring specification is not clear in Storybook. DF-10 suggests error state patterns need more explicit documentation. Fix the instances (2 hours total) and update documentation to prevent recurrence.

---

### System gap (E) — 1 instance

**DF-02 (Checkout confirmation pattern):** The app has a custom success confirmation animation after checkout. This is not in Sparky. The custom implementation is well-designed and appropriate for the checkout flow. This pattern would be valuable to add to the system — checkout confirmation is a common pattern in e-commerce and financial products, and teams are likely to reimplements it locally without system guidance.

**Status:** Contribute to Sparky as a `CheckoutConfirmation` component or as a variant of the existing Toast component. Estimated effort: design + build + documentation (16 hours). Prioritize for Q2 if other products express the same need.

---

## Root cause patterns

**Observation 1: Token references are inconsistently applied.**
Three instances (DF-04, DF-07) involve hardcoded values when tokens exist. This suggests:
- Token documentation is not discoverable from the component level. Developers do not know what tokens are available.
- No lint rule exists to catch hardcoded values when tokens are available.
- Token tooling is not integrated into the development workflow (e.g., IDE autocomplete for token names).

**Recommendation:** Implement a lint rule (stylelint or similar) that flags hardcoded colour and sizing values in stylesheets. Add the rule to the pre-commit hook. Within 2 weeks, this prevents new instances. Running the linter retroactively would catch the three existing instances.

**Observation 2: Version lag is the primary accumulator.**
Two instances (DF-01, DF-06) are caused by the app running an older version of Sparky. The app is six weeks behind the latest release. This is a common entropy pattern in multi-repo systems.

**Recommendation:** Add a dependency version check to CI. If an app is more than 2 minor versions behind the latest system release, the CI check warns (does not fail) and creates a Jira ticket. This surfaces the gap automatically and prevents silent version lag.

**Observation 3: Design documentation is misread when specification is not explicit.**
Two instances (DF-05, DF-10) involve developers implementing something slightly different from the spec. Both involved implementation details not visually obvious from the design.

**Recommendation:** For form-related components (inputs, error states), add implementation stories to Storybook that explicitly show the CSS or Tailwind classes used. Developers copying from Storybook examples will get the details right. For DF-05, show an input with an explicit `box-shadow` story. For DF-10, show an error message example with computed styles visible in the "Show code" panel.

---

## Migration paths and effort estimates

### Priority 1 (Fix immediately — blocking future work)

**DF-06: Pagination migration**
- Effort: 2–3 hours
- Steps: (1) Locate all pagination component usages (estimated 4–6 locations), (2) Replace with Sparky `Pagination` with equivalent props, (3) Delete custom pagination implementation, (4) Run regression tests on affected flows
- Benefit: Unblocks dependency cleanup, reduces maintenance burden

### Priority 2 (Fix in next sprint — high ROI per hour)

**DF-03, DF-04, DF-07, DF-11: Drift cleanup sprint**
- Combined effort: 2–3 hours
- Changes: (1) Update empty state to use Sparky component, (2) Replace hardcoded token values with token references, (3) Delete unused badge code
- Can be combined into a single PR for efficiency

### Priority 3 (Fix before next release — addresses documentation gaps)

**DF-05, DF-10: Specification alignment**
- Combined effort: 1–2 hours
- Changes: (1) Update input focus ring to use box-shadow, (2) Update error message to use normal font weight
- Paired action: Update Storybook documentation to show implementation details explicitly (prevents future misreadings)

### Priority 4 (Consider for contribution — system-level improvement)

**DF-02: Checkout confirmation pattern**
- Effort: 16 hours (design, build, documentation)
- Recommendation: Propose to the Sparky team for Q2 roadmap. Reference the consumer app's implementation as an exemplar. If other products express the same need, prioritize higher.

### Priority 5 (Code cleanup — no functional impact)

**DF-09: Intentional divergence — no action required**
Document the decision record in the app's README or decision log.

---

## Adoption signals from drift classification

This drift report reveals adoption patterns:

- **Intentional divergence (A):** The app team is confident enough to make deliberate design decisions and document them. This suggests good system understanding.
- **Version lag (B):** Two instances suggest upgrade cycles are reactive, not proactive. The app team upgrades when they need a feature or bug fix, not on a regular cadence.
- **Accidental drift (C):** Hardcoded token values suggest token documentation is not discoverable in the development workflow. This is a friction point for adoption.
- **Misunderstanding (D):** Design spec misreadings suggest Storybook examples do not show implementation details. Fixing this (one story per concept) would prevent similar misreadings in other products.
- **System gap (E):** One system gap identified. This is a healthy pattern — most product needs are served by the system; divergence is rare.

**Overall adoption signal:** The app team understands the system and uses it for most needs. Friction points are in version management and documentation clarity, not in system governance or design philosophy.

---

## Recommended actions

**Immediate (this week):**
1. Set up linter rule for hardcoded token values. Add to CI pre-commit hook. (2 hours)

**Next sprint (this month):**
2. Migrate pagination component (DF-06). (2–3 hours)
3. Drift cleanup sprint: empty state, token hardcoding, unused code. (2–3 hours)

**Before next product release:**
4. Update focus ring and error message styles to match spec. Update Storybook with implementation-detail examples. (2–3 hours)

**This quarter:**
5. Add version check to CI for dependency freshness. (4 hours)
6. Propose checkout confirmation as a Sparky contribution. (discovery phase, 8 hours)

---

*Generated by Design Systems OS — `skills/drift-detection` skill*
*Source repository: PetSmart Sparky Design System (Style Dictionary, React 17, Sass)*
