from modules.api_instance.application.add_route import AddRoute
from modules.api_instance.application.add_route import AddRouteCommand
from modules.api_instance.application.delete_api import DeleteApi
from modules.api_instance.application.delete_api import DeleteApiCommand
from modules.api_instance.application.delete_route import DeleteRoute
from modules.api_instance.application.delete_route import DeleteRouteCommand
from modules.api_instance.application.register_api import RegisterApi
from modules.api_instance.application.register_api import RegisterApiCommand
from modules.api_instance.application.update_api import UpdateApi
from modules.api_instance.application.update_api import UpdateApiCommand
from modules.api_instance.application.update_route import UpdateRoute
from modules.api_instance.application.update_route import UpdateRouteCommand
from modules.api_instance.infrastructure import Repository
from modules.shared.infrastructure import CommandBus

repository = Repository()
command_bus = CommandBus()
# use cases
command_bus.register(RegisterApiCommand, RegisterApi(repository))
command_bus.register(AddRouteCommand, AddRoute(repository))
command_bus.register(DeleteApiCommand, DeleteApi(repository))
command_bus.register(DeleteRouteCommand, DeleteRoute(repository))
command_bus.register(UpdateApiCommand, UpdateApi(repository))
command_bus.register(UpdateRouteCommand, UpdateRoute(repository))
