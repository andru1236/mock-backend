from modules.api_instance.domain import Response
from modules.shared.domain.errors import DomainBadRequestError


class Route:
    GET = 'GET'
    POST = 'POST'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    PATH = 'PATH'
    METHODS = [GET, POST, UPDATE, DELETE, PATH]

    def __init__(self, path: str, method: str, response: Response = None) -> None:
        method = method.upper()

        if not method in Route.METHODS:
            raise DomainBadRequestError(f'Method: {method} is invalid')

        if not isinstance(path, str):
            raise DomainBadRequestError(f'This path {path} is not valid')

        self.value = path
        self.method = method
        self.response = response
