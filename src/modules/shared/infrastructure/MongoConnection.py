import os

from pymongo import MongoClient

from modules.shared.domain import IPersistenceConnection


class MongoConnection(IPersistenceConnection):
    __db = None

    @classmethod
    def get_connection(cls):
        if cls.__db is None:
            mongo_link = MongoClient(str(os.environ.get('MONGO_CONNECTION')))
            cls.__db = mongo_link[str(os.environ.get('MONGO_DB'))]
        return cls.__db

    @classmethod
    def restart_data_base(cls):
        mongo_link = MongoClient(str(os.environ.get('MONGO_CONNECTION')))
        mongo_link.drop_database(str(os.environ.get('MONGO_DB')))
