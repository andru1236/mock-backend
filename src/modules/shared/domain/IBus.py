from modules.shared.domain import ICommand
from modules.shared.domain import IUseCase


class IBus:

    def register(self, command: ICommand, use_case: IUseCase): pass

    def execute(self, command: ICommand): pass
