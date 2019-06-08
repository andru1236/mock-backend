from modules.api_instance.domain.api import Response


class Resource:
    def __init__(self, method: str, response: Response) -> None:
        self.method = method
        self.response = response.value

    def is_equals(self, resource):
        return self.method == resource.method
