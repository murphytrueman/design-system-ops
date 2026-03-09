# AI-readiness patterns

**Knowledge note for Design System Ops**
**Auto-loaded by:** ai-component-description, pattern-documentation, usage-guidelines, system-health

---

## What AI readiness means for a design system

An AI-ready design system is one that can be consumed, reasoned about, and generated from by AI agents and tooling without requiring implicit knowledge that was never written down.

Most design systems are not AI-ready. They were built for human consumption: designers who can infer intent from visual context, developers who can ask a colleague when the documentation is unclear. AI agents cannot infer, ask, or defer. They work with what is explicitly provided. When a component description says "use this to show important information," an AI agent has no basis for knowing what "important" means in this context, which components should carry that role, or what distinguishes this component from three others that also "show information."

The gap that AI tools expose is not new. The same implicit knowledge that confuses an AI agent has always confused new team members, external contributors, and cross-functional teams working at the edges of the system. AI readiness is design systems quality, applied with more precision.

---

## The context cascade

Context quality at the source compounds through every downstream consumer. Strong metadata in a Figma component → accurate AI-generated code → correct implementation → reliable testing. Weak metadata → hallucinated props → broken implementation → failed tests. Every layer of the system either inherits good context or amplifies bad context. There is no neutral handoff.

This cascade applies to every transition in the design-to-code lifecycle:

- **Design → Code:** Component descriptions, token intent, composition rules, and accessibility contracts all flow downstream. If the design layer embeds purpose and constraints as structured context, code generation receives signal. If it does not, code generation receives noise.
- **Code → Testing:** A component with documented states, props, and edge cases generates comprehensive test coverage. A component without this context produces tests that cover the happy path and nothing else.
- **System → Consumers:** Product teams and AI agents consuming the system inherit whatever quality of context the system provides. Implicit knowledge is lost at every handoff boundary.

The practical implication: invest in context quality at the source (design specs, component descriptions, token documentation) because that investment compounds. Every hour spent making a component description explicit saves multiples downstream in reduced misuse, fewer support requests, and better AI-generated output.

---

## The three pillars: coverage, context, validation

An agent-ready design system requires three things working together:

**Coverage.** Agents need clear examples, states, and constraints so they can build accurately. Coverage means every interactive state is documented (not just the happy path), every prop has types and defaults, every edge case is addressed (long strings, empty states, maximum data density, RTL layouts). Coverage creates predictable patterns through types, normalised examples, composition rules, and test coverage. A component with five documented states produces reliable AI output. A component with only its default state documented produces unreliable output that requires human correction.

**Context.** Coverage alone is not enough — it must be structured for machine consumption. Context transforms documentation into machine-readable metadata that reduces token usage and increases accuracy during agentic workflows. This means structured JSON metadata alongside prose descriptions, consistent section formats that AI can locate and parse, and explicit relationships between components (not just "related to" but "can contain," "contained in," "alternative to"). Context is what turns a design system from a reference library into infrastructure that AI agents can reason about.

**Validation.** Tests and human sign-off guarantee every agent-generated UI is correct and safe to ship. Validation closes the loop: coverage provides the material, context makes it consumable, and validation confirms the output is accurate. This includes automated checks (prop type validation, accessibility testing, token compliance) and human review gates (design review before release, community preview periods).

---

## The six dimensions of component AI readiness

A component is AI-ready when an LLM reading only its description can:

**1. Identify the correct component for a given requirement.**
The description must communicate purpose clearly enough that the component can be selected over alternatives. This requires distinguishing the component from similar components with overlapping use cases.

**2. Configure it correctly for a given context.**
The props must be documented with types, defaults, and intent descriptions specific enough that correct configuration can be inferred from context.

**3. Avoid the most common misuse patterns.**
Anti-patterns must be specific to this component. Generic advice ("use this component appropriately") does not prevent misuse.

**4. Understand its placement constraints.**
Composition rules must state where the component can and cannot be placed, what it can contain, and what can contain it.

**5. Apply it accessibly without additional guidance.**
Accessibility must be documented at the component level — role, keyboard behaviour, focus management — not as a reference to WCAG.

**6. Generate correct usage examples.**
The description must include enough context that an AI generating from this component produces output that matches real-world usage.

---

## The six-section description format

The `ai-component-description` skill encodes a six-section format developed through production use. Each section addresses a specific class of LLM error.

**Purpose** — prevents misidentification. An LLM that cannot distinguish between components will choose the wrong one. The purpose section is the selection signal.

**Props** — prevents misconfiguration. Undocumented or ambiguously documented props produce wrong configurations. The props section is a contract.

**Anti-patterns** — prevents misapplication. The most common LLM errors are the same as the most common human errors. Anti-patterns encode the team's accumulated knowledge about what goes wrong.

**Composition** — prevents structural errors. An LLM that does not know a component's placement constraints will nest it incorrectly, place it in incompatible contexts, or compose it in ways that break the expected behaviour.

**Accessibility** — prevents accessibility regressions. LLMs do not infer accessibility from visual descriptions. The accessibility section must be explicit.

**Examples** — calibrates generation. Without examples, an LLM generating usage must infer from context. With examples, it has reference points for correct output.

---

## Figma MCP integration

Figma's MCP server allows AI tools to read component descriptions directly from a Figma file. This creates a practical path for design systems to provide AI-optimised documentation at the point where design work happens, without requiring a separate tool or documentation platform.

For the MCP integration to work well, component descriptions in Figma must:
- Be structured consistently so an LLM can locate sections reliably
- Be dense enough to be useful without being so long that the token budget is consumed by a single component
- Use plain section headers (PURPOSE, PROPS, ANTI-PATTERNS, COMPOSITION, ACCESSIBILITY, EXAMPLES) rather than markdown formatting — Figma's description field does not render markdown
- Fit within approximately 300 to 600 words per component to leave budget for multiple components in a single context window

The `ai-component-description` skill produces output formatted for this context.

---

## Token AI readiness

Tokens are machine-readable by design — they are structured data. But machine-readable and AI-ready are not the same thing.

For tokens to be useful to AI tooling:
- Semantic token names must encode intent, not appearance. An AI tool cannot infer that `color.semantic.blue` means "primary action" — it can infer that `color.action.primary` does.
- Token documentation must exist at the semantic tier. Primitive token values are self-documenting. Semantic intent is not.
- Token files should be accessible as structured data that AI tools can parse and reason about. Accepted formats include JSON, DTCG, Style Dictionary configurations, CSS custom properties (`:root { --token: value; }`), SCSS/Sass variables, TypeScript/JavaScript token objects, and Tailwind configurations. The key requirement is that the token structure is parseable — AI tools can work with any of these formats as long as naming conventions make the tier hierarchy inferrable.

The `token-documentation` skill produces documentation that serves both human and AI consumers.

---

## System-level AI readiness

Beyond individual components and tokens, a system's overall AI readiness depends on:

**A component manifest.** A structured, machine-readable index of all components with their purposes, categories, and relationships. An LLM selecting components from an undocumented library must guess. An LLM selecting from a manifest can reason.

**Consistent structure.** AI tools read patterns. A system where every component's documentation uses the same structure is significantly more useful to AI tooling than one where each component's docs are formatted differently.

**Explicit relationships.** Which components compose others, which are typically used together, which are alternatives to each other — these relationships are implicit knowledge in most systems and explicit structure in AI-ready ones.

**Version metadata.** AI tools that consume a design system should know what version they are consuming. A system without versioned, machine-readable metadata produces AI outputs that may be based on outdated component contracts.

---

## Machine-readable component manifest

A component manifest is a structured, machine-readable index of every component in the system. It serves as the single source of truth for tooling — AI agents, documentation platforms, linters, and design tools all consume it.

**Why a manifest matters at staff level.** At the senior level, a team documents components individually. At the staff level, the system exposes itself as structured data. An AI agent querying a manifest can resolve "I need a component for user input with validation" to a specific component, variant, and configuration without reading documentation pages. This is the difference between a design system that works with AI and a design system that is legible to AI.

**Manifest structure.** The manifest should be a JSON file at the root of the component library. Minimum viable fields per component:

- `name` — exact component name as used in code
- `category` — functional category (input, display, navigation, layout, feedback, overlay)
- `description` — one-sentence purpose statement (the same quality bar as the ai-component-description Purpose section)
- `props` — array of prop objects with `name`, `type`, `default`, `required`, and `description`
- `variants` — array of variant names with descriptions
- `composedOf` — array of component names this component is built from
- `composedIn` — array of component names that use this component
- `tokens` — array of token names this component binds to
- `a11y.role` — the primary ARIA role
- `a11y.keyboardPattern` — the keyboard interaction pattern name (e.g., "tabs", "dialog", "combobox")
- `challengeRating` — the Component Bestiary CR, if known
- `status` — lifecycle status (alpha, beta, stable, deprecated)
- `version` — current component version

**Relationship to Custom Elements Manifest.** For web component libraries, the custom-elements-manifest (CEM) spec already provides a machine-readable schema. The DS OS manifest extends beyond CEM by adding semantic fields (category, composition graph, token bindings, challenge rating) that AI tools need for reasoning. Teams using CEM should augment it rather than replace it.

**Relationship to Figma MCP.** The Figma MCP server reads component data from Figma files. The component manifest complements this by providing the code-side truth. A staff-level system maintains both, and the `component-audit` skill should cross-reference them for consistency.

---

## Structured JSON metadata for MCP consumption

Beyond the six-section text description, staff-level AI readiness produces structured metadata in JSON that MCP servers and AI agents can parse programmatically without relying on text extraction.

**Why structured metadata matters.** Text descriptions require an LLM to parse natural language to extract prop names, types, and constraints. Structured metadata gives tools direct access. An MCP server returning `{ "component": "Button", "props": [{ "name": "variant", "type": "enum", "values": ["primary", "secondary", "ghost"], "default": "primary" }] }` is immediately consumable by a code generation agent without interpretation.

**The metadata + description pattern.** The structured JSON metadata and the six-section text description serve different consumers: the JSON serves tools (MCP servers, linters, code generators, testing frameworks), the text serves humans and LLMs in conversational contexts. A staff-level system produces both and keeps them in sync.

**Embedding metadata in component source.** The most reliable way to keep metadata accurate is to derive it from the component source. TypeScript interfaces, PropTypes declarations, and JSDoc annotations already contain prop metadata. The `ai-component-description` skill should extract what can be extracted and flag what must be authored manually (purpose, anti-patterns, composition rules).

---

## AI-readiness assessment

Staff-level work does not just describe AI readiness — it measures it. The assessment framework:

**Per-component AI-readiness checklist:**

| Dimension | Check | Status |
|---|---|---|
| Purpose clarity | Can an LLM reliably select this component over alternatives from the purpose statement alone? | ✅ / ⚠️ / ❌ |
| Prop completeness | Are all props documented with types, defaults, and intent? | ✅ / ⚠️ / ❌ |
| Anti-pattern specificity | Are anti-patterns specific to this component, not generic advice? | ✅ / ⚠️ / ❌ |
| Composition explicitness | Are placement constraints, containment rules, and relationships documented? | ✅ / ⚠️ / ❌ |
| Accessibility completeness | Are keyboard patterns, ARIA contracts, and focus management fully specified? | ✅ / ⚠️ / ❌ |

A component with all five checks passing is AI-ready. A component with one or more warnings is partially ready. A component with any failures has gaps that will produce unreliable AI output.

**System-level AI-readiness indicators:**
- Manifest exists and is current (Y/N)
- Structured JSON metadata coverage (% of components with machine-readable metadata)
- Description consistency (% of components following the six-section format)
- Token documentation rate (% of semantic tokens with intent descriptions)
- Cross-reference integrity (% of components where Figma descriptions match code metadata)

The `system-health` skill should include AI readiness as a dimension in the health assessment at the staff level.

---

## Documentation as living infrastructure

Static documentation decays. A component's description drifts from its implementation the moment someone adds a prop without updating the docs. At the staff level, documentation is not a deliverable — it is infrastructure that stays current through automation and enforcement.

**Derive from source where possible.** The most reliable metadata is extracted, not authored. TypeScript interfaces, PropTypes declarations, JSDoc annotations, and Storybook arg types already contain prop metadata. Skills should extract what can be extracted and flag only what must be authored manually (purpose, anti-patterns, composition rules, accessibility contracts). A prop that exists in the TypeScript interface but not in the documentation is a drift signal.

**Automate freshness checks.** A documentation automation pipeline monitors component source for changes and flags stale documentation. The implementation is straightforward: a scheduled process (CI pipeline, GitHub Action, or recurring skill run) compares the component's current prop interface against its documented props. Mismatches are surfaced as findings, not silently ignored. The `drift-detection` skill can serve this function when run on a recurring cadence with source comparison enabled.

**Writing guidelines for consistency.** Teams producing AI-optimised descriptions should maintain a writing guidelines document that specifies tone, structure, terminology, and examples of correct and incorrect descriptions. This document serves both human authors and AI tools generating descriptions — it calibrates output quality regardless of who is writing. The six-section format in the `ai-component-description` skill is this guideline encoded as a skill.

**Lint before handoff.** Before a component is considered release-ready, its metadata should pass a quality gate: all props documented, all interactive states defined, accessibility contract complete, structured JSON metadata in sync with text description. The `component-to-release` agent chain implements this gate. Teams should target comprehensive metadata coverage before handoff, treating incomplete documentation with the same seriousness as failing tests.

---

## What AI readiness reveals about system quality

Preparing a design system for AI consumption is a quality audit. Every place where AI tooling fails to use the system correctly is a place where the system's implicit knowledge has not been made explicit.

Components with ambiguous names, undocumented anti-patterns, and vague purpose descriptions fail AI consumers first and human consumers next. The pressure to make a system AI-ready creates an incentive to fix problems that have existed for years.

This is the forcing-function argument for AI readiness: not that AI tooling is valuable in itself (though it is), but that preparing for it forces the documentation quality and architectural clarity work that improves the system for every consumer.
