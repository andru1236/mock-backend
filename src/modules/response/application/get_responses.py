from dataclasses import dataclass
from typing import Dict
from modules.shared.domain import IUseCase



@dataclass
class GetResponsesQuery:
    limit: int = 50


class GetResponses(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, query: GetResponsesQuery) -> Dict:
        return self.repository.search_all(query.limit)
        