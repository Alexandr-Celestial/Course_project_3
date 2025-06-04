from pprint import pprint

from src.cls.db_manager import DBManager
from src.cls.head_hunter import HH
from src.cls.vacancy import Vacancy


head_h = HH()


if __name__ == "__main__":
    result_head_h = head_h.get_vacancies()
    result_vac = Vacancy.cast_to_object_list(result_head_h)

    with DBManager() as db:
        db.add_vacancy(result_vac)
        pprint(db.get_companies_and_vacancies_count())
        pprint(db.get_avg_salary())
        pprint(db.get_vacancies_with_higher_salary())
        pprint(db.get_vacancies_with_keyword("python"))
