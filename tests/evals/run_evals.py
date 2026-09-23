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
    return result.returncode == 0, result.stdout.strip().splitlines()[-1:] or [""]


def fresh_fixture(fixture, tmp):
    """Copy the fixture and give it a git history, so git-based checks work."""
    target = os.path.join(tmp, "repo")
    shutil.copytree(os.path.join(REPO, fixture), target)
    git = ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.com"]
    subprocess.run(["git", "init", "-q"], cwd=target, check=True)
    subprocess.run(["git", "add", "-A"], cwd=target, check=True)
    subprocess.run(git + ["commit", "-q", "-m", "Initial commit"], cwd=target, check=True)
    return target


def run_case(case, plugin, fixture, model, timeout):
    with tempfile.TemporaryDirectory(prefix="dsops-eval-") as tmp:
        repo = fresh_fixture(fixture, tmp)
        command = [
            "claude", "-p", case["prompt"],
            "--plugin-dir", plugin,
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
        return stream(command, repo, timeout)


def stream(command, cwd, timeout):
    """Run claude and show progress as it works: S when the skill loads, a dot
    for every other tool call. A case takes minutes; silence looks like a hang."""
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    timer = threading.Timer(timeout, process.kill)
    timer.start()
    lines = []
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


def check(case, output, calls):
    lowered = output.lower()
    problems = []
    if not skill_was_loaded(case["skill"], calls):
        used = sorted({name for name, _ in calls}) or ["none"]
        problems.append("the %s skill was never loaded (tools used: %s)" % (case["skill"], ", ".join(used)))
    for term in case["finds"]:
        if term.lower() not in lowered:
            problems.append("missed: %r" % term)
    for first, second in case.get("must_not_flag", []):
        for line in output.splitlines():
            if first.lower() in line.lower() and second.lower() in line.lower():
                problems.append("flagged a correct thing: %r" % line.strip()[:160])
                break
    return problems


def elapsed(started):
    seconds = int(time.time() - started)
    return "%dm%02ds" % (seconds // 60, seconds % 60)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--case", action="append", help="run only this case id (repeatable)")
    parser.add_argument("--plugin", help="plugin directory or .zip to test (default: a fresh build)")
    parser.add_argument("--model", help="model to run the skills with")
    parser.add_argument("--timeout", type=int, default=900, help="seconds per case (default 900)")
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
        complete, summary = plugin_is_complete(plugin, build_tmp)
        if not complete:
            print("SETUP\n    the plugin under test is incomplete: %s" % summary[0])
            return 2
        for case in cases:
            print("%-26s %-28s " % (case["id"], case["skill"]), end="", flush=True)
            started = time.time()
            try:
                code, output, errors = run_case(case, plugin, spec["fixture"], args.model, args.timeout)
            except subprocess.TimeoutExpired:
                print(" FAIL\n    timed out after %ds" % args.timeout)
                failed += 1
                continue
            if any(marker in (output + errors) for marker in AUTH_FAILURES):
                print(" SETUP\n    claude couldn't authenticate: %s" % (output + errors).strip()[:200])
                print("    Sign in with `claude` interactively (or set ANTHROPIC_API_KEY), then re-run.")
                return 2
            with open(os.path.join(OUT, case["id"] + ".jsonl"), "w", encoding="utf-8") as handle:
                handle.write(output)
            report, calls = parse_stream(output)
            with open(os.path.join(OUT, case["id"] + ".md"), "w", encoding="utf-8") as handle:
                handle.write(report)
            problems = (
                check(case, report, calls)
                if code == 0
                else ["claude exited %d: %s" % (code, (errors or output).strip()[:300])]
            )
            if problems:
                failed += 1
                print(" FAIL (%s)" % elapsed(started))
                for problem in problems:
                    print("    " + problem)
                print("    expected: " + case["why"])
            else:
                print(" ok (%s)" % elapsed(started))
    print("\n%d of %d cases passed. Outputs: %s" % (len(cases) - failed, len(cases), os.path.relpath(OUT, REPO)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
