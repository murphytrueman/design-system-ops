---
name: token-architecture
type: knowledge
---

# Token architecture principles

**Knowledge note for Design System Ops**
**Auto-loaded by:** token-audit, token-documentation, token-compliance, drift-detection

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

Reserved terms to avoid in semantic token names:
- Colour names (`blue`, `green`, `red`) — describe appearance, not intent
- Size terms used ambiguously (`large`, `small`, `medium`) — use the scale value or a role
- Generic qualifiers (`main`, `default` at semantic level, `base`) — these describe nothing

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

**Token types.** DTCG 2025.10 defines 13 token types: color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, strokeStyle, border, transition, shadow, gradient, and typography. The last five are composite types — they combine multiple sub-values into a single token. Skills should validate token type declarations using the `$type` field and flag untyped tokens as a gap.

**Resolver system.** DTCG 2025.10 introduces resolvers (`.resolver.json` files) that organise tokens into sets and enable theming. A resolver can compose multiple token files, define modes (light/dark, brand variants), and control which tokens resolve differently across contexts. Skills should recognise resolver files and use them to validate theming contracts — if a semantic token is declared in a resolver but missing a mode-specific value, that is a coverage gap.

**Sets and composition.** A token set is a collection of tokens that can be declared inline or referenced from external files. Sets enable multi-file token architectures where primitives, semantics, and component tokens live in separate files and are composed at build time. Skills should map set membership when auditing token coverage.

**Composite token validation.** Composite tokens (typography, shadow, border, transition, gradient) contain sub-values that must reference other tokens correctly. A typography composite where `fontSize` is a hardcoded value but `fontFamily` is a proper token reference is a partial violation — skills should flag sub-value compliance, not just top-level compliance.

**Migration signal.** Teams using older Style Dictionary or custom JSON formats should be flagged with an informational note about DTCG 2025.10 alignment. This is not a violation — it is a maturity signal. The token-audit skill should include a DTCG alignment assessment as a separate section.

---

## Common failure patterns

**The system only has primitives.** Everything that should be a semantic token is either hardcoded or references primitives directly. Theming is impossible. Renaming is catastrophic.

**Semantic tokens describe appearance.** `color.semantic.blue` and `color.semantic.large-text` are not semantic. They are primitives with more typing.

**Component tokens reference primitives.** Looks correct. Breaks the semantic contract. Theming does not propagate.

**Token counts grow faster than the product footprint.** Often indicates semantic tokens being added for one-off use cases rather than reused intent. Audit the long tail.

**Multiple tokens resolve to the same value with no documented distinction.** Either a duplicate (clean it up) or an intentional distinction that has not been documented (document it).
