from typing import List

from bson import ObjectId

from modules.api_instance.domain import ApiInstance
from modules.api_instance.domain import IRepository
from modules.api_instance.domain import Route

from modules.shared.infrastructure import MongoConnection


class Repository(IRepository):
    __db = None
    __name_repository = 'apis'

    def __init__(self) -> None:
        self.__db = MongoConnection.get_connection()
        self.__db = self.__db[self.__name_repository]

    def save(self, api_instance: ApiInstance) -> None:
        api_instance_dict = {
            'port': api_instance.port.value,
            'routes': self.__convert_routes_to_dict(api_instance.routes),
            'settings': {
                'created_on': api_instance.settings.created_on,
                'enabled': api_instance.settings.enabled
            }
        }

        if api_instance._id is "":
            self.__db.insert(api_instance_dict)
        else:
            self.__db.update_one({'_id': ObjectId(api_instance._id)}, {
                '$set': api_instance_dict
            })

    def search(self, api_id: str) -> ApiInstance:
        return super().search(api_id)

    def delete(self, api_id: str) -> None:
        super().delete(api_id)

    def __convert_routes_to_dict(self, routes: List[Route]):
        if routes is None:
            return []

        return list(map(lambda route: route.get_dict_object(), routes))
