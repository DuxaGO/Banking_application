from fastapi import FastAPI, HTTPException
from src.external_api import convert_currency
from api.schemas import ConvertRequest

app = FastAPI()

@app.post("/convert")
def convert(data: ConvertRequest):
    result = convert_currency(...)

    if result is None:
        raise HTTPException(status_code=400, detail="Conversion failed")

    return {
        "amount": data.amount,
        "from_currency": data.from_currency,
        "to_currency": data.to_currency,
        "result": result
    }