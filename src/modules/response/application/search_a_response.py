from dataclasses import dataclass, asdict
from modules.shared.domain import IUseCase
from modules.response import domain
from modules.shared.infrastructure import logger

@dataclass
class SearchAResponseQuery:
    response_id: str


class SearchAResponse(IUseCase):

    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: SearchAResponseQuery) -> None:
        logger.info(f'Use case: search response [{command.response_id}]')
        response: domain.Response = self.repository.search(command.response_id)
        return asdict(domain.validation(response))
