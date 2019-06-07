from flask import request
from flask_restplus import Namespace, Resource

from modules.api_instance import AddRouteCommand
from modules.api_instance import RegisterApiCommand
from modules.api_instance import command_bus
from modules.api_instance.infrastructure import Repository

controller = Namespace('api', description='End points for created a api instance')


@controller.route('')
class ApiController(Resource):
    def post(self):
        return command_bus.execute(RegisterApiCommand(**request.get_json())), 201


@controller.route('/<id>/routers')
class RouteController(Resource):
    def post(self, id):
        data = request.get_json()
        return command_bus.execute(AddRouteCommand(id, data['path'], data['method'], data['response'])), 200


@controller.route('/start')
class StartController(Resource):
    def post(self, id):
        repo = Repository()
        api = repo.search(id)
        api.run_api()
        return 'success', 200
