---
name: governance-encoder
description: "Turn written governance rules into enforcement that runs: ESLint, Stylelint, dependency-cruiser and CODEOWNERS config traced to sources, plus GOVERNANCE.md for rules with no executable form. Triggers: governance as code, enforce our rules, lint our rules. Pipeline files: cicd-integration."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(npx eslint:*), Bash(npx stylelint:*), Bash(npx depcruise:*)
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/output-discipline.md
---

# Governance encoder

A skill for turning the governance rules a team has written down into enforcement that actually runs: linter rules, dependency boundaries, code ownership and CI checks, each traced to the document it came from. Rules with no executable form are written to a short governance page that says who checks them and when, so nothing is presented as automated when it isn't.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Most design system governance lives in documents: contribution guidelines in a wiki, naming conventions in a README, token rules in a Slack thread from a year ago. They are enforced by review, when a senior reviewer happens to notice. That model breaks at scale, and it breaks completely for coding agents, which never read the wiki.

The tools that enforce rules already exist. ESLint has a naming-convention rule. Stylelint can forbid raw values in colour properties. dependency-cruiser can stop an atom importing an organism. CODEOWNERS can require the system team's review on token files. A design system's governance-as-code is not a new rule engine; it is those tools, configured to the team's rules, with each rule pointing back at the sentence that justifies it. This skill writes that configuration. An earlier version wrote JSON rules that nothing executed and called them "enforced automatically"; that is exactly the gap this version closes.

## Boundaries

This skill encodes rules that exist. It doesn't decide what the rules should be (`decision-record` records that), write the CI workflow that runs the linters (`cicd-integration`), or audit compliance (`token-compliance`, `naming-audit`, `component-api-validator` do that). If the team has no written rules and can't state any, there is nothing to encode; say so and suggest `contribution-workflow`.

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`). This skill reads:
- `system.framework`, `system.styling`, `system.component_paths`, `system.tokens`
- `governance.severity_model` — how the team maps rule weight to linter levels (default: block-on-merge rules are `error`, review-prompting rules are `warn`)
- `governance.categories` — which rule categories to look for (default: all below)

## Step 1: Inventory the rules and the enforcement that already exists

Read before asking. Sources, in order:

- `CONTRIBUTING.md`, PR and issue templates, review checklists
- READMEs in the token and component directories, a style guide, decision records
- Existing lint config: `eslint.config.*` or `.eslintrc*`, `.stylelintrc*`, `.dependency-cruiser.*`, `CODEOWNERS`, `commitlint`, Changesets config
- `package.json` scripts and the CI workflow, for what already runs

For each rule found, one row:

| Rule (one sentence) | Source (path or URL) | Enforced today by | Executable form |
|---|---|---|---|
| Component export names are PascalCase | `CONTRIBUTING.md#naming` | PR review | ESLint `@typescript-eslint/naming-convention` |
| Component styles use semantic tokens, never primitives | `tokens/README.md` | nobody | Stylelint `declaration-property-value-disallowed-list` |
| Token file changes need the system team's review | `CONTRIBUTING.md#tokens` | habit | `CODEOWNERS` |
| New components need a design review before merge | wiki | nobody | none: GOVERNANCE.md |

Then ask only for what the files don't say: rules that live in the team's heads (each becomes a row with source `team`), rules that are written but nobody wants enforced, and how strict the team wants to be at first.

## Step 2: Map each rule to a tool

Use the executable form that already exists in the ecosystem. The table is the menu; pick per rule, per stack.

| Rule kind | Tool and rule | Notes |
|---|---|---|
| Component or file naming | ESLint `@typescript-eslint/naming-convention`; `unicorn/filename-case` for files | Vue: `vue/component-definition-name-casing` |
| Boolean prop prefixes, handler names | `@typescript-eslint/naming-convention` with a `typeProperty` selector and `prefix` | Partial: it can't tell a boolean prop from a boolean local. Mark it `warn` and say so |
| No raw colour, spacing or type values in styles | Stylelint `stylelint-declaration-strict-value` on the token-backed properties | Tailwind: `eslint-plugin-tailwindcss` `no-arbitrary-value` |
| No primitive tokens in component styles | Stylelint `declaration-property-value-disallowed-list` matching the primitive prefix (`/var\(--color-(blue|gray|red)-/`) | Take the prefix from the real token names |
| No local re-implementations or deep imports | ESLint `no-restricted-imports` (block `@system/*/src/*`, block copied-in paths) | |
| Layer boundaries (atoms don't import organisms) | `dependency-cruiser` rules, or `eslint-plugin-boundaries` | Only if the codebase has layers |
| Accessibility basics in JSX or templates | `eslint-plugin-jsx-a11y` (React), `eslint-plugin-vuejs-accessibility` (Vue) | Runtime a11y is `accessibility-per-component`'s job |
| Deprecated components and tokens must not be newly used | `@typescript-eslint/no-deprecated` on `@deprecated` JSDoc; `no-restricted-imports` for removed paths | Pairs with `deprecation-process` |
| Every exported component has docs | `eslint-plugin-jsdoc` `require-jsdoc` on exported components; a stories-present check is a script for `cicd-integration` | |
| Token, theme or contribution files need system-team review | `CODEOWNERS` | Requires branch protection or rulesets, which `cicd-integration` documents |
| Every release has a changelog entry | Changesets (`changeset status` in CI) or `commitlint` with conventional commits | Which one is the team's call; encode the one they use |
| Design review, accessibility audit, decision record before merge | No executable form. `GOVERNANCE.md` with owner and checkpoint; a PR template checkbox at most | Never claim these are automated |

## Step 3: Write the configuration

- **Edit the config files that exist; don't replace them.** Add rules to the existing ESLint or Stylelint config and keep the team's other settings. If no config exists for a tool, write one and say it's new; don't add a tool the team hasn't chosen without asking.
- **Trace every rule.** Above each added rule, a comment: `// GOV: <rule sentence> — source: CONTRIBUTING.md#naming`. In JSON configs that can't carry comments, put the trace in `GOVERNANCE.md` next to the rule id.
- **Real names.** The primitive-token pattern, the package name in `no-restricted-imports`, the paths in `CODEOWNERS` all come from the repository, not from the example in Step 2.
- **Severity from the team's model.** First encoding usually ships as `warn`; Step 5 says when a rule is ready to become `error`.
- **`GOVERNANCE.md`** (in `docs/` or beside `CONTRIBUTING.md`): one table of every rule from Step 1 with its source, its tool and rule id or "manual", who checks it and at which point (PR review, release, quarterly), and the exception route the team stated. Then a "Proposed, not yet policy" list for anything you suggested that no source supports, each with a one-line reason, for the team to accept or delete. An exception process is written only if the team has one; don't invent approval levels.

## Step 4: Calibrate against the codebase

Run each tool in report mode against the repository (`npx eslint . --format json`, `npx stylelint "**/*.css" --formatter json`, `npx depcruise src`) and count current violations per added rule. Report the counts. A rule that fires four hundred times on day one ships as `warn` with a note that it needs a cleanup pass (a `token-compliance` run gives the list); a rule that fires zero times may be misconfigured, so confirm it fires on a known-bad line before trusting the zero, per the empty-result rule in the output-discipline note. Don't fix violations in this run.

## Step 5: Summarise in chat

- **Headline:** rules encoded (by tool), rules written to `GOVERNANCE.md` as manual, rules proposed
- **Files:** every config written or edited, with the rule count added to each
- **Calibration:** violations per rule today, and which rules are safe to promote to `error`
- **Next:** `cicd-integration` to run these in CI and document branch protection; `token-compliance` for the cleanup list; `decision-record` for any rule the team argued about
- **Scope:** the block from the output-discipline note: sources inspected, sources not reached (wikis, Slack, people), and the note that the encoded set is what was found, not everything the team believes

## Quality checks

- Every added lint rule carries a trace comment with a source path or `team`; no rule exists in the config that isn't in the Step 1 table
- No rule is described as automated unless a tool in the config runs it; process gates live in `GOVERNANCE.md` with a human checkpoint
- Token prefixes, package names and paths in the config are the repository's, not the examples'
- Existing config files were edited, not overwritten, and the summary says what was added to each
- Every rule was run in report mode and its current violation count is in the summary, with a known-bad probe confirming any zero
- Proposed rules are in their own list with a reason each, and none is in a config file
- The output ends with a Scope block
