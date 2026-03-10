# Sample output: Token audit

**Skill:** `skills/token-audit`
**Source:** Helix Design System — CSS custom properties + JSON tokens (42 files, ~480 tokens)
**Assessment method:** Token file analysis (CSS custom properties, JSON with alias references, Tailwind config)
**Library type:** Design system (three-tier architecture, 6 consuming teams, theming support)

---

## Token audit report

Your token architecture has five structural issues that need attention — two critical tier leakage problems, two high-severity naming concerns, and a semantic gap that is generating workarounds downstream. The primitive and semantic tiers are solid in coverage, but the component tier is thin and the handoff from semantic to component is where most of the debt sits. Here is the full breakdown.

### Tier structure

- **Primitive tier:** 🟢 Strong — 14 files covering colour scales (8 hues × 10 steps), spacing (4px base × 12 steps), typography (3 families, 7 weights, 9 sizes), elevation, border-radius, z-index, duration, and easing
- **Semantic tier:** 🟡 Functional — 18 files covering colour roles (action, neutral, feedback, surface), spacing intent (inset, stack, inline), typography roles (heading, body, label, code), and elevation levels
- **Component tier:** 🟠 Weak — 10 files covering button, input, card, badge, toast, dialog, tooltip, avatar, tag, and table-header. No component tokens for 26 other shipped components.
- **Tier leakage instances:** 9

### Findings

| ID | Severity | Category | Finding |
|---|---|---|---|
| TA-01 | 🔴 Critical | Value | **9 component tokens reference primitives directly, bypassing the semantic tier.** `--helix-card-border` resolves to `var(--helix-gray-200)` instead of routing through `var(--helix-border-default)`. Same pattern in toast, dialog, and tooltip border tokens. This means theme switching breaks these components — the primitive value does not change between themes, but the semantic token does. |
| TA-02 | 🔴 Critical | Value | **Feedback colour tokens are disconnected from the feedback system.** `--helix-toast-success-bg` hardcodes `#DCFCE7` instead of referencing `var(--helix-feedback-success-subtle)`. The semantic layer already defines these roles correctly — the component tokens just do not use them. 4 toast variants and 3 badge variants affected. |
| TA-03 | 🟠 High | Naming | **Semantic colour tokens mix intent-based and appearance-based names.** `--helix-action-primary` (intent) coexists with `--helix-blue-surface` (appearance). The blue-surface token should be `--helix-surface-accent` or `--helix-surface-brand` — describing what it is for, not what colour it is. 8 tokens use colour-based names at the semantic tier. |
| TA-04 | 🟠 High | Coverage | **No semantic tokens exist for interactive states.** Hover, focus, active, and disabled colours are defined at the component tier but skip the semantic tier entirely. `--helix-button-hover-bg` resolves directly to a primitive (`--helix-blue-600`). This forces every new component to reinvent state colours instead of referencing a shared semantic set. |
| TA-05 | 🟠 High | Naming | **Spacing tokens use `px` suffix in names.** `--helix-space-4px`, `--helix-space-8px`, `--helix-space-16px` — the suffix duplicates what the value already expresses. If the base unit ever changes (e.g., moving to rem), the names become lies. Standard practice: `--helix-space-1`, `--helix-space-2`, `--helix-space-4` (multiplier-based) or `--helix-space-xs`, `--helix-space-sm`, `--helix-space-md` (T-shirt). |
| TA-06 | 🟡 Medium | Value | **3 alias chains are 4 hops deep.** `--helix-dialog-overlay-bg` → `--helix-surface-overlay` → `--helix-neutral-overlay` → `--helix-black` → `#000000`. Each hop adds fragility and makes debugging harder. 3 hops is the practical maximum — compress to 3 by removing the redundant `--helix-neutral-overlay` layer. |
| TA-07 | 🟡 Medium | Coverage | **Typography semantic tokens exist for size and weight but not for line-height or letter-spacing.** Components set `line-height: 1.5` and `letter-spacing: -0.01em` as raw values. These should be tokenised at the semantic tier (`--helix-leading-normal`, `--helix-tracking-tight`) so typography can be adjusted systematically. |
| TA-08 | 🟡 Medium | Naming | **Component token prefix is inconsistent.** Button tokens use `--helix-button-*`, card tokens use `--helix-card-*`, but toast tokens use `--helix-cmp-toast-*` and dialog uses `--helix-ui-dialog-*`. Pick one convention and migrate. The most common pattern (used by 7 of 10 component token files) is `--helix-{component}-*`. |
| TA-09 | ⚪ Low | Coverage | **No token exists for focus ring offset.** Components use `outline-offset: 2px` as a raw value in 14 places. Create `--helix-focus-ring-offset` as a primitive and reference it from a semantic `--helix-focus-offset` token. |
| TA-10 | ⚪ Low | Naming | **Z-index tokens use raw values as names.** `--helix-z-100`, `--helix-z-500`, `--helix-z-1000` — workable but brittle if a new layer needs to be inserted between existing values. Consider named layers: `--helix-z-dropdown`, `--helix-z-modal`, `--helix-z-toast`. |
| TA-11 | ⚪ Low | Value | **2 orphaned primitive tokens are defined but never referenced.** `--helix-purple-50` and `--helix-purple-100` exist in the colour primitive file but are not referenced by any semantic or component token. If these colours are unused, remove them to keep the primitive tier clean. |

### DTCG 2025.10 compatibility assessment

The Helix token system uses CSS custom properties as its primary format, with a JSON source-of-truth file that generates the CSS output via a build script.

**Current format:**
```css
:root {
  --helix-blue-500: #2563EB;
  --helix-action-primary: var(--helix-blue-500);
  --helix-button-bg: var(--helix-action-primary);
}
```

**DTCG equivalent:**
```json
{
  "helix": {
    "color": {
      "blue": {
        "500": {
          "$value": "#2563EB",
          "$type": "color",
          "$description": "Brand blue, mid-range. Primary brand colour used across action elements."
        }
      }
    }
  }
}
```

**Migration path:**
- The JSON source files can be migrated to DTCG format incrementally — file by file, tier by tier. Style Dictionary v4 supports both formats simultaneously during migration.
- The biggest win is adding `$description` fields at the semantic tier. None of the current 480 tokens have descriptions. Adding them makes the tokens self-documenting for both humans and AI tooling.
- The `$type` field provides explicit type safety. Currently, the system relies on naming convention to distinguish colour tokens from spacing tokens — `$type` makes this machine-readable.

### Remediation priority

**Fix first — structural problems affecting theme switching and consuming teams:**
1. TA-01: Route all component-tier tokens through semantic tokens (9 tier leakage instances). Estimated effort: 8–12 hours. High confidence — the semantic tokens already exist, this is re-pointing references.
2. TA-02: Connect feedback component tokens to the existing semantic feedback tokens (7 variants). Estimated effort: 4–6 hours. High confidence.

**Fix next — naming debt that compounds with every new token:**
3. TA-03: Rename 8 appearance-based semantic tokens to intent-based names. Estimated effort: 6–10 hours (includes updating consuming code). Medium confidence — may surface dependencies in consuming products.
4. TA-04: Create semantic interactive state tokens and re-route component state tokens through them. Estimated effort: 12–16 hours. Medium confidence — requires defining the state colour model first.
5. TA-05: Rename spacing tokens to drop `px` suffix. Estimated effort: 4–8 hours (includes updating consuming code). High confidence — mechanical rename.

**Address eventually — coverage gaps and cleanup:**
6. TA-07: Tokenise line-height and letter-spacing at the semantic tier
7. TA-08: Standardise component token prefix to `--helix-{component}-*`
8. TA-09, TA-10, TA-11: Focus ring, z-index, and orphan cleanup

### Scope

- **Inspected:** 42 token files (14 primitive, 18 semantic, 10 component), `tailwind.config.ts` theme extension, and the token build script
- **Not inspected:** Consuming product codebases (use `token-compliance` for that), Figma variable collections (use `figma-variable-audit` for that), Storybook theme configuration
- **Assumptions:** Token file structure reflects the intended architecture. If tokens are generated from a different source of truth not included in this scan, some findings may not apply.

Some of these findings may reflect deliberate decisions your team already made. If any finding describes something you chose on purpose, flag it — future runs will skip it and focus on the problems you actually need to solve.

---

*Generated by [Design System Ops by Murphy Trueman](https://www.murphytrueman.com) — `skills/token-audit` skill*
*Source: Helix Design System (CSS custom properties, JSON source, React 18, TypeScript, Tailwind v3)*
