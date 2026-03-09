---
name: session-memory
description: "Persist and recall findings across skill runs within and between sessions, building a cumulative knowledge base of what has been discovered about a design system. This is the cross-skill memory layer — it saves what was found, when, and by which skill, so future runs can compare, correlate, and avoid repeating work. Trigger when someone says: save these findings, remember this for later, compare with last run, what did we find before, load previous findings, recall the last audit, session history, show me what changed, cross-reference with previous runs, or anything about persisting, recalling, or comparing findings over time. Do NOT trigger for generating a single standalone report — use the specific skill for that. Do NOT trigger for running a full diagnostic — use full-system-diagnostic for that."
references:
  - references/agent-orchestration-guide.md
  - references/human-oversight-framework.md
---

# Session Memory

A skill for persisting findings across skill runs so that future skills can compare, correlate, and build on what was previously discovered.

**Output type:** Memory file creation and recall. This skill writes structured session files and retrieves previous session data. It does not produce analysis — it provides the memory layer that other skills draw from.

---

## Why this exists

Every skill in Design System Ops produces findings. But those findings are ephemeral — they exist in the conversation, get summarised, and then vanish. The next time someone runs token-audit, it starts from zero. It cannot tell you whether things got better or worse since last quarter. It cannot cross-reference what drift-detection found last month with what component-audit finds today.

Session Memory fixes this. It creates a structured memory layer that:

1. **Saves findings** from any skill run with timestamps, severity, and skill provenance
2. **Recalls findings** when a skill asks "what did we find before?"
3. **Compares findings** between runs to surface trends (improving, stable, worsening)
4. **Correlates findings** across skills to surface patterns that persist over time

This is not a database. It is a structured markdown file per session that accumulates over time. Simple, portable, and readable by both humans and AI.

## Boundaries

This skill is a persistence layer — it saves, recalls, compares, and correlates findings. It does not run audits, produce reports, or generate recommendations on its own. If no previous session files exist and the mode is Recall, Compare, or Correlate, inform the user that there is no history to work with and suggest running an audit first. If the session memory directory does not exist, create it on Save. Do not correlate across skills unless at least two different skill sessions exist — a single-skill history is a Compare, not a Correlate.

---

## Configuration

Check for `.ds-ops-config.yml` in the project root:

```yaml
memory:
  directory: ".ds-ops/sessions"     # Where session files are stored
  retain_count: 12                   # How many session files to keep
  auto_save: true                    # Automatically save after every skill run
  comparison_window: 3               # How many previous sessions to compare against
```

If no configuration exists, use these defaults:
- Directory: `.ds-ops/sessions/`
- Retain count: 12
- Auto-save: true
- Comparison window: 3

---

## Session file format

Each session file is a structured markdown document saved to the memory directory. One file per skill run.

### Filename convention

`[YYYY-MM-DD]-[skill-name]-[short-hash].md`

Example: `2026-03-09-token-audit-a7f3.md`

The short hash is the first 4 characters of a hash of the input parameters, ensuring uniqueness when the same skill is run twice on the same day with different inputs.

### File structure

```markdown
---
skill: token-audit
date: 2026-03-09
scope: "AGDS token architecture"
system: "Australian Government Design System"
component_count: 42
---

# Session: token-audit — 2026-03-09

## Summary
[2–3 sentence summary of what was found]

## Key metrics
| Metric | Value |
|---|---|
| Total tokens | 140 |
| Violations | 12 |
| Critical | 2 |
| High | 4 |
| Orphaned tokens | 45 (32%) |

## Findings
### TA-01 [Critical] — Missing semantic tier for feedback tokens
[One paragraph description]

### TA-02 [High] — Orphaned primitive tokens in legacy palette
[One paragraph description]

[... all findings ...]

## Recommendations
1. [First recommendation]
2. [Second recommendation]

## Cross-references
- Correlates with: [any related findings from prior sessions, or "None — first run"]
- Trend: [Improving / Stable / Worsening / New baseline]
```

---

## Step 0: Determine the operation

Session Memory has four modes. Determine which one based on the request:

### Mode A — Save
Someone ran a skill and wants the findings persisted.

### Mode B — Recall
Someone wants to see what was found in previous runs before running a new skill.

### Mode C — Compare
Someone wants to compare current findings against previous runs to see trends.

### Mode D — Correlate
Someone wants to cross-reference findings across different skills to surface persistent patterns.

---

## Step 1: Save (Mode A)

### Input
Accept findings from any skill output: copy-pasted report, file reference, or inline conversation output.

### Process

1. **Parse the skill output** and extract:
   - Skill name (from the output header or context)
   - Date (today)
   - Scope (what was assessed)
   - System name (from config or context)
   - Component count (if available)
   - Key metrics (counts, scores, percentages)
   - Individual findings with IDs, severities, and descriptions
   - Recommendations

2. **Check for prior sessions** from the same skill:
   - If prior sessions exist, add a `## Trend` section comparing key metrics
   - Calculate deltas: "Violations: 12 → 8 (↓ 33%)"
   - Note new findings not present in the previous run
   - Note resolved findings present previously but absent now

3. **Check for cross-skill correlations**:
   - Load the most recent session file from every other skill
   - Look for findings that reference the same components, tokens, or areas
   - If correlations exist, add them to the `## Cross-references` section
   - Example: "TA-01 (missing feedback tokens) correlates with CA-03 (no feedback component) from component-audit run on 2026-02-15"

4. **Write the session file** to the memory directory using the filename convention

5. **Prune old sessions** if the total exceeds `retain_count`. Delete the oldest files first. Never delete files from the current quarter.

### Output

Confirmation message:

```
Session saved: 2026-03-09-token-audit-a7f3.md
Location: .ds-ops/sessions/
Findings: 12 (2 Critical, 4 High, 4 Medium, 2 Low)
Trend: Improving — violations down from 18 to 12 since 2026-01-15
Cross-references: 2 correlations found with previous component-audit run
```

---

## Step 2: Recall (Mode B)

### Input
A skill name, a date range, or "everything."

### Process

1. **List all session files** in the memory directory
2. **Filter** by the requested skill or date range
3. **Load and summarise** each matching file
4. **Present as a timeline**:
   - Most recent first
   - Key metrics per run
   - Trend arrows between runs

### Output

```markdown
## Session history: token-audit

| Date | Violations | Critical | Trend |
|---|---|---|---|
| 2026-03-09 | 12 | 2 | ↓ Improving |
| 2026-01-15 | 18 | 4 | ↑ Worsening |
| 2025-10-20 | 14 | 3 | Baseline |

### Most recent findings (2026-03-09)
- TA-01 [Critical] — Missing semantic tier for feedback tokens
- TA-02 [High] — Orphaned primitive tokens in legacy palette
[...]
```

---

## Step 3: Compare (Mode C)

### Input
Two specific session files, or "compare latest with previous."

### Process

1. **Load both session files**
2. **Align findings by ID** (TA-01 in run A vs. TA-01 in run B)
3. **Classify each finding:**
   - **Resolved:** Present in old run, absent in new → good news
   - **Persistent:** Present in both runs → still needs work
   - **New:** Absent in old run, present in new → regression or new scope
   - **Changed severity:** Present in both but severity shifted
4. **Calculate metric deltas:**
   - Total violations: old → new (delta, percentage)
   - Per-severity breakdown
   - Any new categories or disappeared categories
5. **Produce a comparison report**

### Output

```markdown
## Comparison: token-audit

**Period:** 2026-01-15 → 2026-03-09 (53 days)

### Metric deltas
| Metric | Previous | Current | Delta |
|---|---|---|---|
| Total violations | 18 | 12 | ↓ 6 (−33%) |
| Critical | 4 | 2 | ↓ 2 (−50%) |
| Orphaned tokens | 52 (38%) | 45 (32%) | ↓ 7 (−6pp) |

### Finding status
| Status | Count | Findings |
|---|---|---|
| Resolved | 4 | TA-04, TA-07, TA-12, TA-15 |
| Persistent | 8 | TA-01, TA-02, TA-03, TA-05, TA-06, TA-08, TA-09, TA-11 |
| New | 2 | TA-16, TA-17 |
| Changed severity | 2 | TA-03 (Critical → High), TA-09 (High → Medium) |

### Interpretation
The system is improving. Critical violations dropped by 50%, and four findings from the previous run have been resolved. Two new findings emerged — both related to a new token category introduced since the last audit. The persistent findings (TA-01, TA-02) should be prioritised for the next sprint.
```

---

## Step 4: Correlate (Mode D)

### Input
"What patterns persist across skills?" or a specific area to investigate.

### Process

1. **Load the most recent session file from every skill**
2. **Index all findings** by:
   - Component name (if applicable)
   - Token name or category (if applicable)
   - Area or team (if identifiable)
   - Severity
3. **Look for convergence:**
   - Same component appears in findings from 2+ skills
   - Same area has violations across token, naming, and component audits
   - Same severity clustering across skills
4. **Rate each correlation:**
   - 2 skills = Possible correlation
   - 3 skills = Probable correlation
   - 4+ skills = Confirmed systemic issue
5. **Produce a correlation report**

### Output

```markdown
## Cross-skill correlation report

**Sessions analysed:** 5 (token-audit, naming-audit, component-audit, drift-detection, system-health)
**Date range:** 2026-01-15 to 2026-03-09

### Confirmed systemic issues (4+ skills)

**Feedback component area**
- token-audit: Missing semantic tier for feedback tokens (TA-01, Critical)
- naming-audit: Inconsistent naming in alert/toast/notification components (NA-06, High)
- component-audit: No feedback component in library (CA-03, High)
- drift-detection: 4 teams building custom feedback patterns (DD-08, High)
- Impact: Every skill surfaces this gap. This is the system's highest-priority structural gap.

### Probable correlations (3 skills)

**Legacy colour palette**
- token-audit: 45 orphaned primitive tokens from legacy palette (TA-02, High)
- naming-audit: Legacy tokens use different naming convention (NA-02, Medium)
- component-audit: 3 components still reference legacy palette directly (CA-11, Medium)

### Possible correlations (2 skills)
[...]
```

---

## Integration with other skills

Any skill can trigger a session save by including this instruction at the end of its output:

> Save these findings to session memory.

Any skill can request previous findings by including:

> Before starting, recall the most recent session for [skill-name].

The full-system-diagnostic agent should automatically save each phase's output and load all previous sessions at the start of Phase 3 (synthesis).

---

## Quality checks

- Session files follow the naming convention exactly
- Every finding has an ID, severity, and description
- Trend calculations are mathematically correct (verify deltas)
- Cross-references cite specific finding IDs from specific sessions, not vague references
- Comparison reports classify every finding (resolved, persistent, new, changed)
- Correlation thresholds use the correct levels (2/3/4+ skills)
- Old sessions are pruned correctly without deleting current-quarter files
- The memory directory path is consistent across all operations
