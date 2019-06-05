import pytest

from modules.api_instance.domain import ApiInstance
from modules.api_instance.domain import Response
from modules.api_instance.domain import Route


@pytest.mark.usefixtures('get_port', 'get_routes_crud')
def test_create_api_instance_success(get_port, get_routes_crud):
    api = ApiInstance(get_port, get_routes_crud)
    assert api.port.value == get_port.value
    for index, route in enumerate(get_routes_crud):
        assert api.routes[index].method == route.method
        assert api.routes[index].response.value == route.response.value
        assert api.routes[index].path == route.path


@pytest.mark.usefixtures('get_port', 'get_routes_crud')
def test_add_route_to_api(get_port, get_routes_crud):
    api = ApiInstance(get_port, get_routes_crud)
    count_routes = len(api.routes)

    new_route = Route('apis', 'delete', Response('{"status": 200}'))
    api.add_route(new_route)

    assert count_routes != len(api.routes)
    assert count_routes + 1 == len(api.routes)


