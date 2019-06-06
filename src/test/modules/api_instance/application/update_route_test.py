from modules.api_instance import AddRoute
from modules.api_instance import AddRouteCommand
from modules.api_instance import RegisterApi
from modules.api_instance import RegisterApiCommand
from modules.api_instance import UpdateRoute
from modules.api_instance import UpdateRouteCommand
from modules.api_instance.infrastructure import FakeRepository


def test_update_route():
    repository = FakeRepository()

    register_api = RegisterApi(repository)
    add_route = AddRoute(repository)
    use_case = UpdateRoute(repository)

    register_api.execute(RegisterApiCommand(8000))

    api = repository.apis[0]
    api_id = repository.apis[0]._id

    response_test = '{"test": "test"}'
    add_route.execute(AddRouteCommand(api_id, 'users', 'get', response_test))

    assert api.routes[0].response.value == response_test

    updated_response = '{"update": "update"}'

    use_case.execute(UpdateRouteCommand(api_id, 'users', 'get', updated_response))

    assert api.routes[0].response.value == updated_response
