from datetime import datetime, timedelta
from http import HTTPStatus
from models import Object, Objects, Departments

import requests


class TestObjects:

    def test_status(self, base_url):
        response = requests.get(f'{base_url}/objects/1')
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что страница {base_url}/objects/1 доступна'
        )

    def test_post_object(self, base_url):
        response = requests.post(f'{base_url}/objects/1')
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
            'Проверьте, что POST запросы неразрешены'
        )

    def test_nonexistent_object_returns_404(self, base_url):
        response = requests.get(f"{base_url}/objects/999999999")
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            'Проверьте, что запрос к несуществующему объекту возвращает код 404'
        )

    def test_invalid_object_id_format(self, base_url):
        response = requests.get(f"{base_url}/objects/invalid-id")
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что запрос к несуществующему объекту возвращает код 400'
        )

    def test_object_response_matches_model(self, base_url):
        object_id = 192
        response = requests.get(f'{base_url}/objects/{object_id}')
        assert response.status_code == HTTPStatus.OK
        obj = Object.model_validate(response.json())
        assert object_id == obj.objectID, (
            'Проверьте, что возвращаемые данные соответствуют модели Object'
        )

    def test_objects_response_matches_model(self, base_url):
        response = requests.get(f'{base_url}/objects')
        objects = Objects.model_validate(response.json())
        assert objects.total == len(objects.objectIDs), (
            'Проверьте, что возвращаемые данные соответствуют модели Objects'
        )

    def test_objects_with_datetime_query(self, base_url):
        date = datetime.now() - timedelta(days=30 * 365)
        date_str = date.strftime("%Y-%m-%d")
        params = {
            "metadataDate": date_str,
        }
        response = requests.get(f"{base_url}/objects", params=params)

        assert response.status_code == HTTPStatus.OK
        objs = Objects.model_validate(response.json())
        object_id = objs.objectIDs[0]

        object_response = requests.get(f"{base_url}/objects/{object_id}")
        obj = Object.model_validate(object_response.json())
        assert obj.metadataDate.replace(tzinfo=None) >= date, (
            'Проверьте, что параметр metadataDate обрабатывается корректно'
        )

    def test_objects_with_department_query(self, base_url):
        department_id = 3
        params = {
            "departmentIds": str(department_id)
        }
        response = requests.get(f"{base_url}/objects", params=params)

        assert response.status_code == HTTPStatus.OK
        objs = Objects.model_validate(response.json())
        object_id = objs.objectIDs[0]

        object_response = requests.get(f"{base_url}/objects/{object_id}")
        obj = Object.model_validate(object_response.json())

        department_response = requests.get(f"{base_url}/departments")
        departments = Departments.model_validate(department_response.json())
        for department in departments.departments:
            if department.departmentId == department_id:
                assert department.displayName == obj.department, (
                    'Проверьте, что параметр departmentIds обрабатывается корректно'
                )
