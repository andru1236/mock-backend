from modules.api_instance.domain.api import ApiInstance
from modules.api_instance.domain.api import IRepository
from modules.api_instance.domain.api import Port
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase
from modules.shared.infrastructure import logger


class RegisterApiCommand(ICommand):
    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port


class RegisterApi(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: RegisterApiCommand):
        logger.info(f'Execute Create new api instance with port {command.port}')
        port = Port(command.port)
        api = ApiInstance(command.name, port)
        self.repository.save(api)
