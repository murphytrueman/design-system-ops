---
name: onboarding
description: "Onboarding guide for a designer or engineer joining a team that uses the design system, grounded in the repo and Figma library rather than a template. Triggers: onboard a new designer, onboard a new engineer, getting-started guide, first week with the system, developer or designer onboarding."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*)
references:
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/output-discipline.md
---

# Onboarding

A skill for writing an onboarding guide for someone joining a team that consumes the design system. One guide, with a shared core and a section for the reader's role: designer, engineer, or both. Every fact in it comes from the repository, the Figma library, or the team; anything else is marked `[confirm: …]` and listed at the top so nobody publishes a guess.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Onboarding docs fail in one of two ways. Written from the system team's side, they assume context and hand the newcomer a reading list instead of a path. Written from a template, they describe a generic design system rather than this one, so the reader learns nothing they couldn't have guessed. Designers and engineers also arrive at the system from opposite sides: a designer composes with a library (Figma, Storybook); an engineer consumes an API (imports, props, types). The drift both create starts in week one, when the system is "close but not quite right" and someone builds around it. A guide that is specific, honest about gaps, and clear about what to do when the system doesn't have something is the highest-leverage adoption work a team can do.

## Step 0: Read before asking

Gather the facts from where they already live. Ask the team only for what these can't answer.

**Config.** `.ds-ops-config.yml`: `system.name`, `system.framework`, `system.styling`, `integrations.figma.file_key`, `integrations.npm.package_name`.

**Repository.** `package.json` (package name, `exports`, peer dependencies, scripts for build, test, lint, storybook), the token source or build output (CSS custom properties, JS token modules, Tailwind theme, Sass), exported TypeScript types, the test setup (Jest or Vitest, Chromatic or Percy, axe or similar), `CONTRIBUTING.md`, `CHANGELOG.md`, a docs site or Storybook URL in the README.

**Figma.** If a Figma MCP is connected and a file key is known: the library's page names, the variable collections and their modes, whether tokens are styles or variables, and the published component set names. If not, ask for the library link and mark the rest `[confirm]`.

**Existing onboarding.** A README section, a wiki page, a Notion doc. If one exists, this skill updates it rather than starting over: keep what is accurate, replace what the files contradict, and say what changed.

Record which facts came from files and which from the team. Anything neither confirms goes in as `[confirm: …]`.

## Step 1: Ask the team for the rest

- Who the reader is: a designer, an engineer, or a guide with both sections
- Team contacts: channel, primary maintainer, office hours if any
- The contribution route: how someone proposes a fix or an addition, and roughly how long it takes
- Policies that are decisions, not facts in the repo: the accessibility guarantee the system makes and against which standard, how often consumers are expected to update, what the team's rule on local wrappers and overrides is, whether Figma library updates are pushed or pulled
- Known rough edges: documented workarounds, components that are mid-migration, docs that lag

Don't fill a policy in from good practice. "Update monthly" is a policy the team sets, not a fact the skill knows. Leave it as `[confirm: update cadence]`.

## Step 2: Write the guide

Use this order. Each section stands alone; no forward references. Write examples in the detected stack (Vue single-file components, Web Components, Vitest and so on), using the real package name, exports, token names and Figma library names.

```
# Getting started with [System name]

**For:** [designers / engineers / both] joining [team]
**Last updated:** [today]
**Questions:** [channel or contact]
**Still to confirm:** [every `[confirm: …]` left in the guide, or "none"]
```

### Shared core (every reader)

**What [System name] is.** One paragraph from the reader's side: what the system covers (components, tokens, patterns, docs), what it deliberately doesn't (product-specific patterns, local conventions), who maintains it, and where it lives (Figma library, docs URL, package name). Be honest about the current state: "the component library is mature; the docs are catching up in [area]" is more useful than "comprehensive".

**How we work.**
- Start with what exists. If the system has it, use it.
- Tokens are decisions the system owns. In Figma they are [styles / variables, from Step 0]; in code they are [the token access pattern, from Step 0]. Never hardcode a value the system has a token for; use semantic tokens, not primitives, so theming keeps working.
- When the system doesn't have what you need: check the docs, ask in [channel], check whether another team has solved it, then raise it through [the contribution route]. Don't build a local version first; local versions are where drift starts. `[confirm: the team's rule for temporary workarounds, if any]`

**Your first two weeks.** Checkbox tasks that start with orientation and end with one real piece of work using only system parts. Include one human task: pair with [name] on a recent feature built with the system.

**Common questions.** Four or five the reader will actually ask: the system doesn't have X; I found a bug; can I modify a component; who owns this; how do I keep up with changes. Answers come from Step 0 and Step 1, or are `[confirm]`.

### Designer section

**Figma setup.** How to enable the library, how to confirm it's on, the page structure and what lives where, the plugins the team uses (names and links), and how tokens appear (styles, variables, modes) with the names from Step 0.

**Documentation.** The docs platform URL, how it's organised, and any known gaps.

**Handoff.** What engineers need from a design file (the states, the tokens named, the spec fields the design-to-code contract lists) and where handoff happens.

**Common mistakes.** Detaching instances to tweak them; using a primitive colour style because it "looks right"; designing a state the component doesn't have without flagging it; local components that duplicate library ones. Each with what to do instead.

### Engineer section

**Install and render.** The install command with the real package name, the real style or theme import from `exports`, and a first render. Copy-pasteable; placeholders only in brackets outside the command.

**Using components.** The import pattern, one complete example in the detected framework, and where the prop docs are (Storybook or docs URL). Types, if the package exports them.

**Using tokens.** The access pattern from Step 0 with real token names, and one wrong/right pair:

```
// Wrong: hardcoded
padding: 16px; color: #222;
// Right: the system's tokens
padding: var(--[real-spacing-token]); color: var(--[real-text-token]);
```

**Testing.** Render the real components in tests; don't mock the design system, because mocking replaces the roles, labels and behaviour your queries depend on. The visual-regression tool and how a diff is reviewed, from Step 0. The accessibility guarantee the system makes and what remains the consumer's job (heading order, alt text, focus management of the composition), from Step 1.

**Common mistakes.** Wrapping components in local styled wrappers; hardcoding values; reaching for primitives; copying component source; `!important` overrides; pinning a version indefinitely (`[confirm: the team's update cadence]`); building a variant locally instead of asking. Each with what to do instead.

**Quick reference.** Install, import, token access, docs URL, channel, contribution route, in ten lines.

## Small-system note

Fewer than five components: name every component in "What the system is", make "what the system covers and what it doesn't" the most prominent section, shorten the first two weeks to a first week with three or four tasks, drop the quick reference, and lean on people: "ask [name] to pair with you on your first task" beats "explore the docs" when the docs have three pages.

## Quality checks

- Every install command, import path, token name, library name and URL comes from the repository, Figma or the team; none is invented, and the "Still to confirm" line lists every `[confirm]`
- Policies (update cadence, wrapper rule, accessibility guarantee) are the team's, or marked `[confirm]`; the guide never states good practice as the team's policy
- Examples are in the detected stack, complete, and render something
- The engineer section tells the reader to render real components in tests, not to mock them
- Each role section names concrete mistakes with what to do instead, not generic advice
- The guide is honest about the system's current state and known gaps
- If an existing guide was updated, the summary says what was kept, replaced and why
