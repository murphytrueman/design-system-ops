#!/usr/bin/env bash
#
# Run the full test suite. Stdlib Python only — nothing to install.
#
# Usage:  ./tests/run.sh            (all tests)
#         ./tests/run.sh -v         (verbose)
#
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

exec python3 -m unittest discover -s tests -t tests "$@"
