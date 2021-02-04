from modules.shared.domain import IBus
from modules.shared.domain import IQuery
from modules.shared.domain import IUseCase
from modules.shared.domain.errors import QueryIsAlreadyRegistered
from .logger import logger


class QueryBus(IBus):

    def __init__(self) -> None:
        self.queries = dict()

    def register(self, command: IQuery, use_case: IUseCase):
        if command.__name__ in self.queries:
            raise QueryIsAlreadyRegistered(f'Command {command.__name__} is already registered')
        logger.info(f'Register query {command.__name__}')
        self.queries[command.__name__] = use_case

    def execute(self, command: IQuery):
        logger.debug(f'Executing query {command.__class__.__name__}')
        return self.queries[command.__class__.__name__].execute(command)
