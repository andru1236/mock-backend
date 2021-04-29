from backend.shared.domain import ICommand
from backend.shared.domain import IQuery
from backend.shared.domain import IResponse


class IUseCase:

    def execute(self, command: ICommand or IQuery) -> None or IResponse: pass
