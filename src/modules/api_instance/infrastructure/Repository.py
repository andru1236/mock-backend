from bson import ObjectId

from modules.api_instance.domain import ApiInstance
from modules.api_instance.domain import IRepository

from modules.shared.infrastructure import MongoConnection


class Repository(IRepository):
    __db = None
    __name_repository = 'apis'

    def __init__(self) -> None:
        self.__db = MongoConnection.get_connection()
        self.__db = self.__db[self.__name_repository]

    def save(self, api_instance: ApiInstance) -> None:
        api_instance_dict = api_instance.get_object_dict()

        if api_instance._id is "":
            del api_instance._id
            self.__db.insert(api_instance_dict)
        else:
            del api_instance_dict['_id']
            self.__db.update_one({'_id': ObjectId(api_instance._id)}, {
                '$set': api_instance_dict
            })

    def search(self, api_id: str) -> ApiInstance:
        return super().search(api_id)

    def delete(self, api_id: str) -> None:
        super().delete(api_id)
