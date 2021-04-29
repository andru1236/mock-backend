from functools import wraps

from gateway.api_rest.utils import ServerResponse
from gateway.api_rest.utils import ErrorHandler
from backend.shared.domain.errors import DomainBaseError
from backend.shared.infrastructure import logger


def return_with_custom_format(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            response, status = f(*args, **kwargs)
            return ServerResponse(response, status).__dict__, status

        except DomainBaseError as error:
            logger.error(error.__dict__)
            ErrorHandler.catch(error)

        except Exception as error:
            logger.error(error)
            raise error

    return decorated
