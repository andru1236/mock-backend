from backend.api_instance.domain import (
    IRepository,
    Response,
    Param,
)
from backend.shared.domain import ICommand, IUseCase

from backend.shared.infrastructure import logger


class UpdateParamsCommand(ICommand):
    def __init__(
        self, api_id: str, route_id: str, params: str, method: str, response
    ) -> None:
        self.api_id = api_id
        self.route_id = route_id
        self.params = params
        self.method = method
        self.response = response


class UpdateParams(IUseCase):
    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: UpdateParamsCommand):
        logger.info(
            f"Execute update param to api {command.api_id}, route {command.route_id}"
        )
        param = Param(command.params, Response(command.response))
        api = self.repository.search(command.api_id)
        path = api.get_path_by_id(command.route_id)
        resource = path.get_resource_by_method(command.method.upper())
        resource.replace_params(param)
        self.repository.save(api)
