from modules.shared.domain import ICommand


class IUseCase:

    def execute(self, command: ICommand): pass
