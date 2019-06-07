from modules.api_instance.domain import IRepository
from modules.shared.domain import IQuery
from modules.shared.domain import IResponse
from modules.shared.domain import IUseCase
from modules.shared.infrastructure import logger


class SearchApiQuery(IQuery):
    def __init__(self, api_id: str) -> None:
        self.api_id = api_id


class SearchApiResponse(IResponse):

    def __init__(self, _id: str, port: int, routes, settings):
        self._id = _id
        self.port = port
        self.routes = routes
        self.settings = settings


class SearchApi(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: SearchApiQuery):
        logger.info(f'Search api {command.api_id}')
        api = self.repository.search(command.api_id)
        return SearchApiResponse(**api.get_object_dict()).__dict__
