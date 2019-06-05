from modules.api_instance.domain import ApiInstance
from modules.api_instance.domain import IRepository

from modules.shared.infrastructure import MongoConnection


class Repository(IRepository):
    __db = None
    __namne_repository = 'apis'

    def __init__(self) -> None:
        self.__db = MongoConnection.get_connection()
        self.__db = self.__db[self.__namne_repository]

    def save(self, api_instance: ApiInstance) -> None:
        api_instance_dict = {
            'port': api_instance.port.value,
            'routes': [],
            'settings': {
                'created_on': api_instance.settings.created_on,
                'enabled': api_instance.settings.enabled
            }
        }
        self.__db.insert(api_instance_dict)

    def search(self, api_id: str) -> ApiInstance:
        return super().search(api_id)

    def delete(self, api_id: str) -> None:
        super().delete(api_id)
