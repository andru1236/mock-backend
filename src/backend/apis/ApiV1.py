from flask import Blueprint
from flask_restplus import Api

from backend.controllers import api_instance_controller


class ApiV1:

    def __init__(self) -> None:
        self.app = Blueprint('api_v1', __name__, url_prefix='/api/v1')
        self.api = Api(self.app)

        self.controllers = [
            # TODO: Add controlers to app
            api_instance_controller
        ]

        self.build_controllers()

    def build_controllers(self):
        for controller in self.controllers:
            self.api.add_namespace(controller)
