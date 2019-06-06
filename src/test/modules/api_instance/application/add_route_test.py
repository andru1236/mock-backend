from modules.api_instance import AddRoute
from modules.api_instance import AddRouteCommand
from modules.api_instance import RegisterApi
from modules.api_instance import RegisterApiCommand
from modules.api_instance.infrastructure import FakeRepository


def test_add_new_route_to_api_success():
    repository = FakeRepository()
    register_api = RegisterApi(repository)
    register_api.execute(RegisterApiCommand(8000))

    api_id = repository.apis[0]._id

    without_routes = 0
    assert len(repository.apis[0].routes) == without_routes

    use_case = AddRoute(repository)
    use_case.execute(AddRouteCommand(api_id, 'users', 'get', '{"test": "test"}'))
    insert_one_route = 1

    assert len(repository.apis[0].routes) == insert_one_route
