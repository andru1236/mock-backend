from modules.shared.domain.errors import DomainBadRequestError


class Route:
    def __init__(self, path: str) -> None:
        if not isinstance(path, str):
            raise DomainBadRequestError(f'this path {path} is not valid')

        self.value = path
