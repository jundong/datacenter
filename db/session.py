import logging
import threading
from types import LockType, List
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import settings
from db.base import DatabaseManager, PyObjectId

logger = logging.getLogger(__name__)


class MongoDBManager(DatabaseManager):
    _instance_lock: LockType = threading.Lock()
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    # 是用单例模式实现连接数据库对象的唯一性
    def __new__(cls, *args, **kwargs):
        if not hasattr(MongoDBManager, "_instance"):
            with MongoDBManager._instance_lock:
                if not hasattr(MongoDBManager, "_instance"):
                    MongoDBManager._instance = object.__new__(cls)
        return MongoDBManager._instance

    async def connect_to_database(self):
        logger.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(
            settings.MONGO_DATABASE_URI,
            maxPoolSize=10,
            minPoolSize=10)
        self.db = getattr(self.client, settings.MONGO_DATABASE)
        logger.info("Connected to MongoDB.")

    async def close_database_connection(self):
        logger.info("Closing connection with MongoDB.")
        self.client.close()
        logger.info("Closed connection with MongoDB.")

    async def get_items(self, collection, model: BaseModel) -> List[BaseModel]:
        if hasattr(self.db, collection):
            collection = getattr(self.db, collection)
        else:
            return []
        item_list = []
        item_query = collection.find()
        async for item in item_query:
            item_list.append(model(**item, id=item['_id']))
        return item_list

    async def get_item(self, collection, id: PyObjectId, model: BaseModel) -> BaseModel:
        if hasattr(self.db, collection):
            collection = getattr(self.db, collection)    
        item = await collection.find_one({'_id': PyObjectId(id)})
        if item:
            return model(**item, id=item['_id'])
    
    async def create_item(self, collection, model: BaseModel):
        if hasattr(self.db, collection):
            collection = getattr(self.db, collection)          
        await collection.insert_one(model.dict(exclude={'id'}))
    
    async def update_item(self, collection, id: PyObjectId, model: BaseModel):
        if hasattr(self.db, collection):
            collection = getattr(self.db, collection)           
        await collection.update_one({'_id': PyObjectId(id)},
                                       {'$set': model.dict(exclude={'id'})})

    async def delete_item(self, id: PyObjectId):
        if hasattr(self.db, collection):
            collection = getattr(self.db, collection)          
        await collection.delete_one({'_id': PyObjectId(id)})