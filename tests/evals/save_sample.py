#!/usr/bin/env python3
"""Turn an eval run's output into a shipped sample.

    python3 tests/evals/save_sample.py <case-id> [--commit SHA]

Reads tests/evals/out/<case>.md (written by run_evals.py), trims the parts
that aren't the report, and writes sample-outputs/fixture-<skill>.md with
the standard header. The report body is verbatim; only these are removed:

- anything before the first H1 (the "I have everything I need" lead-in)
- anything after the closing note blockquote (harness notes about
  connectors, offers to run other skills), when a closing note exists

The header says exactly that, so "Edited: no" stays honest.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, "out")
SAMPLES = os.path.join(REPO, "sample-outputs")
CASES = os.path.join(HERE, "cases.json")

CLOSING_NOTE = re.compile(r"^> \*\*A note on context", re.M)


def trim(text):
    """Keep the report: from the first H1 to the end of the closing note."""
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if line.startswith("# ")), 0)
    body = "\n".join(lines[start:])
    match = None
    for match in CLOSING_NOTE.finditer(body):
        pass
    if match:
        # The note is one paragraph: end at the first blank line after it.
        end = body.find("\n\n", match.start())
        body = body if end == -1 else body[:end]
    return body.strip() + "\n"


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("case")
    parser.add_argument("--commit", help="fixture commit to cite (default: git rev-parse --short HEAD)")
    args = parser.parse_args(argv)

    cases = {c["id"]: c for c in json.load(open(CASES, encoding="utf-8"))["cases"]}
    if args.case not in cases:
        print("unknown case %r" % args.case, file=sys.stderr)
        return 2
    skill = cases[args.case]["skill"]
    source = os.path.join(OUT, args.case + ".md")
    if not os.path.isfile(source):
        print("no output for %s; run: python3 tests/evals/run_evals.py --case %s" % (args.case, args.case),
              file=sys.stderr)
        return 2
    commit = args.commit or subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], cwd=REPO, text=True).strip()
    body = trim(open(source, encoding="utf-8").read())
    header = (
        "# Sample output: %s (fixture run)\n\n"
        "**Skill:** `skills/%s`\n"
        "**Run against:** `tests/fixtures/sample-ds`, a small design system with known problems planted in it, as of commit `%s`\n"
        "**Eval case:** `%s` in `tests/evals/cases.json`\n"
        "**Date:** %s\n"
        "**Edited:** no. The report below is verbatim from a headless run with read-only tools; "
        "`tests/evals/save_sample.py` removed only the chat lead-in before the report's title and any "
        "harness notes after the closing note. Rerun it with `python3 tests/evals/run_evals.py --case %s`; "
        "runs vary, so expect the same findings in different words.\n\n---\n\n"
    ) % (skill, skill, commit, args.case, datetime.date.today().isoformat(), args.case)
    target = os.path.join(SAMPLES, "fixture-%s.md" % skill)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(header + body)
    print("wrote %s" % os.path.relpath(target, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
