import pytest

from src.generators import filter_by_currency, card_number_generator, transaction_descriptions
from typing import Iterable, Dict, Any, Iterator


# Исправленные тесты для filter_by_currency
def test_filter_by_currency_success():
    transactions = [
        {"currency": "USD", "amount": 100},
        {"currency": "EUR", "amount": 200},
        {"currency": "USD", "amount": 300},
        {"currency": "RUB", "amount": 400}
    ]

    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert result[0]["amount"] == 100
    assert result[1]["amount"] == 300


def test_filter_by_currency_no_matches():
    transactions = [
        {"currency": "EUR", "amount": 200},
        {"currency": "RUB", "amount": 400}
    ]

    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0


def test_filter_by_currency_none_input():
    result = list(filter_by_currency(None, "USD"))
    assert result == []  # Исправлено сравнение с None на пустой список




# Исправленные тесты для card_number_generator
def test_card_number_generator_basic():
    gen = card_number_generator(1000000000000000, 1000000000000002)
    expected = ["1000 0000 0000 0000",
                "1000 0000 0000 0001",
                "1000 0000 0000 0002"]

    result = list(gen)
    assert result == expected


def test_card_number_generator_edge_cases():
    # Минимальное значение
    gen_min = card_number_generator(1000000000000000)
    assert next(gen_min) == "1000 0000 0000 0000"

    # Максимальное значение
    gen_max = card_number_generator(9999999999999999)
    assert next(gen_max) == "9999 9999 9999 9999"


def test_card_number_generator_format():
    gen = card_number_generator(1234567890123456)
    number = next(gen)
    assert number == "1234 5678 9012 3456"
    assert len(number) == 19  # 16 цифр + 3 пробела


def test_filter_by_currency():
    transactions = [
        {"amount": 100, "currency": "USD", "date": "2026-02-02"},
        {"amount": 200, "currency": "EUR", "date": "2026-02-03"},
        {"amount": 300, "currency": "USD", "date": "2026-02-04"},
    ]

    # Проверка возврата итератора
    result = filter_by_currency(transactions, "USD")
    assert isinstance(result, Iterator)

    # Проверка фильтрации
    filtered = list(result)
    assert len(filtered) == 2
    assert all(tx["currency"] == "USD" for tx in filtered)


def test_transaction_descriptions():
    transactions = [
        {"amount": 100, "currency": "USD", "date": "2026-02-02"},
        {"amount": 200, "currency": "EUR", "date": "2026-02-03"},
    ]

    descriptions = list(transaction_descriptions(transactions))
    assert len(descriptions) == 2
    assert descriptions[0] == "Транзакция: 100 USD от 2026-02-02"
    assert descriptions[1] == "Транзакция: 200 EUR от 2026-02-03"

def test_full_data():
    transactions = [
        {
            'amount': 100,
            'currency': 'USD',
            'date': '2023-01-01'
        }
    ]
    result = list(transaction_descriptions(transactions))
    assert result[0] == "Транзакция: 100 USD от 2023-01-01"

def test_missing_amount():
    transactions = [
        {'currency': 'EUR', 'date': '2023-01-02'}
    ]
    result = list(transaction_descriptions(transactions))
    assert result[0] == "Транзакция: EUR от 2023-01-02"

def test_empty_transaction():
    transactions = [{}]
    result = list(transaction_descriptions(transactions))
    assert result[0] == "Транзакция: "

def test_multiple_transactions():
    transactions = [
        {'amount': 50, 'currency': 'RUB'},
        {'date': '2023-01-03'}
    ]
    result = list(transaction_descriptions(transactions))
    assert result[0] == "Транзакция: 50 RUB"
    assert result[1] == "Транзакция: от 2023-01-03"
