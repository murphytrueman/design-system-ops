"""The plugin manifest is what Cowork and Claude Code read on install. A typo
here breaks the install for everyone, and nothing else in the repo catches it."""

import json
import re
import unittest

import dsops

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
REQUIRED = ("name", "version", "description", "author", "license")


class TestPluginManifest(unittest.TestCase):
    def setUp(self):
        self.manifest = dsops.load_plugin_manifest()

    def test_is_valid_json(self):
        json.loads(dsops.read_text(dsops.PLUGIN_JSON))

    def test_required_fields_present(self):
        for field in REQUIRED:
            with self.subTest(field=field):
                self.assertIn(field, self.manifest)
                self.assertTrue(self.manifest[field], "empty %s" % field)

    def test_version_is_semver(self):
        self.assertRegex(self.manifest["version"], SEMVER)

    def test_name_matches_repo_directory_convention(self):
        self.assertRegex(self.manifest["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_keywords_are_a_non_empty_list_of_strings(self):
        keywords = self.manifest.get("keywords", [])
        self.assertIsInstance(keywords, list)
        self.assertTrue(keywords)
        for keyword in keywords:
            self.assertIsInstance(keyword, str)

    def test_version_matches_latest_changelog_entry(self):
        changelog = dsops.read_text(dsops.os.path.join(dsops.REPO_ROOT, "CHANGELOG.md"))
        versions = re.findall(r"(?m)^##+\s*\[?v?(\d+\.\d+\.\d+)\]?", changelog)
        self.assertTrue(versions, "no versioned heading found in CHANGELOG.md")
        self.assertEqual(
            versions[0],
            self.manifest["version"],
            "plugin.json version and the top CHANGELOG entry disagree",
        )


if __name__ == "__main__":
    unittest.main()
