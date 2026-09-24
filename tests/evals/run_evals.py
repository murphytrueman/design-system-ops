#!/usr/bin/env python3
"""Run skills against the fixture design system and check what they find.

The unit tests check what the skills say. This checks what they do: each case
in cases.json runs one skill, headless, against a fresh copy of
tests/fixtures/sample-ds and checks the output names the planted problem
("finds") without flagging the things that are correct ("must_not_flag").

It calls Claude, so it costs real usage and isn't part of ./tests/run.sh or
CI. Run it before a release (see "Install rehearsal" in CONTRIBUTING.md) or
after changing a skill that has a case.

Usage:
  python3 tests/evals/run_evals.py                  # every case, against a fresh build
  python3 tests/evals/run_evals.py --case hardcoded-hex --case tier-leakage
  python3 tests/evals/run_evals.py --plugin installable/design-system-ops.zip
  python3 tests/evals/run_evals.py --model claude-sonnet-5

Outputs are saved to tests/evals/out/ (gitignored): <case>.md is the report the
skill produced, <case>.jsonl the full event stream. A case fails unless the
skill under test was actually loaded through the Skill tool.

Exit: 0 all cases pass, 1 any case fails, 2 setup problem.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CASES = os.path.join(HERE, "cases.json")
OUT = os.path.join(HERE, "out")

# Read-only tools only: a skill run must never change anything, even in a
# throwaway copy. Anything else is denied without prompting (dontAsk).
# "Skill" is what loads a skill: without it, a run either reads SKILL.md by
# hand or answers without the skill at all, and the case tests nothing.
ALLOWED_TOOLS = [
    "Skill", "Read", "Grep", "Glob",
    "Bash(ls:*)", "Bash(cat:*)", "Bash(find:*)", "Bash(grep:*)", "Bash(rg:*)",
    "Bash(wc:*)", "Bash(head:*)", "Bash(git log:*)", "Bash(git ls-files:*)",
]

# How many tool calls a routing case may make before it counts as "no skill".
# Passing routes load their skill within the first three steps.
ROUTE_BUDGET = 6


# A run that never reached the model says nothing about the skill.
AUTH_FAILURES = ("Failed to authenticate", "Invalid API key", "Please run /login", "Not logged in")


def build_bundle(tmp):
    env = dict(os.environ, DSOPS_OUT_DIR=tmp)
    subprocess.run(["bash", os.path.join(REPO, "build.sh")], cwd=REPO, env=env,
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.join(tmp, "design-system-ops.zip")


def plugin_is_complete(plugin, tmp):
    """Run the plugin's own verify-install.sh on the build under test.

    This is the real signal for "the skill ran without its references" —
    far more reliable than reading the model's prose, which can mention
    degraded mode to confirm it or to deny it. A skill that hits a broken
    install stops without its findings, which the finds check catches."""
    root = plugin
    if plugin.endswith(".zip"):
        root = os.path.join(tmp, "plugin")
        shutil.unpack_archive(plugin, root, "zip")
    result = subprocess.run(["bash", os.path.join(root, "verify-install.sh"), root],
                            capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip().splitlines()[-1:] or [""], root


def fresh_fixture(fixture, tmp):
    """Copy the fixture and give it a git history, so git-based checks work."""
    target = os.path.join(tmp, "repo")
    shutil.copytree(os.path.join(REPO, fixture), target)
    git = ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.com"]
    subprocess.run(["git", "init", "-q"], cwd=target, check=True)
    subprocess.run(["git", "add", "-A"], cwd=target, check=True)
    subprocess.run(git + ["commit", "-q", "-m", "Initial commit"], cwd=target, check=True)
    return target


def flatten_into(repo, root, skill):
    """Install one skill the way flattening installers do (npx skills install):
    just its SKILL.md, in its own folder, with no knowledge-notes/ beside it."""
    target = os.path.join(repo, ".claude", "skills", skill)
    os.makedirs(target)
    shutil.copy(os.path.join(root, "skills", skill, "SKILL.md"), target)


def run_case(case, plugin, root, fixture, model, timeout, route_budget=ROUTE_BUDGET):
    with tempfile.TemporaryDirectory(prefix="dsops-eval-") as tmp:
        repo = fresh_fixture(fixture, tmp)
        if case.get("layout") == "flattened":
            flatten_into(repo, root, case["skill"])
            source = []  # the flattened copy is the only install
        else:
            source = ["--plugin-dir", plugin]
        command = [
            "claude", "-p", case["prompt"], *source,
            "--output-format", "stream-json", "--verbose",
            "--permission-mode", "dontAsk",
            "--allowedTools", *ALLOWED_TOOLS,
        ]
        if os.environ.get("ANTHROPIC_API_KEY"):
            # Bare mode ignores any installed copy of the plugin, so only the
            # build under test is loaded. It needs an API key.
            command.append("--bare")
        if model:
            command += ["--model", model]
        return stream(command, repo, timeout, stop_at_skill=case.get("expect") == "route",
                      route_budget=route_budget)


def stream(command, cwd, timeout, stop_at_skill=False, route_budget=ROUTE_BUDGET):
    """Run claude and show progress as it works: S when the skill loads, a dot
    for every other tool call. A case takes minutes; silence looks like a hang."""
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    timer = threading.Timer(timeout, process.kill)
    timer.start()
    lines = []
    other_calls = 0
    try:
        for line in process.stdout:
            lines.append(line)
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get("type") != "assistant":
                continue
            for block in event.get("message", {}).get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    print("S" if block.get("name") == "Skill" else ".", end="", flush=True)
                    if stop_at_skill and block.get("name") == "Skill":
                        # Routing is decided: no need to pay for the full run.
                        process.kill()
                    elif stop_at_skill:
                        other_calls += 1
                        if other_calls >= route_budget:
                            # The routing decision comes early. This many steps
                            # without a skill means Claude chose to go without.
                            process.kill()
        errors = process.stderr.read()
        code = process.wait()
    finally:
        timed_out = not timer.is_alive()
        timer.cancel()
    if timed_out:
        raise subprocess.TimeoutExpired(command, timeout)
    return code, "".join(lines), errors


def parse_stream(stream):
    """Split a stream-json run into (final report text, tool calls made)."""
    report, calls = "", []
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    calls.append((block.get("name", ""), block.get("input", {})))
        elif event.get("type") == "result":
            report = event.get("result") or ""
    return report, calls


def skill_was_loaded(skill, calls):
    """The case only means something if the skill under test actually ran."""
    for name, arguments in calls:
        if name == "Skill" and skill in json.dumps(arguments):
            return True
    return False


# A finding is a line carrying a severity or result label, plus the lines under
# it up to the next finding, heading, table row or bold label. Grading only
# counts what's said inside findings: a planted problem mentioned in passing
# isn't found, and a control mentioned in an exclusions note isn't flagged.
MARKER = re.compile("\U0001F534|\U0001F7E0|\U0001F7E1|\u26AA|\u274C|\u26A0")


def findings(report):
    """Return (header line, full text) for each finding in the report."""
    found, current = [], None
    for line in report.splitlines():
        stripped = line.strip()
        if MARKER.search(line):
            current = [line]
            found.append(current)
            if stripped.startswith("|"):
                current = None  # a table row is a whole finding
        elif stripped.startswith(("#", "|")) or (stripped.startswith("**") and current is not None and len(current) > 1):
            current = None
        elif current is not None:
            current.append(line)
    return [(lines[0], "\n".join(lines)) for lines in found]


# A health assessment looks like dimension statuses. A skill that stopped on a
# broken install must not produce one.
ASSESSMENT = re.compile("(\U0001F7E2|\U0001F7E1|\U0001F7E0|\U0001F534)\\s*\\**\\s*(Strong|Functional|Weak|Absent)")


def skills_loaded(calls):
    """Skill names loaded in order, via the Skill tool or by reading SKILL.md."""
    loaded = []
    for name, arguments in calls:
        if name == "Skill":
            loaded.append(str(arguments.get("skill", "")).split(":")[-1])
        elif name == "Read":
            match = re.search(r"skills/([a-z0-9-]+)/SKILL\.md$", str(arguments.get("file_path", "")))
            if match:
                loaded.append(match.group(1))
    return loaded


SCOPE_BLOCK = re.compile(r"(?m)^\s*(\*\*Scope\*\*|#+\s*Scope\b)")


def flagged_subject(header):
    """The part of a finding header that says what was flagged.

    For a table row that's the leading cells (ID, check, severity, location,
    value), not the explanatory ones at the end: a note saying where a leaked
    value surfaces, or that currentColor is exempt, doesn't flag it."""
    stripped = header.strip()
    if stripped.startswith("|"):
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        return " | ".join(cells[:5])
    return header


def check(case, output, calls):
    lowered = output.lower()
    problems = []
    if case.get("expect") == "route":
        # A plain request that names no skill: the first skill Claude loads
        # must be the right one.
        picked = [str(args.get("skill", "")).split(":")[-1] for name, args in calls if name == "Skill"]
        if not picked:
            problems.append("no skill loaded; Claude did the work without one")
        elif picked[0] != case["skill"]:
            problems.append("routed to %s instead of %s" % (picked[0], case["skill"]))
        return problems
    if case.get("expect") == "chain":
        # A workflow command: every chained skill must actually load, and the
        # result is one report (one Scope block), not a stack of reports.
        loaded = set(skills_loaded(calls))
        for skill in case["chain"]:
            if skill not in loaded:
                problems.append("chained skill never loaded: %s" % skill)
        # A blocking gate must stop the pipeline: later steps must not run.
        for skill in case.get("not_after_gate", []):
            if skill in loaded:
                problems.append("ran %s after the gate should have stopped the pipeline" % skill)
        scopes = len(SCOPE_BLOCK.findall(output))
        if scopes != 1:
            problems.append("expected one combined Scope block, found %d" % scopes)
        for term in case.get("finds", []):
            if term.lower() not in lowered:
                problems.append("missed: %r" % term)
        return problems
    if not skill_was_loaded(case["skill"], calls):
        used = sorted({name for name, _ in calls}) or ["none"]
        problems.append("the %s skill was never loaded (tools used: %s)" % (case["skill"], ", ".join(used)))
    if case.get("expect") == "produces":
        # A generator (a description, a health report): the skill must load
        # and the output must carry each term anywhere, since there are no
        # finding blocks to grade inside.
        for term in case.get("finds", []):
            if term.lower() not in lowered:
                problems.append("missed: %r" % term)
        return problems
    if case.get("expect") == "stop":
        # The broken-install case: the skill must refuse to run without its
        # references and say why, not answer anyway.
        if "incomplete" not in lowered and "reinstall" not in lowered:
            problems.append("didn't say the install is incomplete")
        if ASSESSMENT.search(output):
            problems.append("produced an assessment anyway instead of stopping")
        return problems
    blocks = findings(output)
    anchor = case["finds"][0].lower()
    if not any(anchor in text.lower() for _, text in blocks):
        problems.append("no finding names %r (mentioned in passing doesn't count)" % case["finds"][0])
    for term in case["finds"][1:]:
        if term.lower() not in lowered:
            problems.append("missed: %r" % term)
    # Each control is one or more terms that must not all appear in what a
    # finding flags: ["currentColor"], or ["surface-raised", "darker"].
    for terms in case.get("must_not_flag", []):
        for header, _ in blocks:
            subject = flagged_subject(header).lower()
            if all(term.lower() in subject for term in terms):
                problems.append("flagged a correct thing: %r" % header.strip()[:160])
                break
    return problems


def run_one(case, attempt, label, plugin, root, spec, args):
    """Run one case once. True if it passed, False if not, None on a setup error."""
    print("%-30s %-28s " % (label, case["skill"]), end="", flush=True)
    started = time.time()
    try:
        code, output, errors = run_case(case, plugin, root, spec["fixture"], args.model, args.timeout,
                                        route_budget=args.route_budget)
    except subprocess.TimeoutExpired:
        print(" FAIL\n    timed out after %ds" % args.timeout)
        return False
    if any(marker in (output + errors) for marker in AUTH_FAILURES):
        print(" SETUP\n    claude couldn't authenticate: %s" % (output + errors).strip()[:200])
        print("    Sign in with `claude` interactively (or set ANTHROPIC_API_KEY), then re-run.")
        return None
    stem = case["id"] if attempt is None else "%s.%d" % (case["id"], attempt)
    with open(os.path.join(OUT, stem + ".jsonl"), "w", encoding="utf-8") as handle:
        handle.write(output)
    report, calls = parse_stream(output)
    with open(os.path.join(OUT, stem + ".md"), "w", encoding="utf-8") as handle:
        handle.write(report)
    # A routing case is stopped on purpose once routing is decided.
    stopped_on_purpose = case.get("expect") == "route" and bool(calls)
    problems = (
        check(case, report, calls)
        if code == 0 or stopped_on_purpose
        else ["claude exited %d: %s" % (code, (errors or output).strip()[:300])]
    )
    if case.get("known_gap"):
        # A documented limitation: report it, don't fail the run on it, and
        # say so loudly if it starts passing.
        if problems:
            print(" known gap (%s)" % elapsed(started))
            return True
        print(" ok (%s) — this known gap now passes; remove known_gap from the case" % elapsed(started))
        return True
    if problems:
        print(" FAIL (%s)" % elapsed(started))
        for problem in problems:
            print("    " + problem)
        print("    expected: " + case["why"])
        return False
    print(" ok (%s)" % elapsed(started))
    return True


def elapsed(started):
    seconds = int(time.time() - started)
    return "%dm%02ds" % (seconds // 60, seconds % 60)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--case", action="append", help="run only this case id (repeatable)")
    parser.add_argument("--plugin", help="plugin directory or .zip to test (default: a fresh build)")
    parser.add_argument("--model", help="model to run the skills with")
    parser.add_argument("--timeout", type=int, default=900, help="seconds per case (default 900)")
    parser.add_argument("--route-budget", type=int, default=ROUTE_BUDGET,
                        help="tool calls a routing case may make without a skill before it stops (default %d)" % ROUTE_BUDGET)
    parser.add_argument("--repeat", type=int, default=1,
                        help="run each case this many times and report a pass rate; skill use varies run to run")
    args = parser.parse_args()

    if not shutil.which("claude"):
        print("error: the claude CLI isn't on PATH", file=sys.stderr)
        return 2
    spec = json.load(open(CASES, encoding="utf-8"))
    cases = [c for c in spec["cases"] if not args.case or c["id"] in args.case]
    if not cases:
        print("error: no matching cases", file=sys.stderr)
        return 2
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("note: no ANTHROPIC_API_KEY, so runs aren't in bare mode. If you also have\n"
              "      design-system-ops installed as a plugin, disable it first so only the\n"
              "      build under test is loaded.\n")

    print("Each case is a full skill run and takes a few minutes. S = skill loaded, . = a tool call.\n")
    os.makedirs(OUT, exist_ok=True)
    failed = 0
    with tempfile.TemporaryDirectory(prefix="dsops-eval-build-") as build_tmp:
        plugin = os.path.abspath(args.plugin) if args.plugin else build_bundle(build_tmp)
        complete, summary, root = plugin_is_complete(plugin, build_tmp)
        if not complete:
            print("SETUP\n    the plugin under test is incomplete: %s" % summary[0])
            return 2
        results = {}
        for case in cases:
            for attempt in range(1, args.repeat + 1):
                label = case["id"] if args.repeat == 1 else "%s #%d" % (case["id"], attempt)
                outcome = run_one(case, attempt if args.repeat > 1 else None, label, plugin, root, spec, args)
                if outcome is None:
                    return 2
                results.setdefault(case["id"], []).append(outcome)
    runs = sum(len(r) for r in results.values())
    passed = sum(sum(r) for r in results.values())
    if args.repeat > 1:
        print("\nPass rate per case:")
        for case_id, outcomes in results.items():
            print("  %-28s %d of %d" % (case_id, sum(outcomes), len(outcomes)))
    print("\n%d of %d runs passed. Outputs: %s" % (passed, runs, os.path.relpath(OUT, REPO)))
    failed = runs - passed
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
