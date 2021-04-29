from dataclasses import dataclass
from backend.shared.domain import IUseCase
from backend.shared.infrastructure import logger
from backend.response import domain
from ..infrastructure.integration_services import ApiServiceBus


@dataclass
class AssignReponseToAPICommand:
    api_id: str
    response_id: str
    path: str
    method: str
    query_param: str = None


class AssignResponseToAPI(IUseCase):
    def __init__(self, repository, api_entrypoint: ApiServiceBus) -> None:
        self.repository = repository
        self.api_entrypoint: ApiServiceBus = api_entrypoint

    def execute(self, command: AssignReponseToAPICommand) -> None:
        logger.info(
            f"Use case Assign Response: [{command.response_id}] to API: [{command.api_id}]"
        )

        response: domain.Response = self.repository.search(command.response_id)

        self.api_entrypoint.update_api_route(
            command.api_id, command.path, command.method, response.response
        )

        domain.track_response(response, command)
        self.repository.save(response)
