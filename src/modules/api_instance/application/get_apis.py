from modules.api_instance.domain.api import IRepository
from modules.shared.domain import ICommand
from modules.shared.domain import IQuery
from modules.shared.domain import IResponse
from modules.shared.domain import IUseCase


class GetApisQuery(IQuery): pass


class GetApis(IUseCase):

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    def execute(self, command: ICommand or IQuery) -> None or IResponse:
        return self.repository.get_apis()
