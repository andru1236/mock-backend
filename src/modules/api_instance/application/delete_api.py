from modules.api_instance.domain import IRepository
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase


class DeleteApiCommand(ICommand):
    def __init__(self, api_id: str) -> None:
        self.api_id = api_id


class DeleteApi(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: DeleteApiCommand):
        self.repository.delete(command.api_id)
