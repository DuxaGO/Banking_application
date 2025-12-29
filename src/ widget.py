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
        return info # Если формат не соответсвует возвращаем исходник


    # Определяем тип данных
    type_part = ' '.join(parts[:-1])
    number_part = parts[-1]


    # Счет должен состоять только из цифр, если нет возвращаем исходник
    if not number_part.isdigit():
        return info

    if type_part.lower() == 'счет':
        # если счет
        masked_number = '**' + number_part[-4:]
    else:
        # для карты проверяем длину, должно быть 16 символов
        if len(number_part) != 16:
            return info


        # формируем маску для карты: 7000 79** **** 6361
        masked_number = (
            number_part[:4] + ' ' +
            number_part[4:6] + '**' + ' ' +
            '****' + ' ' + number_part[-4:]
        )
    return f'{type_part} {masked_number}'


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата "2024-03-11T02:26:18.671407" в "ДД.ММ.ГГГГ".
    :param date_string:
    :return:
    """

    # удаляем все что может находиться после символа Т и его тоже
    if 'T' in date_string:
        date_part = date_string.split('T')[0]
    else:
        date_part = date_string # возвращаем если не соответсвует

    # разбиваем по "-"
    parts = date_part.split('-')

    # если формат нет сооветствует возвращаем исходник
    if len(parts) != 3:
        return date_string

    year, month, day = parts

    # проверяем все параметры даты на соответствие длинны и числам
    if (len(year) == 4 and len(month) == 2 and len(day) ==2 and year.isdigit() and month.isdigit() and day.isdigit()):
        return f'{day}.{month}.{year}'
    else:
        return date_string # возвращаем если не соответсвует



# Блок кода с тестированием
if __name__ == '__main__':
    # для карты
    print(mask_account_card("Visa Platinum 7000792289606361"))

    print(mask_account_card("Maestro 7000792289606361"))

    # для счета
    print(mask_account_card("Счет 73654108430135874305"))

    # краевые случаи
    # Краевые случаи
    print(mask_account_card("Карта 12345"))  # → Карта 12345 (не 16 цифр)
    print(mask_account_card("Счет ABCD1234"))  # → Счет ABCD1234 (не цифры)
    print(mask_account_card("Короткая строка"))  # → Короткая строка (мало частей)


# Тестирование функции
if __name__ == "__main__":
    # ... предыдущие тесты для mask_account_card ...

    # Тест для get_date
    print(get_date("2024-03-11T02:26:18.671407"))  # → 11.03.2024
    print(get_date("2025-12-29"))                      # → 29.12.2025
    print(get_date("Некорректная дата"))             # → Некорректная дата
    print(get_date("2024-5-5"))                   # → 2024-5-5 (не 2 цифры)
