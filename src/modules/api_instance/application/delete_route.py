from modules.api_instance.domain.api import IRepository
from modules.api_instance.domain.api import Response
from modules.api_instance.domain.api import Route
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase
from modules.shared.infrastructure import logger


class DeleteRouteCommand(ICommand):

    def __init__(self, api_id: str, path: str, method: str) -> None:
        self.api_id = api_id
        self.path = path
        self.method = method


class DeleteRoute(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: DeleteRouteCommand):
        logger.info(f'The route {command.method} {command.path} will be removed from api {command.api_id}')
        route = Route(command.path, command.method, Response({}))
        api = self.repository.search(command.api_id)
        api.remove_route(route)
        self.repository.save(api)
