# Human oversight framework

**Knowledge note for Design System Ops**
**Auto-loaded by:** governance-encoder, system-health

---

## Why oversight matters in AI-assisted design systems

When AI agents operate within a design system — generating components, selecting patterns, applying tokens, writing documentation — they produce output that affects end users. A misapplied accessibility pattern becomes a barrier for real people. A poorly selected component creates confusion in a real product. An incorrectly generated token override propagates through every consuming application.

The quality and safety of agent output is ultimately a human responsibility. Agents execute; humans are accountable. The oversight framework defines where human judgment is required, what agents are trusted to do autonomously, and how errors are attributed and corrected.

This is not a theoretical concern. As design systems adopt AI tooling, the division of responsibility between agents and humans becomes the central governance question. Teams that do not define this boundary explicitly end up with one of two failure modes: agents that are over-trusted (producing unchecked output that degrades system quality) or agents that are under-trusted (requiring so much human review that the productivity benefit disappears).

---

## The autonomy spectrum

Not all agent actions carry equal risk. The oversight framework assigns every agent action to one of four autonomy levels:

### Level 1: Fully autonomous

The agent performs the action without human review. These are low-risk, high-confidence operations where the cost of an error is trivial and easily reversible.

**Examples:**
- Generating a prop type list from a TypeScript interface
- Formatting a token value into a different notation
- Producing a component inventory from file system scanning
- Listing which components use a given token

**Criteria for Level 1:**
- The action is deterministic or near-deterministic
- The output can be validated programmatically
- An error is immediately detectable and cheaply reversible
- The action does not modify the published system

### Level 2: Autonomous with audit trail

The agent performs the action autonomously but logs every decision for asynchronous human review. Humans review the audit trail periodically, not in real time.

**Examples:**
- Generating a first draft of a component description
- Suggesting a component selection for a given requirement
- Identifying potential drift between design and implementation
- Producing a metadata schema from source code analysis

**Criteria for Level 2:**
- The action involves judgment but follows established patterns
- The output quality varies but is generally acceptable
- An error is detectable by periodic review
- The action does not publish or deploy anything

### Level 3: Human-in-the-loop

The agent prepares the action and presents it for human approval before execution. The human reviews, modifies if needed, and explicitly approves.

**Examples:**
- Publishing a component update to the design system package
- Applying a breaking change to a token value
- Generating and publishing component documentation
- Modifying a governance rule
- Creating a new component from a design spec

**Criteria for Level 3:**
- The action modifies the published system
- The consequences of an error affect downstream consumers
- The action involves creative or strategic judgment
- Reversal is possible but costly (requires a new release, communication to consumers)

### Level 4: Human only

The agent is explicitly prohibited from performing this action. These are actions where the risk is too high, the judgment too nuanced, or the accountability too important to delegate.

**Examples:**
- Removing a component from the system
- Changing the design system's architectural direction
- Approving an exception to a governance rule
- Making decisions about inclusive design policy
- Setting accessibility compliance targets

**Criteria for Level 4:**
- The action is irreversible or extremely costly to reverse
- The action requires organisational context that agents cannot possess
- The action carries ethical or legal implications
- Accountability must be attributable to a named person

---

## Error attribution model

When agent output is wrong, someone is responsible. The error attribution model defines who:

### Agent-attributable errors

Errors caused by the agent's processing, even when given correct input:

- **Hallucination**: The agent generated output that contradicts the data it was given (e.g., listing a prop that does not exist in the TypeScript interface)
- **Misapplication**: The agent applied a rule correctly but to the wrong context (e.g., applying form validation rules to a display component)
- **Outdated context**: The agent used stale data because its context was not refreshed (e.g., referencing a deprecated component)

**Response:** Fix the agent's context, improve the prompt or instruction set, or add a validation gate.

### System-attributable errors

Errors caused by incomplete or incorrect system data:

- **Missing metadata**: The component lacked the metadata needed for the agent to make a correct decision (e.g., no anti-patterns documented, so the agent produced a known anti-pattern)
- **Ambiguous documentation**: The documentation was unclear enough that the agent's interpretation, while wrong, was reasonable
- **Inconsistent data**: Different sources (Figma, code, docs) provided conflicting information

**Response:** Fix the system data. The error is a signal that the system's AI readiness has a gap.

### Human-attributable errors

Errors caused by humans in the oversight chain:

- **Insufficient review**: A human approved agent output without adequate review (Level 3 action rubber-stamped)
- **Incorrect override**: A human modified agent output and introduced an error
- **Missing governance**: No governance rule existed to prevent the error, and no human had defined one

**Response:** Improve the review process, update governance rules, or adjust the autonomy level for the action.

### Attribution workflow

When an error is detected:

1. **Classify the error** against the three attribution categories
2. **Trace the chain**: What data did the agent receive? What did it produce? Who reviewed it?
3. **Assign attribution** to the appropriate category (agent, system, or human)
4. **Define the corrective action** based on the attribution
5. **Update the oversight framework** if the error reveals that an action's autonomy level is too high

---

## Review cadences

Different autonomy levels require different review rhythms:

| Level | Review type | Cadence | Reviewer |
|---|---|---|---|
| Level 1 (autonomous) | Spot check | Monthly | Any team member |
| Level 2 (audit trail) | Audit review | Weekly | Component team lead |
| Level 3 (human-in-loop) | Per-action review | Every action | Designated approver |
| Level 4 (human only) | Not applicable | Not applicable | Named decision maker |

### Audit trail requirements

For Level 2 actions, the audit trail must capture:
- What the agent did (action type, input, output)
- When (timestamp)
- What context the agent used (which metadata files, which version)
- What confidence level the agent reported
- Whether a human subsequently reviewed and confirmed or corrected the output

### Escalation triggers

Certain patterns in audit trail data should trigger escalation from one autonomy level to a higher one:

- **Error rate threshold**: If a Level 2 action's error rate exceeds 10% over a review period, escalate to Level 3 until the root cause is resolved
- **Consistency drift**: If agent output for the same input varies significantly across runs, escalate until the non-determinism is understood
- **Scope expansion**: If an agent action's blast radius increases (e.g., it now affects more consumers), reassess the autonomy level
- **Policy change**: If the governance rules change, reassess all autonomy level assignments

---

## Oversight integration with skills

Skills in the Design System Ops product should reference this framework when their output involves different autonomy levels. Specifically:

**Skills that produce Level 1 output** (inventories, audits, reports):
- No additional oversight requirements
- Output is informational and does not modify the system

**Skills that produce Level 2 output** (descriptions, metadata, decision trees):
- Recommend audit trail logging
- Flag output as "draft" or "suggested" — not "final"
- Include confidence indicators in the output

**Skills that produce Level 3 output** (governance rules, release decisions, published documentation):
- Explicitly state that human review is required before the output takes effect
- Structure output to facilitate review (show what changed, highlight decisions, flag uncertainty)
- Never auto-publish or auto-deploy

**Skills that reference Level 4 actions** (system architecture, policy decisions):
- Present the relevant information and analysis
- Explicitly state that the decision belongs to a named human role
- Do not make the decision or frame the output as a recommendation to act

---

## Measuring oversight effectiveness

Track these metrics to assess whether the oversight framework is calibrated correctly:

- **Error escape rate**: Errors that reach consumers without being caught by oversight. Target: trending down.
- **Review throughput**: Time from agent output to human review completion. If this is too long, Level 3 gates become bottlenecks.
- **False positive rate**: Agent actions flagged for review that turned out to be correct. If this is too high, the autonomy level is too conservative.
- **Attribution distribution**: What percentage of errors are agent-attributable vs system-attributable vs human-attributable? This distribution reveals where to invest improvement effort.
- **Autonomy level migration**: How many actions have been escalated or de-escalated over time? Healthy systems show a gradual trend toward higher autonomy as confidence increases.
