from flask import request
from flask_restx import Namespace, Resource

from modules.api_instance import AddRouteCommand
from modules.api_instance import AddParamsCommand
from modules.api_instance import DeleteApiCommand
from modules.api_instance import DeleteRouteCommand
from modules.api_instance import GetApisQuery
from modules.api_instance import LaunchApiInstanceCommand
from modules.api_instance import RegisterApiCommand
from modules.api_instance import SearchApiQuery
from modules.api_instance import StopApiInstanceCommand
from modules.api_instance import UpdateApiCommand
from modules.api_instance import UpdateRouteCommand
from modules.api_instance import UpdateParamsCommand
from modules.api_instance import command_bus
from modules.api_instance import query_bus

from backend.controllers.decorators import end_point

controller = Namespace('apis', description='End points for created a api instance')


@controller.route('')
class ApiController(Resource):
    @end_point
    def post(self):
        return command_bus.execute(RegisterApiCommand(**request.get_json())), 201

    @end_point
    def get(self):
        return query_bus.execute(GetApisQuery()), 200


@controller.route('/<api_id>')
class ApiSearcherController(Resource):

    @end_point
    def get(self, api_id):
        return query_bus.execute(SearchApiQuery(api_id)), 200

    @end_point
    def put(self, api_id):
        body = request.get_json()
        return command_bus.execute(UpdateApiCommand(api_id, body['name'], body['port'])), 200

    @end_point
    def delete(self, api_id):
        return command_bus.execute(DeleteApiCommand(api_id)), 200


@controller.route('/<api_id>/routes')
class RouteController(Resource):
    @end_point
    def post(self, api_id):
        data = request.get_json()
        return command_bus.execute(AddRouteCommand(api_id, data['path'], data['method'], data['response'])), 201

    @end_point
    def put(self, api_id):
        data = request.get_json()
        return command_bus.execute(UpdateRouteCommand(api_id, data['path'], data['method'], data['response'])), 200

    @end_point
    def delete(self, api_id):
        data = request.get_json()
        return command_bus.execute(DeleteRouteCommand(api_id, data['path'], data['method'])), 200

@controller.route('/<api_id>/routes/<route_id>/params')
class ParamsController(Resource):
    @end_point
    def post(self, api_id, route_id):
        return command_bus.execute(AddParamsCommand(api_id, route_id, **request.get_json())), 201

    @end_point
    def put(self, api_id, route_id):
        return command_bus.execute(UpdateParamsCommand(api_id, route_id, **request.get_json())), 200

@controller.route('/<api_id>/start')
class StartController(Resource):
    @end_point
    def post(self, api_id):
        return command_bus.execute(LaunchApiInstanceCommand(api_id)), 200


@controller.route('/<api_id>/stop')
class StopController(Resource):
    @end_point
    def post(self, api_id):
        return command_bus.execute(StopApiInstanceCommand(api_id)), 200
