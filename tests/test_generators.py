import pytest

from src.generators import filter_by_currency, card_number_generator
from typing import Iterable, Dict, Any


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


def test_filter_by_currency_missing_currency():
    transactions = [
        {"amount": 100},
        {"currency": "USD", "amount": 200},
        {"currency": None, "amount": 300}
    ]

    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 1


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


# def test_card_number_generator_invalid_range():
#     # Исправлены проверки на корректные случаи ошибок
#     with pytest.raises(ValueError, match = "start не может быть больше end"):
#         card_number_generator(3, 1)  # start > end
#
#     with pytest.raises(ValueError, match ="start не может быть больше end"):
#         card_number_generator(9999999999999999, 1)  # обратный порядок
#
#     with pytest.raises(ValueError, match = "Start должен быть >= 1"):
#         card_number_generator(0)  # значение меньше минимального


def test_card_number_generator_format():
    gen = card_number_generator(1234567890123456)
    number = next(gen)
    assert number == "1234 5678 9012 3456"
    assert len(number) == 19  # 16 цифр + 3 пробела