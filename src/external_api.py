import os

from typing import Optional

import requests

from dotenv import load_dotenv

load_dotenv()


def convert_currency(
    amount: float, from_currency: str, to_currency: str = "RUB"
) -> Optional[float]:
    """
    Конвертирует сумму из одной валюты в другую через API.

    Args:
        amount (float): Сумма для конвертации.
        from_currency (str): Исходная валюта (например, USD, EUR).
        to_currency (str): Целевая валюта (по умолчанию RUB).

    Returns:
        Optional[float]: Конвертированная сумма или None в случае ошибки.
    """
    api_key = os.getenv('EXCHANGE_API_KEY')
    if not api_key:
        return None

    url = "https://api.apilayer.com/exchangerates_data/convert"
    params = {'to': to_currency, 'from': from_currency, 'amount': amount}
    headers = {'apikey': api_key}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['result']
    except (requests.RequestException, KeyError) as e:
        print(f"Error in currency conversion: {e}")
        return None


def convert_transaction_to_rub(transaction: dict) -> float:
    """
    Конвертирует транзакцию в рубли.

    Args:
        transaction (dict): Словарь с данными о транзакции.
    Returns:
        float: Сумма в рублях.
    """
    amount = transaction['amount']
    currency = transaction.get('currency', 'RUB')

    if currency == 'RUB':
        return float(amount)

    converted_amount = convert_currency(amount, currency, 'RUB')
    if converted_amount is None:
        raise ValueError(f"Не удалось конвертировать {amount} {currency} в RUB")

    return float(converted_amount)
