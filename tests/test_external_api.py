import pytest

from unittest.mock import patch, Mock
from external_api import convert_to_rubles, get_exchange_rate


class TestExternalAPI:
    @patch('external_api.requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        """Тест: успешный запрос курса валюты."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rates': {'RUB': 75.0}}
        mock_get.return_value = mock_response

        rate = get_exchange_rate('USD')
        assert rate == 75.0

    # @patch('external_api.requests.get')
    # def test_get_exchange_rate_failure(self, mock_get):
    #     """Тест: ошибка при запросе курса."""
    #     mock_get.side_effect = Exception("Network error")
    #
    #     rate = get_exchange_rate('USD')
    #     assert rate is None

    @patch('external_api.get_exchange_rate')
    def test_convert_usd_to_rub(self, mock_rate):
        """Тест: конвертация USD в RUB."""
        mock_rate.return_value = 75.0
        transaction = {"amount": 10, "currency": "USD"}
        result = convert_to_rubles(transaction)
        assert result == 750.0

    @patch('external_api.get_exchange_rate')
    def test_convert_eur_to_rub(self, mock_rate):
        """Тест: конвертация EUR в RUB."""
        mock_rate.return_value = 85.0
        transaction = {"amount": 20, "currency": "EUR"}
        result = convert_to_rubles(transaction)
        assert result == 1700.0

    def test_convert_rub_to_rub(self):
        """Тест: сумма уже в рублях."""
        transaction = {"amount": 1000, "currency": "RUB"}
        result = convert_to_rubles(transaction)
        assert result == 1000.0

    @patch('external_api.get_exchange_rate')
    def test_conversion_failure(self, mock_rate):
        """Тест: ошибка конвертации (курс не получен)."""
        mock_rate.return_value = None
        transaction = {"amount": 10, "currency": "USD"}

        with pytest.raises(ValueError):
            convert_to_rubles(transaction)