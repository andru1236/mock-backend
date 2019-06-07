from flask import request
from flask_restplus import Namespace, Resource

from modules.api_instance import AddRouteCommand
from modules.api_instance import DeleteApiCommand
from modules.api_instance import LaunchApiInstanceCommand
from modules.api_instance import RegisterApiCommand
from modules.api_instance import SearchApiQuery
from modules.api_instance import StopApiInstanceCommand
from modules.api_instance import UpdateApiCommand
from modules.api_instance import command_bus
from modules.api_instance import query_bus

controller = Namespace('api', description='End points for created a api instance')


@controller.route('')
class ApiController(Resource):
    def post(self):
        return command_bus.execute(RegisterApiCommand(**request.get_json())), 201


@controller.route('/<api_id>')
class ApiSearcherController(Resource):
    def get(self, api_id):
        return query_bus.execute(SearchApiQuery(api_id)), 200

    def put(self, api_id):
        body = request.get_json()
        command_bus.execute(UpdateApiCommand(api_id, body['port']))
        return 'sucess', 200

    def delete(self, api_id):
        command_bus.execute(DeleteApiCommand(api_id))
        return 'success', 200


@controller.route('/<api_id>/routers')
class RouteController(Resource):
    def post(self, api_id):
        data = request.get_json()
        return command_bus.execute(AddRouteCommand(api_id, data['path'], data['method'], data['response'])), 200


@controller.route('/<api_id>/start')
class StartController(Resource):
    def post(self, api_id):
        command_bus.execute(LaunchApiInstanceCommand(api_id))
        return 'success', 200


@controller.route('/<api_id>/stop')
class StopController(Resource):
    def post(self, api_id):
        command_bus.execute(StopApiInstanceCommand(api_id))
        return 'success', 200
