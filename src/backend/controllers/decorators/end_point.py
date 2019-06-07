from functools import wraps

from backend.utils import ServerResponse
from backend.utils import ErrorHandler
from modules.shared.domain.errors import DomainBaseError
from modules.shared.infrastructure import logger


def end_point(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            response, status = f(*args, **kwargs)
            return ServerResponse(response, status).__dict__, status

        except DomainBaseError as error:
            logger.error(error.__dict__)
            ErrorHandler.catch(error)

        except Exception as error:
            logger.critical(error)
            raise error

    return decorated
