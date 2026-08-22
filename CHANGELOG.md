# Changelog

All notable changes to Design Systems OS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Test suite (`tests/`)** — 43 stdlib-Python tests, no dependencies. Validates skill frontmatter (name/description present, kebab-case, name matches directory, names unique), that every `references:` path resolves and stays inside the repo, that no knowledge note is orphaned, that every slash command declares `allowed-tools` and every `${CLAUDE_PLUGIN_ROOT}` path it loads exists, that `plugin.json` is well-formed semver agreeing with this file, that relative links and images in the shipped docs resolve, and that `build.sh` produces a byte-identical `.zip`/`.plugin` pair containing every skill and no tooling. Run with `./tests/run.sh`.
- **CI (`.github/workflows/ci.yml`)** — Runs the suite on Python 3.9 and 3.12 plus shellcheck on `build.sh`, on every push to `main` and every pull request.

### Changed

- **`build.sh`** — Output directory is now overridable via `DSOPS_OUT_DIR` (namespaced so a generic `OUT_DIR` in a contributor's shell can't redirect the build) so tests can build into a temp dir without touching the committed bundle. `tests/` and `.github/` are excluded from the bundle: CI runs them, installers never see them.
- **README** — `Install` renamed to `Installation` and `Quick examples` to `Usage`, so registry linters that index this repo find the headings they look for. The old `#install` and `#quick-examples` anchors are preserved via inline anchor tags, so existing external links still resolve. Added a CI badge and a contributing note about the test suite.

## [1.2.0] - 2026-06-26

### Added

- **docs-coverage skill** — Audits whether the documentation surface keeps pace with the component library: coverage gaps (components with no docs), staleness (docs that predate the component's last code change, computed from git), and orphaned docs. Works with zero integration from the codebase plus a Storybook build; Zeroheight, Supernova, and custom docs sites are optional layers. Every coverage finding carries a join-confidence tier so a fuzzy name match is never presented as fact. Ships with a new `documentation-coverage` knowledge note, a `docs-coverage` command, and a sample output (`docs-coverage-carbon-react`) generated against a real public Storybook index.
- **theme-audit skill** — Dedicated skill for auditing theme implementation. Covers theme discovery, coverage checking, component-tier propagation, visual consistency, DTCG resolver validation, and regression detection.
- **4 new sample outputs** — system-health-campusiq, drift-detection-sparky-consumer-app, stakeholder-brief-campusiq-q1, component-audit-fintech-pulse. These join the existing samples to provide calibration material across the most-used skill categories.
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
