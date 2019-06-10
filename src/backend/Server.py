import os

from flask import Flask
from flask_cors import CORS
from backend.apis import api_v1


class Server:

    def __init__(self) -> None:
        self.flask_server = Flask('Server')
        CORS(self.flask_server)
        self.apis = [
            # TODO: Add new api versions
            api_v1
        ]

        self.register_apis()

    def register_apis(self):
        for api in self.apis:
            self.flask_server.register_blueprint(api)

    def run(self):
        self.flask_server.run('0.0.0.0', port=os.environ.get('PORT'))
