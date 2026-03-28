import psycopg2
from config import DB_CONFIG


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        if not self.connection:
            try:
                self.connection = psycopg2.connect(**DB_CONFIG)
            except Exception as e:
                print(f"Ошибка: {e}")
        return self.connection

    def get_cursor(self):
        return self.connect().cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()