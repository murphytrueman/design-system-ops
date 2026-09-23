"""The output rules in knowledge-notes/output-discipline.md are only as good as
the text that ships alongside them. A skill template that asks for a score, a
sample output that shows one, or a command that promises one teaches the model
the opposite of the rule. These tests pin the rules to every file the model
reads."""

import json
import os
import re
import unittest

import dsops

SAMPLES_DIR = os.path.join(dsops.REPO_ROOT, "sample-outputs")

# output-discipline.md quotes the banned patterns in order to ban them.
EXEMPT = {"knowledge-notes/output-discipline.md"}

# A line that states the rule ("never a numeric score") is not a violation.
# Kept narrow on purpose: everyday words like "without" or "not" appear in
# ordinary sentences and would hide real violations.
NEGATION = re.compile(
    r"(?i)\b(never|don't|do not|avoid|instead of|banned|prohibited|no numeric|not a score|not scored)\b"
)

SCORE_PATTERNS = [
    (re.compile(r"\b\d+(?:\.\d+)?\s?/\s?(?:5|10|35|100)\b(?![/\d])"), "fraction score (X/5, X/10, X/35, X/100)"),
    (re.compile(r"(?i)\bscored\b"), "'scored'"),
    (re.compile(r"(?i)\bscore\s*:"), "'Score:'"),
    (re.compile(r"(?i)\bscores?\s+out\s+of\b"), "'score out of'"),
    (
        re.compile(
            r"(?i)\b(?:health|compliance|consistency|coverage|overall|weighted|friction|"
            r"maturity|readiness|benchmark|dimension|quality)\s+scores?\b"
        ),
        "a named score",
    ),
    (re.compile(r"(?i)\bgrade\s+[A-F][+-]?(?![\w])"), "letter grade"),
    (
        re.compile(r"(?i)\b\d+%\s+(?:toward|towards|of the way|mature|healthy|ready|complete)\b"),
        "percentage used as a rating",
    ),
    # Maturity only: other notes legitimately number things (oversight
    # autonomy levels in human-oversight-framework, for one).
    (
        re.compile(
            r"\bLevel [1-5]\s*\((?:Ad-hoc|Managed|Systematic|Measured|Optimi[sz]ed)"
            r"|\bL[1-5]\s*(?:→|->)\s*L[1-5]\b"
            r"|(?i:maturity)[^.\n]{0,40}\b[Ll]evel [1-5]\b"
        ),
        "numbered maturity level (use the named stages)",
    ),
]

# [ \t]* not \s*: \s would match newlines and pair the wrong fences.
YAML_FENCE = re.compile(r"(?ms)^([ \t]*)```ya?ml[^\n]*\n(.*?)^\1```")
JSON_FENCE = re.compile(r"(?ms)^([ \t]*)```json[^\n]*\n(.*?)^\1```")
BOOLEAN_KEY = re.compile(r"(?m)^\s*(?:-\s+)?(yes|no|y|n|Yes|No|YES|NO)\s*:(?:\s|$)")


def _shipped_texts():
    paths = dsops.skill_files() + dsops.agent_files() + dsops.command_files()
    paths += sorted(
        os.path.join(dsops.KNOWLEDGE_DIR, n)
        for n in os.listdir(dsops.KNOWLEDGE_DIR)
        if n.endswith(".md")
    )
    paths += sorted(
        os.path.join(SAMPLES_DIR, n)
        for n in os.listdir(SAMPLES_DIR)
        if n.endswith((".md", ".html"))
    )
    return [(dsops.rel(p), dsops.read_text(p)) for p in paths]


class TestNoNumericScores(unittest.TestCase):
    def test_files_were_found(self):
        # Guard against a discovery bug making every check below vacuous.
        self.assertGreater(len(_shipped_texts()), 50)

    def test_no_score_wording_ships(self):
        for name, text in _shipped_texts():
            if name in EXEMPT:
                continue
            hits = []
            for lineno, line in enumerate(text.splitlines(), start=1):
                if NEGATION.search(line):
                    continue
                for pattern, label in SCORE_PATTERNS:
                    match = pattern.search(line)
                    if match:
                        hits.append("line %d: %s — %r" % (lineno, label, match.group(0)))
            with self.subTest(file=name):
                self.assertEqual(
                    [],
                    hits,
                    "output-discipline bans numeric scores and numbered levels; "
                    "use the status labels and named maturity stages",
                )

    def test_the_patterns_catch_what_they_ban(self):
        # Each pattern must fire on the thing it exists to catch.
        probes = [
            "Tokens: 4/5",
            "a scored assessment",
            "Consistency Score: 82%",
            "dimension scores out of 35",
            "Overall health score",
            "Grade B+",
            "Level 3 (Systematic)",
            "L1 → L2",
            "about 60% toward being the system we need",
        ]
        for probe in probes:
            with self.subTest(probe=probe):
                self.assertTrue(
                    any(p.search(probe) for p, _ in SCORE_PATTERNS),
                    "no pattern catches %r" % probe,
                )
        probes_maturity = ["current maturity: Level 1/2/3"]
        for probe in probes_maturity:
            with self.subTest(probe=probe):
                self.assertTrue(any(p.search(probe) for p, _ in SCORE_PATTERNS))
        for fine in (
            "78 of 84 components have tests",
            "WCAG 2.2 AA",
            "2026-09-23",
            "24/7 support",
            "Level 1 — full autonomy",  # oversight levels, not maturity
        ):
            with self.subTest(fine=fine):
                self.assertFalse(any(p.search(fine) for p, _ in SCORE_PATTERNS))


class TestJsonExamples(unittest.TestCase):
    """Skills that generate JSON teach its shape by example. An example that
    doesn't parse teaches the model to write files that don't parse."""

    def test_json_examples_parse(self):
        found = 0
        for name, text in _shipped_texts():
            for block in JSON_FENCE.finditer(text):
                found += 1
                line = text[: block.start()].count("\n") + 1
                with self.subTest(file=name, line=line):
                    try:
                        json.loads(block.group(2))
                    except ValueError as error:
                        self.fail("```json example doesn't parse: %s" % error)
        self.assertGreater(found, 0, "no ```json examples found — check JSON_FENCE")


class TestYamlExamples(unittest.TestCase):
    """YAML 1.1 parsers (PyYAML, Ruby's Psych) read bare yes/no keys as
    booleans, so an agent looking up the key "yes" finds nothing."""

    def test_no_bare_boolean_keys(self):
        for name, text in _shipped_texts():
            for block in YAML_FENCE.finditer(text):
                with self.subTest(file=name):
                    self.assertIsNone(
                        BOOLEAN_KEY.search(block.group(2)),
                        "quote yes/no keys in YAML examples (\"yes\":)",
                    )

    def test_the_key_pattern_catches_bare_keys(self):
        self.assertIsNotNone(BOOLEAN_KEY.search("  yes:\n    resolve: Modal"))
        self.assertIsNone(BOOLEAN_KEY.search('  "yes":\n    resolve: Modal'))


if __name__ == "__main__":
    unittest.main()
