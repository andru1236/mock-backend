from modules.shared.domain import IBus
from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase
from modules.shared.domain.errors import CommandIsAlreadyRegistered


class CommandBus(IBus):

    def __init__(self) -> None:
        self.commands = dict()

    def register(self, command, use_case: IUseCase):
        if command.__name__ in self.commands:
            raise CommandIsAlreadyRegistered(f'Command {command.__name__} is already registered')
        self.commands[command.__name__] = use_case

    def execute(self, command: ICommand):
        return self.commands[command.__class__.__name__].execute(command)
