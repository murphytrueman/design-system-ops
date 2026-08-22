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


def _actual():
    return {
        "skills": len(dsops.skill_dirs()),
        "agents": len(dsops.agent_files()),
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


if __name__ == "__main__":
    unittest.main()
