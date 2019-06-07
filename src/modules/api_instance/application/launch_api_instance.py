from modules.api_instance.domain.api import IRepository
from modules.api_instance.domain.builder_server import BuilderServer
from modules.api_instance.domain.builder_server.errors import ServerIsRunning
from modules.shared.domain import ICommand
from modules.shared.domain import IResponse
from modules.shared.domain import IUseCase
from modules.shared.domain.errors import DomainBadRequestError
from modules.shared.infrastructure import logger


class LaunchApiInstanceCommand(ICommand):
    def __init__(self, api_id: str) -> None:
        self.api_id = api_id


class LaunchApiInstance(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: LaunchApiInstanceCommand) -> None or IResponse:
        api = self.repository.search(command.api_id)
        logger.info(f'Launch api {api._id} in port {api.port.value}')
        if api.settings.enabled is True:
            raise ServerIsRunning(f'The server is running in port {api.port.value}')
        if len(api.routes) == 0:
            raise DomainBadRequestError(f'this API: {api._id} does not have routes')
        api.settings.enabled = True
        self.repository.save(api)

        builder_server = BuilderServer()
        builder_server.run_api(api)
