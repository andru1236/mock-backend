from modules.api_instance.application.delete_route import DeleteRoute, DeleteRouteCommand
from modules.api_instance.application.add_route import AddRoute, AddRouteCommand
from modules.api_instance.application.register_api import RegisterApi, RegisterApiCommand

def test_delete_route_from_api(repository):
    register_api = RegisterApi(repository)
    register_api.execute(RegisterApiCommand('test', 8000))

    api = repository.apis[0]

    add_route = AddRoute(repository)
    add_route.execute(AddRouteCommand(api._id, '/users', 'get', {"test": "test"}))

    insert_one_route_to_api = 1
    assert len(api.get_list_paths()) == insert_one_route_to_api

    delete_route = DeleteRoute(repository)
    delete_route.execute(DeleteRouteCommand(api._id, '/users', 'get'))

    without_routes = 0
    assert len(api.get_list_paths()) == without_routes
