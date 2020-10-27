from modules.api_instance.application.add_route import AddRoute, AddRouteCommand
from modules.api_instance.application.register_api import RegisterApi, RegisterApiCommand


def test_add_new_route_to_api_success(repository):
    register_api = RegisterApi(repository)
    register_api.execute(RegisterApiCommand('test_name', 8000))
    print(repository.apis[0].get_list_paths())
    api_id = repository.apis[0]._id

    without_routes = 0
    assert len(repository.apis[0].get_list_paths()) == without_routes

    use_case = AddRoute(repository)
    use_case.execute(AddRouteCommand(api_id, '/users', 'get', {"test": "test"}))
    insert_one_route = 1

    assert len(repository.apis[0].get_list_paths()) == insert_one_route
