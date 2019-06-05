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
        if self.__this_route_is_registered_in_routes(new_route):
            raise DomainBadRequestError(f'This route [{new_route.method}] {new_route.value} is busy')
        self.routes.append(new_route)

    def replace_route(self, new_route):
        if not self.__this_route_is_registered_in_routes(new_route):
            raise DomainBadRequestError(f'This route [{new_route.method}] {new_route.value} not exist')

        new_routes = self.__get_list_without_route(new_route)

        new_routes.append(new_route)
        self.routes = new_routes

    def remove_route(self, route):
        if not self.__this_route_is_registered_in_routes(route):
            raise DomainBadRequestError(f'This route [{route.method}] {route.value} not exist')

        self.routes = self.__get_list_without_route(route)

    def __get_list_without_route(self, route: Route) -> List[Route]:
        return list(filter(lambda x: not self.__these_routes_are_equals(x, route), self.routes))

    def __this_route_is_registered_in_routes(self, new_route: Route) -> bool:
        for route in self.routes:
            if self.__these_routes_are_equals(route, new_route):
                return True
        return False

    def __these_routes_are_equals(self, route: Route, new_route: Route):
        if new_route.value == route.value and new_route.method == route.method:
            return True
        return False
