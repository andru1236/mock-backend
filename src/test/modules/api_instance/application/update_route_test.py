from modules.api_instance.application.update_route import UpdateRoute, UpdateRouteCommand
from modules.api_instance.application.add_route import AddRoute, AddRouteCommand
from modules.api_instance.application.register_api import RegisterApi, RegisterApiCommand
from modules.api_instance.infrastructure import FakeRepository


def test_update_route():
    repository = FakeRepository()
    register_api = RegisterApi(repository)
    add_route = AddRoute(repository)
    use_case = UpdateRoute(repository)

    register_api.execute(RegisterApiCommand('test', 8000))

    api = repository.apis[0]
    api_id = repository.apis[0]._id

    response_test = {"test": "test"}
    add_route.execute(AddRouteCommand(api_id, '/users', 'get', response_test))

    assert api.get_list_paths()[0].resources[0].response == response_test

    updated_response = {"update": "update"}

    use_case.execute(UpdateRouteCommand(api_id, '/users', 'get', updated_response))

    assert api.get_list_paths()[0].resources[0].response == updated_response
