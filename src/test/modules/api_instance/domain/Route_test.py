import pytest

from modules.api_instance.domain import Route
from modules.shared.domain.errors import DomainBadRequestError


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
