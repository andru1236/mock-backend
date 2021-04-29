import pytest

from backend.api_instance.domain import Path
from backend.api_instance.domain import Resource
from backend.api_instance.domain import Response
from backend.api_instance.domain import Route
from backend.shared.domain.errors import DomainBadRequestError

route_with_get = lambda: Route("/users", "get", Response({"test": "test"}))
route_with_post = lambda: Route("/users", "post", Response({"test_post": "test_post"}))
route_with_put = lambda: Route("/users", "put", Response({"test_put": "test_put"}))
route_with_delete = lambda: Route(
    "/users", "delete", Response({"test_delete": "test_delete"})
)

resource_get = lambda: Resource(route_with_get().method, route_with_get().response)
resource_post = lambda: Resource(route_with_post().method, route_with_post().response)
resource_put = lambda: Resource(route_with_put().method, route_with_put().response)
resource_delete = lambda: Resource(
    route_with_delete().method, route_with_delete().response
)


def test_create_path_success():
    path = Path(route_with_get().path)
    without_resources = 0

    assert path.path == route_with_get().path
    assert len(path.resources) == without_resources


def test_add_resources_to_path():
    path = Path(route_with_get().path)
    without_resources = 0

    assert path.path == route_with_get().path
    assert len(path.resources) == without_resources

    path.add_resource(resource_get())

    one_resource = 1
    assert len(path.resources) == one_resource

    for resource in path.resources:
        assert resource.method == resource_get().method
        assert resource.response == resource_get().response


def test_update_one_resource():
    path = Path(route_with_get().path)
    path.add_resource(resource_get())

    new_response = Response({"updated_test": "updated_test"})
    new_resource_get = Resource(route_with_get().method, new_response)

    path.update_resource(new_resource_get)

    for resource in path.resources:
        if resource.method == new_resource_get.method:
            assert resource.response == new_resource_get.response


def test_remove_resource():
    path = Path(route_with_get().path)

    path.add_resource(resource_get())
    path.add_resource(resource_post())
    path.add_resource(resource_put())

    assert len(path.resources) == 3

    resource_will_be_removed = Resource(
        route_with_get().method, route_with_get().response
    )
    path.remove_resource(resource_will_be_removed)

    assert len(path.resources) == 2


def test_inserting_routes_twice_in_same_path_fail():
    path = Path(route_with_get().path)
    path.add_resource(resource_get())
    with pytest.raises(DomainBadRequestError):
        path.add_resource(resource_get())


def test_get_dict_object_from_path():
    path = Path(route_with_get().path)

    path.add_resource(resource_get())
    path.add_resource(resource_post())
    path.add_resource(resource_put())
    expected_dict = {
        "_id": path._id,
        "path": "/users",
        "resources": [
            {"method": "GET", "params": [], "response": {"test": "test"}},
            {"method": "POST", "params": [], "response": {"test_post": "test_post"}},
            {"method": "PUT", "params": [], "response": {"test_put": "test_put"}},
        ],
    }

    assert expected_dict == path.get_object_dict()
