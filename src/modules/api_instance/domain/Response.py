from json import loads

from modules.shared.domain.errors import DomainBadRequestError


class Response:
    def __init__(self, response: str) -> None:
        try:
            loads(response)
            self.value = response
        except ValueError:
            raise DomainBadRequestError('The response is not a json')
