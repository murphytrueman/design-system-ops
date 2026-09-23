---
name: engineering-onboarding
description: "Onboarding guide for an engineer consuming the design system: install, imports, tokens, testing, escalation, first two weeks. Triggers: onboard new engineer, developer getting started guide, frontend onboarding. For designers use designer-onboarding."
references:
  - ../../knowledge-notes/design-to-code-contract.md
---

# Engineering onboarding

A skill for writing an onboarding guide for an engineer joining a team that consumes the design system, grounded in the team's actual repository and stack.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Engineering onboarding is genuinely different from designer onboarding. The mental model is different (consuming an API vs composing with a library), the first tasks are different (install and import vs connect Figma library), the tooling is different (package manager, TypeScript types, test harness vs Figma, documentation platform). Most importantly, engineers are where component drift originates — wrapping system components in local styled wrappers, hardcoding token values, reimplementing components locally. Proper onboarding from day one is the highest-leverage adoption intervention.

## Key principles

Engineers and designers operate on opposite sides of the contract. Designers compose with a library (Figma, Storybook). Engineers consume an API (imports, props, types). The contract is the component signature: what props it accepts, what slots it exposes, what variants are possible. Drift often begins when an engineer builds a local version because "the system component is close but not quite right" and raises it too late. Onboarding embeds the contract from day one.

**Key principle for engineers:** Do not build local wrapper components. Do not hardcode values. Do not copy source code. Ask first.

**One rule for workarounds, used everywhere in the guide:** if a team needs a visual change the system doesn't offer yet, it may add a class through the component's `className` (or equivalent) prop for at most one sprint — no wrapper component, no `!important` — with a comment linking the tracking issue, and remove it when the system variant ships.

## Configuration

**Read before asking.** Check `.ds-ops-config.yml` in the project root for `system.name`, `system.framework` and `system.styling`. Then inspect the repository: `package.json` (package name, `exports`, peer dependencies, scripts), the token source or build output (CSS custom properties, JS token modules, Tailwind theme), exported TypeScript types, and the test setup (Jest or Vitest config, Chromatic or Percy config, axe or similar). Every fact in the guide — install command, import paths, token names, test tooling, policies — comes from these files or from the team. Anything neither confirms goes in as `[confirm: …]` and is listed at the top of the guide.

The examples in this skill are React and Jest for illustration. Write the guide's examples in the detected stack (Vue single-file components, Web Components, Vitest, and so on) using the real package name, exports and token names.

Ask the team only for what the files can't answer:

1. **Framework:** React, Vue, Web Components, Svelte, Angular, etc.
2. **Package manager:** npm, yarn, pnpm (include install command)
3. **Token consumption:** CSS custom properties, JavaScript imports, Tailwind theme config, Sass variables
4. **Component API patterns:** Props, slots, composition style, controlled vs uncontrolled patterns
5. **TypeScript:** Are component types exported? Import pattern for types?
6. **Testing:** Visual regression tool (Chromatic, Percy), unit testing patterns, accessibility testing expectations
7. **Contribution path:** How does an engineer propose a fix or new component? PR process, code review, approval gates
8. **Known rough edges:** Documented workarounds, temporary incompatibilities, or known limitations
9. **Team contacts:** Slack channel, primary system maintainer, office hours schedule

## Steps

**Step 1: Gather system context from the team**

Start from the config and repository inspection above. Ask the team only for what the files don't show: contribution expectations, update and backport policy, accessibility guarantees, known rough edges, contacts. If documentation exists, review it first — you're clarifying, not starting from scratch. Record which information is documented vs tribal knowledge (tribal knowledge is what gets lost in onboarding).

Output: A 5-minute conversation summary or Slack thread capture.

**Step 2: Structure the onboarding guide**

Use this exact section order. Each section builds on prior context. No forward references.

**Step 3: Write the guide introduction**

```
# Getting started with [Design System Name] — for engineers

**For:** Engineers joining [Team Name]  
**Last updated:** [Today's date]  
**Questions:** [Slack channel or contact email]  
**Estimated time to first component render:** [confirm: time measured by a recent joiner, or omit]  
**Still to confirm:** [every `[confirm: …]` left in the guide, or "none"]

You're consuming a versioned component library and token system. Your job is to use it correctly, not to rebuild it. This guide shows you how.
```

**Step 4: Write "What [System Name] is" section**

One paragraph from engineer perspective. Answer: What am I consuming? What can it do? What shouldn't I do?

Example template:
```
[System Name] is a versioned component library with [X] components and [Y] design tokens. 
It's distributed as an npm package and consumed via import statements in your code. 
The system owns component styling and behavior — your job is to compose components correctly 
and reference tokens instead of hardcoding values. If you need a variant or component that 
doesn't exist, you ask the system team; you don't build a local version.
```

**Step 5: Write "Installation and setup" section**

Copy-pasteable commands. Mark placeholders in brackets, not in the command itself.

```
## Installation and setup

Install the package:
\`\`\`bash
npm install @[org]/[design-system-name]
\`\`\`

Import the CSS (or theme provider for React) — use the path the package actually exports:
\`\`\`jsx
import '@[org]/[design-system-name]/styles/index.css';
\`\`\`

Verify it works — render a Button in your app:
\`\`\`jsx
import { Button } from '@[org]/[design-system-name]';

export default function App() {
  return <Button>Click me</Button>;
}
\`\`\`

You should see a styled button on the screen. If you see an unstyled button or an error, 
check the [install troubleshooting guide](link).
```

**Step 6: Write "Using components" section**

Import pattern. Prop API conventions. One complete code example. TypeScript types if applicable.

```
## Using components

All components are named exports. Import what you need:
\`\`\`jsx
import { Button, Input, Card } from '@[org]/[design-system-name]';
\`\`\`

Read prop documentation in Storybook: [link to component docs]. 
Every prop is listed with type and default value.

Example — a login form using system components:
\`\`\`jsx
import { useState } from 'react';
import { Button, Input, Card, Text } from '@[org]/[design-system-name]';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  
  return (
    <Card padding="large">
      <Text variant="heading">Sign in</Text>
      <Input 
        type="email" 
        placeholder="Email" 
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <Button variant="primary">Sign in</Button>
    </Card>
  );
}
\`\`\`

For TypeScript, component types are exported from the package:
\`\`\`tsx
import type { ButtonProps } from '@[org]/[design-system-name]';
\`\`\`
```

**Step 7: Write "Using tokens" section**

Include before/after example showing wrong vs right.

```
## Using tokens

Tokens are design decisions (spacing, color, typography) managed by the system team. 
Always reference tokens, never hardcode values.

**Access tokens via CSS variables:**
\`\`\`css
.my-component {
  padding: var(--ds-spacing-medium);
  color: var(--ds-color-text-primary);
}
\`\`\`

**or JavaScript imports (if available):**
\`\`\`js
import { spacing, colors } from '@[org]/[design-system-name]/tokens';

const styles = {
  padding: spacing.medium,
  color: colors.text.primary,
};
\`\`\`

**Wrong — hardcoded value:**
\`\`\`jsx
<div style={{ padding: '16px', color: '#222222' }}>
  Content
</div>
\`\`\`

**Right — uses tokens:**
\`\`\`jsx
import { spacing, colors } from '@[org]/[design-system-name]/tokens';

<div style={{ padding: spacing.medium, color: colors.text.primary }}>
  Content
</div>
\`\`\`

Use semantic tokens (e.g., `colors.text.primary`), never primitives directly 
(e.g., never reach for `colors.blue[500]`). Semantic tokens survive theme changes; 
primitives break in dark mode or custom themes.
```

**Step 8: Write "When the system doesn't have what you need" section**

Escalation path. Contribution path. Temporary workarounds.

```
## When the system doesn't have what you need

**First:** Check Storybook [link] and the component API docs.  
**Second:** Ask in #[design-system-slack-channel].  
**Third:** File a feature request in [issue tracker].  

Don't copy component source. Don't build a local wrapper component. Both create drift 
and make the system lose visibility into what you actually need.

**Temporary workarounds** (one sprint at most): while waiting for a system variant, 
you can add a class through the component's `className` prop — no wrapper component, 
no !important overrides. Comment the workaround with a link to the tracking issue, 
and remove it when the system delivers the variant.

**Contributing a fix** (bugs in system components): 
1. Fork [system repo]
2. Fix the issue
3. Add a test
4. Open a PR against the [main/release branch]
5. System team reviews and merges

[Link to contribution guide]
```

**Step 9: Write "Testing with system components" section**

Unit testing, visual regression, accessibility expectations.

```
## Testing with system components

**Unit tests:** Mock system components if needed:
\`\`\`jsx
jest.mock('@[org]/[design-system-name]', () => ({
  Button: ({ children, ...props }) => <button {...props}>{children}</button>,
}));
\`\`\`

Test your component's logic, not the system component's rendering 
(that's the system team's job).

**Visual regression:** We use [Chromatic/Percy]. Your PR will automatically 
compare visual changes against the baseline. Review differences in the PR check 
before merging. If you update a component's appearance intentionally, 
approve the diff.

**Accessibility testing:** [confirm: what the system team guarantees for its components, 
and against which standard — the baseline is WCAG 2.2 AA; some legal baselines, 
e.g. EN 301 549, still reference WCAG 2.1 AA]. Whatever the components guarantee, your 
composition is yours to test: heading hierarchy, alt text on images, and focus management. 
[Link to a11y guide]
```

**Step 10: Write "Common mistakes" section**

Seven anti-patterns specific to engineers.

```
## Common mistakes

1. **Wrapping system components in local styled wrappers**
   Don't: Create a `StyledButton = styled(Button)`. Request a variant from the system instead.

2. **Hardcoding hex values instead of referencing tokens**
   Don't: `color: '#FF4444'`. Use `color: var(--ds-color-error)`.

3. **Using primitive tokens directly**
   Don't: `colors.blue[500]`. Use `colors.primary` (semantic tier).

4. **Copying component source instead of importing**
   Don't: Copy the Button JSX into your repo. That breaks updates forever.

5. **Overriding component styles with !important**
   Don't: `.my-button { color: red !important; }`. Request the system variant.

6. **Pinning to a specific version and never updating**
   Don't: Lock `@[org]/[design-system-name]` to 1.2.0 for a year. 
   Update monthly. Bug fixes and security patches matter.

7. **Building local variants instead of requesting them**
   Don't: Create a custom "success with icon" button variant locally. 
   Tell the system team. It probably belongs in the system.
```

**Step 11: Write "Your first two weeks" section**

Checkbox path with concrete tasks.

```
## Your first two weeks

**Week 1:**
- [ ] Install the package and render your first component (today)
- [ ] Read the [components overview](link) — understand what exists
- [ ] Use tokens in a feature you're working on — don't hardcode values
- [ ] Post a question in #[design-system-channel] — introduce yourself

**Week 2:**
- [ ] Review a PR that touches system components — spot common mistakes
- [ ] File a bug or feature request based on something you hit — 
  show you understand the escalation path
- [ ] Pair with a system team member for 30 min — ask your hardest questions
- [ ] Read [your team's design-to-code contract or handoff doc](link) — understand why things work this way
```

**Step 12: Write "Quick reference card" section**

Compact, printable.

```
## Quick reference card

**Install:**
\`\`\`bash
npm install @[org]/[design-system-name]
\`\`\`

**Import components:**
\`\`\`jsx
import { Button, Input } from '@[org]/[design-system-name]';
\`\`\`

**Access tokens:**
\`\`\`jsx
import { spacing, colors } from '@[org]/[design-system-name]/tokens';
\`\`\`

**Documentation:** [Storybook link]  
**Questions:** [#slack-channel](slack link)  
**Contribute:** [GitHub repo link]  
**Escalate:** Post in Slack first, then file an issue  

**Remember:** Use it correctly. Don't wrap it. Don't copy it. Ask first.
```

**Step 13: Write "Common questions" section**

Four to five engineer-specific Q&As.

```
## Common questions

**Q: Can I override component styles with CSS?**
A: Not with !important. If you need a visual change, request a variant from the system. 
Temporary workarounds are okay (one sprint max) — add a class through the component's 
`className` prop and comment with the issue link.

**Q: What if I need a component that doesn't exist?**
A: Ask in #[design-system-channel] first. The component might be planned or in another team's code. 
If it's genuinely new, file a feature request. Don't build it locally.

**Q: Do I have to use TypeScript types?**
A: No, but they're available if you use TypeScript. [confirm: whether the package 
validates props at runtime for non-TypeScript users]

**Q: How often do I need to update the design system package?**
A: [confirm: the team's update expectation and backport policy — e.g. which versions 
get security fixes]. Major version updates are documented in [migration guide link].

**Q: What's the difference between tokens and component props?**
A: Tokens are values (colors, spacing). Props are component options (size, variant). 
Use both together: a Button's variant sets its colors via tokens internally.
```

## Quality Checks

1. **Completeness for new engineers:** Can someone with zero prior design system experience follow this and render a component by Step 5?
2. **Copy-paste commands:** All install and import commands are directly executable — no placeholders in the command itself. Placeholders are in brackets and marked.
3. **Runnable code examples:** Every code example is complete and renders something visible (not fragments).
4. **Anti-patterns are specific:** Each mistake references an actual pattern, not generic advice. Includes "don't" and "do instead" for each.
5. **Token usage shows wrong vs right:** Before/after code example demonstrates the impact of the mistake.
6. **Testing coverage:** Unit testing, visual regression, and accessibility testing are all mentioned with enough detail to get started.
7. **No forward references:** Each section stands alone. No "see Step X" or "we'll explain later."
8. **Grounded in the repo:** Package name, import paths, token names and test tooling come from the config and repository, and examples use the detected stack. Policies and guarantees (accessibility, backports, runtime validation, time to first render) are confirmed by the team or left as `[confirm: …]` and listed at the top.
9. **One workaround rule:** The one-sprint `className` workaround is stated the same way everywhere; no section suggests a wrapper component.

## Small-system note

For systems with fewer than 5 components, compress the onboarding:

- Compress "Using components" into a single example (install → import → render one component).
- Name every component in the overview so nothing is left implicit.
- Collapse "Installation and setup" + "Using components" into one section if the system is very small.
- Shorten "Your first two weeks" to "Your first week" with 3-4 tasks.
- Remove the quick reference card (too little to reference).
