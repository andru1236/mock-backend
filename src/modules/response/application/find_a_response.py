from dataclasses import dataclass

from modules.shared.domain import IUseCase

from modules.response import domain


@dataclass
class FindAResponseCommand:
    response_id: str


class FindAResponse(IUseCase):

    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: FindAResponseCommand) -> None:
        response: domain.Response = self.repository.search(command.response_id)
        print(response)
        print(type(response.tracking_assignations))

