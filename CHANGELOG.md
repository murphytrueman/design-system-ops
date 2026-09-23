# Changelog

All notable changes to Design Systems OS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Five unedited sample outputs** — `fixture-token-audit`, `fixture-token-compliance`, `fixture-docs-coverage`, `fixture-accessibility-per-component` and `fixture-theme-audit`, produced by the evals against the test design system in `tests/fixtures/`. Unlike the anonymised samples, nothing in them is edited, and anyone can regenerate them. Each was checked as a sample, not just as a pass: the skill loaded, and the planted problem appears as a real finding.

### Fixed

- **The eval grader read words, not findings.** It passed a case if the planted problem was mentioned anywhere and failed it if a correct thing shared a line with a word like "violation" — so an exclusions note saying `currentColor` and `transparent` "are not violations" failed a correct run. It now grades only what appears inside findings.

- **The evals weren't reliably testing the skills.** The runner denied the Skill tool, so a run either read `SKILL.md` by hand or answered without the skill at all — one passing case said outright that it couldn't load the skill. The Skill tool is now allowed, the runner reads Claude Code's event stream, and a case fails unless the skill under test was actually loaded. It also checks the plugin is complete with `verify-install.sh` before running, instead of guessing from the model's wording.
- **`token-compliance` listed some values twice with two labels.** A hardcoded value that matched no token appeared in the violation table with a severity and again in a separate ⚠️ WARN list. Each value now appears once, with off-system values marked in the Notes column.

## [1.3.1] - 2026-09-23

### Fixed

- **Eight commands were hiding the skills they shared a name with.** Claude Code loads each command as a skill too, and `token-audit`, `component-audit`, `system-health`, `docs-coverage`, `system-benchmark`, `visual-report`, `codemod-generator` and `cicd-integration` existed as both. Where names matched, the command's one-line description replaced the skill's, so Claude routed those eight skills on the thin version. The duplicate commands are removed; their pre-approved tools moved into each skill's frontmatter, and the skills run directly as `/design-system-ops:<skill>`. Six commands remain: the four agent workflows plus `drift-check` and `describe-component`. A test now rejects any command that shares a skill's name, and one checks that a skill's own tool list covers the commands it runs.
- **Docs checked against a real install.** Cloning into `.claude/skills/` loads the pack as a skills-directory plugin (`claude plugin list` shows `design-system-ops@skills-dir`); a project-level install needs the folder trusted first. Commands are namespaced (`/design-system-ops:<name>`), and the chained workflows are run by command. The README and install guide now say so, and the token-audit, Challenge Rating and agent-chain descriptions match the skills.
- **The folder tree in `2-WHATS-INCLUDED.md`** listed 39 of 40 skills, 13 command files that don't exist, and 11 of 14 knowledge notes. It's regenerated from the files, and a test now compares it with disk.

## [1.3.0] - 2026-09-23

### Added

- **Install self-check in every reference-bearing skill** — All 36 skills that list `references:` now open with a "Before you begin: verify references" step. If a knowledge note is missing, the skill stops and says the install is incomplete instead of running without its reference material and answering with the same confidence. Third-party installers that flatten each skill into its own folder (for example `npx skills install`) drop the repo-root `knowledge-notes/` directory, and before this change that failure was silent. The skill only proceeds without references if the user explicitly says to, and then labels its output as degraded.
- **`verify-install.sh`** — A doctor script at the repo root (and inside the `.plugin` bundle). It checks every `references:` path in every skill, prints `OK` or `MISSING` per skill, and exits non-zero on an incomplete install. It also recognises a single flattened `SKILL.md`. It refuses to report a pass it can't back up: a skill file with a `references:` field it can't read is reported as `UNREADABLE`, and a `skills/` folder that yields no references at all fails rather than printing "All 0 references resolve." Run it from the install root, or pass an install directory as the first argument.
- **As-shipped check** — The build tests now unpack the freshly built bundle and run the `verify-install.sh` inside it. Every other test reads the repo; this one reads what users actually download.
- **`llms.txt`** — A short map of the pack for AI agents and indexers, including the one thing a flattening installer needs to know: skills depend on `knowledge-notes/` sitting next to `skills/`.
- **Install rehearsal** — A pre-release checklist in `CONTRIBUTING.md`: install the pack each supported way, plus once the unsupported way, into a scratch folder outside the repo, and run a skill in a new session.
- **`tests/sync_selfcheck.py`** — One command to bring every skill's self-check block in line with the canonical text in `dsops.py` (`--check` reports without writing). Test failures now name it.
- **Tests** — `tests/test_verify_install.py` pins the script's behaviour against a clean checkout, a flattened install, a lone `SKILL.md`, an unreadable skill file, an empty `skills/`, and a non-install directory. `TestSkillSelfCheck` in `test_skills.py` requires the self-check block to be a verbatim copy of `dsops.REFERENCE_CHECK_BLOCK`, to be the first H2 in each reference-bearing skill, and to be absent from skills and agents that have no references. It also feeds the resync tool a deliberately edited block and checks the fix restores the canonical text. `test_inventory.py` now pins every present-tense count in `1-INSTALL.md`, `2-WHATS-INCLUDED.md`, and `3-SETUP-AND-CONFIG.md`, including the per-category skill counts, and fails if a claim's wording disappears. CI now shellchecks `verify-install.sh`.

- **`executive-communication` knowledge note** — Audience calibration, framing, metric translation, anti-patterns, and a numbers-honesty section for leadership-facing documents. `system-pitch` and `stakeholder-brief` load it instead of each carrying their own copy, which removes about 3,800 words of near-duplicate guidance between them.
- **Chained-run rules** in the `agent-orchestration-guide` note, followed by all four agents: load each skill only when its step starts, build one inventory up front, pass a short hand-off card between steps, and produce one report with one headline, one Scope block and one closing note rather than a stack of per-skill reports.
- **Output-rule tests (`tests/test_output_rules.py`)** — Scans every skill, agent, command, knowledge note and sample output for numeric scores, percentage ratings and numbered maturity levels; requires every JSON example to parse; and rejects bare `yes`/`no` keys in YAML examples, which YAML 1.1 parsers read as booleans. Each check is probed with known-bad input so it can't pass vacuously.
- **Evals against a fixture design system** — `tests/fixtures/sample-ds/` is a small design system with problems planted in it: a component token that skips the semantic tier, an off-palette hex in a component, an exported component with no documentation, a tooltip that isn't linked to its trigger, and a border with no dark-theme value. It also contains things that are correct and must not be flagged (a dark theme whose raised surfaces are lighter than the base, spacing that inherits between themes). `tests/evals/run_evals.py` runs skills headlessly against a fresh build and checks each one finds its planted problem without flagging the controls. It costs real usage, so it runs before a release rather than in CI. `tests/test_fixture.py` keeps the fixture honest in CI.
- **Consistency tests (`tests/test_consistency.py`)** — Every config key a skill reads must be documented in `ds-ops-config.example.yml`, and every shell command a skill runs must be pre-approved by the slash command that loads it. Both found real gaps: nine undocumented config sections and six commands missing a read-only tool approval.
- **`configuration-and-recurring` knowledge note** — The procedure every configurable skill shared (loading config, falling back when an integration fails, integration cautions, recurring comparisons) now lives in one place. Skills read it only when a `.ds-ops-config.yml` exists, so runs without a config file don't pay for it. It also makes pruning old reports consistent: proposed and confirmed, never automatic.
- **Description length cap** — Skill and agent descriptions are now 300 characters or fewer, enforced by a test. Descriptions are loaded into every session and the listing has a budget; at the previous average of ~600 characters, later skills lost their descriptions and stopped routing.

### Changed

- **Accuracy review of every skill, agent and command.** Each finding was checked against the file before it was fixed. The pattern behind most of them: skills could produce confident output from nothing. The main changes:
  - **A source for every figure and fact.** New `output-discipline` section: facts about the user's system come from inspected files or the user; figures are labelled measured, estimated or assumed; derived figures are recalculated; gaps stay visible as `[needs data]`, and deliverables list open placeholders at the top instead of filling them. Every "no placeholders" or "send as-is" instruction is gone. Generator skills (documentation, metadata, decision trees, governance rules, context-engine blueprints) mark anything not traced to source as `proposed` or `unverified`.
  - **Every audit template ends with a standard Scope block** — inspected, not inspected, how "none found" was checked, assumptions — and searches that can return nothing now include a positive control.
  - **No numeric scores anywhere.** Removed from the `/system-health` and `/full-diagnostic` commands ("scores out of 35"), `system-benchmark`, `schema-validator`, `component-api-validator`, `context-engine-builder`, and three sample outputs. Invented labels (INFO, NEEDS WORK, "clean / minor / significant") replaced with the three standard label sets. Maturity is described by named stage (Ad-hoc, Managed, Systematic, Measured, Optimised), never numbered levels.
  - **WCAG 2.2 AA is the default baseline**, with a note that some legal baselines (e.g. EN 301 549) still reference 2.1 AA. `accessibility-per-component` adds the component-level 2.2 criteria (target size, focus not obscured, dragging movements) and stops citing obsolete 4.1.1.
  - **DTCG 2025.10 value shapes** in `token-architecture` and `schema-validator`: colours, dimensions and durations are objects, dimensions allow only `px` and `rem`, `fontStyle` is not a type, and an untyped token takes its type from its alias target before its group.
  - **Coverage, reach and adoption** now mean one thing each in `adoption-report`: coverage is what the system provides, reach is which teams have access, adoption is which teams ship with it.
  - **Agents stay command-invoked.** Their descriptions now document the chain rather than list trigger phrases, so expensive multi-skill runs start only from an explicit command. `/migration` now calls `codemod-generator` and `deprecation-process` instead of carrying its own versions, and stops for confirmation before the communication phase. The release pipeline no longer writes to Figma.
  - **Neighbouring skills point at each other** ("use X instead") so near-identical requests route to the right one, and several skills stop doing their neighbours' jobs: `token-compliance` drops its token-definition checks, `design-to-code-check` hands API and metadata checks to their own skills, and `ai-component-description` is prose-only, with JSON metadata owned by `metadata-schema-generator`.
  - **Right-sized references.** `system-health` drops three notes it never used and loads the three its dimensions need; `visual-report`, `theme-audit`, `triage` and several others now load `output-discipline`.
- **`output-discipline` knowledge note — empty results need proof.** New section: before a skill reports that something is absent ("no hardcoded colours found", "every component has docs"), it confirms the search could have found it, by showing the pattern matches a known example in the codebase or that it ran over the files that would contain it. Otherwise the result is reported as unconfirmed, not clean. A search that doesn't fit the codebase returns nothing, and nothing reads exactly like a clean result. Applies to every skill that loads the note.

### Fixed

- **`3-SETUP-AND-CONFIG.md` troubleshooting** — The "skill didn't load the knowledge notes" entry cited a path that no longer exists (`skills/audit/token-audit.md`). It now names the real cause, flattening installers, and starts with `verify-install.sh`.
- **`1-INSTALL.md`** — Adds a supported-install-methods note and a "Verify your install" step, and corrects the stale repo-contents table (40 skills, 14 commands, no per-skill `references/` folders).
- **`3-SETUP-AND-CONFIG.md` directory tree** — Said 13 commands and 11 knowledge notes. Found by the new count tests.
- **Factual errors in skills:**
  - `theme-audit` said dark-theme surfaces should be darker than the background; raised surfaces are lighter. It also flagged tokens that correctly inherit from the default theme.
  - `system-pitch`'s worked ROI example claimed a 10-month payback its own numbers didn't support, and valued time at a different hourly rate on each side. Rebuilt with one rate; payback lands in month 15.
  - The `stakeholder-brief` sample computed 20–30% of five engineers as "2–3 engineers" and misread its source, which reported adoption, not time spent.
  - `accessibility-per-component` cited 2.4.11 for focus-ring contrast (it's 1.4.11), and its disclosure example referenced an id that didn't exist.
  - `token-compliance`'s GitHub search was malformed and returned nothing, which read as clean. It now searches the local checkout and checks the pattern finds known values first.
  - `codemod-generator`'s no-op test always failed, and its dry run skipped `.tsx` files.
  - `deprecation-process`'s decision tree made step 3 unreachable.
  - `component-decision-tree`'s YAML used bare `yes`/`no` keys.
  - `context-engine-builder` pointed nine times at a `references/` folder that no longer exists.
  - `session-memory` matched findings across runs by per-run ID, mislabelling resolved and new findings.
  - `figma-variable-audit` assumed dot-separated names and missing mode values, neither of which Figma has, and over-stated what the official Figma MCP can read.
  - `system-health` and `token-audit` treated the component token tier as required.
  - `/full-diagnostic` didn't allow `git log`, so documentation staleness always came back "unknown". `/codemod-generator` promised a ROLLBACK.md the skill never produced; rollback now lives in MIGRATION.md.
  - CI templates used end-of-life Node 20 and old action versions.
- **`ds-ops-config.example.yml` documents every key the skills read** — added `system.component_paths`, `system.tokens`, `system.token_format`, `system.category_model`, `system.content_guidelines_path`, `integrations.code_tokens`, the `severity.api_*` and `severity.schema_*` prefixes, and the skill-specific sections `decision_tree`, `context_engine`, `cicd`, `codemods`, `governance`, `metadata`, `memory`, `benchmark` and `visuals`.
- **Command tool approvals** — `/cicd-integration`, `/codemod-generator`, `/migration`, `/drift-check`, `/governance-review` and `/release-check` now pre-approve the read-only commands their skills run (`git diff`, `npx tsc`, `npm view`, `rg`), so headless runs don't stall on a permission prompt.
- **Sample outputs are described honestly** — the README called them "real outputs from real codebases". One is an unedited run against a public codebase; the rest are anonymised and edited, and the docs now say so.
- **`3-SETUP-AND-CONFIG.md`** — removed its stale version header and moved its dated history log into this file (below), so release history lives in one place.
- **Sample-output counts and tables** — The guides said 7, six and three sample outputs; there are 8, and both tables now list all of them. A test pins the count and requires every file in `sample-outputs/` to appear in each table.
- **Generic example names** — three skills used helper names that looked like they came from a specific codebase; replaced with `theme.colors.primary`, `theme.spacing(4)` and `theme.typography.body`.

## [1.2.1] - 2026-08-22

### Added

- **Test suite (`tests/`)** — 48 stdlib-Python tests, no dependencies. Validates skill frontmatter (name/description present, kebab-case, name matches directory, names unique), that every `references:` path resolves and stays inside the repo, that no knowledge note is orphaned, that every slash command declares `allowed-tools` and every `${CLAUDE_PLUGIN_ROOT}` path it loads exists, that `plugin.json` is well-formed semver agreeing with this file, that relative links and images in the shipped docs resolve, and that `build.sh` produces a byte-identical `.zip`/`.plugin` pair containing every skill and no tooling. Run with `./tests/run.sh`.
- **CI (`.github/workflows/ci.yml`)** — Runs the suite on Python 3.9 and 3.12 plus shellcheck on `build.sh`, on every push to `main` and every pull request.
- **Release automation (`.github/workflows/release.yml`)** — On a `v*` tag, verifies the tag matches `plugin.json`, runs the test suite, rebuilds the bundle, and attaches `design-system-ops.plugin` and `.zip` to the GitHub Release. The README points Cowork users at the latest Release for the download, so this keeps that asset from drifting from the repo.
- **Inventory tests** — The counts advertised in the `plugin.json` description and the skills listed in the README's "What's included" table are now pinned to the filesystem, in both directions.

### Changed

- **`build.sh`** — Output directory is now overridable via `DSOPS_OUT_DIR` (namespaced so a generic `OUT_DIR` in a contributor's shell can't redirect the build) so tests can build into a temp dir without touching the committed bundle. `tests/` and `.github/` are excluded from the bundle: CI runs them, installers never see them.
- **README** — `Install` renamed to `Installation` and `Quick examples` to `Usage`, so registry linters that index this repo find the headings they look for. The old `#install` and `#quick-examples` anchors are preserved via inline anchor tags, so existing external links still resolve. Added a CI badge and a contributing note about the test suite.

## [1.2.0] - 2026-06-26

### Added

- **docs-coverage skill** — Audits whether the documentation surface keeps pace with the component library: coverage gaps (components with no docs), staleness (docs that predate the component's last code change, computed from git), and orphaned docs. Works with zero integration from the codebase plus a Storybook build; Zeroheight, Supernova, and custom docs sites are optional layers. Every coverage finding carries a join-confidence tier so a fuzzy name match is never presented as fact. Ships with a new `documentation-coverage` knowledge note, a `docs-coverage` command, and a sample output (`docs-coverage-carbon-react`) generated against a real public Storybook index.
- **theme-audit skill** — Dedicated skill for auditing theme implementation. Covers theme discovery, coverage checking, component-tier propagation, visual consistency, DTCG resolver validation, and regression detection.
- **4 new sample outputs** — system-health-meridian, drift-detection-harbor-consumer-app, stakeholder-brief-meridian-q1, component-audit-react-library. These join the existing samples to provide calibration material across the most-used skill categories.
- **CHANGELOG.md** — This file.
- **LICENSE** — MIT license.

### Changed

- **full-system-diagnostic agent — docs-coverage added to the sweep.** The diagnostic now chains six audit skills (token, naming, component, drift, **docs-coverage**, system-health), with docs-coverage running before system-health so the documentation dimension is evidenced directly rather than inferred from naming. Pattern 2 (documentation gap) now cites docs-coverage as its direct evidence. `theme-audit` and `figma-variable-audit` were added as **conditional** steps, gated on `system.theming` and `integrations.figma` respectively — skipped (not flagged as gaps) when not applicable. `codebase-index` and `system-benchmark` were deliberately left out of the chain (infrastructure and external-benchmarking, respectively).
- **Config template renamed and un-hidden** — The shipped annotated config template moved from the hidden `.ds-ops-config.yml` to the visible, self-describing `ds-ops-config.example.yml`, following the conventional `.example` pattern. Users copy it into their project root and rename it to `.ds-ops-config.yml` (the name skills still read at runtime — unchanged). Makes the template discoverable in the bundle and unambiguous about being a template.
- **adoption-report skill** — Expanded from a structural outline to a full step-by-step workflow with 5 phases, calibration checkpoint, integration awareness, small-system guidance, and quality checks. Now matches the procedural depth of the audit skills.
- **stakeholder-brief skill** — Expanded with tone calibration by audience (engineering, product, design leadership), framing patterns, anti-patterns, maturity-level framing, and quality checks.
- **system-pitch skill** — Expanded with ROI calculation framework, 7 objection handlers, audience calibration, investment models, risk framing, and anti-patterns section.
- **All 13 commands** — Widened `allowed-tools` lists to include `Bash(ls:*)`, `Bash(cat:*)`, `Bash(head:*)`, `Bash(tail:*)` and other baseline tools where missing, preventing silent failures during real-world codebase navigation.
- **Knowledge note references consolidated** — All skills with references now point to the canonical `knowledge-notes/` directory via `../../knowledge-notes/` instead of per-skill copies. Eliminates duplicated files and the maintenance drift they caused.
- **Redundant prose loading instructions removed** — Skills that had both frontmatter `references:` declarations and prose "Reference material" sections now rely solely on the frontmatter, saving tokens and eliminating ambiguity.

### Fixed

- **Config filename typo in three skills** — `theme-audit`, `adoption-report`, and `stakeholder-brief` looked for `.ds-os-config.yml` (missing the `p`) instead of `.ds-ops-config.yml`, so they would never have found a user's config. Corrected all occurrences.
- **Stale skill lists in 1-INSTALL** — the per-category prompt tables were missing `theme-audit`, `docs-coverage` (Audit), and `triage` (Govern); category counts were corrected (Audit 8→10, Govern 10→11) and the missing rows added.
- **Slash command reference loading** — All 12 commands that load framework context pointed at a per-skill `references/` directory removed during the knowledge-note consolidation. They now read the knowledge notes declared in each skill's frontmatter `references:` field from `knowledge-notes/`, so commands no longer attempt to read a non-existent path.
- **triage skill count** — Corrected the skill count from 38 to 39 to account for the added `theme-audit` skill.
- **Sample output path references** — Corrected provenance paths in sample outputs to match actual plugin structure (`skills/` prefix).

## Before 1.2.0 (March 2026)

The pack's early history, kept as it was written at the time. It was previously logged in `3-SETUP-AND-CONFIG.md`; skill counts and paths below describe the pack as it was then.

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

1. **Knowledge note loading (canonical source)**
   - Established `knowledge-notes/` as the canonical source for all reference material
   - Updated skill files with `references:` YAML frontmatter pointing to knowledge notes via relative paths
   - All 40 skills now reference knowledge notes directly without local copies
   - Changes to knowledge notes are automatically picked up by all skills

2. **Expanded token input formats**
   - Added CSS custom properties, SCSS variables, TypeScript/JavaScript objects, and Tailwind config as accepted inputs
   - Updated `token-audit`, `token-documentation`, `token-compliance` with format-specific detection guidance
   - Updated `ai-readiness` knowledge note in `knowledge-notes/` for all skills to reference

3. **Sample output files**
   - Created `sample-outputs/` directory
   - Generated `example-token-audit.md` (~480 tokens, CSS custom properties + JSON)
   - Generated `example-component-description.md` (Dialog, React 18, Radix UI)

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
