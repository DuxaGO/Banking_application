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
