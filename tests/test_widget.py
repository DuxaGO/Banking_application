import pytest

from src. import mask_account_card

@pytest.mark.parametrize("card_number, expected", [
    ("1234 1234 1234 1234","123412******1234"),
    ("4321-4321-4321-4321","432143******4321")
])
def test_valid_card_number_parametrize(card_number, expected):
    result = mask_account_card(card_number)
    assert result == expected