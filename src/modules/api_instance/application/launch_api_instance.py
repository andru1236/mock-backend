from modules.api_instance.domain.api import IRepository
from modules.api_instance.domain.builder_server import BuilderServer
from modules.shared.domain import ICommand
from modules.shared.domain import IResponse
from modules.shared.domain import IUseCase


class LaunchApiInstanceCommand(ICommand):
    def __init__(self, _id: str) -> None:
        self._id = _id


class LaunchApiInstance(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: LaunchApiInstanceCommand) -> None or IResponse:
        api = self.repository.search(command._id)
        if api.settings.enabled is False:
            api.settings.enabled = True
        self.repository.save(api)

        builder_server = BuilderServer()
        builder_server.run_api(api)
