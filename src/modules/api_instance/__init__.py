# Features
from modules.api_instance.application.add_route import AddRoute, AddRouteCommand
from modules.api_instance.application.add_params import AddParams, AddParamsCommand
from modules.api_instance.application.update_params import UpdateParams, UpdateParamsCommand
from modules.api_instance.application.delete_params import DeleteParams, DeleteParamsCommand
from modules.api_instance.application.delete_api import DeleteApi, DeleteApiCommand
from modules.api_instance.application.delete_route import DeleteRoute, DeleteRouteCommand
from modules.api_instance.application.launch_api_instance import LaunchApiInstance, LaunchApiInstanceCommand
from modules.api_instance.application.register_api import RegisterApi, RegisterApiCommand
from modules.api_instance.application.search_api import SearchApi, SearchApiQuery
from modules.api_instance.application.stop_api_instance import StopApiInstance, StopApiInstanceCommand
from modules.api_instance.application.update_api import UpdateApi, UpdateApiCommand
from modules.api_instance.application.update_route import UpdateRoute, UpdateRouteCommand
from modules.api_instance.application.get_apis import GetApis, GetApisQuery

from modules.shared.infrastructure import CommandBus, QueryBus

from modules.api_instance.infrastructure import Repository

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
command_bus.register(AddParamsCommand, AddParams(repository))
command_bus.register(UpdateParamsCommand, UpdateParams(repository))
command_bus.register(DeleteParamsCommand, DeleteParams(repository))
# Queries
query_bus.register(SearchApiQuery, SearchApi(repository))
query_bus.register(GetApisQuery, GetApis(repository))
