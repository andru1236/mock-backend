from modules.api_instance.domain.builder_server import MethodWithResponse


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