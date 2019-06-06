from modules.shared.domain import ICommand
from modules.shared.domain import IQuery
from modules.shared.domain import IResponse


class IUseCase:

    def execute(self, command: ICommand or IQuery) -> None or IResponse: pass
