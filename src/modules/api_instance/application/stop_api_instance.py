from modules.api_instance.domain.api import IRepository
from modules.api_instance.domain.builder_server import BuilderServer
from modules.api_instance.domain.builder_server.errors import ServerNeverWasStarting
from modules.shared.domain import ICommand
from modules.shared.domain import IResponse
from modules.shared.domain import IUseCase


class StopInstanceCommand(ICommand):

    def __init__(self, api_id: str) -> None:
        self.api_id = api_id


class StopInstance(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: StopInstanceCommand) -> None or IResponse:
        api = self.repository.search(command.api_id)
        if api.settings.enabled is False:
            raise ServerNeverWasStarting(f'The never was starting')
        api.settings.enabled = True
        self.repository.save(api)
        builder_server = BuilderServer()
        builder_server.stop_api(command.api_id)
