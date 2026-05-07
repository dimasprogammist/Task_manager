
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

# Загружаем переменные из .env файла
load_dotenv("sql/.env")
init_script_path = os.getenv('DB_INIT_SCRIPT_PATH')

class Database:
    def __init__(self, use_pool=True, min_conn=1, max_conn=10):
        """Параметры подключения к БД"""
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_USER_PASSWORD')
        }

        if use_pool:
            # Пул соединений для многопоточности
            self.pool = pool.ThreadedConnectionPool(
                min_conn, max_conn, **self.db_config
            )
        else:
            self.pool = None

    def init_database(self):
        try:
            with open(init_script_path, "r", encoding="utf-8") as file:
                sql = file.read()
            queries = [q.strip() for q in sql.split(";") if q.strip()]

            for query in queries:
                self.execute_one(query)
                print(f"Выполнен запрос {query[:50]}")
        except Exception as e:
            print(f"Ошибка инициализации БД: {e}")

    def _get_connection(self):
        """Получить соединение (из пула или новое)"""
        if self.pool:
            return self.pool.getconn()
        return psycopg2.connect(**self.db_config)

    def _return_connection(self, conn):
        """Вернуть соединение в пул"""
        if self.pool:
            self.pool.putconn(conn)
        else:
            conn.close()

    def select(self, query, params=None):
        """Получить несколько записей"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    return cursor.fetchall()
        except Exception as e:
            self._handle_error(e, query, params)
            return []


    def select_one(self, query, params=None):
        """Получить одну запись"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    return cursor.fetchone()
        except Exception as e:
            self._handle_error(e, query, params)
            return None

    def execute_one(self, query, params=None):
        """Вставка одной записи"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    return cursor.rowcount
        except Exception as e:
            self._handle_error(e, query, params)
            return 0

    def execute_many(self, query, params_list):
        """Вставка множества записей"""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.executemany(query, params_list)
                    return cursor.rowcount
        except Exception as e:
            self._handle_error(e, query, params_list)
            return 0

    def _handle_error(self, error, query=None, params=None):
        """Обработка ошибок"""
        if isinstance(error, psycopg2.OperationalError):
            print(f' Ошибка подключения к БД!')
            print(f' Сервер: {self.db_config["host"]}:{self.db_config["port"]}')
            print(f' БД: {self.db_config["database"]}')
            print(f' Текст ошибки: {error}')

        elif isinstance(error, psycopg2.ProgrammingError):
            print(f' Ошибка в SQL запросе!')
            if query:
                print(f' Запрос: {query}')
            if params:
                print(f' Параметры: {params}')
            print(f' Текст ошибки: {error}')

        elif isinstance(error, psycopg2.DataError):
            print(f' Ошибка данных!')
            print(f' Неправильный тип или формат данных')
            print(f' Текст ошибки: {error}')

        elif isinstance(error, psycopg2.IntegrityError):
            print(f' Ошибка целостности данных!')
            print(f' Возможно: дубликат уникального значения')
            print(f' Текст ошибки: {error}')

        elif isinstance(error, psycopg2.DatabaseError):
            print(f' Ошибка базы данных: {error}')

        else:
            print(f' Неизвестная ошибка: {error}')