from modules.shared.domain.errors import DomainBaseError


class ServerIsRunning(DomainBaseError):
    pass


class ServerNeverWasStarting(DomainBaseError):
    pass
