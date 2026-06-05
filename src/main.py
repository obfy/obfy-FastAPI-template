from fastapi import FastAPI

from app.schemas import QuoteResponse
from app.services import pricing_quote

app = FastAPI(title="obfy FastAPI example")


@app.get("/quote", response_model=QuoteResponse)
def quote(units: int = 1) -> dict:
    return pricing_quote(units)
