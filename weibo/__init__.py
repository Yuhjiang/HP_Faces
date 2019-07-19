import pymongo
from config.config import Mongodb_uri


db_client = pymongo.MongoClient(Mongodb_uri)
my_db = db_client['helloproject']