from flask import request
from flask_restplus import Namespace, Resource

from modules.api_instance import RegisterApiCommand
from modules.api_instance import command_bus

controller = Namespace('api', description='End points for created a api instance')


@controller.route('')
class ApiController(Resource):
    def post(self):
        return command_bus.execute(RegisterApiCommand(**request.get_json())), 200
