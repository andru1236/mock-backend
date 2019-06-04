from typing import List

from modules.api_instance.domain import Port
from modules.api_instance.domain import Route


class ApiInstance:

    def __init__(self, port: Port, routes=None) -> None:
        self.port: Port = port
        self.routes: List[Route] = routes

    def add_route(self, route: Route):
        self.routes.append(route)
