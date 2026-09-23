"""The fixture in tests/fixtures/sample-ds is a small design system with known
problems planted in it, plus things that are correct and must not be flagged.
tests/evals/run_evals.py runs skills against it and checks what they find.

These tests don't run any skills. They make sure the fixture still contains
exactly what the eval cases expect, so an eval failure means the skill missed
something, never that the fixture quietly changed."""

import json
import os
import re
import unittest

import dsops

FIXTURE = os.path.join(dsops.REPO_ROOT, "tests", "fixtures", "sample-ds")
CASES = os.path.join(dsops.REPO_ROOT, "tests", "evals", "cases.json")


def fixture(*parts):
    return dsops.read_text(os.path.join(FIXTURE, *parts))


def tokens(name):
    return json.loads(fixture("tokens", name + ".tokens.json"))


def css_block(css, selector):
    match = re.search(re.escape(selector) + r"\s*\{(.*?)\}", css, re.S)
    return match.group(1) if match else ""


def luminance(hex_colour):
    channels = [int(hex_colour[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


class TestPlantedProblems(unittest.TestCase):
    def test_card_border_skips_the_semantic_tier(self):
        self.assertEqual("{color.gray.200}", tokens("component")["card"]["border"]["$value"])
        self.assertIn("200", tokens("primitives")["color"]["gray"])
        self.assertIn("default", tokens("semantic")["color"]["border"])

    def test_card_title_uses_an_off_palette_hex(self):
        self.assertIn("#1a73e8", fixture("src", "components", "Card", "Card.module.css"))
        self.assertNotIn("1a73e8", json.dumps(tokens("primitives")).lower())

    def test_tooltip_is_exported_but_undocumented(self):
        self.assertIn("Tooltip", fixture("src", "index.ts"))
        tooltip_dir = os.path.join(FIXTURE, "src", "components", "Tooltip")
        self.assertFalse([n for n in os.listdir(tooltip_dir) if ".stories." in n])
        for documented in ("Button", "Card"):
            with self.subTest(component=documented):
                self.assertTrue(
                    os.path.isfile(os.path.join(FIXTURE, "src", "components", documented, documented + ".stories.tsx"))
                )

    def test_tooltip_is_not_linked_or_hidden(self):
        source = fixture("src", "components", "Tooltip", "Tooltip.tsx")
        self.assertIn('role="tooltip"', source)
        self.assertNotIn("aria-describedby", source)
        self.assertNotIn("hidden", fixture("src", "components", "Tooltip", "Tooltip.module.css"))

    def test_card_border_has_no_dark_override(self):
        css = fixture("src", "styles", "tokens.css")
        self.assertRegex(css_block(css, ":root"), r"--card-border:\s*#")
        self.assertNotIn("--card-border", css_block(css, '[data-theme="dark"]'))


class TestControls(unittest.TestCase):
    """Correct things a skill must not flag."""

    def test_dark_raised_surface_is_lighter_than_the_base(self):
        dark = css_block(fixture("src", "styles", "tokens.css"), '[data-theme="dark"]')
        base = re.search(r"--color-surface-base:\s*(#[0-9a-fA-F]{6})", dark).group(1)
        raised = re.search(r"--color-surface-raised:\s*(#[0-9a-fA-F]{6})", dark).group(1)
        self.assertGreater(luminance(raised), luminance(base))

    def test_dark_theme_inherits_spacing(self):
        dark = css_block(fixture("src", "styles", "tokens.css"), '[data-theme="dark"]')
        self.assertNotIn("--space-", dark)

    def test_button_uses_only_exempt_keywords(self):
        css = fixture("src", "components", "Button", "Button.module.css")
        self.assertIn("transparent", css)
        self.assertIn("currentColor", css)
        self.assertNotRegex(css, r"#[0-9a-fA-F]{3,8}\b")


class TestFixtureHygiene(unittest.TestCase):
    def test_fixture_gives_no_hints(self):
        # A skill run reads the whole fixture; it must not be told the answers.
        for root, _, files in os.walk(FIXTURE):
            for name in files:
                text = dsops.read_text(os.path.join(root, name)).lower()
                for word in ("planted", "deliberately", "as it should", "as they should", "eval"):
                    with self.subTest(file=name, word=word):
                        self.assertNotIn(word, text)

    def test_token_files_parse(self):
        for name in ("primitives", "semantic", "component"):
            with self.subTest(tokens=name):
                tokens(name)

    def test_cases_name_real_skills(self):
        cases = json.loads(dsops.read_text(CASES))["cases"]
        self.assertGreaterEqual(len(cases), 4)
        skills = {os.path.basename(d) for d in dsops.skill_dirs()}
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertIn(case["skill"], skills)
                self.assertIn(case["skill"], case["prompt"])
                self.assertTrue(case["finds"])


if __name__ == "__main__":
    unittest.main()
