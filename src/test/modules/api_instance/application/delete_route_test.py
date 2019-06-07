from modules.api_instance import AddRoute
from modules.api_instance import AddRouteCommand
from modules.api_instance import DeleteRoute
from modules.api_instance import DeleteRouteCommand
from modules.api_instance import RegisterApi
from modules.api_instance import RegisterApiCommand
from modules.api_instance.infrastructure import FakeRepository


def test_delete_route_from_api():
    repository = FakeRepository()
    register_api = RegisterApi(repository)
    register_api.execute(RegisterApiCommand('test', 8000))

    api = repository.apis[0]

    add_route = AddRoute(repository)
    add_route.execute(AddRouteCommand(api._id, 'users', 'get', {"test": "test"}))

    insert_one_route_to_api = 1
    assert len(api.routes) == insert_one_route_to_api

    delete_route = DeleteRoute(repository)
    delete_route.execute(DeleteRouteCommand(api._id, 'users', 'get'))

    without_routes = 0
    assert len(api.routes) == without_routes
