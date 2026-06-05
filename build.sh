#!/usr/bin/env bash
#
# Protect the FastAPI app in ./src into a drop-in mirror at ./protected.
# Run it with:  python protected/run.py    (or pipenv run serve)
#
# Use the SAME Python you deploy with — obfy's marshal/bytecode format is
# interpreter-version specific.
set -euo pipefail

PYTHON="${PYTHON:-python3}"

rm -rf protected

# --level 3 stops BELOW cross-module public-name renaming on purpose: Pydantic
#   field names and the FastAPI route/response contract are PUBLIC names that
#   must survive (they map to JSON keys and the OpenAPI schema). Level 3 still
#   strips docstrings, mangles string literals, injects dead code, and renames
#   function-local variables — it just leaves public symbols intact.
# Launch via run.py (imports the `app` OBJECT) rather than `uvicorn main:app`
#   (an import STRING), so nothing depends on the textual name `app`.
obfy build --src ./src --out ./protected --python "$PYTHON" --level 3

echo
echo "Done. Serve it with:  python protected/run.py"
