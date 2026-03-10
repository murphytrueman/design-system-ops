---
name: cicd-integration
description: "Generate CI/CD pipeline configurations that automate design system quality checks — token validation, component linting, visual regression, accessibility scanning, and release gating. Produces ready-to-use pipeline files for GitHub Actions, GitLab CI, CircleCI, or Bitbucket Pipelines, configured to enforce the standards that audit skills check manually. Trigger when someone says: set up CI for the design system, automate these checks, add pipeline for tokens, create GitHub Action for design system, CI/CD for components, automate the release process, continuous integration for design system, how do I automate what the audit found, quality gates in CI, or anything about automating design system quality checks in a pipeline. Do NOT trigger for running a manual audit — use the specific audit skill for that. Do NOT trigger for generating a release checklist — use change-communication for that."
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/design-to-code-contract.md
---

# CI/CD Integration

A skill for generating pipeline configurations that automate the quality checks Design System Ops skills perform manually. This bridges the gap between "here are the problems the audit found" and "these problems can never recur because the pipeline catches them."

**Output type:** File creation. This skill produces pipeline configuration files (YAML), scripts, and documentation. It does not execute pipelines — it generates the configuration that teams add to their repository.

---

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
  node_version: "20"                  # Node.js version
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
| Accessibility (automated subset) | Yes | axe-core catches 30–40% of WCAG violations |
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
| Orphaned tokens | Cross-reference token definitions with usage in component files | Custom script: grep token names across component source |
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

on:
  push:
    branches: [main]
    paths:
      - 'packages/tokens/**'
      - 'packages/components/**'
  pull_request:
    branches: [main]
    paths:
      - 'packages/tokens/**'
      - 'packages/components/**'

concurrency:
  group: ds-checks-${{ github.ref }}
  cancel-in-progress: true

jobs:
  token-validation:
    name: Token Validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: Validate token naming
        run: node scripts/ds-checks/validate-token-names.js
      - name: Check for circular references
        run: npx style-dictionary build --config tokens.config.js
      - name: Detect orphaned tokens
        run: node scripts/ds-checks/find-orphaned-tokens.js
      - name: Validate DTCG format
        run: node scripts/ds-checks/validate-dtcg-schema.js

  component-validation:
    name: Component Validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: TypeScript compilation
        run: npx tsc --noEmit
      - name: Check export completeness
        run: node scripts/ds-checks/verify-exports.js
      - name: Accessibility scan
        run: npm run test:a11y
      - name: Bundle size check
        run: npx size-limit

  documentation-validation:
    name: Documentation Validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: Check component docs exist
        run: node scripts/ds-checks/check-docs-exist.js
      - name: Verify Storybook stories exist
        run: node scripts/ds-checks/check-stories-exist.js

  visual-regression:
    name: Visual Regression
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: Build Storybook
        run: npx storybook build
      - name: Run visual regression
        run: npx chromatic --project-token=${{ secrets.CHROMATIC_TOKEN }}
```

### GitLab CI

Produce `.gitlab-ci.yml` with equivalent stages:

```yaml
stages:
  - validate-tokens
  - validate-components
  - validate-docs
  - visual-regression

# [equivalent job definitions]
```

### CircleCI

Produce `.circleci/config.yml` with orbs and workflows.

### Bitbucket Pipelines

Produce `bitbucket-pipelines.yml` with pipeline definitions.

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
const CONVENTIONS = {
  primitives: /^[a-z]+\.[a-z]+\.\d+$/,         // e.g., color.blue.500
  semantic: /^[a-z]+\.[a-z]+\.[a-z]+$/,          // e.g., color.action.primary
  component: /^[a-z]+\.[a-z]+\.[a-z]+\.[a-z]+$/, // e.g., button.background.default
};

// Token file path — adjust to your project
const TOKEN_DIR = process.env.TOKEN_DIR || 'packages/tokens/src';

// [Full implementation: recursively read token files, validate each
//  token name against the appropriate convention regex, collect
//  violations, output them, exit with appropriate code]
```

Provide complete, working implementations for each script. Include:
- Clear comments explaining what the script checks
- Configurable paths and patterns at the top of each file
- Exit codes: 0 for pass, 1 for fail
- Human-readable output: which files, which violations, what to fix
- Provenance comment: "Generated by Design System Ops — cicd-integration"

### Scripts to generate

1. `validate-token-names.js` — Regex-based token name validation
2. `find-orphaned-tokens.js` — Cross-reference token definitions with component usage
3. `validate-dtcg-schema.js` — JSON Schema validation for DTCG format
4. `verify-exports.js` — Compare directory listing with barrel file exports
5. `check-docs-exist.js` — Verify documentation files exist for each component
6. `check-stories-exist.js` — Verify Storybook story files exist for each component

---

## Step 4: Generate a quality gate configuration

Produce a quality gate definition that the pipeline enforces on pull requests:

```yaml
# .ds-ops/quality-gates.yml
# Quality gates for design system pull requests
# Adjust thresholds based on your system's maturity

gates:
  token-naming:
    threshold: 0          # Zero tolerance for naming violations
    block_merge: true
    message: "Token naming violations must be fixed before merge"

  circular-references:
    threshold: 0
    block_merge: true
    message: "Circular token references are not allowed"

  orphaned-tokens:
    threshold: 5          # Allow some orphans during migration periods
    block_merge: false     # Warn but don't block
    message: "New orphaned tokens detected — consider cleanup"

  accessibility:
    threshold: 0          # Zero critical/serious axe violations
    block_merge: true
    message: "Accessibility violations must be resolved"

  bundle-size:
    max_increase_kb: 5    # Allow up to 5KB increase per component
    block_merge: true
    message: "Component bundle size increased beyond threshold"

  visual-regression:
    max_changed_stories: 0 # Any visual change requires review
    block_merge: false      # Require manual approval, don't auto-block
    message: "Visual changes detected — review required"
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
Add path-scoped triggers so that token changes only run token checks, and component changes only run component checks. Use job dependencies so that token validation runs before component validation (since components depend on tokens).

---

## Quality checks

- Pipeline configuration is valid YAML that passes the platform's schema validation
- All referenced scripts exist and are executable
- Scripts have clear error messages that explain what went wrong and how to fix it
- Quality gate thresholds are reasonable defaults (not so strict they block everything, not so loose they catch nothing)
- Documentation explains every check in language a non-engineer can understand
- Provenance marker present in all generated files
- Pipeline configuration respects monorepo structure if applicable
- No secrets or credentials are hardcoded — all sensitive values use environment variables or secrets management
