import pytest
from src.decorators import log  # относительный импорт
import time

class TestLogDecorator:
    def test_successful_execution_console(self, capsys):
        @log()
        def add(a: int, b: int) -> int:
            return a + b

        result = add(5, 3)
        captured = capsys.readouterr()

        assert result == 8
        assert "Вызов функции: add" in captured.out
        assert "args=(5, 3), kwargs={}" in captured.out
        assert "Функция add выполнена успешно" in captured.out
        assert "Результат: 8" in captured.out

    def test_function_with_kwargs(self, capsys):
        @log()
        def greet(name: str, greeting: str = "Привет") -> str:
            return f"{greeting}, {name}!"

        result = greet("Анна", greeting="Здравствуйте")
        captured = capsys.readouterr()

        assert result == "Здравствуйте, Анна!"
        assert "Вызов функции: greet" in captured.out
        assert "Анна" in captured.out  # имя в args
        assert "Здравствуйте" in captured.out  # значение greeting в kwargs

    def test_no_arguments_function(self, capsys):
        @log()
        def get_random() -> int:
            import random
            return random.randint(1, 100)

        result = get_random()
        captured = capsys.readouterr()

        assert 1 <= result <= 100
        assert "Вызов функции: get_random" in captured.out
        assert "args=(), kwargs={}" in captured.out

    def test_nested_functions(self, capsys):
        @log()
        def outer(x: int) -> int:
            @log()
            def inner(y: int) -> int:
                return y * 2
            return inner(x) + 1

        result = outer(5)
        captured = capsys.readouterr()

        assert result == 11
        assert "Вызов функции: outer" in captured.out
        assert "Вызов функции: inner" in captured.out
        assert "Функция inner выполнена успешно" in captured.out
        assert "Функция outer выполнена успешно" in captured.out

    def test_file_logging(self, tmp_path):
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def multiply(x: int, y: int) -> int:
            return x * y

        multiply(4, 7)

        time.sleep(0.1)  # задержка для надёжности

        assert log_file.exists()
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        assert "Вызов функции: multiply" in content
        assert "args=(4, 7), kwargs={}" in content
        assert "Функция multiply выполнена успешно" in content
        assert "Результат: 28" in content