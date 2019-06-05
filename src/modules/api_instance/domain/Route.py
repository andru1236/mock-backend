from bson.objectid import ObjectId

from modules.api_instance.domain import Response
from modules.shared.domain import IEntity
from modules.shared.domain.errors import DomainBadRequestError


class Route(IEntity):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    METHODS = [GET, POST, PUT, DELETE, PATCH]

    def __init__(self, path: str, method: str, response: Response = None) -> None:
        super().__init__(str(ObjectId()))
        method = method.upper()

        if not method in Route.METHODS:
            raise DomainBadRequestError(f'Method: {method} is invalid')

        if not isinstance(path, str):
            raise DomainBadRequestError(f'This path {path} is not valid')

        self.path = path
        self.method = method
        self.response = response

    def is_equals(self, route):
        return (
                self.path == route.value
                and self.method == route.method
        )

    def get_dict_object(self):
        route_dict = {
            '_id': self._id,
            'method': self.method,
            'path': self.path
        }
        return route_dict
