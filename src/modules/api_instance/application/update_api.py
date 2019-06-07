from modules.api_instance.domain.api import IRepository
from modules.api_instance.domain.api import Port
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase
from modules.shared.infrastructure import logger


class UpdateApiCommand(ICommand):

    def __init__(self, api_id: str, port: int) -> None:
        self.api_id = api_id
        self.port = port


class UpdateApi(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: UpdateApiCommand):
        logger.info(f'The api {command.api_id} will be updated')
        port = Port(command.port)
        api = self.repository.search(command.api_id)
        api.port = port
        self.repository.save(api)
