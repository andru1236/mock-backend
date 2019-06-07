import ast
import threading

from flask import Flask
from flask_restplus import Api
from flask_restplus import Resource

from modules.shared.infrastructure.utils import SingletonDecorator


class MethodWithResponse:

    def __init__(self, method: str, response: str) -> None:
        self.method = method
        self.response = response


class RouteUnifyByPath:

    def __init__(self, path: str, resource: MethodWithResponse) -> None:
        self.path = path
        self.resources = []
        self.resources.append(resource)

    def add_resouce(self, new_resource: MethodWithResponse):
        for resource in self.resources:
            if resource.method == new_resource.method:
                raise Exception('This method is already registered')
            self.resources.append(new_resource)


class ServerRunneable:

    def __init__(self, _id: str, thread) -> None:
        self._id = _id
        self.thread = thread


@SingletonDecorator
class BuilderServer:

    def __init__(self) -> None:
        self.threads = []

    def run_api(self, api):
        flask_server = self.build_flask_server(api)

        def executor():
            flask_server.app.run('0.0.0.0', api.port.value)

        thread_flask = threading.Thread(target=executor)
        # self.threads.append(ServerRunneable(api._id, thread_flask))
        try:
            thread_flask.start()
        except Exception:
            print("ALGO")

    def stop_api(self, api_id):
        for api in self.threads:
            if api._id == api_id:
                api.thread.stop()

    def build_flask_server(self, api):
        flask_tenant = Flask(api._id)
        api_tenant = Api(flask_tenant)
        routes = self.sordted_routes_by_path(api.routes)

        def factory_closure(response):
            def closure(self):
                return response, 200
            return closure

        for route in routes:
            # Create dynamic class
            # flask rest-plus run with inheritance class
            mock_class = type(route.path, (Resource, object), Resource.__dict__.copy())
            for resource in route.resources:
                setattr(mock_class, resource.method.lower(), factory_closure(resource.response))
            api_tenant.add_resource(mock_class, route.path)
        return api_tenant
        # api_tenant.app.run('0.0.0.0', api.port.value)

    def sordted_routes_by_path(self, routes):
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


