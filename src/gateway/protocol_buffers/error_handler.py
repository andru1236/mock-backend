from dataclasses import dataclass

from backend.shared.infrastructure.process_manager import PortIsBusy, NotEnoughResources
from backend.api_instance.domain.exceptions import (
    ServerIsRunning,
    ServerNeverWasStarting,
)
from backend.shared.domain.errors import DomainBadRequestError, DomainDontFoundError
from backend.shared.infrastructure import logger


@dataclass
class ErrorResponse:
    message: str
    sucessfull: bool = False


def handler_error(error):
    logger.error(error.message)
    if type(error) == DomainBadRequestError:
        return 400, error.message
    elif type(error) == DomainDontFoundError:
        return 404, error.message
    elif type(error) == ServerIsRunning:
        return 404, error.message
    elif type(error) == ServerNeverWasStarting:
        return 404, error.message
    elif type(error) == PortIsBusy:
        return 404, error.message
    elif type(error) == NotEnoughResources:
        return 404, error.message
    elif type(error) == Exception:
        return 500, error.message


def exec_with_error_handler(fn):
    def _inner_fn(*args, **kwargs):
        try:
            logger.debug("Executing with error handler")
            response = fn(*args, **kwargs)
            if response is not None:
                return response
            return True

        except Exception as error:
            code, message = handler_error(error)
            return ErrorResponse(message=f"Code: {code}. Message: {message}")

    return _inner_fn
