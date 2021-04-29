from flask_restx import abort

from backend.shared.infrastructure.process_manager import PortIsBusy, NotEnoughResources
from backend.api_instance.domain.exceptions import ServerIsRunning, ServerNeverWasStarting
from backend.shared.domain.errors import DomainBadRequestError, DomainDontFoundError


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
