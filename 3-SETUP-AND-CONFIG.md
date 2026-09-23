# Design System Ops — Setup and configuration guide

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
├── skills/              40 skills organised by category
├── commands/            6 command definitions
├── knowledge-notes/     14 reference documents (canonical)
├── sample-outputs/      example outputs for reference
├── .claude-plugin/      plugin manifest for Cowork
└── ds-ops-config.example.yml   annotated config template (copy to your project root as .ds-ops-config.yml)
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

Run the `full-system-diagnostic` agent. This chains six skills (plus conditional theme and Figma audits) and produces a unified report with cross-skill pattern analysis.

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

A full annotated config template ships with the product at `ds-ops-config.example.yml` — copy it into your project root and rename it to `.ds-ops-config.yml`.

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

The knowledge notes are the canonical source in `knowledge-notes/`. Skills reference them directly via relative paths in their frontmatter `references:` field (e.g., `../../knowledge-notes/token-architecture.md`). When you edit a knowledge note, you edit it once in `knowledge-notes/` and all skills automatically pick up the updated version.

**The twelve knowledge notes:**

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
| `adoption-measurement` | Coverage vs adoption distinction, four adoption signals, leading vs lagging indicators, adoption maturity stages |
| `documentation-coverage` | Source-of-truth model, the three rungs of "documented", join-key reliability hierarchy, git-based staleness, per-platform signal matrix |
| `output-discipline` | Shared quality standards for all skill output — scoping claims to what was inspected, proof for empty results, a source for every figure, no numeric scores, consistent severity and status indicators, respecting intentional deviations |
| `executive-communication` | Audience calibration, framing, metric translation, anti-patterns, and numbers honesty for leadership-facing documents |
| `configuration-and-recurring` | How skills load your config, fall back when an integration fails, and run recurring comparisons. Read only when a `.ds-ops-config.yml` exists |

**If you modify a knowledge note:** Edit the file directly in the `knowledge-notes/` directory. All skills automatically reference the updated version through their `references:` frontmatter field — no syncing needed. The change takes effect immediately for all skills that use it.

---

## Step 7: Use the sample outputs as benchmarks

The `sample-outputs/` directory contains 13 sample outputs. The five `fixture-*` files are unedited runs against the test design system in `tests/fixtures/`:

| File | What it demonstrates |
|---|---|
| `example-token-audit.md` | Full token audit against a ~480 token system with CSS custom properties and JSON source. Shows finding format, severity levels, DTCG compatibility assessment, and remediation priority. |
| `example-component-description.md` | Complete six-section Figma MCP description for a React Dialog component. Shows the exact output format for AI component descriptions. |
| `example-health-dashboard.html` | Interactive HTML dashboard generated from audit findings. Shows Chart.js visualisations, health radar, severity distribution, and responsive layout. Open in a browser to see it in action. |
| `system-health-meridian.md` | Health assessment across seven dimensions with status labels, a maturity stage inferred from evidence, and a Scope block. |
| `component-audit-react-library.md` | Component inventory with Challenge Ratings, duplication analysis, and "likely unused" findings backed by a positive control. |
| `drift-detection-harbor-consumer-app.md` | Drift analysis of a consumer app: hardcoded values, local re-implementations, and suggested fixes, each classified by cause. |
| `stakeholder-brief-meridian-q1.md` | One-page executive brief with every figure sourced and open placeholders listed at the top. |
| `docs-coverage-carbon-react.md` | Docs coverage audit of a real public Storybook: coverage by rung, git-based staleness, and join-confidence tiers. |
| `fixture-token-audit.md` | Unedited run against the test fixture: tier leakage in `card.border` found and traced to the dark-mode break it causes. |
| `fixture-token-compliance.md` | Unedited run against the test fixture: an off-palette hex logged once with its nearest token, exempt keywords correctly left alone. |
| `fixture-docs-coverage.md` | Unedited run against the test fixture: an exported component with no story, with path-resolved join confidence. |
| `fixture-accessibility-per-component.md` | Unedited run against the test fixture: a tooltip with no `aria-describedby` link and no hover or focus behaviour, nothing marked PASS on code inference alone. |
| `fixture-theme-audit.md` | Unedited run against the test fixture: a border with no dark value found, correct dark elevation and inherited spacing left alone. |

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

Skills stop and say so when this happens. The usual cause is a third-party installer (for example `npx skills install`) that flattened each skill into its own folder and dropped the repo-root `knowledge-notes/` directory the skills load from.

1. Run `bash verify-install.sh` from the install root (e.g. `~/.claude/skills/design-system-ops/`). It lists every missing reference and exits non-zero if any are gone.
2. If it reports `MISSING` lines, reinstall with git clone or the `.plugin` bundle — see [1-INSTALL.md](1-INSTALL.md). Those are the only supported methods.
3. If you can't run the script, check by hand: open the skill file (e.g. `skills/token-audit/SKILL.md`), find the `references:` list between the `---` lines at the top, and confirm each path resolves from the skill's folder (e.g. `../../knowledge-notes/token-architecture.md` → `knowledge-notes/token-architecture.md` at the install root).

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

## Release history

What changed in each release, and why, is in [CHANGELOG.md](CHANGELOG.md).

---

If you found this useful, [buy me a coffee](https://buymeacoffee.com/murphytrueman).
