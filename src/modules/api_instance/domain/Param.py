from .Response import Response


class Param:
    def __init__(self, param: str, response: Response):
        self.param = param
        self.response = response.value
