from backend.api_instance.application.add_route import Route
from backend.api_instance.application.add_route import Response
from backend.api_instance import AddRoute
from backend.api_instance import AddRouteCommand
from backend.api_instance import RegisterApi
from backend.api_instance import RegisterApiCommand

from backend.api_instance import AddParams
from backend.api_instance import AddParamsCommand
from backend.api_instance import UpdateParams
from backend.api_instance import UpdateParamsCommand

from backend.api_instance.infrastructure import FakeRepository


def test_update_params_from_path():

    # Initialize
    repository = FakeRepository()
    register_api = RegisterApi(repository)
    register_api.execute(RegisterApiCommand('test', 8000))

    api = repository.apis[0]

    add_route = AddRoute(repository)
    add_route.execute(AddRouteCommand(api._id, 'users', 'get', {"test": "test"}))

    # Test
    path = api.paths.get_path_with_this(Route('users', 'get', Response({"s":"s"})))

    add_params = AddParams(repository)
    add_params.execute(AddParamsCommand(api._id, path._id, 'page=2', 'GET', {}))

    resource = path.get_resource_by_method('GET')
    assert len(resource.params) == 1

    data = {'new': 'Data'}
    update_params = UpdateParams(repository)
    update_params.execute(UpdateParamsCommand(api._id, path._id, 'page=2', 'GET', data))

    assert data == resource.params[0].response
