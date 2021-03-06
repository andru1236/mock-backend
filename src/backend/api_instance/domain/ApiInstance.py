from .Paths import Paths
from .Port import Port
from .Route import Route
from .Settings import Settings
from backend.shared.domain import IAggregate


class ApiInstance(IAggregate):

    def __init__(self, name: str, port: Port, paths: Paths = None, settings: Settings = Settings(),
                 _id: str = '') -> None:
        super().__init__(_id)
        self.name = name
        self.port: Port = port
        self.paths: Paths = Paths() if paths is None else paths
        self.settings = settings

    def add_route(self, new_route: Route):
        self.paths.add_route(new_route)

    def replace_route(self, new_route):
        self.paths.update_route(new_route)

    def remove_route(self, route):
        self.paths.remove_route(route)

    def get_list_paths(self):
        return self.paths.paths

    def get_path(self, route: Route):
        return self.paths.get_path_with_this(route)
    
    def get_path_by_id(self, path_id: str):
        return self.paths.get_path_by_id(path_id)

    def get_object_dict(self):
        object_dict = {
            '_id': self._id,
            'name': self.name,
            'port': self.port.value,
            'routes': self.paths.get_object_dict(),
            'settings': self.settings.__dict__
        }
        return object_dict
