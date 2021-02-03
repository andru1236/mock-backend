from modules.shared.domain.errors import DomainBaseError
from modules.api_instance import command_bus, UpdateRouteCommand


class IntegrationError(DomainBaseError): pass


class ApiServiceBus:
    @staticmethod
    def updateApiRoute(api_id, path, method, response):
        try:
            command_bus.execute(UpdateRouteCommand(api_id, path, method, response))
        except Exception:
            raise IntegrationError('The response module was not able to integrate with API instance module')

