import pytest

from modules.api_instance.domain import Response
from modules.api_instance.domain import Route
from modules.shared.domain.errors import DomainBadRequestError


@pytest.fixture
def get_routes_crud():
    path = 'users'
    methods = ['get', 'post', 'put', 'delete']
    generic_response = Response('{"json_test": "value_json"}')
    routes = [Route(path, method, generic_response) for method in methods]
    return routes


@pytest.mark.usefixtures('get_response')
def test_create_route_success(get_response):
    path = 'users'
    method = 'get'
    response = get_response
    route = Route(path, method, response)
    assert route.path == path
    assert route.method == method.upper()
    assert route.response.value == get_response.value


@pytest.mark.usefixtures('get_response')
def test_create_route_with_invalid_method(get_response):
    path = 'users'
    response = get_response

    bad_methods = ['create', 'update', 'detele']
    with pytest.raises(DomainBadRequestError):
        for bad_method in bad_methods:
            Route(path, bad_method, response)


@pytest.mark.usefixtures('get_response')
def test_create_route_with_inteker_like_path(get_response):
    path = 10505050
    method = 'get'
    response = get_response
    with pytest.raises(DomainBadRequestError):
        Route(path, method, response)
