from dataclasses import dataclass
from backend.shared.domain import IUseCase

from backend.response import domain
from backend.shared.infrastructure import logger


@dataclass
class CreateApiResponseCommand:
    name: str
    response: list or dict


class CreateApiResponse(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: CreateApiResponseCommand) -> None:
        logger.info(f"Use case: creating new response")
        new_response = domain.Response(command.name, command.response)
        domain.validation(new_response)
        self.repository.save(new_response)