from modules.shared.domain.errors import DomainBadRequestError


class Port:
    def __init__(self, port: int) -> None:
        if not isinstance(port, int):
            raise DomainBadRequestError(f"Port should be a integer")
        if port < 80:
            raise DomainBadRequestError(f"This port {port} is reserved")
        if port > 65535:
            raise DomainBadRequestError(
                f"This port {port} is not in the range standard range"
            )
        self.value = port
