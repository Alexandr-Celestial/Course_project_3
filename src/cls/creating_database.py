import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection, cursor as _cursor
from typing import Optional

from src.cls.vacancy import Vacancy

load_dotenv()
DATA_BASE: str = os.getenv("DATA_BASE", "")
PASSWORD: str = os.getenv("PASSWORD", "")
DB_USER: str = os.getenv("DB_USER")
DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: str = os.getenv("DB_PORT")


class DataBase:
    """Класс для работы с базой данных PostgreSQL"""

    def __init__(self) -> None:
        """Инициализация объекта DataBase"""
        self._conn: Optional[_connection] = None
        self._cur: Optional[_cursor] = None

    def connect_db(self) -> None:
        """Устанавливает соединение с базой данных"""
        try:
            self._conn = psycopg2.connect(
                host=DB_HOST, database=DATA_BASE, user=DB_USER, password=PASSWORD, port=DB_PORT
            )
            self._cur = self._conn.cursor()
            self._conn.autocommit = True
        except Exception as e:
            raise e

    def crated_table(self) -> None:
        """Создаёт таблицы organizations и vacancy"""
        if self._cur is None:
            raise RuntimeError("Курсор не инициализирован. Вызовите connect_db() перед этим.")
        self._cur.execute(
            """
        CREATE TABLE IF NOT EXISTS organizations (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR NOT NULL)
        """
        )

        self._cur.execute(
            """CREATE TABLE IF NOT EXISTS vacancy (
            id SERIAL PRIMARY KEY,
            company_id INT REFERENCES organizations(company_id),
            name VARCHAR NOT NULL,
            address VARCHAR NOT NULL,
            salary_from INT NOT NULL,
            salary_to INT NOT NULL,
            description VARCHAR)
        """
        )
        print("123")
        self._conn.commit()

    def add_vacancy(self, list_vacancy: list[Vacancy]) -> None:
        """Добавляет список вакансий в таблицы organizations и vacancy"""
        if self._cur is None:
            raise RuntimeError("Курсор не инициализирован. Вызовите connect_db() перед этим.")
        for vac in list_vacancy:
            self._cur.execute(
                """INSERT
                       INTO
                       organizations(company_id, company_name)
                       VALUES(%s, %s)
                       ON
                       CONFLICT(company_id)
                       DO
                       NOTHING""",
                vac.get_organization(),
            )
            self._cur.execute(
                """INSERT
                       INTO
                       vacancy(id, name, address, salary_from, salary_to, description, company_id)
                       VALUES(%s, %s, %s, %s, %s, %s, %s)
                       ON
                       CONFLICT(id)
                       DO
                       NOTHING""",
                vac.get_vacancy(),
            )
            # self.id_vacancy, self.name, self.address, self.salary_from,
            # self.salary_to, self.description, self.company_id

    @staticmethod
    def create_database() -> None:
        """Создаёт базу данных"""
        conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=PASSWORD, host=DB_HOST, port=DB_PORT)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"""SELECT FROM
                pg_database
                WHERE
                datname = '{DATA_BASE}';
                """)
            exists = cur.fetchone()
            if not exists:
                cur.execute(f"CREATE DATABASE {DATA_BASE}")
                print(f"База данных {DATA_BASE} создана")
        except psycopg2.errors.DuplicateDatabase:
            print(f"База данных {DATA_BASE} уже существует")
        cur.close()
        conn.close()

    def close(self) -> None:
        """Закрывает курсор и соединение с базой данных"""
        if self._cur is not None:
            self._cur.close()
        if self._conn is not None:
            self._conn.close()
