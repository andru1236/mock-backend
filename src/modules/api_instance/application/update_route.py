from modules.api_instance.domain import IRepository
from modules.api_instance.domain import Route
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase


class UpdateRouteCommand(ICommand):

    def __init__(self, route_id: str, path: str, method: str) -> None:
        self.route_id = route_id
        self.path = path
        self.method = method


class UpdateRoute(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: UpdateRouteCommand):
        route = Route(command.path, command.method)
