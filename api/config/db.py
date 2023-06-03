from pymongo import MongoClient
from config import MONGO_CONN_STR

db_connection = MongoClient("mongodb://localhost:27017")
