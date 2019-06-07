from flask_restplus import abort

from modules.api_instance.domain.builder_server.errors import ServerIsRunning
from modules.api_instance.domain.builder_server.errors import ServerNeverWasStarting
from modules.shared.domain.errors import DomainBadRequestError
from modules.shared.domain.errors import DomainDontFoundError


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
