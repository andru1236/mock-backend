from dataclasses import dataclass, replace, asdict
from backend.shared.domain import IUseCase
from backend.shared.infrastructure import logger
from backend.response import domain


@dataclass
class UpdateApiResponseCommand:
    response_id: str
    name: str
    response: dict


class UpdateApiResponse(IUseCase):
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, command: UpdateApiResponseCommand) -> None:
        logger.info(f"Use case update response: [{command.response_id}]")
        found_response = self.repository.search(command.response_id)

        to_update = asdict(command)
        del to_update["response_id"]

        response_to_update = replace(found_response, **to_update)
        domain.validation(response_to_update)

        self.repository.save(response_to_update)
