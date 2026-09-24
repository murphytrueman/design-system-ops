# Design System Ops

**A Claude Code skill pack for the designers who build the systems everyone else uses.**

Murphy Trueman · 2026 · [designsystemops.com](https://designsystemops.com)

---

## What is this?

Design System Ops is a toolkit that gives Claude (the AI) deep expertise in design systems work. It turns Claude into a design systems specialist that can audit your tokens, write component documentation, assess system health, plan deprecations, produce stakeholder briefs, encode governance rules, build context engines for AI agents, and much more — all grounded in 14 years of production design systems experience.

Instead of starting from scratch every time you ask Claude for help with your design system, these skills give it the frameworks, mental models, and structured processes that a staff-level design systems practitioner would use.

**What is in the pack:** 36 skills (individual tools that each do one thing well), 4 agents (chained workflows that run multiple skills in sequence), 13 knowledge notes (expert frameworks that power the skills), 13 sample outputs (anonymised examples and unedited fixture runs, so you know what to expect), and an optional configuration file.

---

## Who is this for?

Design systems practitioners — the people who build, govern, and scale the system, not just the people who use it. That includes design systems leads, senior design engineers, and anyone responsible for a shared component library, token architecture, or design-to-code pipeline.

You do not need to be technical to use this. If you can type a prompt, you can use every skill in this pack.

---

## How it works — the key concepts

If you are new to Claude Code, Cowork, or skill packs, here is what you need to know.

### What is Claude Code?

Claude Code is a command-line tool made by Anthropic that lets you work with Claude directly from your terminal (or through an IDE like VS Code or Cursor). It can read your files, write code, run commands, and use specialised tools — all through conversation.

Think of it as Claude with access to your computer. You talk to it, and it can look at your files and do real work.

### What is Cowork?

Cowork is a desktop feature of the Claude app that lets you work with Claude without needing a terminal. You can drag and drop files, install plugins, and have Claude work on tasks for you — all through a chat interface. If you are not comfortable with the command line, Cowork is the easiest way to use Design System Ops.

### What are skills?

Skills are instruction files that teach Claude how to do something specific. A skill is a markdown file that contains a structured process — steps to follow, quality checks, examples of good output, and expert knowledge baked in.

When you ask Claude to do something that matches a skill, Claude reads the skill file and follows its process. The result is output that is dramatically more thorough, specific, and production-ready than what you would get from a generic prompt.

**In this pack, there are 36 skills** organised into five categories: Audit, Govern, Document, Validate, and Communicate.

### What are agents?

Agents are skills that chain multiple other skills together into a single workflow. Instead of running several skills one at a time, an agent runs them in sequence and synthesises the results.

**In this pack, there are 4 agents** that chain skills into end-to-end workflows like a full system diagnostic or a pre-release validation pipeline.

### What are knowledge notes?

Knowledge notes are reference documents that contain expert frameworks and mental models. They are not skills you run directly — they are the background knowledge that makes the skills smart.

For example, the `ai-readiness` knowledge note contains the six dimensions of component AI readiness, the context cascade model, and the three pillars framework. When you run the `ai-component-description` skill, Claude reads that knowledge note first, which is why its output is informed by these frameworks rather than being generic advice.

**In this pack, there are 13 knowledge notes** covering token architecture, component governance, AI readiness, design-to-code contracts, the Component Bestiary challenge rating system, agent orchestration patterns, MCP setup guidance, public design systems as dated reference points, adoption measurement principles, documentation coverage (the source-of-truth model behind the docs-coverage audit), executive communication (audience calibration and honest numbers for leadership-facing documents), configuration and recurring runs (how skills read your config, use integrations, and compare against previous runs), and output discipline (the shared quality standards that keep all audit and assessment output consistent, specific, and honest).

You never need to interact with knowledge notes directly. They load automatically when a skill needs them.

---

## How to install

There are two ways to install Design System Ops, depending on whether you use Cowork (the desktop app) or Claude Code (the terminal).

### Option A: Install in Cowork (easiest — no terminal needed)

1. Download `design-system-ops.plugin` from the [`installable/`](installable/) folder in this repo
2. Open the Claude desktop app and start a Cowork session
3. Drop the `.plugin` file into the chat window
4. Follow the install prompt — done

That is it. The skills are now available in every Cowork session.

### Option B: Install in Claude Code (terminal)

1. Clone the repo directly into your Claude Code skills directory:

```bash
git clone https://github.com/murphytrueman/design-system-ops.git ~/.claude/skills/design-system-ops
```

That path means: your home folder, then the `.claude` folder (it starts with a dot so it may be hidden), then `skills`, then clone `design-system-ops` here.

2. If you want the skills available only for a specific project instead of everywhere:

```bash
git clone https://github.com/murphytrueman/design-system-ops.git your-project/.claude/skills/design-system-ops
```

3. Verify it works by typing a prompt like: "Run system-health on my design system."

### Verifying the install

After installing, try one of these prompts:

- "How healthy is my design system?"
- "Audit my tokens"
- "Write an AI component description for my Button"

If Claude responds with a structured, detailed process (not a generic answer), the skills are loaded and working.

---

## How to update

When a new version of Design System Ops is released:

### Updating in Cowork

1. Download the latest `design-system-ops.plugin` from the [`installable/`](installable/) folder in this repo
2. Open a Cowork session
3. Drag and drop the new `.plugin` file into the chat
4. Follow the install prompt — it will replace the old version automatically

### Updating in Claude Code

1. Pull the latest changes:
   ```bash
   cd ~/.claude/skills/design-system-ops && git pull
   ```
2. That is it — Claude Code loads skills fresh each session

No settings or configuration are lost when you update. Your `.ds-ops-config.yml` file (if you have one) lives in your project root, not inside the skill pack, so it is never overwritten.

---

## Where to use each skill

Design System Ops skills work in different contexts. Some are best used when Claude has access to your code. Others work best when connected to your design tool. Many work with just a conversation.

### Best when connected to your codebase

These skills read your actual source files — token definitions, component code, stylesheets — to produce specific, accurate output.

| Skill | What it reads |
|-------|--------------|
| `token-audit` | Token files (JSON, SCSS, CSS vars, TypeScript, Tailwind config) |
| `token-compliance` | Application code (finds hardcoded values, wrong-tier references) |
| `component-audit` | Component source directory, barrel files, imports |
| `component-api-validator` | Component prop types, TypeScript interfaces |
| `schema-validator` | Token JSON files (validates against DTCG 2025.10) |
| `drift-detection` | Both system code and consuming product code |
| `design-to-code-check` | Component source files (compares against design spec) |
| `accessibility-per-component` | Component source for ARIA, keyboard, focus implementation |
| `codebase-index` | Full component directory (builds a machine-readable map) |
| `naming-audit` | Component and token file names and exports |
| `governance-encoder` | Governance policies (encodes as machine-checkable rules) |
| `metadata-schema-generator` | Component props and constraints (generates JSON schemas) |
| `cicd-integration` | Existing CI config, component and token source directories |
| `codemod-generator` | Component source, import patterns, prop usage |

**How to give Claude access:** Point it at file paths in your prompt, or open Claude Code in your project directory so it can read files directly.

### Best when connected to Figma

These skills work with your Figma design system library through the Figma MCP server.

| Skill | What it reads from Figma |
|-------|--------------------------|
| `ai-component-description` | Component structure, variants, properties |
| `figma-variable-audit` | Variable collections, alias chains, mode coverage |
| `design-to-code-check` | Design specifications for comparison against code |
| `component-audit` | Component inventory, detach rates |

**How to connect Figma:** Install and configure the Figma MCP server (see the Integrations section below). Once connected, these skills auto-pull data from your Figma file.

### Work with just a conversation (no files needed)

These skills work from your description of the situation. You do not need to provide any files.

| Skill | What you provide in the prompt |
|-------|-------------------------------|
| `system-health` | Describe your system and concerns; it infers the maturity stage from evidence rather than asking, and labels a conversation-only run as reported |
| `stakeholder-brief` | Share health findings or describe the situation |
| `system-pitch` | Describe the current state and what you need |
| `adoption-report` | Share measured usage data (imports per repo, library analytics, survey results); without any measured signal it returns a data-collection plan, not a report |
| `onboarding` | Describe the role, the team and the contacts; the rest comes from the repo and Figma |
| `decision-record` | Describe the decision that was made and why |
| `change-communication` | Describe the change being released |
| `deprecation-process` | Describe what is being deprecated and why |
| `contribution-workflow` | Describe your current process or desired process |
| `backlog-generator` | Share audit findings to convert into work items |
| `version-bump-advisor` | Describe the changes in the release |
| `release-retrospective` | Describe what was planned vs what happened |
| `pattern-documentation` | Describe the pattern and its components |
| `token-documentation` | Describe or share token values and intent |
| `usage-guidelines` | Describe the component and how it should be used |
| `component-decision-tree` | Describe competing components and selection criteria |
| `visual-report` | Share audit findings or health statuses to visualise |

---

## Supported design tools

### Figma (full integration)

Design System Ops has deep Figma integration through the Figma MCP server. When connected, skills can read your Figma components, variables, styles, and library analytics directly.

**What works with Figma:**
- `ai-component-description` reads component structure and writes descriptions you paste back into Figma
- `figma-variable-audit` audits your variable collections against token architecture best practices
- `design-to-code-check` compares your Figma specs against code implementation
- `component-audit` pulls your component inventory and detach rates

**How to set up:** See the Figma MCP integration section below.

### Penpot

Penpot does not currently have an MCP server, so there is no direct integration. However, you can still use every skill in the pack by providing your design data manually:

- Export your token values from Penpot and share them in the prompt
- Describe your component structure and variants
- Share screenshots or exported specifications for design-to-code checks

**What works well with Penpot:**
- All audit skills (token-audit, component-audit, naming-audit) — provide your source files
- All documentation skills — describe your components and patterns
- All governance skills — these work from conversation, not design tool data
- All communication skills — these work from conversation

As Penpot develops its API and plugin ecosystem, direct integration may become possible in future versions.

### Paper (WeTransfer)

Paper is a prototyping and presentation tool, not a component library tool, so it does not have the same integration surface as Figma. However:

- If you define tokens or design decisions in Paper, export them and share with Claude
- Use documentation skills to write guidelines based on your Paper designs
- Use governance skills to plan processes that span Paper and code

### Other design tools (Sketch, Adobe XD, InVision)

The same approach applies: export your design data and share it with Claude. All skills work with manually provided information. The Figma MCP integration simply automates what you would otherwise provide by hand.

---

## Supported tool connections

Design System Ops can connect to several tools to pull data automatically instead of requiring manual input. All connections are optional — every skill works without them.

### Why connect tools?

When a tool is connected, skills pull data automatically. Without connections, you provide the same data by pasting it into the conversation or pointing to files. Connections save time but are never required.

| Connection | What it does | Why it helps | Setup effort |
|------------|-------------|-------------|-------------|
| **Figma MCP** | Reads your Figma components, variables, and styles directly | Skills auto-pull design specs, component data, and variables without screenshots or manual export | Medium |
| **GitHub API** | Searches your code for violations, reads component source, tracks PRs | Token compliance scans your whole repo automatically instead of file-by-file | Low |
| **npm registry** | Pulls download statistics for your packages | Adoption reports get real usage data instead of estimates | None (public) |
| **Style Dictionary or Terrazzo** | Builds and validates the token files with the tool you already use | Token skills run it first and reason over resolved aliases and its own errors | Low |
| **Storybook** | Reads component prop metadata and story inventory | Component audits get accurate documentation coverage data | Low |
| **Chromatic** | Pulls visual regression data | Drift detection sees visual diffs, not just code diffs | Low |
| **Documentation platforms** | Cross-references docs coverage (Zeroheight, Supernova, Storybook docs) | System health reports include documentation completeness | Low |

**How to configure connections:** Create a `.ds-ops-config.yml` file in your project root. A fully annotated template is included in the repo root at `ds-ops-config.example.yml` — copy it across and rename it. See the detailed setup guide in `3-SETUP-AND-CONFIG.md`.

---

## The 36 skills — what each one does

### Audit skills (9) — assess where you are

These skills look at what you have and tell you what is working, what is broken, and what to fix first.

---

#### `token-audit`

**What it does:** Examines your design token files and checks for structural problems — tokens referencing the wrong tier, naming inconsistencies, orphaned tokens nobody uses, and alignment with the DTCG 2025.10 specification.

**When to use it:** When you want to understand the health of your token architecture, before a token migration, or as part of a quarterly review.

**Example prompts:**
- "Audit our token architecture. We use Style Dictionary with primitives, semantic tokens, and component tokens."
- "Check our tokens for naming inconsistencies and tier leakage."
- "Are our token files DTCG compliant?"

**Best used with:** Your codebase (reads token files directly)

---

#### `component-audit`

**What it does:** Inventories your component library and assesses each component across multiple dimensions — usage, complexity (using the Challenge Rating system), duplication, AI readiness, and coverage gaps.

**When to use it:** When you inherit a design system and need to understand what you have. When planning the next quarter's work. When making the case for consolidation.

**Example prompts:**
- "Audit our component library. What do we have, what is used, what is duplicated?"
- "We have about 40 components. Give me a full health assessment of the library."
- "Which of our components are AI-ready and which need work?"

**Best used with:** Your codebase (reads component source), optionally Figma and Storybook

---

#### `system-health`

**What it does:** Assesses your design system's health across seven dimensions — tokens, components, documentation, adoption, governance, AI readiness, and platform maturity — rating each as Strong, Functional, Weak, or Absent.

**When to use it:** As your first skill run to understand the big picture. Quarterly to track progress. Before stakeholder conversations.

**Example prompts:**
- "How healthy is my design system? Give me the full picture."
- "Rate my system. We have 15 components, 200 tokens, used by 4 teams."
- "Run a system health check so I can brief leadership."

**Best used with:** Conversation (describe your system), optionally your codebase and Figma

---

#### `drift-detection`

**What it does:** Finds places where teams have diverged from the design system — hardcoded values, local reimplementations, token overrides, and version lag. Classifies each instance by type so you know what to fix vs what to discuss.

**When to use it:** When you suspect teams are working around the system. Before a major version release. As part of a governance review.

**Example prompts:**
- "Where have teams diverged from the system? Check for hardcoded values and local reimplementations."
- "Find all drift in our checkout codebase against the design system."
- "Which teams are going off-system and why?"

**Best used with:** Your codebase (scans consuming code), optionally Figma and Chromatic

---

#### `naming-audit`

**What it does:** Reviews naming conventions across your components and documented patterns. Identifies inconsistencies, evaluates whether names communicate intent, and provides rename suggestions with evidence and sequencing. Token names are `token-audit`'s job and prop names `component-api-validator`'s; this skill cites their findings.

**When to use it:** When naming has grown organically and you need to clean it up. Before publishing a system externally.

**Example prompts:**
- "Review our naming conventions. Component names are all over the place."
- "Are our token names consistent with our component names?"
- "Audit our naming and suggest a migration plan to fix inconsistencies."

**Best used with:** Your codebase (reads file and export names)

---

#### `figma-variable-audit`

**What it does:** Audits Figma variable collections against the three-tier token architecture — naming conventions, alias chains, mode coverage, orphaned variables, and DTCG export readiness.

**When to use it:** When your token architecture is defined in Figma and you want to verify it is properly structured. When preparing to export tokens to code.

**Example prompts:**
- "Audit our Figma variables. Check naming, alias chains, and mode coverage."
- "Are our Figma variable collections ready to export to code?"
- "Find orphaned variables in our Figma design system file."

**Best used with:** Figma MCP (reads variables directly)

---

#### `codebase-index`

**What it does:** Generates a pre-computed, machine-readable index of your design system's codebase — a component inventory, a relationship graph, and summary statistics. The index lives in `.ai/index/` and lets AI agents navigate your system without exploring from scratch every time.

**When to use it:** After adding or removing components. When setting up AI tooling to work with your system. When you want a queryable map of what exists and how things relate.

**Example prompts:**
- "Index my codebase. Build a component map with relationships."
- "Create a dependency graph of my design system components."
- "What depends on what in my component library?"

**Best used with:** Your codebase (scans component directories and imports)

---

#### `theme-audit`

**What it does:** Audits how themes are implemented across a design system — token coverage per theme, component-tier propagation, cross-theme visual consistency, and DTCG resolver validation.

**When to use it:** When your system has dark mode, brand themes, or multi-mode token architectures that need to verify complete and consistent theme implementation.

**Example prompts:**
- "Audit our theme implementation. We have light and dark modes with component-level overrides."
- "Check our themes for propagation gaps and consistency violations."
- "Are all our tokens properly themed across all modes?"

**Best used with:** Your codebase (reads token files and component source), Figma (reads token definitions and applied values)

---

#### `docs-coverage`

**What it does:** Audits whether your documentation surface keeps pace with your components. Measures the code (the source of truth for what exists) against Storybook and any documentation platform, reporting coverage gaps (components with no docs), staleness (docs that predate the component's last code change, computed from git), and orphaned docs. Every coverage finding carries a confidence tier so a fuzzy name match is never presented as fact.

**When to use it:** When you suspect the docs have fallen behind the code. After a release, to check what shipped undocumented. As a recurring health check on the documentation surface. It works with zero integration — a components directory, a Storybook build, and git history are enough; Zeroheight, Supernova, and custom docs sites are optional layers.

**Example prompts:**
- "Which components are undocumented?"
- "Audit our docs coverage — are our Storybook docs keeping pace with the components?"
- "Check for stale documentation against our last few releases."

**Best used with:** Your codebase and a Storybook build (`storybook-static/`); optionally a configured documentation platform

---

### Govern skills (9) — run the system as infrastructure

These skills help you set up and operate the processes that keep a design system healthy over time.

---

#### `contribution-workflow`

**What it does:** Produces a complete contribution process — from proposal through design, build, documentation, review, and release — calibrated by contribution type.

**When to use it:** When you need to formalise how new components and changes get into the system.

**Example prompts:**
- "Document our contribution workflow. How should new components get proposed and built?"
- "Create a contribution guide for external teams wanting to add components."
- "What should the process be for contributing a bug fix vs a new component?"

**Best used with:** Conversation (describe your team and current process)

---

#### `deprecation-process`

**What it does:** Produces a complete deprecation plan — blast radius analysis, migration path, timeline, codemod recommendations, communication plan, and rollback contingency.

**When to use it:** When retiring a component version. When consolidating duplicates. When making a breaking change.

**Example prompts:**
- "Plan the deprecation of our old Card v1. The new Card v2 is ready."
- "How do we sunset our legacy button component safely?"
- "Create a deprecation plan for our old token format."

**Best used with:** Your codebase (for blast radius analysis), conversation otherwise

---

#### `decision-record`

**What it does:** Produces an Architecture Decision Record (ADR) — a structured document capturing why a decision was made, options considered, trade-offs accepted, and when to revisit.

**When to use it:** After any significant decision about your design system.

**Example prompts:**
- "Record why we chose DTCG format for our tokens."
- "Document the decision to use React over Web Components."
- "Create a decision record for our new component naming convention."

**Best used with:** Conversation (describe the decision and reasoning)

---

#### `change-communication`

**What it does:** Produces a communication package calibrated to the change size — from patch notes to full migration guides with team notifications.

**When to use it:** Every time you release something.

**Example prompts:**
- "We are renaming the variant prop to appearance across all components. Create the communications."
- "Write release notes for our v3.2.0 release."
- "Communicate this breaking change to consuming teams."

**Best used with:** Conversation (describe the change)

---

#### `backlog-generator`

**What it does:** Transforms audit findings into sprint-ready work items with effort estimates, acceptance criteria, and stakeholder-friendly rationale.

**When to use it:** After running an audit skill, when you need to turn findings into a prioritised backlog.

**Example prompts:**
- "Create a backlog from our token audit findings. T-shirt size everything."
- "Turn these component audit results into sprint tickets."
- "Generate work items from the system health report."

**Best used with:** Output from an audit skill (paste or reference the findings)

---

#### `version-bump-advisor`

**What it does:** Classifies changes as breaking, minor, or patch with reasoning, flags edge cases, and generates a changelog entry.

**When to use it:** Before tagging a release.

**Example prompts:**
- "We renamed a prop and added new features. What version bump?"
- "Is this a breaking change? We changed the default value of the size prop."
- "Generate a changelog entry for this release."

**Best used with:** Conversation (describe the changes)

---

#### `release-retrospective`

**What it does:** Structured post-release review comparing plan vs reality, classifying gaps, and recommending improvements.

**When to use it:** After any significant release.

**Example prompts:**
- "Review our last major release. What went well and what should we improve?"
- "Run a retro on the token migration we just completed."
- "How did the deprecation of Dialog v1 go compared to the plan?"

**Best used with:** Conversation (describe what was planned vs what happened)

---

#### `governance-encoder`

**What it does:** Turns the governance rules your team has written down into enforcement that runs: ESLint, Stylelint, dependency-cruiser and CODEOWNERS configuration, each rule traced to the document it came from, plus a `GOVERNANCE.md` for rules with no executable form (design review, decision records) that says who checks them and when. Runs the linters in report mode to show how many violations each rule finds today.

**When to use it:** When rules live in a wiki and are enforced by whoever notices. When you want coding agents and CI to follow the same rules reviewers do. Before adding a rule to CI, to see what it would catch.

**Example prompts:**
- "Encode our governance rules as lint config."
- "Turn CONTRIBUTING.md into something CI can enforce."
- "Which of our written rules could a linter check?"

**Best used with:** Your codebase (reads CONTRIBUTING, existing lint config, token names) and `cicd-integration` to run the result in CI

---

#### `codemod-generator`

**What it does:** Generates jscodeshift migration scripts for token renames, prop changes, import path updates, and component replacements. Produces the transform, test cases, a migration runner, and documentation — everything needed for automated migration.

**When to use it:** When a decision requires changes across consuming codebases. After a deprecation decision. When renaming tokens or props at scale.

**Example prompts:**
- "Generate a codemod to rename our color tokens from camelCase to kebab-case."
- "Create a migration script to replace OldButton imports with Button."
- "Write a codemod for the variant→appearance prop rename across all components."

**Best used with:** Your codebase (reads current usage patterns for accurate transforms)

---

### Document skills (7) — make the system legible

These skills produce documentation that makes your system usable by other teams and by AI tools.

**For coding agents.** `agent-instructions` writes the `AGENTS.md` that agents read first and links everything else: the inventory and dependency graph from `codebase-index` (in audit), the per-component metadata from `metadata-schema-generator`, the choosing-between pages from `component-decision-tree`, and the lint configuration `governance-encoder` (in govern) writes so agents can check their own work. Start with `agent-instructions`; add the others as the system grows.

---

#### `ai-component-description`

**What it does:** Generates a structured component description optimised for AI tools to read via Figma's MCP server. Six sections: Purpose, Props, Anti-patterns, Composition, Accessibility, and Examples.

**Why this matters:** Most component descriptions are written for humans. This skill produces descriptions that let AI tools select the right component, configure it correctly, and avoid mistakes — without needing a human to supervise.

**When to use it:** For every component in your system. Start with the 5–10 most-used components.

**Example prompts:**
- "Write an AI-optimised description for our Dialog component."
- "Generate a Figma MCP description for the Button component."
- "Create a six-section description for our Card that Claude can understand."

**Best used with:** Your codebase or Figma (reads component structure), conversation otherwise

---

#### `pattern-documentation`

**What it does:** Writes documentation for design system patterns — recurring solutions composed from multiple components (form validation, empty states, confirmation dialogs).

**When to use it:** When you need to document how components work together, not just individually.

**Example prompts:**
- "Document the form validation pattern — inline and summary validation."
- "Write pattern docs for our empty state pattern."
- "Document the confirmation dialog pattern with all its states."

**Best used with:** Conversation (describe the pattern and its components)

---

#### `token-documentation`

**What it does:** Writes documentation for design tokens that covers semantic intent, usage context, usage constraints, and component associations — not just names and hex values.

**When to use it:** When your token documentation is just a list of names and values.

**Example prompts:**
- "Document our semantic colour tokens. Explain intent, not just hex values."
- "Write token docs that help designers pick tokens by purpose, not colour."
- "Create a token reference with do's and don'ts for each tier."

**Best used with:** Your codebase (reads token files), conversation otherwise

---

#### `usage-guidelines`

**What it does:** Writes component usage guidelines — when to use, when not to, edge cases, anti-patterns, accessibility, and content guidelines.

**When to use it:** When your component documentation describes what it is but not how to use it correctly.

**Example prompts:**
- "Write usage guidelines for our Select component."
- "Create do's and don'ts for the Modal component."
- "When should someone use Tabs vs Accordion?"

**Best used with:** Your codebase or Figma (reads component details), conversation otherwise

---

#### `component-decision-tree`

**What it does:** Builds queryable decision trees that help agents and teams choose between similar components — structured YAML files mapping user intents to the correct component through narrowing questions.

**When to use it:** When teams keep choosing the wrong component because options are confusing (Modal vs Dialog vs Drawer, Select vs Combobox vs Autocomplete).

**Example prompts:**
- "Build a decision tree for choosing between our overlay components."
- "Create a selection guide: when to use Select vs Combobox vs Autocomplete."
- "Help me create an intent-to-component mapping for our form components."

**Best used with:** Conversation (describe the competing components)

---

#### `agent-instructions`

**What it does:** Writes the `AGENTS.md` coding agents read first: where components, tokens and docs live, the rules with a source for each, how to check work (the lint and test commands that exist), and what not to do. Links to `.ai/index/`, `.ai/metadata/`, the choosing-between pages and the token docs rather than copying them. Adds `CLAUDE.md`, Cursor or Copilot pointer files on request, each a one-liner that says "read AGENTS.md".

**When to use it:** When Claude, Cursor or Copilot keep picking the wrong component or typing raw values. When you have `.ai/` files nothing reads. When onboarding an agent the way you'd onboard an engineer.

**Example prompts:**
- "Write an AGENTS.md for our design system."
- "Make our system navigable for coding agents."
- "Add Cursor rules that point at our design system conventions."

**Best used with:** Your codebase; richer after `codebase-index` and `metadata-schema-generator` have run

---

#### `metadata-schema-generator`

**What it does:** Generates structured JSON metadata schemas for components — machine-readable constraint definitions that encode props, behavioural rules, composition constraints, and accessibility contracts as programmatic data for tooling.

**When to use it:** When you need JSON schemas that MCP servers, linters, code generators, or test frameworks can consume programmatically.

**Example prompts:**
- "Generate a JSON metadata schema for our Button component."
- "Create machine-readable component constraints for our MCP server."
- "Build structured metadata that our code generator can use."

**Best used with:** Your codebase (reads component prop types and interfaces)

---

### Validate skills (6) — verify quality before shipping

These skills check specific quality dimensions before a component or update goes out.

---

#### `design-to-code-check`

**What it does:** Compares the design specification against the code implementation and identifies discrepancies — implementation errors, specification gaps, and accepted divergences.

**When to use it:** Before releasing a component update. When design and engineering disagree about "done."

**Example prompts:**
- "Compare our Tabs implementation against the Figma spec."
- "What is different between the design and the build for our Card?"
- "Check if our Button matches the Figma spec."

**Best used with:** Your codebase and Figma MCP (reads both sides of the comparison)

---

#### `accessibility-per-component`

**What it does:** Audits a single component across five accessibility dimensions: keyboard navigation, screen reader support, colour contrast, focus management, and ARIA implementation.

**When to use it:** Before releasing any interactive component.

**Example prompts:**
- "Run an accessibility audit on our Combobox."
- "Is our Dialog keyboard accessible?"
- "Check WCAG compliance on the Tabs component."

**Best used with:** Your codebase (reads component implementation)

---

#### `token-compliance`

**What it does:** Scans a codebase for token compliance violations — hardcoded hex values, primitive token references that should be semantic, and inconsistent application.

**When to use it:** Before a release. When onboarding a new product team. When you suspect hardcoded values.

**Example prompts:**
- "Find all hardcoded hex values in our checkout codebase."
- "Check our app for token compliance violations."
- "Which files have magic numbers instead of spacing tokens?"

**Best used with:** Your codebase (scans source files for violations)

---

#### `schema-validator`

**What it does:** Validates token files against DTCG 2025.10, Style Dictionary, or custom schemas. Catches structural issues before they break build pipelines.

**When to use it:** Before committing token files. As part of pre-release validation.

**Example prompts:**
- "Validate our token files against DTCG 2025.10."
- "Are our token JSON files structurally valid?"
- "Check our Style Dictionary config for schema errors."

**Best used with:** Your codebase (reads token files)

---

#### `component-api-validator`

**What it does:** Audits the public API surface of a component library for consistency, type coverage, and contract alignment across all components.

**When to use it:** When your library has grown and prop patterns have become inconsistent.

**Example prompts:**
- "Audit our component library's API for consistency."
- "Are our prop names consistent across components?"
- "Find where our boolean conventions vary across the library."

**Best used with:** Your codebase (reads component TypeScript interfaces)

---

#### `cicd-integration`

**What it does:** Generates CI/CD pipeline configurations that automate design system quality checks — token validation, naming conventions, documentation coverage, accessibility baseline, and more. Supports GitHub Actions, GitLab CI, CircleCI, and Bitbucket Pipelines.

**When to use it:** When you want to automate quality checks that the audit and validate skills currently run manually. When setting up a new CI pipeline for your design system.

**Example prompts:**
- "Generate a GitHub Actions workflow that validates our tokens and checks for hardcoded values."
- "Set up CI checks for our design system — token naming, docs coverage, and accessibility."
- "What design system checks should we automate in our pipeline?"

**Best used with:** Your codebase (reads existing CI config and source structure)

---

### Communicate skills (5) — move people and decisions

These skills produce documents for different audiences — leadership, engineers, designers, and new team members.

---

#### `adoption-report`

**What it does:** Produces an adoption report separating coverage (who can access the system) from adoption (who actually uses it), with trend direction, at-risk teams, and blocker analysis.

**When to use it:** Quarterly or monthly. Before stakeholder meetings.

**Example prompts:**
- "Create an adoption report for Q1."
- "Which teams are using the system and which are not?"
- "Where is coverage high but adoption low?"

**Best used with:** Usage data (npm downloads, Figma analytics), conversation otherwise

---

#### `stakeholder-brief`

**What it does:** Produces a one-page brief in business language — the situation, why it matters, what you recommend, what you need, and the expected outcome.

**When to use it:** When communicating up. When you need budget or prioritisation support.

**Example prompts:**
- "Write a brief for our VP about our system health findings."
- "Our system health shows two weak dimensions. Make the case for investment without jargon."
- "Summarise our quarterly progress for leadership."

**Best used with:** Health findings or audit results, conversation otherwise

---

#### `system-pitch`

**What it does:** Produces an investment pitch — leading with the cost of the current state before proposing the solution. Frames the system as infrastructure.

**When to use it:** When your org does not yet have a design system. When justifying continued investment.

**Example prompts:**
- "Pitch a design system to leadership. Every team builds their own components."
- "Make the business case for continuing to invest in our system."
- "How do I justify the cost of a design system to executives?"

**Best used with:** Conversation (describe the current situation)

---

#### `onboarding`

**What it does:** Writes an onboarding guide for a designer, an engineer, or both, grounded in the repository and the Figma library: real package name and import paths, real token names, the library's pages and modes, the team's contacts and contribution route. Anything the files and the team don't confirm is marked `[confirm: …]` and listed at the top. Updates an existing guide in place rather than starting over.

**When to use it:** When someone joins next week. When the existing guide was written from a template and nobody trusts it. When drift keeps starting in week one.

**Example prompts:**
- "Write a getting-started guide for a frontend engineer joining next week."
- "Onboard a new product designer to our design system."
- "Update our onboarding doc; it's out of date."

**Best used with:** Your codebase and Figma (for facts), conversation for contacts and policies

---

#### `visual-report`

**What it does:** Generates interactive HTML dashboards, charts, and trend visualisations from audit findings. Eight visual types: health radar, severity distribution, trend line, coverage heatmap, dependency graph, comparison bar, action priority matrix, and full dashboard.

**When to use it:** When you need a visual summary for a stakeholder meeting. When you want to see audit results as charts instead of tables. When tracking trends over time.

**Example prompts:**
- "Create a dashboard from our latest system health and token audit results."
- "Visualise the trend in our token compliance findings over the last four quarters."
- "Generate a health radar chart from our system health assessment."

**Best used with:** Output from audit or health skills (transforms findings into visuals)

---

## The 4 agents — chained workflows

Agents chain multiple skills together and synthesise the combined results. All agent outputs are proposals — they produce analysis and documentation, not changes. You review and approve before anything is acted on.

### `full-system-diagnostic`

**What it chains:** token-audit, naming-audit, component-audit, drift-detection, docs-coverage, system-health — plus theme-audit (if the system supports theming) and figma-variable-audit (if Figma is configured)

**When to use it:** Quarterly reviews. When you inherit a system. Before a major version.

**Example prompt:** "Run a full system diagnostic. Token files are in `src/tokens/`, components in `src/components/`. We have 30 components used by 6 teams."

**What makes it special:** It connects findings across skills — if the token audit finds tier leakage and drift detection finds the same tokens hardcoded in product code, the agent connects them into a single root cause.

---

### `component-to-release`

**What it chains:** design-to-code-check, accessibility-per-component, token-compliance, ai-component-description, usage-guidelines, change-communication

**When to use it:** Before releasing any component — new or updated. It is the pre-flight checklist.

**Example prompt:** "Run the release pipeline for our new Tabs component. Source is at `src/components/Tabs/`. Figma spec is in the main library file."

**What makes it special:** Context carries forward. If the accessibility audit finds keyboard issues, the usage guidelines will include that as an anti-pattern. The change communication reflects everything found upstream.

---

### `governance-review`

**What it chains:** adoption-report, drift-detection, stakeholder-brief

**When to use it:** Monthly or quarterly governance reviews.

**Example prompt:** "Run the governance review for Q1. I need adoption data, drift analysis, and a stakeholder brief for the leadership meeting."

**What makes it special:** The stakeholder brief is informed by adoption data and drift findings — it connects declining adoption to specific drift patterns with evidence.

---

### `token-migration`

**What it chains:** token-audit, a transformation table, codemod-generator, deprecation-process, change-communication. New names ship with the old ones aliased and deprecated in one minor; consumers migrate; removal waits for the next major.

**When to use it:** When executing an end-to-end token migration.

**Example prompt:** "We need to migrate from our custom token format to DTCG. Run the full migration workflow."

**What makes it special:** The migration plan classifies migration type, produces a transformation table, generates codemod recommendations, and phases the rollout. The communication package addresses engineer concerns specific to the transformation.

---

## The 13 knowledge notes — what powers the skills

You do not need to read these to use the skills. They load automatically.

| Note | What it provides | Used by |
|---|---|---|
| `documentation-coverage` | Source-of-truth model, the three rungs of "documented", join-key reliability hierarchy, git-based staleness, per-platform signal matrix | Docs coverage, system health |
| `token-architecture` | Three-tier token model, naming conventions, reference rules, DTCG 2025.10 specification | Token audit, token docs, token compliance, drift detection, schema validator, figma variable audit |
| `component-governance` | Contribution criteria, deprecation triggers, lifecycle stages, maturity model (five stages: Ad-hoc, Managed, Systematic, Measured, Optimised) | Contribution workflow, deprecation process, decision record, component audit, system health, and more |
| `ai-readiness` | Six dimensions of AI readiness, context cascade, three pillars framework | AI component description, pattern docs, usage guidelines, system health, codebase index, and more |
| `design-to-code-contract` | Design, build, documentation, release, and API contracts | Design-to-code check, contribution workflow, drift detection, system health, and more |
| `component-bestiary-reference` | Challenge Rating system for documentation depth calibration | Pattern docs, usage guidelines, AI component description, component audit |
| `agent-orchestration-guide` | The chained-run rules the four agents follow: one inventory, hand-off cards, one report | All four agents |
| `mcp-setup-guide` | What Figma MCP servers can and can't read, what the pack writes for agents, and graceful fallback when Figma isn't connected | AI component description |
| `public-systems-reference` | Named public design systems (Carbon, GOV.UK, USWDS, Primer, Paste, Atlassian, Material, Spectrum) with what each documents publicly, its status, the URL and the date it was checked; the only source for external comparisons | System health |
| `adoption-measurement` | Coverage vs adoption distinction, four adoption signals, leading vs lagging indicators, team-level vs system-level metrics, adoption maturity stages | Adoption report, system health, docs coverage |
| `output-discipline` | Shared quality standards for all audit and assessment output — scoping claims to what was inspected, respecting intentional deviations, cutting process while keeping substance, consistent severity and status indicators, proof for empty results, and a source for every figure | Every audit and validate skill and most document and communicate skills |
| `executive-communication` | Audience calibration, framing, metric translation, anti-patterns, and numbers honesty (every figure measured, estimated, or assumed; derived figures recalculated) | Stakeholder brief, system pitch |
| `configuration-and-recurring` | How skills load `.ds-ops-config.yml`, fall back when an integration fails, integration cautions (GitHub, npm, Figma, Storybook, Chromatic), and the recurring-run procedure (compare, save, propose pruning) | Every configurable skill when a config file exists |

---

## Two levels of output

Every skill operates at two levels automatically — you do not need to configure this.

**Senior level:** Thorough analysis and documentation. This is what most users need and what every skill produces by default.

**Staff level:** Additional capabilities that activate when your system's complexity warrants them. These include dependency graph analysis, blast radius modelling, API contract validation, structured JSON metadata for MCP servers, DTCG 2025.10 specification alignment, design system maturity assessment, AI-readiness assessment, cross-system analysis, and platform infrastructure thinking.

You do not need to ask for staff-level output — the skills assess your system's complexity and include it when relevant.

---

## Sample outputs

The `sample-outputs/` directory contains 13 sample outputs. The five `fixture-*` files are unedited runs against the small test design system in `tests/fixtures/`; anyone can regenerate them with the evals. Use these to understand the depth and format of what the skills produce.

| Sample | Skill used | What it shows |
|---|---|---|
| `example-component-description.md` | ai-component-description | Complete six-section description for a React Dialog component |
| `example-token-audit.md` | token-audit | Full audit of a ~480 token system with CSS custom properties and JSON source |
| `system-health-meridian.md` | system-health | Complete health assessment for a mid-sized design system with seven dimension ratings |
| `component-audit-react-library.md` | component-audit | Full component inventory with Challenge Ratings, duplication analysis, and recommendations |
| `drift-detection-harbor-consumer-app.md` | drift-detection | Drift analysis showing hardcoded values, local reimplementations, and suggested fixes |
| `stakeholder-brief-meridian-q1.md` | stakeholder-brief | One-page executive brief: situation, recommendation, a sourced capacity ask, and open placeholders listed at the top |
| `docs-coverage-carbon-react.md` | docs-coverage | Docs coverage audit of a real public Storybook (IBM Carbon React): coverage by rung, git-based staleness, and join-confidence tiers |
| `example-health-dashboard.html` | visual-report | Interactive HTML dashboard built from audit findings: health radar, severity distribution, priority matrix. Open in a browser |
| `fixture-token-audit.md` | token-audit | Unedited run against the test fixture: tier leakage in `card.border` found and traced to the dark-mode break it causes |
| `fixture-token-compliance.md` | token-compliance | Unedited run against the test fixture: an off-palette hex logged once with its nearest token, exempt keywords correctly left alone |
| `fixture-docs-coverage.md` | docs-coverage | Unedited run against the test fixture: an exported component with no story, with path-resolved join confidence |
| `fixture-accessibility-per-component.md` | accessibility-per-component | Unedited run against the test fixture: a tooltip with no `aria-describedby` link and no hover or focus behaviour, nothing marked PASS on code inference alone |
| `fixture-theme-audit.md` | theme-audit | Unedited run against the test fixture: a border with no dark value found, correct dark elevation and inherited spacing left alone |

---

## Optional configuration

Design System Ops works out of the box with no configuration. If you want to customise it, create a `.ds-ops-config.yml` file in your project root. A fully annotated template ships with the repo at `ds-ops-config.example.yml` in the root — copy it across and rename it.

**What you can configure:**
- Severity levels for specific violation types
- Integration endpoints (Figma MCP, GitHub, npm, Style Dictionary, Storybook, Chromatic, documentation platforms)
- Recurring workflows with trend tracking
- Release gate overrides for agreed team exceptions

See **[3-SETUP-AND-CONFIG.md](3-SETUP-AND-CONFIG.md)** for the complete configuration guide.

---

## Small-system awareness

If your system has fewer than 5 components, every skill and agent adapts automatically. Small systems are not broken systems — they are early systems. Audit skills shift from compliance checking to per-component deep dives. Governance skills recommend workshops over formal processes. Communication skills reframe ROI around quality consistency rather than scale.

---

## Getting started — recommended first steps

**If you want to understand where your system stands:**
Say "how healthy is my design system?" — this triggers `system-health` and gives you the broadest picture.

**If you want to audit your tokens:**
Say "audit my tokens" and point it at your token files.

**If you want to make your components AI-ready:**
Say "write an AI component description for [your most-used component]" — this is the differentiating skill and shows the value immediately.

**If you want the full diagnostic:**
Say "run a full system diagnostic" — this chains six skills (plus conditional theme and Figma audits) and produces a unified report.

**If you just need to communicate up:**
Say "write a stakeholder brief" with whatever data you have.

---

## What is in this package

### Folder structure

```
design-system-ops/
├── .claude-plugin/           ← Plugin manifest
│   └── plugin.json
├── ds-ops-config.example.yml ← Config template (copy to your project as .ds-ops-config.yml)
├── verify-install.sh         ← Checks every skill can find its knowledge notes
├── llms.txt                  ← A short map of the pack for AI agents
├── README.md                 ← Overview
├── 1-INSTALL.md              ← Quick-start installation guide
├── 2-WHATS-INCLUDED.md       ← This file
├── 3-SETUP-AND-CONFIG.md     ← Detailed setup, configuration, and troubleshooting
├── CHANGELOG.md              ← Version history
├── CONTRIBUTING.md           ← Contribution guide
├── LICENSE                   ← MIT license
│
├── skills/                   ← 36 skills, each in its own directory, plus 4 agent chains
│   ├── accessibility-per-component/
│   │   └── SKILL.md
│   ├── adoption-report/
│   │   └── SKILL.md
│   ├── agent-instructions/
│   │   └── SKILL.md
│   ├── ai-component-description/
│   │   └── SKILL.md
│   ├── backlog-generator/
│   │   └── SKILL.md
│   ├── change-communication/
│   │   └── SKILL.md
│   ├── cicd-integration/
│   │   └── SKILL.md
│   ├── codebase-index/
│   │   └── SKILL.md
│   ├── codemod-generator/
│   │   └── SKILL.md
│   ├── component-api-validator/
│   │   └── SKILL.md
│   ├── component-audit/
│   │   └── SKILL.md
│   ├── component-decision-tree/
│   │   └── SKILL.md
│   ├── contribution-workflow/
│   │   └── SKILL.md
│   ├── decision-record/
│   │   └── SKILL.md
│   ├── deprecation-process/
│   │   └── SKILL.md
│   ├── design-to-code-check/
│   │   └── SKILL.md
│   ├── docs-coverage/
│   │   └── SKILL.md
│   ├── drift-detection/
│   │   └── SKILL.md
│   ├── figma-variable-audit/
│   │   └── SKILL.md
│   ├── governance-encoder/
│   │   └── SKILL.md
│   ├── metadata-schema-generator/
│   │   └── SKILL.md
│   ├── naming-audit/
│   │   └── SKILL.md
│   ├── onboarding/
│   │   └── SKILL.md
│   ├── pattern-documentation/
│   │   └── SKILL.md
│   ├── release-retrospective/
│   │   └── SKILL.md
│   ├── schema-validator/
│   │   └── SKILL.md
│   ├── stakeholder-brief/
│   │   └── SKILL.md
│   ├── system-health/
│   │   └── SKILL.md
│   ├── system-pitch/
│   │   └── SKILL.md
│   ├── theme-audit/
│   │   └── SKILL.md
│   ├── token-audit/
│   │   └── SKILL.md
│   ├── token-compliance/
│   │   └── SKILL.md
│   ├── token-documentation/
│   │   └── SKILL.md
│   ├── usage-guidelines/
│   │   └── SKILL.md
│   ├── version-bump-advisor/
│   │   └── SKILL.md
│   ├── visual-report/
│   │   └── SKILL.md
│   ├── component-to-release-agent.md      ← Agent chain
│   ├── full-system-diagnostic-agent.md    ← Agent chain
│   ├── governance-review-agent.md         ← Agent chain
│   └── token-migration-agent.md           ← Agent chain
│
├── commands/                 ← 4 slash commands
│   ├── full-diagnostic.md
│   ├── governance-review.md
│   ├── release-check.md
│   └── token-migration.md
│
├── knowledge-notes/          ← 13 reference documents (single canonical source)
│   ├── adoption-measurement.md
│   ├── agent-orchestration-guide.md
│   ├── ai-readiness.md
│   ├── component-bestiary-reference.md
│   ├── component-governance.md
│   ├── configuration-and-recurring.md
│   ├── design-to-code-contract.md
│   ├── documentation-coverage.md
│   ├── executive-communication.md
│   ├── mcp-setup-guide.md
│   ├── output-discipline.md
│   ├── public-systems-reference.md
│   └── token-architecture.md
│
├── sample-outputs/           ← 13 sample outputs
│   ├── component-audit-react-library.md
│   ├── docs-coverage-carbon-react.md
│   ├── drift-detection-harbor-consumer-app.md
│   ├── example-component-description.md
│   ├── example-health-dashboard.html
│   ├── example-token-audit.md
│   ├── fixture-accessibility-per-component.md
│   ├── fixture-docs-coverage.md
│   ├── fixture-theme-audit.md
│   ├── fixture-token-audit.md
│   ├── fixture-token-compliance.md
│   ├── stakeholder-brief-meridian-q1.md
│   └── system-health-meridian.md
│
└── installable/              ← Pre-built .plugin (Cowork) and .zip bundles
```

Skills reference the canonical `knowledge-notes/` directory directly through frontmatter paths (e.g., `../../knowledge-notes/filename.md`). Each skill tells Claude to read the notes in its `references:` field before it starts, and stops if any are missing — you do not need to manage separate copies. This keeps knowledge notes in a single, maintainable location.

---

## Detailed setup, configuration, and troubleshooting

See **[3-SETUP-AND-CONFIG.md](3-SETUP-AND-CONFIG.md)** for: integration setup instructions, framework compatibility (React, Vue, Twig, Emotion, Tailwind), monorepo considerations, recommended workflow sequences, and troubleshooting.

---

## About

Murphy Trueman is a design systems leader and writer with 14+ years of experience. This product is built from real work — production atomic design systems, a three-tier token architecture built for a large-scale enterprise platform, and production AI governance work in agentic component generation.

blog.murphytrueman.com · thecomponentbestiary.com · designsystemsforai.com

If you found this useful, [buy me a coffee](https://buymeacoffee.com/murphytrueman).
