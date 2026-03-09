---
name: designer-onboarding
description: "Create an onboarding guide for a designer joining a team that uses a design system. Trigger when someone says: onboard new designer, getting started guide, new team member guide, onboarding documentation, first day with the system, new designer guide, or anything about helping a designer new to the team or the design system get up to speed."
---

# Designer onboarding

A skill for creating a practical onboarding guide for a designer joining a team that uses a design system. Output covers system philosophy, tooling setup, contribution norms, and a first contribution path — structured so a new team member can follow it without additional help.

## Context

Onboarding documentation has a failure mode: it gets written for the person creating it, not the person reading it. It assumes context, skips steps that feel obvious to anyone who already knows the system, and leaves the new team member with a list of things to read rather than a path to follow.

The goal is an onboarding guide that a new designer could follow alone on their first day and feel oriented rather than overwhelmed. That means it has to be honest about what the system is and what it is not, explicit about where to get help, and structured so that early wins come before deep context.

## Step 1: Gather the system context

Ask for or confirm:
- The design system name and the organisation or product context it serves
- The tooling stack: Figma library, documentation platform, component package, contribution tools
- The team structure: who owns the system, who the new designer's main contacts are
- The key contribution norms: what the process is for using components, raising gaps, and contributing new work
- Any known rough edges or caveats a new designer should know upfront

If specific details are not available (e.g. specific Figma library link), use placeholders clearly marked for the team to complete before the guide is published.

**Small-system note (fewer than 5 components):** For systems with fewer than 5 components, the onboarding guide should be shorter and more personal. The "what the system covers" section can be a brief list rather than a conceptual overview — with 3 components, name them. The "your first two weeks" timeline can compress to a first week, since there is less to explore. Replace the "when the system does not have what you need" section with a more prominent one: "what the system covers and what it does not" — at this size, the gaps are as important as the coverage, and a new designer should know both from day one. Emphasise human relationships over documentation: "Ask [name] to pair with you on your first task using the system" is more effective than "explore the documentation platform" when the documentation platform has three entries.

## Step 2: Write the onboarding guide

---

### Getting started with [Design system name]

**For:** New designers joining [team/organisation]
**Last updated:** [date]
**Questions?** [Slack channel, team contact, or equivalent]

---

#### What this guide is for

Two to three sentences. This guide will orient you to how we use [design system name] day-to-day. It covers the tools, the way we work, and what to do when the system does not have what you need. It is not exhaustive — the system has more depth than any guide can cover — but it is enough to get you started and know where to look.

---

#### What [design system name] is

One paragraph. Not a textbook definition — a description of what the system actually does for this team.

Include:
- What the system covers (components, tokens, patterns, documentation, or some combination)
- What it does not cover (local team conventions, product-specific patterns that live outside the system)
- Who maintains it (dedicated team, shared responsibility, or named individuals)
- Where it lives (Figma library, documentation URL, npm package)

Be honest about the current state. "The system is mature in its component library but documentation is still catching up in some areas" is more useful to a new team member than "we have a comprehensive design system."

---

#### Tooling setup

Step-by-step setup instructions. Do not skip steps that feel obvious — the goal is that a new team member can follow this without asking for help.

**Figma**
1. [Where to access the Figma library — link or instructions for enabling it]
2. [How to confirm it is enabled and the components are available]
3. [Any Figma plugins the team uses — names, links, brief descriptions]
4. [How the file structure is organised — where to find what]

**Documentation**
1. [Documentation platform URL]
2. [How it is structured — the quickest way to find what you need]
3. [How to search effectively — any quirks or known gaps]

**Code (if relevant to the designer's role)**
1. [How to access the component package in Storybook or equivalent]
2. [What the component package covers and when to reference it vs the Figma library]

**Other tools**
[Any other tools used in the workflow — token management, handoff tooling, contribution tracking]

---

#### How we work

This section covers the norms that are not written anywhere else — the conventions that experienced team members know and new members learn by collision.

**Using the system**
- The system is the starting point for all design work. Start with what exists before designing new.
- If a component exists in the system, use it. Do not modify it locally without a reason, and if you have a reason, it belongs in the contribution process.
- Tokens are [description of how tokens are applied in Figma — styles, variables, or both].

**When the system does not have what you need**
This happens and it is expected. When it does:
1. Check whether a composition of existing components covers the need
2. Check the documentation for patterns that address similar needs
3. Check whether another team has solved this problem — ask in [channel]
4. If the need is real and recurring, raise a contribution proposal

Do not build a local solution without exploring these steps first. Local solutions are the primary source of drift.

**Contribution norms**
[Brief description of how contributions work — reference the contribution-workflow documentation if it exists]

New designers typically contribute after their first [n weeks/months], once they have developed enough familiarity with the system to propose additions that fit its conventions. The expectation is not to contribute immediately, but to be aware of the process.

**Feedback and questions**
[Where to ask questions: Slack channel, office hours, designated contact]
[How to flag bugs or documentation gaps]
[How feedback on the system itself is collected — surveys, quarterly reviews, ad hoc]

---

#### Your first two weeks

A concrete path for the first two weeks — structured so early wins come before deep context.

**Week 1**
- [ ] Complete tooling setup (this guide, above)
- [ ] Explore the documentation platform: find the component you expect to use most
- [ ] Open a current design file and identify which design system components are in use
- [ ] Ask [name or team] to walk you through how a recent feature was built with the system — thirty minutes of context is worth hours of independent exploration

**Week 2**
- [ ] Design a small real-world task using only system components
- [ ] Identify one thing that felt unclear or missing, and note it for the contribution conversation
- [ ] Attend [design system office hours, review meeting, or equivalent — if applicable]

The goal by the end of week two is not mastery — it is orientation. You should know how to find what you need, who to ask when you cannot find it, and what to do when the system does not have what you need.

---

#### Essential reading list

Before diving into the system, these five resources will give you the most useful context in the least time. Each should take no more than fifteen minutes to read.

| # | Resource | What you'll learn | Where to find it |
|---|---|---|---|
| 1 | Component overview page | What exists in the system and what each component does | [Documentation platform URL] |
| 2 | Token reference (semantic tier) | The colour, spacing, and typography tokens you'll use daily | [Documentation platform URL] |
| 3 | Contribution workflow | How to propose additions when the system does not have what you need | [Link or location] |
| 4 | Naming conventions | How components and tokens are named, so you can find things | [Link or decision record] |
| 5 | Recent release notes | What changed recently — gives you a sense of the system's pace and direction | [Link or channel] |

Fill in the actual links before publishing this guide. If any of these resources do not exist yet, that is useful information — flag it for the system team.

#### Quick reference card

A wallet-sized reference for the first month:

```
[Design System Name] — Quick Reference

FIND COMPONENTS: [Documentation URL]
FIND TOKENS: [Token reference URL]
ASK QUESTIONS: [Slack channel]
REPORT BUGS: [Issue tracker URL]
PROPOSE ADDITIONS: [Contribution process URL]
OFFICE HOURS: [Day/time, if applicable]
SYSTEM OWNER: [Name or team]

KEY TOKENS:
  Primary action: color.action.primary
  Body text: color.content.primary
  Standard spacing: spacing.md
  Page margin: spacing.page

KEY SHORTCUTS:
  Figma library: [How to access]
  Storybook: [URL]
```

Adapt this template to the actual system. The quick reference card should be the single most-referenced artifact during the first month — it answers the "where do I..." questions that come up dozens of times.

---

#### Common questions

**The system does not have [component/pattern I need]. What do I do?**
Check the documentation and ask in [channel] before building locally. If the need is genuine and recurring, raise a contribution proposal.

**I found a bug in a component. How do I report it?**
[Specific process — issue tracker link, Slack channel, or equivalent]

**I want to modify a system component for my specific use case. Can I?**
Talk to [name or team] first. Local modifications to system components are the primary source of drift. In some cases a modification is appropriate; in others, the system needs to be updated rather than worked around.

**Who owns the design system?**
[Specific answer for this team — named owner, shared ownership model, or external team]

---

## Quality checks

- Tooling setup is step-by-step with no assumed knowledge
- All placeholders (URLs, contact names, channel names) are clearly marked for completion
- "When the system does not have what you need" section is honest and actionable
- First two weeks path starts with low-risk, high-orientation tasks — not deep dives
- Common questions are questions a new team member would actually ask, not FAQs written from the system team's perspective
- The guide can be followed alone without additional help — no unexplained references
- The guide is honest about the current state of the system, including known gaps
