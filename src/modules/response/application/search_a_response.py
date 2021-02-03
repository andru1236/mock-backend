from dataclasses import dataclass, asdict

from modules.shared.domain import IUseCase

from modules.response import domain


@dataclass
class SearchAResponseQuery:
    response_id: str


class SearchAResponse(IUseCase):

    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: SearchAResponseQuery) -> None:
        response: domain.Response = self.repository.search(command.response_id)
        return asdict(domain.validation(response))
