from flask import request
from flask_restplus import Namespace, Resource

controller = Namespace('api_instances', description='End points for created a api instance')


@controller.route('')
class ApiInstanceController(Resource):
    def post(self):
        data_post = request.get_json()
        print(data_post)
        return 'success', 200
