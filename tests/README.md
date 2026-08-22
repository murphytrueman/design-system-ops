# Tests

This repo ships markdown, not an application — so the tests check the things
that actually break for an installer: frontmatter Claude Code can't parse, a
skill name that no longer matches its directory, a `references:` path that
points at nothing, a slash command that loads a file which isn't there, and a
bundle in `installable/` that has drifted from the source tree.

Stdlib Python only. Nothing to install.

## Run them

```bash
python3 -m unittest discover -s tests -t tests
```

Or with the runner, which is what CI uses:

```bash
./tests/run.sh
```

Single file, verbose:

```bash
python3 -m unittest discover -s tests -t tests -v -p test_skills.py
```

## What each file covers

| File | Covers |
|------|--------|
| `test_skills.py` | Skill frontmatter, kebab-case names, name/directory agreement, uniqueness, `references:` resolution, orphaned knowledge notes, non-stub bodies |
| `test_commands.py` | Slash-command frontmatter, `allowed-tools`, and that every `${CLAUDE_PLUGIN_ROOT}` path resolves |
| `test_plugin_manifest.py` | `.claude-plugin/plugin.json` shape, semver, and agreement with the top CHANGELOG entry |
| `test_docs_links.py` | Relative links and images in the shipped docs, plus the README headings registries look for |
| `test_build.py` | `build.sh` output: identical `.zip`/`.plugin`, every skill and command present, no tooling or scratch files leaking in, and that `installable/` is not stale |

`dsops.py` is the shared helper — a small frontmatter parser and the file
discovery used by the rest.

## When a test fails

Most failures name the file and the exact problem. Two worth calling out:

- **"committed bundle is stale"** — run `./build.sh` and commit the result in
  `installable/`.
- **"knowledge notes no skill references"** — either wire the note into a
  skill's `references:` list or delete it. An unreferenced note ships in the
  bundle and is never read.
