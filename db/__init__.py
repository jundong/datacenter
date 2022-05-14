from db.session import MongoDBManager
from db.init_db import init_db

mongo_db = MongoDBManager()
init_db()