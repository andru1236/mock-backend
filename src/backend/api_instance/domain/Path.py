from typing import List

from backend.shared.domain import IEntity
from backend.shared.domain.errors import DomainBadRequestError

from .Resource import Resource

class Path(IEntity):
    def __init__(self, path: str, resources: List[Resource] = None, _id: str = None) -> None:
        super().__init__(_id)
        self.path = path
        self.resources = [] if resources is None else resources

    def add_resource(self, new_resource: Resource):
        for resource in self.resources:
            if resource.is_equals(new_resource):
                raise DomainBadRequestError(f'this resource {new_resource.method} already exist in {self.path}')
        self.resources.append(new_resource)

    def remove_resource(self, resource_will_be_removed: Resource):
        removed = False
        for index, resource in enumerate(self.resources):
            if resource.is_equals(resource_will_be_removed):
                del self.resources[index]
                removed = True
                break

        if removed is False:
            raise DomainBadRequestError(f'This method {resource_will_be_removed.method} not exist in {self.path}')

    def update_resource(self, new_resource: Resource):
        found = False
        for index, resource in enumerate(self.resources):
            if resource.is_equals(new_resource):
                self.resources[index].response = new_resource.response
                found = True
                break

        if found is False:
            raise DomainBadRequestError(f'This method {new_resource.method} not exist in {self.path}')

    def get_object_dict(self):
        return {
            '_id': self._id,
            'path': self.path,
            'resources': [resource.get_object_dict() for resource in self.resources]
        }

    def get_resource_by_method(self, method: str):
        for index, resource in enumerate(self.resources):
            if resource.method == method:
                return self.resources[index]
        raise DomainBadRequestError(f'This method {method} not exist')
