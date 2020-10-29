from modules.api_instance.application.add_route import Route
from modules.api_instance.application.add_route import Response
from modules.api_instance import AddRoute
from modules.api_instance import AddRouteCommand
from modules.api_instance import DeleteRoute
from modules.api_instance import DeleteRouteCommand
from modules.api_instance import RegisterApi
from modules.api_instance import RegisterApiCommand

from modules.api_instance import AddParams
from modules.api_instance import AddParamsCommand
from modules.api_instance import UpdateParams
from modules.api_instance import UpdateParamsCommand

from modules.api_instance.infrastructure import FakeRepository


def test_delete_params_from_path():

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