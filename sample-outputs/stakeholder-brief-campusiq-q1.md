# Stakeholder brief: CampusIQ design system investment

**Date:** 2026-03-10
**Prepared by:** Design Systems Team
**For:** VP Engineering & Product Leadership
**Regarding:** Q1 2026 design system governance review and investment recommendation

---

## The situation

The CampusIQ design system is currently serving three of six product teams — Facilities, Roster, and Finance teams build new features using shared components and consistent visual design. Three teams — Mobile, Analytics, and Integrations — are building their own component implementations and diverging from the shared system. This is creating duplicate engineering effort (each team building the same Button, Card, Input components) and inconsistent customer experiences (similar features look and work differently depending on which team built them).

A design system is the shared library of interface components and design standards that lets multiple teams build consistently without rebuilding the same pieces each time. CampusIQ is about 60% toward being the system we need — the components are well-built and documented, but governance is informal and adoption is optional. This matters because inconsistent products create customer confusion, support burden, and slower feature development cycles.

---

## Why this matters

The duplicate engineering work is expensive. A conservative estimate: the low-adoption teams are spending 20–30% of their development cycle building and maintaining components that already exist in the system. For a team of 5 engineers across 6 months, that is the equivalent of 2–3 engineers' full-time effort, spent on work that is not moving the product forward.

The inconsistent customer experience is a trust problem. A customer using the Mobile app sees one interface pattern for "empty state" or "error message," then switches to the web app built by the Roster team and sees something visually different. This fragmentation signals a lack of polish and increases support tickets for questions like "Is this a bug or intentional?" In a crowded education-tech market, consistency and polish are competitive differentiators.

If we do nothing, the cost of these parallel implementations will compound. When the Facilities team updates their Button for accessibility or performance, the other teams do not benefit. Each team solves the same problems independently. Over 18 months, this creates a maintenance debt that is expensive to unwind.

---

## What we recommend

**Dedicate one engineering day per sprint from each low-adoption team to system integration, for the next two quarters.** This creates sustained focus on migration without displacing product work. By the end of Q2, the target is 80%+ adoption across all teams — most new features built using shared components, with intentional divergence only where genuinely needed.

We recommend quarterly migration cadence over a one-time effort because the migration compounds. In sprint 1, the Mobile team identifies which of their custom components overlap with system components and prioritizes highest-risk components (authentication, data entry) first. In sprint 2, they migrate 3–4 components and unblock dependent product work. Each sprint gets easier as teams get better at spotting system components that work for their needs.

The alternative — mandatory adoption with enforcement — would be faster (one sprint, 100% adoption) but creates resentment and does not solve the real problem (teams diverging because the system does not serve their needs). The adoption we recommend is negotiated, evidence-based, and leaves room for intentional local work where the system genuinely does not fit.

---

## What we need

- **Decision:** Commit to the system as strategic infrastructure, not optional toolkit. This sets the tone for teams — investment in the system is expected, not discretionary.

- **Resource allocation:** One engineering day per sprint per low-adoption team (approximate: 3 teams × 0.2 FTE × 2 quarters = 0.6 FTE equivalent time). This does not require hiring; it is prioritization within existing headcount.

- **Governance documentation:** Approve a one-week investment for the design systems team to document contribution and deprecation processes. This makes the system predictable for consuming teams and removes friction.

---

## Expected outcome

By end of Q2 2026, the CampusIQ system will be adopted across all product teams for core components (authentication, forms, buttons, navigation, empty states, error handling). Custom implementations will be rare and intentional, documented as decisions. New team members will have a consistent starting point instead of learning different patterns in different parts of the product.

The immediate business impact is straightforward: fewer lines of code maintained per feature, faster feature shipping, and more consistent customer experience. The efficiency gain compounds — teams that are not rebuilding components spend that time on features instead.

This is not a magical transformation. We are not eliminating local customization or requiring teams to use the system for everything. We are creating the conditions where the system becomes the default and divergence is the exception, not the rule.

---

*Generated by Design Systems OS — `communication/stakeholder-brief` skill*
*Source: CampusIQ Design System Q1 2026 health assessment*
