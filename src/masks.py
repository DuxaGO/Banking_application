def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляет первые 6 и последние 4 цифры
    # :param card_number: Номер карты
    # :return: Замасуированный номер карты
    """
    # Удаляем пробелы и дефисы
    cleaned = card_number.replace(" ", "").replace("-", "")

    if not cleaned.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if len(cleaned) < 13 or len(cleaned) > 19:
        raise ValueError("Некорректная длинна номера карты")

    visible_start = cleaned[:6]
    visible_end = cleaned[-4:]
    masked = visible_start + "*" * (len(cleaned) - 10) + visible_end
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета, оставляет посследние 4 цифры
    :param account_number: Номер счета
    :return: ЗАмаскированный номер банковского счета
    """
    # Удаляем пробелы и дефисы
    cleaned = account_number.replace(" ", "").replace("-", "")

    if not cleaned.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    if len(cleaned) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")
    visible_num = cleaned[-4:]
    masked = "*" * 16 + visible_num
    return masked


# Пример для карты
print(get_mask_card_number("1234 5678 9012 3456"))  # 123456******3456

# Пример для счёта
print(get_mask_account("1234 5678 9012 3456 7890"))  # ****************7890
