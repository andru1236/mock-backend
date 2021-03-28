import multiprocessing

from flask import request
from flask import Flask
from flask_restx import Api
from flask_restx import Resource


# TODO: breaking the Hexagonal architecture move to application layer
from modules.shared.infrastructure.process_manager import Process, ProcessManager

from .ApiInstance import ApiInstance


class BuilderServer:
    def run_api(self, api: ApiInstance):
        flask_server = self.build_flask_server(api)

        # The multiprocess should be builded here, other case is not possible serialize
        mult_proc_obj = multiprocessing.Process(
            target=flask_server.app.run, args=("0.0.0.0", api.port.value)
        )

        process = Process(
            api._id,
            api.port.value,
            [],
            mult_proc_obj,
            start_func=lambda: mult_proc_obj.start,
            stop_func=lambda: mult_proc_obj.terminate,
        )
        ProcessManager().run_process(process)

    def stop_api(self, api_id):
        ProcessManager().stop_process(api_id)

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
            setattr(mock_class, "methods", {"GET", "POST", "DELETE", "PUT"})
            api_tenant.add_resource(mock_class, path.path)
        return api_tenant
