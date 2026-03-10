# System health assessment

**Skill:** `skills/system-health`
**Source:** CampusIQ Design System — React/Tailwind component library
**Assessment date:** 2026-03-10
**Assessment type:** Direct inspection (Figma library, npm package, GitHub repository)
**Assessed by:** Design Systems team

---

## Overall health score

**23 / 35** — Functional system with significant gaps in adoption and governance. The system is internally consistent and well-documented, but adoption is uneven across product teams and governance processes are not yet documented. With focused attention on the next two dimensions below, the system moves from Level 2 (Managed) to Level 3 (Systematic).

### Dimension scores

| Dimension | Score | Status |
|-----------|-------|--------|
| Tokens | 4/5 | Solid |
| Components | 3/5 | Functional with gaps |
| Documentation | 4/5 | Strong |
| Adoption | 2/5 | Below expectation for this maturity level |
| Governance | 2/5 | Present but informal |
| AI readiness | 4/5 | Solid |
| Platform maturity | 2/5 | Early stage |
| **Total** | **23/35** | **Level 2–3 transition** |

**Score interpretation:** The CampusIQ system is at a critical junction. Token and documentation work is strong — the foundation is solid. AI readiness is surprisingly mature for a Level 2 system. But adoption is the constraint: teams are not using what has been built. Governance is informal, which means decisions are not recorded and processes are opaque to consuming teams. The next six months should focus on raising adoption and documenting governance.

---

## Maturity level assessment

**Current level: Level 2 (Managed)** — The library exists with some governance. Token architecture is established. Documentation is consistent. Contribution process exists but is informal. Teams are aware of the system but adoption is patchy.

**Why Level 2, not Level 3:** The missing elements are explicit governance processes and adoption tracking. Level 3 requires documented contribution criteria, a deprecation process, and adoption signals that inform prioritisation. CampusIQ has informal versions of all three — the design systems team knows who should contribute and when a component should be deprecated, but these processes are not documented. A new team member cannot predict how to propose a component. Consuming teams cannot see whether their feedback about missing components is considered. This informality limits adoption and creates support burden.

**Path to Level 3:** Document the contribution and deprecation processes explicitly (4 weeks). Establish recurring adoption tracking with a simple dashboard showing component usage by team (2 weeks). Run a governance communication sprint: announce the processes to all consuming teams and record the key decision rationale for existing components (2 weeks). With these complete, the system meets Level 3 criteria.

---

## Dimension findings

### Tokens — 4/5

**Finding 1: Three-tier architecture is complete and consistently applied.**
Primitives (colour, spacing, typography, borders, shadows, z-index) are clearly separated from semantic tokens (action colour, form states, layout spacing, elevation) and component-tier tokens are sparse but well-formed. All component-tier tokens reference semantic tokens, no tier leakage detected. Token names follow an intent-based naming convention (`color.action.primary` not `color.blue.500` at the semantic tier).

**Finding 2: Token files are DTCG-adjacent but not yet compliant.**
Style Dictionary format is used with `.json` files. Tokens have `value` and `description` fields at the semantic tier, but primitive tokens lack descriptions. This is a minor gap — the team is close to full DTCG readiness and the token files are already consumable by AI tooling.

**Finding 3: Token documentation is sparse at the primitive tier.**
Primitive tokens lack intent descriptions. A developer seeing `spacing.2` (which resolves to `0.5rem`) must infer what it is used for. This creates configuration confusion and missed optimization opportunities when rebasing spacing values. Recommendation: Add short intent descriptions to all primitive spacing and sizing tokens (`spacing.2: "Compact spacing for nested form groups and dense list items"`).

**Most important action:** Add intent descriptions to primitive tokens before Q2 release. This unlocks opportunities for AI-assisted design-to-code workflows and reduces configuration errors.

### Components — 3/5

**Finding 1: API consistency is strong across 30 core components.**
All components use consistent prop naming (boolean props are prefixed `is`, size props use T-shirt naming). All components document their prop interface in TypeScript. Variants are used where appropriate, not as a substitute for composition. This API consistency is a strength and makes the system easier for teams to learn.

**Finding 2: Coverage of foundational components is complete, but compound components are under-resourced.**
The system has excellent coverage of primitives: Button (6 variants), Input (4 variants), Checkbox, Radio, Select, TextArea, Icon, Badge, Tag. Compound components are fewer: Card, Modal, Popover, Dropdown. Feature components are minimal (only Dialog and Notification). The distribution suggests the system is well-designed for building new interfaces. Teams report occasionally building local cards and toasts because the system versions did not fit their specific needs.

**Finding 3: Component state coverage has one systematic gap: error states.**
All interactive components (Input, Select, TextArea) document disabled state. None document error state (aria-invalid, error text, error colour). This is a recurring support question: "How should I show validation errors?" The answer exists in the design system (Input with aria-invalid + supporting text), but it is not documented as a pattern. Recommendation: Add an "error state" story to Input and TextArea. Document the pattern in usage guidelines.

**Most important action:** Document error state pattern for form inputs. This closes the gap that teams are currently working around locally.

### Documentation — 4/5

**Finding 1: Storybook is comprehensive and well-maintained.**
Every component has at least one story per documented state. Stories include controls for all interactive props. Accessibility panel is visible in all stories. Documentation tab exists for 28 of 30 components with usage guidelines, anti-patterns, and accessibility notes. Average words per component description: 320 (good balance of depth and scannability).

**Finding 2: Component usage guidelines follow the six-section AI-optimised format consistently.**
Purpose, props reference, anti-patterns, composition, accessibility, and examples are present in every documentation entry. This consistency makes the documentation useful to both humans and AI tooling. Figma components have descriptions in the same format, enabling Figma MCP integration.

**Finding 3: Two components lack documentation: Popover and Dropdown.**
Both are recent additions (added in the last four weeks). They are building-blocked: Storybook is running but documented usage guidelines have not been written. This is a known gap and the documentation is scheduled for completion by end of week. No action needed; noting the recency to calibrate the score.

**Most important action:** Maintain documentation completeness for all new components before release. The current process (build first, document later) has created this gap. Recommend: documentation written before release gates the component from appearing in the published npm package.

### Adoption — 2/5

**Finding 1: Adoption is uneven across product teams.**
Three teams (Facilities, Roster, Finance) have 70%+ adoption of system components. Two teams (Mobile, Analytics) have 20–30% adoption. One team (Integrations) has <5% adoption and builds almost everything locally. The system is optional, not required, which means adoption depends on team choice and incentives. No metric is tracked that would help understand why adoption varies (is it feature gaps, documentation, team preference, or something else?).

**Finding 2: The high-adoption teams are design-driven; the low-adoption teams are engineering-driven.**
Teams where design leads the development process use the system. Teams where engineering leads use system components as a starting point but diverge. This suggests the system is designed for design workflows but does not meet the full needs of engineering-independent development.

**Finding 3: No adoption tracking infrastructure exists.**
npm download metrics do not distinguish between different consumers. There is no dashboard showing which teams use which components or how often. Feedback from teams about missing components is not systematically recorded. Without this data, prioritisation of new components is based on vocal requests, not evidence of need.

**Most important action:** Establish adoption tracking with a monthly dashboard. Track: (1) components by adoption tier (core, growing, niche), (2) components with zero usage, and (3) missing component requests by team. This data informs the next two quarters of roadmap decisions.

### Governance — 2/5

**Finding 1: Contribution criteria exist but are not documented.**
The design systems team has a mental model of what belongs in the system (used by 2+ teams, generalised beyond one product's specific needs, maintainable by a single owner). New contributions are evaluated against these criteria, but the criteria are not written down. Consuming teams cannot predict whether a proposal will be accepted.

**Finding 2: No deprecation process exists.**
A Button variant has been used by one team for six months then abandoned (replaced with a new design). The variant remains in the system with zero usage. No process exists to surface these candidates for removal or to communicate deprecations to teams. Components accumulate indefinitely.

**Finding 3: Decision records do not exist for architectural choices.**
The decision to use Tailwind CSS for styling is known to the team, but the alternatives that were considered are not documented. New team members learn through conversations, not documents. This informality makes it harder to onboard and creates risk — if the person who made the decision leaves, the reasoning goes with them.

**Most important action:** Write and publish: (1) contribution criteria, (2) deprecation process, (3) decision record template and policy. These documents should be added to the system's GitHub wiki or README and communicated to all consuming teams. Expected effort: 8 engineering hours spread over two weeks.

### AI readiness — 4/5

**Finding 1: The six-section description format is implemented consistently across 28 of 30 components.**
Purpose, props, anti-patterns, composition, accessibility, and examples are present. Descriptions are dense enough to be useful (250–400 words per component) without exceeding token budgets. Figma component descriptions are in sync with code documentation. This is a staff-level strength.

**Finding 2: Component manifest does not exist.**
There is no machine-readable JSON index of components, their props, variants, and relationships. An AI agent selecting components from the system must parse Storybook or Figma; it cannot query a manifest. Building a manifest would unlock code generation workflows: an LLM could reliably select the correct component, configure it with the right props, and validate the output against a known API contract.

**Finding 3: Token files are AI-consumable but undescribed at the primitive tier.**
Tokens are in Style Dictionary format with consistent naming. Semantic tokens have intent descriptions. Primitive tokens do not. An AI agent generating colour tokens has no way to infer what `color.neutral.100` is used for — it is white with a name that says "neutral 100." This limits AI token-generation accuracy. Recommendation: Add one-sentence descriptions to all primitive tokens.

**Most important action:** Build a component manifest (JSON, 300 lines of code, 8 hours of effort). This is the infrastructure that unlocks AI-assisted development. Mask tokens with descriptions at the primitive tier (already flagged in the Tokens dimension).

### Platform maturity — 2/5

**Finding 1: No semantic versioning is applied.**
The npm package is published at version `1.x.x` with no patch/minor/major distinction. Changes are released as a semver patch regardless of whether they are breaking changes. This makes it impossible for consuming teams to plan upgrades confidently. A team on v1.2.3 cannot know whether v1.2.4 includes breaking changes without reading the changelog.

**Finding 2: Release cadence is irregular and not communicated.**
Releases happen roughly monthly but dates vary (4–8 weeks between releases). Consuming teams cannot plan feature work around system releases. If a team needs a component for a feature, they cannot estimate whether the system will have it before their deadline.

**Finding 3: No migration path exists for breaking changes.**
When the Button API was significantly expanded in the last release (new props, changed defaults), no migration guide was written. Teams using the old API were not notified in advance and had to discover the change through failed tests.

**Most important action:** Implement semantic versioning immediately. Document the versioning policy, release cadence (propose: second Tuesday of each month), and the changelog process. For the next release, include a migration guide for the Button changes. Expected effort: 4 engineering hours for documentation; no code changes required.

---

## Prioritised action list

### Immediate (next 4 weeks)

These actions unlock other improvements or prevent trust erosion:

1. **Document contribution criteria and publish to the team wiki.** Teams are already asking how to propose components; formalising this removes friction and builds predictability. (4 hours)

2. **Implement semantic versioning for the next release (target: end of March).** This single change removes uncertainty for all consuming teams. No code required; policy only. (2 hours)

3. **Document the error state pattern for form inputs and release in Storybook.** This closes a known gap that teams are currently working around. One story + documentation page. (3 hours)

4. **Establish a monthly adoption dashboard.** This data is needed to prioritise the next quarter's roadmap. Manual data collection acceptable for first month; automate if needed next quarter. (6 hours)

---

### Near-term (next quarter)

Structural improvements that require planning:

5. **Write deprecation process and decision record policy.** Enables clean maintenance of the component inventory going forward. (8 hours split over two weeks)

6. **Build component manifest in JSON format.** Unlocks AI-assisted code generation workflows and significantly improves developer tooling integration. (8 hours)

7. **Add intent descriptions to all primitive tokens.** Completes DTCG readiness and improves AI token generation. (4 hours)

8. **Run a governance communication sprint.** Announce processes to all consuming teams and record key architectural decisions. (8 hours plus async team time)

---

### Longer-term (6+ months)

Investments that compound over time:

9. **Scale adoption in low-adoption teams.** Conduct discovery with Integrations and Analytics teams to understand why system adoption is low. Is it missing components, performance concerns, or team preference? Design a targeted intervention. (16 hours of discovery + analysis)

10. **Expand compound component coverage.** Based on adoption tracking, identify the highest-value missing components (likely: more layout patterns, data table variants, form patterns). Plan contributions from high-adoption teams. (Roadmap item for Q2/Q3)

11. **Implement consumer contract testing.** Add tests that validate consuming applications are calling components correctly. This prevents silent failures and creates a feedback loop for API design. (Engineering effort TBD based on the testing framework chosen)

12. **Establish staff-level AI integration patterns.** Document and codify how the system supports AI-assisted development. Develop reusable prompts and workflows. Publish case studies. (Research + documentation, ongoing)

---

*Generated by Design Systems OS — `skills/system-health` skill*
*Source repository: CampusIQ Design System (React 19, Tailwind v4, Figma + Storybook)*
