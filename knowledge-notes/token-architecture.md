---
name: token-architecture
type: knowledge
---

# Token architecture principles

**Knowledge note for Design System Ops**
**Loaded by:** every skill that lists this note in its frontmatter `references:` (the tests keep that list accurate; this header does not repeat it).

---

## The three-tier model

Design tokens are most useful when they are structured in tiers, each serving a distinct purpose. Most systems need at least two tiers (primitives and semantics). A third tier — component tokens — is available when a system's complexity or branding requirements justify it, but it is not assumed. Collapsing tiers — using only primitives, or skipping primitives entirely in favour of semantics — creates problems that compound over time.

### Tier 1: Primitives

Primitives hold raw values. They are the source of truth for every value in the system. Nothing else in the system should define a raw colour, spacing unit, or typographic value that is not declared first as a primitive.

Naming: primitives describe what they are, not what they mean.
- `color.blue.500` not `color.primary`
- `spacing.4` (representing 16px on a 4px base grid) not `spacing.medium`
- `font-size.base` not `font-size.body`

Primitive sets define the available value space. Everything above the primitive tier is a selection from this set.

### Tier 2: Semantic

Semantic tokens encode intent. They reference primitives and apply meaning. A designer or developer working with semantic tokens should be able to understand what a token communicates to users without knowing its resolved value.

Naming: semantic tokens describe function, context, or role — not visual appearance.
- `color.action.primary` — the primary interactive action colour
- `color.feedback.error` — the colour that communicates an error state
- `spacing.component.gap` — the standard gap between components in a layout

Semantic tokens are the tier that enables theming. When a system needs to support multiple themes, brand variants, or dark/light modes, the semantic tier is where the swap happens — not at the primitive or component tier.

A semantic token that describes visual appearance has failed its purpose. `color.semantic.blue` is a primitive with extra steps.

### Tier 3: Component (optional — use when justified)

Component tokens scope semantic intent to a specific component context. They reference semantic tokens and map intent to a specific application. **Not every system needs component tokens.** Many mature systems operate with only primitives and semantics. Component tokens are a targeted tool — use them when a component genuinely needs an override point or when documenting component-level token dependencies in a machine-readable way adds clear value.

Naming: component tokens identify the component, the property, and the state.
- `button.background.default` → `color.action.primary`
- `button.background.hover` → `color.action.primary-hover`
- `card.padding.inner` → `spacing.component.gap`

Component tokens serve two purposes: they make component-level overrides explicit (a consumer can override `button.background.default` without affecting the broader semantic contract), and they document the component's token dependencies in a machine-readable way.

The decision to introduce component tokens should be deliberate and recorded. Common triggers: white-labelling or multi-brand requirements where specific components need brand-level overrides, a component whose visual treatment is expected to diverge from the semantic palette across themes, or a complex component (data table, rich text editor) where the number of semantic references is large enough to warrant explicit documentation. If none of these apply, semantic tokens referenced directly in component code are sufficient.

---

## Tier reference rules

The direction of reference is strictly downward:
- Component tokens reference semantic tokens
- Semantic tokens reference primitive tokens
- No token references a token from a higher-specificity tier

Upward references create circular dependency-like problems: a semantic token that references a component token is no longer semantic in any meaningful sense.

Cross-tier references at the wrong level are the most architecturally damaging token violation. `button.background.default: {color.blue.500}` appears to work — the right colour is applied — but it breaks the semantic contract. A rebrand or theme change that correctly updates the semantic tier will not reach this component.

---

## Naming conventions

Token names should be readable as hierarchical paths: `category.role.variant.state`.

Not all segments are required for every token. A primitive may only need `category.scale-value`. A semantic token needs at minimum `category.role`. A component token needs `component.property.state`.

Terms to flag in semantic token names, and the exceptions that are normal practice:
- Colour names (`blue`, `green`, `red`) describe appearance, not intent. Always flag at the semantic tier.
- Size terms as the whole role (`color.large`, `text.big`) say nothing about purpose. A t-shirt or numeric *scale* is not this: `spacing.sm`, `radius.lg` and `font-size.3` are the standard way to name a scale and must not be flagged.
- Generic qualifiers that stand alone (`misc`, `other`, `alt`, `main` with no role) describe nothing. `default` and `base` are fine as a state or level segment next to a role: `color.action.default`, `color.surface.base` and `button.background.default` (above) are mainstream. Flag them only when they are the entire role (`color.default`, `spacing.base` with no scale).

Compound words should use the system's established casing convention throughout. Common approaches: kebab-case (`color-action-primary`), dot-notation (`color.action.primary`), camelCase (`colorActionPrimary`). Whichever is chosen, apply it without exception.

---

## Cross-platform considerations

Token architecture must account for platform differences at the transformation layer, not in the token names themselves.

Platform-specific values (iOS and Android may use different typefaces; Web uses px, iOS uses pt, Android uses sp) are handled through Style Dictionary transformations or equivalent tooling. Token names should not encode platform specifics.

Acceptable: `spacing.4` transformed to `16px` on web, `16pt` on iOS, `16dp` on Android
Not acceptable: `spacing.web.4`, `spacing.ios.4`, `spacing.android.4`

The exception is when a value genuinely differs by platform in a way that cannot be normalised — in which case the platform-specific token should be documented as an exception, not treated as the normal pattern.

---

## Governance

Token architecture decisions should be recorded. The three most common decisions that benefit from documentation:
- Why specific naming conventions were chosen over alternatives
- Why the primitive scale has the values it does (and what the constraints were)
- Why specific semantic token names were chosen (particularly any that were debated)

Use the `decision-record` skill for any of these.

---

## DTCG 2025.10 alignment

The Design Tokens Community Group released the first stable specification (DTCG 2025.10) in October 2025. Design System Ops token skills should recognise and work with this format natively.

**Token types.** DTCG 2025.10 defines 13 token types: color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, strokeStyle, border, transition, shadow, gradient, and typography. Six are composite types that combine sub-values into one token: strokeStyle (which also accepts a plain keyword such as `"dashed"`), border, transition, shadow, gradient and typography. `fontStyle` is not a defined type (the spec lists it only as a possible future addition).

**Names.** Token and group names must not begin with `$`, and must not contain `{`, `}` or `.` because those characters make up the alias syntax. The dotted paths this note uses in prose (`color.action.primary`) denote group nesting in a DTCG file, not literal dots in a name.

**Type resolution.** A token's type comes from, in order: its own `$type`; if its value is an alias, the resolved type of the token it references; otherwise the closest parent group's `$type`. Only a token with none of these is untyped. Skills should resolve all three before flagging a token as untyped — an alias or a token inside a typed group is valid without its own `$type`.

**Value shapes.** Several simple types take objects, not strings, in 2025.10:
- `color`: `{ "colorSpace": "srgb", "components": [1, 0, 0], "alpha": 1, "hex": "#ff0000" }` (the full colour representation is in the spec's Color module; `alpha` and `hex` are optional)
- `dimension`: `{ "value": 16, "unit": "px" }` — units are `px` or `rem` only
- `duration`: `{ "value": 200, "unit": "ms" }` — units are `ms` or `s`

A file using string values (`"#ff0000"`, `"16px"`) is in an older draft format, not 2025.10. That's a migration signal, not a broken file.

**Resolvers.** The 2025.10 Resolver module adds `.resolver.json` documents that compose token files for theming. A resolver declares `version: "2025.10"`, `sets` (named collections of token sources, inline or external files), `modifiers` (each with a required `contexts` map such as `theme: { light: [...], dark: [...] }` and an optional `default`), and a `resolutionOrder` listing sets and modifiers in the order they apply. Later sources win on conflict; a token that a context does not redefine keeps its earlier value. The spec's term is *context*; it never says "mode". Use resolvers to learn which tokens a theme is *meant* to change. A theme-dependent token (colour, shadow, border colour) that a context does not redefine, so it silently keeps the default theme's value, is a coverage gap. A spacing, radius or duration token that inherits across contexts is normal and is not a finding.

**Sets and composition.** Sets enable multi-file token architectures where primitives, semantics, and component tokens live in separate files and are composed at build time. Skills should map set membership when auditing token coverage, and report a token file that no resolver includes.

**Composite token validation.** Composite tokens contain sub-values that must reference other tokens correctly. A typography composite where `fontSize` is a hardcoded value but `fontFamily` is a proper token reference is a partial violation — skills should flag sub-value compliance, not just top-level compliance.

**Migration signal.** Teams using older Style Dictionary or custom JSON formats should be flagged with an informational note about DTCG 2025.10 alignment. This is not a violation — it is a maturity signal. The token-audit skill should include a DTCG alignment assessment as a separate section.

**Tooling.** Style Dictionary 4 added DTCG support behind `usesDtcg`; Style Dictionary 5 (current) reads DTCG files natively, and its config and hook API differ from 3. Terrazzo is the DTCG-native build and lint tool. Either will validate a file's aliases by building it, which is more reliable than hand-checking; skills should run the tool the repo already has before reasoning about the file themselves.

---

## Common failure patterns

**The system only has primitives.** Everything that should be a semantic token is either hardcoded or references primitives directly. Theming is impossible. Renaming is catastrophic.

**Semantic tokens describe appearance.** `color.semantic.blue` and `color.semantic.large-text` are not semantic. They are primitives with more typing.

**Component tokens reference primitives.** Looks correct. Breaks the semantic contract. Theming does not propagate.

**Token counts grow faster than the product footprint.** Often indicates semantic tokens being added for one-off use cases rather than reused intent. Audit the long tail.

**Multiple tokens resolve to the same value with no documented distinction.** Either a duplicate (clean it up) or an intentional distinction that has not been documented (document it).
