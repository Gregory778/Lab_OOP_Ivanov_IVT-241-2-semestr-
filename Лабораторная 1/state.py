# Управление соединением с БД (отключено, подключается, подключено, ошибка)
from abc import ABC, abstractmethod
import time


class ConnectionState(ABC):
    @abstractmethod
    def connect(self, conn):
        pass

    @abstractmethod
    def disconnect(self, conn):
        pass

    @abstractmethod
    def execute_query(self, conn, query: str):
        pass


class DisconnectedState(ConnectionState):
    def connect(self, conn):
        print("Подключение к базе данных...")
        conn.state = ConnectingState()

    def disconnect(self, conn):
        print("Уже отключено")

    def execute_query(self, conn, query: str):
        print("Ошибка: нет подключения к БД")


class ConnectingState(ConnectionState):
    def connect(self, conn):
        print("Подключение уже выполняется")

    def disconnect(self, conn):
        print("Отмена подключения")
        conn.state = DisconnectedState()

    def execute_query(self, conn, query: str):
        print("Ошибка: подключение ещё не установлено")


class ConnectedState(ConnectionState):
    def connect(self, conn):
        print("Уже подключено")

    def disconnect(self, conn):
        print("Отключение от БД")
        conn.state = DisconnectedState()

    def execute_query(self, conn, query: str):
        print(f"Выполнение запроса: {query}")
        print("Результат: 10 строк")


class ErrorState(ConnectionState):
    def connect(self, conn):
        print("Попытка переподключения после ошибки")
        conn.state = ConnectingState()

    def disconnect(self, conn):
        print("Отключение после ошибки")
        conn.state = DisconnectedState()

    def execute_query(self, conn, query: str):
        print("Ошибка: соединение в состоянии ошибки")


class DatabaseConnection:
    def __init__(self):
        self.state = DisconnectedState()

    def connect(self):
        self.state.connect(self)

    def disconnect(self):
        self.state.disconnect(self)

    def query(self, sql: str):
        self.state.execute_query(self, sql)


if __name__ == "__main__":
    db = DatabaseConnection()
    db.query("SELECT * FROM users")

    db.connect()
    db.query("SELECT * FROM users")

    db.disconnect()
    db.query("SELECT * FROM users")