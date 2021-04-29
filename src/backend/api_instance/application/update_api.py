from backend.api_instance.domain import IRepository, Port
from backend.shared.domain import ICommand, IUseCase
from backend.shared.infrastructure import logger


class UpdateApiCommand(ICommand):
    def __init__(self, api_id: str, name: str, port: int) -> None:
        self.api_id = api_id
        self.name = name
        self.port = port


class UpdateApi(IUseCase):
    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: UpdateApiCommand):
        logger.info(f"The api {command.api_id} will be updated")
        port = Port(command.port)
        api = self.repository.search(command.api_id)
        api.name = command.name
        api.port = port
        self.repository.save(api)
