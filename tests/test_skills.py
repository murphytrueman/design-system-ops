"""Every skill must be loadable by Claude Code: valid frontmatter, a name that
matches its directory, a description good enough to route on, and reference
paths that actually resolve."""

import os
import re
import unittest

import dsops

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Claude Code routes on the description alone, so it has to carry the trigger
# phrasing. Short ones are almost always a stub someone forgot to finish.
MIN_DESCRIPTION = 40


class TestSkillDirectories(unittest.TestCase):
    def test_every_skill_dir_has_a_skill_md(self):
        missing = [
            dsops.rel(d)
            for d in dsops.skill_dirs()
            if not os.path.isfile(os.path.join(d, "SKILL.md"))
        ]
        self.assertEqual([], missing, "skill directories without a SKILL.md")

    def test_repo_has_skills(self):
        self.assertGreater(len(dsops.skill_files()), 0, "no skills found")


class TestSkillFrontmatter(unittest.TestCase):
    def test_frontmatter_parses(self):
        for path in dsops.skill_files() + dsops.agent_files():
            with self.subTest(skill=dsops.rel(path)):
                dsops.load_document(path)

    def test_name_and_description_present(self):
        for path in dsops.skill_files() + dsops.agent_files():
            with self.subTest(skill=dsops.rel(path)):
                data, _ = dsops.load_document(path)
                self.assertIn("name", data)
                self.assertIn("description", data)
                self.assertTrue(str(data["name"]).strip(), "empty name")
                self.assertGreaterEqual(
                    len(str(data["description"]).strip()),
                    MIN_DESCRIPTION,
                    "description too short to route on",
                )

    def test_name_is_kebab_case(self):
        for path in dsops.skill_files() + dsops.agent_files():
            with self.subTest(skill=dsops.rel(path)):
                name = dsops.load_document(path)[0]["name"]
                self.assertRegex(name, NAME_PATTERN, "name must be kebab-case")

    def test_name_matches_directory(self):
        for path in dsops.skill_files():
            with self.subTest(skill=dsops.rel(path)):
                expected = os.path.basename(os.path.dirname(path))
                self.assertEqual(expected, dsops.load_document(path)[0]["name"])

    def test_names_are_unique(self):
        seen = {}
        for path in dsops.skill_files() + dsops.agent_files():
            name = dsops.load_document(path)[0]["name"]
            self.assertNotIn(
                name,
                seen,
                "duplicate skill name %r in %s and %s"
                % (name, seen.get(name), dsops.rel(path)),
            )
            seen[name] = dsops.rel(path)

    def test_description_is_single_line(self):
        # A newline inside the description silently truncates it at load time.
        for path in dsops.skill_files() + dsops.agent_files():
            with self.subTest(skill=dsops.rel(path)):
                description = dsops.load_document(path)[0]["description"]
                self.assertNotIn("\n", description)


class TestSkillReferences(unittest.TestCase):
    def test_references_resolve(self):
        for path in dsops.skill_files():
            data, _ = dsops.load_document(path)
            for reference in data.get("references", []):
                with self.subTest(skill=dsops.rel(path), reference=reference):
                    target = os.path.normpath(
                        os.path.join(os.path.dirname(path), reference)
                    )
                    self.assertTrue(
                        os.path.isfile(target),
                        "broken reference -> %s" % reference,
                    )

    def test_references_stay_inside_the_repo(self):
        # References ship inside the plugin bundle; one pointing outside the
        # repo would resolve on this machine and break for every installer.
        for path in dsops.skill_files():
            data, _ = dsops.load_document(path)
            for reference in data.get("references", []):
                with self.subTest(skill=dsops.rel(path), reference=reference):
                    target = os.path.normpath(
                        os.path.join(os.path.dirname(path), reference)
                    )
                    self.assertTrue(
                        target.startswith(dsops.REPO_ROOT + os.sep),
                        "reference escapes the repo -> %s" % reference,
                    )

    def test_every_knowledge_note_is_referenced(self):
        referenced = set()
        for path in dsops.skill_files():
            data, _ = dsops.load_document(path)
            for reference in data.get("references", []):
                referenced.add(
                    os.path.basename(os.path.normpath(reference))
                )
        orphans = sorted(
            note
            for note in os.listdir(dsops.KNOWLEDGE_DIR)
            if note.endswith(".md") and note not in referenced
        )
        self.assertEqual([], orphans, "knowledge notes no skill references")


class TestSkillBody(unittest.TestCase):
    def test_body_is_not_empty(self):
        for path in dsops.skill_files() + dsops.agent_files():
            with self.subTest(skill=dsops.rel(path)):
                _, body = dsops.load_document(path)
                self.assertGreater(len(body.strip()), 200, "skill body is a stub")

    def test_body_has_a_heading(self):
        for path in dsops.skill_files() + dsops.agent_files():
            with self.subTest(skill=dsops.rel(path)):
                _, body = dsops.load_document(path)
                self.assertRegex(body, r"(?m)^#{1,3} \S", "no markdown heading")


if __name__ == "__main__":
    unittest.main()
