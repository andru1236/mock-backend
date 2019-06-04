from modules.mock_api.domain import Port


class ApiInstance:

    def __init__(self, port: Port, routes=None) -> None:
        self.port = port
        self.routes = routes
