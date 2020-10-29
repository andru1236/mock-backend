import multiprocessing
import os
from typing import List

from flask import request
from flask import Flask
from flask_restx import Api
from flask_restx import Resource

from modules.api_instance.domain.api import ApiInstance
from modules.api_instance.domain.builder_server import ServerRunnable
from modules.api_instance.domain.builder_server.errors import PortIsBusy
from modules.shared.infrastructure.utils import SingletonDecorator
from modules.api_instance.domain.builder_server.validator import Validator
from modules.api_instance.domain.builder_server.validator import CpuValidator
from modules.api_instance.domain.builder_server.validator import AvailabilityValidator


@SingletonDecorator
class BuilderServer:

    def __init__(self) -> None:
        self.instances_flask: List[ServerRunnable] = []
        self.validators: List[Validator] = [CpuValidator(), AvailabilityValidator()]

    def run_api(self, api):
        for validator in self.validators:
            validator.validate(self.instances_flask, api)

        flask_server = self.build_flask_server(api)

        def executor():
            flask_server.app.run('0.0.0.0', api.port.value)

        flask_process = multiprocessing.Process(target=executor)
        self.instances_flask.append(ServerRunnable(api._id, flask_process, api.port.value))
        try:
            flask_process.start()
        except Exception:
            print("logger error")

    def stop_api(self, api_id):
        position_process_for_remove = -1
        for index, api in enumerate(self.instances_flask):
            if api._id == api_id:
                position_process_for_remove = index
                api.stop_server()
                del api
                break
        del self.instances_flask[position_process_for_remove]

    def build_flask_server(self, api: ApiInstance):
        flask_tenant = Flask(api._id)
        api_tenant = Api(flask_tenant)

        def factory_closure(resource):
            def closure(self):
                # Flask transform dict to json
                query = request.query_string.decode()
                response = resource.get_response(query)
                return response, 200

            return closure

        for path in api.get_list_paths():

            mock_class = type(path.path, (Resource, object), Resource.__dict__.copy())

            for resource in path.resources:
                setattr(mock_class, resource.method.lower(), factory_closure(resource))
            setattr(mock_class, 'methods', {'GET', 'POST', 'DELETE', 'PUT'})
            api_tenant.add_resource(mock_class, path.path)
        return api_tenant
