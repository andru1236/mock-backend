from flask_restx import abort

from modules.shared.infrastructure.process_manager import PortIsBusy, NotEnoughResources
from modules.api_instance.domain.builder_server.exceptions import ServerIsRunning, ServerNeverWasStarting
from modules.shared.domain.errors import DomainBadRequestError, DomainDontFoundError


class ErrorHandler:

    @staticmethod
    def catch(error):
        if type(error) == DomainBadRequestError:
            abort(400, custom=error.__dict__)
        elif type(error) == DomainDontFoundError:
            abort(404, custom=error.__dict__)
        elif type(error) == ServerIsRunning:
            abort(404, custom=error.__dict__)
        elif type(error) == ServerNeverWasStarting:
            abort(404, custom=error.__dict__)
        elif type(error) == PortIsBusy:
            abort(400, custom=error.__dict__)
        elif type(error) == NotEnoughResources:
            abort(400, custom=error.__dict__)
