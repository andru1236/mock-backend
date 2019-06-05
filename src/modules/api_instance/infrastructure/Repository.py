from bson import ObjectId

from modules.api_instance.domain import ApiInstance
from modules.api_instance.domain import IRepository
from modules.api_instance.domain import Port
from modules.api_instance.domain import Response
from modules.api_instance.domain import Route
from modules.api_instance.domain import Settings
from modules.shared.domain.errors import DomainBadRequestError
from modules.shared.domain.errors import DomainDontFoundError

from modules.shared.infrastructure import MongoConnection


class Repository(IRepository):
    __db = None
    __name_repository = 'apis'

    def __init__(self) -> None:
        self.__db = MongoConnection.get_connection()
        self.__db = self.__db[self.__name_repository]

    def save(self, api_instance: ApiInstance) -> None:
        api_instance_dict = api_instance.get_object_dict()
        del api_instance_dict['_id']

        if api_instance._id is "":
            self.__db.insert(api_instance_dict)
        else:
            self.__db.update_one({'_id': ObjectId(api_instance._id)}, {
                '$set': api_instance_dict
            })

    def search(self, api_id: str) -> ApiInstance:
        api_dict = self.__db.find_one({'_id': ObjectId(api_id)})
        if api_dict is None:
            raise DomainDontFoundError(f'Not exist api instance {api_id}')

        return ApiInstance(
            port=Port(api_dict['port']),
            routes=[
                Route(
                    path=dict_route['path'],
                    method=dict_route['method'],
                    response=Response(dict_route['response']),
                    _id=str(dict_route['_id'])
                )
                for dict_route in api_dict['routes']
            ],
            settings=Settings(api_dict['settings']['enabled'], created_on=api_dict['settings']['created_on']),
            _id=str(api_dict['_id'])
        )

    def delete(self, api_id: str) -> None:
        delete_count = self.__db.delete_one({'_id': ObjectId(api_id)}).deleted_count
        if delete_count == 0:
            raise DomainBadRequestError(f'This api {api_id} not exist')
