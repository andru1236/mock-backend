from dataclasses import dataclass
from typing import Dict
from modules.shared.domain import IUseCase
from modules.shared.infrastructure import logger



@dataclass
class GetResponsesQuery:
    limit: int = 50


class GetResponses(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, query: GetResponsesQuery) -> Dict:
        logger.info(f'Use case: Get responses')        
        return self.repository.search_all(query.limit)
