from backend.api_instance.domain import IRepository, Response, Route
from backend.shared.domain import ICommand, IUseCase
from backend.shared.infrastructure import logger


class UpdateRouteCommand(ICommand):
    def __init__(self, api_id: str, path: str, method: str, response) -> None:
        self.api_id = api_id
        self.path = path
        self.method = method
        self.response = response


class UpdateRoute(IUseCase):
    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: UpdateRouteCommand):
        logger.info(
            f"The route {command.method} {command.path} will be updated in api {command.api_id}"
        )
        route = Route(command.path, command.method, Response(command.response))
        api = self.repository.search(command.api_id)
        api.replace_route(route)
        self.repository.save(api)
