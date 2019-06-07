from modules.api_instance.domain.api import IRepository
from modules.api_instance.domain.builder_server import BuilderServer
from modules.api_instance.domain.builder_server.errors import ServerNeverWasStarting
from modules.shared.domain import ICommand
from modules.shared.domain import IResponse
from modules.shared.domain import IUseCase
from modules.shared.infrastructure import logger


class StopApiInstanceCommand(ICommand):

    def __init__(self, api_id: str) -> None:
        self.api_id = api_id


class StopApiInstance(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: StopApiInstanceCommand) -> None or IResponse:
        api = self.repository.search(command.api_id)
        logger.info(f'The api {api._id} in port {api.port} will be stopped')
        if api.settings.enabled is False:
            raise ServerNeverWasStarting(f'The never was starting')
        api.settings.enabled = False
        self.repository.save(api)
        builder_server = BuilderServer()
        builder_server.stop_api(command.api_id)
