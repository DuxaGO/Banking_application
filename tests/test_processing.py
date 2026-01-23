import pytest
from src.processing import filter_by_state, sort_by_date  # замените yourmodule на имя вашего модуля

@pytest.mark.parametrize(
    "data, state, expected",
    [
        # 1. Базовый случай: есть совпадения
        (
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2, "state": "PENDING"},
                {"id": 3, "state": "EXECUTED"}
            ],
            "EXECUTED",
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 3, "state": "EXECUTED"}
            ]
        ),

        # 2. Нет совпадений
        (
            [
                {"id": 1, "state": "PENDING"},
                {"id": 2, "state": "FAILED"}
            ],
            "EXECUTED",
            []
        ),

        # 3. state отсутствует в некоторых словарях
        (
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2},  # нет ключа state
                {"id": 3, "state": "EXECUTED"}
            ],
            "EXECUTED",
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 3, "state": "EXECUTED"}
            ]
        ),

        # 4. state не совпадает ни с одним
        (
            [{"id": 1, "state": "CANCELED"}],
            "EXECUTED",
            []
        ),

        # 5. Пустой список
        (
            [],
            "EXECUTED",
            []
        ),

        # 6. Другой state (не EXECUTED)
        (
            [
                {"id": 1, "state": "PENDING"},
                {"id": 2, "state": "PENDING"}
            ],
            "PENDING",
            [
                {"id": 1, "state": "PENDING"},
                {"id": 2, "state": "PENDING"}
            ]
        ),

        # 7. Все элементы имеют нужный state
        (
            [
                {"id": 1, "state": "COMPLETED"},
                {"id": 2, "state": "COMPLETED"}
            ],
            "COMPLETED",
            [
                {"id": 1, "state": "COMPLETED"},
                {"id": 2, "state": "COMPLETED"}
            ]
        )
    ]
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
                {"id": 3, "date": "2022-01-01"}
            ],
            True,
            [
                {"id": 2, "date": "2024-01-01"},  # самая поздняя
                {"id": 1, "date": "2023-01-01"},
                {"id": 3, "date": "2022-01-01"}   # самая ранняя
            ]
        ),

        # 2. Сортировка по возрастанию (reverse=False)
        (
            [
                {"id": 1, "date": "2023-01-01"},
                {"id": 2, "date": "2024-01-01"},
                {"id": 3, "date": "2022-01-01"}
            ],
            False,
            [
                {"id": 3, "date": "2022-01-01"},  # самая ранняя
                {"id": 1, "date": "2023-01-01"},
                {"id": 2, "date": "2024-01-01"}   # самая поздняя
            ]
        ),

        # 3. Даты в нестандартном формате (но строки)
        (
            [
                {"id": 1, "date": "01.01.2023"},
                {"id": 2, "date": "01.01.2024"},
                {"id": 3, "date": "01.01.2022"}
            ],
            True,
            [
                {"id": 2, "date": "01.01.2024"},
                {"id": 1, "date": "01.01.2023"},
                {"id": 3, "date": "01.01.2022"}
            ]
        ),

        # 4. Отсутствует ключ date
        (
            [
                {"id": 1},  # нет date
                {"id": 2, "date": "2024-01-01"},
                {"id": 3}   # нет date
            ],
            True,
            [
                {"id": 2, "date": "2024-01-01"},  # единственный с date
                {"id": 1},
                {"id": 3}
            ]
        ),

        # 5. Все элементы без date
        (
            [
                {"id": 1},
                {"id": 2}
            ],
            True,
            [
                {"id": 1},
                {"id": 2}
            ]
        ),

        # 6. Пустой список
        (
            [],
            True,
            []
        ),

        # 7. Один элемент
        (
            [{"id": 1, "date": "2025-01-01"}],
            True,
            [{"id": 1, "date": "2025-01-01"}]
        ),

        # 8. Даты с разным форматом строк (сортировка лексикографическая)
        (
            [
                {"id": 1, "date": "2023"},
                {"id": 2, "date": "2023-01"},
                {"id": 3, "date": "2023-01-01"}
            ],
            True,
            [
                {"id": 3, "date": "2023-01-01"},
                {"id": 2, "date": "2023-01"},
                {"id": 1, "date": "2023"}
            ]
        )
    ]
)
def test_sort_by_date(data, reverse, expected):
    result = sort_by_date(data, reverse)
    assert result == expected