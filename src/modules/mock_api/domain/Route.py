from modules.mock_api.domain import Response
from modules.shared.domain.errors import DomainBadRequestError


class Route:
    def __init__(self, path: str, response: Response = None) -> None:
        if not isinstance(path, str):
            raise DomainBadRequestError(f'this path {path} is not valid')

        self.value = path
        self.response = response
