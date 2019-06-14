from modules.api_instance.application.add_route import AddRoute
from modules.api_instance.application.add_route import AddRouteCommand
from modules.api_instance.application.delete_api import DeleteApi
from modules.api_instance.application.delete_api import DeleteApiCommand
from modules.api_instance.application.delete_route import DeleteRoute
from modules.api_instance.application.delete_route import DeleteRouteCommand
from modules.api_instance.application.launch_api_instance import LaunchApiInstance
from modules.api_instance.application.launch_api_instance import LaunchApiInstanceCommand
from modules.api_instance.application.register_api import RegisterApi
from modules.api_instance.application.register_api import RegisterApiCommand
from modules.api_instance.application.search_api import SearchApi
from modules.api_instance.application.search_api import SearchApiQuery
from modules.api_instance.application.stop_api_instance import StopApiInstance
from modules.api_instance.application.stop_api_instance import StopApiInstanceCommand
from modules.api_instance.application.update_api import UpdateApi
from modules.api_instance.application.update_api import UpdateApiCommand
from modules.api_instance.application.update_route import UpdateRoute
from modules.api_instance.application.update_route import UpdateRouteCommand
from modules.api_instance.application.get_apis import GetApis
from modules.api_instance.application.get_apis import GetApisQuery
from modules.api_instance.infrastructure import Repository
from modules.shared.infrastructure import CommandBus
from modules.shared.infrastructure import QueryBus

# Builder module
repository = Repository()
command_bus = CommandBus()
query_bus = QueryBus()
# use cases

# commands
command_bus.register(RegisterApiCommand, RegisterApi(repository))
command_bus.register(AddRouteCommand, AddRoute(repository))
command_bus.register(DeleteApiCommand, DeleteApi(repository))
command_bus.register(DeleteRouteCommand, DeleteRoute(repository))
command_bus.register(UpdateApiCommand, UpdateApi(repository))
command_bus.register(UpdateRouteCommand, UpdateRoute(repository))
command_bus.register(LaunchApiInstanceCommand, LaunchApiInstance(repository))
command_bus.register(StopApiInstanceCommand, StopApiInstance(repository))
# Queries
query_bus.register(SearchApiQuery, SearchApi(repository))
query_bus.register(GetApisQuery, GetApis(repository))
