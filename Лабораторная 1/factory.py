# Фабрика создаёт логгеры для разных назначений (файл, консоль, сеть)
from abc import ABC, abstractmethod
from datetime import datetime


class Logger(ABC):
    @abstractmethod
    def log(self, message: str, level: str):
        pass


class FileLogger(Logger):
    def __init__(self, filename: str):
        self.filename = filename

    def log(self, message: str, level: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, 'a') as f:
            f.write(f"[{timestamp}] {level}: {message}\n")
        print(f"Записано в файл {self.filename}")


class ConsoleLogger(Logger):
    def log(self, message: str, level: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")


class NetworkLogger(Logger):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def log(self, message: str, level: str):
        # Симуляция отправки по сети
        print(f"Отправка на {self.host}:{self.port} - {level}: {message}")


class LoggerFactory(ABC):
    @abstractmethod
    def create_logger(self) -> Logger:
        pass


class FileLoggerFactory(LoggerFactory):
    def __init__(self, filename: str):
        self.filename = filename

    def create_logger(self) -> Logger:
        return FileLogger(self.filename)


class ConsoleLoggerFactory(LoggerFactory):
    def create_logger(self) -> Logger:
        return ConsoleLogger()


class NetworkLoggerFactory(LoggerFactory):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def create_logger(self) -> Logger:
        return NetworkLogger(self.host, self.port)


class Application:
    def __init__(self, factory: LoggerFactory):
        self.logger = factory.create_logger()

    def run(self):
        self.logger.log("Приложение запущено", "INFO")
        self.logger.log("Обработка данных", "DEBUG")
        self.logger.log("Завершение работы", "INFO")


if __name__ == "__main__":
    print("=== Консольный логгер ===")
    app = Application(ConsoleLoggerFactory())
    app.run()

    print("\n=== Файловый логгер ===")
    app = Application(FileLoggerFactory("app.log"))
    app.run()

    print("\n=== Сетевой логгер ===")
    app = Application(NetworkLoggerFactory("192.168.1.100", 514))
    app.run()