---
name: codemod-generator
description: "Generate codemods (automated code transformation scripts) for design system migrations — token renames, component API changes, prop deprecations, and import path updates. Produces ready-to-run jscodeshift or custom AST transform scripts that safely apply changes across consuming codebases. Trigger when someone says: generate a codemod, automate this migration, write a transform script, bulk rename tokens, auto-migrate components, jscodeshift for this change, create a migration script, update all imports, rename this prop everywhere, or anything about automating code changes across consumers of a design system. Do NOT trigger for planning the deprecation process — use deprecation-process for that. Do NOT trigger for writing release notes about a change — use change-communication for that."
references:
  - references/component-governance.md
  - references/design-to-code-contract.md
---

# Codemod Generator

A skill for producing automated code transformation scripts that apply design system changes across consuming codebases. When a token is renamed, a component API changes, or an import path moves, this skill generates the script that makes the change everywhere — safely, consistently, and with a dry-run option.

**Output type:** File creation. This skill produces executable transformation scripts (JavaScript/TypeScript) and documentation. It does not execute the transformations — it generates scripts that teams run in their own codebases.

---

## Why this exists

A design system change without a migration path is a breaking promise. When you rename `color.brand.primary` to `color.action.primary`, every consumer who uses that token has to find and replace it — manually, across every file, hoping they do not miss one. When you change a `Button` prop from `type` to `variant`, every consuming team has to grep their codebase, update every instance, and test every page.

This manual work is where migration debt accumulates. Teams delay adopting the new version because the upgrade cost is too high. The system fragments — some teams on v3, some on v4, some on a custom fork they stopped updating two versions ago.

Codemods fix this by automating the mechanical part of migration. A codemod is a script that reads source code, applies a specific transformation, and writes the result — safely, deterministically, and across thousands of files in seconds.

This skill generates those scripts. It does not replace the deprecation plan or the migration guide — those are context-heavy, human-judgment outputs. It replaces the mechanical labour of applying the changes.

---

## Configuration

Check for `.ds-ops-config.yml` in the project root:

```yaml
codemods:
  language: "typescript"              # typescript, javascript, or both
  transform_engine: "jscodeshift"     # jscodeshift, ts-morph, or custom
  output_directory: "codemods/"
  test_framework: "jest"              # jest or vitest for codemod tests
  style_dictionary_format: false      # If tokens use Style Dictionary format
  css_custom_properties: true         # If tokens are consumed as CSS custom properties
```

If no configuration exists, use these defaults:
- Language: TypeScript
- Transform engine: jscodeshift
- Output directory: `codemods/`
- Test framework: jest

---

## Codemod types

This skill generates five types of codemods:

### Type 1: Token rename
Renames a design token across all consuming files.

**Scope:** CSS custom properties, JavaScript/TypeScript token imports, Sass variables, style objects, className references.

**Example input:**
```
Rename: color.brand.primary → color.action.primary
Affects: CSS custom properties (--color-brand-primary → --color-action-primary)
         JS token imports (tokens.color.brand.primary → tokens.color.action.primary)
         Sass variables ($color-brand-primary → $color-action-primary)
```

### Type 2: Component prop rename
Renames a component prop across all usage sites.

**Example input:**
```
Component: Button
Rename prop: type → variant
Value mapping: type="primary" → variant="primary" (no value change)
```

### Type 3: Component prop removal
Removes a deprecated prop with a safe fallback or migration.

**Example input:**
```
Component: Button
Remove prop: isLoading
Migration: Replace <Button isLoading> with <Button loading>
```

### Type 4: Import path update
Updates import paths when packages are restructured.

**Example input:**
```
Old: import { Button } from '@myds/components'
New: import { Button } from '@myds/react/Button'
```

### Type 5: Component replacement
Replaces one component with another, mapping props.

**Example input:**
```
Replace: DatePicker → DatePickerNext
Prop mapping:
  - value → selectedDate
  - onChange → onDateChange
  - format → dateFormat (default: "yyyy-MM-dd")
  - minDate → min
  - maxDate → max
Removed props: locale (now uses system locale)
New required props: none
```

---

## Step 0: Determine the codemod type

From the user's request, determine:

1. **What is changing?** Token name, prop name, import path, or component replacement
2. **What are the before and after states?** Exact old and new values
3. **What is the scope?** CSS, JS/TS, Sass, all of the above
4. **Are there edge cases?** Conditional logic, dynamic values, spread props
5. **Is there a value mapping?** Or is it a straight rename

If the request is unclear on any of these, ask before generating. A codemod that transforms the wrong thing is worse than no codemod at all.

---

## Step 1: Generate the transform script

### For jscodeshift transforms (JavaScript/TypeScript)

Each codemod is a single file following the jscodeshift API:

```javascript
/**
 * Codemod: [description]
 * Generated by Design System Ops — codemod-generator
 *
 * Usage:
 *   npx jscodeshift --transform codemods/[name].js --extensions=tsx,ts,jsx,js src/
 *
 * Dry run (preview changes without writing):
 *   npx jscodeshift --transform codemods/[name].js --dry --print src/
 *
 * What this codemod does:
 *   [Clear description of the transformation]
 *
 * What this codemod does NOT do:
 *   [Explicit list of things this codemod will not catch]
 */

module.exports = function transformer(file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);
  let hasChanges = false;

  // [Transform logic]

  if (!hasChanges) {
    return undefined; // Return undefined when no changes — jscodeshift skips the file
  }

  return root.toSource({ quote: 'single' });
};

module.exports.parser = 'tsx'; // or 'babel' for JS-only codebases
```

### For CSS/Sass transforms

CSS transforms cannot use jscodeshift (which is for JS ASTs). Generate a Node.js script using postcss for CSS or a regex-based transformer for Sass:

```javascript
/**
 * Codemod: [description] (CSS)
 * Generated by Design System Ops — codemod-generator
 *
 * Usage:
 *   node codemods/[name]-css.js --dir src/ [--dry-run]
 */

const postcss = require('postcss');
const fs = require('fs');
const path = require('path');
const glob = require('glob');

// [PostCSS-based transform logic]
```

### For Style Dictionary token transforms

If tokens use Style Dictionary format, generate a Style Dictionary pre-processor that transforms the token source files:

```javascript
/**
 * Token migration: [description]
 * Generated by Design System Ops — codemod-generator
 *
 * Usage:
 *   node codemods/[name]-tokens.js --dir tokens/ [--dry-run]
 */

// [JSON/YAML transform logic for token source files]
```

---

## Step 2: Generate test cases

Every codemod must include tests. Generate a test file alongside the transform:

```javascript
/**
 * Tests for: [codemod name]
 * Generated by Design System Ops — codemod-generator
 */

const { applyTransform } = require('jscodeshift/dist/testUtils');
const transform = require('./[name]');

describe('[codemod name]', () => {
  // Test 1: Basic transformation
  it('transforms [basic case]', () => {
    const input = `[before code]`;
    const expected = `[after code]`;
    const result = applyTransform(transform, {}, { source: input });
    expect(result).toBe(expected);
  });

  // Test 2: No-op case (file without the pattern)
  it('does not modify files without [pattern]', () => {
    const input = `[unrelated code]`;
    const result = applyTransform(transform, {}, { source: input });
    expect(result).toBeUndefined();
  });

  // Test 3: Edge case — dynamic values
  it('handles [edge case description]', () => {
    const input = `[edge case code]`;
    const expected = `[expected result]`;
    const result = applyTransform(transform, {}, { source: input });
    expect(result).toBe(expected);
  });

  // Test 4: Edge case — spread props
  it('flags [untransformable case] with a comment', () => {
    const input = `[untransformable code]`;
    const result = applyTransform(transform, {}, { source: input });
    expect(result).toContain('/* TODO: Manual migration needed');
  });
});
```

### Test coverage requirements

Each codemod must have tests for:
1. **Basic case** — The simple, expected transformation
2. **No-op case** — A file that does not contain the pattern (should be untouched)
3. **Multiple occurrences** — File with the pattern appearing multiple times
4. **Edge case: dynamic values** — When the value is a variable, not a literal
5. **Edge case: spread props** — When props are spread (`{...props}`)
6. **Edge case: conditional rendering** — When the component/token is used conditionally
7. **Edge case: aliased imports** — When the import is renamed (`import { Button as Btn }`)
8. **Untransformable case** — When the pattern is too complex for automated transformation (should add a TODO comment, not transform incorrectly)

---

## Step 3: Generate the migration runner

Produce a `migrate.js` script that orchestrates running all codemods for a version upgrade:

```javascript
/**
 * Migration runner: [system name] v[X] → v[Y]
 * Generated by Design System Ops — codemod-generator
 *
 * Usage:
 *   node codemods/migrate.js --dir src/ [--dry-run] [--verbose]
 *
 * This script runs all codemods for the v[X] → v[Y] migration in the correct order.
 * Run with --dry-run first to preview changes.
 */

const { execSync } = require('child_process');
const path = require('path');

const CODEMODS = [
  {
    name: '[codemod 1]',
    file: '[name-1].js',
    description: '[what it does]',
    order: 1,
  },
  {
    name: '[codemod 2]',
    file: '[name-2].js',
    description: '[what it does]',
    order: 2,
    dependsOn: '[codemod 1]', // Must run after codemod 1
  },
];

// [Runner logic: execute codemods in order, report results, handle failures]
```

### Order matters

Some codemods must run before others:
- Token renames before component prop updates (if components reference tokens by name)
- Import path changes before component replacements (so the codemod finds the right imports)
- Prop renames before prop removals (to avoid losing context)

The migration runner enforces this ordering.

---

## Step 4: Generate documentation

Produce a `MIGRATION.md` file alongside the codemods:

```markdown
# Migration guide: v[X] → v[Y]

## What changed
[Summary of all changes covered by these codemods]

## Automated migration
Run the migration script:
\`\`\`bash
# Preview changes (recommended first step)
node codemods/migrate.js --dir src/ --dry-run

# Apply changes
node codemods/migrate.js --dir src/
\`\`\`

## What the codemods handle
| Change | Codemod | Scope |
|---|---|---|
| [change 1] | [codemod file] | JS/TS/CSS |
| [change 2] | [codemod file] | JS/TS only |

## What requires manual attention
These changes cannot be fully automated:
- [manual item 1 — why it cannot be automated]
- [manual item 2 — why it cannot be automated]

For each manual item, search your codebase for:
\`\`\`bash
grep -r "[pattern]" src/
\`\`\`

## Verification
After running the codemods:
1. Run your test suite: \`npm test\`
2. Run type checking: \`npx tsc --noEmit\`
3. Visually review the changed files: \`git diff\`
4. Run your application and test the affected components
```

---

## Step 5: Handle untransformable patterns

Not everything can be automated. When the codemod encounters a pattern it cannot safely transform, it must:

1. **Leave the original code untouched** — Never guess. Never transform incorrectly.
2. **Add a TODO comment** at the exact location:
   ```javascript
   /* TODO: Manual migration needed — [description of what needs to change]
    * Old pattern: [what the code currently does]
    * New pattern: [what it should become]
    * Why this was not automated: [reason — dynamic value, complex logic, etc.]
    * Generated by Design System Ops — codemod-generator
    */
   ```
3. **Report it** in the migration runner output:
   ```
   ⚠ [file.tsx:42] — Manual migration needed: [description]
   ```

### Common untransformable patterns

- **Dynamic prop values:** `<Button variant={getVariant()}>` — the codemod cannot know what `getVariant()` returns
- **Spread props:** `<Button {...buttonProps}>` — the codemod cannot know what `buttonProps` contains
- **Computed token access:** `tokens[`color.${category}.${variant}`]` — the codemod cannot resolve template literals
- **Re-exported components:** When a component is re-exported through an intermediary module with different prop types
- **Test files with mocked props:** Mock objects may need different handling than production code

---

## Integration with other skills

### From deprecation-process
When deprecation-process plans a component replacement, codemod-generator can produce the migration script. The deprecation plan's prop mapping table becomes the codemod's transformation rules.

### From change-communication
When change-communication writes release notes, include the codemod usage instructions in the "How to upgrade" section.

### From cicd-integration
Add a CI step that verifies codemods pass their tests before release. Include codemod tests in the design system's test suite.

### From session-memory
After running codemods, save the results (files changed, manual items flagged) to session memory so future runs can track migration completion.

---

## Step 6: Two-sided migration (when Figma Console MCP is available)

If the Figma Console MCP from Southleft is connected (check for `figma_rename_variable` and `figma_update_variable` tool availability), extend the migration to include Figma variable renames alongside the code codemods. This ensures design and code stay in sync during the migration.

**Token renames:** When the codemod type is `token-rename`, use `figma_rename_variable` to rename the corresponding Figma variables. Map each code-side rename to its Figma-side equivalent. Figma renames preserve all values, modes, and alias references — only the name changes.

**Prop renames that affect Figma:** When the codemod type is `prop-change` and the renamed prop maps to a Figma component property, use `figma_edit_component_property` to update the property name in the Figma component. This keeps the Figma component's exposed properties in sync with the code API.

**Workflow:**
1. Generate the code-side codemods and tests (Steps 1–5) first
2. Present the full migration plan, including which Figma variables or properties will be renamed
3. Ask the user to confirm before applying Figma changes: "This migration will rename 8 tokens in code and 8 matching Figma variables. Apply both?"
4. Apply Figma renames
5. Verify by reading back the renamed variables
6. Note any Figma-side changes in the MIGRATION.md documentation alongside the code changes

**When the standard Figma MCP is connected (read-only):** The code-side codemods work normally. Include a section in MIGRATION.md listing the Figma variables that need to be renamed manually, with old name → new name mapping.

---

## Quality checks

- Every codemod has a corresponding test file with ≥8 test cases
- Every codemod includes a dry-run option
- Every codemod handles untransformable patterns with TODO comments, not incorrect transforms
- The migration runner enforces correct ordering based on dependencies
- The MIGRATION.md clearly separates automated from manual steps
- All generated files include provenance comments
- The codemod preserves source code formatting (indentation, quotes, semicolons)
- The codemod returns `undefined` for files that do not need changes (jscodeshift convention)
- Test cases cover: basic, no-op, multiple occurrences, dynamic values, spread props, conditional rendering, aliased imports, and untransformable patterns
- The CSS/Sass transform handles both custom properties (`--token-name`) and Sass variables (`$token-name`)
- If Figma variables were renamed, each rename was verified by reading back the variable
