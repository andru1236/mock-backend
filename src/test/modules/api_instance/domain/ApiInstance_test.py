import pytest

from modules.api_instance.domain import ApiInstance


@pytest.mark.usefixtures('get_port', 'get_routes_crud')
def test_create_api_instance_success(get_port, get_routes_crud):
    api = ApiInstance(get_port, get_routes_crud)
    assert api.port.value == get_port.value
    for index, route in enumerate(get_routes_crud):
        assert api.routes[index].method == route.method
        assert api.routes[index].response.value == route.response.value
        assert api.routes[index].path == route.path
