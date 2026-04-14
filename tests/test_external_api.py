from unittest.mock import Mock, patch

from src.external_api import convert_currency, convert_transaction_to_rub


class TestExternalAPI:
    @patch('src.external_api.requests.get')
    @patch('src.external_api.os.getenv', return_value='test_api_key')
    def test_convert_currency_success(self, mock_getenv, mock_get):
        """Тест: успешная конвертация валюты."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 7500.0}
        mock_get.return_value = mock_response

        result = convert_currency(100, 'USD', 'RUB')
        assert result == 7500.0

    @patch('src.external_api.requests.get')
    @patch('src.external_api.os.getenv', return_value='test_api_key')
    def test_convert_transaction_to_rub_usd(self, mock_getenv, mock_get):
        """Тест конвертации транзакции USD в RUB."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 7500.0}
        mock_get.return_value = mock_response

        transaction = {"amount": 100, "currency": "USD"}
        result = convert_transaction_to_rub(transaction)
        assert result == 7500.0

    def test_convert_transaction_to_rub_rub(self):
        """Тест без конвертации (уже в RUB)."""
        transaction = {"amount": 1000, "currency": "RUB"}
        result = convert_transaction_to_rub(transaction)
        assert result == 1000.0
