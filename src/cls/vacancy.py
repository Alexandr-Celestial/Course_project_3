from typing import Any, Self

import f


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = (
        "id_vacancy",
        "name",
        "address",
        "salary_from",
        "salary_to",
        "description",
        "company_id",
        "company_name",
    )

    def __init__(
        self,
        name: str,
        address: str,
        salary_from: int,
        salary_to: int,
        description: str,
        company_id: int,
        company_name: str,
        id_vacancy: int | str,
    ) -> None:
        """Инициализация экземпляра Vacancy"""
        self.name = Vacancy.__validate_name(name)
        self.address = Vacancy.__validate_address(address)
        self.salary_from = Vacancy.__validate_salary_from(salary_from)
        self.salary_to = Vacancy.__validate_salary_to(salary_to)
        self.description = Vacancy.__validate_description(description)
        self.company_id = Vacancy.__validate_company_id(company_id)
        self.id_vacancy = Vacancy.__validate_id_vacancy(id_vacancy)
        self.company_name = Vacancy.__validate_company_name(company_name)

    @classmethod
    def cast_to_object_list(cls, dirty_list_vacations: list[dict]) -> list[Self]:
        """Преобразует список словарей с данными вакансий в список объектов Vacancy"""
        clear_list_vacations = []
        for item in dirty_list_vacations:
            salary_from = f.ichain(item, "salary_range", "from") or 0
            salary_to = f.ichain(item, "salary_range", "to") or 0
            description = f.ichain(item, "snippet", "responsibility") or "нет описания"
            company_id = f.ichain(item, "employer", "id") or 0
            company_name = f.ichain(item, "employer", "name") or "нет названия"
            id_vacancy = f.ichain(item, "id") or 0
            apply_alternate_url = item["apply_alternate_url"]
            clear_list_vacations.append(
                cls(
                    item["name"],
                    apply_alternate_url,
                    salary_from,
                    salary_to,
                    description,
                    company_id,
                    company_name,
                    id_vacancy,
                )
            )

        return clear_list_vacations

    def __eq__(self, other: Any) -> Any:
        """Переопределённый метод __eq__"""
        return self.salary_to == other.salary_to

    def __lt__(self, other: Any) -> Any:
        """Переопределённый метод __lt__"""
        return self.salary_to < other.salary_to

    def __gt__(self, other: Any) -> Any:
        """Переопределённый метод __gt__"""
        return self.salary_to > other.salary_to

    def __le__(self, other: Any) -> Any:
        """Переопределённый метод __le__"""
        return self.salary_to <= other.salary_to

    def __ge__(self, other: Any) -> Any:
        """Переопределённый метод __ge__"""
        return self.salary_to >= other.salary_to

    def __repr__(self) -> str:
        """Переопределённый метод __repr__"""
        return f"{self.__class__.__name__}('{self.salary_from}-{self.salary_to}')"

    @staticmethod
    def __validate_name(name: str) -> Any:
        """Проводит валидацию названия вакансии"""
        if isinstance(name, str) and len(name) > 0:
            return name
        return NotImplemented

    @staticmethod
    def __validate_address(address: str) -> Any:
        """Проводит валидацию адреса вакансии"""
        if isinstance(address, str) and len(address) > 0:
            return address
        return NotImplemented

    @staticmethod
    def __validate_company_name(company_name: str) -> Any:
        """Проводит валидацию опыта вакансии"""
        if isinstance(company_name, str) and len(company_name) > 0:
            return company_name
        return NotImplemented

    @staticmethod
    def __validate_salary_from(salary_from: int) -> Any:
        """Проводит валидацию зарплаты от"""
        if isinstance(salary_from, int) and salary_from >= 0:
            return salary_from
        return 0

    @staticmethod
    def __validate_company_id(company_id: str | int) -> int:
        """Проводит валидацию company_id"""
        if isinstance(company_id, int):
            return company_id
        if isinstance(company_id, str):
            return int(company_id)
        raise ValueError("id компании передан неверно")

    @staticmethod
    def __validate_salary_to(salary_to: int) -> Any:
        """Проводит валидацию зарплаты до"""
        if isinstance(salary_to, int) and salary_to >= 0:
            return salary_to
        return 0

    @staticmethod
    def __validate_description(description: str) -> Any:
        """Проводит валидацию описания вакансии"""
        if isinstance(description, str) and len(description) > 0:
            return description
        return "Нет результатов"

    @staticmethod
    def __validate_id_vacancy(id_vacancy: str | int) -> int:
        """Проводит валидацию id вакансии"""
        if isinstance(id_vacancy, int):
            return id_vacancy
        if isinstance(id_vacancy, str):
            return int(id_vacancy)
        raise ValueError("id компании передан неверно")

    def __str__(self) -> str:
        """Переопределение метода __str__"""
        return (
            f"{self.__class__.__name__}('{self.name} {self.address} "
            f"{self.salary_from}-{self.salary_to} {self.description}')"
        )

    def get_organization(self) -> tuple:
        """Возвращает кортеж с id и названием компании"""
        return self.company_id, self.company_name

    def get_vacancy(self) -> tuple:
        """Возвращает кортеж с основными данными вакансий для вставки в БД"""
        return (
            self.id_vacancy,
            self.name,
            self.address,
            self.salary_from,
            self.salary_to,
            self.description,
            self.company_id,
        )
