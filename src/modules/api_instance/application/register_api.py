from modules.api_instance.domain import ApiInstance
from modules.api_instance.domain import IRepository
from modules.api_instance.domain import Port
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase


class RegisterApiCommand(ICommand):
    def __init__(self, port: int) -> None:
        self.port = port


class RegisterApi(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: RegisterApiCommand):
        port = Port(command.port)
        api = ApiInstance(port)
        self.repository.save(api)
