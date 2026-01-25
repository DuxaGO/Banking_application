from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(
    data: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа state
    :param data: список словарей
    :param state: "EXECUTED", либо может отсутствовать
    :return: отфильтрованный список словарей
    """
    result = []
    for item in data:
        if item.get("state") == state:
            result.append(item)
    return result


def sort_by_date(
    data: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортируем список по дате, по умолчанию по убыванию
    """

    def get_sort_key(item: Dict[str, Any]) -> str:
        """
        Функция сортирует список словарей по ключу date в порядке убывания по умолчанию
        """
        date_val = item.get("date")
        if isinstance(date_val, str):
            return date_val
        return ""

    return sorted(data, key=get_sort_key, reverse=reverse)
