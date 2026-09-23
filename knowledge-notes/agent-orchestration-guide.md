---
name: agent-orchestration-guide
type: knowledge
---

# Agent orchestration guide

**Knowledge note for Design System Ops**
**Auto-loaded by:** system-health, governance-encoder, context-engine-builder

---

## What agent orchestration means for design systems

A single AI agent working with a design system can generate a component, write a description, or audit a token file. Multiple agents working together can take a design spec and produce a fully documented, tested, accessible component with governance checks and release readiness — without a human touching the keyboard between steps.

Agent orchestration is the coordination layer that makes multi-agent workflows reliable. It defines how agents hand off work to each other, what context flows between them, how conflicts are resolved, and where humans intervene.

This matters for design systems specifically because design system work is inherently multi-disciplinary. A single component touches design (visual spec), engineering (implementation), documentation (descriptions), accessibility (contracts), governance (compliance), and quality (testing). No single agent covers all of these dimensions. Orchestration is how specialised agents collaborate across them.

---

## Orchestration patterns

### Sequential chain

Agents execute in order. Each agent completes its work and passes the result to the next.

```
Design spec → [Component Generator] → [Description Writer] → [Accessibility Auditor] → [Release Validator]
```

**When to use:** Linear workflows where each step depends on the previous step's output. The most common pattern for component creation and documentation workflows.

**Strengths:** Simple to reason about, easy to debug (failures are traceable to a specific step), clear audit trail.

**Weaknesses:** Slow (no parallelism), fragile to early failures (a failure at step 2 blocks steps 3–4), and context can degrade over long chains as each agent only sees its predecessor's output.

**Context passing rule:** Each step receives the original input plus a short hand-off card from the steps before it — not their full output. Passing whole reports down a long chain buries the findings that matter under scaffolding and contradicts the minimal context principle below. The card format for Design System Ops chains is in [Chained-run rules](#chained-run-rules).

### Parallel fan-out

Multiple agents execute simultaneously on the same input, and their outputs are merged.

```
Component source → [Token Auditor] ──┐
                 → [A11y Auditor]  ──┼→ [Report Merger] → Combined audit report
                 → [Naming Auditor] ─┘
```

**When to use:** Independent assessments of the same artefact. Auditing workflows are natural candidates because each audit dimension is independent.

**Strengths:** Fast (parallel execution), resilient (one agent's failure does not block others), produces comprehensive output.

**Weaknesses:** Requires a merge step that understands all output formats, potential for conflicting findings (e.g., naming auditor suggests a rename that breaks the codebase index).

**Conflict resolution rule:** When parallel agents produce conflicting recommendations, the merge step flags the conflict for human resolution rather than picking a winner. No agent should override another agent's findings.

### Supervisor pattern

A coordinating agent decides which specialist agents to invoke based on the task requirements.

```
User request → [Supervisor] → decides which agents to call
                            → [Agent A] → result A
                            → [Agent B] → result B
                            → [Supervisor] → assembles final output
```

**When to use:** Complex tasks where the required agents are not known in advance. The supervisor analyses the request and determines which specialists are needed.

**Strengths:** Flexible (adapts to varied requests), efficient (only invokes necessary agents), can handle multi-step reasoning.

**Weaknesses:** The supervisor is a single point of failure, supervisor quality determines overall quality, and the supervisor needs awareness of all available agents and their capabilities.

**Supervisor requirements:** The supervisor agent must have access to the full agent registry (what agents exist, what each does, what input each requires, what output each produces) and the orchestration rules (which agents can be parallelised, which must be sequential, which require human gates).

### Feedback loop

An agent produces output, a reviewer agent evaluates it, and the original agent revises based on feedback.

```
[Generator] → output → [Reviewer] → feedback → [Generator] → revised output → [Reviewer] → approved
```

**When to use:** Quality-critical output where a single pass is insufficient. Component descriptions, documentation, and governance rules benefit from a generation-review-revision cycle.

**Strengths:** Produces higher quality output than single-pass generation, catches errors that the generator's own validation misses.

**Weaknesses:** Can loop indefinitely if convergence criteria are not defined. Always set a maximum iteration count (recommended: 3 iterations maximum).

**Convergence rule:** The loop terminates when the reviewer reports no findings above a configured severity threshold, or when the maximum iteration count is reached. If the loop reaches the maximum without converging, the output is flagged for human review.

---

## Context management

The single most important aspect of multi-agent orchestration is context management — ensuring that each agent receives the context it needs, no more and no less.

### Context types

**System context** — persistent knowledge about the design system that all agents share:
- Component inventory and relationships
- Token architecture and values
- Governance rules and constraints
- Accessibility requirements
- Content and voice guidelines

System context is loaded once and shared. It changes only when the design system itself changes.

**Task context** — information specific to the current task:
- The user's request or the triggering event
- Constraints and requirements for this specific task
- Outputs from previous agents in the chain

Task context is created per workflow execution and flows between agents.

**Agent context** — information specific to an individual agent's role:
- The agent's prompt and instructions
- The agent's available tools and capabilities
- The agent's output format requirements

Agent context is static per agent configuration.

### Context loading strategy

Not every agent needs every piece of system context. Loading the full design system context into every agent wastes tokens and can degrade performance (agents perform better with focused context).

**Minimal context principle:** Each agent should receive only the system context relevant to its task. A token auditor needs the token architecture but not the content guidelines. An accessibility auditor needs the accessibility contracts but not the business intelligence blueprint.

**Context manifest:** Maintain a mapping of which system context files each agent type requires:

```yaml
agent_context_map:
  component_generator:
    required: [component-inventory, technical-blueprint, ui-blueprint]
    optional: [accessibility-blueprint, content-blueprint]
  description_writer:
    required: [ai-readiness, component-bestiary]
    optional: [content-blueprint]
  token_auditor:
    required: [token-architecture, ui-blueprint]
    optional: [component-inventory]
  accessibility_auditor:
    required: [accessibility-blueprint]
    optional: [component-inventory, technical-blueprint]
```

### Context freshness

Stale context is a major source of agent errors. If the token architecture changed last week but the agent is still using last month's context, it will produce output based on an outdated token set.

**Freshness rules:**
- System context files should include a version or last-modified timestamp
- Before starting a workflow, verify that the system context is current
- If context files are stale (older than the configured threshold), refresh before proceeding
- If refresh fails, warn the user that the output may be based on outdated context

---

## Handoff protocols

When one agent passes work to another, the handoff must include:

### Required handoff fields

```yaml
handoff:
  from_agent: "component_generator"
  to_agent: "description_writer"
  timestamp: "2026-03-09T14:30:00Z"
  task_id: "task-001"
  status: "completed"
  output:
    type: "component_source"
    location: "src/components/NewComponent.tsx"
    summary: "Generated a form field component with text input, label, helper text, and error state"
  context_additions:
    - "Component has 8 props including variant, size, disabled, error, helperText"
    - "Component composes Input, Label, and HelperText atoms"
  open_questions:
    - "Should the error state use inline message or tooltip for error display?"
  confidence: "high"
  next_action: "Write six-section component description"
```

### Handoff validation

Before accepting a handoff, the receiving agent should verify:
- The output from the previous agent exists and is accessible
- The output format matches what the receiving agent expects
- Any open questions are either answerable from context or flagged for human input
- The confidence level from the previous agent does not indicate unresolved issues

If validation fails, the receiving agent should report the failure rather than proceeding with incomplete or invalid input.

---

## Failure handling

Multi-agent workflows fail. The orchestration layer must handle failures gracefully.

### Failure categories

**Recoverable failures** — the agent can retry or an alternative path exists:
- Timeout (retry with extended timeout)
- Missing context file (attempt to load from alternative source)
- Low confidence output (retry with additional context or escalate to human)

**Non-recoverable failures** — the workflow cannot proceed:
- Required input is missing and no source exists
- The agent produced output that fails validation and has exhausted retry attempts
- A human gate is required but no human is available

### Failure response protocol

1. **Log the failure** with full context (agent, input, error, timestamp)
2. **Assess recoverability** against the failure categories
3. **If recoverable:** retry or reroute, then continue the workflow
4. **If non-recoverable:** halt the workflow, preserve all completed work, and report to the user what was completed and where the failure occurred
5. **Never silently skip a failed step** — a skipped audit is worse than a failed audit because the consumer assumes the audit passed

---

## Orchestration in Design System Ops

The Design System Ops product organises orchestration through agent chains — predefined sequences of skills that execute as a coordinated workflow.

### Existing agent chains

The product's agents live at `skills/*-agent.md` and are invoked by the slash commands in `commands/` (for example, `/full-diagnostic` loads `skills/full-system-diagnostic-agent.md`). They are orchestration configurations, not standalone skills. Each agent specifies:
- Which skills to invoke and in what order
- What context each skill receives
- Where human gates exist in the chain
- What output format the chain produces

### Chained-run rules

Every agent follows these rules. The agent file holds only what is specific to its chain.

**Loading**
- Read `output-discipline.md` once per run, at the start.
- Check that the knowledge notes the chained skills reference exist once per run, not once per skill. If any are missing, stop and report it, as each skill's own self-check would.
- Load each chained skill, and the knowledge notes it references, only when its step starts. Don't read every skill up front.

**One inventory**
- Build one inventory before the first step: component source paths, token files, documentation sources (Storybook build, docs platform, MDX), and the consuming repositories in scope.
- Every step uses it and skips its own discovery step (token-audit's Step 0, component-audit's and docs-coverage's inventory steps, system-health's Step 0 where it would re-scan). If a step needs something the inventory lacks, add it to the inventory and note that in the next hand-off card.

**Hand-off card**

Between steps, pass a short card, not the full output:

```markdown
**Hand-off: [skill] → [next skill]**
- **Inventory:** [paths used; anything added this step]
- **Key counts:** [the two or three figures the next step or the synthesis needs]
- **Top findings:** [up to 3, each with 🔴/🟠/🟡/⚪ severity and file evidence]
- **Inspected vs inferred:** [what was read directly; what was inferred or reported]
- **Open questions:** [anything the user needs to answer]
```

Keep each step's full findings available so the user can ask for them, but don't carry them forward.

**One report**
- Chained skills return findings only: no opening headline, no Scope block, no closing note, and no recurring save or compare of their own.
- The agent writes one headline sentence to open the report, one combined Scope block (per output-discipline) covering every step, and one closing note inviting the user to flag intentional deviations.
- Provenance ("Generated by", date, scope, assessment method) goes in a one-line footer, not above the headline.
- Status labels, severity labels and maturity stages follow output-discipline. No numeric scores.

**Permissions and gaps**
- If a step needs a tool the run isn't permitted to use (for example, Figma MCP tools, which no command pre-approves), skip it and record the skip under "Not inspected" in the Scope block. Never skip silently.
- If access is partial, proceed with what's available and list the gaps in Scope. A partial run with explicit gaps is more useful than a delayed complete one.

**Configuration**
- If `.ds-ops-config.yml` exists in the project root, read it once. Configured integrations and `severity.*` settings apply to every chained skill, so severity is consistent across the run. Don't re-configure per skill.

**Recurring runs and session memory**
- If `recurring` is configured, the agent as a whole loads the previous run of the same agent from `recurring.output_directory`, compares against it, saves the new output there, and prunes per `recurring.retain_count`. Individual skills in the chain don't save or compare.
- If session memory is enabled, save the combined output once, at the end of the run.

### Adding orchestration to new skills

When creating a new skill that participates in agent chains:
- Define the skill's input contract (what context it requires)
- Define the skill's output contract (what it produces and in what format)
- Specify which agent chains the skill can participate in
- Document handoff requirements (what the previous skill must provide, what the next skill expects)

### Orchestration anti-patterns

**Context hoarding:** An agent that loads all system context regardless of need. This wastes tokens and can cause the agent to attend to irrelevant information.

**Silent degradation:** An agent that produces partial output without flagging what was skipped. The next agent in the chain receives incomplete input and may produce subtly wrong output.

**Retry storms:** An agent that retries indefinitely on failure. Set maximum retry counts and escalate to human after exhaustion.

**Implicit ordering:** Agents that must run in a specific order but the ordering is not documented. All ordering constraints should be explicit in the orchestration configuration.

---

## Measuring orchestration health

Track these metrics to assess whether orchestration is working:

- **Chain completion rate**: What percentage of multi-agent workflows complete successfully end-to-end?
- **Handoff failure rate**: What percentage of agent-to-agent handoffs fail validation?
- **Context load efficiency**: What is the average context size per agent relative to the minimum required context? (Lower is better — indicates focused context loading)
- **Human intervention rate**: How often do workflows stop at human gates? If this is too high, the autonomy levels may be too conservative. If too low, the oversight may be insufficient.
- **Mean time to completion**: Average wall-clock time from workflow start to final output. Track this over time to identify degradation.
