from backend.shared.domain import IBus
from backend.shared.domain import ICommand
from backend.shared.domain import IUseCase
from backend.shared.domain.errors import CommandIsAlreadyRegistered
from .logger import logger



class CommandBus(IBus):

    def __init__(self) -> None:
        self.commands = dict()

    def register(self, command, use_case: IUseCase):
        if command.__name__ in self.commands:
            raise CommandIsAlreadyRegistered(f'Command {command.__name__} is already registered')
        logger.info(f'Register command {command.__name__}')
        self.commands[command.__name__] = use_case

    def execute(self, command: ICommand):
        logger.debug(f'Executing command {command.__class__.__name__}')
        return self.commands[command.__class__.__name__].execute(command)
