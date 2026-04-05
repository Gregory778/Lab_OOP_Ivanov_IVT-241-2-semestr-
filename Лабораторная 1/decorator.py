# Добавление функциональности к функциям без изменения их кода
import time
from functools import wraps


def timer_decorator(func):
    """Замеряет время выполнения функции"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} выполнена за {end - start:.4f} секунд")
        return result

    return wrapper


def cache_decorator(func):
    """Кэширует результаты вызовов"""
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key in cache:
            print(f"[CACHE] Возврат кэшированного результата для {func.__name__}")
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        print(f"[CACHE] Сохранён результат для {func.__name__}")
        return result

    return wrapper


def log_decorator(func):
    """Логирует вызовы функций"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Вызов {func.__name__} с аргументами: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} вернула: {result}")
        return result

    return wrapper


def retry_decorator(max_retries=3, delay=1):
    """Повторяет выполнение при ошибках"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY] Попытка {attempt + 1} не удалась: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        raise
            return None

        return wrapper

    return decorator


# Пример использования
@timer_decorator
@log_decorator
def slow_function(n):
    time.sleep(0.5)
    return sum(range(n))


@cache_decorator
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@retry_decorator(max_retries=3, delay=0.5)
def unstable_network_call():
    import random
    if random.random() < 0.7:
        raise Exception("Сетевая ошибка")
    return "Успешно!"


if __name__ == "__main__":
    print("=== Пример с таймером и логированием ===")
    result = slow_function(100)
    print(f"Результат: {result}")

    print("\n=== Пример с кэшированием ===")
    print(fibonacci(10))
    print(fibonacci(10))  # Из кэша

    print("\n=== Пример с повторами ===")
    result = unstable_network_call()
    print(f"Результат: {result}")