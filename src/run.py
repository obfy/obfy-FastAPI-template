"""Production-style entry point.

Imports the FastAPI app object directly and hands it to uvicorn. Passing the
object (not the `"main:app"` import string) keeps it working even at higher
obfuscation levels, where public names can be renamed.
"""

import os

import uvicorn

from main import app


def serve() -> None:
    uvicorn.run(
        app,
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8000")),
    )


if __name__ == "__main__":
    serve()
