from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"  # API для курса валют


@app.get("/")
def read_root():
    return {"message": "Welcome to the Dollar to Ruble Converter API"}


@app.get("/convert/")
async def convert_dollars_to_rubles(amount: float):
    """
    Конвертирует сумму в долларах в рубли.
    :param amount: Сумма в долларах
    :return: Конвертированная сумма в рублях
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL)
            response.raise_for_status()
            data = response.json()

        # Получение курса рубля
        ruble_rate = data["rates"].get("RUB")
        if not ruble_rate:
            raise HTTPException(status_code=500, detail="Currency rate for RUB not found.")

        # Конвертация
        rub_amount = amount * ruble_rate
        return {
            "amount_in_usd": amount,
            "amount_in_rub": rub_amount,
            "exchange_rate": ruble_rate
        }

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch exchange rates: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
