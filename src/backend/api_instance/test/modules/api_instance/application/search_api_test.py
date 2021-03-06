from backend.api_instance import RegisterApi
from backend.api_instance import RegisterApiCommand
from backend.api_instance.application.search_api import SearchApi
from backend.api_instance.application.search_api import SearchApiQuery
from backend.api_instance.infrastructure import FakeRepository


def test_search_api():
    repository = FakeRepository()
    register_api = RegisterApi(repository)

    register_api.execute(RegisterApiCommand('test', 8000))

    api = repository.apis[0]

    search_api = SearchApi(repository)
    response_query = search_api.execute(SearchApiQuery(api._id))

    assert response_query['_id'] == api._id
