from flask import request
from flask import Flask
from flask_restx import Api
from flask_restx import Resource

from backend.api_instance.domain.ApiInstance import ApiInstance


def build_flask_server(api: ApiInstance):
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
