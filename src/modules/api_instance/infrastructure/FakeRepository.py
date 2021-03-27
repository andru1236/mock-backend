from typing import List

from bson import ObjectId

from modules.api_instance.domain import ApiInstance, IRepository
from modules.shared.domain.errors import DomainDontFoundError


class FakeRepository(IRepository):
    def __init__(self) -> None:
        self.apis: List[ApiInstance] = []

    def save(self, api_instance: ApiInstance) -> None:
        if api_instance._id == "":
            api_instance._id = str(ObjectId())
            self.apis.append(api_instance)
        else:
            for api in self.apis:
                if api._id == api_instance._id:
                    api.name = api_instance.name
                    api.paths = api_instance.paths
                    api.port = api_instance.port
                    api.settings = api_instance.settings

    def search(self, api_id: str) -> ApiInstance:
        found_api = None
        for api in self.apis:
            if api._id == api_id:
                found_api = api
                break
        return (
            found_api
            if found_api is not None
            else DomainDontFoundError(f"This api {api_id} not exist")
        )

    def delete(self, api_id: str) -> None:
        self.apis = list(filter(lambda api: api._id != api_id, self.apis))
