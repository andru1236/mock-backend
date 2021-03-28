import os

from dataclasses import asdict

from bson.objectid import ObjectId
from modules.device_snmp.domain import Device
from modules.shared.infrastructure import logger, MongoConnection
from modules.shared.domain import errors

COLLECTION_DEVICE = os.environ.get("COLLECTION_DEVICE") or "devices"

db = MongoConnection.get_connection()
db = db[COLLECTION_DEVICE]


def _parse_id_to_str(mongo_result):
    mongo_result["_id"] = str(mongo_result["_id"])
    return mongo_result


def save(device: Device):
    device_dict = asdict(device)
    del device_dict["_id"]

    if device._id is None:
        logger.info(f"Registering new device")
        db.insert(device_dict)
        return True
    logger.info(f"Updating the device: {device._id}")
    db.update_one({"_id": ObjectId(device._id)}, {"$set": device_dict})    
    return True


def search(device_id: str):
    logger.info(f"Searching the device: {device_id}")
    device_dict = db.find_one({"_id": ObjectId(device_id)})
    if device_dict is None:
        raise errors.DomainDontFoundError(f"The device:{device_id} does not exists")
    _parse_id_to_str(device_dict)
    return Device(**device_dict)
