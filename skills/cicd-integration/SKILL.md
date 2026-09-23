---
name: cicd-integration
description: "Generate CI pipeline files and check scripts (GitHub Actions, GitLab, CircleCI, Bitbucket) that automate design system checks: token validation, hardcoded values, a11y scans, visual regression, bundle size. Trigger: set up CI, quality gates, automate these checks. Not for running an audit."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*), Bash(sort:*), Bash(tail:*), Bash(wc:*), Bash(git diff:*)
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/design-to-code-contract.md
---

# CI/CD Integration

A skill for generating pipeline configurations that automate the quality checks Design System Ops skills perform manually. This bridges the gap between "here are the problems the audit found" and "these problems can never recur because the pipeline catches them."

**Output type:** File creation. This skill produces pipeline configuration files (YAML), scripts, and documentation. It does not execute pipelines — it generates the configuration that teams add to their repository.

---

## Before you begin: verify references

Before doing anything else, confirm that every file listed in this skill's frontmatter `references:` field exists at its relative path from this SKILL.md. If any are missing, stop — the install is incomplete. This usually means a third-party installer (for example `npx skills install`) flattened the skill into a standalone folder and dropped the repo-root `knowledge-notes/` directory this skill depends on. Tell the user to reinstall using a supported method from `1-INSTALL.md` (git clone, or the `.plugin` bundle in Cowork) and to run `verify-install.sh` from the install root to confirm the fix. Only proceed without the references if the user explicitly says to — and if they do, state clearly in your output that it was produced in degraded mode without the pack's reference material.

## Why this exists

Every audit skill in Design System Ops finds problems. Some of those problems should never have reached a human reviewer because they are mechanically detectable: a hardcoded hex value in a component file, a token alias that references a non-existent token, a component export missing from the barrel file, an accessibility violation that an automated scanner would catch.

CI/CD Integration converts audit findings into automated pipeline checks. The goal is not to replace the audit skills — those handle nuance, context, and cross-skill synthesis that pipelines cannot. The goal is to automate the mechanical subset so that audits focus on the problems only humans can evaluate.

---

## Configuration

Check for `.ds-ops-config.yml` in the project root:

```yaml
cicd:
  platform: "github-actions"         # github-actions, gitlab-ci, circleci, bitbucket
  package_manager: "npm"              # npm, yarn, pnpm
  node_version: "22"                  # Node.js version (22 or 24; both LTS)
  test_framework: "jest"              # jest, vitest, playwright
  component_library_path: "packages/components"
  token_path: "packages/tokens"
  monorepo: true                      # Whether the project uses a monorepo structure
  triggers:
    - "push to main"
    - "pull request to main"
```

If no configuration exists, ask for:
1. CI/CD platform (default: GitHub Actions)
2. Package manager (default: npm)
3. Whether the project is a monorepo
4. Paths to token files and component files

---

## Step 0: Assess what to automate

Before generating any pipeline configuration, determine which checks are worth automating. Not everything should be in CI.

### Automation decision matrix

| Check type | Automate in CI? | Why |
|---|---|---|
| Token naming violations | Yes | Mechanical — regex patterns, no judgment needed |
| Token circular references | Yes | Graph traversal — computers are better at this |
| Hardcoded colour values | Yes | grep/AST — exact match detection |
| Component prop type checking | Yes | TypeScript/Flow already does this |
| Accessibility (automated subset) | Yes | axe-core catches the machine-detectable subset of WCAG issues; keyboard and screen reader checks stay manual |
| Visual regression | Yes | Pixel comparison catches unintended changes |
| Component export completeness | Yes | AST/barrel file check |
| Bundle size tracking | Yes | Byte comparison — pure measurement |
| Token coverage gaps | Partial | Can check primitive→semantic mapping exists, cannot judge if mappings are correct |
| Component API consistency | Partial | Can lint prop naming patterns, cannot judge API design quality |
| Documentation completeness | Partial | Can check if docs exist, cannot judge if they are good |
| Cross-component pattern compliance | No | Requires too much context and judgment |
| Naming convention quality | No | Conventions need human validation first, then automation |
| Usage guideline adherence | No | Requires consuming-app context that CI rarely has |

### Rule of thumb
If the skill's finding includes a specific, unambiguous rule (e.g., "tokens must use kebab-case", "no hex values outside token files"), it can be automated. If the finding requires judgment (e.g., "this token naming could be clearer"), it cannot.

---

## Step 1: Map audit findings to pipeline checks

For each audit finding category, determine the automated check:

### Token checks

| Finding category | Pipeline check | Tool |
|---|---|---|
| Naming violations | Lint token names against convention regex | Custom script or Style Dictionary validator |
| Circular references | Build-time alias resolution check | Style Dictionary build (fails on circular refs) |
| Orphaned tokens | Cross-reference token definitions with usage in component files | Custom script: grep token names across component source. Warn only — it can't see tokens consumed outside the repo (product apps, native platforms, Figma), so an "orphan" may be in use |
| Missing semantic tier | Check that every component token reference resolves through a semantic alias | Custom script or Style Dictionary referencing |
| DTCG format compliance | Validate token files against DTCG schema | JSON Schema validation |

### Component checks

| Finding category | Pipeline check | Tool |
|---|---|---|
| Export completeness | Verify barrel file exports match component directories | Custom script: compare fs listing with exports |
| Prop type safety | TypeScript strict mode compilation | `tsc --noEmit` |
| Accessibility | Run axe-core on rendered components | `@axe-core/cli`, `jest-axe`, or Playwright + axe |
| Visual regression | Screenshot comparison against baselines | Chromatic, Percy, Playwright visual comparisons |
| Bundle size | Track and gate on component bundle sizes | `size-limit`, `bundlesize`, or custom webpack analysis |

### Documentation checks

| Finding category | Pipeline check | Tool |
|---|---|---|
| Existence | Check that each component directory has a README or docs file | Custom script: file existence check |
| Prop documentation | Check that JSDoc/TSDoc exists for all exported props | `eslint-plugin-jsdoc` or custom TSDoc validator |
| Storybook stories | Check that each component has at least one story file | Custom script: file pattern match |

---

## Step 2: Generate the pipeline configuration

### GitHub Actions

Produce a workflow file: `.github/workflows/design-system-checks.yml`

Structure:

```yaml
name: Design System Quality Checks

# No `paths:` filter here: if these jobs are required checks, a PR that
# doesn't touch the paths would leave them pending forever. The `changes`
# job decides what to run instead; skipped jobs count as passing.
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: read   # lets the path filter list PR files

concurrency:
  group: ds-checks-${{ github.ref }}
  cancel-in-progress: true

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      tokens: ${{ steps.filter.outputs.tokens }}
      components: ${{ steps.filter.outputs.components }}
    steps:
      - uses: actions/checkout@v7
      - uses: dorny/paths-filter@v4
        id: filter
        with:
          filters: |
            tokens:
              - 'packages/tokens/**'
            components:
              - 'packages/components/**'
              - 'packages/tokens/**'

  token-validation:
    name: Token Validation
    needs: changes
    if: needs.changes.outputs.tokens == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: Validate token naming
        run: node scripts/ds-checks/validate-token-names.js
      - name: Check for circular references
        run: npx style-dictionary build --config tokens.config.js
      - name: Detect orphaned tokens (warn only)
        run: node scripts/ds-checks/find-orphaned-tokens.js
      - name: Validate DTCG format
        run: node scripts/ds-checks/validate-dtcg-schema.js

  component-validation:
    name: Component Validation
    needs: [changes, token-validation]
    if: ${{ !failure() && !cancelled() && needs.changes.outputs.components == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: TypeScript compilation
        run: npx tsc --noEmit
      - name: Check export completeness
        run: node scripts/ds-checks/verify-exports.js
      - name: Accessibility scan
        run: npm run test:a11y      # prerequisite — see Step 3
      - name: Bundle size check
        run: npx size-limit         # prerequisite — see Step 3

  documentation-validation:
    name: Documentation Validation
    needs: changes
    if: needs.changes.outputs.components == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: Check component docs exist
        run: node scripts/ds-checks/check-docs-exist.js
      - name: Verify Storybook stories exist
        run: node scripts/ds-checks/check-stories-exist.js

  visual-regression:
    name: Visual Regression
    needs: changes
    if: github.event_name == 'pull_request' && needs.changes.outputs.components == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0          # Chromatic needs git history for baselines
      - uses: actions/setup-node@v7
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: Build Storybook
        run: npx storybook build --output-dir storybook-static
      - name: Run visual regression
        # Reuse the build above rather than letting Chromatic build Storybook again
        run: npx chromatic --project-token=${{ secrets.CHROMATIC_PROJECT_TOKEN }} --storybook-build-dir=storybook-static
```

Pin each action to its current major when you generate the file; the majors above were current when this skill was written. Use the Node version from `cicd.node_version` (22 or 24). `dorny/paths-filter` is a third-party action; if the team's policy disallows those, replace the `changes` job with a `git diff --name-only` step that sets the same outputs.

**Blocking merges needs branch protection.** A failing job only blocks a merge if the repository requires it. Tell the user to add the job names as required status checks under branch protection or a ruleset on `main`; the pipeline can't enforce this itself.

### GitLab CI

Produce `.gitlab-ci.yml`. Minimal skeleton — mirror the full check list from the GitHub workflow:

```yaml
default:
  image: node:22
  cache:
    key:
      files: [package-lock.json]
    paths: [.npm/]
  before_script:
    - npm ci --cache .npm --prefer-offline

stages: [validate, visual]

token-validation:
  stage: validate
  script:
    - node scripts/ds-checks/validate-token-names.js
    - npx style-dictionary build --config tokens.config.js
    - node scripts/ds-checks/validate-dtcg-schema.js
    - node scripts/ds-checks/find-orphaned-tokens.js
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes: [packages/tokens/**/*]

component-validation:
  stage: validate
  script:
    - npx tsc --noEmit
    - node scripts/ds-checks/verify-exports.js
    - npm run test:a11y
    - npx size-limit
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes: [packages/components/**/*, packages/tokens/**/*]

visual-regression:
  stage: visual
  script:
    - npx storybook build --output-dir storybook-static
    - npx chromatic --project-token="$CHROMATIC_PROJECT_TOKEN" --storybook-build-dir=storybook-static
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

Set `CHROMATIC_PROJECT_TOKEN` as a masked CI/CD variable. To block merges, enable "Pipelines must succeed" in the project's merge request settings.

### CircleCI

Produce `.circleci/config.yml`:

```yaml
version: 2.1

executors:
  node:
    docker:
      - image: cimg/node:22.23   # any current 22.x or 24.x tag

commands:
  install:
    steps:
      - checkout
      - restore_cache:
          keys:
            - npm-{{ checksum "package-lock.json" }}
      - run: npm ci
      - save_cache:
          key: npm-{{ checksum "package-lock.json" }}
          paths: [~/.npm]

jobs:
  token-validation:
    executor: node
    steps:
      - install
      - run: node scripts/ds-checks/validate-token-names.js
      - run: npx style-dictionary build --config tokens.config.js
      - run: node scripts/ds-checks/validate-dtcg-schema.js
      - run: node scripts/ds-checks/find-orphaned-tokens.js
  component-validation:
    executor: node
    steps:
      - install
      - run: npx tsc --noEmit
      - run: node scripts/ds-checks/verify-exports.js
      - run: npm run test:a11y
      - run: npx size-limit

workflows:
  design-system-checks:
    jobs:
      - token-validation
      - component-validation:
          requires: [token-validation]
```

CircleCI has no built-in path filtering; add it with the path-filtering orb and dynamic config only if the run time matters. To block merges, mark the jobs as required status checks in GitHub or Bitbucket.

### Bitbucket Pipelines

Produce `bitbucket-pipelines.yml`:

```yaml
image: node:22

definitions:
  steps:
    - step: &tokens
        name: Token validation
        caches: [node]
        script:
          - npm ci
          - node scripts/ds-checks/validate-token-names.js
          - npx style-dictionary build --config tokens.config.js
          - node scripts/ds-checks/validate-dtcg-schema.js
          - node scripts/ds-checks/find-orphaned-tokens.js
    - step: &components
        name: Component validation
        caches: [node]
        script:
          - npm ci
          - npx tsc --noEmit
          - node scripts/ds-checks/verify-exports.js
          - npm run test:a11y
          - npx size-limit

pipelines:
  pull-requests:
    '**':
      - parallel:
          - step: *tokens
          - step: *components
  branches:
    main:
      - parallel:
          - step: *tokens
          - step: *components
```

Add a `condition: changesets: includePaths:` block to a step to scope it by path. To block merges, add a merge check requiring passing builds (a Premium feature on Bitbucket Cloud).

---

## Step 3: Generate the helper scripts

Each pipeline check references a script. Generate the scripts in `scripts/ds-checks/`:

### `validate-token-names.js`

```javascript
/**
 * Validates token names against the configured naming convention.
 * Exits with code 1 if violations are found.
 *
 * Generated by Design System Ops — cicd-integration
 */

const fs = require('fs');
const path = require('path');

// Configuration — adjust these to match your conventions
// A segment is lowercase letters and digits, optionally hyphenated:
// spacing.4, font-size.base, color.blue.500, color.action.primary-hover,
// button.background.hover all pass. 2–5 segments.
const SEGMENT = '[a-z0-9]+(?:-[a-z0-9]+)*';
const TOKEN_NAME = new RegExp(`^${SEGMENT}(?:\\.${SEGMENT}){1,4}$`);

// Tier comes from where a token is defined (file or set), not from how many
// segments its name has — spacing.4 and button.background.default can't be
// told apart by shape alone.
const TIER_BY_PATH = {
  primitive: 'primitives/',
  semantic: 'semantic/',
  component: 'component/',
};

// Token file path — adjust to your project
const TOKEN_DIR = process.env.TOKEN_DIR || 'packages/tokens/src';

// [Full implementation: recursively read token files, assign each token
//  a tier from TIER_BY_PATH, validate its name against TOKEN_NAME and any
//  tier-specific rules, collect violations, read the threshold for
//  `token-naming` from .ds-ops/quality-gates.yml, output violations, and
//  exit 1 only if the count exceeds the threshold and block_merge is true]
```

Provide complete, working implementations for each script. Include:
- Clear comments explaining what the script checks
- Configurable paths and patterns at the top of each file
- Thresholds read from `.ds-ops/quality-gates.yml` (Step 4) via a shared helper, not hardcoded
- Exit codes: 1 only when a gate with `block_merge: true` is exceeded; otherwise 0, printing warnings (on GitHub, as `::warning::` lines so they show on the PR)
- Human-readable output: which files, which violations, what to fix
- Provenance comment: "Generated by Design System Ops — cicd-integration"

### Scripts to generate

1. `validate-token-names.js` — Regex-based token name validation
2. `find-orphaned-tokens.js` — Cross-reference token definitions with component usage
3. `validate-dtcg-schema.js` — JSON Schema validation for DTCG format
4. `verify-exports.js` — Compare directory listing with barrel file exports
5. `check-docs-exist.js` — Verify documentation files exist for each component
6. `check-stories-exist.js` — Verify Storybook story files exist for each component
7. `read-gates.js` — Shared helper that loads `.ds-ops/quality-gates.yml` and returns the threshold and `block_merge` flag for a gate

### Prerequisites the pipeline assumes

Two steps call tools the scripts above don't create. Generate them, or list them as prerequisites the team must add before the pipeline goes green:

- **`test:a11y` script** in `package.json` — for example `"test:a11y": "vitest run --project a11y"` with `jest-axe`/`vitest-axe` tests, or `"test:a11y": "test-storybook"` with the Storybook test-runner and axe. Generate one example test per component type found.
- **`size-limit` config** — a `.size-limit.json` listing each entry point with a `limit`, plus `size-limit` and its preset (e.g. `@size-limit/preset-small-lib`) as dev dependencies.

---

## Step 4: Generate a quality gate configuration

Produce a quality gate definition that the pipeline enforces on pull requests:

The `scripts/ds-checks/` scripts read this file through `read-gates.js`. Checks run by other tools (Style Dictionary, axe, size-limit, Chromatic) are gated by their own exit codes and config — set their thresholds there, and say so in `PIPELINE.md`.

```yaml
# .ds-ops/quality-gates.yml
# Quality gates for design system pull requests, read by scripts/ds-checks/
# Adjust thresholds based on your system's maturity

gates:
  token-naming:
    threshold: 0          # Zero tolerance for naming violations
    block_merge: true
    message: "Token naming violations must be fixed before merge"

  orphaned-tokens:
    threshold: 5          # Allow some orphans during migration periods
    block_merge: false    # Warn only: tokens consumed outside this repo look orphaned
    message: "Possibly orphaned tokens — check external consumers before removing"

  exports:
    threshold: 0
    block_merge: true
    message: "Every component directory must be exported from the package entry point"

  docs-and-stories:
    threshold: 0
    block_merge: false
    message: "Components without docs or stories detected"
```

---

## Step 5: Generate documentation

Produce a `PIPELINE.md` file that explains:

1. **What each check does** — in plain language a product manager would understand
2. **How to add a new check** — step-by-step for an engineer
3. **How to adjust thresholds** — where the configuration lives and what each threshold means
4. **What to do when a check fails** — troubleshooting guide for each check type
5. **How this relates to Design System Ops audits** — which audit findings each check automates

---

## Adaptation by platform

### For teams using Figma MCP
Add a step that auto-pulls Figma variable values and compares them against token file definitions. This catches design-code drift at the CI level.

### For teams using Style Dictionary
The token validation steps should use Style Dictionary's built-in validation rather than custom scripts. Generate a Style Dictionary config that enforces naming conventions and reference integrity.

### For teams using Storybook
Integrate the visual regression step with Storybook's built-in visual testing or Chromatic. Generate test-runner configuration for accessibility checks within stories.

### For monorepo projects
Scope jobs by changed paths inside the pipeline (the `changes` job above), not with workflow-level `paths:` filters, so required checks never sit pending. Token changes run token checks; component changes run component checks. Use job dependencies so that token validation runs before component validation (since components depend on tokens).

---

## Quality checks

- Pipeline configuration is valid YAML that passes the platform's schema validation
- All referenced scripts exist and are executable, and every tool a step calls (`test:a11y`, `size-limit`) is either generated or listed as a prerequisite
- Actions are pinned to current majors and Node is 22 or 24
- Gate thresholds come from `.ds-ops/quality-gates.yml`, and the user is told to enable branch protection for blocking checks
- Scripts have clear error messages that explain what went wrong and how to fix it
- Quality gate thresholds are reasonable defaults (not so strict they block everything, not so loose they catch nothing)
- Documentation explains every check in language a non-engineer can understand
- Provenance marker present in all generated files
- Pipeline configuration respects monorepo structure if applicable
- No secrets or credentials are hardcoded — all sensitive values use environment variables or secrets management
