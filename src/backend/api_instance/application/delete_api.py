from backend.api_instance.domain import IRepository
from backend.shared.domain import ICommand, IUseCase
from backend.shared.infrastructure import logger


class DeleteApiCommand(ICommand):
    def __init__(self, api_id: str) -> None:
        self.api_id = api_id


class DeleteApi(IUseCase):
    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: DeleteApiCommand):
        logger.info(f"Execute delete api {command.api_id}")
        self.repository.delete(command.api_id)
