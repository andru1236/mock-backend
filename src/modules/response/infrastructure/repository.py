import os
from dataclasses import asdict
from bson import ObjectId

from modules.response import domain
from modules.shared.domain.errors import DomainDontFoundError, DomainBadRequestError
from modules.shared.infrastructure.MongoConnection import MongoConnection
from modules.shared.infrastructure import logger


COLLECTION_RESPONSE = os.environ.get("COLLECTION_RESPONSE") or "responses"

db = MongoConnection.get_connection()
db = db[COLLECTION_RESPONSE]


def _parse_id_to_str(mongo_result):
    mongo_result["_id"] = str(mongo_result["_id"])
    return mongo_result


def save(response: domain.Response):
    response_dict = asdict(response)
    logger.info(f"Response [{response._id}] will be stored in database")
    del response_dict["_id"]

    if response._id is not None:
        db.update_one({"_id": ObjectId(response._id)}, {"$set": response_dict})
        return True

    db.insert(response_dict)

    return True


def delete(response_id: str):
    conunt_removed_items = db.delete_one({"_id": ObjectId(response_id)}).deleted_count
    if conunt_removed_items == 0:
        raise DomainBadRequestError(f"This response does not exists {response_id}")
    logger.info(f"Response {response_id} will be removed")


def search(response_id: str):
    mongo_result = db.find_one({"_id": ObjectId(response_id)})
    if mongo_result is None:
        raise DomainDontFoundError("The response does not exists")
    _parse_id_to_str(mongo_result)
    logger.info(f"search Response: [{response_id}]  from database")
    return domain.Response(**mongo_result)


def search_all(limit):
    logger.info(f"search {limit} responses from database")
    responses = db.find().limit(limit)
    return list(map(_parse_id_to_str, responses))
