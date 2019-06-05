from modules.api_instance.domain import IRepository
from modules.api_instance.domain import Route
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase


class AddRouteCommand(ICommand):
    def __init__(self, api_id: str, path: str, method: str) -> None:
        self.api_id = api_id
        self.path = path
        self.method = method


class AddRoute(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: AddRouteCommand):
        route = Route(command.path, command.method)
        api = self.repository.search(command.api_id)
        api.add_route(route)
        self.repository.save(api)