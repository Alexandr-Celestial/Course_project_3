from abc import ABC, abstractmethod

import requests


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

    BASE_URL = "https://api.hh.ru"

    def __init__(self) -> None:
        """Инициализация объекта HH"""
        self.__vacancies: list[dict] = []
        self.__session = requests.Session()

    def get_vacancies(self, keyword: str) -> list:
        """Метод для получения списка вакансий по ключевому слову"""
        self._connect_to_api()
        params: dict = {"text": keyword, "page": 0, "per_page": 100}
        while params.get("page") != 2:
            response = self.__session.get(f"{self.BASE_URL}/vacancies", params=params)
            if response.status_code == 200:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                params["page"] += 1
        return self.__vacancies

    def _connect_to_api(self) -> None:
        """Метод соединения с API HeadHunter"""
        headers = {"User-Agent": "HH-User-Agent"}
        self.__session.get(self.BASE_URL, headers=headers)
