from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple, cast
from psycopg2.extensions import cursor as _cursor

from src.cls.creating_database import DataBase


class DBBase(ABC):
    """Абстрактный базовый класс для работы с базой данных вакансий"""

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        pass

    @abstractmethod
    def get_all_vacancies(self) -> list:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    @abstractmethod
    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        pass


class DBManager(DataBase):
    def __init__(self) -> None:
        super().__init__()

    def __enter__(self) -> "DBManager":
        """Контекстный менеджер: подключение к базе данных и создание таблиц"""
        self.create_database()
        self.connect_db()
        self.crated_table()
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """Контекстный менеджер: закрытие соединения с базой данных"""
        self.close()

    def _check_cursor(self) -> _cursor:
        if self._cur is None:
            raise RuntimeError("Курсор не инициализирован. Вызовите connect_db() перед использованием.")
        return self._cur

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        cur = self._check_cursor()
        cur.execute(
            """
            SELECT company_name, COUNT(*) FROM public.organizations
            INNER JOIN public.vacancy USING(company_id)
            GROUP BY public.organizations.company_name
            """
        )
        result = cur.fetchall()
        return cast(List[Tuple[str, int]], result)

    def get_all_vacancies(self) -> List[Tuple[Any, ...]]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        cur = self._check_cursor()
        cur.execute(
            """
            SELECT company_name, name, salary_from || '-' || salary_to as salary, address
            FROM public.organizations
            INNER JOIN public.vacancy USING(company_id)
            """
        )
        result = cur.fetchall()
        return cast(List[Tuple[Any, ...]], result)

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        cur = self._check_cursor()
        cur.execute(
            """
            SELECT (AVG(salary_from) + AVG(salary_to))/2 as salary_avg FROM public.vacancy
            """
        )
        result: Optional[Tuple[Optional[float]]] = cur.fetchone()
        if result is None or result[0] is None:
            return 0.0
        return float(result[0])

    def get_vacancies_with_higher_salary(self) -> List[Tuple[Any, ...]]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        cur = self._check_cursor()
        cur.execute("SELECT * FROM public.vacancy WHERE salary_to > %s", (avg_salary,))
        result = cur.fetchall()
        return cast(List[Tuple[Any, ...]], result)

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[Any, ...]]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        cur = self._check_cursor()
        cur.execute("SELECT * FROM public.vacancy WHERE name ILIKE %s", (f"%{keyword}%",))
        result = cur.fetchall()
        return cast(List[Tuple[Any, ...]], result)
