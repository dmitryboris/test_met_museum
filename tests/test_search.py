from http import HTTPStatus
from models import SearchResult, Object

import requests


class TestSearch:

    def test_status(self, base_url):
        params = {
            'q': 'sunflower'
        }
        response = requests.get(f'{base_url}/search', params=params)

        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что страница {base_url}/search доступна'
        )

    def test_search_response_matches_model(self, base_url):
        params = {
            'q': 'sunflower'
        }
        response = requests.get(f'{base_url}/search', params=params)
        result = SearchResult.model_validate(response.json())
        assert result.total == len(result.objectIDs), (
            'Проверьте, что возвращаемые данные соответствуют модели SearchResult'
        )

    def test_search(self, base_url):
        params = {
            'q': 'attendant bodhisattva',
            'title': 'true'
        }
        response = requests.get(f'{base_url}/search', params=params)
        assert response.status_code == HTTPStatus.OK

        result = SearchResult.model_validate(response.json())
        assert result.objectIDs, 'Не найдено ни одного объекта по запросу'

        object_id = result.objectIDs[0]
        object_response = requests.get(f'{base_url}/objects/{object_id}')
        assert object_response.status_code == HTTPStatus.OK

        obj = Object.model_validate(object_response.json())
        assert obj.title and params['q'].lower() in obj.title.lower(), (
            f"Значение параметра q ('{params['q']}') не найдено в названии объекта: {obj.title}"
        )

    def test_search_result_count_reasonable(self, base_url):
        params = {
            'q': 'a'
        }
        response = requests.get(f'{base_url}/search', params=params)
        assert response.status_code == HTTPStatus.OK

        result = SearchResult.model_validate(response.json())

        assert result.total <= 10000, (
            f'Нет ограничения на количество возвращаемых результатов. '
            f'Кол-во объектов: {result.total}'
        )
