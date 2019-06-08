import pytest

from modules.api_instance.domain.api import Path
from modules.api_instance.domain.api import Resource
from modules.api_instance.domain.api import Response
from modules.api_instance.domain.api import Route
from modules.shared.domain.errors import DomainBadRequestError

route_with_get = Route('/users', 'get', Response({'test': 'test'}))
route_with_post = Route('/users', 'post', Response({'test_post': 'test_post'}))
route_with_put = Route('/users', 'put', Response({'test_put': 'test_put'}))
route_with_delete = Route('/users', 'delete', Response({'test_delete': 'test_delete'}))

resource_get = Resource(route_with_get.method, route_with_get.response)
resource_post = Resource(route_with_post.method, route_with_post.response)
resource_put = Resource(route_with_put.method, route_with_put.response)
resource_delete = Resource(route_with_delete.method, route_with_delete.response)


def test_create_path_success():
    path = Path(route_with_get.path)
    without_resources = 0

    assert path.path == route_with_get.path
    assert len(path.resources) == without_resources


def test_add_resources_to_path():
    path = Path(route_with_get.path)
    without_resources = 0

    assert path.path == route_with_get.path
    assert len(path.resources) == without_resources

    path.add_resource(resource_get)

    one_resource = 1
    assert len(path.resources) == one_resource

    for resource in path.resources:
        assert resource.method == resource_get.method
        assert resource.response == resource_get.response


def test_update_one_resource():
    path = Path(route_with_get.path)
    path.add_resource(resource_get)

    new_response = Response({'updated_test': 'updated_test'})
    new_resource_get = Resource(route_with_get.method, new_response)

    path.update_resource(new_resource_get)

    for resource in path.resources:
        if resource.method == new_resource_get.method:
            assert resource.response == new_resource_get.response


def test_remove_resource():
    path = Path(route_with_get.path)

    path.add_resource(resource_get)
    path.add_resource(resource_post)
    path.add_resource(resource_put)

    assert len(path.resources) == 3

    resource_will_be_removed = Resource(route_with_get.method, route_with_get.response)
    path.remove_resource(resource_will_be_removed)

    assert len(path.resources) == 2


def test_inserting_routes_twice_in_same_path_fail():
    path = Path(route_with_get.path)
    path.add_resource(resource_get)
    with pytest.raises(DomainBadRequestError):
        path.add_resource(resource_get)

