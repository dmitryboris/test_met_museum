from http import HTTPStatus
from models import Departments, Department

import requests


class TestDepartments:

    def test_status(self, base_url):
        response = requests.get(f'{base_url}/departments')
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что страница {base_url}/departments доступна'
        )

    def test_departments(self, base_url):
        response = requests.get(f'{base_url}/departments')
        departments = Departments.model_validate(response.json())
        assert isinstance(departments.departments[0], Department), (
            'Проверьте, что модель Department соответствует API'
        )
