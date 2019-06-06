from modules.shared.domain import IBus
from modules.shared.domain import IQuery
from modules.shared.domain import IUseCase
from modules.shared.domain.errors import QueryIsAlreadyRegistered


class QueryBus(IBus):

    def __init__(self) -> None:
        self.querys = dict()

    def register(self, command: IQuery, use_case: IUseCase):
        if command.__name__ in self.querys:
            raise QueryIsAlreadyRegistered(f'Command {command.__name__} is already registered')
        self.querys[command.__name__] = use_case

    def execute(self, command: IQuery):
        return self.querys[command.__class__.__name__].execute(command)
