from backend.shared.domain import ICommand, IResponse, IUseCase
from backend.shared.domain.errors import DomainBadRequestError
from backend.shared.infrastructure import logger, process_manager

from backend.api_instance.domain import IRepository
from backend.api_instance.domain.exceptions import ServerIsRunning
from backend.api_instance.infrastructure.builder_webs import build_flask_server


class LaunchApiInstanceCommand(ICommand):
    def __init__(self, api_id: str) -> None:
        self.api_id = api_id


class LaunchApiInstance(IUseCase):
    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: LaunchApiInstanceCommand) -> None or IResponse:
        api = self.repository.search(command.api_id)
        logger.info(f"Launch api {api._id} in port {api.port.value}")

        if api.settings.enabled is True:
            raise ServerIsRunning(f"The server is running in port {api.port.value}")
        if len(api.get_list_paths()) == 0:
            raise DomainBadRequestError(f"this API: {api._id} does not have routes")

        flask_instance = build_flask_server(api)
        process_manager.ProcessManager().run_obj_as_process(
            api._id,
            flask_instance,
            flask_instance.app.run,
            ("0.0.0.0", api.port.value),
            api.port.value,
            []
        )

        api.settings.enabled = True
        self.repository.save(api)
