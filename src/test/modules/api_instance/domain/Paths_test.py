from modules.api_instance.domain.api import Path
from modules.api_instance.domain.api import Resource
from modules.api_instance.domain.api import Response
from modules.api_instance.domain.api import Route
from modules.api_instance.domain.api.Paths import Paths

Response_get = Response({'test_get': 'test_get'})
Response_post = Response({'test_post': 'test_post'})
Response_put = Response({'test_put': 'test_put'})
Response_delete = Response({'test_delete': 'test_delete'})

user_path = Path('/users')
user_path.add_resource(Resource('GET', Response_get))
user_path.add_resource(Resource('POST', Response_post))
user_path.add_resource(Resource('PUT', Response_put))
user_path.add_resource(Resource('DELETE', Response_delete))

admin_path = Path('/admin')
admin_path.add_resource(Resource('GET', Response_get))
admin_path.add_resource(Resource('POST', Response_post))
admin_path.add_resource(Resource('PUT', Response_put))
admin_path.add_resource(Resource('DELETE', Response_delete))

user_route_get = Route('/users', 'get', Response_get)
user_route_post = Route('/users', 'post', Response_post)
user_route_put = Route('/users', 'put', Response_put)
user_route_delete = Route('/users', 'delete', Response_delete)

admin_route_get = Route('/admin', 'get', Response_get)
admin_route_post = Route('/admin', 'post', Response_post)
admin_route_put = Route('/admin', 'put', Response_put)
admin_route_delete = Route('/admin', 'delete', Response_delete)


def test_create_path():
    paths = Paths()
    assert len(paths.paths) == 0


def test_add_path():
    paths = Paths()

    paths.add_route(user_route_get)
    paths.add_route(user_route_post)
    paths.add_route(user_route_put)
    paths.add_route(user_route_delete)

    assert len(paths.paths) == 1

    paths.add_route(admin_route_get)
    paths.add_route(admin_route_post)
    paths.add_route(admin_route_put)
    paths.add_route(admin_route_delete)

    assert len(paths.paths) == 2


def test_get_object_dict_of_paths():
    paths = Paths()

    paths.add_route(user_route_get)
    paths.add_route(user_route_post)
    paths.add_route(user_route_put)
    paths.add_route(user_route_delete)

    paths.add_route(admin_route_get)
    paths.add_route(admin_route_post)
    paths.add_route(admin_route_put)
    paths.add_route(admin_route_delete)

    expected_dict = {
        'paths': [user_path.get_object_dict(), admin_path.get_object_dict()]
    }

    print(expected_dict)
    print(paths.get_object_dict())
    assert paths.get_object_dict() == expected_dict
