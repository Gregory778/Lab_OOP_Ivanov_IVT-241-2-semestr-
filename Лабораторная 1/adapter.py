# Адаптер для MySQL, PostgreSQL и SQLite к единому интерфейсу
from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def connect(self, connection_string: str):
        pass

    @abstractmethod
    def execute(self, sql: str):
        pass

    @abstractmethod
    def fetch_one(self):
        pass


class MySQLDriver:
    def open_connection(self, host, user, password, database):
        print(f"MySQL: подключение к {host}/{database}")
        return "mysql_conn"

    def run_query(self, connection, query):
        print(f"MySQL: выполнение запроса '{query}'")
        return [{"id": 1, "name": "Alice"}]

    def close(self, connection):
        print("MySQL: закрытие соединения")


class PostgreSQLDriver:
    def connect_db(self, conn_string):
        print(f"PostgreSQL: подключение через {conn_string}")
        return "pg_conn"

    def query(self, connection, sql):
        print(f"PostgreSQL: выполнение '{sql}'")
        return [{"id": 1, "name": "Bob"}]

    def disconnect(self, connection):
        print("PostgreSQL: отключение")


class SQLiteDriver:
    def open(self, filepath):
        print(f"SQLite: открытие файла {filepath}")
        return "sqlite_conn"

    def exec(self, connection, command):
        print(f"SQLite: выполнение '{command}'")
        return [{"id": 1, "name": "Charlie"}]

    def close_db(self, connection):
        print("SQLite: закрытие")


class MySQLAdapter(Database):
    def __init__(self):
        self.driver = MySQLDriver()
        self.connection = None

    def connect(self, connection_string: str):
        # Парсим строку подключения mysql://user:pass@host/db
        parts = connection_string.replace("mysql://", "").split("/")
        host_part = parts[0].split("@")[1] if "@" in parts[0] else "localhost"
        db_name = parts[1] if len(parts) > 1 else "test"
        self.connection = self.driver.open_connection(host_part, "user", "pass", db_name)

    def execute(self, sql: str):
        return self.driver.run_query(self.connection, sql)

    def fetch_one(self):
        return {"id": 1, "name": "Alice"}

    def close(self):
        self.driver.close(self.connection)


class PostgreSQLAdapter(Database):
    def __init__(self):
        self.driver = PostgreSQLDriver()
        self.connection = None

    def connect(self, connection_string: str):
        self.connection = self.driver.connect_db(connection_string)

    def execute(self, sql: str):
        return self.driver.query(self.connection, sql)

    def fetch_one(self):
        return {"id": 1, "name": "Bob"}

    def close(self):
        self.driver.disconnect(self.connection)


class SQLiteAdapter(Database):
    def __init__(self):
        self.driver = SQLiteDriver()
        self.connection = None

    def connect(self, connection_string: str):
        filepath = connection_string.replace("sqlite://", "")
        self.connection = self.driver.open(filepath)

    def execute(self, sql: str):
        return self.driver.exec(self.connection, sql)

    def fetch_one(self):
        return {"id": 1, "name": "Charlie"}

    def close(self):
        self.driver.close_db(self.connection)


class DatabaseClient:
    def __init__(self, db: Database, connection_string: str):
        self.db = db
        self.db.connect(connection_string)

    def get_user(self, user_id: int):
        self.db.execute(f"SELECT * FROM users WHERE id = {user_id}")
        return self.db.fetch_one()

    def cleanup(self):
        self.db.close()


if __name__ == "__main__":
    databases = [
        ("MySQL", MySQLAdapter(), "mysql://localhost/mydb"),
        ("PostgreSQL", PostgreSQLAdapter(), "postgresql://localhost/mydb"),
        ("SQLite", SQLiteAdapter(), "sqlite:///mydb.db")
    ]

    for name, adapter, conn_str in databases:
        print(f"\n=== {name} ===")
        client = DatabaseClient(adapter, conn_str)
        user = client.get_user(1)
        print(f"Результат: {user}")
        client.cleanup()