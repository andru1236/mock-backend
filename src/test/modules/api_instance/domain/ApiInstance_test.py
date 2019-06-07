import pytest

from modules.api_instance.domain.api import ApiInstance
from modules.api_instance.domain.api import Response
from modules.api_instance.domain.api import Route
from modules.shared.domain.errors import DomainBadRequestError

test_name = 'Api test'


@pytest.mark.usefixtures('get_port', 'get_users_routes_crud')
def test_create_api_instance_success(get_port, get_users_routes_crud):
    api = ApiInstance(test_name, get_port, get_users_routes_crud)
    assert api.name == test_name
    assert api.port.value == get_port.value
    for index, route in enumerate(get_users_routes_crud):
        assert api.routes[index].method == route.method
        assert api.routes[index].response.value == route.response.value
        assert api.routes[index].path == route.path


@pytest.mark.usefixtures('get_port', 'get_users_routes_crud')
def test_add_route_to_api(get_port, get_users_routes_crud):
    api = ApiInstance(test_name, get_port, get_users_routes_crud)
    count_routes = len(api.routes)

    new_route = Route('apis', 'delete', Response({"status": 200}))
    api.add_route(new_route)

    assert count_routes != len(api.routes)
    assert count_routes + 1 == len(api.routes)


@pytest.mark.usefixtures('get_port', 'get_users_routes_crud')
def test_replace_route(get_port, get_users_routes_crud):
    api = ApiInstance(test_name, get_port, get_users_routes_crud)
    new_route = Route('users', 'delete', Response({"status": 200}))
    for route in api.routes:
        if route.path == new_route.path and route.method == new_route.method:
            assert route.response.value != new_route.response

    api.replace_route(new_route)
    for route in api.routes:
        if route.path == new_route.path and route.method == new_route.method:
            assert route.response == new_route.response


@pytest.mark.usefixtures('get_port', 'get_users_routes_crud')
def test_replace_route_that_not_exist(get_port, get_users_routes_crud):
    api = ApiInstance(test_name, get_port, get_users_routes_crud)
    new_route = Route('user', 'delete', Response({"status": 200}))
    with pytest.raises(DomainBadRequestError):
        api.replace_route(new_route)


@pytest.mark.usefixtures('get_port', 'get_users_routes_crud')
def test_remove_route_from_api_success(get_port, get_users_routes_crud):
    api = ApiInstance(test_name, get_port, get_users_routes_crud)
    count_routes = len(api.routes)
    this_route_will_be_removed = Route('users', 'delete', Response({"status": 200}))
    api.remove_route(this_route_will_be_removed)
    assert len(api.routes) == count_routes - 1


@pytest.mark.usefixtures('get_port', 'get_users_routes_crud')
def test_remove_route_that_not_exist_in_api(get_port, get_users_routes_crud):
    api = ApiInstance(test_name, get_port, get_users_routes_crud)
    this_route_not_exist = Route('test', 'delete', Response({"status": 200}))
    with pytest.raises(DomainBadRequestError):
        api.remove_route(this_route_not_exist)
