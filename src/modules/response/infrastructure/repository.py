from dataclasses import asdict
from bson import ObjectId

from modules.response import domain
from modules.shared.domain.errors import DomainDontFoundError, DomainBadRequestError
from modules.shared.infrastructure.MongoConnection import MongoConnection


NAME_DB_COLLECTION = 'responses'

db = MongoConnection.get_connection()
db = db[NAME_DB_COLLECTION]

def _parse_id_to_str(mongo_result):
    mongo_result['_id'] = str(mongo_result['_id'])
    return mongo_result


def save(response: domain.Response):
    response_dict = asdict(response)
    del response_dict['_id']

    if response._id is not None:
        db.update_one({'_id': ObjectId(response._id)}, {
            '$set': response_dict
        })
        return True
    
    db.insert(response_dict)

    return True


def delete(response_id: str):
    conunt_removed_items = db.delete_one({'_id': ObjectId(response_id)}).deleted_count
    if conunt_removed_items == 0:
        raise DomainBadRequestError(f'This response does not exists {response_id}')

def search(response_id: str):
    mongo_result = db.find_one({'_id': ObjectId(response_id)})
    if mongo_result is None:
        raise DomainDontFoundError('The response does not exists')
    _parse_id_to_str(mongo_result)
    return domain.Response(**mongo_result)

def search_all(limit):
    responses = db.find().limit(limit)
    return list(map(_parse_id_to_str,responses))

    


