from flask import request
from flask_restx import Namespace, Resource

from backend.response import (
    command_bus, 
    query_bus,
    get_responses,
    create_api_response,
    search_a_response,
    update_api_response,
    remove_response,
    assign_response_to_api
)


from .decorators import return_with_custom_format


controller = Namespace('responses', description='End points for response feature')


@controller.route('')
class ResponseRootController(Resource):
    @return_with_custom_format
    def get(self):
        list_of_responses = query_bus.execute(get_responses.GetResponsesQuery(50))
        return {'responses': list_of_responses} , 200

    @return_with_custom_format
    def post(self):
        return command_bus.execute(create_api_response.CreateApiResponseCommand(**request.get_json())), 201


@controller.route('/<response_id>')
class ResponseController(Resource):
    @return_with_custom_format
    def get(self, response_id):
        return query_bus.execute(search_a_response.SearchAResponseQuery(response_id)), 200

    @return_with_custom_format
    def put(self, response_id):
        body = request.get_json()
        body.update({'response_id': response_id})
        return command_bus.execute(update_api_response.UpdateApiResponseCommand(**body)), 200

    @return_with_custom_format
    def delete(self, response_id):
        return command_bus.execute(remove_response.RemoveResponseCommand(response_id)), 200

    @return_with_custom_format
    def post(self, response_id):
        body = request.get_json()
        body.update({'response_id': response_id})
        return command_bus.execute(assign_response_to_api.AssignReponseToAPICommand(**body)), 200

