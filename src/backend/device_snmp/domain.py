from dataclasses import dataclass
from backend.shared.domain import errors


def valid_port(port: int):
    if not isinstance(port, int):
        raise errors.DomainBadRequestError("The port should be integer")
    if port < 80:
        raise errors.DomainBadRequestError(f"This port {port} is reserved")
    if port > 65535:
        raise errors.DomainBadRequestError(
            f"This port {port} is not in the range standard range"
        )


@dataclass
class Device:
    agent_db: str
    port: int
    is_running: bool = False
    id: str = None

    def __post_init__(self):
        valid_port(self.port)
