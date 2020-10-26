from modules.api_instance.domain.api import Response


class Param:
    def __init__(self, param: str, response: Response):
        self.param = param
        self.response = response.value
