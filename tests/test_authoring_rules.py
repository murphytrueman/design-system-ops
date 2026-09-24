"""The authoring rules every skill follows.

These were applied by hand in the 2.0 review; the tests keep the next
contribution from drifting back. Each check is probed with a known-bad
input so it can't pass vacuously.
"""

import re
import unittest

import dsops

SEVERITIES = ("🔴 Critical", "🟠 High", "🟡 Medium", "⚪ Low")
EVIDENCE = re.compile(r"evidence|location|file and line|file:line", re.I)
# A findings template: a "- Finding ID (e.g. …)" list or a table whose
# header carries an ID and a Severity column. Visualisers and generators
# don't have one (visual-report mentions "Finding IDs" only as parsed input).
FINDINGS_TABLE = re.compile(r"- Finding ID \(|\| ID \|[^\n]*Severity")
# The DTCG resolver module has sets, modifiers and contexts. "Mode" belongs
# to Figma; these phrasings were the wrong model and must not come back.
# "Figma modes" near "resolver" is fine: that's the mapping sentence.
RESOLVER_MODES = re.compile(
    r"resolver mode|mode-specific value|missing mode value|declared mode|"
    r"resolver(?:(?!Figma)[^.\n]){0,60}\bmodes\b",
    re.I,
)


def _skills():
    for path in dsops.skill_files():
        data, body = dsops.load_document(path)
        yield path, data, body


class TestAllowedTools(unittest.TestCase):
    def test_every_skill_declares_the_tools_it_may_use(self):
        for path, data, _ in _skills():
            with self.subTest(skill=dsops.rel(path)):
                self.assertTrue(
                    data.get("allowed-tools", "").strip(),
                    "no allowed-tools: the skill can't run its own commands headlessly",
                )


class TestOutputDiscipline(unittest.TestCase):
    def test_every_skill_loads_output_discipline(self):
        for path, data, _ in _skills():
            with self.subTest(skill=dsops.rel(path)):
                refs = data.get("references", [])
                self.assertTrue(
                    any(r.endswith("output-discipline.md") for r in refs),
                    "every skill makes claims about the user's system; load the note",
                )


class TestSeverityRubric(unittest.TestCase):
    def _missing(self, body):
        if "🔴 Critical" not in body:
            return []
        return [s for s in SEVERITIES if s not in body]

    def test_skills_that_rate_severity_define_all_four_levels(self):
        for path, _, body in _skills():
            with self.subTest(skill=dsops.rel(path)):
                self.assertEqual([], self._missing(body), "severity used without all four levels")

    def test_probe_catches_a_missing_level(self):
        self.assertEqual(["⚪ Low"], self._missing("🔴 Critical 🟠 High 🟡 Medium"))


class TestEvidenceColumn(unittest.TestCase):
    def _lacks_evidence(self, body):
        return bool(FINDINGS_TABLE.search(body)) and not EVIDENCE.search(body)

    def test_findings_templates_require_evidence(self):
        for path, _, body in _skills():
            with self.subTest(skill=dsops.rel(path)):
                self.assertFalse(
                    self._lacks_evidence(body),
                    "a findings template with no evidence column lets a finding ship without a file and line",
                )

    def test_probe_catches_a_table_without_evidence(self):
        self.assertTrue(self._lacks_evidence("| ID | Severity | Description |"))
        self.assertFalse(self._lacks_evidence("| ID | Severity | Evidence | Description |"))


class TestResolverVocabulary(unittest.TestCase):
    def test_no_skill_or_note_uses_the_wrong_resolver_model(self):
        paths = dsops.skill_files() + [
            p for p in __import__("glob").glob(dsops.KNOWLEDGE_DIR + "/*.md")
        ]
        for path in paths:
            with self.subTest(file=dsops.rel(path)):
                _, body = dsops.load_document(path)
                self.assertIsNone(
                    RESOLVER_MODES.search(body),
                    "DTCG resolvers have sets, modifiers and contexts, not modes",
                )

    def test_probe_catches_the_old_wording(self):
        self.assertIsNotNone(RESOLVER_MODES.search("validate every declared mode in the resolver"))
        self.assertIsNotNone(RESOLVER_MODES.search("a token missing a mode-specific value"))
        self.assertIsNone(RESOLVER_MODES.search("in a DTCG resolver each Figma mode becomes a context"))


if __name__ == "__main__":
    unittest.main()
