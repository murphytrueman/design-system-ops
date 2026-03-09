# Installing Design System Ops

[designsystemops.com](https://designsystemops.com)

## Quick start (2 minutes)

**In Cowork (desktop app — easiest, no terminal needed):**
1. Download `design-system-ops.plugin` from the [`installable/`](installable/) folder in this repo
2. Open the Claude desktop app and start a Cowork session
3. Drop the `.plugin` file into the chat
4. Follow the install prompt — done

**In Claude Code (terminal):**
1. Clone the repo directly into your skills directory:
   ```bash
   git clone https://github.com/murphytrueman/design-system-ops.git ~/.claude/skills/design-system-ops
   ```
   For project-level installation instead of global:
   ```bash
   git clone https://github.com/murphytrueman/design-system-ops.git your-project/.claude/skills/design-system-ops
   ```
2. Open Claude Code and try: "How healthy is my design system?"
3. If Claude responds with a structured, multi-step process — not generic advice — you're set up

---

## Point it at your design system

The skills need access to your design system's files. How you provide access depends on which tool you're using.

**In Cowork:** Click the folder icon in the top bar and select your design system's project folder. Once selected, skills can find your token files, component directories, and configuration automatically.

If your design system spans multiple repositories, select the root folder that contains both — or select the most relevant one and provide paths to others when asked.

**In Claude Code:** Open Claude Code from within your project directory:

```bash
cd ~/projects/my-design-system
claude
```

If your project is a monorepo, open from the root so skills can traverse packages.

**What the skills look for:** Most skills start by scanning your project for recognisable files. They look for things like:
- Token files: `.json` files with token definitions, `.scss` files with `$variables`, `.css` files with `--custom-properties`
- Component directories: folders named `components/`, `src/`, or anything with React/Vue/Twig files inside
- Config files: `package.json`, `storybook/`, `tailwind.config.js`, `style-dictionary/`

If a skill cannot find what it needs, it asks you. You can always include paths in your prompt to skip the scanning step entirely.

**Example:** "Audit the tokens in `src/tokens/`" or "Our components are in `packages/ui/src/components/`".

---

## Start here: pick your entry point

You don't need to memorise skill names. Describe what you need in plain language and the right skill activates. But if you're not sure where to begin, pick the scenario that sounds most like your situation.

### "I just want to know where we stand"

**Say:** "How healthy is my design system?"

This triggers `system-health`, which assesses your system across seven dimensions — tokens, components, documentation, adoption, governance, AI readiness, and platform maturity. Each dimension gets a status (Strong, Functional, Weak, or Absent) with specific evidence and a prioritised action list.

**Example output:**

```
Your system is strong on components and tokens, but governance
and documentation are the bottleneck. Here's the dimension-by-
dimension picture.

| Dimension          | Status       | Key finding                    |
|--------------------|--------------|--------------------------------|
| Tokens             | 🟢 Strong    | Three-tier architecture, clean |
| Components         | 🟢 Strong    | 89 components, good API docs   |
| Documentation      | 🟡 Functional| Present but no anti-patterns   |
| Adoption           | 🟡 Functional| Used by eng, not design        |
| Governance         | 🟠 Weak      | No deprecation process         |
| AI readiness       | 🔴 Absent    | No structured metadata         |
| Platform maturity  | 🟡 Functional| Versioned but no SLAs          |
```

**Good for:** Quarterly reviews, new DS lead onboarding, preparing a stakeholder conversation.

---

### "Our tokens are a mess"

**Say:** "Audit my tokens"

This triggers `token-audit`. The skill scans your codebase for token files automatically (CSS custom properties, SCSS variables, JSON/DTCG files, TypeScript objects, Tailwind configs), maps the tier structure (primitive → semantic → component), and runs checks against naming, values, coverage, and DTCG compliance.

**Example output:**

```
TA-01 | 🔴 Critical | Value | Component tokens hardcoded to hex
  button.background.default: '#0f62fe' instead of
  referencing semantic token {color.action.primary}

TA-02 | 🟠 High | Naming | 42 semantic tokens use numeric
  suffixes without documented rationale
  layer01, layer02, field01 — unclear what numbers mean

Remediation priority:
  Fix first: TA-01 (12–16 hours, High confidence)
  Fix next: TA-02 (8–12 hours, Medium confidence)
```

**Good for:** Token architecture reviews, pre-migration assessment, identifying structural debt.

---

### "I need to make our components AI-ready"

**Say:** "Write an AI component description for Button"

This triggers `ai-component-description`. The skill reads your component's source code (or Figma component if connected), and generates a structured six-section description optimised for LLM consumption: purpose, states and interactions, accessibility, common patterns, variants and props, and migration notes.

**Example output:**

```
## Button

### Purpose
A clickable element that triggers an action. Use Button for
primary, secondary, and tertiary actions. Do NOT use for
navigation — use Link instead.

### States and interactions
- Default → Hover (cursor: pointer, background lightens)
- Focus (2px ring, offset 2px, meets WCAG 2.4.7)
- Active (background darkens, scale 0.98)
- Disabled (opacity 0.4, pointer-events: none)
- Loading (spinner replaces label, aria-busy="true")
...
```

With the Figma Console MCP connected, the description gets written directly into the component's description field in Figma — visible in Dev Mode immediately.

**Good for:** Making your library usable by AI coding tools, improving Figma Dev Mode content, standardising component documentation.

---

### "We need to deprecate a component"

**Say:** "Help me deprecate DatePicker in favour of DatePickerNext"

This triggers `deprecation-process`. The skill searches your codebase for every usage of the component being deprecated, counts consuming teams, produces a blast radius analysis, drafts a migration timeline, and generates the communication package.

**Example output:**

```
Blast radius:
  4 consuming teams, 23 files, 47 import statements

Migration timeline:
  Week 1-2: Publish deprecation notice, add console warning
  Week 3-6: Teams migrate (estimated 2-4 hours per team)
  Week 7-8: Remove from library, verify zero remaining imports

Communication draft:
  [Full announcement with migration guide, before/after
   code examples, and FAQ]
```

**Good for:** Managing breaking changes without breaking trust, giving teams a predictable migration path.

---

### "I need to convince leadership to invest in the system"

**Say:** "Write a stakeholder brief for leadership about our design system"

This triggers `stakeholder-brief`. The skill produces a one-page brief in business language — no design system jargon — with a clear situation, consequences of inaction, specific recommendation, and a concrete ask.

**Example output:**

```
SITUATION
Our design system serves 6 teams and 40+ components. Two of
seven health dimensions are weak — governance and documentation.
This means changes ship without migration paths, and new team
members take 3x longer to onboard.

WHY THIS MATTERS
Every uncoordinated component change costs 3-4x more to fix
after shipping than it would cost to prevent.

WHAT WE RECOMMEND
One dedicated engineer + one designer for two quarters.

WHAT WE NEED
1. Headcount approval for Q3-Q4
2. Executive sponsor for quarterly reviews
3. Agreement to treat the system as shared infrastructure
```

**Good for:** Budget requests, quarterly exec updates, making the case for dedicated DS headcount.

---

### "I need to check accessibility on a specific component"

**Say:** "Run an accessibility audit on our Accordion component"

This triggers `accessibility-per-component`. The skill checks keyboard navigation, screen reader behaviour, ARIA contracts, focus management, colour contrast, motion sensitivity, and forced-colours mode — with code examples for every finding.

**Example output:**

```
ACC-01 | 🔴 Critical | Keyboard | Missing arrow key navigation
  between accordion headers
  Expected: Up/Down arrows move focus between headers
  Found: Only Tab key works — traps user in sequential nav

ACC-02 | 🟠 High | ARIA | Missing aria-expanded on trigger
  Expected: aria-expanded="true|false" on each header button
  Found: No aria-expanded attribute present

  Fix:
  <button aria-expanded={isOpen} aria-controls={`panel-${id}`}>
```

**Good for:** Pre-release accessibility validation, fixing specific WCAG violations, building accessible component documentation.

---

### "Show me where teams are going off-system"

**Say:** "Check where teams have drifted from our design system"

This triggers `drift-detection`. The skill scans consuming codebases for hardcoded values, local reimplementations, token overrides, and version lag — then classifies each instance so you know what to fix versus what to discuss.

**Example output:**

```
Drift classification:
| Type | Count | Example |
|------|-------|---------|
| A — Intentional divergence | 3 | Checkout uses custom button for payment flow |
| B — Version lag | 8 | Team Alpha on v2.1, current is v3.0 |
| C — Accidental drift | 12 | Hardcoded #0066CC instead of var(--color-action) |
| D — Misunderstanding | 4 | Using Card for layout instead of Box |
| E — System gap | 2 | No date range picker, team built their own |

Priority: Fix C (accidental) first. Document A (intentional).
Evaluate E (gaps) for contribution.
```

**Good for:** Quarterly governance reviews, understanding why teams go off-system, identifying contribution candidates.

---

### "I'm releasing a component and want to validate everything"

**Say:** "Run the release pipeline for Dialog"

This triggers the `component-to-release` agent, which chains six skills in sequence: design-to-code check → accessibility audit → token compliance → AI component description → usage guidelines → change communication. One prompt, full pre-release validation.

**Good for:** Shipping components with confidence, catching issues before they reach consumers.

---

### "Give me the full quarterly picture"

**Say:** "Run a full system diagnostic"

This triggers the `full-system-diagnostic` agent, which chains: token-audit → naming-audit → component-audit → drift-detection → system-health. Produces a comprehensive report with cross-referenced findings and a unified action plan.

**Good for:** Quarterly reviews, annual planning, board-level reporting on system health.

---

## Every skill, with an example prompt

### Audit (8 skills)

| Skill | What to say | What you get |
|-------|-------------|-------------|
| `token-audit` | "Audit my tokens" | Naming violations, tier leakage, hardcoded values, DTCG alignment, orphan count, effort estimates |
| `component-audit` | "Audit my component library" | Inventory with usage, duplication, coverage gaps, complexity distribution, stale components |
| `system-health` | "How healthy is my design system?" | 7-dimension assessment with statuses, prioritised action list, maturity stage |
| `drift-detection` | "Where are teams going off-system?" | Classified drift instances (intentional/accidental/version lag/gap), blast radius per instance |
| `naming-audit` | "Are our naming conventions consistent?" | Component, token, and file naming violations with suggested renames |
| `figma-variable-audit` | "Audit my Figma variables" | Variable naming, tier structure, mode consistency, code-vs-Figma mismatches |
| `codebase-index` | "Build a component map of our system" | Machine-readable component index with file paths, exports, dependencies, and categories |
| `system-benchmark` | "How does our system compare to industry standards?" | 12-dimension benchmark against comparable public systems |

### Govern (10 skills)

| Skill | What to say | What you get |
|-------|-------------|-------------|
| `contribution-workflow` | "Document our contribution process" | Step-by-step contribution guide with templates, review criteria, and decision tree |
| `deprecation-process` | "Deprecate DatePicker for DatePickerNext" | Blast radius analysis, migration timeline, communication package, codemod suggestions |
| `decision-record` | "Record why we chose DTCG over custom tokens" | Structured ADR with context, options evaluated, decision rationale, consequences |
| `change-communication` | "Write release notes for Button v3" | Release notes, migration guide, team announcement — three audiences, one command |
| `backlog-generator` | "Turn these audit findings into tickets" | Sprint-ready work items with acceptance criteria, effort estimates, priority order |
| `version-bump-advisor` | "Should this be a major or minor bump?" | Semver recommendation with reasoning, breaking change analysis, changelog draft |
| `release-retrospective` | "Review how the last release went" | Plan vs reality comparison, what went well, what to improve, process recommendations |
| `governance-encoder` | "Encode our governance rules" | Machine-executable governance constraints (linting rules, CI checks, review policies) |
| `session-memory` | "Track findings across skill runs" | Persistent finding store with trend tracking, cross-skill correlation, progress monitoring |
| `codemod-generator` | "Generate a codemod for renaming color-primary" | jscodeshift migration script with dry-run support, before/after examples, edge case handling |

### Document (7 skills)

| Skill | What to say | What you get |
|-------|-------------|-------------|
| `ai-component-description` | "Write an AI description for Button" | Six-section structured description optimised for LLM consumption and Figma Dev Mode |
| `pattern-documentation` | "Document our form validation pattern" | Multi-component pattern doc with use cases, composition rules, anti-patterns |
| `token-documentation` | "Document our colour tokens" | Token reference docs with semantic intent, usage context, do/don't examples |
| `usage-guidelines` | "Write usage guidelines for Card" | Do's, don'ts, edge cases, anti-patterns, quick-reference card |
| `component-decision-tree` | "Help users choose between Dialog and Sheet" | Selection logic flowchart for choosing between similar components |
| `context-engine-builder` | "Build a context engine for our system" | Seven-blueprint context engine for AI agent integration |
| `metadata-schema-generator` | "Generate a JSON schema for our components" | JSON metadata schemas for tooling, CI, and AI agent consumption |

### Validate (6 skills)

| Skill | What to say | What you get |
|-------|-------------|-------------|
| `design-to-code-check` | "Does our Card match the Figma spec?" | Property-by-property comparison with discrepancy classification (error/gap/accepted) |
| `accessibility-per-component` | "Is our Accordion accessible?" | WCAG audit with keyboard, ARIA, focus, contrast, motion — code examples for every finding |
| `token-compliance` | "Are we using tokens correctly in our app?" | Hardcoded values, wrong-tier references, intentional overrides — per file, per component |
| `schema-validator` | "Validate our tokens against DTCG" | DTCG 2025.10 compliance check — type declarations, composite integrity, resolver coverage |
| `component-api-validator` | "Is our component API consistent?" | Cross-library API audit — prop naming, type patterns, default conventions |
| `cicd-integration` | "Set up CI checks for our design system" | GitHub Actions / GitLab CI config files for automated token, accessibility, and compliance checks |

### Communicate (6 skills)

| Skill | What to say | What you get |
|-------|-------------|-------------|
| `adoption-report` | "How widely is our system adopted?" | Coverage vs actual adoption, team-by-team breakdown, trend direction, risk flags |
| `stakeholder-brief` | "Write a brief for leadership" | One-page executive brief in business language with a clear ask |
| `system-pitch` | "Pitch the design system to leadership" | Investment case with cost quantification, ROI framing, competitive context |
| `designer-onboarding` | "Create an onboarding guide for new designers" | Getting-started guide covering tools, workflows, system conventions |
| `engineering-onboarding` | "Create an onboarding guide for new engineers" | Getting-started guide covering setup, component usage, contribution process |
| `visual-report` | "Create a dashboard of our system health" | Interactive HTML dashboard with charts, trend visualisations, and drill-down sections |

### Agents (4 chained workflows)

| Agent | What to say | What it chains |
|-------|-------------|----------------|
| `full-system-diagnostic` | "Run a full diagnostic" | token-audit → naming-audit → component-audit → drift-detection → system-health |
| `component-to-release` | "Run the release pipeline for Dialog" | design-to-code → accessibility → token-compliance → description → guidelines → comms |
| `governance-review` | "Run a quarterly governance review" | adoption-report → drift-detection → stakeholder-brief |
| `migration` | "Plan a migration to the new token format" | token-audit → naming-audit → migration plan → change-communication |

---

## Setting up Figma integration

Several skills become more powerful when Claude can read your Figma file directly. Without Figma integration, you describe your components or paste token values into the conversation manually. With it, skills pull that data automatically.

**This is entirely optional.** Every skill works without Figma. But if you use Figma as your design tool, connecting it saves significant time.

### Option A: Figma Console MCP from Southleft (recommended)

The [Figma Console MCP](https://github.com/southleft/figma-console-mcp) gives Claude both read and write access to Figma. Skills can write descriptions back into components, rename variables, create missing tokens, and capture live screenshots.

**Setup:**
1. Install the MCP server: [github.com/southleft/figma-console-mcp](https://github.com/southleft/figma-console-mcp)
2. Install the Desktop Bridge plugin in Figma Desktop (included in the repo)
3. Add the MCP server to your Claude Code or Cowork configuration
4. Open your design system file in Figma Desktop and make sure the Desktop Bridge plugin is running
5. Test: "Show me a summary of my design system in Figma"

### Option B: Standard Figma MCP (read-only)

The [standard Figma MCP](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) from Figma gives Claude read access. Skills can pull component data, variable collections, and design specs. Findings stay as reports — Claude can't write changes back.

**Setup:**
1. Follow [Figma's guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) to install the MCP server
2. Generate a Figma personal access token with read access to files and variables
3. Test: "List the variable collections in my Figma file"

### Which skills use Figma?

| Skill | What it reads | What it writes (Console MCP only) |
|-------|--------------|----------------------------------|
| `ai-component-description` | Component structure, variants, properties | Writes description into Figma |
| `figma-variable-audit` | Variable collections, modes, values | Renames variables, adds modes |
| `token-audit` | Variable values for cross-reference | Creates missing semantic variables |
| `component-audit` | Full inventory with detach rates | — |
| `design-to-code-check` | Design spec with rendered image | — |
| `drift-detection` | Design reference + screenshots | — |
| `token-compliance` | Token values for ground-truth | — |
| `system-health` | Component count and analytics | — |
| `adoption-report` | Library usage and insertion data | — |

### Figma file key in config

Add your file key to `.ds-ops-config.yml` so skills auto-pull without being asked:

```yaml
integrations:
  figma:
    enabled: true
    file_key: "abc123def456"  # The string after /design/ in your Figma URL
```

**How to find your file key:** Open your design system file in Figma. Look at the URL in your browser — it looks something like `figma.com/design/abc123def456/My-Design-System`. The `abc123def456` part (between `/design/` and `/My-Design-System`) is your file key. Copy it and paste it into the config above.

### Troubleshooting Figma

**"Claude doesn't see my file"** — Check: (1) MCP server running, (2) token/Bridge has access, (3) correct file key. Restart your Claude session after config changes.

**"Variables are empty"** — Your file may not have published variables, or the token may lack variable read permissions. These are separate from file permissions in Figma.

**"Wrong file"** — Specify the file key in `.ds-ops-config.yml` or include the Figma URL in your prompt.

---

## Optional configuration

**You do not need to configure anything.** Every skill works out of the box with sensible defaults.

If you want to customise how the skills behave — for example, making certain types of violations more severe, connecting to Figma or GitHub, or enabling recurring trend tracking — create a file called `.ds-ops-config.yml` in your project root (the same folder as your `package.json`).

A fully annotated template with explanations for every setting is included at `.ds-ops-config.yml` in the repo root. Copy it into your project root, read the comments, and uncomment the settings you want.

For a detailed walkthrough of every configuration option, see `3-SETUP-AND-CONFIG.md`.

---

## Updating to a new version

**In Cowork:** Download the latest `.plugin` file from the repo and drop it into the chat. It replaces the old version automatically. Your `.ds-ops-config.yml` is not affected.

**In Claude Code:** Pull the latest changes:
```bash
cd ~/.claude/skills/design-system-ops && git pull
```
Your project-level config is not inside the skill pack, so it's never overwritten.

---

## What's in the repo

| Path | What it's for |
|------|--------------|
| `skills/` | 37 skill files organised by name, each with a `SKILL.md` and `references/` |
| `commands/` | 13 command definitions for agent workflows and shortcuts |
| `knowledge-notes/` | 10 canonical reference documents that power the skills |
| `sample-outputs/` | Real skill outputs showing expected depth and format |
| `.ds-ops-config.yml` | Annotated configuration template |
| `installable/` | Pre-packaged `.plugin` (Cowork) and `.zip` for quick installation |
| `1-INSTALL.md` | This file |
| `2-WHATS-INCLUDED.md` | Full product documentation — skills, agents, knowledge notes |
| `3-SETUP-AND-CONFIG.md` | Deep-dive setup guide with framework compatibility, monorepo handling, troubleshooting |
| `CONTRIBUTING.md` | How to contribute |
| `LICENSE` | MIT license |

---

If you found this useful, [buy me a coffee](https://buymeacoffee.com/murphytrueman).
