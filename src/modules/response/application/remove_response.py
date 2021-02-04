from dataclasses import dataclass
from modules.shared.domain import IUseCase
from modules.shared.infrastructure import logger


@dataclass
class RemoveResponseCommand:
    response_id: str = None


class RemoveResponse(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: RemoveResponseCommand) -> None:
        logger.info(f'Use case remove  response [{command.response_id}]')
        self.repository.delete(command.response_id)


