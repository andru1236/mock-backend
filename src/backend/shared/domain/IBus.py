from backend.shared.domain import ICommand
from backend.shared.domain import IQuery
from backend.shared.domain import IUseCase


class IBus:

    def register(self, command: ICommand or IQuery, use_case: IUseCase): pass

    def execute(self, command: ICommand or IQuery): pass
