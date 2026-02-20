from typing import Any, Dict, Generator, Iterable, Iterator, List


def filter_by_currency(
    transactions: Iterable[Dict[str, Any]], currency: str
) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по указанной валюте и возвращает итератор
    """
    if transactions is None:
        return iter(())  # Возвращаем пустой итератор

    filtered = [t for t in transactions if t['currency'] == currency]
    return iter(filtered)  # Возвращаем итератор, а не генератор


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) -> Generator[str]:
    """
    Генерирует описания транзакций в формате:
    "Транзакция: {amount} {currency} от {date}"

    Если поле отсутствует, оно пропускается.
    """
    for transaction in transactions:
        amount = transaction.get('amount')
        currency = transaction.get('currency')
        date = transaction.get('date')

        # Формируем описание, игнорируя отсутствующие поля
        parts = []
        if amount is not None:
            parts.append(str(amount))
        if currency is not None:
            parts.append(currency)
        if date is not None:
            parts.append(f"от {date}")

        description = "Транзакция: " + " ".join(parts)
        yield description


def card_number_generator(
    start: int = 1, end: int = 9999_9999_9999_9999
) -> Iterator[str]:
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
