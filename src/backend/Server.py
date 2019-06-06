import os

from flask import Flask

from backend.apis import api_v1


class Server:

    def __init__(self) -> None:
        self.flask_server = Flask('Server')
        self.apis = [
            # TODO: Add new api versions
            api_v1
        ]

        self.register_apis()

    def register_apis(self):
        for api in self.apis:
            self.flask_server.register_blueprint(api)

    def run(self):
        environment = os.environ.get('ENV')
        if environment == 'DEV':
            self.flask_server.run(debug=True, host='0.0.0.0')
        elif enumerate == 'PROD':
            # TODO: Implement rules for run in production
            self.flask_server.run()
