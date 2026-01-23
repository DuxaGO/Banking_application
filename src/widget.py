from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """
    Принимает название карты и ее номер или счет и транфорирует в зааскированную версию
    Для карт: шаблон «7000 79** **** 6361»
    Для счетов: шаблон «**XXXX» (две звёздочки + последние 4 цифры)

    Args:
        info (str): Например, "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"


    Returns:
        str: Замаскированная строка, например:
               - "Visa Platinum 7000 79** **** 6361" (карта)
               - "Счет **4305" (счёт)
    :param info:
    :return:
    """
    # разбиваем по частям
    parts = info.strip().split()
    if len(parts) < 2:
        return info  # Если формат не соответсвует возвращаем исходник

    # Определяем тип данных
    type_part = ' '.join(parts[:-1])
    number_part = parts[-1]
    valid_account_types = {"счет", "счёт"}

    if type_part.lower() in valid_account_types:
        # Если это счёт — оборачиваем в try/except
        try:
            masked_number = get_mask_account(number_part)
        except ValueError:
            masked_number = number_part  # Возвращаем исходный номер при ошибке
    else:
        # Если это карта — уже есть обработка ошибок
        try:
            masked_number = get_mask_card_number(number_part)
        except ValueError:
            masked_number = number_part

    return f'{type_part} {masked_number}'


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата "2024-03-11T02:26:18.671407" в "ДД.ММ.ГГГГ".
    :param date_string:
    :return:
    """

    date_string = date_string.strip()
    if not date_string:  # если после обрезки строка пуста
        return date_string

    # удаляем все что может находиться после символа Т и его тоже
    if 'T' in date_string:
        date_part = date_string.split('T')[0]
    else:
        date_part = date_string  # возвращаем если не соответсвует

    # разбиваем по "-"
    parts = date_part.split('-')

    # если формат нет сооветствует возвращаем исходник
    if len(parts) != 3:
        return date_string

    year, month, day = parts

    # проверяем все параметры даты на соответствие длинны и числам
    if (
        len(year) == 4
        and len(month) == 2
        and len(day) == 2
        and year.isdigit()
        and month.isdigit()
        and day.isdigit()
    ):
        return f'{day}.{month}.{year}'
    else:
        return date_string  # возвращаем если не соответсвует
