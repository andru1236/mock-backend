from .Response import Response
from backend.shared.domain import IEntity
from backend.shared.domain.errors import DomainBadRequestError


class Route(IEntity):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    METHODS = [GET, POST, PUT, DELETE, PATCH]

    def __init__(self, path: str, method: str, response: Response, _id: str = None) -> None:
        super().__init__(_id)
        method = method.upper()

        if method not in Route.METHODS:
            raise DomainBadRequestError(f'Method: {method} is invalid')

        if not isinstance(path, str):
            raise DomainBadRequestError(f'This path {path} is not valid')

        if not isinstance(response, Response):
            raise DomainBadRequestError(f'Response should be json object')

        self.path = path
        self.method = method
        self.response = response

    def is_equals(self, route):
        return (
                self.path == route.path
                and self.method == route.method
        )

    def get_object_dict(self):
        route_dict = {
            '_id': self._id,
            'method': self.method,
            'path': self.path,
            'response': self.response.value
        }
        return route_dict
