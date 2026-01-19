import pytest

from src.masks import get_mask_card_number, get_mask_account

@pytest.mark.parametrize("card_number,expected", [
    ("1234 1234 1234 1234","123412******1234"),
    ("4321-4321-4321-4321","432143******4321")
])
def test_valid_card_parametrize(card_number, expected):
    result = get_mask_card_number(card_number)
    assert result == expected

@pytest.mark.parametrize("invalid_string", [
    "",
    "    ",
    "123asd3214"
])
def test_invalid_string_parametrize(invalid_string):
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_string)

@pytest.mark.parametrize("account_number, expected", [
    ("12345123451234512345","****************2345"),
    ("12345-12345-12345-12345","****************2345")
])
def test_valid_account_parametrize(account_number, expected):
    result = get_mask_account(account_number)
    assert result == expected

@pytest.mark.parametrize("invalid_string", [
    "",
    "   ",
    "asdfq12123"
])
def test_invalid_string_account_parametrize(invalid_string):
    with pytest.raises(ValueError):
        get_mask_account(invalid_string)

