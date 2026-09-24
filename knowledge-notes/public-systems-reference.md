---
name: public-systems-reference
type: knowledge
---

# Public design systems: reference points

**Knowledge note for Design System Ops**
**Loaded by:** every skill that lists this note in its frontmatter `references:` (the tests keep that list accurate; this header does not repeat it).

---

## How to use this note

`system-health` may add an "External reference points" section when the user asks how their system compares with what public systems do. This note is the only source for claims about those systems. The rules:

- **Cite the URL and the check date** for every claim, exactly as recorded below. If a claim isn't in this note, don't make it; offer to fetch and check the system's current docs instead, and record what you find with today's date.
- **Compare practices, not maturity.** These systems have teams, budgets and histories the user's system doesn't. "Carbon publishes its theme tokens as a package" is a useful reference. "Your system is behind Carbon" is not.
- **Never state adoption figures, team sizes or component counts** for a public system. None are recorded here because none are published in a form that stays true between releases.
- **Status changes.** Systems get archived, renamed and moved. The status column is the reason this note carries dates. Before quoting a system, check the entry's date; if it is more than six months old, re-check the URL and update the entry.

Everything below was checked on **2026-09-24** by reading the linked page. "Not checked" means the page didn't show it, not that it doesn't exist.

---

## Reference table

| System | Owner | Status on check date | Source checked |
|---|---|---|---|
| Carbon | IBM | Active | https://github.com/carbon-design-system/carbon |
| GOV.UK Design System / GOV.UK Frontend | UK Government Digital Service | Active (Frontend v6.5.0 shown on the site) | https://design-system.service.gov.uk/ and https://github.com/alphagov/govuk-frontend |
| USWDS | US General Services Administration | Active | https://designsystem.digital.gov/ |
| Primer | GitHub | Active | https://github.com/primer/react |
| Paste | Twilio | Active, "open source and contributions are welcome" | https://github.com/twilio-labs/paste |
| Atlassian Design System | Atlassian | Active | https://atlassian.design/foundations/tokens |
| Material Design 3 | Google | Active | https://m3.material.io/foundations/design-tokens/overview |
| Spectrum | Adobe | Active; the `spectrum-tokens` repository is "maintained as a placeholder for redirects only" and points to a new repository | https://github.com/adobe/spectrum-tokens |
| Polaris | Shopify | **Archived.** The repository README says "This repository is archived and unmaintained" and "We are no longer accepting contributions or feature requests in this repository" (archived 2026-09-11). The docs redirect to https://shopify.dev/docs/api/polaris | https://github.com/Shopify/polaris |
| Australian Government Design System (AGDS) | Australian Government | **Gone.** `designsystem.gov.au` did not resolve on the check date | (domain unreachable) |

---

## What each system documents publicly

Only what the checked page showed. Use these as examples of a practice, with the URL.

**Carbon.** Tokens and foundations ship as packages: `@carbon/themes` ("Theme tokens for Carbon color systems"), `@carbon/colors`, `@carbon/layout` ("Layout units and spacing scale tokens"), `@carbon/type`, `@carbon/motion`, `@carbon/elements`. Components in `@carbon/react` and `@carbon/web-components`; styles in `@carbon/styles` (Sass). A CONTRIBUTING.md exists: "Contributions are welcome. See CONTRIBUTING.md for contribution guidelines and repository expectations." Accessibility, release cadence and deprecation policy: not checked.

**GOV.UK Frontend.** Distributed as the `govuk-frontend` npm package, or "by copying our CSS, JavaScript and asset files into your project." A CONTRIBUTING.md exists. Accessibility claim: "Using Frontend will help your service meet level AA of WCAG 2.2." Browser support is graded A, B, C and X, with JavaScript enhancements supported only for grades A to C. The design system site publishes an accessibility statement and component lifecycle statuses ("Trial" and "Stable"), and a community section for "discussions, events and co-design collaborations." Deprecation policy: not checked.

**USWDS.** Publishes design tokens as "the building blocks of USWDS component design," with token pages for color, typesetting, flex, opacity, order, shadow, spacing units and z-index. A contribute page exists at `/about/contribute/` and an accessibility page at `/documentation/accessibility/`. Source: https://github.com/uswds/uswds. Release and deprecation policy: not checked.

**Primer.** Components in `@primer/react`; the docs site describes "Primer's design tokens for color, spacing, and typography" under Primitives. Contributing docs exist ("See the contributing docs for more info on code style, testing, coverage, and troubleshooting"), and the repository carries a `migrating.md`. Deprecation policy and accessibility statement: not checked.

**Paste.** Packages include `@twilio-paste/design-tokens`, `@twilio-paste/theme`, `@twilio-paste/box` and `@twilio-paste/style-props`. Contributing guidelines and a code of conduct exist. Accessibility: not checked.

**Atlassian Design System.** Publishes a tokens foundation with names of the form `color.text.accent.red` and `color.background.accent.lime.bold`, with sections for "Use tokens in code" and "Migrate to tokens." Package name, ESLint or codemod tooling, contribution and deprecation policy: not checked (the landing page didn't show them; the sub-pages likely do).

**Material Design 3.** Documents design tokens at the URL above. Token naming, tiers and dynamic colour: not checked (the page didn't render in the fetch; read it directly before quoting).

**Spectrum.** Publishes `@adobe/spectrum-tokens`, `@adobe/spectrum-component-api-schemas` and `@adobe/spectrum-design-data-mcp`, described as "Design tokens and token management tools," "JSON schemas for component options and APIs" and an MCP server for design data. Token format (DTCG or not): not checked.

---

## Practices worth pointing at

Each of these is a specific, sourced example a practitioner can open. They are the reference points system-health may use; nothing else in this note is.

- **Tokens as versioned packages, separate from components:** Carbon (`@carbon/themes`, `@carbon/type`), Paste (`@twilio-paste/design-tokens`), Spectrum (`@adobe/spectrum-tokens`).
- **A published accessibility baseline tied to a WCAG version:** GOV.UK Frontend ("level AA of WCAG 2.2").
- **A published browser-support grading:** GOV.UK Frontend (grades A to X).
- **Component lifecycle statuses on the docs site:** GOV.UK Design System ("Trial", "Stable").
- **Component API schemas and an MCP server published alongside tokens:** Spectrum (`@adobe/spectrum-component-api-schemas`, `@adobe/spectrum-design-data-mcp`).
- **A migration guide kept in the repository:** Primer (`migrating.md`).
- **A public contribution guide:** Carbon, GOV.UK Frontend, USWDS, Primer, Paste.

## What this note deliberately doesn't say

No maturity stages for public systems, no "typical profiles" by system type, no adoption or team figures, and no claims about governance quality. Those can't be read from a docs page, and an earlier version of the pack presented them as if they could.
