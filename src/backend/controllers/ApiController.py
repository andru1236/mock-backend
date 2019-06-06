from flask import request
from flask_restplus import Namespace, Resource

controller = Namespace('api', description='End points for created a api instance')


@controller.route('')
class ApiController(Resource):
    def post(self):
        data_post = request.get_json()
        print(data_post)
        return 'success', 200
