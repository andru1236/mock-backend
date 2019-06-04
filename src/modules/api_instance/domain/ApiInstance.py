from typing import List

from modules.api_instance.domain import Port
from modules.api_instance.domain import Route
from modules.shared.domain import IAggregate
from modules.shared.domain.errors import DomainBadRequestError


class ApiInstance(IAggregate):

    def __init__(self, port: Port, routes=None) -> None:
        super().__init__()
        self.port: Port = port
        self.routes: List[Route] = routes

    def add_route(self, new_route: Route):
        for route in self.routes:
            if new_route.value == route.value and new_route.method == route.method:
                raise DomainBadRequestError(f'This route [{new_route.method}] {new_route.value} is busy')

        self.routes.append(new_route)
