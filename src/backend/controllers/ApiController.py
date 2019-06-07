from flask import request
from flask_restplus import Namespace, Resource

from modules.api_instance import AddRouteCommand
from modules.api_instance import RegisterApiCommand
from modules.api_instance import SearchApiQuery
from modules.api_instance import command_bus
from modules.api_instance import query_bus
from modules.api_instance.infrastructure import Repository

controller = Namespace('api', description='End points for created a api instance')


@controller.route('')
class ApiController(Resource):
    def post(self):
        return command_bus.execute(RegisterApiCommand(**request.get_json())), 201


@controller.route('/<api_id>')
class ApiSearcherController(Resource):
    def get(self, api_id):
        return query_bus.execute(SearchApiQuery(api_id))


@controller.route('/<api_id>/routers')
class RouteController(Resource):
    def post(self, api_id):
        data = request.get_json()
        return command_bus.execute(AddRouteCommand(api_id, data['path'], data['method'], data['response'])), 200


@controller.route('/<api_id>/start')
class StartController(Resource):
    def post(self, api_id):
        repo = Repository()
        api = repo.search(api_id)
        api.run_api()
        return 'success', 200
