# Adoption measurement principles

**Knowledge note for Design System Ops**
**Auto-loaded by:** adoption-report

---

## Coverage is not adoption

Coverage measures whether the system provides what teams need. Adoption measures whether teams actually use what the system provides. A system can have 100% component coverage and 20% adoption if teams build custom implementations instead of consuming the library.

The distinction matters because the interventions are different. Low coverage is a supply problem — the system team needs to build more. Low adoption with high coverage is a demand problem — the system team needs to understand why teams are not consuming what exists.

---

## The four adoption signals

### 1. Installation and integration

The most basic signal: are teams using the system's packages at all? Measured by package install counts, version currency (how far behind the latest release each consumer is), and integration completeness (are teams importing the token layer, the component layer, or both?).

This is a necessary but not sufficient signal. A team can install the package and not use it.

### 2. Component consumption

Are teams using the system's components in their product code? Measured by import analysis across consuming codebases: which components are imported, how frequently, and by how many distinct products or teams.

The long tail matters: a system where 5 components account for 90% of imports and 30 components are rarely used has an adoption problem in the tail, even if the headline number looks good.

### 3. Token compliance

Are teams using the system's tokens rather than hardcoding values? Measured by scanning consuming codebases for raw values (hex colours, pixel values, font stacks) that should be token references. This is the adoption signal that most directly correlates with system value — token adoption is what enables theming, rebranding, and consistency.

### 4. Pattern adherence

Are teams following the system's documented patterns for composition, layout, and interaction? This is the hardest signal to measure automatically and often requires periodic manual review or heuristic analysis.

---

## Leading vs lagging indicators

**Leading indicators** predict future adoption health:
- New team onboarding time (are teams getting started faster?)
- Contribution rate (are consuming teams contributing back?)
- Support ticket volume and topic distribution (what are teams struggling with?)
- Documentation page views and search patterns (what are teams looking for?)

**Lagging indicators** confirm past adoption outcomes:
- Component import counts across codebases
- Token compliance percentages
- Version currency across consumers
- Custom implementation counts (components built outside the system that duplicate system functionality)

A healthy adoption report includes both. Leading indicators alone are aspirational. Lagging indicators alone are retrospective.

---

## Team-level vs system-level metrics

System-level metrics (total imports, overall token compliance) mask team-level variation. A system with 85% overall token compliance might have three teams at 98% and two teams at 40%. The system-level number suggests health; the team-level numbers reveal a problem.

Always break adoption metrics down by team or product area. The team-level view is where actionable insights live.

---

## Adoption maturity stages

Not every team will be at the same stage, and that is expected. The stages help calibrate expectations and identify appropriate interventions:

**Stage 1: Aware** — The team knows the system exists but has not integrated it. Intervention: onboarding support, not pressure.

**Stage 2: Installed** — The team has installed the packages but uses them minimally. Intervention: identify barriers (missing components? poor documentation? competing priorities?).

**Stage 3: Consuming** — The team actively uses system components and tokens for new work. Intervention: support, gather feedback, address gaps.

**Stage 4: Contributing** — The team contributes back to the system (bug reports, component proposals, documentation improvements). Intervention: streamline the contribution path, recognise contributions.

**Stage 5: Advocating** — The team promotes the system to other teams and helps onboard them. Intervention: enable peer support, involve in governance.

---

## What adoption reports should not do

Adoption reports should not rank teams competitively. Publishing a league table of "best adopters" and "worst adopters" creates political dynamics that undermine trust. Report team-level data to the system team for targeted support. Report system-level aggregates to leadership for investment decisions.

Adoption reports should not treat non-adoption as failure without understanding context. A team that builds a custom data visualisation library is not failing to adopt the system — the system may not cover their domain. The report should distinguish between "chose not to use available components" and "needed something the system does not provide."
