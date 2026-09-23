"""What the docs advertise must match what the repo actually contains.

Inventory claims rot silently: a skill gets added, the README table and the
manifest description keep quoting the old numbers, and nothing anywhere
notices. These tests pin the claims to the filesystem."""

import os
import re
import unittest

import dsops

README = os.path.join(dsops.REPO_ROOT, "README.md")

# "40 skills, 4 agents, and 12 knowledge notes"
COUNT_CLAIMS = {
    "skills": r"(\d+)\s+skills\b",
    "agents": r"(\d+)\s+agents\b",
    "knowledge notes": r"(\d+)\s+knowledge notes\b",
}

# Rows of the "What's included" skills table, keyed by category.
SKILL_ROW = re.compile(
    r"^\|\s*\*\*(?:Audit|Govern|Document|Validate|Communicate)\*\*\s*\|\s*(.+?)\s*\|",
    re.M,
)
# Rows of the Agents table: | `/full-diagnostic` | ... |
AGENT_ROW = re.compile(r"^\|\s*`/([a-z0-9-]+)`\s*\|", re.M)


# Present-tense count claims in the guides: (file, pattern, what it counts).
# Only claims about the pack as it is now — dated history entries (e.g. the
# "27 → 37 skills" log in 3-SETUP-AND-CONFIG.md) are records, not claims.
DOC_CLAIMS = [
    ("1-INSTALL.md", r"^\| `skills/` \| (\d+) skills", "skills"),
    ("1-INSTALL.md", r"plus (\d+) agent definitions", "agents"),
    ("1-INSTALL.md", r"^\| `commands/` \| (\d+) command definitions", "commands"),
    ("1-INSTALL.md", r"^\| `knowledge-notes/` \| (\d+) canonical", "knowledge notes"),
    ("2-WHATS-INCLUDED.md", r"What is in the pack:\*\* (\d+) skills", "skills"),
    ("2-WHATS-INCLUDED.md", r"(\d+) agents \(chained", "agents"),
    ("2-WHATS-INCLUDED.md", r"(\d+) knowledge notes \(expert", "knowledge notes"),
    ("2-WHATS-INCLUDED.md", r"there are (\d+) skills\*\*", "skills"),
    ("2-WHATS-INCLUDED.md", r"there are (\d+) agents\*\*", "agents"),
    ("2-WHATS-INCLUDED.md", r"there are (\d+) knowledge notes\*\*", "knowledge notes"),
    ("2-WHATS-INCLUDED.md", r"^## The (\d+) skills", "skills"),
    ("2-WHATS-INCLUDED.md", r"^## The (\d+) agents", "agents"),
    ("2-WHATS-INCLUDED.md", r"^## The (\d+) knowledge notes", "knowledge notes"),
    ("2-WHATS-INCLUDED.md", r"skills/ +← (\d+) skills", "skills"),
    ("3-SETUP-AND-CONFIG.md", r"── skills/ +(\d+) skills", "skills"),
    ("3-SETUP-AND-CONFIG.md", r"── commands/ +(\d+) command definitions", "commands"),
    ("3-SETUP-AND-CONFIG.md", r"── knowledge-notes/ +(\d+) ", "knowledge notes"),
    ("2-WHATS-INCLUDED.md", r"(\d+) sample outputs \(anonymised", "sample outputs"),
    ("2-WHATS-INCLUDED.md", r"directory contains (\d+) sample outputs", "sample outputs"),
    ("3-SETUP-AND-CONFIG.md", r"directory contains (\d+) sample outputs", "sample outputs"),
]

# Guides whose sample-output tables must list every file in sample-outputs/.
SAMPLE_TABLES = ("2-WHATS-INCLUDED.md", "3-SETUP-AND-CONFIG.md")
SAMPLES_DIR = os.path.join(dsops.REPO_ROOT, "sample-outputs")


def _sample_files():
    return sorted(
        n for n in os.listdir(SAMPLES_DIR) if n.endswith((".md", ".html"))
    )


# Per-category skill counts in the guides' section headings, checked against
# the README table: "### Audit (10 skills)" and "### Audit skills (10)".
CATEGORIES = ("Audit", "Govern", "Document", "Validate", "Communicate")
CATEGORY_HEADINGS = {
    "1-INSTALL.md": r"^### %s \((\d+) skills\)",
    "2-WHATS-INCLUDED.md": r"^### %s skills \((\d+)\)",
}
CATEGORY_ROW = r"^\|\s*\*\*%s\*\*\s*\|\s*(.+?)\s*\|"


def _actual():
    return {
        "skills": len(dsops.skill_dirs()),
        "agents": len(dsops.agent_files()),
        "commands": len(dsops.command_files()),
        "sample outputs": len(_sample_files()),
        "knowledge notes": len(
            [n for n in os.listdir(dsops.KNOWLEDGE_DIR) if n.endswith(".md")]
        ),
    }


class TestManifestCounts(unittest.TestCase):
    """The manifest description is marketing copy that ships to every
    installer. If it quotes a number, the number has to be true."""

    def setUp(self):
        self.description = dsops.load_plugin_manifest()["description"]
        self.actual = _actual()

    def test_advertised_counts_are_accurate(self):
        found_any = False
        for label, pattern in COUNT_CLAIMS.items():
            match = re.search(pattern, self.description)
            if not match:
                # Not every phrasing has to quote every count.
                continue
            found_any = True
            with self.subTest(claim=label):
                self.assertEqual(
                    self.actual[label],
                    int(match.group(1)),
                    "plugin.json advertises %s %s but the repo has %d"
                    % (match.group(1), label, self.actual[label]),
                )
        self.assertTrue(
            found_any,
            "no inventory counts found in the manifest description — if the "
            "wording changed deliberately, update COUNT_CLAIMS here too",
        )


class TestReadmeInventory(unittest.TestCase):
    """The README tables are the first thing a prospective user reads. A skill
    missing from them is effectively undiscoverable."""

    def setUp(self):
        self.readme = dsops.read_text(README)
        self.skill_dirs = {os.path.basename(d) for d in dsops.skill_dirs()}

    def _listed_skills(self):
        listed = set()
        for row in SKILL_ROW.findall(self.readme):
            listed |= {name.strip() for name in row.split(",") if name.strip()}
        return listed

    def test_readme_table_was_parsed(self):
        # Guard against the table being reformatted into something the regex
        # silently matches zero rows of, which would make the tests below vacuous.
        self.assertGreater(len(self._listed_skills()), 0, "no skill table rows parsed")

    def test_every_listed_skill_exists(self):
        phantom = sorted(self._listed_skills() - self.skill_dirs)
        self.assertEqual(
            [], phantom, "README lists skills with no directory under skills/"
        )

    def test_every_skill_is_listed(self):
        missing = sorted(self.skill_dirs - self._listed_skills())
        self.assertEqual(
            [], missing, "skills missing from the README 'What's included' table"
        )

    def test_every_listed_agent_has_a_command(self):
        commands = {
            os.path.splitext(os.path.basename(p))[0] for p in dsops.command_files()
        }
        listed = set(AGENT_ROW.findall(self.readme))
        self.assertTrue(listed, "no agent rows parsed from the README")
        missing = sorted(listed - commands)
        self.assertEqual(
            [], missing, "README advertises agents with no command file"
        )


class TestGuideCounts(unittest.TestCase):
    """Facts are pinned, voice is free: the guides stay hand-written, but any
    number they quote about the pack has to match the files on disk."""

    def setUp(self):
        self.actual = _actual()

    def _doc(self, name):
        return dsops.read_text(os.path.join(dsops.REPO_ROOT, name))

    def test_guide_counts_are_accurate(self):
        for name, pattern, label in DOC_CLAIMS:
            with self.subTest(doc=name, claim=pattern):
                match = re.search(pattern, self._doc(name), re.M)
                self.assertIsNotNone(
                    match,
                    "claim not found — if the wording changed deliberately, "
                    "update DOC_CLAIMS in test_inventory.py",
                )
                self.assertEqual(
                    self.actual[label],
                    int(match.group(1)),
                    "%s says %s %s but the repo has %d"
                    % (name, match.group(1), label, self.actual[label]),
                )

    def test_category_counts_match_the_readme(self):
        readme = dsops.read_text(README)
        for category in CATEGORIES:
            row = re.search(CATEGORY_ROW % category, readme, re.M)
            self.assertIsNotNone(row, "no README row for %s" % category)
            expected = len([s for s in row.group(1).split(",") if s.strip()])
            for name, pattern in CATEGORY_HEADINGS.items():
                with self.subTest(doc=name, category=category):
                    match = re.search(pattern % category, self._doc(name), re.M)
                    self.assertIsNotNone(match, "no %s heading found" % category)
                    self.assertEqual(expected, int(match.group(1)))


class TestSampleTables(unittest.TestCase):
    """A sample missing from the guides' tables is a calibration example
    nobody is told about."""

    def test_every_sample_is_listed(self):
        self.assertTrue(_sample_files(), "no sample outputs found")
        for name in SAMPLE_TABLES:
            text = dsops.read_text(os.path.join(dsops.REPO_ROOT, name))
            for sample in _sample_files():
                with self.subTest(doc=name, sample=sample):
                    self.assertRegex(
                        text,
                        r"(?m)^\|\s*`%s`\s*\|" % re.escape(sample),
                        "sample output missing from this guide's table",
                    )


if __name__ == "__main__":
    unittest.main()
