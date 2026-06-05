# obfy + FastAPI template

A minimal FastAPI service wired to ship with its source **obfuscated and
AES-256-GCM encrypted** by [obfy](https://github.com/obfy/obfy). `obfy build`
turns `./src` into a drop-in protected mirror (`./protected`) that you serve
exactly like the original.

```
src/run.py + main.py + app/  ──► obfy build ──► protected/  ──► python protected/run.py
        (your code)                             (encrypted)      (or uvicorn)
```

## Layout

| Path | What it is |
|------|------------|
| `src/run.py` | Production entry point — imports the `app` object and runs uvicorn. |
| `src/main.py` | FastAPI app + routes. |
| `src/app/services.py` | The **protected business logic**. |
| `src/app/schemas.py` | Pydantic response models (public API contract). |
| `build.sh` | Runs `obfy build` with FastAPI-safe flags. |
| `Pipfile` | Deps (`fastapi`, `uvicorn`, plus `obfy` as a build tool). |
| `protected/` | Generated protected mirror (git-ignored). |

## Prerequisites

- **CPython 3.10–3.13.** Build with the **same Python version** you deploy with —
  obfy's marshalled bytecode is interpreter-version specific.
- macOS, Linux, or Windows.

## Setup

This template uses [pipenv](https://pipenv.pypa.io/) (the `Pipfile` pins
`python_version = "3.12"`):

```bash
pip install --user pipenv          # if you don't have it
pipenv install
```

Prefer plain venv + pip? `python3 -m venv .venv && source .venv/bin/activate &&
pip install fastapi "uvicorn[standard]" obfy`.

## Develop (unprotected)

Iterate on the real source with hot reload:

```bash
pipenv run dev                     # == uvicorn main:app --reload --app-dir src
# -> http://127.0.0.1:8000/quote?units=10
# -> http://127.0.0.1:8000/docs
```

## Build the protected tree

```bash
pipenv run build                   # == bash build.sh
```

Then run the **protected** mirror — same app, different directory:

```bash
pipenv run serve                   # == python protected/run.py
```

`./protected` is a 1:1 mirror of `./src`: each `.py` becomes a tiny
self-activating stub, the real code lives encrypted under `protected/__obfy__/`,
and obfy's native loader is bundled in. Decryption happens in memory at import
time; plaintext source never lands on disk.

## Why the build flags matter (FastAPI specifics)

Two things are **public contracts** that obfuscation must not rename:

- **Pydantic field names** (`schemas.py`) map directly to JSON keys and the
  OpenAPI schema. **`--level 3`** stops below cross-module public-name renaming,
  so field and route names survive. Levels 4–5 would rename them and break the
  API. (Level 3 still strips docstrings, mangles string literals, injects dead
  code, and renames function-local variables.)
- **The `app` object name.** `run.py` launches uvicorn with the app *object*
  (`uvicorn.run(app)`), not the `"main:app"` import *string*. Strings are never
  renamed, but they also aren't protected — passing the object keeps you free to
  raise the level later without a dangling string reference.

Have a pure-logic module with no external contract (no Pydantic fields, no names
referenced by string)? Split it into its own package and protect *that* at a
higher level separately.

## Deploying

Serve `./protected` with whatever you already use. Because the app is launched by
object, point your process manager at `run.py`:

```bash
python protected/run.py            # honors HOST / PORT env vars
```

For Docker, build `./protected` in a build stage and `COPY` it into the image
instead of your source. See
[packaging](https://docs.camouflage.network/obfy/guides/packaging) and
[deploying](https://docs.camouflage.network/obfy/deploying).

## Honest posture

Python obfuscation is **deterrence, not encryption-grade security** — CPython must
eventually execute real bytecode. obfy stops casual copying and raises the cost for
everyone else; it does not replace legal protection for sensitive IP. See the
[honest posture](https://docs.camouflage.network/obfy/guides/obfuscation-levels#honest-posture).

## Docs

Full obfy documentation: **[docs.camouflage.network/obfy](https://docs.camouflage.network/obfy/introduction)**.

## License

MIT — see [LICENSE](./LICENSE). The code you build with this template is yours.
