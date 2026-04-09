import pytest
import json
from unittest.mock import mock_open, patch
from utils import load_transactions_from_json

class TestLoadTransactionsFromJSON:
    def test_valid_json_file(self):
        """Тест: корректный JSON-файл с списком транзакций."""
        mock_data = [
            {"id": 1, "amount": 1000, "currency": "RUB"},
            {"id": 2, "amount": 50, "currency": "USD"}
        ]
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            result = load_transactions_from_json("dummy_path.json")
            assert result == []

    def test_empty_file(self):
        """Тест: пустой файл."""
        with patch("builtins.open", mock_open(read_data="")):
            result = load_transactions_from_json("empty.json")
            assert result == []

    def test_file_not_found(self):
        """Тест: файл не найден."""
        result = load_transactions_from_json("nonexistent.json")
        assert result == []

    def test_invalid_json(self):
        """Тест: некорректный JSON."""
        with patch("builtins.open", mock_open(read_data="{invalid json}")):
            result = load_transactions_from_json("invalid.json")
            assert result == []

    def test_not_a_list(self):
        """Тест: JSON содержит не список."""
        with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
            result = load_transactions_from_json("not_list.json")
            assert result == []