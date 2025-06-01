import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection, cursor as _cursor
from typing import Optional

from src.cls.vacancy import Vacancy

load_dotenv()
DATA_BASE: str | None = os.getenv("database")
PASSWORD: str | None = os.getenv("password")


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
                host="localhost", database=DATA_BASE, user="postgres", password=PASSWORD, port="5432"
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

    def close(self) -> None:
        """Закрывает курсор и соединение с базой данных"""
        if self._cur is not None:
            self._cur.close()
        if self._conn is not None:
            self._conn.close()
