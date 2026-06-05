from pydantic import BaseModel


class QuoteResponse(BaseModel):
    units: int
    unit_price: float
    discount: float
    total: float
