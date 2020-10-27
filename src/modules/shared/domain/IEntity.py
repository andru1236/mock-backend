from bson import ObjectId


class IEntity:

    def __init__(self, _id: str = None) -> None:
        self._id = str(ObjectId()) if _id is None else _id
