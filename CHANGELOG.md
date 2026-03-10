# Changelog

All notable changes to Design Systems OS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **theme-audit skill** — Dedicated skill for auditing theme implementation. Covers theme discovery, coverage checking, component-tier propagation, visual consistency, DTCG resolver validation, and regression detection.
- **4 new sample outputs** — system-health-campusiq, drift-detection-sparky-consumer-app, stakeholder-brief-campusiq-q1, component-audit-fintech-pulse. These join the existing samples to provide calibration material across the most-used skill categories.
- **CHANGELOG.md** — This file.
- **LICENSE** — MIT license.

### Changed

- **adoption-report skill** — Expanded from a structural outline to a full step-by-step workflow with 5 phases, calibration checkpoint, integration awareness, small-system guidance, and quality checks. Now matches the procedural depth of the audit skills.
- **stakeholder-brief skill** — Expanded with tone calibration by audience (engineering, product, design leadership), framing patterns, anti-patterns, maturity-level framing, and quality checks.
- **system-pitch skill** — Expanded with ROI calculation framework, 7 objection handlers, audience calibration, investment models, risk framing, and anti-patterns section.
- **All 13 commands** — Widened `allowed-tools` lists to include `Bash(ls:*)`, `Bash(cat:*)`, `Bash(head:*)`, `Bash(tail:*)` and other baseline tools where missing, preventing silent failures during real-world codebase navigation.
- **Knowledge note references consolidated** — All skills with references now point to the canonical `knowledge-notes/` directory via `../../knowledge-notes/` instead of per-skill copies. Eliminates duplicated files and the maintenance drift they caused.
- **Redundant prose loading instructions removed** — Skills that had both frontmatter `references:` declarations and prose "Reference material" sections now rely solely on the frontmatter, saving tokens and eliminating ambiguity.

### Fixed

- **Sample output path references** — Corrected provenance paths in sample outputs to match actual plugin structure (`skills/` prefix).
