import multiprocessing

from flask import Flask
from flask_restplus import Api
from flask_restplus import Resource

from modules.api_instance.domain.builder_server import MethodWithResponse
from modules.api_instance.domain.builder_server import RouteUnifyByPath
from modules.api_instance.domain.builder_server import ServerRunnable
from modules.shared.infrastructure.utils import SingletonDecorator


@SingletonDecorator
class BuilderServer:

    def __init__(self) -> None:
        self.flask_runnables = []

    def run_api(self, api):
        flask_server = self.build_flask_server(api)

        def executor():
            flask_server.app.run('0.0.0.0', api.port.value)

        flask_process = multiprocessing.Process(target=executor)

        self.flask_runnables.append(ServerRunnable(api._id, flask_process))
        try:
            flask_process.start()
        except Exception:
            print("logger error")

    def stop_api(self, api_id):
        position_process_for_remove = -1
        for index, api in enumerate(self.flask_runnables):
            if api._id == api_id:
                position_process_for_remove = index
                api.stop_server()
                del api
                break
        del self.flask_runnables[position_process_for_remove]

    def build_flask_server(self, api):
        flask_tenant = Flask(api._id)
        api_tenant = Api(flask_tenant)
        routes = self.sorted_routes_by_path(api.routes)

        def factory_closure(response):
            def closure(self):
                # Flask transform dict to json
                return response, 200

            return closure

        for route in routes:
            # Create dynamic class
            # flask rest-plus need classes for create routes that's run with inheritance class
            mock_class = type(route.path, (Resource, object), Resource.__dict__.copy())
            for resource in route.resources:
                setattr(mock_class, resource.method.lower(), factory_closure(resource.response))
            api_tenant.add_resource(mock_class, route.path)
        return api_tenant

    # TODO: change logic of routes, this work but change the logic business
    def sorted_routes_by_path(self, routes):
        routes_by_path = []
        for route in routes:
            if len(routes_by_path) == 0:
                routes_by_path.append(RouteUnifyByPath(route.path, MethodWithResponse(route.method, route.response)))
            else:
                for index, route_by_path in enumerate(routes_by_path):
                    if route.path == route_by_path.path:
                        try:
                            route_by_path.add_resouce(MethodWithResponse(route.method, route.response))
                        except Exception as error:
                            pass
                    elif len(routes_by_path) - 1 == index:
                        routes_by_path.append(
                            RouteUnifyByPath(route.path, MethodWithResponse(route.method, route.response))
                        )
        return routes_by_path
