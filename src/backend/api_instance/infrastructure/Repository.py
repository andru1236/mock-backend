import os
from bson import ObjectId

from backend.api_instance.domain import (
    ApiInstance,
    IRepository,
    Param,
    Path,
    Paths,
    Port,
    Resource,
    Response,
    Settings,
)
from backend.shared.domain.errors import DomainBadRequestError, DomainDontFoundError
from backend.shared.infrastructure import MongoConnection, logger

COLLECTION_API=os.environ.get("COLLECTION_API") or "apis"

class Repository(IRepository):
    __db = None
    __name_repository = COLLECTION_API

    def __init__(self) -> None:
        self.__db = MongoConnection.get_connection()
        self.__db = self.__db[self.__name_repository]

    def save(self, api_instance: ApiInstance) -> None:
        api_instance_dict = api_instance.get_object_dict()
        del api_instance_dict["_id"]

        if api_instance._id is "":
            logger.info(f"A new API will be create in port {api_instance.port.value}")
            self.__db.insert(api_instance_dict)
        else:
            logger.info(f"The Api: {api_instance._id} will be updated")
            self.__db.update_one(
                {"_id": ObjectId(api_instance._id)}, {"$set": api_instance_dict}
            )

    def search(self, api_id: str) -> ApiInstance:
        api_dict = self.__db.find_one({"_id": ObjectId(api_id)})
        if api_dict is None:
            raise DomainDontFoundError(f"Not exist api instance {api_id}")

        paths = []
        for path_dict in api_dict["routes"]:
            resources = self._transform_resources_to_object(path_dict["resources"])
            paths.append(Path(path_dict["path"], resources, path_dict["_id"]))

        return ApiInstance(
            name=api_dict["name"],
            port=Port(api_dict["port"]),
            paths=Paths(paths),
            settings=Settings(
                api_dict["settings"]["enabled"],
                created_on=api_dict["settings"]["created_on"],
            ),
            _id=str(api_dict["_id"]),
        )

    def delete(self, api_id: str) -> None:
        logger.info(f"The Api: {api_id} will be deleted")
        delete_count = self.__db.delete_one({"_id": ObjectId(api_id)}).deleted_count
        if delete_count == 0:
            raise DomainBadRequestError(f"This api {api_id} not exist")

    def get_apis(self):
        logger.info(f"Get all apis")
        apis_cursor = self.__db.find()
        api_list = []
        for api in apis_cursor:
            api["_id"] = str(api["_id"])
            api_list.append(api)

        return {"apis": api_list}

    def _transform_resources_to_object(self, resources_json):
        resources = []
        for resource in resources_json:
            params = self._transform_params_to_object(resource.get("params"))

            resource_obj = Resource(
                resource["method"], Response(resource["response"]), params
            )
            resources.append(resource_obj)
        return resources

    def _transform_params_to_object(self, params_json):
        params = []
        if params_json is None:
            return params

        for param in params_json:
            param_obj = Param(param["param"], Response(param["response"]))
            params.append(param_obj)

        return params
