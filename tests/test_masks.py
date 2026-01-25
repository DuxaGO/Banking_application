import pytest

from src.masks import get_mask_account, get_mask_card_number

# Тесты без фикстур
@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("1234 1234 1234 1234", "123412******1234"),
        ("4321-4321-4321-4321", "432143******4321"),
    ],
)
def test_valid_card_parametrize(card_number, expected):
    result = get_mask_card_number(card_number)
    assert result == expected


@pytest.mark.parametrize("invalid_string", ["", "    ", "123asd3214"])
def test_invalid_string_parametrize(invalid_string):
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_string)


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("12345123451234512345", "****************2345"),
        ("12345-12345-12345-12345", "****************2345"),
    ],
)
def test_valid_account_parametrize(account_number, expected):
    result = get_mask_account(account_number)
    assert result == expected


@pytest.mark.parametrize("invalid_string", ["", "   ", "asdfq12123"])
def test_invalid_string_account_parametrize(invalid_string):
    with pytest.raises(ValueError):
        get_mask_account(invalid_string)


# Фикстура: тестовые данные в виде словаря (ключ — исходная строка, значение — ожидаемый результат)
@pytest.fixture
def account_test_data():
    return {
        "12345123451234512345": "****************2345",
        "12345-12345-12345-12345": "****************2345",
        "98765432109876543210": "****************3210"
    }

# Фикстура: контекстный менеджер для временного изменения состояния (например, логирования)
@pytest.fixture
def mock_logging():
    class MockLogger:
        def __init__(self):
            self.messages = []

        def log(self, message):
            self.messages.append(message)

    logger = MockLogger()
    # Здесь можно подменить реальный логгер на MockLogger
    return logger

def test_mask_account_valid_data(account_test_data):
    """Тест с фикстурой-словарём: проверяем маскировку счетов."""
    for account_number, expected in account_test_data.items():
        result = get_mask_account(account_number)
        assert result == expected

def test_mask_account_with_logging(mock_logging):
    """Тест с фикстурой-контекст-менеджером: проверяем логирование ошибок."""
    invalid_account = "invalid_account"

    try:
        get_mask_account(invalid_account)
    except ValueError as e:
        mock_logging.log(f"Error: {e}")

    # Проверяем, что ошибка была залогирована
    assert len(mock_logging.messages) == 1
    assert "Error" in mock_logging.messages[0]

# Фикстура: набор валидных номеров карт (возвращает список)
@pytest.fixture
def valid_card_numbers():
    return [
        "1234 1234 1234 1234",
        "4321-4321-4321-4321",
        "5555 5555 5555 5555"
    ]

# Фикстура: набор невалидных строк (возвращает генератор)
@pytest.fixture
def invalid_card_strings():
    return ("", "    ", "123asd3214", "1234")


def test_mask_card_valid_numbers(valid_card_numbers):
    """Тест с фикстурой-списком: проверяем маскировку валидных номеров."""
    for card_number in valid_card_numbers:
        result = get_mask_card_number(card_number)

        # 1. Проверяем общую длину (должна быть 16)
        assert len(result) == 16, f"Длина результата != 16: {result}"

        # 2. Проверяем первые 4 символа — должны быть цифрами
        assert result[:4].isdigit(), f"Первые 4 символа не цифры: {result[:4]}"

        # # 3. Проверяем средние 6 символов — должны быть звёздочками
        # assert result[4:10] == "******", f"Средние 6 символов не звёздочки: {result[4:10]}"
        # # 4. Проверяем последние 4 символа — должны быть цифрами
        # assert result[10:].isdigit(), f"Последние 4 символа не цифры: {result[10:]}"

        # 5. Дополнительно: проверяем, что в результате нет пробелов/дефисов
        assert " " not in result and "-" not in result, f"Есть разделители в результате: {result}"

def test_mask_card_invalid_strings(invalid_card_strings):
    """Тест с фикстурой-генератором: проверяем обработку невалидных строк."""
    for invalid_string in invalid_card_strings:
        with pytest.raises(ValueError):
            get_mask_card_number(invalid_string)