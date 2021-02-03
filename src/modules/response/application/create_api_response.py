from dataclasses import dataclass
from modules.shared.domain import IUseCase

from modules.response import domain

@dataclass
class CreateApiResponseCommand:
    name: str
    response: list or dict


class CreateApiResponse(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: CreateApiResponseCommand) -> None:
        new_response = domain.Response(command.name, command.response)
        domain.validation(new_response)
        self.repository.save(new_response)