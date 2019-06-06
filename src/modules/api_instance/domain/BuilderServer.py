from flask import Flask
from flask_restplus import Api
from flask_restplus import Resource

from modules.api_instance.domain import ApiInstance


class GenericRoute(Resource): pass


class BuilderServer:
    # Singleton pattern
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(BuilderServer, cls)
        return cls.__instance

    def __init__(self) -> None:
        self.threads = []

    def run_api(self, api: ApiInstance):
        flask_tenant = Flask(api._id)
        api_tenant = Api(flask_tenant)
        mock_class = type(, (Resource, object), Resource.__dict__.copy())

