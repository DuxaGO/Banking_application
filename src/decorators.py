import datetime
import functools
import logging
import sys

from typing import Any, Callable, Optional, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(filename: Optional[str] = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Создаём отдельный логгер для каждой функции
            logger = logging.getLogger(f"{func.__module__}.{func.__name__}")
            logger.setLevel(logging.INFO)
            logger.propagate = False  # Отключаем распространение вверх
            logger.handlers.clear()  # Удаляем старые обработчики

            # Настраиваем обработчик
            if filename:
                handler = logging.FileHandler(filename, encoding='utf-8')
            else:
                handler = logging.StreamHandler(sys.stdout)  # Явно направляем в stdout

            formatter = logging.Formatter(
                '%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            start_time = datetime.datetime.now()
            logger.info(f"Вызов функции: {func.__name__}")
            logger.info(f"Аргументы: args={args}, kwargs={kwargs}")

            try:
                result = func(*args, **kwargs)
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                logger.info(
                    f"Функция {func.__name__} выполнена успешно за {execution_time:.4f} сек. "
                    f"Результат: {result}"
                )
                return result
            except Exception as e:
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                logger.error(
                    f"Ошибка в функции {func.__name__}: {type(e).__name__}: {e}. "
                    f"Аргументы при вызове: args={args}, kwargs={kwargs}. "
                    f"Время выполнения до ошибки: {execution_time:.4f} сек."
                )
                raise
            finally:
                logger.removeHandler(handler)
                handler.close()

        return wrapper

    return decorator
