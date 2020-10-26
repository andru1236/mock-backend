from modules.api_instance.domain.api import IRepository
from modules.api_instance.domain.api import Response
from modules.api_instance.domain.api import Route
from modules.api_instance.domain.api import Param, Path, Resource
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase

from modules.shared.infrastructure import logger


class DeleteParamsCommand(ICommand):
    def __init__(self, api_id: str, route_id:str, params: str, method: str) -> None:
        self.api_id = api_id
        self.route_id = route_id
        self.params = params
        self.method = method


class DeleteParams(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: DeleteParamsCommand):
        logger.info(f'The param {command.params} will be removed from api {command.api_id} and route {command.route_id}')
        param = Param(command.params, Response({}))
        api = self.repository.search(command.api_id)
        path = api.get_path_by_id(command.route_id)
        resource = path.get_resource_by_method(command.method)
        resource.remove_params(param)
        self.repository.save(api)
