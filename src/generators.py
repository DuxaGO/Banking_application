from typing import List, Dict, Any, Iterable, Iterator

def filter_by_currency(transactions: Iterable[Dict[str, Any]], currency: str):
    """
    Фильтрует транзакции по указанной валюте
    """
    if transactions is None:
        return
    for transaction in transactions:
        if transaction.get("currency")  == currency:
            yield transaction

def card_number_generator(start: int = 1, end: int = 9999_9999_9999_9999) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате ХХХХ ХХХХ ХХХХ ХХХХ
    """
    if start < 1:
        raise ValueError('Start должен быть >= 1')
    if end > 9999_9999_9999_9999:
        raise ValueError("End должен быть не больше 9999_9999_9999_9999")
    if start > end:
        raise ValueError("start не может быть больше end")
    for number in range(start, end + 1):
        if len(f"{number}") > 16:
            raise ValueError("Номер должен содержать 16 цифр")
        num_str = f"{number:016d}"
        formated = f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
        yield formated