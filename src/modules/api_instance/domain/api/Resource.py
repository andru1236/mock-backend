from bson import ObjectId

from modules.api_instance.domain.api import Response
from modules.shared.domain import IEntity
from modules.shared.domain.errors import DomainBadRequestError


class Resource:

    def __init__(self, method: str, response: Response) -> None:
        self.method = method
        self.response = response

    def is_equals(self, resource):
        return resource.method == self.method and resource.response.value == self.response.value


class Path(IEntity):
    def __init__(self, path: str, resource: Resource, _id: str = str(ObjectId())) -> None:
        super().__init__(_id)
        self.path = path
        self.resources = []
        self.resources.append(resource)

    def add_response(self, new_resource: Resource):
        for resource in self.resources:
            if new_resource.is_equals(resource):
                raise DomainBadRequestError(f'Route {self.path} {new_resource.method} already exist')
        self.resources.append(new_resource)
