from typing import List

from modules.api_instance.domain.api import Path
from modules.api_instance.domain.api import Resource
from modules.api_instance.domain.api import Route
from modules.shared.domain.errors import DomainBadRequestError


class Paths:
    def __init__(self, paths=None) -> None:
        self.paths: List[Path] = [] if paths is None else paths

    def add_route(self, route: Route):
        path = self.get_path_with_this(route)

        if path is None:
            path = Path(route.path)
            path.add_resource(Resource(route.method, route.response))
            self.paths.append(path)
        else:
            path.add_resource(Resource(route.method, route.response))

    def remove_route(self, route: Route):
        path = self.get_path_with_this(route)
        if path is None:
            raise DomainBadRequestError(f'This path {route.path} not exist')

        path.remove_resource(Resource(route.method, route.response))

        if len(path.resources) == 0:
            self.__path_garbage_collector(path)

    def update_route(self, route: Route):
        path = self.get_path_with_this(route)
        if path is None:
            raise DomainBadRequestError(f'This path {route.path} not exist')
        path.update_resource(Resource(route.method, route.response))

    def get_path_with_this(self, route: Route):
        for index, path in enumerate(self.paths):
            if path.path == route.path:
                return self.paths[index]
        return None

    def get_path_by_id(self, id_path: str):
        for path in self.paths:
            if path._id == id_path:
                return path
        raise DomainBadRequestError(f'This path id {id_path} not exist')

    def get_object_dict(self):
        return [path.get_object_dict() for path in self.paths]

    def __path_garbage_collector(self, path):
        for index, p in enumerate(self.paths):
            if p.path == path.path:
                del self.paths[index]
                break
