from aip import AipFace
from secret import SECRET_KEY
import pymongo
from config.config import Mongodb_uri

APP_ID = '14303012'
API_KEY = 't4GyIHmNULqO50d0RlvY86PV'
SECRET_KEY = SECRET_KEY

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
db_client = pymongo.MongoClient(Mongodb_uri)
my_db = db_client['helloproject']