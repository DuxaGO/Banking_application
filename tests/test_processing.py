import pytest

from src.processing import (  # замените yourmodule на имя вашего модуля
    filter_by_state,
    sort_by_date,
)
from datetime import datetime

@pytest.mark.parametrize(
    "data, state, expected",
    [
        # 1. Базовый случай: есть совпадения
        (
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2, "state": "PENDING"},
                {"id": 3, "state": "EXECUTED"},
            ],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}],
        ),
        # 2. Нет совпадений
        ([{"id": 1, "state": "PENDING"}, {"id": 2, "state": "FAILED"}], "EXECUTED", []),
        # 3. state отсутствует в некоторых словарях
        (
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2},  # нет ключа state
                {"id": 3, "state": "EXECUTED"},
            ],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}],
        ),
        # 4. state не совпадает ни с одним
        ([{"id": 1, "state": "CANCELED"}], "EXECUTED", []),
        # 5. Пустой список
        ([], "EXECUTED", []),
        # 6. Другой state (не EXECUTED)
        (
            [{"id": 1, "state": "PENDING"}, {"id": 2, "state": "PENDING"}],
            "PENDING",
            [{"id": 1, "state": "PENDING"}, {"id": 2, "state": "PENDING"}],
        ),
        # 7. Все элементы имеют нужный state
        (
            [{"id": 1, "state": "COMPLETED"}, {"id": 2, "state": "COMPLETED"}],
            "COMPLETED",
            [{"id": 1, "state": "COMPLETED"}, {"id": 2, "state": "COMPLETED"}],
        ),
    ],
)
def test_filter_by_state(data, state, expected):
    result = filter_by_state(data, state)
    assert result == expected


@pytest.mark.parametrize(
    "data, reverse, expected",
    [
        # 1. Базовая сортировка по убыванию (reverse=True)
        (
            [
                {"id": 1, "date": "2023-01-01"},
                {"id": 2, "date": "2024-01-01"},
                {"id": 3, "date": "2022-01-01"},
            ],
            True,
            [
                {"id": 2, "date": "2024-01-01"},  # самая поздняя
                {"id": 1, "date": "2023-01-01"},
                {"id": 3, "date": "2022-01-01"},  # самая ранняя
            ],
        ),
        # 2. Сортировка по возрастанию (reverse=False)
        (
            [
                {"id": 1, "date": "2023-01-01"},
                {"id": 2, "date": "2024-01-01"},
                {"id": 3, "date": "2022-01-01"},
            ],
            False,
            [
                {"id": 3, "date": "2022-01-01"},  # самая ранняя
                {"id": 1, "date": "2023-01-01"},
                {"id": 2, "date": "2024-01-01"},  # самая поздняя
            ],
        ),
        # 3. Даты в нестандартном формате (но строки)
        (
            [
                {"id": 1, "date": "01.01.2023"},
                {"id": 2, "date": "01.01.2024"},
                {"id": 3, "date": "01.01.2022"},
            ],
            True,
            [
                {"id": 2, "date": "01.01.2024"},
                {"id": 1, "date": "01.01.2023"},
                {"id": 3, "date": "01.01.2022"},
            ],
        ),
        # 4. Отсутствует ключ date
        (
            [
                {"id": 1},  # нет date
                {"id": 2, "date": "2024-01-01"},
                {"id": 3},  # нет date
            ],
            True,
            [
                {"id": 2, "date": "2024-01-01"},  # единственный с date
                {"id": 1},
                {"id": 3},
            ],
        ),
        # 5. Все элементы без date
        ([{"id": 1}, {"id": 2}], True, [{"id": 1}, {"id": 2}]),
        # 6. Пустой список
        ([], True, []),
        # 7. Один элемент
        ([{"id": 1, "date": "2025-01-01"}], True, [{"id": 1, "date": "2025-01-01"}]),
        # 8. Даты с разным форматом строк (сортировка лексикографическая)
        (
            [
                {"id": 1, "date": "2023"},
                {"id": 2, "date": "2023-01"},
                {"id": 3, "date": "2023-01-01"},
            ],
            True,
            [
                {"id": 3, "date": "2023-01-01"},
                {"id": 2, "date": "2023-01"},
                {"id": 1, "date": "2023"},
            ],
        ),
    ],
)
def test_sort_by_date(data, reverse, expected):
    result = sort_by_date(data, reverse)
    assert result == expected

#  Тесты с использование фикстур
@pytest.fixture
def sample_data_with_states():
    """Базовый набор данных с разными значениями state."""
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "PENDING", "amount": 200},
        {"id": 3, "state": "EXECUTED", "amount": 300},
        {"id": 4, "state": "FAILED", "amount": 50},
        {"id": 5, "amount": 75},  # state отсутствует
    ]

@pytest.fixture
def empty_data():
    """Пустой список — крайний случай."""
    return []

@pytest.fixture
def all_executed_data():
    """Все элементы имеют state == "EXECUTED"."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-02"},
    ]

@pytest.fixture
def no_executed_data():
    """Ни один элемент не имеет state == "EXECUTED"."""
    return [
        {"id": 1, "state": "PENDING"},
        {"id": 2, "state": "FAILED"},
    ]

@pytest.fixture
def sample_data_with_dates():
    """Данные с корректными строковыми датами."""
    return [
        {"id": 1, "date": "2023-01-01T10:00:00", "amount": 100},
        {"id": 2, "date": "2Newton", "amount": 200},  # некорректная дата
        {"id": 3, "date": "2023-01-03T12:00:00", "amount": 300},
        {"id": 4, "date": "", "amount": 50},  # пустая строка
        {"id": 5, "amount": 75},  # ключа 'date' нет
    ]

@pytest.fixture
def data_with_none_dates():
    """Даты со значениями None."""
    return [
        {"id": 1, "date": None, "amount": 100},
        {"id": 2, "date": "2023-01-02T11:00:00", "amount": 200},
    ]

@pytest.fixture
def sorted_ascending_expected():
    """Ожидаемый результат для сортировки по возрастанию."""
    return [
        {"id": 1, "date": "2023-01-01T10:00:00", "amount": 100},
        {"id": 3, "date": "2023-01-03T12:00:00", "amount": 300},
    ]

@pytest.fixture
def data_only_valid_dates():
    """Только валидные даты — для проверки чистой сортировки."""
    return [
        {"id": 1, "date": "2023-01-05"},
        {"id": 2, "date": "2023-01-01"},
        {"id": 3, "date": "2023-01-03"},
    ]

def test_filter_by_state_default(sample_data_with_states):
    result = filter_by_state(sample_data_with_states)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)

def test_filter_by_state_empty(empty_data):
    result = filter_by_state(empty_data, "EXECUTED")
    assert result == []

def test_filter_by_state_all_match(all_executed_data):
    result = filter_by_state(all_executed_data, "EXECUTED")
    assert result == all_executed_data

def test_filter_by_state_no_match(no_executed_data):
    result = filter_by_state(no_executed_data, "EXECUTED")
    assert result == []

def test_sort_by_date_descending(sample_data_with_dates):
    result = sort_by_date(sample_data_with_dates, reverse=True)
    # Проверяем, что валидные даты отсортированы по убыванию
    dates = [item["date"] for item in result if "date" in item and item["date"]]
    assert dates == sorted([d for d in dates if d], reverse=True)

# def test_sort_by_date_ascending(data_only_valid_dates, sorted_ascending_expected):
#     result = sort_by_date(data_only_valid_dates, reverse=False)
#     # Оставляем только элементы с датой для сравнения
#     filtered_result = [item for item in result if "date" in item]
#     assert filtered_result == sorted_ascending_expected

def test_sort_by_date_with_none(data_with_none_dates):
    result = sort_by_date(data_with_none_dates, reverse=True)
    # None-значения должны идти в конце при reverse=True
    none_indices = [i for i, item in enumerate(result) if item.get("date") is None]
    assert none_indices == [len(result) - 1]  # последний элемент

def test_sort_by_date_empty(empty_data):
    result = sort_by_date(empty_data, reverse=True)
    assert result == []