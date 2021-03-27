import pytest

from modules.api_instance.domain import ApiInstance
from modules.api_instance.domain import Paths
from modules.api_instance.domain import Response
from modules.api_instance.domain import Route
from modules.shared.domain.errors import DomainBadRequestError

test_name = "Api test"


@pytest.mark.usefixtures("get_port", "get_users_routes_crud")
def test_create_api_instance_success(get_port, get_users_routes_crud):
    paths = Paths()
    for route in get_users_routes_crud:
        paths.add_route(route)

    api = ApiInstance(test_name, get_port, paths)
    assert api.name == test_name
    assert api.port.value == get_port.value

    for route in get_users_routes_crud:
        assert route.path == api.get_path(route).path
        assert (
            route.response.value
            == api.get_path(route).get_resource_by_method(route.method).response
        )


@pytest.mark.usefixtures("get_port", "get_users_routes_crud")
def test_add_route_to_api(get_port, get_users_routes_crud):
    paths = Paths()
    for route in get_users_routes_crud:
        paths.add_route(route)

    api = ApiInstance(test_name, get_port, paths)
    assert len(api.get_list_paths()) == 1

    # New path api
    new_route = Route("apis", "delete", Response({"status": 200}))
    api.add_route(new_route)
    assert len(api.get_list_paths()) == 2

    new_route = Route("apis", "post", Response({"status": 200}))
    api.add_route(new_route)
    assert len(api.get_list_paths()) == 2


@pytest.mark.usefixtures("get_port", "get_users_routes_crud")
def test_replace_route(get_port, get_users_routes_crud):
    paths = Paths()
    for route in get_users_routes_crud:
        paths.add_route(route)
    api = ApiInstance(test_name, get_port, paths)
    new_route = Route("users", "delete", Response({"status": 200}))

    api.replace_route(new_route)

    api_path = api.get_path(new_route)
    assert (
        api_path.get_resource_by_method(route.method).response
        == new_route.response.value
    )


@pytest.mark.usefixtures("get_port", "get_users_routes_crud")
def test_replace_route_that_not_exist(get_port, get_users_routes_crud):
    paths = Paths()
    for route in get_users_routes_crud:
        paths.add_route(route)

    api = ApiInstance(test_name, get_port, paths)
    new_route = Route("user", "delete", Response({"status": 200}))
    with pytest.raises(DomainBadRequestError):
        api.replace_route(new_route)


@pytest.mark.usefixtures("get_port", "get_users_routes_crud")
def test_remove_route_from_api_success(get_port, get_users_routes_crud):
    paths = Paths()
    for route in get_users_routes_crud:
        paths.add_route(route)

    api = ApiInstance(test_name, get_port, paths)
    this_route_will_be_removed = Route("users", "delete", Response({"status": 200}))

    assert len(api.get_path(this_route_will_be_removed).resources) == 4
    api.remove_route(this_route_will_be_removed)
    assert len(api.get_path(this_route_will_be_removed).resources) == 3


@pytest.mark.usefixtures("get_port", "get_users_routes_crud")
def test_remove_route_that_not_exist_in_api(get_port, get_users_routes_crud):
    paths = Paths()
    for route in get_users_routes_crud:
        paths.add_route(route)
    api = ApiInstance(test_name, get_port, paths)
    this_route_not_exist = Route("test", "delete", Response({"status": 200}))
    with pytest.raises(DomainBadRequestError):
        api.remove_route(this_route_not_exist)
