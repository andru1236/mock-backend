# Features
from .application import (
    create_api_response,
    update_api_response,
    remove_response,
    get_responses,
    search_a_response,
    assign_response_to_api,
)

# repository
from .infrastructure import repository

# integration to other backend
from .infrastructure.integration_services import ApiServiceBus

# bus of communications
from backend.shared.infrastructure import CommandBus, QueryBus


# module entry point
command_bus = CommandBus()
query_bus = QueryBus()

command_bus.register(
    create_api_response.CreateApiResponseCommand,
    create_api_response.CreateApiResponse(repository),
)
command_bus.register(
    update_api_response.UpdateApiResponseCommand,
    update_api_response.UpdateApiResponse(repository),
)
command_bus.register(
    remove_response.RemoveResponseCommand, remove_response.RemoveResponse(repository)
)

# communication with api instance module
command_bus.register(
    assign_response_to_api.AssignReponseToAPICommand,
    assign_response_to_api.AssignResponseToAPI(repository, ApiServiceBus()),
)

query_bus.register(
    get_responses.GetResponsesQuery, get_responses.GetResponses(repository)
)
query_bus.register(
    search_a_response.SearchAResponseQuery,
    search_a_response.SearchAResponse(repository),
)
