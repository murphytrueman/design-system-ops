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
| `test_skills.py` | Skill frontmatter, kebab-case names, descriptions of 300 characters or fewer, name/directory agreement, uniqueness, `references:` resolution, orphaned knowledge notes, non-stub bodies, and the install self-check block (verbatim, first H2, only where there are references) |
| `test_output_rules.py` | The output-discipline rules hold in everything the model reads — skills, agents, commands, knowledge notes and sample outputs: no numeric scores, percentage ratings or numbered maturity levels; every ```json example parses; no bare `yes`/`no` keys in YAML examples |
| `test_consistency.py` | Every `.ds-ops-config.yml` key a skill reads is documented in `ds-ops-config.example.yml` — including whole sections a skill declares in its Configuration block — and every shell command a skill tells the model to run is pre-approved by the slash command that loads it (`gh api` is left to prompt on purpose, since it can write) |
| `test_fixture.py` | The fixture design system in `fixtures/sample-ds/` still contains every planted problem and every correct-and-must-not-be-flagged control the eval cases expect, and gives the skill no hints |
| `test_verify_install.py` | `verify-install.sh` exit codes and output against a clean checkout, a flattened install missing `knowledge-notes/`, a lone `SKILL.md`, an unreadable skill file, an empty `skills/`, and a non-install directory |
| `test_commands.py` | Slash-command frontmatter, `allowed-tools`, and that every `${CLAUDE_PLUGIN_ROOT}` path resolves |
| `test_plugin_manifest.py` | `.claude-plugin/plugin.json` shape, semver, and agreement with the top CHANGELOG entry |
| `test_docs_links.py` | Relative links and images in the shipped docs, plus the README headings registries look for |
| `test_inventory.py` | The counts advertised in `plugin.json`, the skills and agents listed in the README tables, and every present-tense count in the install, contents, and setup guides match what is actually on disk |
| `test_build.py` | `build.sh` output: identical `.zip`/`.plugin`, every skill and command present, no tooling or scratch files leaking in, that `installable/` is not stale, and the as-shipped check: the unpacked bundle passes its own `verify-install.sh` |

`dsops.py` is the shared helper — a small frontmatter parser and the file
discovery used by the rest. `sync_selfcheck.py` is not a test: it's the
one-command fix for the self-check block, and the tests check it too.

## Evals: what the skills actually do

The tests above check what the skills *say*. `tests/evals/run_evals.py` checks what they *do*: it runs skills headlessly with the `claude` CLI against a fresh copy of `fixtures/sample-ds/` — a small design system with problems planted in it — and checks each output names the planted problem without flagging the things that are correct. A case also fails unless the skill under test was actually loaded through the Skill tool, and the runner checks the plugin under test with `verify-install.sh` before any case runs. Cases live in `evals/cases.json`, outside the fixture, so a skill run can't read the answers.

```bash
python3 tests/evals/run_evals.py                      # every case, against a fresh build
python3 tests/evals/run_evals.py --case tier-leakage  # one case
```

There are four kinds of case:

- **Finds** (default): the skill must name the planted problem inside a finding, without flagging the correct controls.
- **Stop** (`flattened-install`): a skill installed on its own with no `knowledge-notes/`, the way flattening installers leave it. It must stop and say the install is incomplete.
- **Route** (`route-*`): a plain request that doesn't name a skill. The first skill Claude loads must be the right one, not a neighbour. The run stops as soon as a skill loads, so these take seconds.
- **Chain** (`release-chain`): a workflow command. Every chained skill must load, and the result must be one combined report with a single Scope block.

It calls Claude, so it costs real usage and isn't part of `./tests/run.sh` or CI. Run it before a release. Outputs land in `tests/evals/out/` (gitignored). A run that can't sign in stops with exit 2 rather than blaming the skill. Without `ANTHROPIC_API_KEY`, disable any installed copy of the plugin first so only the build under test loads.

## When a test fails

Most failures name the file and the exact problem. Two worth calling out:

- **"committed bundle is stale"** — run `./build.sh` and commit the result in
  `installable/`.
- **"knowledge notes no skill references"** — either wire the note into a
  skill's `references:` list or delete it. An unreferenced note ships in the
  bundle and is never read.
- **"self-check block missing, duplicated, or edited"** — the block's text
  lives in `dsops.REFERENCE_CHECK_BLOCK`. To change the wording, edit it there,
  then run `python3 tests/sync_selfcheck.py` to bring every skill in line
  (`--check` lists what's out of line without writing). Never hand-edit one
  copy.
- **"claim not found"** in `test_inventory.py` — a count in one of the guides
  was reworded, so the test can no longer find it. Update the pattern in
  `DOC_CLAIMS` rather than deleting it.

## Every check has to be able to fail

A check that can't fail looks exactly like one that passes. So each check here
comes with a known-bad case it must catch, and where it matters a known-good
case it must pass without complaint: the doctor script is run against a
flattened install, an unreadable skill file, and an empty `skills/`. The
self-check test is fed a deliberately edited block. The count tests fail if a
claim's wording disappears rather than silently skipping it.
