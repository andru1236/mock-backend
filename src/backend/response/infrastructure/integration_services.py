from backend.shared.domain.errors import DomainBaseError
from backend.api_instance import command_bus, UpdateRouteCommand
from backend.shared.infrastructure import logger


# TODO Move to new module: exceptions in root of infrastructure
class IntegrationError(DomainBaseError):
    pass


class ApiServiceBus:
    @staticmethod
    def update_api_route(api_id, path, method, response):
        logger.info(f"Connect with [api_instance] Module")
        try:
            command_bus.execute(UpdateRouteCommand(api_id, path, method, response))
        except Exception:
            raise IntegrationError(
                "The response module was not able to integrate with API instance module"
            )
