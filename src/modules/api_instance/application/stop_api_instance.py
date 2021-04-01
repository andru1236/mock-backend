from modules.api_instance.domain import IRepository
from modules.api_instance.domain.exceptions import ServerNeverWasStarting
from modules.shared.domain import ICommand, IResponse, IUseCase
from modules.shared.infrastructure import logger, process_manager


class StopApiInstanceCommand(ICommand):
    def __init__(self, api_id: str) -> None:
        self.api_id = api_id


class StopApiInstance(IUseCase):
    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: StopApiInstanceCommand) -> None or IResponse:
        api = self.repository.search(command.api_id)
        logger.info(f"The api {api._id} in port {api.port.value} will be stopped")

        if api.settings.enabled is False:
            raise ServerNeverWasStarting(f"The never was starting")

        api.settings.enabled = False
        self.repository.save(api)

        process_manager.ProcessManager().stop_process(api._id)
