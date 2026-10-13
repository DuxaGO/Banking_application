from pydantic import BaseModel


class ConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str = "RUB"