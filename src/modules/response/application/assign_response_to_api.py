from dataclasses import dataclass
from modules.shared.domain import IUseCase
from ..infrastructure.integration_services import ApiServiceBus
from modules.response import domain

@dataclass
class AssignReponseToAPICommand:
    api_id: str
    response_id: str
    path: str
    method: str
    query_param: str = None


class AssignResponseToAPI(IUseCase):

    def __init__(self, repository, bus: ApiServiceBus) -> None:
        self.repository = repository
        self.bus = bus

    def execute(self, command: AssignReponseToAPICommand) -> None:
        response: domain.Response = self.repository.search(command.response_id)
        self.bus.updateApiRoute(
            command.api_id,
            command.path,
            command.method,
            response.response
        )
        domain.track_response(response, command)
        self.repository.save(response)
        
        
