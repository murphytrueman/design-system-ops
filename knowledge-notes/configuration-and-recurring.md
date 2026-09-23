---
name: configuration-and-recurring
type: knowledge
---

# Configuration, integrations, and recurring runs

**Knowledge note for Design System Ops**
**Auto-loaded by:** session-memory. Every skill with a Configuration section reads it when a `.ds-ops-config.yml` file exists — most runs have no config file and never need it.

This note holds the procedure every configurable skill shares. Each skill's own Configuration, Auto-pull and Recurring sections list only what is specific to that skill: which keys it reads, what it pulls from each integration, and what its trend section compares.

---

## Loading configuration

Check the project root for `.ds-ops-config.yml` before producing output. The annotated template, `ds-ops-config.example.yml`, documents every key.

- **No config file:** proceed with defaults and ask for what you need. Don't mention configuration unless the user asks.
- **Config file present:** load the keys the skill lists. Keys it doesn't list are for other skills; ignore them.
- **`severity.*`** overrides replace the skill's default severity for the named finding type. They never create a new label: values are critical, high, medium or low.
- **`system.*`** keys describe the system (framework, styling, theming, component and token paths). Treat them as facts the user has stated. If the code clearly contradicts one — `system.styling: tailwind` in a repo with no Tailwind config — say so in the Scope block rather than silently choosing one.

---

## Auto-pull integrations

When an integration is enabled (`integrations.<name>.enabled: true`), pull its data before asking the user for the same information.

- **An integration that fails** (auth error, rate limit, missing tool permission) never blocks the run. Note the failure in the Scope block and fall back to local files or manual input.
- **An integration's data is a source like any other.** Name it in the Scope block, and apply the empty-result rule from output-discipline: an integration that returns nothing hasn't shown that nothing exists.

Integration-specific cautions:

- **GitHub.** Prefer a local clone for searches and counts. `gh api search/code` has no regex support, searches only the default branch, and returns approximate counts: use it to find files worth reading, never to count violations or usages. `gh api` can also write with the user's credentials, so commands leave it to prompt rather than pre-approving it.
- **npm.** Download counts are inflated by CI runs, caches and registry mirrors, can't be attributed to teams, and may be unavailable on a private registry (`integrations.npm.registry_url`). Use them for direction, not as adoption figures. `npm view <package> version` gives the latest published version for version-lag checks.
- **Figma.** The Figma Console MCP reads and writes whole variable collections and component descriptions. The official Figma MCP reads only the current selection (`get_variable_defs` returns the variables a selected node uses, not whole collections) and writes through `use_figma`. The Variables REST API is Enterprise-only. State which one was used and what it couldn't see.
- **Storybook.** A local build's `index.json` (or `stories.json` in Storybook 6) is the most reliable source. A published URL may need auth.
- **Chromatic.** Accepted visual changes show what changed since the baseline, not whether the build matches the design.

---

## Recurring runs

A skill supports recurring runs when its Recurring section says so. The `recurring` section of the config switches them on.

1. **Find the previous report** in `recurring.output_directory` that matches `recurring.naming_pattern` for this skill.
2. **Check the runs are comparable.** Compare their Scope blocks first. Findings in areas one run inspected and the other didn't are "not comparable", not resolved or new.
3. **Match findings by content, not ID.** Finding IDs are numbered per run, so match on the rule or category plus the component or token it concerns.
4. **Classify each finding:** new (present now, not before), resolved (present before, not now, within the shared scope), or persistent (present in both). Persistent for two or more consecutive runs usually warrants escalating severity by one level; the skill's Recurring section says when.
5. **Add the skill's trend section** near the top of the report, with the date of the previous run and the direction in one sentence (improving, stable, or declining since [date]).
6. **Save** the new report to `recurring.output_directory` using `recurring.naming_pattern`.
7. **Pruning is proposed, never automatic.** If the number of saved reports exceeds `recurring.retain_count`, list the oldest ones beyond the limit and delete them only after the user confirms.

If no previous report exists, say "This is the baseline run. Trend analysis will be available from the next run." and save the report.

`recurring.comparison_mode` sets the depth: `full` shows the side-by-side changes; `summary` shows only the deltas.
