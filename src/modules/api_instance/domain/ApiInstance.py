from typing import List

from modules.api_instance.domain import Port
from modules.api_instance.domain import Route
from modules.api_instance.domain import Settings
from modules.shared.domain import IAggregate
from modules.shared.domain.errors import DomainBadRequestError


class ApiInstance(IAggregate):

    def __init__(self, port: Port, routes=None, settings: Settings = Settings(), _id: str = '') -> None:
        super().__init__(_id)
        self.port: Port = port
        self.routes: List[Route] = [] if routes is None else routes
        self.settings = settings

    def add_route(self, new_route: Route):
        if self.__this_route_is_registered_in_routes(new_route):
            raise DomainBadRequestError(f'This route [{new_route.method}] {new_route.path} is busy')
        self.routes.append(new_route)

    def replace_route(self, new_route):
        if not self.__this_route_is_registered_in_routes(new_route):
            raise DomainBadRequestError(f'This route [{new_route.method}] {new_route.path} not exist')

        new_routes = self.__get_list_without_route(new_route)

        new_routes.append(new_route)
        self.routes = new_routes

    def remove_route(self, route):
        if not self.__this_route_is_registered_in_routes(route):
            raise DomainBadRequestError(f'This route [{route.method}] {route.path} not exist')

        self.routes = self.__get_list_without_route(route)

    def run_api(self):
        pass

    def get_object_dict(self):
        object_dict = {
            '_id': self._id,
            'port': self.port.value,
            'routes': [route.get_object_dict() for route in self.routes],
            'settings': self.settings.__dict__
        }
        return object_dict

    def __get_list_without_route(self, route: Route) -> List[Route]:
        return list(filter(lambda x: not route.is_equals(x), self.routes))

    def __this_route_is_registered_in_routes(self, new_route: Route) -> bool:
        for route in self.routes:
            if route.is_equals(new_route):
                return True
        return False
