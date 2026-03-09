---
description: Score your design system's overall health
allowed-tools: Read, Grep, Glob
---

Run the system-health skill to produce a scored health assessment of the user's design system.

Load the system-health skill from ${CLAUDE_PLUGIN_ROOT}/skills/system-health/SKILL.md and follow its complete workflow.

Before starting, read the reference material specified in the skill's frontmatter from ${CLAUDE_PLUGIN_ROOT}/skills/system-health/references/.

Begin with Step 1b (Baseline calibration) to establish the system's maturity level before scoring. Score all 7 dimensions (Tokens, Components, Documentation, Adoption, Governance, AI readiness, Platform maturity) with calibrated expectations appropriate to the system's maturity level.

Produce the full health report including: dimension scores out of 35, maturity level assessment, specific findings per dimension, and a prioritised action list.

If the user provides context about their system as an argument, use it: $ARGUMENTS
