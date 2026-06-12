from dotenv import load_dotenv
import os
from threading import Lock

from pymongo import MongoClient

load_dotenv()


class MongoDBSingleton:
    _instance = None
    _lock = Lock()
    _client = None
    _db = None

    def __new__(cls):
        return cls.get_instance()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._connect()
        return cls._instance

    def _connect(self):
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            raise RuntimeError("MONGO_URI is missing from .env")

        self._client = MongoClient(mongo_uri)
        self._db = self._client["varsity_management"]

    @property
    def client(self):
        return self._client

    @property
    def db(self):
        return self._db

    def get_collection(self, collection_name: str):
        return self._db[collection_name]

    def close(self):
        if self._client:
            self._client.close()


mongodb = MongoDBSingleton.get_instance()
client = mongodb.client
db = mongodb.db
