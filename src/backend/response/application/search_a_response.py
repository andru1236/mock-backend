from dataclasses import dataclass, asdict
from backend.shared.domain import IUseCase
from backend.response import domain
from backend.shared.infrastructure import logger


@dataclass
class SearchAResponseQuery:
    response_id: str


class SearchAResponse(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: SearchAResponseQuery) -> None:
        logger.info(f"Use case: search response [{command.response_id}]")
        response: domain.Response = self.repository.search(command.response_id)
        return asdict(domain.validation(response))
