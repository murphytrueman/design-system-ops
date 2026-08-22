# Contributing to Design System Ops

Thanks for considering a contribution. This project benefits from the experience of real design systems practitioners, and contributions that improve the skills for everyone are welcome.

## What makes a good contribution

The skills in this pack are built from production experience. Contributions that land well tend to share a few traits: they address a real problem encountered in actual design systems work, they improve the specificity or accuracy of an existing skill, or they fill a gap that practitioners hit regularly.

## How to contribute

**Bug fixes and improvements to existing skills:**
Open a pull request with a clear description of what was wrong and what you changed. If you can include an example of the improved output, that helps reviewers understand the impact.

**New skills:**
Open an issue first describing the skill you'd like to add. Include what problem it solves, who would use it, and a rough outline of the process the skill would follow. This avoids duplicate work and lets us discuss scope before you invest time writing it.

**Documentation improvements:**
Pull requests welcome. If something in the install guide, setup docs, or skill descriptions is unclear or wrong, fix it.

## Skill structure

Each skill is a markdown file (`SKILL.md`) inside its own folder under `skills/`. Skills reference knowledge notes directly from the canonical `knowledge-notes/` directory via their frontmatter `references:` field using relative paths like `../../knowledge-notes/filename.md`. When adding a new skill, include the knowledge note paths in the skill's frontmatter `references:` array. The project structure includes: skills in `skills/skillname/SKILL.md`, commands in `commands/`, knowledge notes in `knowledge-notes/`, and sample outputs in `sample-outputs/`.

## Running the tests

Before opening a pull request, run the suite:

```bash
./tests/run.sh
```

It is stdlib Python — nothing to install — and it runs in well under a second. The tests check the things that break silently for installers: frontmatter Claude Code can't parse, a skill name that no longer matches its directory, a `references:` path pointing at a note that isn't there, a slash command loading a file that doesn't exist, and a bundle in `installable/` that has drifted from the source tree. CI runs the same suite on every pull request.

If you changed anything that ships inside the plugin, rebuild the bundle and commit it:

```bash
./build.sh
```

See [tests/README.md](tests/README.md) for what each test file covers.

## What to avoid

- Generic AI advice. Every finding, recommendation, and output should be specific to the user's actual codebase, not templated.
- Skills that duplicate what an existing skill already does. Check `2-WHATS-INCLUDED.md` for the full inventory.
- Changes to knowledge notes without understanding which skills depend on them. The notes are shared references — changes propagate.

## Code of conduct

Be decent. Assume good intent. Give constructive feedback. This is a project for practitioners helping practitioners.

## Questions?

Open an issue or reach out at [hello@murphytrueman.com](mailto:hello@murphytrueman.com).
