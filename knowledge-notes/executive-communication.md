---
name: executive-communication
type: knowledge
---

# Executive communication

**Knowledge note for Design System Ops**
**Auto-loaded by:** system-pitch, stakeholder-brief

---

## Numbers honesty

Leadership documents get forwarded, quoted in budget meetings and checked months later. A number that turns out to be invented costs more credibility than the whole document earned. This is output-discipline's "Every figure and fact needs a source" rule, applied to briefs and pitches.

- **Label every figure.** Measured (from a named source: a file, a tool output, a prior skill's report, or the user), estimated (with the reasoning shown), or assumed (stated as an input the reader can change). A figure with none of these labels doesn't go in.
- **Recompute every derived figure.** Totals, ROI, payback and FTE equivalents are recalculated from the inputs shown, every time. Payback is the first month in which cumulative benefit is at least cumulative cost, not the month a single year's benefit would cover a single year's cost.
- **One loaded hourly rate.** Cost the investment and value the benefit at the same loaded rate, stated as an assumption. Valuing saved hours at $150 while costing an FTE at $150,000 a year (about $72 an hour) inflates the return by half.
- **No conclusion fixed before the data.** Don't decide that the case pays back and then pick inputs until it does. If the honest inputs don't pay back, say so and narrow the ask.
- **No borrowed benchmarks.** Industry figures ("teams with mature systems ship 30% faster") go in only when the user supplies the source, and the source is cited.
- **Gaps stay visible.** Unknown figures are written as `[needs data: what's missing]`, and a document meant to be sent lists its open placeholders at the top.
- **Close with provenance.** End with one line: `Based on: [sources, with dates]`, so the reader can check where the figures came from.

---

## Audience calibration

Different readers fund different outcomes. Pick the primary reader and calibrate to them; a combined audience gets the executive framing.

| Audience | What they care about | Lead with | Language that lands | Avoid |
|---|---|---|---|---|
| Engineering leadership | Technical debt, velocity, maintenance burden, reliability | Duplicated engineering effort; the system as shared platform infrastructure | Engineering velocity, technical debt, maintenance burden, system reliability, platform dependency | Design terminology without translation; aesthetic arguments without an engineering benefit; efficiency claims without numbers |
| Product leadership | Customer experience, feature velocity, time-to-market, competitive position | The inconsistent customer experience; speed from composing proven components | Customer experience, feature velocity, time-to-market, customer trust, competitive positioning | Implementation detail; component counts that mean nothing outside design; process without customer impact |
| Design leadership | Design quality, consistency, scalability of design work | Fragmented patterns undermining design intent; design leverage (designers freed for novel problems) | Design consistency, design quality, design scalability, design leverage, design standards | Engineering-only metrics; implementation choices as the main point; process-heavy governance language |
| Executive / C-level | Strategic alignment, risk, financial return, organisational efficiency | The strategic goal the system enables, the risk of the current state, and the money | Strategic alignment, return on investment, operational efficiency, risk exposure, platform infrastructure, scalability | Design and engineering jargon equally; specific components; any assumption that the reader knows what a design system is |

Two framings work for every audience:

- **Infrastructure, not design convenience.** "Teams are creating parallel infrastructure because the shared platform doesn't cover their needs" rather than "teams are building outside the system". "The infrastructure needs a defined service level: response time for bug reports, a predictable release cadence, documented API contracts" rather than "we need a dedicated team".
- **Maturity as a named stage.** If a system-health assessment gave a maturity stage, use its name (Ad-hoc, Managed, Systematic, Measured, Optimised), explain it in one plain sentence, and frame the recommendation as the transition to the next stage. The stages and what each transition requires are in the component-governance note. Never use numbered levels.

---

## Framing patterns

The same situation can lead three ways. Choose the one that matches the reader's priorities.

**Lead with growth** — when the system enables scale or speed. Pattern: "We are currently [current state]. To [strategic goal], we need [investment]. This will [specific speed or scale benefit]." Works for product leadership, executives, growth-stage organisations, and cases where the system enables new products or markets.

**Lead with risk** — when there is technical, compliance or user-facing risk. Pattern: "We are currently [current state], which creates [specific risk]. The cost of this risk is [impact]. We can remove it by [investment]." Example: separate accessibility implementations across teams create legal exposure and exclude users; centralising the implementation in the system removes that. Works for executives and compliance-conscious organisations, and for preventing a repeat incident.

**Lead with cost** — when the problem is efficiency or waste. Pattern: "We are currently [current state], which costs us [figure, labelled]. We can recover this by [investment]." Works for engineering leadership, finance-conscious organisations, and cases where the cost can be quantified from real inputs.

---

## Translating system metrics

System metrics don't land with a business audience until they're translated into consequences. Choose the one or two translations most relevant to the reader; eight consequences read as a list of complaints.

| Design system metric | Business translation |
|---|---|
| Low token adoption | "Visual inconsistency across products is creating a fragmented brand experience" |
| High component drift | "Teams are maintaining separate versions of the same interface elements, duplicating engineering effort" |
| Poor documentation coverage | "New team members take longer to become productive because system knowledge is tribal, not documented" |
| Accessibility failures found in audit | "We have documented compliance gaps that create legal exposure and exclude users with disabilities" |
| Declining adoption | "Teams are choosing to build independently rather than use shared infrastructure — the system is not serving their needs" |
| No AI-readiness | "Our component library cannot be consumed reliably by AI development tools, so we are not benefiting from AI-assisted coding" |
| Version lag across teams | "Multiple teams are running outdated versions, so bug fixes and improvements are not reaching users" |
| Missing governance process | "There is no defined process for how the system evolves, which creates unpredictability for the teams that depend on it" |

The translation carries the evidence with it: "documented compliance gaps" needs the audit it came from cited in the `Based on:` line.

---

## Anti-patterns

These cost credibility faster than anything else in a leadership document.

- **Reporting only good news.** Readers detect cherry-picking and wonder what is hidden. Lead with the honest picture: what is working and what is not, with the evidence for both.
- **Jargon without translation.** "Low token adoption and declining API consistency" loses a non-design reader in the first sentence. Translate everything: "teams are not using the shared design values consistently, so interfaces look different across products even when they should look the same".
- **Leading with tooling.** Nobody funds Figma, Storybook and React. Lead with what changes for the business; mention tools in passing if at all.
- **Asking for resources without the arithmetic.** "Please allocate 1 FTE" gives the reader no way to judge whether that is reasonable. Show the cost of the current state, the cost of the ask, and the recomputed payback, with every input labelled.
- **Presenting data without interpretation.** "34% of teams use the system" leaves the reader guessing whether that is good. Say what the figure means and what it points to.
- **Too many asks, or asks scattered through the text.** Three asks or fewer, stated together in one section. Everything else builds the case for those asks.
- **Asking for too much too soon, or mixing the ask with the vision.** A multi-year, multi-scope ask feels unmovable and gets approved as something other than what was meant. Ask for the first phase; ask for the next once the first is delivering.
- **Presenting a component library as a design system.** A library without governance, documentation standards and adoption support is a code artefact teams won't trust. Name the parts that make it a system.
- **Ignoring a previous attempt.** If the organisation tried before and it didn't stick, readers remember. Name what happened and what is specifically different this time.
- **Overpromising.** "Eliminate all inconsistency, halve engineering time" creates expectation debt that is paid in trust when the outcomes don't fully arrive. Be specific about what the investment will do, and name what it will not.

---

## Getting to a decision

This is guidance for the person sending the document, not content for the document itself.

- Send it to the decision-maker or budget owner directly, not to their staff, and say when the decision is needed.
- Allow time for questions: about a week before a decision meeting for a brief; two to three weeks before a budget deadline for an investment pitch.
- Offer a follow-up conversation. If there's no decision after two weeks, ask whether there are questions or the proposal needs adjusting.
- If the answer is no, ask why. The real objection is often not the one the document addressed (timing, a competing priority, missing product buy-in), and knowing it shapes the next attempt.
- If the answer is yes, confirm the scope, timeline and success measures, record the decision (the decision-record skill does this), and plan the communication to consuming teams.
