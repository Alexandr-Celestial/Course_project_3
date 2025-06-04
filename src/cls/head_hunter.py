from abc import ABC, abstractmethod

import requests

EMPLOYER_ID = [
    11669695,
    2066667,
    1911403,
    4685961,
    197566,
    2300703,
    1189354,
    45124,
    9498120,
    2393,
    4437201,
    5125017,
    710,
    167893
]


class HHBase(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str) -> list: ...

    """Абстрактный метод для получения списка вакансий по ключевому слову"""

    @abstractmethod
    def _connect_to_api(self) -> None: ...

    """Абстрактный метод для установки соединения с API"""

class HH(HHBase):
    """
    Класс для работы с API HeadHunter
    """

    BASE_URL = "https://api.hh.ru/"

    def __init__(self) -> None:
        """Инициализация объекта HH"""
        self.__vacancies: list[dict] = []
        self.__session = requests.Session()

    def get_vacancies(self) -> list:
        """Метод для получения списка вакансий по ключевому слову"""

        self._connect_to_api()
        for emp_id in EMPLOYER_ID:
            params: dict = {"text": '', "per_page": 100, "employer_id": emp_id}
            response = self.__session.get(f"{self.BASE_URL}/vacancies", params=params)
            if response.status_code == 200:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
        return self.__vacancies

    def _connect_to_api(self) -> None:
        """Метод соединения с API HeadHunter"""
        headers = {"User-Agent": "HH-User-Agent"}
        self.__session.get(self.BASE_URL, headers=headers)
