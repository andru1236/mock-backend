from modules.api_instance.domain import IRepository
from modules.api_instance.domain import Response
from modules.api_instance.domain import Route
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase

from modules.shared.infrastructure import logger


class AddRouteCommand(ICommand):
    def __init__(self, api_id: str, path: str, method: str, response: str) -> None:
        self.api_id = api_id
        self.path = path
        self.method = method
        self.response = response


class AddRoute(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: AddRouteCommand):
        logger.info(f'Execute add route to api {command.api_id}')
        route = Route(command.path, command.method, Response(command.response))
        api = self.repository.search(command.api_id)
        api.add_route(route)
        self.repository.save(api)
