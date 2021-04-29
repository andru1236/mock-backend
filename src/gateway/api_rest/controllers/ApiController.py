from flask import request
from flask_restx import Namespace, Resource

from backend.api_instance import AddRouteCommand
from backend.api_instance import AddParamsCommand
from backend.api_instance import DeleteApiCommand
from backend.api_instance import DeleteRouteCommand
from backend.api_instance import DeleteParamsCommand
from backend.api_instance import GetApisQuery
from backend.api_instance import LaunchApiInstanceCommand
from backend.api_instance import RegisterApiCommand
from backend.api_instance import SearchApiQuery
from backend.api_instance import StopApiInstanceCommand
from backend.api_instance import UpdateApiCommand
from backend.api_instance import UpdateRouteCommand
from backend.api_instance import UpdateParamsCommand
from backend.api_instance import command_bus
from backend.api_instance import query_bus

from gateway.api_rest.controllers.decorators import return_with_custom_format

controller = Namespace('apis', description='End points for created a api instance')


@controller.route('')
class ApiController(Resource):
    @return_with_custom_format
    def post(self):
        return command_bus.execute(RegisterApiCommand(**request.get_json())), 201

    @return_with_custom_format
    def get(self):
        return query_bus.execute(GetApisQuery()), 200


@controller.route('/<api_id>')
class ApiSearcherController(Resource):

    @return_with_custom_format
    def get(self, api_id):
        return query_bus.execute(SearchApiQuery(api_id)), 200

    @return_with_custom_format
    def put(self, api_id):
        body = request.get_json()
        return command_bus.execute(UpdateApiCommand(api_id, body['name'], body['port'])), 200

    @return_with_custom_format
    def delete(self, api_id):
        return command_bus.execute(DeleteApiCommand(api_id)), 200


@controller.route('/<api_id>/routes')
class RouteController(Resource):
    @return_with_custom_format
    def post(self, api_id):
        data = request.get_json()
        return command_bus.execute(AddRouteCommand(api_id, data['path'], data['method'], data['response'])), 201

    @return_with_custom_format
    def put(self, api_id):
        data = request.get_json()
        return command_bus.execute(UpdateRouteCommand(api_id, data['path'], data['method'], data['response'])), 200

    @return_with_custom_format
    def delete(self, api_id):
        data = request.get_json()
        return command_bus.execute(DeleteRouteCommand(api_id, data['path'], data['method'])), 200

@controller.route('/<api_id>/routes/<route_id>/params')
class ParamsController(Resource):
    @return_with_custom_format
    def post(self, api_id, route_id):
        return command_bus.execute(AddParamsCommand(api_id, route_id, **request.get_json())), 201

    @return_with_custom_format
    def put(self, api_id, route_id):
        return command_bus.execute(UpdateParamsCommand(api_id, route_id, **request.get_json())), 200

    @return_with_custom_format
    def delete(self, api_id, route_id):
        data = request.get_json()
        return command_bus.execute(DeleteParamsCommand(api_id, route_id, data['params'], data['method'])), 200


@controller.route('/<api_id>/start')
class StartController(Resource):
    @return_with_custom_format
    def post(self, api_id):
        return command_bus.execute(LaunchApiInstanceCommand(api_id)), 200


@controller.route('/<api_id>/stop')
class StopController(Resource):
    @return_with_custom_format
    def post(self, api_id):
        return command_bus.execute(StopApiInstanceCommand(api_id)), 200
