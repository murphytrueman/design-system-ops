---
name: component-decision-tree
description: "Write \"choosing between\" pages (docs/choosing/) that route an intent to the right component via narrowing questions; YAML trees on request. Triggers: which component should I use, choose between X and Y, dialog vs drawer, selection guide. One chosen component: usage-guidelines."
allowed-tools: Read, Write, Grep, Glob, Bash(cat:*), Bash(find:*), Bash(head:*), Bash(ls:*)
references:
  - ../../knowledge-notes/ai-readiness.md
  - ../../knowledge-notes/component-bestiary-reference.md
  - ../../knowledge-notes/output-discipline.md
---

# Component decision tree

A skill for building decision trees that map user intents and requirements to specific component selections. The primary output is a set of "Choosing between…" pages in the docs, one per cluster of confusable components, written as the questions a senior designer would ask; the same trees can be written as YAML for tooling when something will read it. Both reduce the guesswork that leads to component misuse, duplication, and inconsistency.

## Before you begin: verify references

Confirm that every path in this skill's frontmatter `references:` exists relative to this SKILL.md. If any is missing, stop: the install is incomplete, usually because a flattening installer (for example `npx skills install`) dropped the repo-root `knowledge-notes/` directory. Tell the user to reinstall by a method in `1-INSTALL.md` and run `verify-install.sh` from the install root. Proceed without the references only if the user explicitly says to, and then say in the output that it was produced without the pack's reference material.

## Context

Component selection is the first decision in any design system interaction, and it is the one that AI agents get wrong most often. The failure mode is not random — it follows predictable patterns. An agent selects a Modal when a Dialog was appropriate. It uses a Card where a List Item fits better. It creates a custom component because it could not find the existing one that serves the need.

These errors have the same root cause: the agent does not have a decision framework. It has a list of components (if it has anything at all) and it pattern-matches the user's request against component names and descriptions. This works when the match is obvious ("I need a button" → Button) and fails when the match requires judgment ("I need to show a collection of items that users can filter and sort" → is that a Table, a DataGrid, a List with filters, or a custom composition?).

Decision trees encode the judgment. Instead of relying on an agent's ability to infer the right component from a description, the tree asks a structured sequence of questions that narrow the selection to the correct component. The questions are the same ones a senior designer or developer would ask when advising a junior team member.

The practical output is a page a human reads and an agent is pointed at from `AGENTS.md` (`agent-instructions` links the choosing pages). A YAML form of the same tree is useful only when a tool will traverse it; write it on request, not by default, so there is one thing to keep current.

## Boundaries

This skill produces decision trees for component selection — choosing between components. It does not document how to use a single component once selected (use `usage-guidelines` for that) or generate component metadata schemas (use `metadata-schema-generator`). If the system has fewer than 5 components, a decision tree adds overhead without value — a simple component index is sufficient. If no component inventory exists, run `component-audit` or `codebase-index` first to establish one.

---

## Configuration

If `.ds-ops-config.yml` exists, follow the configuration-and-recurring knowledge note (`../../knowledge-notes/configuration-and-recurring.md`) for loading, integration fallbacks and recurring runs. This skill reads:
- `system.component_paths` — directs scanning to component directories
- `system.category_model` — determines top-level decision tree branches (atomic, functional, custom)
- `integrations.*` — component data sources (see below)
- `decision_tree.output_format` — `markdown` (default: pages in `docs/choosing/`), `yaml` or `json` (machine-readable trees in `.ai/decision-trees/` as well as the pages)

## Auto-pull integrations

**Figma MCP** (`integrations.figma.enabled: true`):
- Read the published component library from `integrations.figma.file_key`
- Extract component names, descriptions, and variant structures
- Use descriptions as input for decision node generation

**Storybook** (`integrations.storybook.enabled: true`):
- Fetch the story index for a complete component list
- Extract documented use cases from story titles and descriptions

**Codebase index** (`.ai/index/component-inventory.yml`):
- If a codebase index exists, load the component inventory and relationship graph
- Use category assignments and relationship data to inform tree structure

---

## Step 1: Map the component landscape

Before building decision trees, understand what components exist and how they cluster.

**Component inventory**: List every component with its purpose and category. If a codebase index exists, use it. If not, scan the component directories.

**Functional clusters**: Group components by the user need they serve, not by their technical category. A single user need often spans multiple components. The two tables below are illustrative: build yours from the scanned inventory, not from these names.

| User need | Components that serve it |
|---|---|
| Show a notification | Toast, Banner, Alert, InlineMessage, Snackbar |
| Collect user input | Input, TextArea, Select, Combobox, DatePicker, Checkbox, Radio, Switch |
| Navigate between views | Tabs, Sidebar, Breadcrumb, Pagination, BottomNav |
| Display a collection | Table, DataGrid, List, CardGrid, Timeline |
| Confirm an action | Dialog, ConfirmationModal, AlertDialog |
| Show contextual info | Tooltip, Popover, HoverCard, Dropdown |

**Overlap analysis**: Identify components with overlapping use cases. These are the decision points where agents (and humans) get confused. In real output, each distinguishing factor cites where it came from (the system's docs, source, or the user); otherwise mark it `proposed`:

| Component A | Component B | Distinguishing factor |
|---|---|---|
| Dialog | Drawer | Dialog interrupts for a focused decision and closes; Drawer keeps the page in view for a task alongside it (if the system's docs say so). "Modal" is a property either can have, not a component, per the ARIA Authoring Practices; a system with both `Modal` and `Dialog` components has a naming finding for `naming-audit` |
| Toast | Banner | Toast is transient and non-blocking; Banner persists until dismissed |
| Select | Combobox | Select has a fixed option list; Combobox allows search/filter |

**Provenance rule.** Two hard rules for everything this skill writes:
- Every `resolve:` names a component that exists in the scanned inventory. If the right answer is a component the system doesn't have, say so in the summary rather than resolving to it.
- Every leaf rationale and distinguishing factor carries a `basis`: a docs or source path, `user`, or `proposed`. Selection logic you inferred from general design practice is `proposed` until the team confirms it. See "Every figure and fact needs a source" in the output-discipline knowledge note.

Ask for or confirm:
- Are there components that teams frequently confuse or misuse? (These are high-priority decision points)
- Are there component selection decisions that are currently undocumented and rely on tribal knowledge?
- Are there recent cases where an AI agent or a new team member selected the wrong component?

---

## Step 2: Build the intent taxonomy

Define the intents that drive component selection. Intents are what the user or agent is trying to accomplish, expressed independently of any specific component.

### Intent categories

Cover the categories the inventory actually needs; typical ones:
- **Display** — show information (a value, a list, a table, a status, a notification, contextual help, media)
- **Input** — collect information (text, a choice from options, a date, a boolean, a file, a search query, a complex form)
- **Action** — let the user do something (primary or secondary action, navigate, confirm a destructive action, open a menu, toggle)
- **Layout** — organise content (group, separate, create navigable structure, contain an interactive flow)

### Intent format

```yaml
intents:
  display_notification:
    description: "Show feedback about an action or system event"
    qualifiers:
      persistence: ["transient", "persistent", "dismissible"]
      severity: ["success", "warning", "error", "info"]
      position: ["inline", "overlay", "page-level"]
      blocking: ["blocks_interaction", "non_blocking"]
```

---

## Step 3: Build the decision trees

For each functional cluster, build a decision tree that maps intents and qualifiers to component selections.

### Tree structure

Each node in the tree is either a **question node** (asks a qualifying question) or a **leaf node** (resolves to a component).

Quote answer keys that YAML would otherwise read as booleans: `"yes"`, `"no"`, `"on"`, `"off"`, `"true"`, `"false"`. Unquoted `yes:` and `no:` parse as `true` and `false` in YAML 1.1 parsers, so a tool looking up `"yes"` finds nothing. Descriptive keys (`persists`, `transient`) avoid the problem entirely.

Illustrative example (component names stand in for the scanned inventory):

```yaml
decision_trees:
  notification:
    description: "Select the right component for showing feedback or notifications"
    root:
      question: "Does the notification need to persist until the user dismisses it?"
      options:
        "yes":
          question: "Is the notification related to the current page/section or the whole application?"
          options:
            current_section:
              question: "Is it inline with the content or separate from it?"
              options:
                inline:
                  resolve: "InlineMessage"
                  confidence: "high"
                  rationale: "Inline messages appear within the content flow for contextual feedback"
                  basis: "docs/components/inline-message.md"
                separate:
                  resolve: "Alert"
                  confidence: "high"
                  rationale: "Alerts appear as distinct blocks for section-level notifications"
                  basis: "docs/components/alert.md"
            whole_application:
              resolve: "Banner"
              confidence: "high"
              rationale: "Banners span the full width for application-level persistent messages"
              basis: "user"
        "no":
          question: "Does the user need to take action based on the notification?"
          options:
            "yes":
              resolve: "Alert"
              confidence: "medium"
              rationale: "An action the user must be able to take shouldn't live in something that disappears"
              basis: "proposed"
              notes: "A Toast with an action fails keyboard and screen-reader users who can't reach it before it times out (WCAG 2.2.1 Timing Adjustable); use a persistent Alert, or a Toast only if it never auto-dismisses"
            "no":
              resolve: "Toast"
              confidence: "high"
              rationale: "Standard toast for transient, informational feedback"
              basis: "docs/components/toast.md"
```

### Decision node requirements

Every question node must:
- Ask a single, unambiguous question
- Have mutually exclusive answer options (no overlap between paths)
- Be answerable from the user's requirements (not require implementation knowledge)

Every leaf node must:
- Resolve to exactly one component from the scanned inventory
- Include a confidence level (high, medium, low)
- Include a rationale explaining why this component fits, with a `basis`
- Include `notes` when there is an edge case or alternative (required for medium and low confidence; optional otherwise)

### Confidence levels

- **High**: The decision tree path unambiguously leads to this component. No reasonable alternative exists.
- **Medium**: This is the best fit, but an alternative exists for specific edge cases. The notes field describes the alternative.
- **Low**: Multiple components could serve this need. The tree suggests one based on the most common use case, but the consumer should verify.

---

## Step 4: Add disambiguation nodes

For component pairs that are frequently confused, add explicit disambiguation. Illustrative example: the Dialog/Drawer split and the option-count threshold are one system's conventions, not general rules, so take yours from the system's docs or mark them `proposed`.

```yaml
disambiguation:
  dialog_vs_drawer:
    trigger: "Agent or user is uncertain between Dialog and Drawer"
    question: "Does the user need to see the page behind while they work?"
    options:
      decision_then_return:
        description: "A focused decision or short form; the page is irrelevant until it's done"
        resolve: "Dialog"
        rationale: "Dialogs interrupt, take focus, and close on completion"
        basis: "docs/overlays.md"
      task_alongside_page:
        description: "Editing or browsing something that relates to what's on the page"
        resolve: "Drawer"
        rationale: "Drawers keep the page visible and can stay open while the user works"
        basis: "docs/overlays.md"
      confirming_an_action:
        description: "The user is confirming or cancelling a specific action"
        resolve: "ConfirmationDialog"
        rationale: "Confirmation dialogs are specialised for binary confirm/cancel decisions"
        basis: "proposed"

  select_vs_combobox:
    trigger: "Agent or user is uncertain between Select and Combobox"
    question: "How many options are there, and does the user know what they're looking for?"
    options:
      few_options_user_browses:
        description: "Fewer than [threshold] options, user scans the list"
        resolve: "Select"
        rationale: "Select is simpler and appropriate when the option set is scannable"
        basis: "proposed"
      many_options_user_searches:
        description: "[threshold] or more options, or user typically knows what they want"
        resolve: "Combobox"
        rationale: "Combobox adds search/filter capability for large or known-target option sets"
        basis: "proposed"
      options_are_dynamic:
        description: "Options are loaded from an API or depend on user input"
        resolve: "Combobox"
        rationale: "Combobox supports async loading and filtered results"
        basis: "src/components/Combobox/Combobox.tsx"
```

Set `[threshold]` from the system's docs; if they don't give one, ask, or leave the placeholder and list it in the summary.

---

## Step 5: Generate the output

### The pages (always)

One markdown page per functional cluster in `docs/choosing/` (or the docs platform's equivalent), plus an index:

```
docs/choosing/
  README.md              index: one line per cluster, and the confusable pairs
  notifications.md
  input.md
  overlays.md
  ...
```

Each page renders its tree as the questions in order, with the answer that resolves and why, and ends with a "Confusable pairs" table for its disambiguation nodes:

```markdown
# Choosing a notification component

Start here if you need to tell the user something happened.

1. **Does it need to persist until the user dismisses it?**
   - Yes, and it concerns the current section → **InlineMessage** if it sits in the content flow, **Alert** if it's a distinct block. [docs/components/alert.md]
   - Yes, and it concerns the whole application → **Banner**. [user]
   - No → next question.
2. **Does the user need to act on it?**
   - Yes → **Alert** (persistent). A Toast with an action fails users who can't reach it before it times out. [proposed]
   - No → **Toast**. [docs/components/toast.md]

## Confusable pairs
| If you're torn between | Ask | Choose |
|---|---|---|
| Toast and Banner | Does it need to persist? | Banner if yes, Toast if no |
```

Every resolution carries its basis in brackets, and `[proposed]` marks the ones the team hasn't confirmed. If `agent-instructions` has written `AGENTS.md`, add the `docs/choosing/` link to it (or tell the user to).

### The trees (on request, or when `decision_tree.output_format` is `yaml` or `json`)

```
.ai/decision-trees/
  trees/<cluster>.yml
  disambiguation/<pair>.yml
  intent-taxonomy.yml
  decision-tree-manifest.yml
  query-guide.md
```

The manifest lists each tree with its file, the components it covers and its depth, and the components deliberately left uncovered with the reason (utility components don't need selection logic). Coverage figures are counted from the files written. `query-guide.md` tells an agent how to traverse: map the request to an intent, answer each question from the requirements and ask rather than guess, treat `basis: proposed` as a suggestion, present both paths when two look equally valid, and fall back to name matching for uncovered components. The pages and the trees must say the same thing; generate the YAML from the same decisions, not separately.

---

## Step 6: Summarise in chat

End with a short chat summary:
- **Headline:** how many trees and disambiguation files were written, and which clusters they cover
- **Files written:** the pages under `docs/choosing/`, and any trees under `.ai/decision-trees/`
- **Proposed:** every node with `basis: proposed`, every open placeholder such as `[threshold]`, and any intent the inventory has no component for
- **Scope:** the block from the output-discipline knowledge note, naming the inventory source and anything not scanned

---

## Recommend to the user

- Start with the functional clusters where component confusion is most common — these have the highest return
- Validate decision trees with real scenarios from the team's recent work
- Include disambiguation nodes for every component pair that has caused confusion in the past
- Review uncovered components — utility components genuinely do not need trees, but any component that a user might need to choose between should be covered
- Commit the decision trees alongside component metadata and update them when components are added, deprecated, or significantly changed

---

## Quality checks

- Every decision tree path terminates at a leaf node (no dead ends)
- Question options are mutually exclusive (no overlap between paths)
- Every component that could reasonably be confused with another is covered by either a tree or a disambiguation node
- Confidence levels are honest — "high" means there is genuinely no reasonable alternative, not that the tree author is confident
- Rationale in leaf nodes explains why this component fits, not just which component it is
- The query guide provides clear instructions for handling ambiguity
- Every `resolve:` names a component in the scanned inventory, and every rationale has a `basis`
- Answer keys `"yes"`/`"no"` are quoted (or replaced with descriptive keys) and the files parse as YAML
- The pages are the primary output and read as questions a person can answer; YAML, if written, says the same thing
- Manifest coverage counts are accurate and uncovered components have documented reasons for exclusion
- Decision trees are traversable from user requirements alone — no question requires implementation knowledge or system internals to answer
