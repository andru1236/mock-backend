from dataclasses import dataclass
from modules.shared.domain import IUseCase


@dataclass
class RemoveResponseCommand:
    response_id: str = None


class RemoveResponse(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: RemoveResponseCommand) -> None:
        self.repository.delete(command.response_id)


