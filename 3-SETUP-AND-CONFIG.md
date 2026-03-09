# Design System Ops — Setup and configuration guide

**Version:** 1.1
**Last updated:** 2026-03-08
**Maintainer:** Murphy Trueman · [designsystemops.com](https://designsystemops.com)

This document is the single source of truth for installing, configuring, and getting value from Design System Ops. Update it whenever the product changes.

---

## Prerequisites

Before installing, make sure you have:

1. **Claude Code** installed and running. This is the command-line tool from Anthropic that lets you talk to Claude from your terminal. If you do not have it yet, visit [claude.ai](https://claude.ai) to get started. (Cowork users: you do not need Claude Code — just drag and drop the `.plugin` file.)
2. **Node.js 18 or newer** installed on your computer. This is only needed if you use Style Dictionary to build tokens. If you are not sure whether you have it, open a terminal and type `node --version`. If you see a number like `v18.0.0` or higher, you are good.
3. **Access to your design system's source files** — at minimum, your token files (JSON, SCSS, CSS, or whatever format you use) and your component source code (React, Vue, Twig, etc.)
4. **Figma desktop app** (optional but recommended). Some skills can read your Figma components and variables directly. This is not required — every skill works without it.

---

## Step 1: Install the skill pack

Clone the repo directly into your Claude Code skills directory. The `~` symbol means your home folder (for example, `/Users/yourname/` on Mac or `/home/yourname/` on Linux):

```bash
git clone https://github.com/murphytrueman/design-system-ops.git ~/.claude/skills/design-system-ops
```

**What this means in plain terms:** This creates the `design-system-ops` folder inside the hidden `.claude/skills/` directory in your home folder. The `.claude` folder starts with a dot, so it may be hidden in your file browser — on Mac, press `Cmd+Shift+.` to show hidden files.

If you only want the skills available for one specific project (not globally):

```bash
git clone https://github.com/murphytrueman/design-system-ops.git your-project/.claude/skills/design-system-ops
```

**Example:** If your project is at `~/projects/my-design-system`, the command would be:

```bash
git clone https://github.com/murphytrueman/design-system-ops.git ~/projects/my-design-system/.claude/skills/design-system-ops
```

After cloning, the directory structure should look like:

```
design-system-ops/
├── skills/              38 skills organised by category
├── commands/            13 command definitions
├── knowledge-notes/     11 reference documents (canonical)
├── sample-outputs/      example outputs for reference
├── .claude-plugin/      plugin manifest for Cowork
└── .ds-ops-config.yml   annotated configuration template
```

**Verify the install:** Run any skill by name in Claude Code. Example: "Run token-audit on my token files." Claude should find and load the skill. If it does not, check that the skills directory path is correct in your Claude Code configuration.

---

## Step 2: Prepare your design system inputs

Each skill needs access to specific source material. Here is a mapping of what to prepare for the most common starting workflows:

### For token auditing and compliance

Gather your token files in whichever format your system uses:

| Format | What to provide | Example path |
|---|---|---|
| JSON / DTCG | Token JSON files | `src/tokens/colors.json` |
| Style Dictionary | Config + source files | `style-dictionary/config.json` |
| CSS custom properties | CSS files with `:root` vars | `src/styles/tokens.css` |
| SCSS variables | SCSS partials with `$` vars | `src/styles/_variables.scss` |
| TypeScript objects | Exported token objects | `src/tokens.ts` |
| Tailwind config | `tailwind.config.js` or `.ts` | `tailwind.config.ts` |

The skills accept any of these. You do not need to convert formats.

### For component auditing

Provide access to:
- Your component source directory (e.g. `src/components/`)
- Your Storybook instance URL (if published)
- Your npm package name (if published to a registry)

### For documentation skills

Provide:
- Component source files (the skills read props, variants, and implementation details directly)
- Any existing documentation that should be incorporated

### For governance skills

Provide:
- Your team's contribution workflow (even if informal)
- Any existing ADRs or decision records
- Access to your repository's PR/issue history (for contribution tracking)

---

## Step 3: Run your first skill

Start with one of these depending on your immediate need:

### Option A: "I want to understand the state of my system"

Run `system-health`. This is the broadest assessment and produces a findings-based report across seven dimensions.

```
Prompt: "Run system-health on my design system.
Here are my token files: [path to tokens]
Here is my component library: [path to components]
We have approximately [N] components used by [M] teams."
```

### Option B: "I want to audit my tokens"

Run `token-audit`. This produces a detailed tier analysis with specific findings.

```
Prompt: "Run token-audit on [path to token files].
The tokens are in [format: JSON/SCSS/CSS vars/TypeScript/Tailwind config]."
```

### Option C: "I want to write AI-optimised component descriptions"

Run `ai-component-description`. This is the differentiating skill — it produces six-section descriptions structured for Figma MCP and LLM consumption.

```
Prompt: "Run ai-component-description on [path to Button component].
The component uses [framework: React/Vue/Twig] with [styling: Tailwind/SCSS/Emotion]."
```

### Option D: "I want the full picture"

Run the `full-system-diagnostic` agent. This chains five skills and produces a unified report with cross-skill pattern analysis.

**Note:** If your system has fewer than 5 components, the agent will recommend individual skills instead. See the small-system gate in the agent file.

```
Prompt: "Run full-system-diagnostic on my design system.
Token files: [path]
Component library: [path]
Documentation: [URL or path]
Approximate size: [N] components, [M] consuming teams."
```

---

## Step 4: Configure your team (optional)

**You can skip this step entirely.** Every skill works with sensible defaults. This section is for teams that want to fine-tune how the skills behave.

If you do want to customise, create a file called `.ds-ops-config.yml` in your project's root folder (the same folder where your `package.json` lives). This single file controls three things:

### Severity calibration

This lets you tell the skills how strict to be about different types of problems. By default, a hardcoded colour value is flagged as "High" severity. But if your team actively supports theming (light mode, dark mode, etc.), a hardcoded colour is actually a critical problem — so you can tell the skills to treat it that way.

**Example:** Add this to your `.ds-ops-config.yml`:

```yaml
severity:
  hardcoded_color: critical    # We actively theme — hardcoded colours break theming
  wrong_tier_reference: critical
  naming_violation: high       # Our naming conventions are formalised and enforced
```

**What this does:** Every skill that produces findings (like `token-audit`, `token-compliance`, `drift-detection`) reads these settings and adjusts its severity ratings accordingly. If you do not create this file, skills use sensible defaults that work for most teams.

### Recurring workflow

If you run skills regularly (say, a token audit every quarter), this feature lets the skills remember what they found last time so they can tell you what changed.

**Without recurring:** Each skill run is a fresh start. You get a report, but no comparison to the past.

**With recurring:** Each skill run loads the previous report, compares the findings, and tells you: "17 new violations since Q3, 9 resolved, 23 persistent." It turns one-off audits into a monitoring system.

**Example:** Add this to your `.ds-ops-config.yml`:

```yaml
recurring:
  output_directory: ".ds-ops-reports/"   # Where reports are saved (a folder in your project)
  naming_pattern: "{skill}-{date}"       # Files are named like "token-audit-2026-03-09.md"
  comparison_mode: "full"                # Compare every finding, not just summaries
  retain_count: 8                        # Keep the last 8 reports, delete older ones
```

**What happens when you run a skill with this configured:**

1. The skill checks `.ds-ops-reports/` for a previous report
2. It compares what it finds now against what it found last time
3. It adds a "What changed" section to the output showing new, resolved, and persistent findings
4. It saves the new report and deletes any beyond the last 8

**Skills that support recurring:** `token-audit`, `drift-detection`, `system-health`, `adoption-report`, and all four agents.

### Release gates

Override the component-to-release agent's release gates for agreed team exceptions:

```yaml
gates:
  accessibility:
    contrast_blocks_release: false  # Brand transition in progress — tracking timeline separately
```

A full annotated config template ships with the product at `.ds-ops-config.yml`.

---

## Step 5: Configure integrations (optional)

**You can skip this step entirely.** Every skill works without any integrations. You just provide your files and data manually in the conversation.

Integrations save you time by letting skills pull data automatically. Instead of pasting your Figma file key into every prompt, for example, you configure it once and skills read from Figma directly.

**Think of it this way:** Without integrations, you bring the data to the skill. With integrations, the skill goes and gets the data itself.

### Figma MCP server (HIGH value)

**What it does in plain terms:** Lets Claude read your Figma file directly — components, variables, styles, and analytics. Instead of describing your components or pasting screenshots, skills pull the data straight from Figma.

**Setup:**

1. Install the Figma MCP server by following [Figma's official guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
2. In your Claude Code settings, add the Figma MCP server (the guide above explains how)
3. Create a Figma personal access token (Figma → Settings → Personal access tokens → Generate)
4. Add your Figma file key to `.ds-ops-config.yml`:
   ```yaml
   integrations:
     figma:
       enabled: true
       file_key: "abc123def456"  # This is the string after /design/ in your Figma URL
   ```
   **How to find your file key:** Open your Figma file. Look at the URL — it looks like `figma.com/design/abc123def456/My-File`. The `abc123def456` part is your file key.
5. Test it: Ask Claude "List the variable collections in my Figma file." If it returns real data from your file, the connection is working.

**Skills that use this:** `ai-component-description`, `component-audit`, `design-to-code-check`, `drift-detection`, `token-audit`, `token-documentation`, `system-health`, `adoption-report`

### Style Dictionary v4 (HIGH value)

**What it enables:** Automatic token parsing, DTCG compliance checking, and multi-platform token transformation. When configured, token skills parse your tokens automatically instead of requiring manual file input.

**Setup:**
1. Install Style Dictionary: `npm install -g style-dictionary@4`
2. Add to `.ds-ops-config.yml`:
   ```yaml
   integrations:
     style_dictionary:
       enabled: true
       config_path: "style-dictionary/config.json"
   ```

**Skills that auto-pull:** `token-audit` (full token tree with references), `token-compliance` (token lookup for remediation), `token-documentation` (tier structure + values)

### GitHub API (MEDIUM-HIGH value)

**What it does in plain terms:** Lets Claude search your GitHub repository automatically. Instead of you pasting file contents, skills can search your whole repo for hardcoded values, read component source code, and check PR activity.

**Setup:**

1. Create a GitHub Personal Access Token:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `repo` and `read:org`
   - Copy the token (it starts with `ghp_`)
2. Set it as an environment variable so Claude can use it. Add this to your shell profile (e.g., `~/.zshrc` or `~/.bashrc`):
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```
   Then restart your terminal or run `source ~/.zshrc`.
3. Add to `.ds-ops-config.yml`:
   ```yaml
   integrations:
     github:
       enabled: true
       repo: "yourorg/design-system"  # Your GitHub org and repo name
   ```

**Skills that use this:** `token-compliance`, `token-audit`, `drift-detection`, `component-audit`, `adoption-report`, `system-health`, `ai-component-description`

### npm registry API (MEDIUM value)

**What it enables:** Automatic download statistics and version distribution for adoption tracking. When configured, adoption and audit skills pull download trends without manual data gathering.

**Setup:** No authentication required for public packages. For private packages, configure your `.npmrc` with the appropriate registry token. Add to `.ds-ops-config.yml`:
```yaml
integrations:
  npm:
    enabled: true
    package_name: "@yourorg/design-system"
    scoped_packages: ["@yourorg/button", "@yourorg/card"]  # For monorepos
```

**Skills that auto-pull:** `adoption-report` (download trends), `component-audit` (per-component usage signals), `system-health` (adoption dimension data)

### Chromatic / Storybook (MEDIUM value)

**What it enables:** Visual regression data, component story inventory, documentation coverage checks. When configured, skills pull component inventories from Storybook and visual diff data from Chromatic automatically.

**Setup:**
```yaml
integrations:
  storybook:
    enabled: true
    url: "https://storybook.yourorg.com"
  chromatic:
    enabled: true
    app_id: "your-app-id"
```

**Skills that auto-pull:** `component-audit` (story count, docs tab status), `drift-detection` (visual diffs), `design-to-code-check` (visual snapshots), `ai-component-description` (prop types from stories)

### Documentation platform (MEDIUM value)

**What it enables:** Documentation coverage checking against component inventories. When configured, skills cross-reference your documentation platform to identify under-documented components.

**Supported platforms:** Zeroheight, Supernova, Storybook (docs tab)

**Setup:**
```yaml
integrations:
  documentation:
    enabled: true
    platform: "zeroheight"       # or "supernova" or "storybook"
    url: "https://docs.yourorg.com"
    api_key_env: "ZEROHEIGHT_API_KEY"
```

**Skills that auto-pull:** `component-audit` (docs coverage), `system-health` (documentation dimension), `adoption-report` (page view analytics), `token-documentation` (existing docs to incorporate)

---

## Step 6: Understand the knowledge note system

Skills are powered by bundled knowledge notes. Think of knowledge notes as cheat sheets full of expert knowledge — they contain the frameworks, mental models, and best practices that make skill output production-grade instead of generic. You do not need to do anything to activate them.

**How it works:** Each skill file has a small section at the top (called YAML frontmatter — the part between the `---` lines) that lists which knowledge notes it needs. When Claude runs a skill, it reads those knowledge notes first, then uses that expert knowledge to produce better output.

**Example:** When you run `token-audit`, Claude first reads the `token-architecture` knowledge note (which explains the three-tier token model, naming rules, and common failures). That background knowledge is why the audit catches things like tier leakage and naming violations — it is not guessing, it is applying a framework.

The knowledge notes live in `references/` folders inside each skill category. They are copies of the master files in `knowledge-notes/`.

**The ten knowledge notes:**

| Note | What it provides |
|---|---|
| `token-architecture` | Three-tier model, naming conventions, reference rules, common failures |
| `component-governance` | Contribution criteria, deprecation triggers, lifecycle patterns |
| `ai-readiness` | Six dimensions of component AI readiness, description format |
| `design-to-code-contract` | Design, build, documentation, and release contract definitions |
| `component-bestiary-reference` | Challenge Rating system for documentation depth calibration |
| `agent-orchestration-guide` | Multi-agent coordination patterns and context management |
| `human-oversight-framework` | Human-in-the-loop validation for AI agent workflows |
| `mcp-setup-guide` | Three-layer MCP architecture for design system tooling |
| `context-engine-blueprints` | YAML output templates for all seven context engine blueprints |
| `output-discipline` | Shared quality standards for all skill output — scoping claims to what was inspected, no numeric scores, consistent severity and status indicators, respecting intentional deviations |

**If you modify a knowledge note:** The canonical copy is in `knowledge-notes/`. After editing, sync the updated file to every `references/` subdirectory that contains a copy. The README documents which directories receive each note.

---

## Step 7: Use the sample outputs as benchmarks

The `sample-outputs/` directory contains three real skill outputs:

| File | What it demonstrates |
|---|---|
| `example-token-audit.md` | Full token audit against a ~480 token system with CSS custom properties and JSON source. Shows finding format, severity levels, DTCG compatibility assessment, and remediation priority. |
| `example-component-description.md` | Complete six-section Figma MCP description for a React Dialog component. Shows the exact output format for AI component descriptions. |
| `example-health-dashboard.html` | Interactive HTML dashboard generated from audit findings. Shows Chart.js visualisations, health radar, severity distribution, and responsive layout. Open in a browser to see it in action. |

**How to use them:** Compare your first skill run against the sample. The sample demonstrates the expected depth, specificity, and structure. If your output is significantly less detailed, check that the knowledge notes loaded correctly (the skill should mention reading them in its process).

---

## Framework compatibility

Design System Ops works with any component framework. Here is framework-specific guidance:

### React (JSX/TSX)

The default assumption. All skills work natively with React component files. Styling approaches supported: CSS Modules, SCSS, Tailwind, Emotion, styled-components, CSS custom properties.

### Vue SFC (.vue files)

Skills recognise single-file component structure (`<template>`, `<script>`, `<style>`). When running token-compliance or design-to-code-check, note the styling approach in your prompt:
- Scoped SCSS: `<style lang="scss" scoped>` — violations appear as raw values in style blocks
- CSS custom properties: `var(--token)` references in scoped styles
- `v-bind()` for dynamic CSS: valid token usage when bound to token-backed props

### Twig / Fractal

Skills recognise Atomic Design directory conventions (`01-atoms/`, `02-molecules/`, `03-organisms/`). Components are identified by `.twig` file + `.config.yml` pairs. Token references are typically via BEM utility classes — audit the backing SCSS, not just the template. Inline `style=""` attributes in templates are always violations.

### Emotion / CSS-in-JS with TypeScript

Skills recognise TypeScript token objects (`export const tokens = { ... }`), theme objects, and helper functions (`mapSpacing()`, `boxPalette.foregroundAction`). Token violations are string literals in style objects: `color: '#FF0000'`, `padding: '16px'`.

### Tailwind CSS

Skills distinguish between token references (utility classes mapped to the design system's Tailwind config) and hardcoded values (arbitrary value brackets: `h-[12px]`, `bg-[#ff0000]`). Standard utility classes that resolve to configured tokens are not violations.

---

## Monorepo considerations

If your design system is a monorepo:

- **Per-package npm downloads are unreliable** — use import analysis across consuming products instead
- **Watch for versioning patterns:** `-next` or `-v2` suffixed packages indicate in-flight migrations. Count both but flag the pair.
- **Private vs. public components:** Components with underscore prefixes, in `internal/` directories, or not re-exported from barrel files are internal implementation details — exclude from public counts.
- **Utility vs. user-facing:** Layout primitives (`Box`, `Stack`, `Flex`, `VisuallyHidden`) are infrastructure, not UI components. Categorise separately.

---

## Recommended workflow sequences

### Quarterly review

1. Run `full-system-diagnostic` agent (or individual skills if < 15 components)
2. Run `stakeholder-brief` using the diagnostic as input
3. Run `adoption-report` if usage data is available
4. Share the stakeholder brief with leadership

### Pre-release validation (per component)

1. Run `design-to-code-check` against the Figma spec
2. Run `accessibility-per-component`
3. Run `token-compliance` on the component's source
4. Run `ai-component-description` to generate the Figma description
5. Run `usage-guidelines` to produce the documentation page
6. Run `change-communication` to draft the release announcement

Or use the `component-to-release` agent, which chains these automatically.

### New system lead onboarding

1. Run `system-health` for the big picture
2. Run `component-audit` for the component inventory
3. Run `token-audit` for the token architecture assessment
4. Read the knowledge notes directly for the frameworks behind the skills

---

## Troubleshooting

**"The skill didn't load the knowledge notes"**

This means the `references/` folder inside a skill category is missing files. To check:
1. Open the skill file (e.g., `audit/token-audit.md`)
2. Look at the top of the file — between the `---` lines, you will see a `references:` section listing file names
3. Check that each of those files exists in the `references/` folder of that category (e.g., `audit/references/`)
4. If any are missing, copy them from the master `knowledge-notes/` folder

**Example:** If `audit/token-audit.md` lists `references/token-architecture.md` but that file does not exist in `audit/references/`, copy `knowledge-notes/token-architecture.md` into `audit/references/`.

**"The output is generic / not specific enough"**

This almost always means the skill did not have access to your actual files. Skills produce dramatically better output when they can read your source code directly, rather than working from your description of it.

**Fix:** Instead of describing your tokens ("we have about 200 tokens in three tiers"), point Claude at the actual files: "Audit the tokens in `src/tokens/`." Instead of describing your components, say "Our components are in `src/components/`. Audit them."

**"The skill doesn't understand my token format"**

Tell the skill your format explicitly. The format-specific guidance inside each skill activates based on what you tell it.

**Example prompts that work:**
- "My tokens are in CSS custom properties in `src/styles/tokens.css`"
- "We use SCSS variables — `$color-primary: #0f62fe`"
- "Our tokens are in DTCG JSON format, managed by Style Dictionary"
- "Tokens are TypeScript objects exported from `src/tokens.ts`"

If your format is not recognised, the skill will do its best with naming pattern inference — it can usually detect the structure even without being told the format.

**"The monorepo structure is confusing the audit"**

Tell Claude it is a monorepo in your prompt. The skill has specific handling for monorepo patterns.

**Example:** "Audit our component library. This is a monorepo — packages are in `packages/`. The main library is `packages/core/`."

The skill will then handle: per-package versioning patterns (like `-next` or `-v2` suffixes), private vs public components, utility classification, and unreliable per-package download counts.

---

## Changelog

This section tracks every change to the product. Update it with every modification.

### 2026-03-09 — Ten new skills and eight skill improvements (27 → 37 skills)

**New skills added (10):**

*Practitioner-facing skills (5):*

54. **`system-benchmark`** (audit/) — Benchmarks your system against industry standards and comparable public systems. 12 dimensions across 4 pillars. Industry reference points by system type, percentile estimation, comparison matrix against named public systems. References: token-architecture, component-governance, ai-readiness, component-bestiary-reference.

55. **`session-memory`** (govern/) — Persists findings across skill runs for trend tracking, comparison, and cross-skill correlation. Four modes: Save, Recall, Compare, Correlate. Session file format with YAML frontmatter. Correlation scoring: 2 skills = possible, 3 = probable, 4+ = confirmed systemic. References: agent-orchestration-guide, human-oversight-framework.

56. **`codemod-generator`** (govern/) — Generates jscodeshift migration scripts for token renames, prop changes, import path updates, and component replacements. 5 codemod types, 8 required test cases per transform, migration runner with dependency ordering, CSS/Sass transforms via postcss, untransformable pattern handling. References: component-governance, design-to-code-contract.

57. **`cicd-integration`** (validate/) — Generates CI/CD pipeline configs for GitHub Actions, GitLab CI, CircleCI, and Bitbucket Pipelines. Automation decision matrix, helper script generation, quality gate configuration. References: component-governance, token-architecture, design-to-code-contract.

58. **`visual-report`** (communicate/) — Generates interactive HTML dashboards, charts, and trend visualisations from audit findings. 8 visual types: health radar, severity distribution, trend line, coverage heatmap, dependency graph, comparison bar, action priority matrix, full dashboard. Chart.js CDN, responsive, WCAG AA accessible. References: human-oversight-framework.

*AI infrastructure skills (5) — these produce machine-readable YAML and JSON files for `.ai/` directories, not practitioner-facing documents. They build the structured metadata that AI agents consume when working with your design system:*

59. **`context-engine-builder`** (document/) — Generates a context engine: seven structured blueprint files (UX, UI, content, accessibility, ethical, technical, business intelligence) that encode everything an AI agent needs to work with your design system. Outputs to `.ai/context-engine/`. References: ai-readiness, mcp-setup-guide, context-engine-blueprints.

60. **`governance-encoder`** (govern/) — Converts human governance policies into machine-checkable YAML rules that AI agents can enforce automatically. Outputs to `.ai/governance/`. References: component-governance, agent-orchestration-guide, human-oversight-framework.

61. **`codebase-index`** (audit/) — Generates a pre-computed, machine-readable index of your design system codebase — component inventory, relationship graph, and summary statistics. Outputs to `.ai/index/`. References: ai-readiness, component-governance.

62. **`component-decision-tree`** (document/) — Produces a structured decision tree for choosing between competing or similar components. Machine-readable YAML format for agent consumption, human-readable markdown for documentation. References: component-bestiary-reference, ai-readiness.

63. **`metadata-schema-generator`** (document/) — Generates JSON Schema definitions from your component props and constraints. Produces machine-readable schemas that AI agents use to validate component usage. References: ai-readiness, design-to-code-contract.

**Existing skill improvements (8):**

64. **`accessibility-per-component`** — Added remediation code examples (before/after with WCAG criterion) for every FAIL finding. Added complex component deep-dive protocol for Combobox, DatePicker, DataTable, Modal, and Tabs with 5–6 additional checks each.

65. **`token-audit`** — Added calibrated effort estimates with range, assumptions, and confidence rating. Expanded DTCG migration from one paragraph to a 4-phase plan with before/after code examples and per-phase effort estimates.

66. **`ai-component-description`** — Added expected DOM output requirement in usage examples. Added prose tightness review step with cross-section deduplication rules.

67. **`usage-guidelines`** — Added quick-reference card format (~150 words). Added system-specific voice and tone adaptation with examples for production design systems.

68. **`stakeholder-brief`** — Shortened DS explanation to one sentence maximum. Rewrote "why this matters" to require exactly 2 sentences with urgency pattern.

69. **`deprecation-process`** — Added automated usage counting with concrete grep commands. Added structured usage summary format with per-consumer breakdown. Added timeline visual in Mermaid gantt format with ASCII fallback.

70. **`decision-record`** — Added impact assessment section with quantification table (7 dimensions). Added recommended follow-up skills section linking to 6 other skills based on decision type.

71. **`token-compliance`** — Added messy codebase protocol (legacy value mapping, violation age estimation, hotspot detection). Expanded context-aware severity with era-based adjustments and 7-scenario discrimination examples.

**Documentation updates:**

72. Updated 1-INSTALL.md skill tables from 27 to 37 skills with all new skills and improvement notes.
73. Updated 2-WHATS-INCLUDED.md with new skill descriptions, category counts, folder structure, and "where to use" tables.
74. Updated 3-SETUP-AND-CONFIG.md directory structure and changelog.

---

### 2026-03-08 — Opportunity implementation across all 22 skill and agent files

**Changes made:**

53. **Designer onboarding enhancements**
    - Added Essential reading list (5 resources, 15 min each) for prioritized first-week reading
    - Added Quick reference card template (wallet-sized with key URLs, tokens, shortcuts)

52. **System pitch business metrics**
    - Added Step 1b (Business metrics worksheet): 5-part cost estimation templates (duplicated effort, inconsistency cost, onboarding cost, accessibility risk, speed cost) with calculation formulas

51. **Stakeholder brief business translation**
    - Added Step 2b (Business metrics translation guide): 8-row table mapping DS metrics to business consequences (token adoption→brand fragmentation, drift→duplicated effort, etc.)

50. **Adoption report definition worksheet**
    - Added Step 1b (Adoption definition worksheet): 4-part worksheet defining what "using the system" means, design adoption, engineering adoption, and partial vs full thresholds

49. **Token compliance context-aware severity**
    - Added context-aware violation severity: elevated severity for critical path/high fan-in/theming-sensitive components, reduced severity for utility/deprecated/legacy components

48. **Accessibility screen reader testing guide**
    - Added Step 2b (Screen reader testing guide): practical guides for VoiceOver (macOS) and NVDA (Windows), plus component-type-specific listening guidance

47. **Design-to-code specification checklist**
    - Added Step 1b (Design specification checklist): 8-item pre-handoff checklist (interactive states, spacing tokens, colour tokens, typography, responsive, focus, overflow, touch targets)

46. **Governance review adoption calibration**
    - Added Step 1b (Adoption measurement calibration): maturity-appropriate adoption expectations per level with interpretation guide

45. **Component-to-release type decision**
    - Added Phase 0 (Component type decision): 4×5 classification table (new/enhancement/breaking/bugfix) mapping to validation, documentation, and communication depth

44. **Full system diagnostic synthesis decision tree**
    - Added 7-question binary decision tree in Phase 3 routing to 7 pattern types (concentrated debt, documentation gap, governance gap, structural gap, AI-readiness gap, platform maturity gap, dependency cascade)

43. **Usage guidelines anti-pattern template**
    - Added consistent 4-field anti-pattern template format (What happens, Why it's harmful, What to do instead, How to detect) with example

42. **Token documentation governance and quick reference**
    - Added Step 4b (Token governance note): who owns tokens, request process, change cadence, documentation update responsibility
    - Added Step 6b (Quick reference by semantic function): task-based lookup organized by "I need a colour for...", "I need spacing for...", "I need typography for..."

41. **Pattern documentation discovery and impact**
    - Added Step 0 (Pattern discovery guide): criteria for documentable patterns (3+ contexts, user-facing problem, composes 2+ components, convergent evolution, consequences for errors)
    - Added documentation impact measurement section (reduced drift, reduced support questions, increased consistency)

40. **AI component description anti-pattern inference**
    - Added anti-pattern inference guide after Section 3: 6 inference patterns based on API structure (variant props, size props, disabled props, containers, icon props, action props)

39. **Change communication tailoring matrix**
    - Added Step 1b (Communication tailoring matrix): adjusts messaging by adoption context (high-adoption, partial-adoption, low-adoption/at-risk, new teams)

38. **Decision record trigger checklist**
    - Added Step 0 (Decision trigger checklist): 7 "create a record if" conditions and 3 "skip if" conditions

37. **Deprecation process migration path decision tree**
    - Added 3-step migration path decision tree for when the replacement doesn't cover 100% of use cases (80%+ coverage check → valid needs check → composition possibility check)

36. **Contribution workflow templates and deferred handling**
    - Added proposal template in Stage 1 (What, Why, Evidence, Existing awareness, Contributor commitment)
    - Added deferred proposal handling (re-evaluation dates, backlog logging, escalation on repeated need)
    - Added rejection decision record section using `decision-record` skill

35. **Naming audit decision worksheet**
    - Added Step 1b (Naming decision worksheet): template for establishing conventions (casing, specificity direction, abbreviation policy, tier separator, semantic pattern)
    - Added connection to decision-record in Recommendations section

34. **Drift detection severity weighting and recommendation paths**
    - Added Step 4a (Drift impact severity weighting): weights severity by component criticality (critical path = elevated, utility = reduced)
    - Added recommendation paths by classification table (A→decision-record, B→deprecation-process, C→design-to-code-check, D→change-communication, E→contribution-workflow)

33. **System health baseline calibration**
    - Added Step 1b (Baseline calibration): establishes maturity stage before assessment, with calibrated expectations per stage (e.g., a Managed system shouldn't be penalised for lacking Optimised capabilities)

32. **Component audit usage signals and deduplication**
    - Added Step 1b (Define usage signals): asks users to choose which usage signals they'll track (Figma instantiations, code imports, production shipping, support tickets)
    - Added Deduplication decision rubric in Dimension 3: structured worksheet for identifying and resolving component overlap
    - Added drift-detection tie-in in Dimension 4: cross-references coverage gaps with Classification E findings

31. **PRODUCT_TEST_ANALYSIS.md updated** — All 22 implemented opportunities marked as RESOLVED/IMPLEMENTED across audit, govern, document, validate, communicate, and agent categories

---

### 2026-03-08 — README rewrite for accessibility

**Changes made:**

30. **Token discovery and orphan detection in token-audit**
    - Added Step 0 (Token discovery): auto-searches codebase for CSS custom properties, SCSS variables, JSON/YAML token files, Style Dictionary configs, TypeScript token objects, Tailwind configs, and Tokens Studio exports before asking for manual input
    - Added Step 0b (Orphan detection checkpoint): counts declared vs. referenced tokens, identifies orphaned tokens, produces a quick summary before the full audit begins
    - Step 1 now uses discovered sources as primary input, only asking for manual input if discovery found nothing

29. **README rewritten for novice-friendly clarity**
    - Complete README rewrite focused on beginner accessibility
    - Added "How it works — the key concepts" section explaining what Claude Code, skills, agents, and knowledge notes are
    - Added "Quick start" section with step-by-step clone → install → verify instructions
    - Expanded all 20 skill descriptions with "What it does," "When to use it," "Example prompt," and "What you get back" format
    - Added plain-language explanations for all 3 agents covering what they chain and why chaining matters
    - Added knowledge notes explanation table with what each note provides
    - Added "Two levels of output" section explaining senior vs staff-level output
    - Added "Getting started — recommended first steps" section for different starting points
    - Removed assumption that reader knows Claude Code terminology
    - Removed test repositories from product (not shipped)

---

### 2026-03-08 — Staff-level enhancements

**Changes made:**

17. **DTCG 2025.10 alignment**
    - Added DTCG 2025.10 section to `token-architecture` knowledge note: 13 token types, resolver system, sets and composition, composite token validation, migration signals
    - Added Step 3b (DTCG 2025.10 alignment assessment) to `token-audit`: type declaration compliance, composite sub-value compliance, resolver coverage, color space declarations
    - Added Check 6 (DTCG 2025.10 compliance) to `token-compliance`: type declarations, composite sub-values, resolver coverage, alias chain integrity
    - Added Step 5 (DTCG 2025.10 alignment documentation) to `token-documentation`: type documentation, resolver docs, migration status

18. **Structured JSON metadata and machine-readable manifests**
    - Added component manifest specification to `ai-readiness` knowledge note: minimum viable fields, relationship to Custom Elements Manifest and Figma MCP
    - Added Step 4 (Generate structured JSON metadata) to `ai-component-description`: full JSON schema for machine-readable component metadata
    - Added Step 5b (Machine-readable token reference) to `token-documentation`: JSON reference for semantic tokens with intent, themes, and usage
    - Updated `component-to-release` agent to include structured JSON metadata in release package

19. **Component dependency graphs and blast radius**
    - Added Step 3b (Composition dependency graph) to `component-audit`: fan-in/fan-out analysis, foundation vs hub vs leaf components, token-to-component mapping
    - Added blast radius analysis to `deprecation-process`: direct/indirect impact, migration effort estimation, codemod recommendations, rollback contingency
    - Added breaking change impact modelling to `drift-detection`: per-instance migration cost, aggregate debt, migration path clarity
    - Added Pattern 7 (dependency cascade) to `full-system-diagnostic` agent

20. **API contract validation and platform thinking**
    - Added API contract section to `design-to-code-contract` knowledge note: prop API as public contract, semantic versioning, consumer contract testing, breaking change blast radius, platform SLA thinking
    - Added Step 3b (API contract validation) to `design-to-code-check`: prop contract compliance, type safety, consumer contract signals
    - Added API versioning contract and consumer contract testing to `contribution-workflow`
    - Added API contract summary to `component-to-release` agent release package

21. **Design system maturity model**
    - Added maturity model (five stages: Ad-hoc through Optimised) to `component-governance` knowledge note
    - Added Step 3d (Maturity level assessment) to `component-audit`
    - Updated `system-health` to include maturity level mapping in the report
    - Updated `stakeholder-brief` to frame progress as maturity level transitions

22. **AI-readiness assessment**
    - Added AI-readiness assessment framework to `ai-readiness` knowledge note: per-component checklist, system-level indicators
    - Added Step 3c (AI-readiness assessment) to `component-audit`: per-component assessment, system-level indicators, manifest coverage
    - Added Step 3c (AI-readiness validation) to `design-to-code-check`: metadata drift detection
    - Added Dimension 6 (AI readiness) and Dimension 7 (Platform maturity) to `system-health` (now 7 dimensions)
    - Added Pattern 5 (AI-readiness gap) and Pattern 6 (Platform maturity gap) to `full-system-diagnostic`

23. **Cross-system analysis**
    - Added Step 4c (Cross-system drift) to `drift-detection`: shared primitive divergence, semantic inconsistency, component contract conflicts
    - Added Check 7 (Cross-system token consistency) to `token-compliance`: naming collision analysis
    - Added component dependency graph section to `component-governance` knowledge note

24. **Platform and maturity framing in communications**
    - Added Step 5 (Platform and maturity framing) to `stakeholder-brief`: infrastructure language, maturity level context, AI-readiness as competitive argument
    - Added platform reliability metrics and AI tooling adoption sections to `adoption-report`

25. **Context cascade and agent-readiness framework**
    - Added "The context cascade" section to `ai-readiness` knowledge note: context quality compounds through every downstream consumer, investment at source pays multiples downstream
    - Added "The three pillars: coverage, context, validation" to `ai-readiness` knowledge note: the framework for agent-ready design systems
    - Added "Documentation as living infrastructure" to `ai-readiness` knowledge note: derive-from-source, automated freshness checks, writing guidelines, lint-before-handoff

26. **Pattern state coverage**
    - Added "State coverage" section to `pattern-documentation`: every state the pattern can occupy (empty, loading, populated, error, submitting, success, disabled), transitions between states, component visibility per state
    - Updated quality checks to require state coverage

27. **Accessibility rigour for AI-generated components**
    - Enhanced Section 5 (Accessibility) in `ai-component-description`: semantic HTML over ARIA-only roles, `disabled` vs `aria-disabled` guidance, `aria-label` for icon-only actions, visible focus indicator contrast requirements
    - This addresses the primary failure mode of AI-generated components — accessibility that passes theory but fails testing

28. **README skill examples**
    - Added example prompts and detailed output previews for all 20 skills in the README
    - Each skill entry includes a realistic user prompt and concrete output excerpts showing tables, findings, scores, and recommendations

---

### 2026-03-08 — Integration depth, recurring workflows, and team calibration

**Changes made:**

11. **Team calibration config (`.ds-ops-config.yml`)**
    - Created annotated config template with severity overrides, integration endpoints, recurring workflow settings, and release gate overrides
    - All threshold-using skills read `severity.*` settings before classifying findings
    - Config is optional — all skills work with sensible defaults when absent

12. **Native integration auto-pull**
    - Added Configuration and Auto-pull sections to 8 skills: `token-audit`, `component-audit`, `drift-detection`, `system-health`, `adoption-report`, `token-compliance`, `design-to-code-check`, `ai-component-description`
    - Added integration hooks to 2 document skills: `token-documentation`, `ai-component-description`
    - Supported integrations: Figma MCP, npm registry, GitHub API, Style Dictionary v4, Chromatic, Storybook, documentation platforms (Zeroheight, Supernova)
    - Skills auto-pull data when integrations are configured, skip manual input questions for auto-resolved data, and fall back gracefully when integrations fail

13. **Recurring workflow support**
    - Added Recurring workflow sections to 5 skills: `token-audit`, `drift-detection`, `system-health`, `adoption-report` (via config), and `naming-audit` (inherits via agent)
    - Added Recurring workflow sections to all 3 agents: `full-system-diagnostic`, `governance-review`, `component-to-release`
    - Each recurring run: loads previous report, compares findings (new/resolved/persistent), adds trend section, saves output, prunes old reports
    - Persistent findings (present 3+ cycles) auto-escalate in priority

14. **Agent integration orchestration**
    - All 3 agents now inherit `.ds-ops-config.yml` settings and pass them to chained skills
    - Integration config flows once at the agent level, not per-skill
    - `component-to-release` respects `gates.*` overrides for release-blocking decisions

15. **Documentation platform integration**
    - Added documentation platform as a new integration type (Zeroheight, Supernova, Storybook docs)
    - `component-audit`, `system-health`, `adoption-report`, and `token-documentation` pull from doc platforms when configured

16. **Small-system detection (product-wide)**
    - Extended to all applicable skills: 5 audit, 3 govern, 4 communicate, 2 agents (13 total + existing diagnostic gate)
    - Each note is specific to its skill's domain — not boilerplate

---

### 2026-03-08 — Pre-launch stress test and hardening

**Changes made:**

1. **Knowledge note loading (bundled references)**
   - Created `references/` subdirectories in `audit/`, `govern/`, `document/`, `validate/`
   - Copied knowledge notes to each skill directory that needs them
   - Updated 13 skill files with `references:` YAML frontmatter and "Reference material" body sections
   - Updated README to reflect bundled reference architecture

2. **Expanded token input formats**
   - Added CSS custom properties, SCSS variables, TypeScript/JavaScript objects, and Tailwind config as accepted inputs
   - Updated `token-audit`, `token-documentation`, `token-compliance` with format-specific detection guidance
   - Updated `ai-readiness` knowledge note and all synced copies

3. **Sample output files**
   - Created `sample-outputs/` directory
   - Generated `example-token-audit.md` (Helix, ~480 tokens, CSS custom properties + JSON)
   - Generated `example-component-description.md` (Helix Dialog, React 18, Radix UI)

4. **DTCG compatibility**
   - Added DTCG compatibility assessment section to token-audit sample output
   - Added DTCG format examples showing current vs DTCG-native token structure
   - Referenced Style Dictionary v4 as the migration path

5. **Small-system detection**
   - Added small-system gate to `full-system-diagnostic` agent
   - Systems under 5 components skip cross-skill synthesis; recommends individual skills instead
   - Systems 5–15 components proceed with noted synthesis limitations

6. **Framework-specific guidance**
   - Added Vue SFC, Twig/Fractal, and Emotion/CSS-in-JS detection notes to `token-compliance`, `design-to-code-check`, `component-audit`
   - Added Tailwind arbitrary value bracket detection (distinguishes utility classes from violations)
   - Added SCSS `map-get()` and getter function pattern recognition

7. **TypeScript token object support**
   - Expanded TypeScript/JavaScript guidance in `token-audit` with `as const`, barrel exports, theme-to-CSS-variable mapping patterns
   - Added TypeScript object path documentation guidance in `token-documentation`
   - Covers Emotion and helper-function-style patterns (helper functions, flat/nested exports)

8. **Monorepo handling**
   - Added monorepo-specific section to `component-audit` Step 1
   - Covers: unreliable per-package downloads, versioning patterns (`-next`, `-v2`), private component detection (underscore prefix, internal directories, barrel file exclusion), utility vs. user-facing classification

9. **Extended SCSS/Tailwind awareness**
   - Added styling approach detection to `drift-detection` (token drift section)
   - Added source format expansion to `system-health` and `design-to-code-check` Step 1
   - Framework-specific spacing check notes in `design-to-code-check` Dimension 1

10. **This setup guide**
    - Created `3-SETUP-AND-CONFIG.md` as the single source of truth for installation, configuration, integrations, and troubleshooting

---

If you found this useful, [buy me a coffee](https://buymeacoffee.com/murphytrueman).
