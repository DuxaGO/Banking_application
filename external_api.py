import requests
import os
from typing import Optional

def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> Optional[float]:
    """
    Получает текущий курс обмена валюты через API.

    Args:
        base_currency (str): Базовая валюта (например, USD, EUR).
        target_currency (str): Целевая валюта (по умолчанию RUB).

    Returns:
        Optional[float]: Курс обмена или None в случае ошибки.
    """
    api_key = os.getenv('EXCHANGE_API_KEY')
    if not api_key:
        raise ValueError("API key not found in environment variables")

    url = "https://api.apilayer.com/exchangerates_data/latest"
    params = {
        'base': base_currency,
        'symbols': target_currency
    }
    headers = {
        'apikey': api_key
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['rates'][target_currency]
    except (requests.RequestException, KeyError) as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict[str, Any]): Словарь с данными транзакции.

    Returns:
        float: Сумма в рублях.
    """
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB')

    if currency == 'RUB':
        return float(amount)

    rate = get_exchange_rate(currency)
    if rate is not None:
        return float(amount * rate)
    else:
        raise ValueError(f"Failed to convert {currency} to RUB")